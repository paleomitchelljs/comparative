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
  division.csv      muscle x taxon differentiation states and part counts
  parts.csv         one row per named subunit, long form under division.csv
  elements.csv      the skeletal ontology, flattened with lineage
  fusions.csv       skeletal fusion and fission events, one row per taxon
  innervation.csv   muscle x nerve, with plexus division and mass agreement
  joints.csv        the joint ontology: which bone surfaces articulate
  actions.csv       muscle x joint x motion, checked against what it spans
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

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jointgraph

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((ROOT / "data" / name).read_text())



# Occurrences are keyed on species; the clade is derived. Every export keeps BOTH
# columns, because a downstream analysis wants the species it was observed in and
# the clade it rolls up to, and reconstructing either from the other outside the
# repo is exactly the kind of re-derivation these files exist to prevent.
def _species_index():
    with open(ROOT / "data/species.json") as fh:
        doc = json.load(fh)
    return ({s["id"]: s.get("clade") for s in doc["species"]},
            {s["id"]: s.get("binomial", s["id"]) for s in doc["species"]})


SPECIES_CLADE, SPECIES_NAME = _species_index()


def occ_taxon(occ):
    return SPECIES_CLADE.get(occ.get("species"), "")


def occ_species(occ):
    return occ.get("species", "")


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
                    "species_id", "species", "taxon_id", "taxon_clade", "taxon_order", "attachment_type",
                    "element_id", "element_label", "side", "landmark_id", "landmark_label",
                    "is_correlate", "inherited", "sources"])
        n = 0
        for m in muscles:
            cons = m.get("attachments", {})
            for occ in m.get("occurrences", []):
                tid = occ_taxon(occ)
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
                            occ_species(occ), SPECIES_NAME.get(occ_species(occ), ""),
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
                    "species_id", "species", "taxon_id", "taxon_clade", "taxon_order",
                    "state", "local_name", "sources"])
        rows = 0
        for m in muscles:
            for occ in m.get("occurrences", []):
                tid = occ_taxon(occ)
                w.writerow([m["id"], m["name"], m.get("region", ""), m.get("mass", ""),
                            m.get("layer", ""), m.get("segment", ""),
                            occ_species(occ), SPECIES_NAME.get(occ_species(occ), ""),
                            tid, next((t["clade"] for t in taxa_doc["taxa"] if t["id"] == tid), tid),
                            taxon_order.get(tid, ""),
                            occ.get("present", "yes"), occ.get("name", ""),
                            ";".join(occ.get("sources", []))])
                rows += 1

    # ---- division.csv (differentiation character) ---------------------------
    #
    # Two files, because the question has two shapes. `division.csv` is the
    # character matrix: one row per muscle x taxon, with the ordered state and a
    # part count, ready to optimise on the tree the way presence already is.
    # `parts.csv` is the long form underneath it, one row per named subunit, so
    # a disputed part can be included or dropped by filtering rather than by
    # re-reading the JSON.
    #
    # `n_parts_firm` counts only parts whose membership is established;
    # `n_parts_max` counts every part listed. Where the two differ the count is
    # a range, not a number, and `parts_open` marks the source enumerating
    # rather than finishing — so `n_parts_max` is itself a floor there.
    with open(outdir / "division.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "region", "taxon_id", "taxon_order",
                    "division", "division_rank", "n_parts_firm", "n_parts_max",
                    "parts_open", "sources"])
        # single < heads < divided. `variable` is polymorphic and deliberately
        # unranked: it means the clade contains more than one state.
        rank = {"single": 0, "heads": 1, "divided": 2}
        div_n = 0
        for m in muscles:
            for occ in m.get("occurrences", []):
                d = occ.get("division")
                if not d:
                    continue
                parts = occ.get("parts", [])
                firm = [x for x in parts
                        if (x.get("membership") or "established") == "established"]
                w.writerow([m["id"], m["name"], m.get("region", ""), occ_species(occ), SPECIES_NAME.get(occ_species(occ), ""), occ_taxon(occ),
                            taxon_order.get(occ_taxon(occ), ""),
                            d, rank.get(d, ""),
                            len(firm) if parts else (1 if d == "single" else ""),
                            len(parts) if parts else (1 if d == "single" else ""),
                            "TRUE" if occ.get("partsOpen") else "FALSE",
                            ";".join(occ.get("sources", []))])
                div_n += 1

    with open(outdir / "parts.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "taxon_id", "division",
                    "part", "membership", "part_muscle_id", "note", "sources"])
        part_n = 0
        for m in muscles:
            for occ in m.get("occurrences", []):
                for x in occ.get("parts", []):
                    w.writerow([m["id"], m["name"], occ_taxon(occ), occ.get("division", ""),
                                x.get("name", ""),
                                x.get("membership") or "established",
                                x.get("muscle", ""), x.get("note", ""),
                                ";".join(x.get("sources") or occ.get("sources", []))])
                    part_n += 1

    # ---- architecture.csv ---------------------------------------------------
    with open(outdir / "architecture.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "region", "taxon_id", "species", "n",
                    "part", "abbr", "mass_g_mean", "mass_g_sd",
                    "fascicle_mm_mean", "fascicle_mm_sd", "pcsa_cm2_mean", "pcsa_cm2_sd",
                    "pennation_deg", "max_isometric_force_N", "body_mass_kg", "sources"])
        arch_n = 0
        for m in muscles:
            for occ in m.get("occurrences", []):
                a = occ.get("architecture")
                if not a:
                    continue
                for pt in a.get("parts", []):
                    g = lambda k, f: (pt.get(k) or {}).get(f, "")
                    w.writerow([m["id"], m["name"], m.get("region", ""), occ_taxon(occ),
                                a.get("species", ""), a.get("n", ""),
                                pt.get("name", ""), pt.get("abbr", ""),
                                g("mass_g", "mean"), g("mass_g", "sd"),
                                g("fascicleLength_mm", "mean"), g("fascicleLength_mm", "sd"),
                                g("pcsa_cm2", "mean"), g("pcsa_cm2", "sd"),
                                g("pennation_deg", "mean"), g("maxIsometricForce_N", "mean"),
                                a.get("bodyMass_kg", ""),
                                ";".join(a.get("sources", []))])
                    arch_n += 1

    # ---- elements.csv -------------------------------------------------------
    with open(outdir / "elements.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["element_id", "label", "kind", "region", "segment", "part_of",
                    "lineage", "is_correlate", "presence_default",
                    "present_in", "absent_in", "fused_from", "derived_from", "sources"])
        for e in skel["elements"]:
            p = e.get("presence", {})
            w.writerow([e["id"], e["label"], e["kind"], e.get("region", ""), e.get("segment", ""),
                        e.get("partOf", ""), ">".join(reversed(lineage(e["id"]))),
                        "TRUE" if e.get("correlate") else "FALSE",
                        p.get("default", ""), ";".join(p.get("present", [])),
                        ";".join(p.get("absent", [])),
                        ";".join(e.get("fusedFrom", [])), e.get("derivedFrom", ""),
                        ";".join(p.get("sources", []))])

    # ---- innervation.csv ----------------------------------------------------
    #
    # One row per muscle x scope x nerve, carrying the nerve's inherited limb-bud
    # division and its chain up to the plexus. `scope` is "consensus" or a taxon
    # id, following the same placement rule as attachments.
    #
    # `division_agrees` compares the nerve's division against the muscle's
    # `mass`. That is the cross-check the structured nerves exist for: a limb
    # muscle's supply should sit in the division of the plexus matching the
    # limb-bud mass it came from, and a disagreement is either a data error or
    # something worth writing about.
    nerves_doc = load("nerves.json")
    nerve_by_id = {n["id"]: n for n in nerves_doc["nerves"]}

    def nerve_chain(nid):
        out, cur, guard = [], nid, 0
        while cur and guard < 20:
            out.append(cur)
            cur, guard = nerve_by_id.get(cur, {}).get("partOf"), guard + 1
        return out

    def nerve_div(nid):
        for x in nerve_chain(nid):
            d = nerve_by_id.get(x, {}).get("division")
            if d:
                return d
        return ""

    with open(outdir / "innervation.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "region", "mass", "scope",
                    "nerve_id", "nerve_label", "nerve_kind", "cranial_nerve",
                    "arch", "division", "division_agrees", "segments", "chain"])
        nerve_n = 0
        for m in muscles:
            scopes = [("consensus", m)] + [(occ_taxon(o), o) for o in m.get("occurrences", [])]
            for scope, holder in scopes:
                for r in holder.get("nerves") or []:
                    nid = r["nerve"]
                    nrec = nerve_by_id.get(nid, {})
                    d = nerve_div(nid)
                    agrees = ""
                    if d and m.get("mass") in ("dorsal", "ventral"):
                        agrees = "TRUE" if d == m["mass"] else "FALSE"
                    w.writerow([m["id"], m["name"], m.get("region", ""), m.get("mass", ""),
                                scope, nid, nrec.get("label", ""), nrec.get("kind", ""),
                                nrec.get("cn", ""), nrec.get("arch", ""), d, agrees,
                                r.get("segments", ""),
                                ">".join(reversed(nerve_chain(nid)))])
                    nerve_n += 1

    # ---- actions.csv --------------------------------------------------------
    #
    # One row per muscle x scope x joint x motion, plus `spans` — whether the
    # muscle's attachments actually cross that joint. The two are independent
    # (a claim from a source against a derivation from attachments), so the
    # column is a check, not a restatement. FALSE means either a scoring error
    # or a muscle acting through another's tendon; both are worth filtering for.
    #
    # `joints.csv` is the ontology itself, one row per joint x side x element,
    # which is the long form of "distal femur articulates with proximal tibia".
    joints_doc = load("joints.json")
    graph = jointgraph.build(joints_doc, by_id)
    joint_by_id = {j["id"]: j for j in joints_doc["joints"]}

    with open(outdir / "joints.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["joint_id", "joint_label", "region", "kind", "crossing",
                    "side", "element_id", "element_label", "element_side",
                    "landmark_id", "motions", "sources"])
        joint_n = 0
        for j in joints_doc["joints"]:
            prox = {r.get("element") for r in j.get("proximal", [])}
            dist = {r.get("element") for r in j.get("distal", [])}
            crossing = j.get("crossing", "serial" if prox == dist else "chain")
            for side_key in ("proximal", "distal"):
                for r in j.get(side_key, []):
                    w.writerow([j["id"], j["label"], j.get("region", ""), j["kind"],
                                crossing, side_key, r.get("element", ""),
                                by_id.get(r.get("element"), {}).get("label", ""),
                                r.get("side", ""), r.get("landmark", ""),
                                ";".join(j.get("motions", [])),
                                ";".join(j.get("sources", []))])
                    joint_n += 1

    with open(outdir / "actions.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muscle_id", "muscle_name", "region", "scope",
                    "joint_id", "joint_label", "joint_region", "motion", "spans"])
        act_n = 0
        for m in muscles:
            spans = graph.spanned_by(m.get("attachments"))
            scopes = [("consensus", m)] + [(occ_taxon(o), o) for o in m.get("occurrences", [])]
            for scope, holder in scopes:
                for r in holder.get("actions") or []:
                    jid = r.get("joint")
                    j = joint_by_id.get(jid, {})
                    w.writerow([m["id"], m["name"], m.get("region", ""), scope,
                                jid, j.get("label", ""), j.get("region", ""),
                                r.get("motion", ""),
                                "" if not spans or jid in graph.exempt
                                else ("TRUE" if jid in spans else "FALSE")])
                    act_n += 1

    # ---- fusions.csv --------------------------------------------------------
    #
    # Skeletal fusion and fission as one long-format character: one row per
    # compound x component x taxon. `event` is `fusion` where several elements
    # became one and `fission` where one became several, so the two read off the
    # same column and can be counted on the same tree.
    #
    # A fusion is scored in the taxa where the compound is present; a fission in
    # the taxa where the DERIVED element is present, since that is where the
    # split has happened.
    with open(outdir / "fusions.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["event", "compound_id", "compound_label", "component_id",
                    "component_label", "taxon_id", "taxon_order", "region",
                    "segment", "note", "sources"])
        fuse_n = 0
        for e in skel["elements"]:
            p = e.get("presence", {})
            pairs = [("fusion", c) for c in e.get("fusedFrom", [])]
            if e.get("derivedFrom"):
                pairs.append(("fission", e["derivedFrom"]))
            for event, other in pairs:
                for tid in p.get("present", []) or [""]:
                    w.writerow([event, e["id"], e["label"], other,
                                by_id.get(other, {}).get("label", other),
                                tid, taxon_order.get(tid, ""),
                                e.get("region", ""), e.get("segment", ""),
                                p.get("note", ""), ";".join(p.get("sources", []))])
                    fuse_n += 1

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
    print(f"architecture.csv {arch_n} rows")
    print(f"presence.csv     {rows} rows")
    print(f"division.csv     {div_n} rows")
    print(f"parts.csv        {part_n} rows")
    print(f"elements.csv     {len(skel['elements'])} rows")
    print(f"fusions.csv      {fuse_n} rows")
    print(f"innervation.csv  {nerve_n} rows")
    print(f"joints.csv       {joint_n} rows")
    print(f"actions.csv      {act_n} rows")
    print(f"muscles.csv      {len(muscles)} rows")
    print(f"-> {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "export")))
