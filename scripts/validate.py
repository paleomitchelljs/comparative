#!/usr/bin/env python3
"""Schema and referential-integrity check for the muscle dataset.

Run from the repo root:  python3 scripts/validate.py
Exit status is non-zero if any error is found, so this works as a pre-commit hook.
"""

import json
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
MUSCLE_FILES = sorted(ROOT.glob("data/muscles-*.json"))

PRESENCE = {"yes", "no", "variable", "uncertain", "inferred"}
CONFIDENCE = {"well-supported", "moderate", "contested", "uncertain"}
SERIAL_BASIS = {"topological", "developmental", "none"}
LAYERS = {"superficialis", "profundus", "preaxial", "postaxial", "primaxial"}

errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(path):
    with open(path) as fh:
        return json.load(fh)


def main():
    if not MUSCLE_FILES:
        err("no data/muscles-*.json files found")
        return report()

    taxa_doc = load(ROOT / "data/taxa.json")
    sources_doc = load(ROOT / "data/sources.json")

    taxon_ids = {t["id"] for t in taxa_doc["taxa"]}
    source_keys = {s["key"] for s in sources_doc["sources"]}

    # Every taxon in the topology must be defined, and vice versa.
    topo_ids = set()

    def walk(node):
        if "taxon" in node:
            topo_ids.add(node["taxon"])
        for child in node.get("children", []):
            walk(child)

    walk(taxa_doc["topology"])
    for missing in sorted(topo_ids - taxon_ids):
        err(f"taxa.json: topology references undefined taxon '{missing}'")
    for orphan in sorted(taxon_ids - topo_ids):
        err(f"taxa.json: taxon '{orphan}' is defined but absent from the topology")

    muscles = {}
    for path in MUSCLE_FILES:
        doc = load(path)
        rel = path.relative_to(ROOT)
        if "region" not in doc:
            err(f"{rel}: missing top-level 'region'")
        for m in doc.get("muscles", []):
            mid = m.get("id")
            if not mid:
                err(f"{rel}: a muscle record has no id")
                continue
            if mid in muscles:
                err(f"{rel}: duplicate muscle id '{mid}'")
            muscles[mid] = (m, rel)

    for mid, (m, rel) in muscles.items():
        where = f"{rel}:{mid}"

        for field in ("name", "region", "occurrences", "sources"):
            if field not in m:
                err(f"{where}: missing required field '{field}'")

        cons = m.get("consensus", {})
        for field in ("origin", "insertion", "action", "innervation"):
            if not cons.get(field):
                warn(f"{where}: consensus.{field} is empty")

        for key in m.get("sources", []):
            if key not in source_keys:
                err(f"{where}: unknown source key '{key}'")

        seen_taxa = Counter()
        for occ in m.get("occurrences", []):
            tid = occ.get("taxon")
            if tid not in taxon_ids:
                err(f"{where}: occurrence references unknown taxon '{tid}'")
            seen_taxa[tid] += 1

            pres = occ.get("present", "yes")
            if pres not in PRESENCE:
                err(f"{where}/{tid}: present='{pres}' not in {sorted(PRESENCE)}")

            if pres != "no" and not occ.get("sources"):
                warn(f"{where}/{tid}: present but no source cited")

            for key in occ.get("sources", []):
                if key not in source_keys:
                    err(f"{where}/{tid}: unknown source key '{key}'")

            # A present muscle should be named in that taxon, else the row says nothing.
            if pres in {"yes", "inferred"} and not occ.get("name"):
                warn(f"{where}/{tid}: present='{pres}' but no local name given")

        for tid, n in seen_taxa.items():
            if n > 1:
                err(f"{where}: taxon '{tid}' appears in {n} occurrence rows")

        hom = m.get("homology", {})
        conf = hom.get("confidence")
        if conf and conf not in CONFIDENCE:
            err(f"{where}: homology.confidence='{conf}' not in {sorted(CONFIDENCE)}")
        if not conf:
            warn(f"{where}: no homology.confidence")

        for ref in hom.get("related", []):
            if ref not in muscles:
                err(f"{where}: homology.related points at unknown muscle '{ref}'")

        # `derivatives` links an ancestral fin muscle to the tetrapod muscles it
        # gave rise to. Directed, not symmetric — the app renders the reverse
        # edge ("derived from") by scanning, so only one direction is curated.
        derivs = m.get("derivatives", {})
        if derivs:
            if m.get("region") != "fin":
                warn(f"{where}: has `derivatives` but region is not 'fin'")
            for appendage, refs in derivs.items():
                if appendage not in {"pectoral", "pelvic"}:
                    err(f"{where}: derivatives key '{appendage}' not in ['pectoral', 'pelvic']")
                for ref in refs:
                    if ref not in muscles:
                        err(f"{where}: derivatives.{appendage} points at unknown muscle '{ref}'")

        layer = m.get("layer")
        if layer and layer not in LAYERS:
            err(f"{where}: layer='{layer}' not in {sorted(LAYERS)}")
        if m.get("region") == "fin" and not layer:
            warn(f"{where}: fin muscle without a `layer`")

        serial = hom.get("serial")
        if serial:
            basis = serial.get("basis")
            if basis not in SERIAL_BASIS:
                err(f"{where}: serial.basis='{basis}' not in {sorted(SERIAL_BASIS)}")
            fl = serial.get("forelimb")
            if fl and fl not in muscles:
                err(f"{where}: serial.forelimb points at unknown muscle '{fl}'")

    # Reciprocity: if A lists B as related, B should list A. Cheap way to keep the graph sane.
    for mid, (m, rel) in muscles.items():
        for ref in m.get("homology", {}).get("related", []):
            other = muscles.get(ref)
            if other and mid not in other[0].get("homology", {}).get("related", []):
                warn(f"{rel}:{mid}: related '{ref}' does not link back")

    unused = source_keys - {
        k
        for m, _ in muscles.values()
        for k in list(m.get("sources", []))
        + [s for o in m.get("occurrences", []) for s in o.get("sources", [])]
    }
    for key in sorted(unused):
        warn(f"sources.json: '{key}' is never cited")

    print(f"checked {len(muscles)} muscles across {len(MUSCLE_FILES)} files, "
          f"{len(taxon_ids)} taxa, {len(source_keys)} sources")
    return report()


def report():
    for w in warnings:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
