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
LAYERS = {"superficialis", "profundus", "intermediate", "preaxial", "postaxial", "primaxial"}
SEGMENTS = {"cranial", "axial", "girdle", "stylopod", "zeugopod", "autopod", "fin"}

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
    skeleton_doc = load(ROOT / "data/skeleton.json")

    taxon_ids = {t["id"] for t in taxa_doc["taxa"]}
    source_keys = {s["key"] for s in sources_doc["sources"]}
    element_ids = {e["id"] for e in skeleton_doc["elements"]}
    side_terms = set(skeleton_doc.get("sides", []))

    # Skeleton internal consistency.
    kinds = set(skeleton_doc["kinds"])
    segments = set(skeleton_doc["segments"])
    seen_elements = set()
    for e in skeleton_doc["elements"]:
        eid = e.get("id")
        if not eid:
            err("skeleton.json: element without an id")
            continue
        if eid in seen_elements:
            err(f"skeleton.json: duplicate element id '{eid}'")
        seen_elements.add(eid)
        if e.get("kind") not in kinds:
            err(f"skeleton.json:{eid}: kind '{e.get('kind')}' not in {sorted(kinds)}")
        if e.get("segment") not in segments:
            err(f"skeleton.json:{eid}: segment '{e.get('segment')}' not in {sorted(segments)}")
        parent = e.get("partOf")
        if parent and parent not in element_ids:
            err(f"skeleton.json:{eid}: partOf '{parent}' is not an element")
        pres = e.get("presence", {})
        if pres.get("default") not in {"yes", "no", "variable"}:
            err(f"skeleton.json:{eid}: presence.default must be yes/no/variable")
        for key in ("present", "absent", "variable", "partial", "reduced"):
            for tid in pres.get(key, []):
                if tid not in taxon_ids:
                    err(f"skeleton.json:{eid}: presence.{key} lists unknown taxon '{tid}'")
        for k in pres.get("sources", []):
            if k not in source_keys:
                err(f"skeleton.json:{eid}: unknown source key '{k}'")

    by_id = {e["id"]: e for e in skeleton_doc["elements"] if e.get("id")}

    def lineage(eid):
        out, cur = [], eid
        while cur and cur not in out:
            out.append(cur)
            cur = by_id.get(cur, {}).get("partOf")
        return out

    def present_in(eid, tid):
        p = by_id.get(eid, {}).get("presence", {})
        if tid in p.get("absent", []):
            return False
        if p.get("default") == "no":
            return tid in (p.get("present", []) + p.get("partial", []) + p.get("reduced", []))
        return True

    # partOf must not cycle, or the bone-first drill-down recurses forever.
    for eid in by_id:
        seen, cur = set(), eid
        while cur:
            if cur in seen:
                err(f"skeleton.json: partOf cycle involving '{eid}'")
                break
            seen.add(cur)
            cur = by_id.get(cur, {}).get("partOf")

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

        def check_rows(att, label, taxon=None):
            """An attachment row is {element, side?, landmark?}. The landmark must
            sit inside the element, or the bone-first drill-down would file it in
            the wrong place."""
            for side_key in ("origin", "insertion"):
                for row in att.get(side_key, []):
                    if not isinstance(row, dict):
                        err(f"{label}: attachments.{side_key} entry is not an "
                            f"element/side/landmark row: {row!r}")
                        continue
                    el = row.get("element")
                    if el not in element_ids:
                        err(f"{label}: attachments.{side_key} element '{el}' "
                            f"is not in skeleton.json")
                        continue
                    if row.get("side") and row["side"] not in side_terms:
                        err(f"{label}: side '{row['side']}' not in {sorted(side_terms)}")
                    lm = row.get("landmark")
                    if lm:
                        if lm not in element_ids:
                            err(f"{label}: landmark '{lm}' is not in skeleton.json")
                        elif el not in lineage(lm):
                            err(f"{label}: landmark '{lm}' is not part of '{el}'")
                    if taxon:
                        for ref in filter(None, (el, lm)):
                            if not present_in(ref, taxon):
                                err(f"{label}: attaches to '{ref}', which "
                                    f"skeleton.json records as absent in {taxon}")

        check_rows(m.get("attachments", {}), where)

        seen_taxa = Counter()
        for occ in m.get("occurrences", []):
            tid = occ.get("taxon")
            if tid not in taxon_ids:
                err(f"{where}: occurrence references unknown taxon '{tid}'")
            seen_taxa[tid] += 1

            check_rows(occ.get("attachments", {}), f"{where}/{tid}", taxon=tid)
            if occ.get("attachments") and not occ.get("sources"):
                warn(f"{where}/{tid}: taxon-specific attachments with no source")

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

        seg = m.get("segment")
        if seg and seg not in SEGMENTS:
            err(f"{where}: segment='{seg}' not in {sorted(SEGMENTS)}")
        if not seg:
            warn(f"{where}: no `segment` (run scripts/assign_hierarchy.py --write)")

        ls = m.get("layerSource")
        if ls:
            if ls.get("from") not in muscles:
                err(f"{where}: layerSource.from '{ls.get('from')}' is not a muscle")
            for k in ls.get("sources", []):
                if k not in source_keys:
                    err(f"{where}: layerSource unknown source key '{k}'")

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
