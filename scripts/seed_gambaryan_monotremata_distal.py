#!/usr/bin/env python3
"""Gambaryan et al. (2015), part two: the monotreme forearm and hand.

The companion to `seed_gambaryan_monotremata.py`, which took the girdle and the
arm. Same paper, same three genera — *Zaglossus bruijnii*, *Tachyglossus
aculeatus*, *Ornithorhynchus anatinus* — and the same per-genus Origin and
Insertion structure. Hand was the dataset's thinnest region at 47% and forearm
its second thinnest at 58%, and no monotreme row existed in either.

The distal half of this paper is where its argument lives. Its thesis is that
Tachyglossidae are the more primitive monotremes above the elbow and
*Ornithorhynchus* below it, so the girdle pass took the half where the echidnas
lead and this one takes the half where the platypus does.

Five things here are more than rows:

* **A muscle the dataset records as lost in amniotes, found in a mammal.**
  `contrahentium-caput-longum` — the urodele ulnocarpalis — reads "an amphibian
  muscle lost in amniotes, retaining only its distal derivatives", with no
  therian row on it at all. Gambaryan et al. identify it as the caput humerale
  profundum of the flexor digitorum profundus in *Ornithorhynchus*: it wedges
  between the caput olecrani and the caput ulnare exactly as the urodele
  ulnocarpalis wedges between the two heads of the palmaris communis profundus
  (which are Diogo & Abdala's flexor accessorius lateralis and medialis, both
  records here), and it ends on the ligamentum flexorium commune transversum,
  which they read as the surviving postaxial segment of the urodele transverse
  subcarpal ligament. Against Straus (1942), who held the muscle dissolved into
  the flexor digitorum profundus beyond amphibians. Scored `yes` in the platypus
  and `uncertain` in both echidnas, where the belly is present and the
  diagnostic ligament is reported only by Kajava (1911) and only as variation.

* **The prepollex is not an anuran peculiarity.** `GAPS.md` §1 singles it out as
  the position-versus-identity case: anurans lost digit I and the preaxial
  muscles attach to the prepollex instead. Monotremes have one too, did not lose
  digit I, and hang more on it — the entire flexor carpi radialis insertion in
  all three genera, plus the origins of the interossei of digits I to III.

* **Two sourced absences that are characters.** The palmaris longus is absent in
  all three genera, surviving in *Zaglossus* only as a bundle of the cutaneus
  trunci, and Gambaryan et al. list that absence among the primitive features.
  The intermetacarpales are absent in both echidnas and present in the platypus
  — explicitly against Kajava (1911) and Howell (1936), who reported the
  reverse.

* **A homology claim about which record a muscle belongs on.** The monotreme
  extensor carpi radialis inserts symmetrically about the mid-axis of the
  metacarpus, centred on metacarpal III, and Gambaryan et al. say that makes it
  comparable with the REPTILIAN extensor digitorum communis (= humerodorsalis of
  Haines 1939, already a synonym on `extensor-digitorum`) rather than with the
  reptilian extensor carpi radialis. Recorded in the note on the rows and in the
  record's homology block. Not acted on: moving it would be a re-score of six
  other columns on one remark.

* **One new record.** `extensor-digitorum-profundus`, for the extensor pollicis
  et indicis — Haines' (1939) extensor digitorum profundus, and Diogo & Abdala's
  extensor pollicis longus + extensor indicis + extensor digitus III proprius
  rolled into one. The dataset had nowhere to put a deep digital extensor
  arising from the ulna, and its digital formula differs in all three genera
  with a stated polarity, which is the kind of character the region has almost
  none of.

    python3 scripts/seed_gambaryan_monotremata_distal.py           # report
    python3 scripts/seed_gambaryan_monotremata_distal.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "gambaryan-etal-2015"
FILE = ROOT / "data/muscles-forearm-hand.json"

ZAG = "zaglossus-bruijnii"
TAC = "tachyglossus-aculeatus"
ORN = "ornithorhynchus-anatinus"

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
V = "variable"

# The new record. Created here rather than authored into the data file so a
# rebuild reproduces it, following seed_walthall_taricha.py.
NEW_RECORD = {
    "id": "extensor-digitorum-profundus",
    "name": "Extensor digitorum profundus",
    "region": "forearm",
    "subregion": "deep dorsal",
    "segment": "zeugopod",
    "mass": "dorsal",
    "layer": "profundus",
    "developmental": "Somitic; deep dorsal mass.",
    "synonyms": [
        "extensor digitorum profundus (Haines 1939)",
        "extensor pollicis et indicis (Gambaryan et al. 2015)",
        "extensor pollicis longus + extensor indicis + extensor digitus III proprius (Diogo & Abdala 2010)",
    ],
    "consensus": {
        "origin": "Anterior (dorsal) surface of the ulna.",
        "insertion": "Ungual phalanges, preaxial and proximal to the corresponding branches of the extensor digitorum.",
        "action": "Extends the terminal phalanges.",
        "innervation": "Radial nerve, deep branch.",
    },
    "attachments": {
        "origin": [o("ulna", "anterior")],
        "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus")],
    },
    "homology": {
        "confidence": "moderate",
        "notes": (
            "A deep digital extensor distinct from the extensor digitorum, "
            "arising from the ulna rather than the humerus. Haines (1939) named "
            "it the extensor digitorum profundus; Diogo & Abdala (2010) carry it "
            "in therians as three muscles — extensor pollicis longus, extensor "
            "indicis and extensor digitus III proprius — and Gambaryan et al. "
            "(2015) find it undivided in monotremes and count that integrity "
            "among the primitive features. **Scored so far only in Monotremata, "
            "so its absence elsewhere in this dataset is unsampled rather than "
            "observed** — the record exists because there was nowhere to put a "
            "muscle three sources agree on, not because monotremes are the only "
            "animals with one."
        ),
        "openQuestion": (
            "Is the therian three-way split of this muscle one event or three, "
            "and does the extensor indicis retain the tendon to digit III (and "
            "sometimes IV) because it is the unsplit remnant?"
        ),
        "related": ["extensor-digitorum", "extensores-digitorum-breves",
                    "abductor-pollicis-longus"],
    },
    "nerves": [{"nerve": "radial-deep"}],
    "occurrences": [],
}

UNSAMPLED = (" Scored here from Monotremata only; the muscle is not yet scored "
             "in other taxa in this dataset, so its absence elsewhere is "
             "unsampled rather than observed.")

SEED: list[tuple[str, str, dict]] = [

    # ------------------------------------------------------------------
    # Dorsal forearm
    # ------------------------------------------------------------------
    ("supinator", ZAG, {
        "name": "Supinator",
        "present": "yes",
        "origin": "Fleshy from the entire ventral surface of the ectepicondylus of the humerus, beneath the other antebrachial extensors, with an aponeurosis of origin on its anterior side running almost to the midlength of the belly.",
        "insertion": "Fleshy on the preaxial side of the proximal three-quarters of the radius, a little clear of the elbow joint.",
        "attachmentNote": "Zaglossus bruijnii. The three genera differ in which stretch of the radius is taken: the proximal three-quarters here, the distal two-thirds in Tachyglossus, the proximal half in the platypus.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("radius", "anterior")],
        },
        "sources": [SRC],
    }),
    ("supinator", TAC, {
        "name": "Supinator",
        "present": "yes",
        "origin": "Ventral side of the ectepicondylus by two aponeuroses covering the anterior and anteromedial sides of the belly, some fibres arising from the proximal quarter of the medial aponeurosis of origin of the extensor digitorum communis.",
        "insertion": "Fleshy on the anteropreaxial side of the distal two-thirds of the radius, a little clear of the wrist joint.",
        "attachmentNote": "Tachyglossus aculeatus. The only one of the three whose supinator insertion is distal rather than proximal on the radius.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("radius", "anterior")],
        },
        "sources": [SRC],
    }),
    ("supinator", ORN, {
        "name": "Supinator",
        "present": "yes",
        "origin": "Ventral side of the ectepicondylus, mostly fleshy, aided by an aponeurosis on the anterolateral side.",
        "insertion": "Fleshy on the anteropreaxial side of the proximal half of the radius, a little clear of the elbow joint.",
        "attachmentNote": "Ornithorhynchus anatinus. This record's homology note calls the therian supinator a muscle with no confidently identified counterpart outside Mammalia; the monotreme rows are the outgroup evidence for that statement rather than against it, since monotremes are mammals.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("radius", "anterior")],
        },
        "sources": [SRC],
    }),

    ("brachioradialis", ZAG, {
        "name": "Brachioradialis",
        "present": "yes",
        "origin": "Fleshy from the ventral surface of the ectepicondylus near its proximal border, deeper than the extensor carpi radialis.",
        "insertion": "Terminal tendon passing under the abductor pollicis longus onto the dorsal projection of the preaxial carpal complex, between its joints with distal carpals II and III; the tendon is held at the distal end of the radius by a connective-tissue sheath.",
        "attachmentNote": "Zaglossus bruijnii. **The insertion is not on the radius.** Everywhere else in this dataset the brachioradialis ends on the radius — that is what the name is about — and in all three monotreme genera it passes the radius entirely and ends on the fused radiale + intermedium + centrale, the preaxial carpal complex.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("carpal-preaxial-complex", "dorsal")],
        },
        "sources": [SRC],
    }),
    ("brachioradialis", TAC, {
        "name": "Brachioradialis",
        "present": "yes",
        "origin": "Fleshy from the ventral surface of the ectepicondylus along its proximal border, only the postaxial part of the origin passing under that of the extensor carpi radialis.",
        "insertion": "Terminal tendon passing under the abductor pollicis longus onto the dorsal projection of the preaxial carpal complex, between its joints with distal carpals II and III.",
        "attachmentNote": "Tachyglossus aculeatus. Allen (1912) took the radial head of the brachialis for this muscle, which is worth noting because the two do lie together and the mistake is in the older literature the therian rows on this record descend from.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("carpal-preaxial-complex", "dorsal")],
        },
        "sources": [SRC],
    }),
    ("brachioradialis", ORN, {
        "name": "Brachioradialis",
        "present": "yes",
        "origin": "Fleshy from the ventral surface of the ectepicondylus clear of its proximal border, deeper than both the extensor carpi radialis and the extensor digitorum communis, which has expanded proximally along the ectepicondylar border.",
        "insertion": "As in the echidnas, onto the preaxial carpal complex; the only real difference is that the tendon is bound to the distal end of the radius by a transverse branch of the abductor pollicis longus tendon rather than by its own sheath.",
        "attachmentNote": "Ornithorhynchus anatinus. Same bone, different retaining structure — the tendon is held down by a neighbour's tendon instead of by a ligament of its own.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("carpal-preaxial-complex", "dorsal")],
        },
        "sources": [SRC],
    }),

    ("extensor-antebrachii-carpi-radialis", ZAG, {
        "name": "Extensor carpi radialis",
        "present": "yes",
        "origin": "Ventral side of the crista supraectepicondylaris, a crest along the proximal border of the ectepicondylus of the humerus.",
        "insertion": "Terminal tendon passing under the abductor pollicis longus and under a transverse retinaculum binding it to the distal radius, then splitting into three branches onto the dorsal bases of metacarpals II-IV; the branch to metacarpal III is thickest and that to IV is sometimes absent.",
        "attachmentNote": "Zaglossus bruijnii. **The insertion is symmetrical about metacarpal III**, the mid-axis of the metacarpus, and Gambaryan et al. list that symmetry among the primitive monotreme features. They draw a homology conclusion from it: a muscle centred like this is comparable with the REPTILIAN extensor digitorum communis — the humerodorsalis of Haines (1939), already a synonym on `extensor-digitorum` — rather than with the reptilian extensor carpi radialis, which ends more proximally and preaxially. The rows stay on this record; see its homology block.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("metacarpals", "dorsal")],
        },
        "sources": [SRC],
    }),
    ("extensor-antebrachii-carpi-radialis", TAC, {
        "name": "Extensor carpi radialis",
        "present": "yes",
        "origin": "Ventral side of the proximal and preaxial borders of the ectepicondylus.",
        "insertion": "As in the long-beaked echidna, but the branch to metacarpal II is considerably thinner and that to metacarpal IV is absent — though Haines (1939) described one.",
        "attachmentNote": "Tachyglossus aculeatus. A disagreement with Haines over whether the fourth branch exists, kept because the record's own homology note says the interesting variable on this muscle is the level and spread of its insertion rather than its presence.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("metacarpals", "dorsal")],
        },
        "sources": [SRC],
    }),
    ("extensor-antebrachii-carpi-radialis", ORN, {
        "name": "Extensor carpi radialis",
        "present": "yes",
        "origin": "Ventral surface of the ectepicondylus parallel to its proximal border, deeper than the extensor digitorum communis.",
        "insertion": "Three terminal branches onto the dorsal bases of metacarpals II-IV. The tendon passes under the abductor pollicis longus but over that muscle's transverse branch, and there is no transverse retinaculum binding it to the radius as there is in both echidnas.",
        "attachmentNote": "Ornithorhynchus anatinus. The full three-branch insertion is retained here where the short-beaked echidna has lost the fourth; the retinaculum that holds the tendon down in Tachyglossidae is absent.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("metacarpals", "dorsal")],
        },
        "sources": [SRC],
    }),

    ("abductor-pollicis-longus", ZAG, {
        "name": "Abductor pollicis longus",
        "present": "yes",
        "origin": "Adjacent parts of the anterior sides of the radius and ulna, descending from the elbow joint over more than half the length of the radius.",
        "insertion": "Terminal tendon formed in the distal quarter of the antebrachium, running under its own transverse retinaculum in a groove on the distal end of the radius to the preaxial side of metacarpal I.",
        "attachmentNote": "Zaglossus bruijnii. The groove on the distal radius is an osteological correlate for the tendon rather than for the muscle.",
        "attachments": {
            "origin": [o("radius", "anterior"), o("ulna", "anterior")],
            "insertion": [o("metacarpals", "anterior")],
        },
        "sources": [SRC],
    }),
    ("abductor-pollicis-longus", TAC, {
        "name": "Abductor pollicis longus",
        "present": "yes",
        "origin": "The ulna only. More postaxially the anterior surface of the ulna is taken by the extensor digitorum profundus, and the boundary between the two origins is marked on the bone by a rugosity.",
        "insertion": "Distal aponeuroses on the inner and outer surfaces of the belly fuse into a terminal tendon passing under its own transverse retinaculum at the distal end of the radius to the preaxial side of metacarpal I.",
        "attachmentNote": "Tachyglossus aculeatus. The one genus whose abductor pollicis longus has left the radius entirely, and it leaves a readable boundary: a rugosity on the ulna separating it from the extensor digitorum profundus. Two muscles sharing a bone and marking where one stops.",
        "attachments": {
            "origin": [o("ulna", "anterior")],
            "insertion": [o("metacarpals", "anterior")],
        },
        "sources": [SRC],
    }),
    ("abductor-pollicis-longus", ORN, {
        "name": "Abductor pollicis longus",
        "present": "yes",
        "origin": "Anterior side of the proximal end of the radius and the adjacent part of the ulna.",
        "insertion": "Terminal tendon under its own transverse retinaculum at the distal end of the radius to the preaxial side of the base of metacarpal I, giving off at the level of the wrist a postaxial branch which passes over the brachioradialis tendon, deeper than every other extensor tendon, to insert on the preaxial side of the ulnare.",
        "attachmentNote": "Ornithorhynchus anatinus. The postaxial branch onto the ulnare is unique to this genus, and it is the structure that holds the brachioradialis tendon down in place of the sheath the echidnas use.",
        "attachments": {
            "origin": [o("radius", "anterior"), o("ulna", "anterior")],
            "insertion": [o("metacarpals", "anterior"),
                          o("carpals", "anterior", "ulnare")],
        },
        "sources": [SRC],
    }),

    ("extensor-digitorum-profundus", ZAG, {
        "name": "Extensor pollicis et indicis",
        "present": "yes",
        "origin": "Anterior surface of the ulna except its distal end and the olecranon, with a small tubercle at the proximal point of the area of origin.",
        "insertion": "A flat tendon, formed as a superficial aponeurosis over the distal two-thirds of the belly, passing under the retinaculum extensorum deeper than the extensor digitorum communis tendon and separated from it by a bridge of that retinaculum, then splitting into three branches to the ungual phalanges of digits II-IV, each preaxial and proximal to the corresponding extensor digitorum branch.",
        "attachmentNote": "Zaglossus bruijnii. Digits II-IV here, I-IV in Tachyglossus and I-III in the platypus; Gambaryan et al. read the four-digit condition as the most primitive of the three." + UNSAMPLED,
        "attachments": {
            "origin": [o("ulna", "anterior")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus")],
        },
        "division": "single",
        "divisionNote": "Undivided, and its integrity is listed among the primitive monotreme features. Placentals usually split it into the extensor pollicis longus and the extensor indicis, the latter often keeping a tendon to digit III and sometimes IV.",
        "sources": [SRC],
    }),
    ("extensor-digitorum-profundus", TAC, {
        "name": "Extensor pollicis et indicis",
        "present": "yes",
        "origin": "Anterior surface of the ulna, excluding its distal end but including the base of the olecranon; the belly also receives a small bundle of fibres from the extensor digitorum communis.",
        "insertion": "Branches to the ungual phalanges of digits II-IV as in the long-beaked echidna, plus a branch to the ungual phalanx of digit I which joins the corresponding extensor digitorum communis tendon at its insertion; before dividing, the ventral surface of the common tendinous plate also sends deeper branches to the bases of the preungual phalanges of digits II-IV.",
        "attachmentNote": "Tachyglossus aculeatus. The four-digit formula Gambaryan et al. take as primitive, and the only one of the three with the extra collateral insertions onto the preungual phalanges." + UNSAMPLED,
        "attachments": {
            "origin": [o("ulna", "anterior")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus"),
                          o("phalanges-manus", "distal")],
        },
        "division": "single",
        "sources": [SRC],
    }),
    ("extensor-digitorum-profundus", ORN, {
        "name": "Extensor pollicis et indicis",
        "present": "yes",
        "origin": "Mainly the olecranon: the origin descends from its anterior projection along the anterior side of the ulnar crest to the level of the elbow joint and a little beyond.",
        "insertion": "A flat tendon over the distal half of the belly, passing under the retinaculum extensorum deeper than the extensor digitorum communis tendon and splitting into three branches to the ungual phalanges of digits I-III, shared with the corresponding extensor digitorum communis branches.",
        "attachmentNote": "Ornithorhynchus anatinus. The origin has withdrawn onto the olecranon, off the ulnar shaft the echidnas use, and the digital formula has shifted preaxially — I-III rather than II-IV." + UNSAMPLED,
        "attachments": {
            "origin": [o("ulna", "anterior", "olecranon")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus")],
        },
        "division": "single",
        "sources": [SRC],
    }),

    ("extensor-digitorum", ZAG, {
        "name": "Extensor digitorum communis",
        "present": "yes",
        "origin": "Ventral side of the preaxial border of the ectepicondylus, deeper than the extensor carpi ulnaris and sharing its aponeurosis of origin; that aponeurosis also gives rise to the extensor digitorum lateralis.",
        "insertion": "A flat terminal tendon passing under the retinaculum extensorum, expanding strongly on the dorsum of the manus and splitting into three branches to the ungual phalanges of digits II-IV.",
        "attachmentNote": "Zaglossus bruijnii. One of the three specimens carried the pre-mammalian condition as an individual variation: the extensor digitorum communis and the extensor digitorum profundus fused into a single tendon before branching, giving one extensor to all five digits with a humeral and an ulnar head. Gambaryan et al. treat that variant as a model of the ancestral integrity of the digital extensors, and the fibre slip that crosses between the two muscles in Tachyglossus as the other trace of it.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus")],
        },
        "division": "divided",
        "parts": [p("Extensor digitorum communis"),
                  p("Extensor digitorum lateralis", membership=D,
                    note="Gambaryan et al. give it as Diogo & Abdala's (2010) extensor digiti minimi. Marked disputed because in all three genera its fibres arise from the extensor digitorum communis' own aponeurosis of origin rather than from bone, which is an argument that it is a differentiation of that muscle rather than an independent one. In Zaglossus, two of three specimens also had a fleshy origin directly on the ectepicondylus.")],
        "divisionNote": "The lateralis inserts on digits IV and V — in this genus onto the ungual phalanx of IV and the PREUNGUAL phalanx of V, whose ungual is reduced.",
        "sources": [SRC],
    }),
    ("extensor-digitorum", TAC, {
        "name": "Extensor digitorum communis",
        "present": "yes",
        "origin": "Ventral side of the distal-preaxial angle of the ectepicondylus, deeper than the extensor carpi ulnaris, by two superficial aponeuroses; the outer one is shared with the humeral head of the extensor carpi ulnaris and with the extensor digitorum lateralis, and forms a longitudinal trough housing the belly of the latter.",
        "insertion": "Three main branches to digits II-IV, the branch to digit II sending a minor sub-branch to the ungual phalanx of digit I and the branch to digit IV a pair of sub-branches to the ungual phalanx of digit V.",
        "attachmentNote": "Tachyglossus aculeatus. Some fibres split off the belly to join the extensor digitorum profundus, which is the second trace of the undivided ancestral extensor.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus")],
        },
        "division": "divided",
        "parts": [p("Extensor digitorum communis"),
                  p("Extensor digitorum lateralis", membership=D)],
        "divisionNote": "The lateralis reaches the ungual phalanges of both digits IV and V here, where in the long-beaked echidna digit V takes only the preungual.",
        "sources": [SRC],
    }),
    ("extensor-digitorum", ORN, {
        "name": "Extensor digitorum communis",
        "present": "yes",
        "origin": "Ventral side of the ectepicondylus, ascending from the crest on its preaxial apex — where it arises under the extensor carpi ulnaris — along the whole proximal border, where it arises over the extensor carpi radialis. Two aponeuroses of origin, the outer shared with the extensor carpi ulnaris and the extensor digitorum lateralis.",
        "insertion": "On the manus the terminal tendon divides into a superficial sheet splitting to the ungual phalanges of digits I-IV and a deep sheet splitting to those of digits II-IV; the long tendons also send short deep branches to the bases of the preungual phalanges and fuse dorsally with the interdigital tendons of the cutaneus trunci.",
        "attachmentNote": "Ornithorhynchus anatinus. The dorsal digital tendons here are continuous with the skin muscle, which is a muscle end no correlate would record — the cutaneus trunci branches run out between the digits and insert on opposing sides of the claws.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus"),
                          o("phalanges-manus", "distal")],
        },
        "division": "divided",
        "parts": [p("Extensor digitorum communis"),
                  p("Extensor digitorum lateralis", membership=D,
                    note="Rudimentary in this genus: a very thin tendon whose branches to digits IV and V thin out and fuse with the corresponding extensor digitorum communis tendons before insertion.")],
        "sources": [SRC],
    }),

    ("extensor-antebrachii-carpi-ulnaris", ZAG, {
        "name": "Extensor carpi ulnaris",
        "present": "yes",
        "origin": "Two heads. The humeral head from the apex of the ectepicondylus by an inner-side aponeurosis shared with the extensor digitorum communis and lateralis; the ulnar head from the anterior aspect of the ulna at the level of the proximal end of the radius.",
        "insertion": "The two heads fuse at the midlength of the antebrachium into a common tendon which passes under a transverse retinaculum at the distal end of the ulna and inserts on digit V by two branches — a proximal one on the postaxial side of its metacarpophalangeal joint and a distal one on the preaxial side of its proximal interphalangeal joint. Distal to the ulnare the tendon is underlaid by a collagen-adipose pad.",
        "attachmentNote": "Zaglossus bruijnii. Gambaryan et al. list the extremely distal insertion of this muscle, almost reaching the end of digit V, among the ADVANCED monotreme features — a wrist extensor that has become a digital one.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle"),
                       o("ulna", "anterior")],
            "insertion": [o("phalanges-manus", "proximal"),
                          o("metacarpals", "posterior")],
        },
        "division": "heads",
        "parts": [p("Caput humerale"), p("Caput ulnare")],
        "sources": [SRC],
    }),
    ("extensor-antebrachii-carpi-ulnaris", TAC, {
        "name": "Extensor carpi ulnaris",
        "present": "yes",
        "origin": "Humeral head from the apex of the ectepicondylus, expanding onto its dorsal side, by the inner-side aponeurosis shared with the extensor digitorum communis and lateralis; ulnar head from the anterior aspect of the olecranon up to the level of the proximal end of the radius.",
        "insertion": "The two heads converge bipennately on a common aponeurosis and the tendon passes under a transverse retinaculum at the end of the ulna to insert extremely distally, on the base of the ungual phalanx of digit V, postaxial to the extensor digitorum lateralis.",
        "attachmentNote": "Tachyglossus aculeatus. The most distal of the three: this one reaches the terminal phalanx.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle"),
                       o("ulna", "anterior", "olecranon")],
            "insertion": [o("phalanges-manus", landmark="ungual-phalanges-manus")],
        },
        "division": "heads",
        "parts": [p("Caput humerale"), p("Caput ulnare")],
        "sources": [SRC],
    }),
    ("extensor-antebrachii-carpi-ulnaris", ORN, {
        "name": "Extensor carpi ulnaris",
        "present": "yes",
        "origin": "One head only, the humeral: a fleshy origin on the apex of the ectepicondylus slightly aided by the aponeurosis shared with the extensor digitorum lateralis and communis.",
        "insertion": "Terminal tendon under the transverse retinaculum at the distal end of the ulna, together with the extensor digitorum lateralis tendon, splitting in the metacarpal region into four branches: three insert in cascade on the postaxial side of the three joints of digit V, and the most proximal thin one deviates postaxially to join the interosseus V lateralis on the outer side of metacarpal V.",
        "attachmentNote": "Ornithorhynchus anatinus. **The ulnar head is gone** — both echidnas have two heads and the platypus one, so the division is polymorphic within Monotremata and the clade computes as `variable`. A muscle branch ending on another muscle rather than on bone is also worth noting: the fourth branch joins the interosseus.",
        "attachments": {
            "origin": [o("humerus", "ventral", "lateral-epicondyle")],
            "insertion": [o("phalanges-manus", "posterior"),
                          o("metacarpals", "posterior")],
        },
        "division": "single",
        "divisionNote": "Single against `heads` in both echidnas, on the loss of the caput ulnare.",
        "sources": [SRC],
    }),

    ("anconeus", ZAG, {
        "name": "Epitrochleoanconeus lateralis",
        "present": "yes",
        "origin": "Dorsal surface of the ectepicondylus of the humerus, preaxial to the triceps medialis.",
        "insertion": "Along the anterior border of the olecranon, descending onto the ulna a little distal to the elbow joint.",
        "note": "Zaglossus bruijnii. Gambaryan et al. give this as the m. anconeus of Diogo & Abdala (2010) — which is this record — and read it as homologous with the extensor antebrachii ulnaris of lower tetrapods (Haines 1939).",
        "attachments": {
            "origin": [o("humerus", "dorsal", "lateral-epicondyle")],
            "insertion": [o("ulna", "anterior", "olecranon")],
        },
        "sources": [SRC],
    }),
    ("anconeus", TAC, {
        "name": "Epitrochleoanconeus lateralis",
        "present": "yes",
        "origin": "Dorsal surface of the ectepicondylus, preaxial to the triceps medialis.",
        "insertion": "The anterior border of the olecranon, not descending distal to the elbow joint; the insertion is marked by a rugosity.",
        "note": "Tachyglossus aculeatus. The shortest insertion of the three, and the only one that leaves a named rugosity.",
        "attachments": {
            "origin": [o("humerus", "dorsal", "lateral-epicondyle")],
            "insertion": [o("ulna", "anterior", "olecranon")],
        },
        "sources": [SRC],
    }),
    ("anconeus", ORN, {
        "name": "Epitrochleoanconeus lateralis",
        "present": "yes",
        "origin": "Dorsal surface of the ectepicondylus, preaxial to the triceps medialis.",
        "insertion": "Along the anterior border of the olecranon, descending onto the ulna a little distal to the elbow joint.",
        "note": "Ornithorhynchus anatinus. = m. anconeus sensu Diogo & Abdala (2010). One of the two links in the naming chain that runs the other way: here Gambaryan et al. keep a name of their own for a muscle Diogo & Abdala call by the name this record uses.",
        "attachments": {
            "origin": [o("humerus", "dorsal", "lateral-epicondyle")],
            "insertion": [o("ulna", "anterior", "olecranon")],
        },
        "sources": [SRC],
    }),

    ("epitrochleoanconeus", ZAG, {
        "name": "Epitrochleoanconeus medialis",
        "present": "yes",
        "origin": "Dorsal surface of the entepicondylus of the humerus, close to its tip.",
        "insertion": "Posterior projection of the olecranon apex.",
        "note": "Zaglossus bruijnii. = m. epitrochleoanconeus sensu Diogo & Abdala (2010), and homologous with the flexor antebrachii ulnaris of lower tetrapods (Jouffroy et al. 1971). It is separated from the triceps medialis by the nerves converging on the entepicondylar foramen, which is how the two are told apart.",
        "attachments": {
            "origin": [o("humerus", "dorsal", "medial-epicondyle")],
            "insertion": [o("ulna", "posterior", "olecranon")],
        },
        "sources": [SRC],
    }),
    ("epitrochleoanconeus", TAC, {
        "name": "Epitrochleoanconeus medialis",
        "present": "yes",
        "origin": "Dorsal surface of the entepicondylus, close to its tip.",
        "insertion": "Posterior projection of the olecranon apex.",
        "note": "Tachyglossus aculeatus. Identical in all three genera, which is worth recording as sameness rather than omitting: three species examined, one arrangement found.",
        "attachments": {
            "origin": [o("humerus", "dorsal", "medial-epicondyle")],
            "insertion": [o("ulna", "posterior", "olecranon")],
        },
        "sources": [SRC],
    }),
    ("epitrochleoanconeus", ORN, {
        "name": "Epitrochleoanconeus medialis",
        "present": "yes",
        "origin": "Dorsal surface of the tip of the entepicondylus.",
        "insertion": "Posterior projection of the olecranon apex.",
        "note": "Ornithorhynchus anatinus.",
        "attachments": {
            "origin": [o("humerus", "dorsal", "medial-epicondyle")],
            "insertion": [o("ulna", "posterior", "olecranon")],
        },
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Ventral forearm
    # ------------------------------------------------------------------
    ("pronator-teres", ZAG, {
        "name": "Pronator teres",
        "present": "yes",
        "origin": "A round area on the ventral side of the entepicondylus, plus an aponeurosis on the posterior side of the muscle shared with the flexor carpi radialis.",
        "insertion": "Preaxial side of the radius distal to its midlength.",
        "note": "Zaglossus bruijnii. The most superficial muscle on the inner surface of the antebrachium in all three genera.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("radius", "anterior")],
        },
        "sources": [SRC],
    }),
    ("pronator-teres", TAC, {
        "name": "Pronator teres",
        "present": "yes",
        "origin": "A narrower area on the ventral side of the entepicondylus than in the long-beaked echidna, with aponeuroses of origin on both the posterior side — shared with the flexor carpi radialis — and the anterior side of the belly.",
        "insertion": "Preaxial side of the distal part of the radius.",
        "note": "Tachyglossus aculeatus.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("radius", "anterior")],
        },
        "sources": [SRC],
    }),
    ("pronator-teres", ORN, {
        "name": "Pronator teres",
        "present": "yes",
        "origin": "Ventral side of the apex of the entepicondylus.",
        "insertion": "Terminal aponeuroses on the anterior and posterior sides of the belly fuse into a flat tendon inserting on the POSTERIOR side of the radius close to its midlength.",
        "attachmentNote": "Ornithorhynchus anatinus. Both echidnas insert on the preaxial side of the radius and the platypus on its posterior side, which for a pronator is a change in the line of action and not just in position.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("radius", "posterior")],
        },
        "sources": [SRC],
    }),

    ("flexor-carpi-radialis", ZAG, {
        "name": "Flexor carpi radialis",
        "present": "yes",
        "origin": "Along the ventral side of the entire distal border of the entepicondylus from its apex to the humeral condyle, interrupted by the origin of the caput humerale profundum of the flexor digitorum profundus; aponeuroses of origin on the inner side shared with the pronator teres and on the outer side with the caput humerale superficiale.",
        "insertion": "A wide flat tendon to the proximal apex of the prepollex, which articulates with the preaxial carpal complex; from the prepollex the pull is relayed by ligaments to the distal carpals and metacarpals I-III.",
        "attachmentNote": "Zaglossus bruijnii. **The insertion is on the prepollex**, in all three genera — the element `GAPS.md` §1 singles out as the anuran position-versus-identity case. Monotremes did not lose digit I and have one anyway, and hang more on it than anurans do. The distal ligaments here make it a lever for the carpometacarpal I-III joints as well as for the wrist.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("carpals", "proximal", "prepollex")],
        },
        "sources": [SRC],
    }),
    ("flexor-carpi-radialis", TAC, {
        "name": "Flexor carpi radialis",
        "present": "yes",
        "origin": "As in the long-beaked echidna but uninterrupted by the caput humerale profundum, with relatively shorter fibres and more developed aponeuroses of origin, which descend about half the length of the antebrachium.",
        "insertion": "A flat tendon to the proximal apex of the prepollex, which is connected to the preaxial carpal complex and, by two ligaments, to distal carpals I and II.",
        "attachmentNote": "Tachyglossus aculeatus. Two ligaments to the distal carpals rather than the long-beaked echidna's relay to metacarpals I-III.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("carpals", "proximal", "prepollex")],
        },
        "sources": [SRC],
    }),
    ("flexor-carpi-radialis", ORN, {
        "name": "Flexor carpi radialis",
        "present": "yes",
        "origin": "As in Tachyglossidae, but the belly is flattened in the parasagittal plane and more sharply bipennate: the anterior penna bears an aponeurosis facing the humeral condyle and the radius, the posterior penna two, shared with the pronator teres and the caput humerale superficiale.",
        "insertion": "A round tendon on the proximal apex of the prepollex, with no ligamentous relay onward.",
        "attachmentNote": "Ornithorhynchus anatinus. The prepollex insertion is shared with both echidnas; what is missing here is the onward ligamentous transfer to the carpals and metacarpals, so the muscle acts on the wrist alone.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("carpals", "proximal", "prepollex")],
        },
        "sources": [SRC],
    }),

    ("flexor-digitorum-longus", ZAG, {
        "name": "Flexor digitorum profundus",
        "present": "yes",
        "origin": "Four heads. Caput humerale superficiale from the ventral side of the distal border of the entepicondylus throughout its length; caput humerale profundum compactly from the ventral side of the spina entepicondyli; caput olecrani and caput ulnare undifferentiated from one another and arising together from the proximal three-quarters of the posterior side of the ulna including the olecranon.",
        "insertion": "The heads converge on a common tendon which splits, at a palmar sesamoid, into branches to the ventral bases of the ungual phalanges of digits I-V, II-V or II-IV depending on the specimen.",
        "attachmentNote": "Zaglossus bruijnii. = m. flexor digitorum longus sensu Diogo & Abdala (2010), which is this record. The variable digital formula is the reduction of the marginal fingers this genus is going through, and it is why the authors recommend Z. bartoni — which keeps all five claws — as the better model. In one specimen a few deep fibres arose from the distal quarter of the posterior radius, which they read as a rudiment of the therian caput radiale.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle"),
                       o("ulna", "posterior"),
                       o("ulna", "posterior", "olecranon")],
            "insertion": [o("carpals", landmark="palmar-sesamoid"),
                          o("phalanges-manus", "ventral", "ungual-phalanges-manus")],
        },
        "division": "heads",
        "parts": [p("Caput humerale superficiale"),
                  p("Caput humerale profundum", muscle="contrahentium-caput-longum",
                    note="Identified by Gambaryan et al. as the retained ulnocarpalis; see the contrahentium-caput-longum record."),
                  p("Caput olecrani"), p("Caput ulnare"),
                  p("Caput radiale", membership=V,
                    note="A few deep fibres from the posterior radius in one specimen only, read as a rudiment of the therian head.")],
        "sources": [SRC],
    }),
    ("flexor-digitorum-longus", TAC, {
        "name": "Flexor digitorum profundus",
        "present": "yes",
        "origin": "As in the long-beaked echidna; the origin of the united caput ulnare et olecrani is outlined on the ulna by two crests.",
        "insertion": "A large palmar sesamoid is embedded in the common tendon at the point of branching, so that the common tendon inserts on the proximal apex of that bone and five digital branches leave its distal end for the ungual phalanges; the proximal paw pad attaches to its ventral side.",
        "attachmentNote": "Tachyglossus aculeatus. The sesamoid is large enough here that the muscle does not reach the digits directly at all — it ends on a bone in its own tendon, and a second set of tendons continues from that bone. Five digits, against a variable II-V or II-IV in the long-beaked echidna.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle"),
                       o("ulna", "posterior"),
                       o("ulna", "posterior", "olecranon")],
            "insertion": [o("carpals", "proximal", "palmar-sesamoid"),
                          o("phalanges-manus", "ventral", "ungual-phalanges-manus")],
        },
        "division": "heads",
        "parts": [p("Caput humerale superficiale"),
                  p("Caput humerale profundum", muscle="contrahentium-caput-longum"),
                  p("Caput olecrani"), p("Caput ulnare")],
        "sources": [SRC],
    }),
    ("flexor-digitorum-longus", ORN, {
        "name": "Flexor digitorum profundus",
        "present": "yes",
        "origin": "Caput humerale superficiale from the distal border of the entepicondylus — the biggest and, with fibres only about 2 mm long, by far the strongest head; caput humerale profundum with long fibres from the ventral side of the spina entepicondyli; caput olecrani and the smaller caput ulnare from the posterior side of the ulna below the midlength of the bone, here fully separate from one another.",
        "insertion": "Two palmar sesamoids on the thick common tendon at the level of the carpus. The medial one gives the terminal tendons of digits I-III and the lateral one those of digits IV and V; all five insert on the bases of the ungual phalanges. The thin tendon of the caput humerale profundum inserts on the two sesamoids separately, deeper than the common tendon. Four thick elastin bands run from the sesamoids between the digits into the swimming membrane beyond the claws.",
        "attachmentNote": "Ornithorhynchus anatinus. Gambaryan et al. call this muscle a combination of extreme specialisation and profound primitiveness. The specialisation is the caput humerale superficiale: 2 mm fibres give enormous force for underwater rowing and cost the animal finger extension, which is why it knuckle-walks. The primitiveness is the caput humerale profundum, scored on `contrahentium-caput-longum`.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle"),
                       o("ulna", "posterior"),
                       o("ulna", "posterior", "olecranon")],
            "insertion": [o("carpals", landmark="palmar-sesamoid"),
                          o("phalanges-manus", "ventral", "ungual-phalanges-manus")],
        },
        "division": "heads",
        "parts": [p("Caput humerale superficiale"),
                  p("Caput humerale profundum", muscle="contrahentium-caput-longum"),
                  p("Caput olecrani"), p("Caput ulnare")],
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # The ulnocarpalis, in a mammal
    # ------------------------------------------------------------------
    ("contrahentium-caput-longum", ORN, {
        "name": "Flexor digitorum profundus, caput humerale profundum",
        "present": "yes",
        "origin": "Ventral side of the spina entepicondyli — the distal styloid process of the entepicondylus of the humerus — by long fibres, the belly then squeezing down between the caput olecrani and the caput ulnare of the flexor digitorum profundus.",
        "insertion": "A thin terminal tendon running to the manus in a groove on the deep side of the common flexor tendon, inserting separately on the two palmar sesamoids and, through the ligamentum flexorium commune transversum, on the ventral side of the ulnare.",
        "note": "Ornithorhynchus anatinus. **This record says the muscle was lost in amniotes; Gambaryan et al. say it was not.** Straus (1942) held the urodele ulnocarpalis to have dissolved into the flexor digitorum profundus beyond amphibians. Their evidence that it kept its identity instead is topological and ligamentous, not merely positional: the head wedges between the caput olecrani and the caput ulnare exactly as the urodele ulnocarpalis wedges between the two heads of the palmaris communis profundus sensu Miner (1925) — which are the flexor accessorius lateralis and flexor accessorius medialis of Diogo & Abdala (2010), both records in this dataset — and it ends on the ligamentum flexorium commune transversum, which they identify as the surviving postaxial segment of the transverse subcarpal ligament that the urodele muscle specifically inserts on. On their reading the muscle is not lost but captured: its origin has migrated from the ulna onto the humerus and it has been imprisoned inside the former palmaris communis.",
        "attachmentNote": "The origin is on the HUMERUS, against this record's consensus origin on the distal ulna, and that migration is the substance of the claim rather than an inconvenience for it.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("carpals", landmark="palmar-sesamoid"),
                          o("subcarpal-ligament-transverse")],
        },
        "sources": [SRC],
    }),
    ("contrahentium-caput-longum", TAC, {
        "name": "Flexor digitorum profundus, caput humerale profundum",
        "present": "uncertain",
        "origin": "Ventral side of the spina entepicondyli of the humerus, the belly hidden in the cleft between the caput humerale superficiale and the caput ulnare et olecrani.",
        "insertion": "A thin tendon running separately beneath the main flexor tendon almost as far as the palmar sesamoid.",
        "note": "Tachyglossus aculeatus. `uncertain` rather than `yes` because the head itself is present but the structure that carries Gambaryan et al.'s identification is not confirmed in it. They rest the argument on the ligamentum flexorium commune transversum, which they find in the platypus and report from this animal only on Kajava's (1911) authority and, they say, probably as individual variation. Straus (1942) reports it in some lipotyphlan insectivores as well, so if the identification holds the muscle is not a monotreme relic either.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("carpals", "proximal", "palmar-sesamoid")],
        },
        "sources": [SRC],
    }),
    ("contrahentium-caput-longum", ZAG, {
        "name": "Flexor digitorum profundus, caput humerale profundum",
        "present": "uncertain",
        "origin": "Compact origin on the ventral side of the spina entepicondyli of the humerus.",
        "insertion": "A thin terminal tendon running separately under the common tendon of the other heads, coated on its inner side by the distal-most fibres of the caput ulnare, and fusing into the deep side of that common tendon at the level of the wrist.",
        "note": "Zaglossus bruijnii. `uncertain` on the same grounds as the short-beaked echidna: the head is described in full and is the most distinct of the four, but the transverse ligament that makes it identifiable as the ulnocarpalis is reported only in the platypus. Three rows on one record disagreeing about a muscle's identity rather than its presence is what this field is for.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle")],
            "insertion": [o("carpals", landmark="palmar-sesamoid")],
        },
        "sources": [SRC],
    }),

    ("flexor-carpi-ulnaris", ZAG, {
        "name": "Flexor carpi ulnaris",
        "present": "yes",
        "origin": "Caput humerale from the apex and postaxial part of the distal border of the entepicondylus, with an inner-side aponeurosis shared with the caput humerale superficiale of the flexor digitorum profundus; caput ulnare from the posterior-postaxial side of the ulna along almost its whole length, excluding the distal end but including the olecranon.",
        "insertion": "The two heads form a common aponeurosis and a flat tendon running to the proximal apex of the pisiform, from which three pisometacarpal ligaments descend to the bases of metacarpals II-IV.",
        "attachmentNote": "Zaglossus bruijnii. The pisiform is used as a lever exactly as the prepollex is on the other side of the wrist: it lengthens the moment arm for flexion and lateral abduction, and the ligaments carry the pull on to the carpometacarpal II-IV joints.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle"),
                       o("ulna", "posterior")],
            "insertion": [o("carpals", "proximal", "pisiform")],
        },
        "division": "heads",
        "parts": [p("Caput humerale"), p("Caput ulnare")],
        "sources": [SRC],
    }),
    ("flexor-carpi-ulnaris", TAC, {
        "name": "Flexor carpi ulnaris",
        "present": "yes",
        "origin": "Caput humerale from the dorsal side of the postaxial distal angle of the entepicondylus, itself divided into two portions of which the posterior fuses with the caput ulnare; caput ulnare from the posterior-postaxial side of the ulna throughout its length.",
        "insertion": "Both heads onto the pisiform, from which pisometacarpal ligaments descend to metacarpals II-IV.",
        "attachmentNote": "Tachyglossus aculeatus. The humeral head is itself split here, its anterior portion staying separate from the ulnar head and its posterior portion fusing with it — a division within a division that neither of the other two genera shows.",
        "attachments": {
            "origin": [o("humerus", "dorsal", "medial-epicondyle"),
                       o("ulna", "posterior")],
            "insertion": [o("carpals", "proximal", "pisiform")],
        },
        "division": "heads",
        "parts": [p("Caput humerale"), p("Caput ulnare")],
        "sources": [SRC],
    }),
    ("flexor-carpi-ulnaris", ORN, {
        "name": "Flexor carpi ulnaris",
        "present": "yes",
        "origin": "Caput humerale from the apex and postaxial part of the distal border of the entepicondylus, unipennate; caput ulnare tripennate, from the posterior-postaxial surface of the olecranon, descending a little distal to the elbow joint.",
        "insertion": "A short thick common tendon on the proximal apex of the pisiform. Ligaments from the pisiform to the metacarpals are ABSENT.",
        "attachmentNote": "Ornithorhynchus anatinus. The pisometacarpal ligaments both echidnas use to relay the pull onward are missing, which is the same difference the flexor carpi radialis shows on the preaxial side: in the platypus both wrist flexors act on the wrist alone.",
        "attachments": {
            "origin": [o("humerus", "ventral", "medial-epicondyle"),
                       o("ulna", "posterior", "olecranon")],
            "insertion": [o("carpals", "proximal", "pisiform")],
        },
        "division": "heads",
        "parts": [p("Caput humerale"), p("Caput ulnare")],
        "sources": [SRC],
    }),

    ("palmaris-longus", ZAG, {
        "name": "Palmaris longus",
        "present": "no",
        "note": "Zaglossus bruijnii. Absent, and Gambaryan et al. list the absence among the primitive features of monotremes as a whole. What stands in its place is a bundle of the cutaneus trunci running down the flexor side of the antebrachium to the wrist and joining, through the fascia palmaris manus, the preaxial side of the common tendon of the flexor digitorum profundus near its branching point — which they call the apparent predecessor of the therian palmaris longus. A skin muscle occupying the position of a limb muscle that does not yet exist.",
        "sources": [SRC],
    }),
    ("palmaris-longus", TAC, {
        "name": "Palmaris longus",
        "present": "no",
        "note": "Tachyglossus aculeatus. Absent, and without even the cutaneus trunci bundle the long-beaked echidna has in its place.",
        "sources": [SRC],
    }),
    ("palmaris-longus", ORN, {
        "name": "Palmaris longus",
        "present": "no",
        "note": "Ornithorhynchus anatinus. Absent. Here the cutaneus trunci runs to the EXTENSOR side of the antebrachium instead, terminating at the wrist in a subcutaneous aponeurosis that splits into four interdigital branches, each bifurcating to insert on opposing sides of the claws of adjacent digits.",
        "sources": [SRC],
    }),

    # ------------------------------------------------------------------
    # Intrinsic hand
    # ------------------------------------------------------------------
    ("flexores-breves-superficiales", ZAG, {
        "name": "Flexores breves superficiales",
        "present": "yes",
        "origin": "Four preaxial flexors for digits I-IV and sometimes up to three postaxial ones for digits II-IV. The first arises from the preaxial edge of the common tendon of the flexor digitorum profundus and the rest from its ventral side, the origin spreading proximally onto the fascia palmaris manus and even the fascia antebrachii.",
        "insertion": "The preaxial flexors pass preaxial to the corresponding digital tendon of the flexor digitorum profundus and insert through the metacarpophalangeal subarticular ligament on the preaxial base of phalanx 1; where a postaxial flexor is also present the two embrace the profundus tendon like the perforated tendon of the therian flexor digitorum superficialis.",
        "attachmentNote": "Zaglossus bruijnii. **These bellies are inside the hand**, not the forearm, and Gambaryan et al. count that among the primitive monotreme features while arguing the series is the therian flexor digitorum superficialis — on the strength of the embracing insertion, and of the same distal origin turning up in tupaias (Panyutina et al. 2015) and felids (Haines 1950). In other therians the muscle has migrated proximally onto the profundus aponeurosis or onto the entepicondylus itself.",
        "attachments": {
            "origin": [o("carpals", "ventral", "palmar-sesamoid")],
            "insertion": [o("phalanges-manus", "proximal")],
        },
        "partsOpen": True,
        "division": "variable",
        "parts": [p("Preaxial flexores breves superficiales I-IV"),
                  p("Postaxial flexores breves superficiales II-IV", membership=V,
                    note="Most often present in digit IV, more rarely in II and III.")],
        "divisionNote": "The set varies between specimens of this genus, which the authors tie to the reduction of the marginal fingers.",
        "sources": [SRC],
    }),
    ("flexores-breves-superficiales", TAC, {
        "name": "Flexor brevis superficialis I",
        "present": "yes",
        "origin": "The preaxial edge and adjacent dorsal side of the palmar sesamoid of the common tendon of the flexor digitorum profundus.",
        "insertion": "Preaxially at the end of the preungual phalanx of the thumb.",
        "attachmentNote": "Tachyglossus aculeatus. **One muscle, for digit I alone**, against four or more in the long-beaked echidna and four in the platypus — the most reduced condition of the three by a wide margin. Gambaryan et al. note it could alternatively be read as the lumbricalis I, and reject that on the general grounds that no tetrapod supplies the thumb from the lumbrical series.",
        "attachments": {
            "origin": [o("carpals", "ventral", "palmar-sesamoid")],
            "insertion": [o("phalanges-manus", "distal")],
        },
        "division": "single",
        "sources": [SRC],
    }),
    ("flexores-breves-superficiales", ORN, {
        "name": "Flexores breves superficiales",
        "present": "yes",
        "origin": "Four muscles for digits I-IV, from the ventral side of the common tendon of the flexor digitorum profundus at the proximal border of its sesamoids.",
        "insertion": "The terminal tendons thin into sheets which disappear distally into the loose elastic tissue enveloping each digit. In digit I the tendon is distinct as far as the metacarpophalangeal subarticular ligament; in digits II-IV the tendons reach the midlength of the first phalanges, where they embrace the corresponding profundus tendons as very thin perforated tendons.",
        "attachmentNote": "Ornithorhynchus anatinus. Gambaryan et al. correct Diogo & Abdala (2010) here: the tendons embrace the profundus tendons but are NOT fused with them, which matters because the embracing-not-fusing relation is what the flexor digitorum superficialis homology rests on.",
        "attachments": {
            "origin": [o("carpals", "ventral", "palmar-sesamoid")],
            "insertion": [o("phalanges-manus", "proximal")],
        },
        "division": "divided",
        "parts": [p("Flexor brevis superficialis I"), p("II"), p("III"), p("IV")],
        "sources": [SRC],
    }),

    ("lumbricales", ZAG, {
        "name": "Lumbricales",
        "present": "yes",
        "origin": "The dorsal (deep) side of the common tendon of the flexor digitorum profundus immediately proximal to its branching. Lumbricales IV and V are always present and III is rare.",
        "insertion": "Fleshy or tendinous, always on the end of the preungual phalanx at its preaxial side.",
        "attachmentNote": "Zaglossus bruijnii. Two muscles reliably, three at most, against four in the short-beaked echidna and three in the platypus.",
        "attachments": {
            "origin": [o("carpals", "dorsal", "palmar-sesamoid")],
            "insertion": [o("phalanges-manus", "distal")],
        },
        "sources": [SRC],
    }),
    ("lumbricales", TAC, {
        "name": "Lumbricales",
        "present": "yes",
        "origin": "Four muscles, lumbricales II-V, all from the dorsal side of the palmar sesamoid of the common tendon of the flexor digitorum profundus; lumbricalis II is not always present.",
        "insertion": "Preaxially at the end of the preungual phalanges of digits II-V. Lumbricales III and IV — and, per Fewkes (1877), V as well — bifurcate, each splitting off a preaxial head to the postaxial side of the preungual phalanx of the PRECEDING digit, so lumbricalis III supplies digits III and II, IV supplies IV and III, and V may supply V and IV.",
        "attachmentNote": "Tachyglossus aculeatus. **The bifurcation is a very rare morphological condition**, reported elsewhere only in colugos (Panyutina et al. 2015), which bifurcate lumbricales III-V. It gives this series postaxial supply to digits II-IV, which the lumbricals of other tetrapods do not have.",
        "attachments": {
            "origin": [o("carpals", "dorsal", "palmar-sesamoid")],
            "insertion": [o("phalanges-manus", "distal")],
        },
        "sources": [SRC],
    }),
    ("lumbricales", ORN, {
        "name": "Lumbricales",
        "present": "yes",
        "origin": "Three muscles, from the dorsal side of the common tendon of the flexor digitorum profundus at the distal border of its sesamoids: lumbricalis III from the medial sesamoid, IV from between the two, V from the lateral sesamoid.",
        "insertion": "Thin sheet-like tendons running to the preaxial side of digits III-V, crossing the first interphalangeal joint without firm attachment onto the dorsum of the digit and fusing into the preaxial edge of the corresponding extensor digitorum communis tendon. Lumbricalis V fuses with the interosseus V medialis at the preaxial side of the metacarpophalangeal V joint on the way.",
        "attachmentNote": "Ornithorhynchus anatinus. A flexor-side muscle ending on an extensor tendon — the row records the phalanges it runs to, but the actual termination is on another muscle's tendon, which no osteological correlate would recover.",
        "attachments": {
            "origin": [o("carpals", "dorsal", "palmar-sesamoid")],
            "insertion": [o("phalanges-manus", "proximal")],
        },
        "sources": [SRC],
    }),

    ("flexores-breves-profundi", ZAG, {
        "name": "Interossei",
        "present": "yes",
        "origin": "Interossei I-III from the prepollex; interossei IV and V from the pisiform and from the ligament connecting it to metacarpal IV.",
        "insertion": "Preaxially (mediales) or postaxially (laterales) on the metacarpophalangeal joints, though reduction of the marginal digits displaces the insertions of interossei I and V.",
        "attachmentNote": "Zaglossus bruijnii. = mm. flexores breves profundi sensu Diogo & Abdala (2010), which is this record. The set is variable: interossei I and II mediales and II and V laterales are the commonest, and all six others are possible. Special names apply at the margins — interosseus I medialis is the opponens pollicis, I lateralis the adductor pollicis, V lateralis the opponens digiti quinti.",
        "attachments": {
            "origin": [o("carpals", landmark="prepollex"),
                       o("carpals", landmark="pisiform")],
            "insertion": [o("phalanges-manus", "proximal"),
                          o("metacarpals", "distal")],
        },
        "division": "variable",
        "partsOpen": True,
        "parts": [p("Interossei mediales I-V", membership=V),
                  p("Interossei laterales I-V", membership=V)],
        "divisionNote": "Of the ten possible muscles the authors found no fixed set in this genus, which is the individual variation below the elbow the paper is careful to document rather than average away.",
        "sources": [SRC],
    }),
    ("flexores-breves-profundi", TAC, {
        "name": "Interossei",
        "present": "yes",
        "origin": "The muscles of digits I and II from the prepollex — three by a common tendon from its distal end, the interosseus II lateralis fleshy; those of digit III from the ligament between the prepollex and metacarpal III; the occasional interosseus IV medialis from the pisiform.",
        "insertion": "Preaxially or postaxially on the metacarpophalangeal joints of the digits they serve.",
        "attachmentNote": "Tachyglossus aculeatus. Five muscles always present — interosseus I medialis, both of digit II and both of digit III — with I lateralis and IV medialis optional and interosseus IV lateralis and both of digit V not found at all, against the complete set of ten Kajava (1911) assembled from his variants. Gambaryan et al.'s Kajava correspondence is worth keeping: his flexores breves profundi radialis and ulnaris are the mediales and laterales here.",
        "attachments": {
            "origin": [o("carpals", landmark="prepollex"),
                       o("carpals", landmark="pisiform")],
            "insertion": [o("phalanges-manus", "proximal"),
                          o("metacarpals", "distal")],
        },
        "division": "variable",
        "partsOpen": True,
        "parts": [p("Interossei mediales"), p("Interossei laterales", membership=V)],
        "sources": [SRC],
    }),
    ("flexores-breves-profundi", ORN, {
        "name": "Interossei",
        "present": "yes",
        "origin": "A complete set of ten, all by long tendons of which there are five: interossei I from the distal end of the prepollex; interossei II deeper from the same point and from intercarpal ligaments; interossei III from intercarpal ligaments; interossei IV and interosseus V medialis from intercarpal ligaments and the ulnare; interosseus V lateralis from the distal end of the pisiform.",
        "insertion": "Preaxially (mediales) or postaxially (laterales) on the metacarpophalangeal joints of every digit.",
        "attachmentNote": "Ornithorhynchus anatinus. **The full set of ten**, which Gambaryan et al. list among the features in which the platypus is more primitive than the echidnas, and one of which may even be the contrahens V. The tendon of the interosseus V medialis is shared with the interossei IV rather than with its own twin, which is an oddity of grouping rather than of position.",
        "attachments": {
            "origin": [o("carpals", landmark="prepollex"),
                       o("carpals", landmark="pisiform"),
                       o("carpals", landmark="ulnare")],
            "insertion": [o("phalanges-manus", "proximal"),
                          o("metacarpals", "distal")],
        },
        "division": "divided",
        "parts": [p("Interossei mediales I-V"), p("Interossei laterales I-V"),
                  p("Contrahens V", membership=D,
                    note="Gambaryan et al. suggest one of the ten may be the contrahens V, without deciding which.")],
        "sources": [SRC],
    }),

    ("intermetacarpales", ZAG, {
        "name": "Intermetacarpales",
        "present": "no",
        "note": "Zaglossus bruijnii. Absent in Tachyglossidae. Gambaryan et al. report this against Kajava (1911) and Howell (1936), who had it the other way round — present in echidnas and absent in the platypus.",
        "sources": [SRC],
    }),
    ("intermetacarpales", TAC, {
        "name": "Intermetacarpales",
        "present": "no",
        "note": "Tachyglossus aculeatus. Absent, against Kajava (1911) and Howell (1936). A sourced absence in one genus of a clade whose other genus has the muscle, which is what makes Monotremata compute as `variable` here rather than as present.",
        "sources": [SRC],
    }),
    ("intermetacarpales", ORN, {
        "name": "Intermetacarpales",
        "present": "yes",
        "origin": "Four muscles: the first from the postaxial side of metacarpal II, the second from the preaxial side of metacarpal III, the third from the postaxial side of metacarpal III, the fourth from the preaxial side of metacarpal IV — two in the space between metacarpals II and III, two between III and IV.",
        "insertion": "Each is unipennate, its fibres inserting on a tendon parallel to the metacarpal of origin which runs along the same digit to end at the tip of phalanx 1, on the same side as the origin. Digit II therefore carries a postaxial muscle, digit IV a preaxial one, and digit III both.",
        "attachmentNote": "Ornithorhynchus anatinus. = mm. interossei dorsales. Present here and absent in both echidnas, which Gambaryan et al. count among the ways the platypus is the more primitive monotreme below the elbow.",
        "attachments": {
            "origin": [o("metacarpals")],
            "insertion": [o("phalanges-manus", "proximal")],
        },
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

    created = 0
    if NEW_RECORD["id"] not in index:
        created = 1
        if write:
            rec = json.loads(json.dumps(NEW_RECORD))
            docs[FILE]["muscles"].append(rec)
            index[rec["id"]] = (FILE, rec)
        else:
            index[NEW_RECORD["id"]] = (FILE, json.loads(json.dumps(NEW_RECORD)))

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

    # The new record's `sources` is derived from the rows that landed on it.
    if NEW_RECORD["id"] in index:
        _, rec = index[NEW_RECORD["id"]]
        if rec.get("occurrences"):
            rec["sources"] = sorted({s for x in rec["occurrences"]
                                     for s in x.get("sources", [])})

    for line in missing:
        print(f"  MISS  {line}")
    print(f"\n{len(SEED)} distal rows from Gambaryan et al. (2015): {added} to add, "
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
