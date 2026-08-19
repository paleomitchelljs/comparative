#!/usr/bin/env python3
"""Integrate Gambaryan et al. (2015), shoulder girdle and forelimb myology of
extant Monotremata.

Monotremata held seven occurrences before this pass, all pectoral, four of them
unscored, and all seven on *Tachyglossus aculeatus*. The paper describes ALL
THREE living genera side by side — *Zaglossus bruijnii* (3 specimens),
*Tachyglossus aculeatus* (2) and *Ornithorhynchus anatinus* (1) — with a separate
Origin and Insertion paragraph per genus for fifty-seven muscles. It is the
densest under-mined source in the corpus at ~10.6 origin/insertion mentions per
page over 56 pages, and it was cited here for names while its attachment data sat
untouched. This is the same failure the loon, the second gecko, Johnston's two
frogs and Sánchez's three cats each exposed: the paper describes N animals and
the dataset held one.

This script takes the girdle and the arm. The forearm and hand are described just
as fully and are left for a second pass; see docs/MINING.md.

Four things worth flagging beyond the row count:

* **Three of the seven existing rows were wrong, and all three cited this
  paper.** The pectoralis carried `division: divided` with a superficialis and a
  profundus, when Gambaryan et al. open the section with "not divided in
  monotremes ... as is typical to therians" and list the undivided sheet among
  the primitive features. The sternocoracoideus inserted on the coracoid; it
  inserts on the PROCORACOID. The serratus anterior arose from "ribs 1-8 and the
  cervical transverse processes"; the cervical slips arise from the cervical
  RIBS, one per vertebra from the axis to C7, and the thoracic slips come from
  three to five ribs, not eight.

* **A three-way naming conflict with Diogo & Abdala (2010)**, whose tables this
  dataset's therian and monotreme columns are largely built from. Gambaryan et
  al. reject Howell's (1937) re-identification and restore Westling (1889) and
  McKay (1894), which shifts three muscles one position down a chain: their
  supracoracoideus is Diogo & Abdala's infraspinatus, their infraspinatus is
  Diogo & Abdala's teres minor, and their teres minor is Diogo & Abdala's
  scapulohumeralis anterior. Each affected occurrence carries the equivalence in
  its note. Nothing is renamed on one paper's say-so.

* **The homology dispute that follows from it.** Romer's (1922) derivation of the
  therian supraspinatus and infraspinatus from the supracoracoideus of lower
  tetrapods — which this record's synonym list encodes — is argued from shared
  innervation, and Gambaryan et al.'s objection is that in monotremes ALL THREE
  MUSCLES ARE PRESENT AT ONCE. Their reading is that the monotreme
  supracoracoideus is homologous with the reptilian, avian and amphibian
  supracoracoideus outright, and that supraspinatus and infraspinatus are
  mammalian additions to the group. The two are recorded as `membership:
  disputed` parts rather than the record being restructured on one source.

* **Attachments that go to the wrong end of the bone.** The monotreme latissimus
  inserts on the medial epicondyle — the far distal humerus — where the therian
  and reptilian muscle inserts near the lesser tubercle. Gambaryan et al. tie it
  to the barrel-shaped rib cage: the elbow sits in the same parasagittal plane as
  the widest point of the ribs, so the muscle runs straight down the flank onto
  the epicondyle. A muscle moving the length of a bone, with a mechanical reason
  attached.

    python3 scripts/seed_gambaryan_monotremata.py           # report
    python3 scripts/seed_gambaryan_monotremata.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "gambaryan-etal-2015"

ZAG = "zaglossus-bruijnii"
TAC = "tachyglossus-aculeatus"
ORN = "ornithorhynchus-anatinus"

# Fields this script owns. Anything else already on a matching occurrence —
# `nerves`, `actions`, `architecture`, `speciesBasis` — is left alone, because
# later build steps write those and re-running must not undo them.
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


def p(name, membership=None, muscle=None, note=None):
    row = {"name": name}
    if membership:
        row["membership"] = membership
    if muscle:
        row["muscle"] = muscle
    if note:
        row["note"] = note
    return row


D = "disputed"

# `attribute_species.py` reattributes every occurrence from scratch on each
# build, and its first rule is the first binomial appearing in
# attachmentNote + note + divisionNote + name that belongs to the row's clade.
# All three of these animals are monotremes, so EVERY row below opens its
# attachmentNote (or its note, where there is no attachmentNote) with its own
# binomial, and refers to the other two by bare genus, which the index does not
# match. Get this wrong and three species collapse onto whichever one a
# comparison happened to mention first.
SEED: list[tuple[str, str, dict]] = [

    # ------------------------------------------------------------------
    # Ventral trunk to limb
    # ------------------------------------------------------------------
    ("pectoralis", ZAG, {
        "name": "Pectoralis",
        "present": "yes",
        "origin": "Anterior fifth of the stem of the interclavicle, sparing its most cranial part.",
        "insertion": "Ventral side of the pectoral crest of the humerus, over about a tenth of the bone's length.",
        "division": "single",
        "divisionNote": "Undivided. Gambaryan et al. find no separation into pectoralis superficialis and profundus in any monotreme and count the single sheet among the primitive features monotremes retain against therians.",
        "attachmentNote": "Zaglossus bruijnii. The most restricted pectoralis of the three genera: interclavicle only, with no sternal or costal component, and the shortest humeral insertion.",
        "attachments": {
            "origin": [o("interclavicle", "ventral")],
            "insertion": [o("humerus", "ventral", "deltopectoral-crest")],
        },
        "sources": [SRC],
    }),
    ("pectoralis", TAC, {
        "name": "Pectoralis",
        "present": "yes",
        "origin": "Anterior quarter of the stem of the interclavicle, sparing its most cranial part, and further back from the sternum excluding the xiphoid process.",
        "insertion": "A compact area on the ventral side of the pectoral crest of the humerus.",
        "division": "single",
        "divisionNote": "Undivided, as in the other two genera. This replaces a `divided` row carrying a pectoralis superficialis and profundus, which is the therian condition Gambaryan et al. explicitly contrast monotremes with.",
        "attachmentNote": "Tachyglossus aculeatus. The only one of the three with a sternal origin. The clavicle is NOT part of it — a clavicular origin previously scored here belongs to the clavodeltoideus.",
        "attachments": {
            "origin": [o("interclavicle", "ventral"), o("sternum", "ventral")],
            "insertion": [o("humerus", "ventral", "deltopectoral-crest")],
        },
        "sources": [SRC],
    }),
    ("pectoralis", ORN, {
        "name": "Pectoralis",
        "present": "yes",
        "origin": "Anterior fifth of the stem of the interclavicle, sparing its most cranial part, and the ventral (sternal) parts of the costal cartilages of the first five ribs.",
        "insertion": "The whole length of the pectoral crest of the humerus, on its ventral side.",
        "division": "single",
        "attachmentNote": "Ornithorhynchus anatinus. Costal rather than sternal behind the interclavicle, and the insertion runs the full length of the crest instead of occupying part of it — the widest pectoralis of the three, on the animal with the widest humerus.",
        "attachments": {
            "origin": [o("interclavicle", "ventral"), o("ribs", "ventral", "costal-cartilage")],
            "insertion": [o("humerus", "ventral", "deltopectoral-crest")],
        },
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Supracoracoideus — and the three-muscle problem
    # ------------------------------------------------------------------
    ("supracoracoideus", ZAG, {
        "name": "Supracoracoideus",
        "present": "yes",
        "origin": "Cranial part of the ventral surface of the procoracoid, passing through a gap between its cranial border and the interclavicle onto the dorsal side of both bones.",
        "insertion": "Anteroproximal part of the proximal ventral surface of the humerus, anterior to the coracobrachialis brevis, then along the anterior side of the greater tubercle onto its dorsal side between the infraspinatus (proximal) and the pectoralis (distal).",
        "attachmentNote": "Zaglossus bruijnii. Of the three genera this one alone carries the insertion over the greater tubercle and onto its dorsal face; in the short-beaked echidna it stops short of it.",
        "attachments": {
            "origin": [o("procoracoid", "ventral"), o("procoracoid", "dorsal"),
                       o("interclavicle", "dorsal")],
            "insertion": [o("humerus", "ventral"),
                          o("humerus", "dorsal", "greater-tubercle")],
        },
        "division": "divided",
        "parts": [p("Supracoracoideus"),
                  p("Supraspinatus", membership=D),
                  p("Infraspinatus", membership=D)],
        "divisionNote": "Three separate muscles, not two — and that is the argument. Romer (1922) derived the therian supraspinatus and infraspinatus from the supracoracoideus of lower tetrapods on the strength of shared innervation, which is the hypothesis this record's synonym list encodes. Gambaryan et al. object that in monotremes all three are present simultaneously, and read the monotreme supracoracoideus as homologous with the reptilian, avian and amphibian muscle outright, with supraspinatus and infraspinatus as mammalian additions to the group. Their membership is marked disputed on that basis rather than the record being restructured on one source.",
        "sources": [SRC],
    }),
    ("supracoracoideus", TAC, {
        "name": "Supracoracoideus",
        "present": "yes",
        "origin": "Cranial part of the ventral surface of the procoracoid, passing through a gap between its cranial border and the interclavicle onto its dorsal side.",
        "insertion": "Anteroproximal part of the proximal ventral surface of the humerus only, between the coracobrachialis brevis (posteriorly) and the infraspinatus (anteriorly), without reaching the anterior or dorsal sides of the greater tubercle.",
        "attachmentNote": "Tachyglossus aculeatus. The attachments here are Gambaryan et al.'s m. supracoracoideus alone, which is the muscle Diogo & Abdala (2010) call the infraspinatus. The two muscles this record's synonym list treats as its mammalian halves are separate bellies in this animal and are not scored into these rows: the supraspinatus runs from the lower third of the INTERNAL surface of the scapula to the proximal apex of the greater tubercle, and the infraspinatus from the external surface of the scapula, cranial to the triceps longus crest, to the greater tubercle just distal to the supraspinatus.",
        "attachments": {
            "origin": [o("procoracoid", "ventral"), o("procoracoid", "dorsal")],
            "insertion": [o("humerus", "ventral")],
        },
        "division": "divided",
        "parts": [p("Supracoracoideus"),
                  p("Supraspinatus", membership=D),
                  p("Infraspinatus", membership=D)],
        "divisionNote": "See the Zaglossus row on this record for the argument. Howell (1937) failed to find supracoracoid innervation for the big infraspinous muscle and renamed it teres minor, which Gambaryan et al. say destroyed the homologisation of everything around it; Westling (1889), McKay (1894) and Shrivastava (1962) all did find that nerve supply, and this paper restores their identification.",
        "sources": ["fahn-lai-etal-2020", SRC],
    }),
    ("supracoracoideus", ORN, {
        "name": "Supracoracoideus",
        "present": "yes",
        "origin": "Almost the entire ventral surface of the procoracoid, passing through a gap between its cranial border and the interclavicle slightly onto its dorsal side.",
        "insertion": "Mostly fleshy along the dorsal — not the ventral — side of the pectoral crest of the humerus, descending from its proximal apex at the greater tubercle to the insertion of the acromiodeltoideus.",
        "attachmentNote": "Ornithorhynchus anatinus. The largest procoracoid origin of the three and the only insertion that runs down the pectoral crest rather than sitting on the proximal humeral surface. The supraspinatus is vestigial in this animal, restricted to the internal side of the base of the acromion, which Gambaryan et al. read as secondary reduction following the invasion of the subscapularis onto the inner face of the scapula.",
        "attachments": {
            "origin": [o("procoracoid", "ventral"), o("procoracoid", "dorsal")],
            "insertion": [o("humerus", "dorsal", "deltopectoral-crest"),
                          o("humerus", "dorsal", "greater-tubercle")],
        },
        "division": "divided",
        "parts": [p("Supracoracoideus"),
                  p("Supraspinatus", membership=D),
                  p("Infraspinatus", membership=D)],
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Deltoid group
    # ------------------------------------------------------------------
    ("deltoideus-scapularis", ZAG, {
        "name": "Spinodeltoideus",
        "present": "yes",
        "origin": "Edge of the craniodorsal angle of the scapula.",
        "insertion": "By a tendon from mid-height of the scapula onto the proximal dorsal surface of the humerus, between the clavodeltoideus in front and the acromiodeltoideus behind.",
        "note": "Zaglossus bruijnii. Gambaryan et al. give the equivalence directly: their m. spinodeltoideus is the m. dorsalis scapulae of the older literature and the m. deltoideus scapularis of Diogo & Abdala (2010), which is this record.",
        "attachments": {
            "origin": [o("scapula", "dorsal", "scapula-cranial-angle")],
            "insertion": [o("humerus", "dorsal")],
        },
        "sources": [SRC],
    }),
    ("deltoideus-scapularis", TAC, {
        "name": "Spinodeltoideus",
        "present": "yes",
        "origin": "Edge of the craniodorsal angle of the scapula.",
        "insertion": "Proximal dorsal surface of the humerus between the clavodeltoideus and the acromiodeltoideus, closer to the pectoral crest than in the long-beaked echidna.",
        "note": "Tachyglossus aculeatus. = m. dorsalis scapulae = m. deltoideus scapularis sensu Diogo & Abdala (2010).",
        "attachments": {
            "origin": [o("scapula", "dorsal", "scapula-cranial-angle")],
            "insertion": [o("humerus", "dorsal")],
        },
        "sources": [SRC],
    }),
    ("deltoideus-scapularis", ORN, {
        "name": "Spinodeltoideus",
        "present": "yes",
        "origin": "Edge of the craniodorsal angle of the scapula, the origin split by the insertion of the spinotrapezius so that the cranial fibres arise over that muscle and the caudal fibres emerge from beneath it.",
        "insertion": "Terminal tendon on the dorsal side of the pectoral crest of the humerus, between the clavodeltoideus and the acromiodeltoideus.",
        "attachmentNote": "Ornithorhynchus anatinus. The only genus in which another muscle's insertion divides this one's origin, and the only one whose insertion reaches the pectoral crest rather than the proximal humeral surface.",
        "attachments": {
            "origin": [o("scapula", "dorsal", "scapula-cranial-angle")],
            "insertion": [o("humerus", "dorsal", "deltopectoral-crest")],
        },
        "sources": [SRC],
    }),

    ("deltoideus-clavicularis", ZAG, {
        "name": "Clavodeltoideus",
        "present": "yes",
        "origin": "Caudal border of the clavicle and the lateral ramus of the interclavicle, from the level of the procoracoid to the acromion.",
        "insertion": "Widely on the anterior part of the proximal dorsal surface of the humerus, including the pectoral crest.",
        "attachmentNote": "Zaglossus bruijnii. The acromiodeltoideus is a separate muscle here, from the apex of the acromion, inserting by an aponeurosis that embraces the spinodeltoideus from behind and fuses with the clavodeltoideus above and below it.",
        "attachments": {
            "origin": [o("clavicle", "posterior"), o("interclavicle", "lateral")],
            "insertion": [o("humerus", "dorsal", "deltopectoral-crest")],
        },
        "division": "divided",
        "parts": [p("Clavodeltoideus"),
                  p("Acromiodeltoideus", membership=D,
                    note="Gambaryan et al. note that reptiles have only two deltoid muscles, matching the clavodeltoideus and spinodeltoideus, and that the submerged position and wide humeral insertion of the acromiodeltoideus in monotremes suggest it is instead a portion of the reptilian scapulohumeralis anterior — whose deeper portion is the therian teres minor.")],
        "sources": [SRC],
    }),
    ("deltoideus-clavicularis", TAC, {
        "name": "Clavodeltoideus",
        "present": "yes",
        "origin": "Entire ventral surface of the clavicle except its acromial end, and the entire ventral surface of the lateral ramus of the interclavicle, with a superficial aponeurosis over the medial quarter of its length.",
        "insertion": "Dorsal side of the pectoral crest of the humerus, the most distal fibres by a short strong tendon.",
        "attachmentNote": "Tachyglossus aculeatus. The acromiodeltoideus is separate, arising only from the apex of the acromion and inserting on the proximal dorsal humerus behind the clavodeltoideus and spinodeltoideus.",
        "attachments": {
            "origin": [o("clavicle", "ventral"), o("interclavicle", "ventral")],
            "insertion": [o("humerus", "dorsal", "deltopectoral-crest")],
        },
        "division": "divided",
        "parts": [p("Clavodeltoideus"), p("Acromiodeltoideus", membership=D)],
        "sources": [SRC],
    }),
    ("deltoideus-clavicularis", ORN, {
        "name": "Clavodeltoideus + acromiodeltoideus",
        "present": "yes",
        "origin": "Ventral surface of the acromion, the ventral surface of the lateral ramus of the interclavicle, and the clavicle as far medially as the sternomastoideus insertion.",
        "insertion": "Descends along the pectoral crest of the humerus and far distal to it.",
        "attachmentNote": "Ornithorhynchus anatinus. The two deltoids are inseparable here and together embrace the spinodeltoideus from below; the fibres caudal to it can be called acromiodeltoideus and those cranial to it clavodeltoideus, but there is no boundary. Diogo & Abdala (2010) do not list an acromiodeltoideus for this animal at all.",
        "attachments": {
            "origin": [o("scapula", "ventral", "acromion"),
                       o("interclavicle", "ventral"), o("clavicle", "ventral")],
            "insertion": [o("humerus", "dorsal", "deltopectoral-crest")],
        },
        "division": "heads",
        "parts": [p("Pars clavicularis (clavodeltoideus)"),
                  p("Pars acromialis (acromiodeltoideus)")],
        "divisionNote": "`heads` rather than `divided` against both echidnas, which is a real difference and not a reading of the same thing: in Tachyglossidae the two are distinct muscles with separate origins and insertions, and in the platypus they are one continuous sheet whose parts are named by where they sit relative to the spinodeltoideus.",
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Scapulohumeralis anterior — Gambaryan's teres minor
    # ------------------------------------------------------------------
    ("scapulohumeralis-anterior", ZAG, {
        "name": "Teres minor",
        "present": "yes",
        "origin": "A notch in the cranial border of the scapula between the acromion and the shoulder joint, and partly from the joint capsule.",
        "insertion": "Fleshy in a fossa on the dorsal side of the LESSER tubercle of the humerus, immediately anterior to the subscapularis insertion.",
        "attachmentNote": "Zaglossus bruijnii. Gambaryan et al. identify this as the m. scapulohumeralis anterior of Diogo & Abdala (2010), which is this record. The insertion is the point: instead of taking the therian teres minor's short route from scapula to greater tubercle, it passes postaxially beneath the triceps longus to the lesser tubercle beside the subscapularis. Compare the Galictis row on this record, which inserts on the greater tubercle.",
        "attachments": {
            "origin": [o("scapula", "anterior"), o("glenoid")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle")],
        },
        "sources": [SRC],
    }),
    ("scapulohumeralis-anterior", TAC, {
        "name": "Teres minor",
        "present": "yes",
        "origin": "A notch in the cranial border of the scapula between the acromion and the shoulder joint, and partly from the joint capsule.",
        "insertion": "Fleshy in a fossa on the dorsal side of the lesser tubercle of the humerus, immediately anterior to the subscapularis insertion.",
        "note": "Tachyglossus aculeatus. Gambaryan et al. read this muscle as the posteromedial (postaxial) subdivision of the lizard m. scapulohumeralis anterior and the therian teres minor as the anterolateral subdivision of the same mass — which is a third position on this record's open question, alongside the amniote-wide hypothesis and Romer's (1924) derivation of teres minor from the procoracohumeralis. Shrivastava (1962) took a fourth: that the true homologue of the therian teres minor is fused inseparably into the monotreme infraspinatus.",
        "attachments": {
            "origin": [o("scapula", "anterior"), o("glenoid")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle")],
        },
        "sources": [SRC],
    }),
    ("scapulohumeralis-anterior", ORN, {
        "name": "Teres minor",
        "present": "yes",
        "origin": "External side of the scapula just anterior to the triceps longus profundus — a fossa for the fleshy fibres with a ridge along its anterior border for the aponeurosis — and partly from the articular capsule of the shoulder joint.",
        "insertion": "Fleshy in a fossa on the dorsal side of the lesser tubercle of the humerus, immediately anterior to the subscapularis insertion.",
        "attachmentNote": "Ornithorhynchus anatinus. The one genus of the three whose origin has moved off the cranial border onto the lateral face of the scapular blade, and it leaves an osteological correlate: a fossa with a bounding ridge.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("glenoid")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle")],
        },
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Teres major
    # ------------------------------------------------------------------
    ("teres-major", ZAG, {
        "name": "Teres major",
        "present": "yes",
        "origin": "External side of the apex of the caudal angle of the scapula, extending slightly onto its internal side below the serratus ventralis insertions.",
        "insertion": "Dorsal side of the distal part of the crest of the lesser tubercle of the humerus, between the subcoracoideus insertion and the triceps accessorius origin.",
        "note": "Zaglossus bruijnii.",
        "attachments": {
            "origin": [o("scapula", "lateral", "scapula-caudal-angle"),
                       o("scapula", "medial", "scapula-caudal-angle")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle-crest")],
        },
        "sources": [SRC],
    }),
    ("teres-major", TAC, {
        "name": "Teres major",
        "present": "yes",
        "origin": "External side of the apex of the caudal angle of the scapula and also its internal side, wedging between the insertions of the serratus ventralis cervicis in front and the serratus ventralis thoracis behind.",
        "insertion": "Dorsal side of the distal part of the crest of the lesser tubercle of the humerus, between the subcoracoideus insertion and the triceps accessorius origin.",
        "attachmentNote": "Tachyglossus aculeatus. The insertion is on the crest and not the apex of the lesser tubercle, which is the subscapularis' — the two are scored as separate landmarks because keeping them apart is the observation.",
        "attachments": {
            "origin": [o("scapula", "lateral", "scapula-caudal-angle"),
                       o("scapula", "medial", "scapula-caudal-angle")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle-crest")],
        },
        "sources": [SRC],
    }),
    ("teres-major", ORN, {
        "name": "Teres major",
        "present": "yes",
        "origin": "Along the external side of the caudal half of the dorsal border of the scapula, up to the apex of the caudal angle where the serratus ventralis thoracis inserts.",
        "insertion": "Dorsal side of the distal part of the crest of the lesser tubercle of the humerus, between the subcoracoideus insertion and the triceps accessorius origin.",
        "note": "Ornithorhynchus anatinus. The origin has spread forward along the dorsal border instead of concentrating on the angle, and it does not reach the internal face at all.",
        "attachments": {
            "origin": [o("scapula", "lateral", "scapula-caudal-angle"),
                       o("scapula", "lateral")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle-crest")],
        },
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Subcoracoscapularis — subscapularis + subcoracoideus
    # ------------------------------------------------------------------
    ("subcoracoscapularis", ZAG, {
        "name": "Subscapularis + subcoracoideus",
        "present": "yes",
        "origin": "Subscapularis from the EXTERNAL surface of the scapula caudal to the crest for the triceps longus, from the caudal border, and from a narrow strip of the internal surface along it; subcoracoideus from the dorsal (internal) surfaces of the procoracoid and coracoid, bifurcating along two longitudinal crests on the procoracoid.",
        "insertion": "Subscapularis, bipennate, on the proximal apex of the lesser tubercle of the humerus; subcoracoideus tendinous, descending from the lesser tubercle along its crest between the coracobrachialis brevis below and the teres major above.",
        "attachmentNote": "Zaglossus bruijnii. Both heads are present, which is the plesiomorphic amniote condition this record's name describes and which therians lost with the coracoid. The subscapularis origin is the finding: it is on the OUTER face of the scapular blade, the inverse of the therian arrangement, and the inner face is taken instead by the supraspinatus and the serratus ventralis cervicis.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("scapula", "posterior"),
                       o("procoracoid", "dorsal"), o("coracoid", "dorsal")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle"),
                          o("humerus", "dorsal", "lesser-tubercle-crest")],
        },
        "division": "divided",
        "parts": [p("Subscapularis"), p("Subcoracoideus")],
        "sources": [SRC],
    }),
    ("subcoracoscapularis", TAC, {
        "name": "Subscapularis + subcoracoideus",
        "present": "yes",
        "origin": "Subscapularis from the external surface of the scapula caudal to the triceps longus crest, the caudal border, and a narrow strip of the internal surface; subcoracoideus from the dorsal surfaces of the procoracoid and coracoid, reaching the caudal angle of the coracoid where it fuses with the coracobrachialis brevis origin.",
        "insertion": "Subscapularis on the proximal apex of the lesser tubercle of the humerus; subcoracoideus along the crest of the lesser tubercle between the coracobrachialis brevis and the teres major.",
        "attachmentNote": "Tachyglossus aculeatus. Gambaryan et al. regard this arrangement — subscapularis outside, supraspinatus and serratus ventralis cervicis inside — as the most primitive in mammals and probably in all synapsids, noting the half-external subscapularis that turns up in the giant anteater. The subcoracoideus tendon slides over the apex of the lesser tubercle, which carries hyaline cartilage and a synovial capsule for it.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("scapula", "posterior"),
                       o("procoracoid", "dorsal"), o("coracoid", "dorsal")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle"),
                          o("humerus", "dorsal", "lesser-tubercle-crest")],
        },
        "division": "divided",
        "parts": [p("Subscapularis"), p("Subcoracoideus")],
        "sources": [SRC],
    }),
    ("subcoracoscapularis", ORN, {
        "name": "Subscapularis + subcoracoideus",
        "present": "yes",
        "origin": "Subscapularis in two incompletely fused heads — a laterocaudal head, twice the bulk, from the caudal border and caudal external surface of the scapula, and a medial head covering the internal surface between the two portions of the serratus ventralis cervicis; subcoracoideus from the entire dorsal surface of the procoracoid but for a narrow medial strip, its origin completely fused with that of the coracobrachialis brevis at the procoracoid-coracoid boundary.",
        "insertion": "Subscapularis by two aponeuroses onto the proximal apex of the lesser tubercle, the medial head onto a sesamoid bone there and the laterocaudal head onto the tubercle just distal to it; subcoracoideus by four flat overlying tendons onto the lesser tubercle and its crest.",
        "attachmentNote": "Ornithorhynchus anatinus. The subscapularis has begun to invade the internal face of the scapula here, which Gambaryan et al. read as the derived state and as the cause of the reduction of the supraspinatus in this animal. A sesamoid sits in the medial head's tendon at the apex of the lesser tubercle, joined to it by a synovial joint; the most proximal of the four subcoracoideus tendons inserts on that sesamoid rather than on bone, so no attachment row is written for it. Howell (1937) could not separate subcoracoideus from coracobrachialis brevis in this animal and called the mass together the m. coracobrachialis profundus, having found only the ventral nerve supply.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("scapula", "posterior"),
                       o("scapula", "medial"), o("procoracoid", "dorsal")],
            "insertion": [o("humerus", "dorsal", "lesser-tubercle"),
                          o("humerus", "dorsal", "lesser-tubercle-crest")],
        },
        "division": "divided",
        "parts": [p("Subscapularis"), p("Subcoracoideus")],
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Latissimus — spinalis and costalis
    # ------------------------------------------------------------------
    ("latissimus-dorsi", ZAG, {
        "name": "Latissimus spinalis + latissimus costalis",
        "present": "yes",
        "origin": "Spinalis from the neural spines of thoracic vertebrae 1 or 2 to 11 or 12 — fleshy to the fifth or sixth and aponeurotic behind that — plus slips from ribs 7 and 8 and a slip from the external surface of the ventral part of the caudal angle of the scapula; costalis as slips from five to seven ribs beginning at rib 8.",
        "insertion": "Spinalis by aponeurosis onto a distinct tubercle on the dorsal side of the posterior border of the entepicondylus of the humerus; costalis by a first aponeurosis just distal to it, then continuing as the fascia antebrachii.",
        "attachmentNote": "Zaglossus bruijnii. The insertion is the finding, and it is at the wrong end of the bone: in therians and in extant reptiles the latissimus ends near the lesser tubercle, and here it ends on the medial epicondyle. Gambaryan et al. read it as secondary and tie it to the barrel-shaped monotreme rib cage — the elbow falls in the same parasagittal plane as the widest point of the ribs, so the muscle runs straight down the flank onto the epicondyle.",
        "attachments": {
            "origin": [o("thoracic-vertebrae", "dorsal", "thoracic-neural-spines"),
                       o("ribs"),
                       o("scapula", "lateral", "scapula-caudal-angle")],
            "insertion": [o("humerus", "dorsal", "medial-epicondyle")],
        },
        "division": "divided",
        "parts": [p("Latissimus spinalis"),
                  p("Latissimus costalis",
                    note="Gambaryan et al. state that a latissimus costalis of this kind — rib-borne, alongside a separate spinal head — is found nowhere outside monotremes.")],
        "sources": [SRC],
    }),
    ("latissimus-dorsi", TAC, {
        "name": "Latissimus spinalis + latissimus costalis",
        "present": "yes",
        "origin": "Spinalis from the neural spines of thoracic vertebrae 2 to 10 or 11 — fleshy to vertebra 7, aponeurotic behind it — plus the external surface of the ventral part of the caudal angle of the scapula and the proximal third of the teres major's aponeurosis of origin; costalis from ribs 8 to 14.",
        "insertion": "Spinalis by aponeurosis onto a tubercle on the dorsal side of the posterior border of the entepicondylus; costalis by aponeurosis just distal to that, its posterior fibres bypassing the epicondyle to continue into the tensor fasciae antebrachii across a tendinous interseptum.",
        "attachmentNote": "Tachyglossus aculeatus. The latissimus costalis and the tensor fasciae antebrachii form a digastric complex across the elbow, and one of the two specimens lacked the interseptum entirely, the two muscles running continuous as they do in the long-beaked echidna. Gambaryan et al. read the continuous state as primitive and the interseptum as intermediate towards the platypus, where the tensor is a separate muscle — which would make the therian tensor fasciae antebrachii the last remnant of the latissimus costalis.",
        "attachments": {
            "origin": [o("thoracic-vertebrae", "dorsal", "thoracic-neural-spines"),
                       o("ribs"),
                       o("scapula", "lateral", "scapula-caudal-angle")],
            "insertion": [o("humerus", "dorsal", "medial-epicondyle")],
        },
        "division": "divided",
        "parts": [p("Latissimus spinalis"), p("Latissimus costalis")],
        "sources": [SRC],
    }),
    ("latissimus-dorsi", ORN, {
        "name": "Latissimus spinalis + latissimus costalis",
        "present": "yes",
        "origin": "Spinalis from the neural spines of thoracic vertebrae 3 to 11, fleshy to vertebra 7 and aponeurotic behind it, with no scapular or costal slip; costalis from ribs 8 to 15.",
        "insertion": "Spinalis mainly fleshy along the postaxial aspect of the humerus, from the distal angle of the pectoral crest to the entepicondylar foramen, leaving a distinct facet; costalis by a flat tendon along the posterior side of the pectoral crest, PROXIMAL to the spinalis rather than distal to it.",
        "attachmentNote": "Ornithorhynchus anatinus. The order of the two insertions is reversed against both echidnas — costalis proximal and spinalis distal here, the other way round in Tachyglossidae — and the spinalis insertion has climbed back up the humerus from the epicondyle towards the pectoral crest. That proximal shift is what crowds the coracobrachialis longus distally in this animal.",
        "attachments": {
            "origin": [o("thoracic-vertebrae", "dorsal", "thoracic-neural-spines"),
                       o("ribs")],
            "insertion": [o("humerus", "posterior", "medial-epicondyle"),
                          o("humerus", "ventral", "deltopectoral-crest")],
        },
        "division": "divided",
        "parts": [p("Latissimus spinalis"), p("Latissimus costalis")],
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Serratus ventralis
    # ------------------------------------------------------------------
    ("serratus-anterior", ZAG, {
        "name": "Serratus ventralis cervicis + thoracis",
        "present": "yes",
        "origin": "Cervicis as six slips from the cervical ribs of vertebrae II to VII, one per vertebra, the atlas excepted; thoracis as four slips from the lower halves of the first four ribs, short of the costal cartilages.",
        "insertion": "Cervicis on the internal surface of the scapula, each slip spreading as a flat fan and each successive fan set lower and wider than the last; thoracis fused into one before reaching the scapula and inserting on the external side of the caudal angle, just cranial to the scapular slip of the latissimus spinalis.",
        "attachmentNote": "Zaglossus bruijnii. The serratus ventralis thoracis is underdeveloped against the cervicis, the reverse of the therian balance, because the dorsal border of the monotreme scapula lies in the cervical region rather than over the thorax — so the body's weight is transmitted through the cervical part of the sling.",
        "attachments": {
            "origin": [o("ribs", landmark="cervical-ribs"), o("ribs")],
            "insertion": [o("scapula", "medial"),
                          o("scapula", "lateral", "scapula-caudal-angle")],
        },
        "division": "divided",
        "parts": [p("Serratus ventralis cervicis proprius"),
                  p("Serratus ventralis cervicis accessorius"),
                  p("Serratus ventralis thoracis")],
        "divisionNote": "The slips from the last three cervical vertebrae bifurcate into a subvertical main portion and a subhorizontal accessory portion. Gambaryan et al. argue the accessorius is additional to the therian condition rather than a subdivision of it — therians have the proprius alone — and that the homonomic monotreme series is the most primitive among living tetrapods, more complete than the bifurcating caudal slips Miner (1925) found in urodeles and Sphenodon.",
        "sources": [SRC],
    }),
    ("serratus-anterior", TAC, {
        "name": "Serratus ventralis cervicis + thoracis",
        "present": "yes",
        "origin": "Cervicis as six slips from the cervical ribs of vertebrae II to VII; thoracis as four or five slips from the first four or five ribs, the foremost occupying the whole length of the first rib from tubercle to costal cartilage.",
        "insertion": "Cervicis in fans on the internal surface of the scapula; thoracis on the caudal angle of the scapula, on the internal as well as the external side.",
        "attachmentNote": "Tachyglossus aculeatus. This replaces a row giving the origin as 'ribs 1-8 and the cervical transverse processes'. Gambaryan et al. put the cervical slips on the cervical RIBS, one per vertebra from the axis back, and the thoracic slips on four or five ribs, not eight.",
        "attachments": {
            "origin": [o("ribs", landmark="cervical-ribs"), o("ribs")],
            "insertion": [o("scapula", "medial"),
                          o("scapula", "lateral", "scapula-caudal-angle"),
                          o("scapula", "medial", "scapula-caudal-angle")],
        },
        "division": "divided",
        "parts": [p("Serratus ventralis cervicis proprius"),
                  p("Serratus ventralis cervicis accessorius"),
                  p("Serratus ventralis thoracis")],
        "sources": [SRC],
    }),
    ("serratus-anterior", ORN, {
        "name": "Serratus ventralis cervicis + thoracis",
        "present": "yes",
        "origin": "Cervicis as six slips from the cervical ribs of vertebrae II to VII; thoracis as three slips from the lower halves of the first three ribs, short of the costal cartilages.",
        "insertion": "Cervicis gathered near the dorsal and cranial borders of the internal surface of the scapula, occupying much less of that surface than in the echidnas because the subscapularis has taken most of it; thoracis compactly on the external side of the caudal angle, fusing near its insertion with the main portion of the last cervical slip.",
        "attachmentNote": "Ornithorhynchus anatinus. Five of the six cervical slips bifurcate here against three in Tachyglossidae, which Gambaryan et al. count as the derived state, while the retreat of the cervicis from the internal face of the scapula is the counterpart of the subscapularis moving onto it.",
        "attachments": {
            "origin": [o("ribs", landmark="cervical-ribs"), o("ribs")],
            "insertion": [o("scapula", "medial"),
                          o("scapula", "lateral", "scapula-caudal-angle")],
        },
        "division": "divided",
        "parts": [p("Serratus ventralis cervicis proprius"),
                  p("Serratus ventralis cervicis accessorius"),
                  p("Serratus ventralis thoracis")],
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Levator scapulae
    # ------------------------------------------------------------------
    ("levator-scapulae", ZAG, {
        "name": "Levator scapulae (dorsalis, intermedius, ventralis)",
        "present": "yes",
        "origin": "Dorsalis by a wide aponeurosis from the ventral side of the occiput behind the detrahens mandibulae; intermedius from the capsule of the atlanto-occipital joint back onto the ventral border of the epistropheal rib; ventralis from the ventral border of the epistropheal rib.",
        "insertion": "Dorsalis on the internal side of the dorsal border of the scapula; intermedius on the remaining cranial part of that border and the dorsal half of the cranial border; ventralis on the rest of the cranial border, the acromial process and the distal sixth of the clavicle.",
        "attachmentNote": "Zaglossus bruijnii. The occipital origin is the widest of the three genera, and Gambaryan et al. use that spread to argue that the tight association with the atlas seen in therians and in the platypus is an advanced condition reached independently in each.",
        "attachments": {
            "origin": [o("occiput", "ventral"), o("atlas"),
                       o("ribs", "ventral", "cervical-ribs")],
            "insertion": [o("scapula", "medial"), o("scapula", "anterior"),
                          o("scapula", landmark="acromion"), o("clavicle", "distal")],
        },
        "division": "divided",
        "parts": [p("Levator scapulae dorsalis",
                    note="= m. atlantoscapularis of therians."),
                  p("Levator scapulae intermedius",
                    note="Gambaryan et al. find no therian counterpart and read it as lost in that lineage."),
                  p("Levator scapulae ventralis",
                    note="= m. atlantoacromialis of therians, and the m. levator claviculae of Diogo & Abdala (2010).")],
        "divisionNote": "Three portions, not the two this row previously carried. The intermedius is the interesting one: it has no therian counterpart, so the monotreme condition is not an unsplit version of the mammalian muscle but a more subdivided one.",
        "sources": [SRC],
    }),
    ("levator-scapulae", TAC, {
        "name": "Levator scapulae (dorsalis, intermedius, ventralis)",
        "present": "yes",
        "origin": "Dorsalis by a tendon from the ventral side of the occiput behind the detrahens mandibulae, converging with the common tendon of the other two portions from the ventral tubercle of the atlas wing; intermedius additionally by an accessory tendon and ventralis fleshy along the whole length of the epistropheal rib.",
        "insertion": "Dorsalis on the internal side of almost the entire dorsal border of the scapula and the dorsal fifth of its cranial border; intermedius on the medial side of the next two-fifths of the cranial border; ventralis on the internal side of the remaining ventral two-fifths and the acromion.",
        "attachmentNote": "Tachyglossus aculeatus. Unlike the long-beaked echidna and the platypus, no portion reaches the clavicle, and the intermedius insertion stays on the medial side of the cranial border instead of wrapping onto the external side.",
        "attachments": {
            "origin": [o("occiput", "ventral"),
                       o("atlas", "ventral", "atlas-transverse-process"),
                       o("ribs", "ventral", "cervical-ribs")],
            "insertion": [o("scapula", "medial"), o("scapula", "anterior"),
                          o("scapula", landmark="acromion")],
        },
        "division": "divided",
        "parts": [p("Levator scapulae dorsalis"),
                  p("Levator scapulae intermedius"),
                  p("Levator scapulae ventralis")],
        "sources": [SRC],
    }),
    ("levator-scapulae", ORN, {
        "name": "Levator scapulae (dorsalis, intermedius, ventralis)",
        "present": "yes",
        "origin": "All three portions mainly from the ventral tubercle of the atlas wing — dorsalis by a short flat tendon, intermedius by a longer one plus a thin accessory tendon from the atlanto-occipital joint capsule, ventralis by an aponeurosis separated from the other two by the scalenus, its posterior fibres running fleshy along the caudoventral border of the atlas wing to the epistropheal rib.",
        "insertion": "Dorsalis on the internal side of the cranial three-fifths of the dorsal border of the scapula and the dorsal half of its cranial border; intermedius on a short segment of the cranial border below it; ventralis on the remaining ventral part of the cranial border, the acromial process and the distal fifth of the clavicle. All three cover both faces of the cranial border.",
        "attachmentNote": "Ornithorhynchus anatinus. The origin has withdrawn almost entirely onto the atlas, which is the therian arrangement — and Gambaryan et al. argue it was reached independently here rather than shared, because the echidnas keep the wide occipital origin.",
        "attachments": {
            "origin": [o("atlas", "ventral", "atlas-transverse-process"),
                       o("ribs", "ventral", "cervical-ribs")],
            "insertion": [o("scapula", "medial"), o("scapula", "anterior"),
                          o("scapula", "lateral"),
                          o("scapula", landmark="acromion"), o("clavicle", "distal")],
        },
        "division": "divided",
        "parts": [p("Levator scapulae dorsalis"),
                  p("Levator scapulae intermedius"),
                  p("Levator scapulae ventralis")],
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Coracoid-plate muscles
    # ------------------------------------------------------------------
    ("sternocoracoideus", ZAG, {
        "name": "Sternocoracoideus",
        "present": "yes",
        "origin": "By a short aponeurosis from the dorsal side of the sternal manubrium along the rim of the sternocoracoid joint and from the internal side of the sternal end of the first costal cartilage, adjoining the costocoracoideus from below.",
        "insertion": "Dorsal (internal) side of the medial border of the procoracoid.",
        "attachmentNote": "Zaglossus bruijnii. The insertion is on the PROCORACOID, not the coracoid, in all three genera. Sternocoracoid mobility is much reduced in monotremes, but Gambaryan et al. argue the muscle's long fibres show it is still real, and point to the overlapping left and right procoracoids as a remnant of the pronounced craniocaudal sternocoracoid sliding seen in urodeles and lizards.",
        "attachments": {
            "origin": [o("sternum", "dorsal"), o("ribs", "medial", "costal-cartilage")],
            "insertion": [o("procoracoid", "dorsal")],
        },
        "sources": ["abdala-diogo-2010", SRC],
    }),
    ("sternocoracoideus", TAC, {
        "name": "Sternocoracoideus",
        "present": "yes",
        "origin": "Fleshy from the dorsal side of the sternal manubrium along the rim of the sternocoracoid joint and from the internal side of the ventral part of a calcified region of the first costal cartilage.",
        "insertion": "Dorsal (internal) side of the medial border of the procoracoid.",
        "attachmentNote": "Tachyglossus aculeatus. This corrects an insertion previously scored on the coracoid. Gambaryan et al. put it on the procoracoid in all three genera, and the distinction matters here because the costocoracoideus, which inserts alongside it, is the one that takes the coracoid.",
        "attachments": {
            "origin": [o("sternum", "dorsal"), o("ribs", "medial", "costal-cartilage")],
            "insertion": [o("procoracoid", "dorsal")],
        },
        "sources": ["abdala-diogo-2010", SRC],
    }),
    ("sternocoracoideus", ORN, {
        "name": "Sternocoracoideus",
        "present": "yes",
        "origin": "Fleshy from the dorsal side of the sternal manubrium along the rim of the sternocoracoid joint, from that joint's articular capsule, and from the internal side of the ventral segment of the first costal cartilage.",
        "insertion": "Unipennate; the terminal aponeurosis inserts on the dorsal side of the medial border of the procoracoid in its posterior half, clear of the suture with the coracoid, while the most anterior fibres insert fleshy on the cartilaginous lining of the procoracoid border.",
        "attachmentNote": "Ornithorhynchus anatinus. The only genus in which part of the insertion is onto cartilage rather than bone, and the only one whose origin takes in the joint capsule.",
        "attachments": {
            "origin": [o("sternum", "dorsal"), o("ribs", "medial", "costal-cartilage")],
            "insertion": [o("procoracoid", "dorsal")],
        },
        "sources": [SRC],
    }),

    ("costocoracoideus", ZAG, {
        "name": "Costocoracoideus",
        "present": "yes",
        "origin": "By a wide aponeurosis from the internal side of the first costal cartilage and the cranial border of the first rib itself.",
        "insertion": "By a short aponeurosis on the dorsal (internal) side of the medial border of the coracoid, and also on the procoracoid just lateral to the posterior part of the sternocoracoideus.",
        "attachmentNote": "Zaglossus bruijnii. The only genus whose costocoracoideus reaches the procoracoid as well as the coracoid.",
        "attachments": {
            "origin": [o("ribs", "medial", "costal-cartilage"), o("ribs", "anterior")],
            "insertion": [o("coracoid", "dorsal"), o("procoracoid", "dorsal")],
        },
        "sources": ["abdala-diogo-2010", SRC],
    }),
    ("costocoracoideus", TAC, {
        "name": "Costocoracoideus",
        "present": "yes",
        "origin": "Fleshy from the cranial border of both the cartilaginous and the bony segments of the first rib.",
        "insertion": "By a short aponeurosis on the dorsal side of the medial border of the coracoid, adjoining the sternocoracoideus at the procoracoid-coracoid suture.",
        "attachmentNote": "Tachyglossus aculeatus. Together with the sternocoracoideus, the subcoracoideus and the supracoracoideus this is one of the four coracoid-plate muscles monotremes retain and therians have lost with the bone.",
        "attachments": {
            "origin": [o("ribs", "anterior", "costal-cartilage"), o("ribs", "anterior")],
            "insertion": [o("coracoid", "dorsal")],
        },
        "sources": ["abdala-diogo-2010", SRC],
    }),
    ("costocoracoideus", ORN, {
        "name": "Costocoracoideus",
        "present": "yes",
        "origin": "Fleshy from the cranial border of the upper part of the first costal cartilage and the lower part of the first rib, rising slightly above the origin of the anterior slip of the serratus ventralis thoracis, with the scalenus wedged between them.",
        "insertion": "Restricted to the posterior half of the dorsal side of the medial border of the coracoid, not reaching forward to the procoracoid suture.",
        "attachmentNote": "Ornithorhynchus anatinus. The most restricted of the three insertions — it stops short of the suture that the short-beaked echidna's reaches and the long-beaked echidna's crosses.",
        "attachments": {
            "origin": [o("ribs", "anterior", "costal-cartilage"), o("ribs", "anterior")],
            "insertion": [o("coracoid", "dorsal")],
        },
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Rhomboideus
    # ------------------------------------------------------------------
    ("rhomboideus", ZAG, {
        "name": "Rhomboideus",
        "present": "yes",
        "origin": "Transverse crest of the occiput and the dorsal midline of the whole neck; aponeurotic as far back as the neural spine of the epistropheus, then fleshy to the midline, meeting its opposite number above the nuchal ligament.",
        "insertion": "Cranial portion on the uppermost part of the cranial border of the scapula, its cranial angle, and both faces of its dorsal border; caudal portion on the internal side of the caudal angle.",
        "attachmentNote": "Zaglossus bruijnii.",
        "attachments": {
            "origin": [o("occiput", "dorsal"), o("cervical-vertebrae", "dorsal")],
            "insertion": [o("scapula", "anterior"),
                          o("scapula", "dorsal", "scapula-cranial-angle"),
                          o("scapula", "medial", "scapula-caudal-angle")],
        },
        "division": "heads",
        "parts": [p("Cranial portion (rhomboideus capitis)"),
                  p("Caudal portion (rhomboideus thoracis)")],
        "divisionNote": "Incipiently divided in Tachyglossidae: the two portions run at sharply different fibre angles — the cranial anteroposteriorly, the caudal mediolaterally — and correspond to the therian rhomboideus capitis and thoracis without being separate muscles.",
        "sources": [SRC],
    }),
    ("rhomboideus", TAC, {
        "name": "Rhomboideus",
        "present": "yes",
        "origin": "Transverse crest of the occiput and the dorsal midline of the neck, aponeurotic to the neural spine of the epistropheus and fleshy behind it.",
        "insertion": "Cranial portion on the uppermost cranial border of the scapula, its cranial angle and both faces of the dorsal border; caudal portion on the internal side of the caudal angle.",
        "attachmentNote": "Tachyglossus aculeatus.",
        "attachments": {
            "origin": [o("occiput", "dorsal"), o("cervical-vertebrae", "dorsal")],
            "insertion": [o("scapula", "anterior"),
                          o("scapula", "dorsal", "scapula-cranial-angle"),
                          o("scapula", "medial", "scapula-caudal-angle")],
        },
        "division": "heads",
        "parts": [p("Cranial portion (rhomboideus capitis)"),
                  p("Caudal portion (rhomboideus thoracis)")],
        "sources": [SRC],
    }),
    ("rhomboideus", ORN, {
        "name": "Rhomboideus",
        "present": "yes",
        "origin": "Transverse crest of the occiput and the dorsal midline of the neck, the occipital part set further back from the origin of the clavoacromiotrapezius than in the echidnas.",
        "insertion": "Internal side of the caudal part of the dorsal border of the scapula, as far as its caudal angle.",
        "attachmentNote": "Ornithorhynchus anatinus. Undivided, against the two portions of both echidnas, and the insertion is correspondingly confined to the caudal half of the dorsal border.",
        "attachments": {
            "origin": [o("occiput", "dorsal"), o("cervical-vertebrae", "dorsal")],
            "insertion": [o("scapula", "medial"),
                          o("scapula", "medial", "scapula-caudal-angle")],
        },
        "division": "single",
        "divisionNote": "Single here against `heads` in Tachyglossidae, which puts the differentiation of the rhomboideus inside Monotremata rather than on its stem.",
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Arm
    # ------------------------------------------------------------------
    ("coracobrachialis", ZAG, {
        "name": "Coracobrachialis brevis + longus",
        "present": "yes",
        "origin": "Brevis from the ventral (external) side of the caudolateral border of the coracoid except its tip; longus from the ventral side of that tip.",
        "insertion": "Brevis fleshy over the proximal ventral surface of the humerus from the crest of the lesser tubercle almost to the pectoral crest; longus in a sharply outlined triangular area on the ventral side of the postaxial border of the humerus, over its distal third up to the base of the entepicondylus.",
        "attachmentNote": "Zaglossus bruijnii. The two are separated by a neurovascular bundle in Tachyglossidae, and the longus insertion leaves a defined facet on the bone in every genus.",
        "attachments": {
            "origin": [o("coracoid", "ventral")],
            "insertion": [o("humerus", "ventral"),
                          o("humerus", "ventral", "medial-epicondyle")],
        },
        "division": "divided",
        "parts": [p("Coracobrachialis brevis"), p("Coracobrachialis longus")],
        "sources": [SRC],
    }),
    ("coracobrachialis", TAC, {
        "name": "Coracobrachialis brevis + longus",
        "present": "yes",
        "origin": "Brevis from the ventral side of the caudolateral border of the coracoid just cranial to the longus and the subcoracoideus; longus by a tendon from the ventral side of the caudal tip of the coracoid, the tendon splitting into superficial, middle and deep aponeuroses.",
        "insertion": "Brevis fleshy over the proximal ventral humerus from the crest of the lesser tubercle almost to the pectoral crest; longus in a distinct fossa on the ventral side of the postaxial border, over the distal half of the bone from the end of the pectoral crest to the base of the entepicondylus.",
        "attachmentNote": "Tachyglossus aculeatus. The longus fossa is a clean osteological correlate — a defined depression, not a roughened area.",
        "attachments": {
            "origin": [o("coracoid", "ventral")],
            "insertion": [o("humerus", "ventral"),
                          o("humerus", "ventral", "medial-epicondyle")],
        },
        "division": "divided",
        "parts": [p("Coracobrachialis brevis"), p("Coracobrachialis longus")],
        "sources": [SRC],
    }),
    ("coracobrachialis", ORN, {
        "name": "Coracobrachialis brevis + longus",
        "present": "yes",
        "origin": "Brevis from the ventral side of the caudolateral border of the coracoid except its tip AND from its dorsal (internal) surface up to the coracoid-procoracoid boundary, where it meets the subcoracoideus origin; longus by a narrow tendon from the ventral side of the caudal tip of the coracoid.",
        "insertion": "Brevis over the whole proximal ventral surface of the humerus, but not adjoined distally by the longus; longus along a narrow line continuing the pectoral crest onto the ventral side of the base of the entepicondylus, at the level of the entepicondylar foramen.",
        "attachmentNote": "Ornithorhynchus anatinus. The brevis has spread onto the internal face of the coracoid here, and its complete fusion with the subcoracoideus origin at the procoracoid boundary is what Gambaryan et al. take as evidence of the two muscles' close affinity — and what defeated Howell (1937), who lumped them as m. coracobrachialis profundus. The longus is crowded distally by the latissimus, which has shifted its insertion proximally onto the pectoral crest in this animal.",
        "attachments": {
            "origin": [o("coracoid", "ventral"), o("coracoid", "dorsal")],
            "insertion": [o("humerus", "ventral"),
                          o("humerus", "ventral", "medial-epicondyle")],
        },
        "division": "divided",
        "parts": [p("Coracobrachialis brevis"), p("Coracobrachialis longus")],
        "sources": [SRC],
    }),

    ("triceps-brachii", ZAG, {
        "name": "Triceps brachii (five heads)",
        "present": "yes",
        "origin": "Both long heads by a superficial aponeurosis from a crest running down the middle of the lower part of the external surface of the scapula to the glenoid, the profundus curving further caudal to the glenoid and close to the coracoid; lateralis by a narrow tendon a little proximal to the centre of the proximal dorsal surface of the humerus; medialis and accessorius from the proximal and distal dorsal surfaces of the humerus.",
        "insertion": "Longus superficialis on the posterior projection of the olecranon apex, over more than half its extent; longus profundus across almost the whole apex from posterior to anterior projection; lateralis on the anterior projection; accessorius along the apical border of the humerus-facing aspect and medialis on the surface between that border and the elbow joint facet.",
        "attachmentNote": "Zaglossus bruijnii. Five heads, and the two scapular ones are the point: the superficialis arises cranial to the profundus and inserts posterior to it, so the two pull the ulna criss-cross. Gambaryan et al. suggest that suits the ball-and-socket monotreme elbow, which among tetrapods is otherwise an anuran arrangement.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("glenoid"), o("humerus", "dorsal")],
            "insertion": [o("ulna", landmark="olecranon")],
        },
        "division": "heads",
        "parts": [p("Triceps longus superficialis"), p("Triceps longus profundus"),
                  p("Triceps lateralis"), p("Triceps medialis"),
                  p("Triceps accessorius")],
        "divisionNote": "A divided triceps longus is listed among the ADVANCED monotreme features, against the primitive ones. Gambaryan et al. note that mustelids carry a second two-jointed scapular head, the caput angulare (Ercoli et al. 2015), which resembles the monotreme triceps longus superficialis; if those are homologous the double-headed scapular triceps is primitive for mammals as a whole. The Galictis row on this record is from the companion paper.",
        "sources": [SRC],
    }),
    ("triceps-brachii", TAC, {
        "name": "Triceps brachii (five heads)",
        "present": "yes",
        "origin": "Both long heads by a superficial aponeurosis from a crest on the lower part of the external surface of the scapula running to the glenoid; lateralis fleshy from the proximal dorsal surface of the humerus just distal to the shoulder joint capsule; medialis and accessorius united at their origin on the dorsal surface of the humerus and separated further distally by a neurovascular bundle.",
        "insertion": "Longus superficialis on the posterior projection of the olecranon apex, over about a quarter of its extent; longus profundus across almost the whole apex; lateralis on the anterior projection; accessorius and medialis on the humerus-facing aspect, aided by aponeuroses posteriorly and anteriorly respectively.",
        "attachmentNote": "Tachyglossus aculeatus. The triceps lateralis is separated from the other four heads by a neurovascular bundle in every genus, which is what makes the accessorius readable as a proximal subdivision of the medialis rather than an independent head.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("glenoid"), o("humerus", "dorsal")],
            "insertion": [o("ulna", landmark="olecranon")],
        },
        "division": "heads",
        "parts": [p("Triceps longus superficialis"), p("Triceps longus profundus"),
                  p("Triceps lateralis"), p("Triceps medialis"),
                  p("Triceps accessorius")],
        "sources": [SRC],
    }),
    ("triceps-brachii", ORN, {
        "name": "Triceps brachii (five heads)",
        "present": "yes",
        "origin": "Both long heads from the scapular crest running to the glenoid; lateralis by a narrow tendon from a distinct tubercle on the proximal dorsal surface of the humerus, between the infraspinatus insertion and the brachialis origin; medialis and accessorius from the dorsal surface of the humerus, their origins completely separate from one another.",
        "insertion": "Longus superficialis on the posterior projection of the olecranon apex over about a quarter of its extent; longus profundus across almost the whole apex; lateralis fleshy on the anterior projection, nearly fusing behind with the accessorius; accessorius and medialis on the humerus-facing aspect.",
        "attachmentNote": "Ornithorhynchus anatinus. The lateralis origin has a named bony tubercle here where the echidnas have only a surface, and the medialis and accessorius origins are fully separate where in Tachyglossidae they are united.",
        "attachments": {
            "origin": [o("scapula", "lateral"), o("glenoid"), o("humerus", "dorsal")],
            "insertion": [o("ulna", landmark="olecranon")],
        },
        "division": "heads",
        "parts": [p("Triceps longus superficialis"), p("Triceps longus profundus"),
                  p("Triceps lateralis"), p("Triceps medialis"),
                  p("Triceps accessorius")],
        "sources": [SRC],
    }),

    ("biceps-brachii", ZAG, {
        "name": "Biceps longus + biceps brevis",
        "present": "yes",
        "origin": "Longus just caudal to the supracoracoideus from the ventral side of the procoracoid; brevis just caudal to the longus from the procoracoid and the adjacent lateral border of the stem of the interclavicle.",
        "insertion": "Longus by a narrow aponeurosis on the radial edge of the ulna just distal to the brachialis ulnaris; brevis further distally by a wider aponeurosis on the radius, distal to and closer to the ulna than the brachialis radialis.",
        "attachmentNote": "Zaglossus bruijnii. The origin is on the PROCORACOID and the interclavicle, bones no therian has — the therian biceps arises from the supraglenoid tubercle and the coracoid process of the scapula. Allen (1912) denied any ulnar insertion of the biceps in this genus; Gambaryan et al. find one.",
        "attachments": {
            "origin": [o("procoracoid", "ventral"), o("interclavicle", "lateral")],
            "insertion": [o("ulna"), o("radius", "posterior")],
        },
        "division": "heads",
        "parts": [p("Biceps longus (caput longum)"), p("Biceps brevis (caput breve)")],
        "divisionNote": "Two heads, homologous with the therian caput longum and caput breve, but with the size relation reversed: the brevis is the larger in monotremes.",
        "sources": [SRC],
    }),
    ("biceps-brachii", TAC, {
        "name": "Biceps longus + biceps brevis",
        "present": "yes",
        "origin": "Longus just caudal to the supracoracoideus from the ventral side of the procoracoid, penetrating under the lateral border of the stem of the interclavicle; brevis just caudal to it from the procoracoid and the coracoid.",
        "insertion": "Longus by a narrow aponeurosis on the radial edge of the ulna just distal to the brachialis ulnaris; brevis by a wider aponeurosis on the radius, distal to the brachialis radialis.",
        "attachmentNote": "Tachyglossus aculeatus. The brevis is the only one of the two to reach the coracoid; both heads take the procoracoid.",
        "attachments": {
            "origin": [o("procoracoid", "ventral"), o("coracoid", "ventral")],
            "insertion": [o("ulna"), o("radius", "posterior")],
        },
        "division": "heads",
        "parts": [p("Biceps longus (caput longum)"), p("Biceps brevis (caput breve)")],
        "sources": [SRC],
    }),
    ("biceps-brachii", ORN, {
        "name": "Biceps longus + biceps brevis",
        "present": "yes",
        "origin": "Longus just caudomedial to the supracoracoideus from the ventral side of the medial border of the procoracoid and a little from the dorsal side of the lateral border of the interclavicle stem; brevis further caudally from the ventral side of the caudal tip of the coracoid, just cranial to the coracobrachialis longus.",
        "insertion": "The longus fuses with the brevis distal to the level of the pectoral crest and the two insert together on the posterior surface of the radius at its midlength, distal to the brachialis radialis, the longus' share of the common area remaining proximal to the brevis'.",
        "attachmentNote": "Ornithorhynchus anatinus. The biceps longus has left the ulna: in both echidnas it inserts on the radial edge of the ulna and here it has moved onto the radius, fused with the brevis. A head changing which zeugopod bone it ends on, inside one clade.",
        "attachments": {
            "origin": [o("procoracoid", "ventral"), o("interclavicle", "dorsal"),
                       o("coracoid", "ventral")],
            "insertion": [o("radius", "posterior")],
        },
        "division": "heads",
        "parts": [p("Biceps longus (caput longum)"), p("Biceps brevis (caput breve)")],
        "sources": [SRC],
    }),

    ("brachialis", ZAG, {
        "name": "Brachialis ulnaris + brachialis radialis",
        "present": "yes",
        "origin": "Radialis wedging proximally onto the proximal dorsal surface of the humerus between the triceps lateralis in front and the triceps accessorius behind, then descending along the anterior dorsoventral line; ulnaris anterior and distal to it, reaching a little onto the distal ventral surface around the preaxial side of the bone.",
        "insertion": "Ulnaris on the radial edge of the posterior surface of the ulna just distal to the elbow joint; radialis just distal to that on the posterior surface of the radius, descending almost to its midlength.",
        "attachmentNote": "Zaglossus bruijnii. Romer (1922) held the origin on the distal ventral surface of the humerus to be the primitive tetrapod condition and its spread onto the proximal dorsal surface to be a synapsid advance; this genus keeps a trace of the ventral origin that the other two have lost. Allen (1912) mistook the radial head for the brachioradialis.",
        "attachments": {
            "origin": [o("humerus", "dorsal"), o("humerus", "ventral")],
            "insertion": [o("ulna", "posterior"), o("radius", "posterior")],
        },
        "division": "heads",
        "parts": [p("Brachialis ulnaris (caput ulnare)"),
                  p("Brachialis radialis (caput radiale)")],
        "divisionNote": "Gambaryan et al. read the two-headed brachialis as a remnant of a stage with freer rotation of the radius against the ulna, since intra-antebrachial mobility in living monotremes is extremely reduced — a muscle keeping a division its joint no longer uses.",
        "sources": [SRC],
    }),
    ("brachialis", TAC, {
        "name": "Brachialis ulnaris + brachialis radialis",
        "present": "yes",
        "origin": "Both heads side by side on the proximal dorsal surface of the humerus, the ulnaris anterior to the radialis, the radialis approaching the humeral head anterior to the triceps lateralis origin.",
        "insertion": "Ulnaris on the radial edge of the posterior surface of the ulna just distal to the elbow joint; radialis just distal to it on the posterior surface of the radius, descending almost to its midlength.",
        "attachmentNote": "Tachyglossus aculeatus. The two heads are furthest apart in this genus and closest together in the platypus, with the long-beaked echidna between them.",
        "attachments": {
            "origin": [o("humerus", "dorsal")],
            "insertion": [o("ulna", "posterior"), o("radius", "posterior")],
        },
        "division": "heads",
        "parts": [p("Brachialis ulnaris (caput ulnare)"),
                  p("Brachialis radialis (caput radiale)")],
        "sources": [SRC],
    }),
    ("brachialis", ORN, {
        "name": "Brachialis ulnaris + brachialis radialis",
        "present": "yes",
        "origin": "The two heads least separate of the three genera, arising together from the proximal dorsal surface of the humerus and widely separating the triceps lateralis origin in front from the triceps accessorius behind.",
        "insertion": "As in the echidnas, but the radialis insertion on the radius is shorter; the ulna carries a groove for the flat terminal tendon of the ulnaris.",
        "attachmentNote": "Ornithorhynchus anatinus. The groove on the ulna is an osteological correlate for a tendon, which is rarer in this dataset than a scar for a fleshy attachment.",
        "attachments": {
            "origin": [o("humerus", "dorsal")],
            "insertion": [o("ulna", "posterior"), o("radius", "posterior")],
        },
        "division": "heads",
        "parts": [p("Brachialis ulnaris (caput ulnare)"),
                  p("Brachialis radialis (caput radiale)")],
        "sources": [SRC],
    }),
]


def main():
    write = "--write" in sys.argv
    files = sorted(ROOT.glob("data/muscles-*.json"))
    docs = {path: json.loads(path.read_text()) for path in files}

    index = {}
    for path, doc in docs.items():
        for m in doc["muscles"]:
            index[m["id"]] = (path, m)

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

        target = {"species": sid, **spec}
        if occ is None:
            if write:
                muscle["occurrences"].append(target)
            added += 1
            continue

        # Seed, not sync. `MANAGED` used to mean "this script owns the field
        # and replaces it", which made every build reimpose the table's original
        # copy over later curation — dropping `russell-bauer-2008` and
        # `cunningham-1882` off rows that had since been scored against a second
        # source, and truncating the attachmentNote back to the pre-merge
        # version. It now means "this script may FILL the field": absent fields
        # get the seeded value, present ones are left alone, and `sources` is a
        # union so a citation can never be seeded away. Revising a seeded row
        # means editing the JSON.
        merged = dict(occ)
        for field, value in target.items():
            if field not in merged:
                merged[field] = value
        merged["sources"] = sorted(set(occ.get("sources", []))
                                   | set(target.get("sources", [])))
        merged = {"species": sid, **{k: v for k, v in merged.items() if k != "species"}}
        if merged == occ:
            unchanged += 1
            continue
        if write:
            occ.clear()
            occ.update(merged)
        updated += 1

    for line in missing:
        print(f"  MISS  {line}")
    print(f"\n{len(SEED)} rows from Gambaryan et al. (2015): {added} to add, "
          f"{updated} to update, {unchanged} already current, {len(missing)} unresolved")

    if write and (added or updated):
        for path, doc in docs.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {len(docs)} files")
    elif not write:
        print("(dry run — pass --write to apply)")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
