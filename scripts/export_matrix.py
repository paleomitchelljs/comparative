#!/usr/bin/env python3
"""Export the dataset as tidy CSVs for downstream analysis.

The attachment structure is only a firm basis for analysis if it can leave the
app. These exports are long-format (one observation per row), which is what
comparative methods in R or Python expect, and every row carries its source and
whether the value was observed or inherited from the consensus.

    python3 scripts/export_matrix.py [outdir]     # default: export/

Writes:
  attachments.csv   muscle x taxon x side x element x landmark, one row each
  presence.csv      muscle x taxon presence states — a character matrix
  elements.csv      the skeletal ontology, flattened with lineage
  muscles.csv       one row per muscle with hierarchy fields

Nothing here is derived or imputed beyond what the app itself shows: `inherited`
marks a row taken from the muscle-level consensus because no taxon-specific
attachment is on record. Filter those out for any analysis that needs observed
data only.
"""

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


def main(outdir: pathlib.Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)

    skel = load("skeleton.json")
    taxa_doc = load("taxa.json")
    by_id = {e["id"]: e for e in skel["elements"]}

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

    muscles = []
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        for m in doc["muscles"]:
            m["_file"] = path.name
            m["_regionLabel"] = doc["region"]
            muscles.append(m)

    taxon_order = {}

    def walk(node):
        if "taxon" in node:
            taxon_order[node["taxon"]] = len(taxon_order)
        for c in node.get("children", []):
            walk(c)
    walk(taxa_doc["topology"])

    # ---- attachments.csv ----------------------------------------------------
    with open(outdir / "attachments.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "region", "segment", "mass", "layer",
                    "taxon_id", "taxon_clade", "taxon_order", "attachment_type",
                    "element_id", "element_label", "side", "landmark_id", "landmark_label",
                    "is_correlate", "inherited", "sources"])
        n = 0
        for m in muscles:
            cons = m.get("attachments", {})
            for occ in m.get("occurrences", []):
                tid = occ["taxon"]
                if (occ.get("present") or "yes") == "no":
                    continue
                att, inherited = (occ["attachments"], False) if occ.get("attachments") else (cons, True)
                srcs = ";".join(occ.get("sources", []) if not inherited else m.get("sources", []))
                for kind in ("origin", "insertion"):
                    for r in att.get(kind, []):
                        els = [x for x in (r.get("element"), r.get("landmark")) if x]
                        if inherited and not all(present_in(x, tid) for x in els):
                            continue      # would assert an attachment to a bone the taxon lacks
                        lm = r.get("landmark")
                        w.writerow([
                            m["id"], m["name"], m.get("region", ""), m.get("segment", ""),
                            m.get("mass", ""), m.get("layer", ""),
                            tid, next((t["clade"] for t in taxa_doc["taxa"] if t["id"] == tid), tid),
                            taxon_order.get(tid, ""),
                            kind, r.get("element", ""),
                            by_id.get(r.get("element"), {}).get("label", ""),
                            r.get("side", ""), lm or "",
                            by_id.get(lm, {}).get("label", "") if lm else "",
                            "TRUE" if by_id.get(lm or r.get("element"), {}).get("correlate") else "FALSE",
                            "TRUE" if inherited else "FALSE", srcs])
                        n += 1

    # ---- presence.csv (character matrix) -----------------------------------
    with open(outdir / "presence.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "region", "mass", "layer", "segment",
                    "taxon_id", "taxon_clade", "taxon_order", "state", "local_name", "sources"])
        rows = 0
        for m in muscles:
            for occ in m.get("occurrences", []):
                tid = occ["taxon"]
                w.writerow([m["id"], m["name"], m.get("region", ""), m.get("mass", ""),
                            m.get("layer", ""), m.get("segment", ""),
                            tid, next((t["clade"] for t in taxa_doc["taxa"] if t["id"] == tid), tid),
                            taxon_order.get(tid, ""),
                            occ.get("present", "yes"), occ.get("name", ""),
                            ";".join(occ.get("sources", []))])
                rows += 1

    # ---- elements.csv -------------------------------------------------------
    with open(outdir / "elements.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["element_id", "label", "kind", "region", "segment", "part_of",
                    "lineage", "is_correlate", "presence_default",
                    "present_in", "absent_in", "sources"])
        for e in skel["elements"]:
            p = e.get("presence", {})
            w.writerow([e["id"], e["label"], e["kind"], e.get("region", ""), e.get("segment", ""),
                        e.get("partOf", ""), ">".join(reversed(lineage(e["id"]))),
                        "TRUE" if e.get("correlate") else "FALSE",
                        p.get("default", ""), ";".join(p.get("present", [])),
                        ";".join(p.get("absent", [])), ";".join(p.get("sources", []))])

    # ---- muscles.csv --------------------------------------------------------
    with open(outdir / "muscles.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "name", "region", "region_label", "subregion", "segment",
                    "mass", "layer", "layer_from", "arch", "ancestral_node",
                    "homology_confidence", "n_taxa_present", "synonyms", "sources"])
        for m in muscles:
            present = sum(1 for o in m.get("occurrences", [])
                          if (o.get("present") or "yes") != "no")
            w.writerow([m["id"], m["name"], m.get("region", ""), m.get("_regionLabel", ""),
                        m.get("subregion", ""), m.get("segment", ""), m.get("mass", ""),
                        m.get("layer", ""), (m.get("layerSource") or {}).get("from", ""),
                        m.get("arch", ""), m.get("ancestralNode", ""),
                        (m.get("homology") or {}).get("confidence", ""),
                        present, ";".join(m.get("synonyms", [])), ";".join(m.get("sources", []))])

    print(f"attachments.csv  {n} rows")
    print(f"presence.csv     {rows} rows")
    print(f"elements.csv     {len(skel['elements'])} rows")
    print(f"muscles.csv      {len(muscles)} rows")
    print(f"-> {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "export")))
