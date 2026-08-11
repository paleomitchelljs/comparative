#!/usr/bin/env python3
"""Schema and referential-integrity check for the muscle dataset.

Run from the repo root:  python3 scripts/validate.py
Exit status is non-zero if any error is found, so this works as a pre-commit hook.
"""

import json
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jointgraph

ROOT = pathlib.Path(__file__).resolve().parent.parent
MUSCLE_FILES = sorted(ROOT.glob("data/muscles-*.json"))

PRESENCE = {"yes", "no", "variable", "uncertain", "inferred"}
CONFIDENCE = {"well-supported", "moderate", "contested", "uncertain"}
SERIAL_BASIS = {"topological", "developmental", "none"}
LAYERS = {"superficialis", "profundus", "intermediate", "preaxial", "postaxial", "primaxial"}
SEGMENTS = {"cranial", "axial", "girdle", "stylopod", "zeugopod", "autopod", "fin"}

# `region` and `mass` were the two classification fields with no enforced
# vocabulary, and both drifted: `mass` carried a lone "branchial" against
# thirteen "branchiomeric", and SCHEMA.md's region list had fallen behind the
# addition of "axial". Neither is visible until the field becomes a facet, at
# which point a typo renders as its own button.
REGIONS = {"cranial", "axial", "fin", "pectoral", "arm", "forearm", "hand",
           "pelvic", "thigh", "leg", "foot"}
MASSES = {"dorsal", "ventral", "somitic", "somitic-axial", "branchiomeric",
          "extraocular"}

# How far one homology group has been split in one taxon. Ordered: a field that
# is `single` in a salamander, `heads` in a frog and `divided` in a mammal has
# differentiated twice. Absent means unrecorded, never `single` — the same
# distinction `present` draws, and for the same reason.
DIVISION = {"single", "heads", "divided", "variable"}
DIVISION_WITH_PARTS = {"heads", "divided", "variable"}
MEMBERSHIP = {"established", "disputed", "variable"}

errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(path):
    with open(path) as fh:
        return json.load(fh)


def check_nerves(holder, label, nerves_by_id, source_keys):
    """`nerves` is a list of {nerve, segments?, note?} rows.

    Placement follows `attachments`: on the muscle it is the consensus, on an
    occurrence it is what a source records for that taxon.
    """
    rows = holder.get("nerves")
    if rows is None:
        return []
    if not isinstance(rows, list) or not rows:
        err(f"{label}: `nerves` must be a non-empty list")
        return []

    seen, ids = set(), []
    for i, row in enumerate(rows):
        at = f"{label}: nerves[{i}]"
        if not isinstance(row, dict):
            err(f"{at} is not a {{nerve, segments?}} row: {row!r}")
            continue
        nid = row.get("nerve")
        if nid not in nerves_by_id:
            err(f"{at} nerve '{nid}' is not in nerves.json")
            continue
        if nid in seen:
            err(f"{at} repeats nerve '{nid}'")
        seen.add(nid)
        ids.append(nid)
        for key in row.get("sources", []):
            if key not in source_keys:
                err(f"{at} unknown source key '{key}'")
    return ids


def check_occurrence_name(occ, label, muscle):
    """An occurrence `name` names ONE thing in one taxon.

    Where it instead enumerates the taxon's several muscles, that list has a
    structured home already — `parts` for a homology group that has split,
    `derivatives` for an ancestral fin muscle that became several tetrapod ones
    — and writing it twice gives one fact two homes. It also leaks: names are
    indexed at name priority and rendered as the card heading, so a prose list
    of a dozen muscles came back as the top hit for any one of them, under a
    paragraph-long title.

    Warnings, not errors. Several of these need a collective term the sources
    supply and this script cannot invent, so the job is to surface the list, not
    to force a rewrite.
    """
    name = occ.get("name")
    if not name:
        return

    parts = [p.get("name", "") for p in occ.get("parts", []) if isinstance(p, dict)]
    low = name.lower()

    # Re-listing what `parts` already holds. The threshold is three, not two,
    # because naming a muscle after its two heads is how the sources do it —
    # "Triceps brachii (scapulotriceps + humerotriceps)", "Deltoideus, pars
    # acromialis and pars clavicularis" — and those are labels with a
    # parenthetical, not enumerations standing in for one. At three the name has
    # stopped being a name.
    echoed = [p for p in parts if p and p.lower() in low]
    if len(echoed) >= 3:
        warn(f"{label}: name re-lists {len(echoed)} of its own `parts` "
             f"({', '.join(echoed[:3])}{'…' if len(echoed) > 3 else ''}) — "
             f"the parts are the home for that list")
        return

    derived = [d for k in ("pectoral", "pelvic")
               for d in (muscle.get("derivatives", {}) or {}).get(k, [])]
    if derived and sum(1 for d in derived if d.replace("-", " ") in low) >= 2:
        warn(f"{label}: name re-lists this fin muscle's `derivatives` — "
             f"ancestry is curated there and rendered from there")
        return

    # A list shape with no structured home at all: the list is the only record
    # of the split, and nothing can count it.
    if not parts and (low.count(";") >= 2 or low.count(",") >= 2):
        warn(f"{label}: name looks like a list of several muscles but the "
             f"occurrence has no `division`/`parts` to hold them")


def check_division(occ, label, present, muscles, source_keys):
    """How far this homology group is split in this taxon.

    `division` is the scalar; `parts` names the pieces. The pairing is enforced
    both ways, because either half alone is a claim the other contradicts: parts
    without a division state do not say whether they are heads of one muscle or
    separate muscles, and `divided` without parts asserts a split it cannot
    name.
    """
    div = occ.get("division")
    parts = occ.get("parts")

    if div is None and parts is None:
        return

    if div is not None and div not in DIVISION:
        err(f"{label}: division='{div}' not in {sorted(DIVISION)}")
        return

    if parts is not None and div is None:
        err(f"{label}: has `parts` but no `division` state")
    if div == "single" and parts:
        err(f"{label}: division='single' cannot carry `parts`")
    if div in DIVISION_WITH_PARTS and not parts:
        err(f"{label}: division='{div}' but no `parts` listed")

    # Dividing a muscle the source did not find is incoherent.
    if present == "no" and div:
        err(f"{label}: present='no' but division='{div}'")

    if div and not occ.get("sources"):
        warn(f"{label}: division='{div}' with no source cited")

    if not parts:
        return

    if div in {"heads", "divided"} and len(parts) < 2:
        err(f"{label}: division='{div}' needs at least two parts, got {len(parts)}")

    seen = set()
    for i, part in enumerate(parts):
        at = f"{label}: parts[{i}]"
        if not isinstance(part, dict):
            err(f"{at} is not an object: {part!r}")
            continue
        name = part.get("name")
        if not name:
            err(f"{at} has no name")
        elif name in seen:
            err(f"{at} duplicates the name '{name}'")
        else:
            seen.add(name)

        mem = part.get("membership", "established")
        if mem not in MEMBERSHIP:
            err(f"{at} membership='{mem}' not in {sorted(MEMBERSHIP)}")

        # Optional link to this part's own homology-group record, where the
        # dataset has one. A part is a name in a taxon, not a record, so the
        # link stays optional and is never inferred from the name.
        ref = part.get("muscle")
        if ref is not None and ref not in muscles:
            err(f"{at} muscle='{ref}' is not a muscle record")

        for key in part.get("sources", []):
            if key not in source_keys:
                err(f"{at} unknown source key '{key}'")


def main():
    if not MUSCLE_FILES:
        err("no data/muscles-*.json files found")
        return report()

    taxa_doc = load(ROOT / "data/taxa.json")
    sources_doc = load(ROOT / "data/sources.json")
    skeleton_doc = load(ROOT / "data/skeleton.json")
    nerves_doc = load(ROOT / "data/nerves.json")
    joints_doc = load(ROOT / "data/joints.json")

    taxon_ids = {t["id"] for t in taxa_doc["taxa"]}

    # Species are the unit of observation; a clade is a rollup over them.
    species_doc = load(ROOT / "data/species.json")
    species_ids, species_clade = set(), {}
    for sp in species_doc["species"]:
        sid = sp.get("id")
        if sid in species_ids:
            err(f"species.json: duplicate id '{sid}'")
        species_ids.add(sid)
        if sp.get("clade") not in taxon_ids:
            err(f"species.json:{sid}: clade '{sp.get('clade')}' is not a taxon in taxa.json")
        species_clade[sid] = sp.get("clade")
        for field in ("binomial", "clade"):
            if not sp.get(field):
                err(f"species.json:{sid}: missing `{field}`")

    # Every operational taxon needs at least one species, or it can never be
    # rolled up from anything.
    for tid in taxon_ids:
        if tid not in set(species_clade.values()):
            warn(f"taxa.json:{tid}: no species in species.json rolls up into it")
    source_keys = {s["key"] for s in sources_doc["sources"]}
    # Collapsing the list into a set hides a repeated key, and a repeated key is
    # a live bug rather than clutter: the app builds its bibliography as a Map,
    # so the later entry silently wins. That is how the Klinkhamer 2017 record
    # spent a while pointing at a `pdf` filename with `notes: null`, and why the
    # source count read 58, 59, 62 and 63 in four different places.
    if len(source_keys) != len(sources_doc["sources"]):
        seen = set()
        for s in sources_doc["sources"]:
            if s["key"] in seen:
                err(f"sources.json: duplicate key '{s['key']}'")
            seen.add(s["key"])
    element_ids = {e["id"] for e in skeleton_doc["elements"]}
    side_terms = set(skeleton_doc.get("sides", []))
    nerves_by_id = {n["id"]: n for n in nerves_doc["nerves"]}
    joints_by_id = {j["id"]: j for j in joints_doc["joints"]}
    motion_terms = set(joints_doc["motions"])

    # Nerve internal consistency. Nerves are homology groups on the same
    # pattern as skeletal elements: one record, names as per-taxon attributes.
    nerve_kinds = set(nerves_doc["kinds"])
    nerve_divisions = set(nerves_doc["divisions"])
    for n in nerves_doc["nerves"]:
        nid = n.get("id")
        where = f"nerves.json:{nid}"
        if not nid:
            err("nerves.json: a nerve has no id")
            continue
        if n.get("kind") not in nerve_kinds:
            err(f"{where}: kind='{n.get('kind')}' not in {sorted(nerve_kinds)}")
        if n.get("division") and n["division"] not in nerve_divisions:
            err(f"{where}: division='{n['division']}' not in {sorted(nerve_divisions)}")
        parent = n.get("partOf")
        if parent and parent not in nerves_by_id:
            err(f"{where}: partOf '{parent}' is not a nerve")
        for tn in n.get("taxonNames", []):
            for tid in tn.get("taxa", []):
                if tid not in taxon_ids:
                    err(f"{where}: taxonNames lists unknown taxon '{tid}'")
        for k in n.get("sources", []):
            if k not in source_keys:
                err(f"{where}: unknown source key '{k}'")

    for nid in nerves_by_id:
        seen_n, cur = set(), nid
        while cur:
            if cur in seen_n:
                err(f"nerves.json: partOf cycle involving '{nid}'")
                break
            seen_n.add(cur)
            cur = nerves_by_id.get(cur, {}).get("partOf")

    def nerve_division(nid):
        """A nerve's limb-bud division, inherited from its parent — the deep
        branch of the radial is dorsal because the radial is."""
        cur, guard = nid, 0
        while cur and guard < 20:
            n = nerves_by_id.get(cur, {})
            if n.get("division"):
                return n["division"]
            cur, guard = n.get("partOf"), guard + 1
        return None

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

        # taxonNames is the element-level equivalent of a muscle's occurrence
        # names: one element, different names in different taxa. It is what
        # stops a homologous element being split into two rows.
        named = []
        for tn in e.get("taxonNames", []):
            if not tn.get("name"):
                err(f"skeleton.json:{eid}: taxonNames entry without a name")
            for tid in tn.get("taxa", []):
                if tid not in taxon_ids:
                    err(f"skeleton.json:{eid}: taxonNames lists unknown taxon '{tid}'")
                if tid in named:
                    err(f"skeleton.json:{eid}: taxon '{tid}' named more than once")
                named.append(tid)

        df = e.get("derivedFrom")
        if df and df not in element_ids:
            err(f"skeleton.json:{eid}: derivedFrom '{df}' is not an element")

        # `fusedFrom` is the inverse of `derivedFrom`: several elements became
        # one. It must NOT be `partOf`, which the attachment diff reads as
        # containment — that is what made a bird's tarsometatarsal insertion
        # look like a more precise reading of a crocodylian metatarsal one.
        fused = e.get("fusedFrom")
        if fused is not None:
            if not isinstance(fused, list) or not fused:
                err(f"skeleton.json:{eid}: fusedFrom must be a non-empty list")
            else:
                if e.get("partOf"):
                    err(f"skeleton.json:{eid}: has both partOf and fusedFrom — "
                        f"a fusion product is not a part of its components")
                if eid in fused:
                    err(f"skeleton.json:{eid}: fusedFrom includes itself")
                for c in fused:
                    if c not in element_ids:
                        err(f"skeleton.json:{eid}: fusedFrom '{c}' is not an element")
                if len(set(fused)) != len(fused):
                    err(f"skeleton.json:{eid}: fusedFrom repeats a component")
                if not pres.get("present"):
                    warn(f"skeleton.json:{eid}: fusedFrom but presence lists no "
                         f"taxa — a fusion happens somewhere in particular")

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

    # Joint internal consistency. A joint's two sides use exactly the
    # element/side/landmark row form that attachments use, so the same
    # containment rule applies: a landmark must sit inside its element.
    joint_kinds = set(joints_doc["kinds"])
    for j in joints_doc["joints"]:
        jid = j.get("id")
        where = f"joints.json:{jid}"
        if not jid:
            err("joints.json: a joint has no id")
            continue
        if j.get("kind") not in joint_kinds:
            err(f"{where}: kind='{j.get('kind')}' not in {sorted(joint_kinds)}")
        if not j.get("proximal") or not j.get("distal"):
            err(f"{where}: a joint needs both a proximal and a distal side")
        for side_key in ("proximal", "distal"):
            for row in j.get(side_key, []):
                el = row.get("element")
                if el not in element_ids:
                    err(f"{where}: {side_key} element '{el}' is not in skeleton.json")
                    continue
                if row.get("side") and row["side"] not in side_terms:
                    err(f"{where}: {side_key} side '{row['side']}' not in {sorted(side_terms)}")
                lm = row.get("landmark")
                if lm and lm not in element_ids:
                    err(f"{where}: {side_key} landmark '{lm}' is not in skeleton.json")
                elif lm and el not in lineage(lm):
                    err(f"{where}: {side_key} landmark '{lm}' is not part of '{el}'")
        for mo in j.get("motions", []):
            if mo not in motion_terms:
                err(f"{where}: motion '{mo}' not in {sorted(motion_terms)}")
        if not j.get("motions"):
            warn(f"{where}: no motions listed, so no action can point at it")
        for tn in j.get("taxonNames", []):
            for tid in tn.get("taxa", []):
                if tid not in taxon_ids:
                    err(f"{where}: taxonNames lists unknown taxon '{tid}'")
        for k in j.get("sources", []):
            if k not in source_keys:
                err(f"{where}: unknown source key '{k}'")

    graph = jointgraph.build(joints_doc, by_id)

    # partOf must not cycle, or the bone-first drill-down recurses forever.
    for eid in by_id:
        seen, cur = set(), eid
        while cur:
            if cur in seen:
                err(f"skeleton.json: partOf cycle involving '{eid}'")
                break
            seen.add(cur)
            cur = by_id.get(cur, {}).get("partOf")

    # fusedFrom must not cycle either, and a component cannot be absent from a
    # taxon that has the compound: a bird cannot have a tarsometatarsus without
    # having the metatarsals that went into it.
    def fusion_walk(eid, seen):
        if eid in seen:
            err(f"skeleton.json: fusedFrom cycle involving '{eid}'")
            return
        for c in by_id.get(eid, {}).get("fusedFrom", []):
            fusion_walk(c, seen | {eid})

    for eid, e in by_id.items():
        if not e.get("fusedFrom"):
            continue
        fusion_walk(eid, set())
        for tid in e.get("presence", {}).get("present", []):
            for c in e["fusedFrom"]:
                if not present_in(c, tid):
                    err(f"skeleton.json:{eid}: fused from '{c}', which is "
                        f"recorded as absent in {tid}")

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

        # An occurrence is one SPECIES observed by one set of sources. The clade
        # it rolls up into is derived from species.json and is never stored — a
        # muscle may therefore carry several rows for one clade (Gallus, the
        # ostrich, the tinamou, a penguin), and their agreement or disagreement
        # is what produces the clade's presence state.
        seen_species = Counter()
        for occ in m.get("occurrences", []):
            sid = occ.get("species")
            if sid not in species_ids:
                err(f"{where}: occurrence references unknown species '{sid}'")
                continue
            tid = species_clade[sid]
            seen_species[sid] += 1

            check_rows(occ.get("attachments", {}), f"{where}/{sid}", taxon=tid)

            arch = occ.get("architecture")
            if arch:
                for k in arch.get("sources", []):
                    if k not in source_keys:
                        err(f"{where}/{tid}: architecture unknown source key '{k}'")
                if not arch.get("sources"):
                    err(f"{where}/{tid}: architecture block with no source")
                if not arch.get("species"):
                    warn(f"{where}/{tid}: architecture with no sampled species")
                for part in arch.get("parts", []):
                    for metric in ("mass_g", "fascicleLength_mm", "pcsa_cm2",
                                   "pennation_deg", "maxIsometricForce_N"):
                        v = part.get(metric)
                        if v is not None and not isinstance(v.get("mean"), (int, float)):
                            err(f"{where}/{tid}: architecture {part.get('name')}.{metric} has no numeric mean")
            if occ.get("attachments") and not occ.get("sources"):
                warn(f"{where}/{tid}: taxon-specific attachments with no source")

            pres = occ.get("present", "yes")
            if pres not in PRESENCE:
                err(f"{where}/{tid}: present='{pres}' not in {sorted(PRESENCE)}")

            check_division(occ, f"{where}/{sid}", pres, muscles, source_keys)
            check_occurrence_name(occ, f"{where}/{sid}", m)
            check_nerves(occ, f"{where}/{sid}", nerves_by_id, source_keys)

            if pres != "no" and not occ.get("sources"):
                warn(f"{where}/{tid}: present but no source cited")

            for key in occ.get("sources", []):
                if key not in source_keys:
                    err(f"{where}/{tid}: unknown source key '{key}'")

            # A present muscle should be named in that taxon, else the row says
            # nothing — UNLESS it has no single name there to give. An ancestral
            # fin muscle present in a tetrapod is the field that became several
            # muscles, and those several are in `derivatives`. Demanding a name
            # is what put a prose list of them in this slot in the first place.
            subdivided = any((m.get("derivatives") or {}).get(k)
                             for k in ("pectoral", "pelvic"))
            if pres in {"yes", "inferred"} and not occ.get("name") and not subdivided:
                warn(f"{where}/{tid}: present='{pres}' but no local name given")

        for sid, n in seen_species.items():
            if n > 1:
                err(f"{where}: species '{sid}' appears in {n} occurrence rows")

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

        region = m.get("region")
        if region and region not in REGIONS:
            err(f"{where}: region='{region}' not in {sorted(REGIONS)}")

        # The whole reason to structure innervation: a limb muscle's nerve
        # should sit in the division of the plexus matching its limb-bud mass.
        # Where it does not, either the mass or the nerve is wrong, or the
        # muscle is a genuinely interesting exception — all three are worth
        # surfacing, so this warns rather than erroring.
        # `actions` point at joints. A muscle can only act on a joint it spans,
        # and the joint graph knows which those are from the attachments — so
        # this is one half of the data checking the other, with nothing
        # asserted twice. Serial joints (intervertebral, interphalangeal) form
        # no graph edge and are exempt; a muscle with no consensus attachments
        # cannot be checked at all.
        act_rows = m.get("actions")
        if act_rows is not None:
            if not isinstance(act_rows, list) or not act_rows:
                err(f"{where}: `actions` must be a non-empty list")
                act_rows = []
            spans = graph.spanned_by(m.get("attachments"))
            for i, row in enumerate(act_rows):
                at = f"{where}: actions[{i}]"
                if not isinstance(row, dict):
                    err(f"{at} is not a {{joint, motion}} row: {row!r}")
                    continue
                jid, motion = row.get("joint"), row.get("motion")
                if jid not in joints_by_id:
                    err(f"{at} joint '{jid}' is not in joints.json")
                    continue
                if motion not in motion_terms:
                    err(f"{at} motion='{motion}' not in {sorted(motion_terms)}")
                # `stabilisation` is resisting movement rather than a direction
                # of it, so it applies to any joint and is not listed per joint.
                elif motion != "stabilisation" and \
                        motion not in joints_by_id[jid].get("motions", []):
                    warn(f"{at} '{motion}' is not listed among the motions of "
                         f"'{jid}'")
                if spans and jid not in spans and jid not in graph.exempt:
                    warn(f"{at} acts on '{jid}' but its attachments do not span "
                         f"it (spans: {', '.join(sorted(spans)) or 'nothing'})")

        nerve_ids = check_nerves(m, where, nerves_by_id, source_keys)
        if m.get("mass") in {"dorsal", "ventral"} and nerve_ids:
            divs = {nerve_division(n) for n in nerve_ids}
            divs.discard(None)
            if divs and m["mass"] not in divs:
                warn(f"{where}: mass='{m['mass']}' but its nerves are "
                     f"{sorted(divs)} division ({', '.join(nerve_ids)})")

        mass = m.get("mass")
        if mass and mass not in MASSES:
            err(f"{where}: mass='{mass}' not in {sorted(MASSES)}")

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
