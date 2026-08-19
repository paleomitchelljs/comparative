#!/usr/bin/env python3
"""Set `homology.authority` — whose homology scheme each muscle record follows.

The rule this implements is in `docs/METHODS.md`: **an attachment is an
observation and does not age; a homology is an interpretation and does.** Where
two sources disagree about where a muscle attaches, both are right about their own
animal and both rows stand. Where they disagree about what a muscle *is* — whether
two bellies are one muscle, which reptilian muscle a mammalian one descends from,
what to call it — the more recent comparative treatment governs, because it had
the earlier one in front of it.

So this picks, from the sources cited anywhere on a record, the most recent one
flagged `homologyScope` in `sources.json`, and writes it as the record's
authority. Idempotent; re-runnable at any time.

`basis: "curated"` opts a record out. The seed will not touch it and the
validator requires a `note` saying why the dataset follows an older scheme —
usually because the newer source does not examine the taxa the record turns on.

    python3 scripts/seed_homology_authority.py           # report
    python3 scripts/seed_homology_authority.py --write   # apply
"""
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv


def cited_keys(muscle):
    """Every source key the record leans on, at any depth."""
    keys = set(muscle.get("sources") or [])
    keys.update((muscle.get("layerSource") or {}).get("sources") or [])
    # A correspondence is a homology claim in its own right, so whoever supports
    # it is a candidate for governing this record's homology — but not every
    # relation says something about what THIS muscle is.
    #
    # `descends-from` and `corresponds-to-part-of` do: they place the record in
    # an ancestry or inside a whole, and are directed, so their source is
    # speaking about this end of the edge.
    #
    # `serial` does not. It is symmetric, it is topological rather than
    # genealogical by default, and Diogo & Molnar (2014) reject it as strict
    # serial homology outright — so it says these two muscles are one series in
    # different segments, not what either muscle IS. Feeding its source into
    # authority also breaks in both directions at once: attributing the
    # forelimb–hindlimb edges to the paper written about that axis would have
    # handed five forelimb records (abductor pollicis longus, pronator teres,
    # both flexores accessorii, intermetacarpales) from Abdala & Diogo's
    # forelimb synonymy to a hindlimb paper, purely for carrying one edge to a
    # muscle of the foot.
    #
    # `no-counterpart` is on the same axis vocabulary and would raise the same
    # question, but every such edge in the data is hindlimb-side, so excluding
    # it would change nothing today and it is left in deliberately.
    for e in ((muscle.get("homology") or {}).get("correspondences") or []):
        if e.get("relation") == "serial":
            continue
        keys.update(e.get("sources") or [])
    for occ in muscle.get("occurrences") or []:
        keys.update(occ.get("sources") or [])
        for part in occ.get("parts") or []:
            keys.update(part.get("sources") or [])
        for row in occ.get("nerves") or []:
            keys.update(row.get("sources") or [])
        keys.update((occ.get("architecture") or {}).get("sources") or [])
    return keys


def main():
    sources = json.load(open(ROOT / "data/sources.json"))["sources"]
    # A source governs homology only if establishing homology, synonymy or
    # nomenclature ACROSS MORE THAN ONE TAXON is part of its stated purpose.
    # Describing one animal well does not qualify — that is the other half of
    # the rule, and it is why Cunningham (1882) and Osawa (1898) are not here.
    authority_year = {s["key"]: s.get("year") or 0
                      for s in sources if s.get("homologyScope")}
    if not authority_year:
        sys.exit("no sources carry `homologyScope` — nothing to seed")

    changed = orphans = curated = 0
    for path in sorted(glob.glob(str(ROOT / "data/muscles-*.json"))):
        doc = json.load(open(path))
        dirty = False
        for m in doc["muscles"]:
            hom = m.setdefault("homology", {})
            existing = hom.get("authority") or {}
            if existing.get("basis") == "curated":
                curated += 1
                continue

            candidates = cited_keys(m) & authority_year.keys()
            if not candidates:
                # Homology resting on descriptive sources alone. Left without an
                # authority rather than given a plausible one; validate.py warns.
                if hom.pop("authority", None) is not None:
                    dirty = True
                orphans += 1
                continue

            # Most recent wins; the key breaks year ties so the result is stable.
            best = max(candidates, key=lambda k: (authority_year[k], k))
            want = {"source": best, "basis": "computed"}
            if existing != want:
                hom["authority"] = want
                dirty = True
                changed += 1

        if dirty and WRITE:
            with open(path, "w") as fh:
                json.dump(doc, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    verb = "set" if WRITE else "would set"
    print(f"homology.authority: {verb} on {changed} records; "
          f"{curated} curated and left alone; "
          f"{orphans} cite no homology-scope source")
    if not WRITE and changed:
        print("re-run with --write to apply")


if __name__ == "__main__":
    main()
