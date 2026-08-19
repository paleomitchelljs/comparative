#!/usr/bin/env python3
"""Regenerate the measured numbers in README.md, docs/GAPS.md and docs/MINING.md.

Every count in those files had drifted: the README said 108 muscles and 16 taxa,
GAPS.md said 126 and 16, validate.py said 126 and 19, and the live footer said
something else again. Numbers written by hand go stale the moment a source is
mined, and a coverage document whose coverage figures are wrong is worse than
one with no figures, because it is quoted.

So the measured blocks are generated. Curated prose around them is untouched:
the script only rewrites what sits between a matched pair of

    <!-- counts:NAME -->  ...  <!-- /counts:NAME -->

markers, and errors out if a marker it expects has gone missing.

    python3 scripts/doc_counts.py            # print, change nothing
    python3 scripts/doc_counts.py --write    # rewrite the marked blocks

Definitions, since the old figures used at least two:

  occurrence row     any entry in a record's `occurrences`
  present occurrence one whose `present` is not `no` — so `variable`,
                     `uncertain` and `inferred` count, on the same reasoning
                     that keeps them out of the absence column everywhere else
  scored occurrence  a present occurrence carrying its own `attachments`
  %att               scored / present, per region or per taxon
  observed row       an attachment row on an occurrence. Consensus rows are
                     excluded from the resolution figures: they are one row
                     inherited by up to nineteen taxa, and counting them once
                     per taxon inflates `side` and `landmark` coverage.
"""

import collections
import glob
import json
import pathlib
import re
import sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGION_ORDER = ['cranial', 'axial', 'fin', 'pectoral', 'arm', 'forearm', 'hand',
                'pelvic', 'thigh', 'leg', 'foot']


def load(rel):
    return json.loads((ROOT / rel).read_text())


def gather():
    muscles = []
    for path in sorted(glob.glob(str(ROOT / "data/muscles-*.json"))):
        doc = json.loads(pathlib.Path(path).read_text())
        for m in doc["muscles"]:
            m["_regionLabel"] = doc["region"]
            muscles.append(m)

    taxa = load("data/taxa.json")["taxa"]
    elements = load("data/skeleton.json")["elements"]
    sources = load("data/sources.json")["sources"]

    order = {t["id"]: i for i, t in enumerate(taxa)}
    clade = {t["id"]: t["clade"] for t in taxa}

    present = [(m, o) for m in muscles for o in m.get("occurrences", [])
               if (o.get("present") or "yes") != "no"]
    scored = [(m, o) for m, o in present if o.get("attachments")]

    obs_rows = [r for _, o in present
                for side in ("origin", "insertion")
                for r in (o.get("attachments") or {}).get(side, [])]

    carriers = set()
    for m in muscles:
        for att in [m.get("attachments")] + [o.get("attachments") for o in m.get("occurrences", [])]:
            for side in ("origin", "insertion"):
                for r in (att or {}).get(side, []):
                    carriers.update(x for x in (r.get("element"), r.get("landmark")) if x)

    return dict(
        muscles=muscles, taxa=taxa, elements=elements, sources=sources,
        order=order, clade=clade, present=present, scored=scored, obs_rows=obs_rows,
        carriers=carriers,
        occ_rows=sum(len(m.get("occurrences", [])) for m in muscles),
    )


def pct(a, b):
    return f"{round(100 * a / b)}%" if b else "—"


def coverage(d, keyf):
    total = collections.Counter()
    hit = collections.Counter()
    seen = collections.defaultdict(set)
    for m, o in d["present"]:
        k = keyf(m, o)
        total[k] += 1
        seen[k].add(m["id"])
    for m, o in d["scored"]:
        hit[keyf(m, o)] += 1
    return total, hit, seen


def block_headline(d):
    return (f"{len(d['muscles'])} muscle records · {len(d['present'])} present occurrences · "
            f"{len(d['elements'])} skeletal elements · {len(d['sources'])} sources · "
            f"{len(d['taxa'])} operational taxa")


def block_unscored(d):
    """MINING.md's headline. It was hand-written and said 222 while the live
    figure was 225 — the one number in the file whose whole job is to say how
    much work is left, drifting quietly because this script did not own it."""
    return (f"{len(d['present']) - len(d['scored'])} present occurrences still have "
            f"no attachment rows.")


def block_region_table(d):
    total, hit, seen = coverage(d, lambda m, o: m["region"])
    rows = sorted(total, key=lambda k: (-hit[k] / total[k], k))
    out = ["| Region | Muscles | Present occurrences | Scored | %att |",
           "|---|---:|---:|---:|---:|"]
    for k in rows:
        out.append(f"| {k} | {len(seen[k])} | {total[k]} | {hit[k]} | {pct(hit[k], total[k])} |")
    out.append(f"| **all** | {len(d['muscles'])} | {sum(total.values())} | "
               f"{sum(hit.values())} | **{pct(sum(hit.values()), sum(total.values()))}** |")
    return "\n".join(out)


def block_taxon_table(d):
    total, hit, _ = coverage(d, lambda m, o: speciesmap.clade_of(o))
    rows = sorted(total, key=lambda k: (-hit[k] / total[k], d["order"].get(k, 99)))
    out = ["| Taxon | Present occurrences | Scored | %att |", "|---|---:|---:|---:|"]
    for k in rows:
        out.append(f"| {d['clade'].get(k, k)} | {total[k]} | {hit[k]} | {pct(hit[k], total[k])} |")
    return "\n".join(out)


def block_skeleton_table(d):
    els, obs = d["elements"], d["obs_rows"]
    corr = [e for e in els if e.get("correlate")]
    lm = sum(1 for r in obs if r.get("landmark"))
    sd = sum(1 for r in obs if r.get("side"))
    used = sum(1 for e in els if e["id"] in d["carriers"])
    return "\n".join([
        "| | |", "|---|---|",
        f"| Elements | {len(els)}, of which {used} ({pct(used, len(els))}) carry at least one attachment |",
        f"| Observed attachment rows | {len(obs)} |",
        f"| Rows naming a **landmark** | {lm} ({pct(lm, len(obs))}) |",
        f"| Rows naming a **side** | {sd} ({pct(sd, len(obs))}) |",
        f"| Osteological correlates | {len(corr)} flagged, "
        f"{sum(1 for e in corr if e['id'] in d['carriers'])} carry a muscle |",
    ])


def block_authority(d):
    """Which homology scheme each record follows, and how old it is.

    Recency governs homology and does not govern attachment (docs/METHODS.md), so
    the interesting number is not how many records have an authority — the seed
    gives one to every record that can have one — but how old the newest
    comparative source bearing on each record is, and how many records have none
    at all.
    """
    year = {s["key"]: s.get("year") or 0 for s in d["sources"]}
    scope = {s["key"] for s in d["sources"] if s.get("homologyScope")}
    have, none = [], []
    for m in d["muscles"]:
        a = (m.get("homology") or {}).get("authority") or {}
        (have if a.get("source") else none).append(m)
    years = sorted(year.get(((m.get("homology") or {})["authority"])["source"], 0)
                   for m in have)
    med = years[len(years) // 2] if years else 0
    stale = sum(1 for y in years if y < 2010)
    return "\n".join([
        "| | |", "|---|---|",
        f"| Sources that can adjudicate a homology | {len(scope)} of {len(d['sources'])} |",
        f"| Records following one | {len(have)} of {len(d['muscles'])} "
        f"({pct(len(have), len(d['muscles']))}) |",
        f"| Median year of the governing source | {med} |",
        f"| Records governed by pre-2010 work | {stale} ({pct(stale, len(have))}) |",
        f"| Records with **no** homology-scope source | {len(none)} — "
        f"their homology rests on descriptive work alone |",
    ])


def block_gaps_summary(d):
    total, hit, _ = coverage(d, lambda m, o: speciesmap.clade_of(o))
    ranked = sorted((k for k in total if total[k] >= 20), key=lambda k: hit[k] / total[k])
    worst = ", ".join(f"{d['clade'].get(k, k)} at {pct(hit[k], total[k])}" for k in ranked[:3])
    rtot, rhit, _ = coverage(d, lambda m, o: m["region"])
    rworst = sorted(rtot, key=lambda k: rhit[k] / rtot[k])[:3]
    obs = d["obs_rows"]
    appendicular = [m for m in d["muscles"] if m["region"] not in ("cranial", "axial")]
    arch = [(m["id"], speciesmap.clade_of(o)) for m in d["muscles"] for o in m.get("occurrences", [])
            if o.get("architecture")]
    return (
        f"Taxon-specific attachments cover **{pct(len(d['scored']), len(d['present']))}** of "
        f"{len(d['present'])} present occurrences. The thinnest columns of any size are "
        f"{worst}; the thinnest regions are {', '.join(rworst)}. "
        f"`side` is on {pct(sum(1 for r in obs if r.get('side')), len(obs))} of observed rows and "
        f"`landmark` on {pct(sum(1 for r in obs if r.get('landmark')), len(obs))}; "
        f"`layer` resolves for {sum(1 for m in appendicular if m.get('layer'))} of "
        f"{len(appendicular)} appendicular muscles; architecture data covers {len(arch)} "
        f"muscle–taxon pairs across {len({t for _, t in arch})} taxa."
    )


def block_scored(d):
    return (f"**Taxon-specific attachments: {len(d['scored'])} of {len(d['present'])} "
            f"present occurrences ({pct(len(d['scored']), len(d['present']))}).**")


def block_holes(d):
    rows = collections.Counter()
    for m, o in d["scored"]:
        rows[m["region"]] += sum(len((o.get("attachments") or {}).get(s, []))
                                 for s in ("origin", "insertion"))
    out = ["| Region | Muscles | Observed attachment rows |", "|---|---:|---:|"]
    seen = collections.defaultdict(set)
    for m in d["muscles"]:
        seen[m["region"]].add(m["id"])
    for k in sorted(rows, key=lambda k: -rows[k]):
        out.append(f"| {k} | {len(seen[k])} | {rows[k]} |")
    return "\n".join(out)


def block_parity(d):
    """Elements per muscle, by the region of the SKELETON — a parity check on
    whether the ontology is thick enough to carry the musculature hung off it."""
    by_region = collections.defaultdict(lambda: (set(), set()))
    for m in d["muscles"]:
        for att in [m.get("attachments")] + [o.get("attachments") for o in m.get("occurrences", [])]:
            for side in ("origin", "insertion"):
                for r in (att or {}).get(side, []):
                    for x in (r.get("element"), r.get("landmark")):
                        if not x:
                            continue
                        el = next((e for e in d["elements"] if e["id"] == x), None)
                        if not el:
                            continue
                        muscles, els = by_region[el.get("region", "—")]
                        muscles.add(m["id"])
                        els.add(x)
    out = ["| Region | Muscles | Elements | Elements per muscle |", "|---|---:|---:|---:|"]
    for k, (mm, ee) in sorted(by_region.items(), key=lambda kv: -len(kv[1][1]) / len(kv[1][0])):
        out.append(f"| {k} | {len(mm)} | {len(ee)} | {len(ee) / len(mm):.1f} |")
    return "\n".join(out)


def block_region_records(d, existing):
    """README's region table: regenerate the count column, keep the curated prose.

    The principal-source column is an editorial judgement and stays in the
    document. Only the middle cell is measured, so only the middle cell moves.
    """
    counts = collections.Counter(m["_regionLabel"] for m in d["muscles"])
    out = []
    for line in existing.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] in counts:
            cells[1] = str(counts[cells[0]])
            out.append("| " + " | ".join(cells) + " |")
        else:
            out.append(line)
    missing = set(counts) - {c.strip() for line in existing.splitlines()
                             for c in line.strip().strip("|").split("|")}
    if missing:
        raise SystemExit(f"doc_counts: region table is missing rows for {sorted(missing)}")
    return "\n".join(out)


BLOCKS = {
    "headline": block_headline,
    "regions": block_region_table,
    "taxa": block_taxon_table,
    "skeleton": block_skeleton_table,
    "summary": block_gaps_summary,
    "scored": block_scored,
    "holes": block_holes,
    "parity": block_parity,
    "unscored": block_unscored,
    "authority": block_authority,
}

TARGETS = ["README.md", "docs/GAPS.md", "docs/MINING.md"]


def main(write):
    d = gather()
    changed = []
    for rel in TARGETS:
        path = ROOT / rel
        text = original = path.read_text()
        for name in list(BLOCKS) + ["region-records"]:
            # The body may be empty on a first run, so it is not required to
            # contain a newline — an empty block still has to match, or the
            # script reports "current" while writing nothing.
            pattern = re.compile(
                rf"<!-- counts:{name} -->(.*?)<!-- /counts:{name} -->", re.S)
            match = pattern.search(text)
            if not match:
                continue
            body = match.group(1).strip("\n")
            new = (block_region_records(d, body) if name == "region-records"
                   else BLOCKS[name](d)).strip("\n")
            text = (text[:match.start()] + f"<!-- counts:{name} -->\n{new}\n"
                    f"<!-- /counts:{name} -->" + text[match.end():])
        if text != original:
            changed.append(rel)
            if write:
                path.write_text(text)
    print(block_headline(d))
    print(f"  {d['occ_rows']} occurrence rows, {len(d['present'])} present, "
          f"{len(d['scored'])} scored ({pct(len(d['scored']), len(d['present']))})")
    if changed:
        print(("rewrote " if write else "stale, run with --write: ") + ", ".join(changed))
    else:
        print("docs are current")
    return 0 if (write or not changed) else 1


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
