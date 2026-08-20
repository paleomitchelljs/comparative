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
import copy
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

# Fields that belong to the extraction file and do not travel back into an
# occurrence. `record` and `region` place the row; `blockedBy`, `blockedNote` and
# `muscle` only exist while it is unassigned; the underscore fields are the
# round-trip machinery `split()` wrote and a hand-written row will not have.
EXTRACTION_ONLY = {"record", "region", "blockedBy", "blockedNote", "muscle",
                   "_occ", "_keys", "_srcs", "_id"}

# Sorts a row with no `_occ` after every row that has one, without inventing an
# index for it. See `join`.
UNPLACED = float("inf")

# Fields that accumulate across the sources describing one occurrence rather than
# having to agree between them. `attachments` because an observation of where a
# muscle attaches does not age or get outvoted; the prose because it is already
# written a paragraph per source, and concatenating is what keeps each source's
# reading in that source's own file.
PROSE = ("attachmentNote", "note")
ACCUMULATE = ("attachments",) + PROSE
NOTE_SEP = "\n\n"

# Fields where the sources may differ and the occurrence keeps the established
# value. `name` because what each source calls the muscle is recorded per source
# in `data/mapping/` — that layer exists for it — while the occurrence carries one
# label, and a new mining pass has no business silently relabelling a curated one.
# `speciesBasis` because SCHEMA.md records it as historical: it said how strongly
# a species attribution was evidenced back when the species had to be inferred,
# and the filename declares the animal now.
FIRST_WINS = ("name", "speciesBasis")


def occurrence_keys(row):
    """The occurrence's field order, for a row `split()` did not write.

    `_keys` records the order an occurrence already had, so the round trip stays
    byte-identical and `build.sh` stays a fixed point. A row written by hand
    during a mining pass has no such history: its own key order is the miner's,
    and the join places around it the two fields it reconstructs — `species`
    first, because every occurrence starts with it, and `sources` immediately
    before `attachments`, which is where the large majority of the committed
    occurrences carry it.
    """
    if row.get("_keys"):
        # `_keys` is the order the occurrence HAD, so a field added to the row
        # afterwards is not in it. Returning it bare dropped that field on the
        # floor — silently, because the join only emits keys it finds in the
        # shape. Adding `division` to eight scaffolded rows produced eight rows
        # the build ignored and no message anywhere. Anything the row carries
        # and the history does not is appended, which keeps the recorded order
        # for everything that has one.
        known = row["_keys"]
        extra = [k for k in row
                 if k not in known and k not in EXTRACTION_ONLY
                 and k not in ("species", "sources")]
        return known + extra if extra else known
    out = ["species"]
    for k in row:
        if k in EXTRACTION_ONLY or k in ("species", "sources"):
            continue
        if k == "attachments":
            out.append("sources")
        out.append(k)
    if "sources" not in out:
        out.append("sources")
    return out


def muscle_files():
    return sorted(glob.glob(str(ROOT / "data/muscles-*.json")))


def split():
    """muscles-*.json -> one file per (species, source), plus a mapping per source."""
    obs = collections.defaultdict(list)      # (species, source) -> [row]

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
    keep_obs = set()

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


    for d, keep in ((OBS, keep_obs),):
        for f in d.glob("*.json"):
            if f.name not in keep:
                f.unlink()
    return len(obs), 0, sum(len(v) for v in obs.values())


def write_mapping():
    """Regenerate data/mapping/ as a READ-ONLY VIEW of the homology decisions.

    The assignment itself lives on each observation row, in `record`. This
    directory is derived from those rows and exists so the homology layer can be
    read on its own — by the eventual UI build, and by anyone asking "if I move
    this name to another record, what does it touch?". That last question is the
    reason it is worth generating: 297 of 1273 (source, name, region) keys span
    more than one species, and one of Cunningham's spans fourteen.

    Editing a file here does nothing. Change `record` on the rows.
    """
    view = collections.defaultdict(lambda: collections.defaultdict(
        lambda: {"record": None, "species": set()}))
    unassigned = collections.Counter()
    for f in sorted(OBS.glob("*.json")):
        doc = json.load(open(f))
        for row in doc.get("observations") or []:
            nm = (row.get("name") or "").strip().lower()
            if not row.get("record"):
                unassigned[doc["source"]] += 1
                continue
            if not nm:
                continue          # unnamed rows are keyed by nothing; see `record`
            e = view[doc["source"]][f"{nm}|{row.get('region')}"]
            e["record"] = row["record"]
            e["species"].add(doc["species"])

    MAP.mkdir(parents=True, exist_ok=True)
    keep = set()
    for src in sorted(set(view) | set(unassigned)):
        table = {k: {"record": v["record"], "species": sorted(v["species"])}
                 for k, v in sorted(view.get(src, {}).items())}
        doc = {
            "source": src,
            "$comment": ("GENERATED VIEW — do not edit. The homology assignment lives "
                         "on each row in data/observations/ as `record`; this is that "
                         "layer read on its own, regenerated by build_observations.py "
                         "--join. `species` lists which animals a key covers, so the "
                         "cost of re-homologising it is visible: change the rows, not "
                         "this file."),
            "unassignedRows": unassigned.get(src, 0),
            "mapping": table,
        }
        out = MAP / f"{src}.json"
        keep.add(out.name)
        text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        if not out.exists() or out.read_text() != text:
            out.write_text(text)
    for f in MAP.glob("*.json"):
        if f.name not in keep:
            f.unlink()
    return len(keep)


def attach_parts(got, src, group, record, species, unheld):
    """Give each named part its own attachments, from the rows that describe it.

    An occurrence holds one union of attachment rows, so a record that is one
    muscle in a salamander and six in a human could say *that* six sites are
    used and never which muscle uses which. The detail was not missing from the
    dataset — it was in the extraction file all along, as one row per muscle,
    and the join was flattening it on the way in. 1692 named parts carried a
    name and nothing else.

    So: where ONE source contributes several named rows to one occurrence, each
    row's attachments are carried onto the part of that name. The union stays,
    because it is what the record as a whole attaches to and the app reads it;
    the parts now say how it divides.

    Two rules keep this from inventing claims.

    **Only within one source.** Several rows from one study are several muscles
    that study distinguishes; several rows from different studies are one muscle
    described twice, and merging those into parts would turn a synonymy into a
    division. That is why the caller keys on (species, source).

    **Never invent `division`.** How far a group has split is a judgement — one
    muscle with three heads and three separate muscles are different claims, and
    nothing in an extraction file distinguishes them. Where the occurrence
    already declares `heads`, `divided` or `variable`, the parts follow. Where it
    declares nothing, the rows are recorded in `unheld` and `validate.py` says
    so, because the fix is one authored field and then this runs by itself.
    """
    # Whether the row the occurrence takes its name from is itself a part turns
    # on whether anyone authored a `parts` list. If they did, that row is the
    # umbrella — `Masseter, temporalis, the pterygoids and the tensors` — and
    # listing it beside the six muscles it names would be nonsense. If they did
    # not, the rows are siblings and the occurrence is carrying one of their
    # names because something had to; `Triceps scapularis` is a head of the
    # triceps and belongs in the list with `Triceps humeralis`.
    umbrella = bool(got.get("parts"))
    rows = [r for r in group
            if not umbrella or r.get("name") != got.get("name")]
    if len(group) < 2 or not rows:
        return
    if got.get("division") not in ("heads", "divided", "variable"):
        unheld.append((record, species, src, [r["name"] for r in rows]))
        return
    parts = got.setdefault("parts", [])
    by_name = {p.get("name"): p for p in parts if isinstance(p, dict)}
    for row in rows:
        part = by_name.get(row["name"])
        if part is None:
            part = {"name": row["name"]}
            parts.append(part)
            by_name[row["name"]] = part
        part["attachments"] = copy.deepcopy(row["attachments"])
        if src != "(unsourced)" and src not in (part.get("sources") or []):
            part.setdefault("sources", []).append(src)
        # Field order, so the round trip does not depend on insertion order.
        order = ["name", "membership", "claimedBy", "muscle", "attachments",
                 "sources", "note"]
        for k in sorted(part, key=lambda x: (order.index(x) if x in order
                                             else len(order), x)):
            part[k] = part.pop(k)


def join(into):
    """observations/ + mapping/ -> muscle occurrences, written into `into`.

    Two studies of the same muscle in the same animal are two rows in two files
    and one occurrence, and the three kinds of field merge differently.

    **Attachments accumulate.** `CLAUDE.md`: an attachment is an observation and
    does not age, and two workers who each dissected an animal cannot conflict,
    because they are different rows. So origin and insertion are unions of
    distinct element/side/landmark rows. Freitas et al. put the iguana's
    deltoideus clavicularis on the interclavicle and Russell & Bauer put it on
    the clavicle; the occurrence carries both, under both names, which is what
    two dissections of one animal actually amount to.

    **Prose accumulates too, per source.** `attachmentNote` and `note` are
    already written a paragraph per source — nearly every one opens by naming its
    author — so the join concatenates the distinct ones in source order. That is
    what lets a source's reading live in that source's file instead of being
    copied into every other file that touches the same occurrence.

    **Everything else must agree.** A field two sources set to two different
    values stops the build and names the record, the animal, the field and both
    sources. Whether the pectoralis has two parts or three is one claim about one
    muscle, and the join has no business picking the alphabetically luckier
    source: somebody has to decide, and say why.

    The alternative, which this replaced, was for the first row read to win.
    That was harmless only while `--split` wrote every source's row from one
    merged occurrence, so the copies could not differ — which is also why none of
    this moves the committed data. The first hand-mined row added beside an
    older one would have been dropped on filename order.
    """
    unheld: list = []          # occurrences whose parts cannot be broken out yet
    by_record = collections.defaultdict(list)   # record -> [(species, source, row)]
    for f in sorted(OBS.glob("*.json")):
        doc = json.load(open(f))
        for row in doc["observations"]:
            if not row.get("record"):
                continue          # not assigned to a homology group yet
            by_record[row["record"]].append((doc["species"], doc["source"], row))

    write_mapping()

    conflicts, pending = [], []
    for path in muscle_files():
        doc = json.load(open(path))
        for m in doc["muscles"]:
            # An occurrence is identified by (record, species): that pair is
            # unique across all 1649 committed occurrences, which is why the
            # merge can key on the species the filename already declares rather
            # than on `_occ`. `_occ` survives as what it always was underneath —
            # the occurrence's ORDER within its record — so a row written by
            # hand needs no index and lands after the rows that have one.
            fields = {}                           # species -> {field: value}
            keys = {}                             # species -> field order
            order = {}                            # species -> [_occ, first seen]
            said_by = {}                          # (species, field) -> source
            contributed = collections.defaultdict(set)   # (species, field) -> notes
            srcs_of = collections.defaultdict(list)
            # Rows carrying an `_occ` — the ones that came out of the previous
            # store — merge before rows written by hand. So an established
            # label survives a new mining pass, a newly mined attachment is
            # appended after the ones already recorded rather than in front of
            # them, and a new source's paragraph reads after the older one.
            # Every committed row has an `_occ`, so this does not reorder
            # anything that exists today.
            # (species, source) -> [row], for the part synthesis below. A group
            # of several named rows from ONE source is several muscles the
            # source distinguishes inside one homology group; several rows from
            # DIFFERENT sources are one muscle described twice. Only the first
            # is a division, which is why this is keyed on the source too.
            per_source = collections.defaultdict(list)
            settled = sorted(enumerate(by_record.get(m["id"], [])),
                             key=lambda t: (t[1][2].get("_occ") is None, t[0]))
            for seen, (sp, src, row) in ((i, t) for i, t in settled):
                if row.get("name") and row.get("attachments"):
                    per_source[(sp, src)].append(row)
                slot = order.setdefault(sp, [UNPLACED, seen])
                if row.get("_occ") is not None:
                    slot[0] = min(slot[0], row["_occ"])
                got = fields.setdefault(sp, {})
                shape = keys.setdefault(sp, [])
                for k in occurrence_keys(row):
                    if k not in shape:
                        shape.append(k)
                    if k in ("species", "sources") or k not in row:
                        continue
                    if k not in got:
                        got[k] = copy.deepcopy(row[k]) if k in ACCUMULATE else row[k]
                        said_by[(sp, k)] = src
                        if k in PROSE:
                            contributed[(sp, k)].add(row[k])
                    elif k == "attachments":
                        for end, rows in row[k].items():
                            into_end = got[k].setdefault(end, [])
                            for one in rows:
                                if one not in into_end:
                                    into_end.append(one)
                    elif k in FIRST_WINS:
                        pass
                    elif k in PROSE:
                        # Membership is tested against the paragraphs actually
                        # contributed, not against a re-split of the running
                        # text: many of these notes carry blank lines of their
                        # own, so splitting the accumulated string never finds a
                        # multi-paragraph note and every build appended it again.
                        if row[k] not in contributed[(sp, k)]:
                            got[k] += NOTE_SEP + row[k]
                            contributed[(sp, k)].add(row[k])
                    elif got[k] != row[k]:
                        conflicts.append(
                            f"  {m['id']} / {sp}: '{k}' — {said_by[(sp, k)]} and "
                            f"{src} say different things")
                if src != "(unsourced)" and src not in srcs_of[sp]:
                    srcs_of[sp].append(src)
                    # Restore the order the record had, not the order the files
                    # happen to be read in.
                    was = row.get("_srcs") or []
                    srcs_of[sp].sort(
                        key=lambda x: was.index(x) if x in was else len(was))
            for (sp, src), group in per_source.items():
                if sp in fields:
                    attach_parts(fields[sp], src, group, m["id"], sp, unheld)

            out = []
            for sp in sorted(order, key=lambda s: tuple(order[s])):
                occ = {}
                for k in keys[sp]:
                    if k == "species":
                        occ["species"] = sp
                    elif k == "sources":
                        if srcs_of[sp]:
                            occ["sources"] = srcs_of[sp]
                    elif k in fields[sp]:
                        occ[k] = fields[sp][k]
                # `parts` can be gained by the synthesis above on an occurrence
                # whose recorded key order never had it.
                if "parts" in fields[sp] and "parts" not in occ:
                    occ["parts"] = fields[sp]["parts"]
                out.append(occ)
            if out or m.get("occurrences") is not None:
                m["occurrences"] = out
        pending.append((pathlib.Path(into) / pathlib.Path(path).name,
                        json.dumps(doc, indent=2, ensure_ascii=False) + "\n"))

    if conflicts:
        sys.exit("two sources disagree inside one occurrence, and the join will "
                 "not choose between them:\n" + "\n".join(sorted(set(conflicts))) +
                 "\n\nReconcile them in data/observations/. Where the disagreement "
                 "is real, it belongs in `attachmentNote` under both names.")
    for out, text in pending:
        out.write_text(text)

    if unheld:
        n = sum(len(v[3]) for v in unheld)
        print(f"  {n} part attachments in {len(unheld)} occurrences are held in "
              f"the union only, because the occurrence declares no `division`. "
              f"validate.py lists them.")


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
