#!/usr/bin/env python3
"""Split the muscle records into extraction files, and put them back together.

The migration described in `docs/MIGRATION.md` inverts where an observation
lives. Today it sits inside the homology group it was assigned to, which is why
"is this source fully mined?" cannot be asked of the data — the paper is not a
unit the schema knows about. Afterwards it sits in a file named for the animal
and the study, and the homology group is a mapping applied on top.

This script does both directions:

    python3 scripts/build_observations.py --split    muscles-*.json -> observations/ + mapping/
                                                    ONE-TIME MIGRATION. Needs --force now,
                                                    because it overwrites the source of truth
                                                    from a file generated out of it.
    python3 scripts/build_observations.py --join     observations/ + mapping/ -> muscles-*.json
    python3 scripts/build_observations.py --check    split, join, and diff against the original

`--check` is read-only and safe to run any time: it joins the committed
observations into a scratch directory and diffs. It proves the two halves still
reconstruct the muscle files exactly. It proves nothing whatever about
*completeness* — a file marked `"status": "scaffolded"` is the previous pass's
extraction in a new shape, which nobody has checked against the paper.

The extraction key is (species, source, name, region). `validate.py` errors if
that ever resolves to two records; see Task 1 in `docs/MIGRATION.md`.
"""
import collections
import glob
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OBS = ROOT / "data/observations"
MAP = ROOT / "data/mapping"

# Everything on an occurrence belongs to the observation EXCEPT these two, which
# the join reconstructs: `species` from the filename, `sources` from which file
# the row is in. Taking the complement rather than a whitelist is deliberate — a
# whitelist silently drops any field added later, and this script's whole purpose
# is to prove nothing is dropped.
OCC_DROP = {"species", "sources"}


def muscle_files():
    return sorted(glob.glob(str(ROOT / "data/muscles-*.json")))


def split():
    """muscles-*.json -> one file per (species, source), plus a mapping per source."""
    obs = collections.defaultdict(list)      # (species, source) -> [row]
    mapping = collections.defaultdict(dict)  # source -> "name|region" -> record

    for path in muscle_files():
        doc = json.load(open(path))
        for m in doc["muscles"]:
            for idx, occ in enumerate(m.get("occurrences") or []):
                sp = occ.get("species")
                for src in (occ.get("sources") or ["(unsourced)"]):
                    row = {k: v for k, v in occ.items() if k not in OCC_DROP}
                    row["region"] = m.get("region")
                    # Provenance the join needs, and a human needs to audit by eye.
                    row["record"] = m["id"]
                    # The occurrence's position in its record. An occurrence with
                    # several sources becomes one row per source, and this is what
                    # merges them back into one and keeps the original order --
                    # without it the join reorders occurrences and the round trip
                    # cannot be compared field by field.
                    row["_occ"] = idx
                    # The occurrence's original key order, so the join can rebuild
                    # it byte-for-byte. build.sh is a fixed point and CI fails if
                    # the committed data moves, so "same content, different field
                    # order" is not good enough.
                    row["_keys"] = list(occ.keys())
                    # And the original order of `sources`. The join reads the
                    # observation files alphabetically, so without this a
                    # two-source occurrence comes back with its citations swapped.
                    row["_srcs"] = list(occ.get("sources") or [])
                    obs[(sp, src)].append(row)
                    nm = (occ.get("name") or "").strip().lower()
                    if nm:
                        mapping[src][f"{nm}|{m.get('region')}"] = m["id"]

    # The parked layer joins the same store. A row with `record: null` is an
    # observation nobody has assigned to a homology group yet; a row with a
    # record is one that has been. Keeping them in two places was an artefact of
    # occurrences having to live inside a record -- there is no reason for it once
    # the file is keyed on the study and the animal.
    parked_path = ROOT / "data/observations.json"
    if parked_path.exists():
        for row in json.load(open(parked_path)).get("observations") or []:
            r = {k: v for k, v in row.items() if k not in ("source", "species", "id")}
            r["record"] = None
            r["_id"] = row["id"]
            obs[(row["species"], row["source"])].append(r)

    # Write in place and delete only what is stale. rmtree-then-recreate makes
    # a file-syncing client (this repo lives in Dropbox) treat 248 rewritten
    # files as 248 conflicts, and it produced a "conflicted copy" of every one.
    OBS.mkdir(parents=True, exist_ok=True)
    MAP.mkdir(parents=True, exist_ok=True)
    keep_obs, keep_map = set(), set()

    status_by = {k: v.get("status", "not-started") for k, v in
                 (json.load(open(ROOT / "data/remine-status.json")).get("sources") or {}).items()}

    for (sp, src), rows in sorted(obs.items()):
        rows.sort(key=lambda r: (r.get("region") or "", (r.get("name") or "").lower(),
                                 r.get("record") or "~", r.get("_occ", -1)))
        doc = {
            "species": sp,
            "source": src,
            "status": status_by.get(src, "scaffolded"),
            "$comment": ("What this study says about this animal. `record` names the "
                         "homology group a row has been assigned to; null means nobody has "
                         "assigned it yet, and `blockedBy` says what is missing. `status` "
                         "mirrors data/remine-status.json: `scaffolded` means these rows "
                         "came out of the old storage and NOBODY HAS CHECKED THEM AGAINST "
                         "THE PAPER."),
            "observations": rows,
        }
        out = OBS / f"{sp}__{src}.json"
        keep_obs.add(out.name)
        text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        if not out.exists() or out.read_text() != text:
            out.write_text(text)

    for src, table in sorted(mapping.items()):
        doc = {
            "source": src,
            "$comment": ("GENERATED. Which muscle record each of this source's names "
                         "belongs to, keyed 'name|region'. Per source deliberately: two "
                         "authors assigning one muscle to different groups is the thing "
                         "this dataset exists to preserve, and a global name table would "
                         "destroy it."),
            "mapping": dict(sorted(table.items())),
        }
        out = MAP / f"{src}.json"
        keep_map.add(out.name)
        text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        if not out.exists() or out.read_text() != text:
            out.write_text(text)

    for d, keep in ((OBS, keep_obs), (MAP, keep_map)):
        for f in d.glob("*.json"):
            if f.name not in keep:
                f.unlink()
    return len(obs), len(mapping), sum(len(v) for v in obs.values())


def join(into):
    """observations/ + mapping/ -> muscle occurrences, written into `into`."""
    by_record = collections.defaultdict(list)   # record -> [(species, source, row)]
    for f in sorted(OBS.glob("*.json")):
        doc = json.load(open(f))
        for row in doc["observations"]:
            if not row.get("record"):
                continue          # not assigned to a homology group yet
            by_record[row["record"]].append((doc["species"], doc["source"], row))

    for path in muscle_files():
        doc = json.load(open(path))
        for m in doc["muscles"]:
            rebuilt = {}                          # original index -> occurrence
            for sp, src, row in by_record.get(m["id"], []):
                key = row["_occ"]
                occ = rebuilt.get(key)
                if occ is None:
                    occ = {}
                    for k in row["_keys"]:
                        if k == "species":
                            occ["species"] = sp
                        elif k == "sources":
                            occ["sources"] = []
                        elif k in row:
                            occ[k] = row[k]
                    occ.setdefault("sources", [])
                    rebuilt[key] = occ
                if src != "(unsourced)" and src not in occ["sources"]:
                    occ["sources"].append(src)
                    # Restore the order the record had, not the order the files
                    # happen to be read in.
                    order = row.get("_srcs") or []
                    occ["sources"].sort(
                        key=lambda x: order.index(x) if x in order else len(order))
            out = []
            for _, occ in sorted(rebuilt.items()):
                if not occ["sources"]:
                    del occ["sources"]
                out.append(occ)
            if out or m.get("occurrences") is not None:
                m["occurrences"] = out
        (pathlib.Path(into) / pathlib.Path(path).name).write_text(
            json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def check():
    """Join the committed observations into a scratch dir and diff.

    This used to call split() first, which was right while muscles-*.json was
    the source of truth and catastrophic afterwards: split() regenerates the
    observation files FROM the generated muscle files and deletes any that do
    not appear there, so running --check silently destroyed every file holding
    only unassigned rows. It is a read-only check now.
    """
    n_files = len(list(OBS.glob("*.json")))
    n_rows = sum(len(json.load(open(f)).get("observations") or [])
                 for f in OBS.glob("*.json"))
    print(f"source of truth: {n_files} observation files, {n_rows} rows")

    tmp = ROOT / ".roundtrip"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    join(tmp)

    bad = 0
    for path in muscle_files():
        name = pathlib.Path(path).name
        before = json.load(open(path))
        after = json.load(open(tmp / name))
        for a, b in zip(before["muscles"], after["muscles"]):
            oa, ob = a.get("occurrences") or [], b.get("occurrences") or []
            if len(oa) != len(ob):
                print(f"  {a['id']}: {len(oa)} occurrences -> {len(ob)}")
                bad += 1
                continue
            for x, y in zip(oa, ob):
                for k in set(x) | set(y):
                    if k == "sources":
                        if sorted(x.get(k, [])) != sorted(y.get(k, [])):
                            print(f"  {a['id']}/{x.get('species')}: sources "
                                  f"{x.get(k)} -> {y.get(k)}")
                            bad += 1
                    elif x.get(k) != y.get(k):
                        print(f"  {a['id']}/{x.get('species')}: field '{k}' differs")
                        bad += 1
    shutil.rmtree(tmp)
    if bad:
        print(f"\nROUND TRIP LOSSY — {bad} difference(s). The new shape cannot yet "
              f"hold everything the old one holds.")
        return 1
    print("\nround trip is lossless: every occurrence and every field survives")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    if "--split" in sys.argv:
        if (ROOT / "data/observations").exists() and "--force" not in sys.argv:
            sys.exit("data/observations/ is the source of truth now — --split would "
                     "overwrite it from the generated muscles-*.json. Pass --force if "
                     "that is really what you mean.")
        a, b, c = split()
        print(f"wrote {a} observation files and {b} mapping files ({c} rows)")
    elif "--join" in sys.argv:
        join(ROOT / "data")
        print("rebuilt data/muscles-*.json from observations/ + mapping/")
    else:
        sys.exit(__doc__)
