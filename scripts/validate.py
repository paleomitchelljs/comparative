#!/usr/bin/env python3
"""Schema and referential-integrity check for the muscle dataset.

Run from the repo root:  python3 scripts/validate.py
Exit status is non-zero if any error is found, so this works as a pre-commit hook.
"""

import json
import re
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jointgraph
# One definition of "which sources does this record lean on", shared with the
# seed that writes homology.authority, so the check and the seed cannot drift.
from seed_homology_authority import cited_keys as cited_source_keys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MUSCLE_FILES = sorted(ROOT.glob("data/muscles-*.json"))

PRESENCE = {"yes", "no", "variable", "uncertain", "inferred"}
CONFIDENCE = {"well-supported", "moderate", "contested", "uncertain"}
SERIAL_BASIS = {"topological", "developmental", "none"}

# How an occurrence was attributed to its species. `generalised` is the honest
# answer for a source that describes a clade rather than an animal — Winterbottom's
# teleost synonymy reconciles names across the group and dissects nobody. Those
# rows used to claim `source`, which the schema defines as citing a single-species
# study, so the one basis that means "this is not an observation of any one animal"
# was the one being asserted as the opposite.
CORRESPONDENCE = {"serial", "no-counterpart", "descends-from", "corresponds-to-part-of"}
CORRESPONDENCE_AXES = {"forelimb-hindlimb", "pharyngeal-arch"}

SPECIES_BASIS = {"note", "source", "survey", "default", "generalised"}
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

# Terms that only make sense of a human, or that presuppose a human vertebral
# count. A spinal ROOT level is the clearest tell: no source in this
# bibliography states one, and the roots differ between mammals anyway, so a
# parenthetical "(C5-C6)" on a mustelid is a textbook value, not an observation.
# "T12" as a named vertebra assumes twelve thoracics — Galictis cuja has fifteen
# or sixteen, so the row named a vertebra the animal does not have.
HUMAN_ONLY = re.compile(
    r"\((?:\s*[CTLS]\d\s*[–—-]\s*[CTLS]?\d\s*)\)"      # (C5-C6), (L2-L4)
    r"|\bT1[0-2]\b"                                     # T10-T12
    r"|lateral third of the clavicle"
    r"|deltoid tuberosity"
    r"|iliac fossa"
    r"|anterior (?:superior|inferior) iliac spine"
    r"|\bscaphoid\b|\btrapezium\b|\blinea aspera\b|\bbicipital groove\b",
    re.I)
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


def check_occurrence_name(occ, label, muscle, descendants=()):
    """An occurrence `name` names ONE thing in one taxon.

    Where it instead enumerates the taxon's several muscles, that list has a
    structured home already — `parts` for a homology group that has split,
    `descends-from` correspondences for an ancestral fin muscle that became
    several tetrapod ones
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

    if descendants and sum(1 for d in descendants if d.replace("-", " ") in low) >= 2:
        warn(f"{label}: name re-lists the muscles that descend from this one — "
             f"ancestry is curated on them as `descends-from` and rendered from there")
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

    # `present: "variable"` on a SPECIES row, with attachments scored, is a
    # contradiction: somebody dissected this animal and wrote down where the
    # muscle attached, so its presence in this animal is not variable. Every
    # instance found so far was a clade-wide or mammal-wide generalisation
    # written onto one animal — the same error as the Galictis caudofemoralis
    # and the Ascaphus levator anguli oris. `variable` is a rollup RESULT,
    # computed when species disagree; at species level use yes/no/uncertain and
    # put genuine within-species variation in the note.
    att = occ.get("attachments") or {}
    if present == "variable" and any(att.get(k) for k in ("origin", "insertion")):
        warn(f"{label}: present='variable' but attachments are scored — "
             "variable is a clade rollup, not a species observation; if the "
             "source dissected this animal use yes/no/uncertain")

    # Human anatomy standing in for an animal nobody dissected.
    #
    # The therian rows were seeded with textbook prose — "lateral third of the
    # clavicle", "deltoid tuberosity", "Axillary nerve (C5-C6)", "flexor
    # retinaculum, scaphoid and trapezium" — and given whichever paper was
    # associated with the clade as a citation. That pairing is bibliographic, not
    # evidential, and three mechanical passes then treated it as evidence: the
    # attachment seed transcribed the prose into element ids and inherited the
    # citation, and attribute_species.py read the citation to assign a SPECIES.
    # So a human sentence acquired a mustelid's name and a `speciesBasis` of
    # "source". Ercoli et al. (2014) never writes "clavicle"; Ercoli et al.
    # (2012) never writes "nerve". `homo-sapiens` has no occurrences and the
    # bibliography holds no human source, so nothing here can legitimately carry
    # a human-only landmark or a spinal root level.
    if occ.get("species") != "homo-sapiens":
        for field in ("origin", "insertion", "innervation", "action"):
            v = occ.get(field)
            if not isinstance(v, str):
                continue
            hit = HUMAN_ONLY.search(v)
            if hit:
                warn(f"{label}: {field} uses human-specific anatomy "
                     f"('{hit.group(0)}') on a non-human row — check it against "
                     "the cited source rather than a textbook")

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


unsourced: list = []


def part_names(muscle):
    """Every part name this record uses anywhere. A correspondence may address a
    part, and a part is a name in a taxon rather than a record, so the check is
    that some occurrence somewhere names it."""
    return {p.get("name") for o in muscle.get("occurrences", [])
            for p in (o.get("parts") or []) if p.get("name")}


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
    generalised_species = set()
    for sp in species_doc["species"]:
        sid = sp.get("id")
        if sid in species_ids:
            err(f"species.json: duplicate id '{sid}'")
        species_ids.add(sid)
        # A record standing for a clade rather than an animal has to say so, or
        # it reads as a specimen in every view and every export.
        if sp.get("generalised"):
            generalised_species.add(sid)
            if sp.get("fossil"):
                err(f"species.json:{sid}: generalised and fossil together is not "
                    f"a claim this schema can carry")
        elif "(generalised)" in (sp.get("binomial") or ""):
            err(f"species.json:{sid}: binomial says generalised but the record "
                f"is not flagged `generalised: true`")
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
    source_year = {s["key"]: s.get("year") for s in sources_doc["sources"]}
    # Sources whose stated purpose includes establishing homology, synonymy or
    # nomenclature across more than one taxon. Only these can adjudicate what a
    # muscle IS; any source at all can report where it attaches.
    homology_scope_keys = {s["key"] for s in sources_doc["sources"]
                           if s.get("homologyScope")}
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

    # Ancestry is stored on the descendant, so "what did this fin muscle become"
    # is a reverse lookup. Build it once: ancestor id -> the muscles naming it.
    descendants_of = {}
    for mid, (m, _) in muscles.items():
        for e in ((m.get("homology") or {}).get("correspondences") or []):
            if e.get("relation") == "descends-from" and e.get("to"):
                descendants_of.setdefault(e["to"], []).append(mid)

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

            # A clade-level placeholder and a real animal must not be able to
            # pass for one another in either direction.
            basis = occ.get("speciesBasis")
            if basis is not None and basis not in SPECIES_BASIS:
                err(f"{where}/{sid}: speciesBasis='{basis}' not in {sorted(SPECIES_BASIS)}")
            is_gen = sid in generalised_species
            if is_gen and basis != "generalised":
                err(f"{where}/{sid}: '{sid}' is a clade-level generalisation, so its "
                    f"speciesBasis must be 'generalised', not '{basis}'")
            if basis == "generalised" and not is_gen:
                err(f"{where}/{sid}: speciesBasis='generalised' but '{sid}' is a real "
                    f"species — say which basis actually attributed it")

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
            check_occurrence_name(occ, f"{where}/{sid}", m, descendants_of.get(mid, ()))
            check_nerves(occ, f"{where}/{sid}", nerves_by_id, source_keys)

            if pres != "no" and not occ.get("sources"):
                warn(f"{where}/{tid}: present but no source cited")

            for key in occ.get("sources", []):
                if key not in source_keys:
                    err(f"{where}/{tid}: unknown source key '{key}'")

            # A present muscle should be named in that taxon, else the row says
            # nothing — UNLESS it has no single name there to give. An ancestral
            # fin muscle present in a tetrapod is the field that became several
            # muscles, and those several name it with `descends-from`. Demanding a name
            # is what put a prose list of them in this slot in the first place.
            subdivided = bool(descendants_of.get(mid))
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

        # Whose homology scheme this record follows.
        #
        # An attachment is an observation and does not age: Cunningham's 1882
        # thylacine origin is worth exactly what a 2021 one is, and two workers
        # who dissected two animals cannot conflict. A homology is an
        # interpretation and does age, because the later worker had the earlier
        # one in front of them. So `authority` is the most recent source cited on
        # the record whose stated purpose includes homology across more than one
        # taxon, and it is DERIVED — if it drifts from what the sources support,
        # the seed is stale and this errors rather than warns.
        auth = hom.get("authority")
        candidates = homology_scope_keys & cited_source_keys(m)
        if auth is not None:
            if not isinstance(auth, dict):
                err(f"{where}: homology.authority is not a {{source, basis}} block")
            else:
                key, basis = auth.get("source"), auth.get("basis")
                if key not in source_keys:
                    err(f"{where}: homology.authority unknown source key '{key}'")
                elif key not in homology_scope_keys:
                    err(f"{where}: homology.authority names '{key}', which is not "
                        f"flagged `homologyScope` in sources.json — a description "
                        f"of one animal cannot adjudicate a homology")
                if basis not in {"computed", "curated"}:
                    err(f"{where}: homology.authority.basis='{basis}' "
                        f"not in ['computed', 'curated']")
                elif basis == "computed":
                    if candidates:
                        best = max(candidates,
                                   key=lambda k: (source_year.get(k) or 0, k))
                        if key != best:
                            err(f"{where}: homology.authority is '{key}' but the "
                                f"most recent homology-scope source cited here is "
                                f"'{best}' — run "
                                f"scripts/seed_homology_authority.py --write, or "
                                f"set basis='curated' with a note saying why the "
                                f"older scheme is followed")
                    else:
                        err(f"{where}: homology.authority='{key}' is not cited "
                            f"anywhere on this record")
                elif not (auth.get("note") or "").strip():
                    err(f"{where}: homology.authority.basis='curated' needs a "
                        f"`note` saying why this record follows an older scheme "
                        f"than the most recent homology-scope source it cites")
        elif candidates:
            err(f"{where}: cites homology-scope sources but has no "
                f"homology.authority — run scripts/seed_homology_authority.py")
        else:
            # Not a defect in itself, but worth surfacing: nothing cited here
            # was written to settle what this muscle is.
            warn(f"{where}: no homology-scope source cited — its homology rests "
                 f"on descriptive sources alone")

        # `homology.correspondences` — typed homology claims between records.
        # This replaced `derivatives` and `homology.serial`, which could express
        # one relation each and neither could carry a source, a clade scope or a
        # part. `related` survives alongside it and means something different:
        # topological adjacency, untyped, with no claim attached.
        for i, e in enumerate(hom.get("correspondences", []) or []):
            at = f"{where}: correspondences[{i}]"
            rel_kind = e.get("relation")
            if rel_kind not in CORRESPONDENCE:
                err(f"{at}: relation='{rel_kind}' not in {sorted(CORRESPONDENCE)}")
                continue

            # `no-counterpart` asserts there is nothing to point at, so it is the
            # one relation with no `to`. Everything else must resolve.
            if rel_kind == "no-counterpart":
                if e.get("to"):
                    err(f"{at}: 'no-counterpart' asserts an absence and must not carry `to`")
            else:
                ref = e.get("to")
                if not ref:
                    err(f"{at}: '{rel_kind}' needs a `to`")
                elif ref not in muscles:
                    err(f"{at}: `to` points at unknown muscle '{ref}'")
                elif ref == mid:
                    err(f"{at}: `to` is this record itself — a part that subdivides "
                        f"differently between taxa of one record is a division fact, "
                        f"and belongs in `parts` and `divisionNote`")

            if rel_kind in {"serial", "no-counterpart"}:
                if e.get("axis") not in CORRESPONDENCE_AXES:
                    err(f"{at}: axis='{e.get('axis')}' not in {sorted(CORRESPONDENCE_AXES)}")
            elif e.get("axis"):
                err(f"{at}: `axis` is only meaningful on 'serial' and 'no-counterpart'")

            basis = e.get("basis")
            if basis and basis not in SERIAL_BASIS:
                err(f"{at}: basis='{basis}' not in {sorted(SERIAL_BASIS)}")
            conf = e.get("confidence")
            if conf and conf not in CONFIDENCE:
                err(f"{at}: confidence='{conf}' not in {sorted(CONFIDENCE)}")
            for k in e.get("sources", []):
                if k not in source_keys:
                    err(f"{at}: unknown source key '{k}'")
            for tx in e.get("taxa", []):
                if tx not in taxon_ids:
                    err(f"{at}: taxa '{tx}' is not in taxa.json")

            # A correspondence is a homology claim, so it ages and it ought to
            # say whose it is. The edges migrated out of `homology.serial` and
            # `derivatives` have none — they inherited their record's blanket
            # `sources` and nobody ever attributed the individual claim. That is
            # a real backlog and it is reported once, with a count, rather than
            # as one warning per edge: they all have the same fix, and ninety of
            # them would bury every other warning in the run.
            if not e.get("sources"):
                unsourced.append(f"{mid}:{rel_kind}->{e.get('to') or e.get('axis')}")

            for side in ("fromPart", "toPart"):
                name = e.get(side)
                if not name:
                    continue
                owner = mid if side == "fromPart" else e.get("to")
                if owner in muscles and not part_names(muscles[owner][0]) & {name}:
                    err(f"{at}: {side} '{name}' is not a part named on any occurrence "
                        f"of '{owner}'")

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

    if unsourced:
        warn(f"{len(unsourced)} homology correspondences carry no `sources` — "
             f"migrated from `homology.serial` and `derivatives`, which had no "
             f"per-edge attribution. e.g. {', '.join(sorted(unsourced)[:3])}")

    # Reciprocity. `serial` is symmetric and gets an error, because
    # symmetrise_links.py writes the reverse edge and a missing one means the
    # build was not run. `descends-from` and `corresponds-to-part-of` are
    # directed and must NOT be reciprocated — reversing them reverses the claim.
    for mid, (m, rel) in muscles.items():
        for e in (m.get("homology", {}).get("correspondences") or []):
            if e.get("relation") != "serial":
                continue
            other = muscles.get(e.get("to"))
            if not other:
                continue
            back = [b for b in (other[0].get("homology", {}).get("correspondences") or [])
                    if b.get("relation") == "serial" and b.get("to") == mid
                    and b.get("axis") == e.get("axis")]
            if not back:
                err(f"{rel}:{mid}: serial '{e.get('to')}' on axis '{e.get('axis')}' "
                    f"does not link back — run symmetrise_links.py --write")

    # A contested part names the record contesting it, and that record has to
    # know. Without this, `membership: \"disputed\"` records that a dispute
    # exists and never who with, which is how the gemelli and the tensor tympani
    # both ended up carrying their other claimant in a sentence.
    for mid, (m, rel) in muscles.items():
        for occ in m.get("occurrences", []):
            for p in (occ.get("parts") or []):
                other_id = p.get("claimedBy")
                if not other_id:
                    continue
                if p.get("membership") != "disputed":
                    err(f"{rel}:{mid}/{occ.get('species')}: part '{p.get('name')}' has "
                        f"`claimedBy` but membership is not 'disputed'")
                if other_id not in muscles:
                    err(f"{rel}:{mid}/{occ.get('species')}: part '{p.get('name')}' "
                        f"claimedBy unknown muscle '{other_id}'")
                    continue
                if other_id == mid:
                    err(f"{rel}:{mid}/{occ.get('species')}: part '{p.get('name')}' "
                        f"claimedBy itself")
                    continue
                linked = any(
                    e.get("relation") == "corresponds-to-part-of"
                    and {e.get("to"), owner} == {mid, other_id}
                    for owner, side in ((mid, m), (other_id, muscles[other_id][0]))
                    for e in (side.get("homology", {}).get("correspondences") or []))
                if not linked:
                    err(f"{rel}:{mid}/{occ.get('species')}: part '{p.get('name')}' is "
                        f"claimedBy '{other_id}', but neither record carries a "
                        f"`corresponds-to-part-of` edge between them — the dispute is "
                        f"asserted on one side only")

    # Reciprocity: if A lists B as related, B should list A. Cheap way to keep the graph sane.
    for mid, (m, rel) in muscles.items():
        for ref in m.get("homology", {}).get("related", []):
            other = muscles.get(ref)
            if other and mid not in other[0].get("homology", {}).get("related", []):
                warn(f"{rel}:{mid}: related '{ref}' does not link back")

    cited = {
        k
        for m, _ in muscles.values()
        for k in list(m.get("sources", []))
        + [s for o in m.get("occurrences", []) for s in o.get("sources", [])]
    }
    # skeleton.json cites too, and a source used only there is mined, not pending.
    # Pereyra et al. (2019) is the case that surfaced this: it yields no muscle rows
    # at all, only evidence for what `correlate` asserts, so scanning muscles alone
    # left it on the worklist permanently.
    cited |= {
        k
        for e in skeleton_doc["elements"]
        for k in (e.get("presence") or {}).get("sources", []) or []
    }
    for key in sorted(source_keys - cited):
        warn(f"sources.json: '{key}' is never cited")

    # A mined source with no reading note is the gap that is invisible from
    # inside the data: the rows look complete, and the record of what the paper
    # actually says exists nowhere in the repository. Every cited source has one
    # as of this check being written, so this warns on regression rather than on
    # a backlog. An uncited source is exempt — it is a promise, not yet a debt.
    for key in sorted(cited):
        src = next((s for s in sources_doc["sources"] if s["key"] == key), {})
        rel = src.get("notes")
        if not rel:
            warn(f"sources.json: '{key}' is cited but has no `notes` reading note")
        elif not (ROOT / rel).exists():
            err(f"sources.json: '{key}' notes -> '{rel}', which does not exist")

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
