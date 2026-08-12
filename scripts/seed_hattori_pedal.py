#!/usr/bin/env python3
"""Hattori & Tsuihiji (2021), the dorsal pedal musculature of four sauropsid clades.

Top of the citation-derived ranking in docs/MINING.md: 9.7 origin/insertion
mentions per page over 35 pages, four citations here and three scored rows. It
dissects seven animals across every extant sauropsid clade — *Iguana iguana*,
*Varanus indicus*, *Chelydra serpentina*, *Paleosuchus palpebrosus*, *Crocodylus
porosus*, *Gallus gallus* and *Grus japonensis* — and gives origin, insertion,
innervation and an osteological correlate for each of 26 pedal muscles. This
script takes the dorsal half, §3.1.1 to §3.1.13. The plantar half, §3.2, is 16
more muscles in the same structure and is left for a second pass.

What makes it worth a script rather than a note:

* **The paper's headline homology revision was already recorded here and its
  evidence was not.** `tibialis-anterior` and `extensor-digitorum-longus-hl` both
  carry the argument that the avian and non-avian assignments are swapped — avian
  m. tibialis cranialis homologous with non-avian m. extensor digitorum longus,
  avian m. extensor digitorum longus with non-avian m. tibialis anterior — and
  both had the Struthio rows at `uncertain` with nothing underneath. The
  attachments that argument turns on are now scored in seven animals. Hattori &
  Tsuihiji's case is that the classical scheme needs the extensor digitorum
  longus origin to jump the knee joint and the tibialis cranialis to lose its MT
  I insertion, and theirs needs neither; the rows below are where that is
  checkable. The Struthio rows stay `uncertain`.

* **A second revision with nowhere to live.** The muscles running from one
  metatarsal onto the digit lateral to it have been read as part of the short
  digital extensors in lepidosaurs and turtles (Walker 1973; Russell & Bauer
  2008). Hattori & Tsuihiji separate them: distinct slips, stout tendons, a
  consistent origin one metatarsal medial to the digit of insertion, and in
  crocodilians a distinct innervation. `extensores-digitorum-breves-pes` would
  reproduce the error they correct, and `intermetatarsales` is a different muscle
  — metatarsal to metatarsal, web-forming, lateral plantar nerve. Hence a new
  record, `interossei-dorsales-pes`.

* **Three orphan correlates close.** `GAPS.md` §3 lists fifteen osteological
  correlates carrying no muscle. The avian tibialis cranialis takes the cranial
  and lateral cnemial crests, and the avian m. abductor digiti II takes the fossa
  metatarsi I. Those are landmarks a palaeontologist reads first, and the dataset
  said nothing about what pulled on them.

* **Two species per clade, and the sameness is data.** Hattori & Tsuihiji
  describe Iguana with Varanus, Paleosuchus with Crocodylus and Gallus with Grus,
  and where they record no difference that is an observation of sameness in two
  animals rather than a description of one. Both get rows, on the precedent of
  Zaaf's two geckos in `GAPS.md` §6. Where they do distinguish — and they do for
  the tibialis anterior origin and the short extensor slips in the two squamates
  — the rows differ.

    python3 scripts/seed_hattori_pedal.py           # report
    python3 scripts/seed_hattori_pedal.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "hattori-tsuihiji-2021"
FILE = ROOT / "data/muscles-hindlimb.json"

IGU, VAR = "iguana-iguana", "varanus-indicus"
CHE = "chelydra-serpentina"
PAL, CRO = "paleosuchus-palpebrosus", "crocodylus-porosus"
GAL, GRU = "gallus-domesticus", "grus-japonensis"

MANAGED = ("name", "present", "origin", "insertion", "action", "innervation",
           "note", "attachmentNote", "attachments", "division", "parts",
           "partsOpen", "divisionNote", "sources")


def o(element, side=None, landmark=None):
    row = {"element": element}
    if side:
        row["side"] = side
    if landmark:
        row["landmark"] = landmark
    return row


def p(name, membership=None, note=None):
    row = {"name": name}
    if membership:
        row["membership"] = membership
    if note:
        row["note"] = note
    return row


D, V = "disputed", "variable"

# Hattori & Tsuihiji dissected these in pairs and report no difference for most
# muscles. The second row of a pair says so rather than repeating the argument.
PAIRED = ("Hattori & Tsuihiji describe this animal together with its clade-mate "
          "and record no difference between the two for this muscle. A blank in "
          "a comparison is an observation of sameness, which is why both carry "
          "rows rather than one standing for the clade.")

NEW_RECORD = {
    "id": "interossei-dorsales-pes",
    "name": "Interossei dorsales (pes)",
    "region": "foot",
    "subregion": "deep dorsal intrinsic layer",
    "segment": "autopod",
    "mass": "dorsal",
    "layer": "profundus",
    "developmental": "Somitic; deep dorsal mass of the pes.",
    "synonyms": [
        "mm. interossei dorsales digiti II-IV (Hattori & Tsuihiji 2021)",
        "part of mm. extensores breves (Russell & Bauer 2008, for lepidosaurs)",
        "part of mm. interossei dorsales (Walker 1973, for turtles)",
        "m. abductor digiti II (Aves; Vanden Berge & Zweers 1993)",
    ],
    "consensus": {
        "origin": "Dorsal or lateroplantar aspect of the metatarsal one position medial to the digit of insertion.",
        "insertion": "Proximodorsal lip of the phalanges of that digit, largely through the dorsal aponeurosis.",
        "action": "Abducts digits II and III and adducts digit IV, if the slips act independently of the short extensors they fuse with distally.",
        "innervation": "Deep fibular nerve; superficial in some crocodilian accounts.",
    },
    "attachments": {
        "origin": [o("metatarsals", "dorsal")],
        "insertion": [o("phalanges-pes", "dorsal")],
    },
    "homology": {
        "confidence": "moderate",
        "notes": (
            "**A series separated from the short digital extensors by Hattori & "
            "Tsuihiji (2021), not a renaming of them.** In lepidosaurs and turtles "
            "these slips had been described as portions of mm. extensores breves "
            "(Russell & Bauer 2008) or of mm. interossei dorsales without being "
            "distinguished from them (Walker 1973). Their case for a distinct "
            "series is that each slip arises from the proximolateral aspect of the "
            "metatarsal MEDIALLY ADJACENT to the digit it serves, carries a stout "
            "tendon of its own, and forms the medial portion of that digit's "
            "extensor — so most fibres end on the proximomedial margins of the "
            "phalanges and the slips would act as abductors of digits II-III and "
            "an adductor of digit IV. They fuse distally with the short extensors, "
            "which is why they were missed. The distinction was previously unknown "
            "in non-archosaurian sauropsids and is what lets the avian short "
            "extensors be compared with the non-avian ones at all.\n\n"
            "Kept separate from `intermetatarsales`, which runs metatarsal to "
            "metatarsal, forms the interdigital webs and takes the lateral plantar "
            "nerve — a different muscle by attachment and by innervation, not a "
            "different name for this one.\n\n"
            "**Scored so far only from Hattori & Tsuihiji's seven sauropsids**, so "
            "absence elsewhere in this dataset is unsampled rather than observed."
        ),
        "openQuestion": (
            "Only the digit II member survives in birds, as m. abductor digiti II. "
            "Hattori & Tsuihiji reject the avian mm. extensores breves digiti III "
            "and IV as homologues of the digit III and IV members on the grounds "
            "that their tarsometatarsal origins correspond to the wrong metatarsal "
            "and that they extend rather than adduct. Is that a loss of two "
            "muscles, or a fusion into the avian short extensors?"
        ),
        "related": ["extensores-digitorum-breves-pes", "intermetatarsales",
                    "flexores-breves-profundi-pes"],
    },
    "nerves": [{"nerve": "deep-fibular"}],
    "occurrences": [],
}

SEED: list[tuple[str, str, dict]] = []


def add(mid, sid, **spec):
    spec.setdefault("sources", [SRC])
    SEED.append((mid, sid, spec))


# ---------------------------------------------------------------------------
# §3.1.1 m. tibialis cranialis  ->  extensor-digitorum-longus-hl
# ---------------------------------------------------------------------------
_edl_note = ("This is the muscle Hattori & Tsuihiji standardise as m. tibialis "
             "cranialis, and its avian member is the point of the paper: on their "
             "reading the bird's m. tibialis cranialis belongs on THIS record and "
             "not on `tibialis-anterior`, where the classical scheme puts it.")

for sid, name, org, ins, att, extra in [
    (IGU, "Extensor digitorum longus",
     "Dorsomedial aspect of the lateral distal condyle of the femur.",
     "Metatarsals II and III by two tendons, each passing the lateral aspect of the proximal shaft to the tubercle on its lateroplantar aspect.",
     {"origin": [o("femur", "dorsal", "femoral-condyles")],
      "insertion": [o("metatarsals", "lateral")]},
     "Iguana iguana. " + _edl_note),
    (VAR, "Extensor digitorum longus",
     "Dorsomedial aspect of the lateral distal condyle of the femur.",
     "Metatarsals II and III by two tendons, onto the tubercle on the lateroplantar aspect of each proximal shaft.",
     {"origin": [o("femur", "dorsal", "femoral-condyles")],
      "insertion": [o("metatarsals", "lateral")]},
     "Varanus indicus. " + PAIRED),
    (CHE, "Extensor digitorum communis",
     "Dorsal aspect of the lateral distal condyle of the femur.",
     "Lateral sides of metatarsals I-IV and the proximodorsal lip of phalanx I-2.",
     {"origin": [o("femur", "dorsal", "femoral-condyles")],
      "insertion": [o("metatarsals", "lateral"), o("phalanges-pes", "dorsal")]},
     "Chelydra serpentina. The widest insertion of any sauropsid on this record — all four metatarsals — and turtles vary in it: Gadow (1882) put the insertion on the proximal phalanges of digits I-IV instead, and Ribbing (1938) found the Emys condition scored here. " + _edl_note),
    (PAL, "Extensor digitorum longus",
     "Dorsal aspect of the femur just proximal to the lateral distal condyle.",
     "Tubercle on the medial margin of the proximal shaft of each of metatarsals II-IV, merging at the medial-most site with the tibialis anterior.",
     {"origin": [o("femur", "dorsal", "femoral-condyles")],
      "insertion": [o("metatarsals", "medial")]},
     "Paleosuchus palpebrosus. An MT I insertion is reported by Gadow (1882), Ribbing (1909, 1938) and Cong et al. (1998) and was not found here. " + _edl_note),
    (CRO, "Extensor digitorum longus",
     "Dorsal aspect of the femur just proximal to the lateral distal condyle.",
     "Tubercle on the medial margin of the proximal shaft of each of metatarsals II-IV.",
     {"origin": [o("femur", "dorsal", "femoral-condyles")],
      "insertion": [o("metatarsals", "medial")]},
     "Crocodylus porosus. " + PAIRED),
    (GAL, "Tibialis cranialis",
     "Distal extremity of the lateral distal condyle of the femur, at the fovea tendinis m. tibialis cranialis, plus the lateral expansion of the cranial cnemial crest and the dorsoventral expansion of the lateral cnemial crest of the tibia.",
     "Tubercles on the dorsal aspect of the proximal tarsometatarsus — the tuberositas m. tibialis cranialis.",
     {"origin": [o("femur", "distal", "femoral-condyles"),
                 o("tibia", "anterior", "cnemial-crest-cranial"),
                 o("tibia", "lateral", "cnemial-crest-lateral")],
      "insertion": [o("tarsometatarsus", "dorsal")]},
     "Gallus gallus. **The row the homology revision turns on.** Hattori & Tsuihiji place the avian m. tibialis cranialis here, with the non-avian extensor digitorum longus, because the femoral origin is conserved across all four clades and the avian tuberositas on the tarsometatarsus sits where metatarsals II and III would have been. The classical scheme instead pairs it with `tibialis-anterior`, which requires the extensor digitorum longus origin to cross the knee joint and the tibialis cranialis to lose its MT I insertion. The tibial origin, on the two cnemial crests, is the avian addition. Two of the fifteen orphan correlates in GAPS §3 close on this row."),
    (GRU, "Tibialis cranialis",
     "Distal extremity of the lateral distal condyle of the femur and the cranial and lateral cnemial crests of the tibia.",
     "Tubercles on the dorsal aspect of the proximal tarsometatarsus.",
     {"origin": [o("femur", "distal", "femoral-condyles"),
                 o("tibia", "anterior", "cnemial-crest-cranial"),
                 o("tibia", "lateral", "cnemial-crest-lateral")],
      "insertion": [o("tarsometatarsus", "dorsal")]},
     "Grus japonensis. " + PAIRED),
]:
    add("extensor-digitorum-longus-hl", sid, name=name, present="yes",
        origin=org, insertion=ins, innervation="Fibular nerve.",
        attachments=att, attachmentNote=extra)

# ---------------------------------------------------------------------------
# §3.1.2 m. extensor digitorum longus  ->  tibialis-anterior
# ---------------------------------------------------------------------------
for sid, name, org, ins, att, extra in [
    (IGU, "Tibialis anterior",
     "Broad area on the shaft of the tibia — the proximal two-thirds of the dorsal surface and the distal two-thirds of the ventral aspect.",
     "Medial margin of metatarsal I.",
     {"origin": [o("tibia", "dorsal"), o("tibia", "ventral")],
      "insertion": [o("metatarsals", "medial")]},
     "Iguana iguana. The two squamates differ here and the difference is scored rather than averaged: the iguana's dorsal origin stops short of the distal tibia and the monitor's does not."),
    (VAR, "Tibialis anterior",
     "Broad area on the shaft of the tibia, the dorsal surface origin continuing to the distal end of the bone.",
     "Medial margin of metatarsal I.",
     {"origin": [o("tibia", "dorsal")],
      "insertion": [o("metatarsals", "medial")]},
     "Varanus indicus. Against Iguana, the dorsal origin runs the whole length of the tibia."),
    (CHE, "Tibialis anterior",
     "Dorsomedial margin of the tibia, marked on the bone by a rugose longitudinal sulcus.",
     "Proximomedial end of metatarsal I, marked by a tubercle.",
     {"origin": [o("tibia", "medial")],
      "insertion": [o("metatarsals", "medial")]},
     "Chelydra serpentina. Both ends leave a correlate — a sulcus at the origin and a tubercle at the insertion — which is what makes this muscle reconstructable in a fossil turtle."),
    (PAL, "Tibialis anterior",
     "Proximal-most portion of the dorsal aspect of the tibia, marked with surface rugosity that broadens proximodistally on the lateral side.",
     "Bulge on the dorsal aspect of each of metatarsals I and II.",
     {"origin": [o("tibia", "dorsal")],
      "insertion": [o("metatarsals", "dorsal")]},
     "Paleosuchus palpebrosus."),
    (CRO, "Tibialis anterior",
     "Proximal-most portion of the dorsal aspect of the tibia, marked by distinct rugosity.",
     "Bulge on the dorsal aspect of each of metatarsals I and II.",
     {"origin": [o("tibia", "dorsal")],
      "insertion": [o("metatarsals", "dorsal")]},
     "Crocodylus porosus. " + PAIRED),
    (GAL, "Extensor digitorum longus",
     "Broad surface between the cranial and lateral cnemial crests and the dorsolateral aspect of the tibial shaft, tapering distally.",
     "Processes on the proximodorsal lips of the phalanges of digits II-IV.",
     {"origin": [o("tibia", "anterior", "cnemial-crest-cranial"),
                 o("tibia", "lateral", "cnemial-crest-lateral"),
                 o("tibia", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Gallus gallus. The other half of the revision: Hattori & Tsuihiji put the avian m. extensor digitorum longus HERE, with the non-avian tibialis anterior, on the strength of the shared tibial origin. Note what that does to the shared cnemial crests — under their scheme both anterior tibial muscles take them in birds, the tibialis cranialis on the crests' expansions and this one on the surface between them."),
    (GRU, "Extensor digitorum longus",
     "Broad surface between the cranial and lateral cnemial crests and the dorsolateral tibial shaft.",
     "Processes on the proximodorsal lips of the phalanges of digits II-IV.",
     {"origin": [o("tibia", "anterior", "cnemial-crest-cranial"),
                 o("tibia", "lateral", "cnemial-crest-lateral"),
                 o("tibia", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Grus japonensis. " + PAIRED),
]:
    add("tibialis-anterior", sid, name=name, present="yes", origin=org,
        insertion=ins, innervation="Fibular nerve.", attachments=att,
        attachmentNote=extra)

# ---------------------------------------------------------------------------
# §3.1.3 + §3.1.4 m. peroneus longus and brevis  ->  fibularis-group
# ---------------------------------------------------------------------------
_pero_parts = [p("Peroneus (fibularis) longus"), p("Peroneus (fibularis) brevis")]

for sid, name, org, ins, att, extra in [
    (IGU, "Peroneus longus + peroneus brevis",
     "Longus from the lateral femoral epicondyle just distal to the flexor digitorum longus origin; brevis from almost the entire anterior, lateral and medial surfaces of the fibula, over nearly its whole length.",
     "Longus into a depression on the dorsolateral aspect of the shaft of metatarsal V; brevis onto the outer process on the proximolateral margin of metatarsal V.",
     {"origin": [o("femur", "lateral", "femoral-epicondyle-lateral"), o("fibula", "lateral")],
      "insertion": [o("metatarsals", "lateral")]},
     "Iguana iguana. The longus insertion is a depression, against the 'lateral plantar tubercle' of Russell & Bauer (2008) — Hattori & Tsuihiji contradict them on the correlate itself, not on the muscle."),
    (VAR, "Peroneus longus + peroneus brevis",
     "Longus from the lateral femoral epicondyle; brevis from almost the whole fibula.",
     "Longus into a depression on the dorsolateral shaft of metatarsal V; brevis onto the proximolateral margin of metatarsal V.",
     {"origin": [o("femur", "lateral", "femoral-epicondyle-lateral"), o("fibula", "lateral")],
      "insertion": [o("metatarsals", "lateral")]},
     "Varanus indicus. " + PAIRED),
    (CHE, "Peroneus anterior + peroneus brevis",
     "Peroneus anterior — the longus of this record — from the distal half of the dorsal aspect of the fibula, the origin marked by a slightly excavated surface; brevis from the distal end of the fibula.",
     "Peroneus anterior onto the dorsal aspect of the proximolateral margins of metatarsal V and phalanx IV-1; brevis onto the proximal margin of the dorsal aspect of metatarsal V.",
     {"origin": [o("fibula", "dorsal")],
      "insertion": [o("metatarsals", "dorsal"), o("phalanges-pes", "dorsal")]},
     "Chelydra serpentina. The femoral origin the squamates give the longus is gone here — both heads are on the fibula, which is the condition crocodilians share and which Hattori & Tsuihiji use to group the two clades against lepidosaurs and birds."),
    (PAL, "Peroneus longus + peroneus brevis",
     "Longus from almost the entire laterodorsal aspect of the fibula, the surface between the longitudinal ridges on its dorsal and lateral aspects; brevis from the flat laterodorsal surface of the distal two-thirds of the fibular shaft.",
     "Longus merges with the brevis and inserts on the flat surface at its insertion site; brevis on the proximolateral margin of metatarsal V.",
     {"origin": [o("fibula", "lateral"), o("fibula", "dorsal")],
      "insertion": [o("metatarsals", "lateral")]},
     "Paleosuchus palpebrosus. Both origins are bounded by ridges or are flat surfaces, so the fibula records the whole group."),
    (CRO, "Peroneus longus + peroneus brevis",
     "Longus from almost the entire laterodorsal aspect of the fibula; brevis from the laterodorsal aspect of the distal two-thirds of the fibular shaft.",
     "Longus onto the brevis insertion; brevis on the proximolateral margin of metatarsal V.",
     {"origin": [o("fibula", "lateral"), o("fibula", "dorsal")],
      "insertion": [o("metatarsals", "lateral")]},
     "Crocodylus porosus. " + PAIRED),
    (GAL, "Fibularis longus + fibularis brevis",
     "Longus from the proximal margins of the cranial and lateral cnemial crests, the patellar tendon and associated fascia; brevis from most of the interosseal space between tibia and fibula — a narrow surface between two longitudinal ridges on the distal two-thirds of the tibial shaft, and the dorsal surface of the distal half of the fibula.",
     "Longus onto soft tissue, the sustentaculum tarsi and the insertion tendon of the flexor perforatus digiti III; brevis onto a proximal surface near the lateral margin of the hypotarsus, the tuberculum m. fibularis brevis.",
     {"origin": [o("tibia", "anterior", "cnemial-crest-cranial"),
                 o("tibia", "lateral", "cnemial-crest-lateral"),
                 o("tibia", "lateral"), o("fibula", "dorsal")],
      "insertion": [o("tarsometatarsus", "proximal")]},
     "Gallus gallus. **The insertion is different because the bone is gone.** In all three non-avian clades both heads end on metatarsal V; birds have lost it, and Hattori & Tsuihiji read the avian insertions — on the hypotarsus, on soft tissue and on another muscle's tendon — as the consequence. An attachment relocating because its element was lost, which is the same case as the therian supracoracoideus and the coracoid. The longus account is Fujioka's (1962) on Gallus rather than their own dissection."),
    (GRU, "Fibularis longus + fibularis brevis",
     "Longus from the proximal cnemial crests and the patellar tendon; brevis from the interosseal space between tibia and fibula.",
     "Longus onto soft tissue, the sustentaculum tarsi and the flexor perforatus digiti III tendon; brevis near the lateral margin of the hypotarsus.",
     {"origin": [o("tibia", "anterior", "cnemial-crest-cranial"),
                 o("tibia", "lateral", "cnemial-crest-lateral"),
                 o("fibula", "dorsal")],
      "insertion": [o("tarsometatarsus", "proximal")]},
     "Grus japonensis. " + PAIRED),
]:
    add("fibularis-group", sid, name=name, present="yes", origin=org,
        insertion=ins, attachments=att, attachmentNote=extra,
        division="divided", parts=_pero_parts)

# ---------------------------------------------------------------------------
# §3.1.5 m. adductor hallucis dorsalis  ->  abductor-et-extensor-digiti-i-pes
# ---------------------------------------------------------------------------
for sid, name, org, ins, att, extra, pres in [
    (IGU, "Adductor et extensor hallucis et indicus",
     "A broad, flat or slightly depressed surface on the dorsolateral aspect of the distal fibula, and the medial half of a slight convex lip at the proximolateral margin of the tarsal facet of the astragalocalcaneum.",
     "Medial margin and laterodistal shaft of metatarsal I, and metatarsal II.",
     {"origin": [o("fibula", "lateral"), o("astragalocalcaneum", "lateral")],
      "insertion": [o("metatarsals", "medial")]},
     "Iguana iguana. The record's name comes from Russell & Bauer's for this muscle, so this is the animal it was named from.", "yes"),
    (VAR, "Adductor et extensor hallucis et indicus",
     "Dorsolateral aspect of the distal fibula and the proximolateral margin of the tarsal facet of the astragalocalcaneum.",
     "Metatarsal I only, the insertion marked by rugosity on the bone.",
     {"origin": [o("fibula", "lateral"), o("astragalocalcaneum", "lateral")],
      "insertion": [o("metatarsals", "medial")]},
     "Varanus indicus. **The insertion is narrower than the iguana's** — MT I alone, where Iguana takes MT I and MT II, and Chamaeleo takes only MT II (Russell & Bauer 2008). Three squamates, three different digits for one muscle, which is the position-versus-identity question asked inside a clade.", "yes"),
    (CHE, "Extensor hallucis proprius",
     "Distal end of the fibula, the origin marked as a clear depression on the distodorsal margin of the bone, and the dorsal aspect of the astragalocalcaneum.",
     "Lateral sides of the distal third of metatarsal I and the proximal half of phalanx I-1, and the medial side of the mid-shaft of I-1.",
     {"origin": [o("fibula", "distal"), o("astragalocalcaneum", "dorsal")],
      "insertion": [o("metatarsals", "lateral"), o("phalanges-pes", "medial")]},
     "Chelydra serpentina. The tarsal origin is absent in Trachemys (Walker 1973), so it varies within turtles.", "yes"),
    (PAL, "Adductor hallucis dorsalis",
     "Dorsal aspect of the distal fibula.",
     "Dorsal aspect of the proximal third of the shaft of metatarsal I, just proximal to the tibialis anterior insertion; the distal border of the insertion is marked by a transverse ridge on metatarsal I.",
     {"origin": [o("fibula", "dorsal")],
      "insertion": [o("metatarsals", "dorsal")]},
     "Paleosuchus palpebrosus. No tarsal origin here, unlike the squamates and the turtle.", "yes"),
    (CRO, "Adductor hallucis dorsalis",
     "Dorsal aspect of the distal fibula.",
     "Dorsal aspect of the proximal third of metatarsal I, bounded distally by a transverse ridge.",
     {"origin": [o("fibula", "dorsal")],
      "insertion": [o("metatarsals", "dorsal")]},
     "Crocodylus porosus. Suzuki et al. (2011) described the insertion as divided into two sites in this species; Hattori & Tsuihiji dissected the same species and did not find the division, and read the disagreement as intraspecific variation rather than error.", "yes"),
    (GAL, "Adductor hallucis dorsalis", None, None, None,
     "Gallus gallus. Absent. Hutchinson (2002) treated this muscle as the homologue of the avian m. extensor hallucis longus; Hattori & Tsuihiji reject that and place the avian muscle with the extensor hallucis brevis instead, on `extensores-digitorum-breves-pes`. So the absence here is a positive claim about where the avian muscle went, not silence.", "no"),
    (GRU, "Adductor hallucis dorsalis", None, None, None,
     "Grus japonensis. Absent, as in Gallus.", "no"),
]:
    kw = {"name": name, "present": pres, "note": extra}
    if pres != "no":
        kw.update(origin=org, insertion=ins, attachments=att,
                  innervation="Deep fibular nerve.")
        kw["attachmentNote"] = kw.pop("note")
    add("abductor-et-extensor-digiti-i-pes", sid, **kw)

# ---------------------------------------------------------------------------
# §3.1.6-§3.1.10 short dorsal extensors  ->  extensores-digitorum-breves-pes
# ---------------------------------------------------------------------------
_sb = [p("Extensor digitorum brevis"), p("Extensor hallucis brevis"),
       p("Extensor digiti II"), p("Extensor digiti III"), p("Extensor digiti IV")]

for sid, name, org, ins, att, extra, parts, pres in [
    (IGU, "Extensores digitorum breves",
     "Two proximal heads from the dorsal depression on the astragalus; the hallucal slip from the dorsal aspect of metatarsal I; the digit II, III and IV slips from the dorsal or dorsolateral aspects of metatarsals II, III and the astragalocalcaneum lip respectively.",
     "Proximodorsal lip of each phalanx of digits III and IV from the tarsal heads; the proximodorsal lips of phalanges I-1 and I-2 from the hallucal slip; the proximodorsal lips of the phalanges of digits II and III from their own slips; the ungual of digit IV with accessory insertions on IV-2 to IV-4.",
     {"origin": [o("tarsals", "dorsal", "astragalus"), o("metatarsals", "dorsal"),
                 o("astragalocalcaneum", "lateral")],
      "insertion": [o("phalanges-pes", "dorsal"),
                    o("phalanges-pes", landmark="ungual-phalanges-pes")]},
     "Iguana iguana. Hattori & Tsuihiji's separation of the interossei dorsales out of this complex is what makes the remainder countable; the slips left here are the ones arising from the tarsus or from the digit's OWN metatarsal, and those arising from the metatarsal medial to the digit are on `interossei-dorsales-pes`.",
     _sb, "yes"),
    (VAR, "Extensores digitorum breves",
     "Dorsal depression on the astragalus, with two additional slips beyond the Iguana condition; the digit II and III slips from the dorsal and dorsolateral aspects of metatarsals II and III.",
     "Proximodorsal lips of the phalanges of digits III and IV, and — unlike Iguana — of digits I and II as well; in Varanus an additional tendinous insertion on the medial margin of the distal metatarsal III.",
     {"origin": [o("tarsals", "dorsal", "astragalus"), o("metatarsals", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal"), o("metatarsals", "medial")]},
     "Varanus indicus. **Two more slips than the iguana**, serving digits I and II, which is the second scored difference between Hattori & Tsuihiji's two squamates.",
     _sb, "yes"),
    (CHE, "Extensor digitorum brevis + abductor hallucis",
     "Depression on the dorsal aspect of distal tarsal IV; the hallucal member (m. abductor hallucis) from the dorsal aspect of metatarsal I with an additional origin on phalanx I-1.",
     "Merging distally with the interossei dorsales and inserting with them on the proximodorsal lips of the distal phalanges of digits III and IV; the hallucal member on the proximodorsal lips of I-1 and I-2.",
     {"origin": [o("tarsals", "dorsal", "distal-tarsals"), o("metatarsals", "dorsal"),
                 o("phalanges-pes", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Chelydra serpentina. The tarsal origin is on distal tarsal IV rather than on the astragalus as in squamates and crocodilians — the one place Hattori & Tsuihiji concede the turtle origin is 'slightly different', while still following Gadow (1882) in calling it homologous. Trachemys adds an origin from DT III and an insertion on digit II (Walker 1973). The additional hallucal origin on I-1 is this animal's; Trachemys has it on DT I instead.",
     _sb, "yes"),
    (PAL, "Extensor digitorum I, II et III",
     "Depression on the dorsal aspect of the astragalus; the hallucal slip from the dorsal aspect of metatarsal I; the digit II, III and IV slips from the dorsal surfaces of metatarsals II, III and IV.",
     "Dorsally on digits I-III through the dorsal aponeurosis; the hallucal slip on the proximodorsal lips of I-1 and I-2; each digital slip on the proximodorsal lip of every phalanx of its digit.",
     {"origin": [o("tarsals", "dorsal", "astragalus"), o("metatarsals", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Paleosuchus palpebrosus. Suzuki et al. (2011) kept this muscle separate in crocodilians as m. extensor digitorum I, II et III; Hattori & Tsuihiji propose extensor digitorum brevis as the standard name for it and its homologues, because the digit I-II bellies are sometimes missing in lepidosaurs and the digit IV belly in crocodilians, so a name fixed to a digit list does not travel. In Caiman the origin is not on the astragalus but on soft tissue between it and the calcaneum.",
     _sb, "yes"),
    (CRO, "Extensor digitorum I, II et III",
     "Depression on the dorsal aspect of the astragalus, plus the dorsal surfaces of metatarsals I-IV for the digital slips.",
     "Dorsally on digits I-III by the dorsal aponeurosis, and on the proximodorsal lips of the phalanges of each digit served.",
     {"origin": [o("tarsals", "dorsal", "astragalus"), o("metatarsals", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Crocodylus porosus. " + PAIRED,
     _sb, "yes"),
    (GAL, "Extensores breves digitorum III et IV",
     "Dorsal aspect of the distal half of the tarsometatarsus, the digit III origin marked by a slightly depressed rugose surface and the digit IV origin by a sulcus lateral to it.",
     "Proximodorsal lip of phalanx III-1, and the medial aspect of IV-1 — the latter tendon running through the canalis interosseus distalis and its insertion marked by a tuber.",
     {"origin": [o("tarsometatarsus", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Gallus gallus. **Two members left of five.** The extensor digitorum brevis and the extensor hallucis brevis are both absent in birds, and only the digit III and IV slips survive, both now arising from the tarsometatarsus. Hattori & Tsuihiji use the digit III member as a test case for their metatarsal-identity reasoning: its origin on the middle of the distal half of the tarsometatarsus corresponds to metatarsal III, not to metatarsal II, which is why they refuse it as the homologue of the non-avian interosseous dorsalis digiti III.",
     [p("Extensor brevis digiti III"), p("Extensor brevis digiti IV")], "yes"),
    (GRU, "Extensores breves digitorum III et IV",
     "Dorsal aspect of the distal half of the tarsometatarsus.",
     "Proximodorsal lip of III-1 and the medial aspect of IV-1.",
     {"origin": [o("tarsometatarsus", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Grus japonensis. " + PAIRED,
     [p("Extensor brevis digiti III"), p("Extensor brevis digiti IV")], "yes"),
]:
    add("extensores-digitorum-breves-pes", sid, name=name, present=pres,
        origin=org, insertion=ins, attachments=att, attachmentNote=extra,
        innervation="Deep fibular nerve.", division="divided", parts=parts)

# ---------------------------------------------------------------------------
# §3.1.11-§3.1.13 mm. interossei dorsales  ->  interossei-dorsales-pes (new)
# ---------------------------------------------------------------------------
_io = [p("Interosseous dorsalis digiti II"), p("Interosseous dorsalis digiti III"),
       p("Interosseous dorsalis digiti IV")]

for sid, name, org, ins, att, extra, parts in [
    (IGU, "Interossei dorsales digiti II-IV (as slips of mm. extensores digitores breves)",
     "Ridge-like longitudinal rugose areas: the digit II slip from metatarsal I, the digit III slip tendinously from the lateral margin of the proximal half of metatarsal II, the digit IV slip from the lateral margin of the proximal half of metatarsal III.",
     "Each forms the medial portion of the dorsal aponeurosis of its digit and inserts on the proximodorsal lip of each phalanx; the digit IV slip inserts medially on the proximal margin of each phalanx.",
     {"origin": [o("metatarsals", "lateral")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Iguana iguana. Russell & Bauer (2008) read these as portions of mm. extensores breves; Hattori & Tsuihiji separate them on the rugose longitudinal ridges each arises from, which are visible on the bone and are the correlate for the whole series.",
     _io),
    (VAR, "Interossei dorsales digiti II-III",
     "Ridge-like longitudinal rugose areas on metatarsals I and II.",
     "The medial portion of the dorsal aponeurosis of digits II and III, on the proximodorsal lip of each phalanx; in Varanus an additional tendinous insertion on the medial margin of distal metatarsal III.",
     {"origin": [o("metatarsals", "lateral")],
      "insertion": [o("phalanges-pes", "dorsal"), o("metatarsals", "medial")]},
     "Varanus indicus. The digit IV member was found in Iguana and not here. Russell & Bauer described the digit III belly as arising from the lateral aspect of the DISTAL portion of metatarsal II; Hattori & Tsuihiji find it proximal and treat the difference as intraspecific variation.",
     [p("Interosseous dorsalis digiti II"), p("Interosseous dorsalis digiti III")]),
    (CHE, "Interossei dorsales digiti II-IV",
     "Rugosities on the proximomedial margin of the dorsal aspect of metatarsals I, II and III, the digit II member also from the astragalocalcaneum, distal tarsal I and phalanx II-1, and the digit IV member also from distal tarsal IV and phalanx IV-1.",
     "The distal phalanges of digits II, III and IV by a dorsal aponeurosis.",
     {"origin": [o("metatarsals", "dorsal"), o("astragalocalcaneum", "dorsal"),
                 o("tarsals", "dorsal", "distal-tarsals"), o("phalanges-pes", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Chelydra serpentina. Walker (1973) already used the name mm. interossei dorsales for the turtle series but did not distinguish it from the short extensors it merges with; the accessory origins on the first phalanges are this animal's, and Trachemys lacks several of them.",
     _io),
    (PAL, "Interossei dorsales digiti II-IV",
     "Digit II member from the depression on the lateroplantar aspect of metatarsal I with a stout tendinous structure; digit III member from the rugose surface on the dorsal and lateral aspects of the lateral margin of proximal metatarsal II; digit IV member from the depression on the lateroplantar aspect of the proximal-most shaft of metatarsal III.",
     "Each joins the dorsal aponeurosis of its digit, but most fibres end on the proximodorsal lip of the first phalanx.",
     {"origin": [o("metatarsals", "lateral"), o("metatarsals", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Paleosuchus palpebrosus. The crocodilian members are the clearest of the series: named separately by Suzuki et al. (2011), carrying their own tendons, and — for the digit III member — innervated differently from the short extensors it lies beside. Hattori & Tsuihiji note the digit IV member is absent from Cong et al.'s (1998) account and so is possibly absent in Alligator sinensis.",
     _io),
    (CRO, "Interossei dorsales digiti II-IV",
     "Depressions and rugosities on the lateral aspects of metatarsals I, II and III.",
     "The dorsal aponeurosis of digits II, III and IV, most fibres ending on the proximodorsal lip of the first phalanx of each.",
     {"origin": [o("metatarsals", "lateral"), o("metatarsals", "dorsal")],
      "insertion": [o("phalanges-pes", "dorsal")]},
     "Crocodylus porosus. " + PAIRED,
     _io),
    (GAL, "Abductor digiti II",
     "Lateral aspect of metatarsal I and the dorsomedial aspect of the tarsometatarsus, the tarsometatarsal origin marked by an oblique groove on the medial aspect of the shaft and by the fossa metatarsi I.",
     "Medioplantar tubercle at the proximal end of phalanx II-1.",
     {"origin": [o("metatarsals", "lateral"),
                 o("tarsometatarsus", "medial", "fossa-metatarsi-i")],
      "insertion": [o("phalanges-pes", "proximal")]},
     "Gallus gallus. **One of three members survives in birds, and it closes an orphan correlate.** The digit II member persists as m. abductor digiti II, keeping the metatarsal I origin, the digit II insertion and the deep fibular nerve that identify the series; the digit III and IV members are absent, and Hattori & Tsuihiji explicitly refuse the avian extensores breves digiti III and IV as their homologues because those arise from the wrong metatarsal and extend rather than adduct. The fossa metatarsi I is one of the fifteen osteological correlates GAPS §3 listed as carrying no muscle.",
     [p("Interosseous dorsalis digiti II (m. abductor digiti II)"),
      p("Interosseous dorsalis digiti III", membership=D,
        note="Absent in birds on Hattori & Tsuihiji's reading; the avian m. extensor brevis digiti III is not accepted as its homologue."),
      p("Interosseous dorsalis digiti IV", membership=D,
        note="Absent in birds; the avian m. extensor brevis digiti IV is scored on extensores-digitorum-breves-pes.")]),
    (GRU, "Abductor digiti II",
     "Lateral aspect of metatarsal I and the dorsomedial aspect of the tarsometatarsus at the fossa metatarsi I.",
     "Medioplantar tubercle at the proximal end of phalanx II-1.",
     {"origin": [o("metatarsals", "lateral"),
                 o("tarsometatarsus", "medial", "fossa-metatarsi-i")],
      "insertion": [o("phalanges-pes", "proximal")]},
     "Grus japonensis. " + PAIRED,
     [p("Interosseous dorsalis digiti II (m. abductor digiti II)")]),
]:
    kw = dict(name=name, present="yes", origin=org, insertion=ins,
              attachments=att, attachmentNote=extra,
              innervation="Deep fibular nerve.")
    if len(parts) > 1:
        kw.update(division="divided", parts=parts)
    add("interossei-dorsales-pes", sid, **kw)


def main():
    write = "--write" in sys.argv
    files = sorted(ROOT.glob("data/muscles-*.json"))
    docs = {path: json.loads(path.read_text()) for path in files}

    index = {}
    for path, doc in docs.items():
        for m in doc["muscles"]:
            index[m["id"]] = (path, m)

    created = 0
    if NEW_RECORD["id"] not in index:
        created = 1
        rec = json.loads(json.dumps(NEW_RECORD))
        if write:
            docs[FILE]["muscles"].append(rec)
        index[rec["id"]] = (FILE, rec)

    seen = set()
    for mid, sid, _ in SEED:
        if (mid, sid) in seen:
            sys.exit(f"seed error: duplicate entry for {mid}/{sid}")
        seen.add((mid, sid))

    added = updated = unchanged = 0
    missing = []
    for mid, sid, spec in SEED:
        entry = index.get(mid)
        if not entry:
            missing.append(f"{mid}/{sid}: no such muscle record")
            continue
        _, muscle = entry
        occ = next((x for x in muscle.setdefault("occurrences", [])
                    if x.get("species") == sid), None)
        target = {"species": sid, **{k: v for k, v in spec.items() if v is not None}}
        if occ is None:
            if write:
                muscle["occurrences"].append(target)
            added += 1
            continue
        merged = {k: v for k, v in occ.items() if k not in MANAGED}
        merged.update(target)
        merged = {"species": sid, **{k: v for k, v in merged.items() if k != "species"}}
        if merged == occ:
            unchanged += 1
            continue
        if write:
            occ.clear()
            occ.update(merged)
        updated += 1

    if NEW_RECORD["id"] in index:
        _, rec = index[NEW_RECORD["id"]]
        if rec.get("occurrences"):
            rec["sources"] = sorted({s for x in rec["occurrences"]
                                     for s in x.get("sources", [])})

    for line in missing:
        print(f"  MISS  {line}")
    print(f"\n{len(SEED)} pedal rows from Hattori & Tsuihiji (2021): {added} to add, "
          f"{updated} to update, {unchanged} already current, "
          f"{created} record to create, {len(missing)} unresolved")

    if write and (added or updated or created):
        for path, doc in docs.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {len(docs)} files")
    elif not write:
        print("(dry run — pass --write to apply)")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
