#!/usr/bin/env python3
"""Structure the taxon-specific subdivision of each homology group.

    python3 scripts/seed_division.py           # report
    python3 scripts/seed_division.py --write   # apply

Ninety-odd occurrence rows carried their subdivision inside the `name` string —
"Iliacus + psoas major (+ sartorius)", "Semitendinosus, semimembranosus, biceps
femoris". That is readable and unanalysable: it cannot answer how many muscles a
homology group comprises in a taxon, and so cannot say on which branches a field
differentiated. This moves that content into `division` + `parts` and leaves the
name alone.

Every row here was read off its own `name` and `note`; nothing is split by rule.
The distinctions the prose makes and a regex would not:

  * `heads` vs `divided` — the biceps has two heads and is one muscle; the
    puboischiofemoralis internus is three muscles in a mammal. Both are
    differentiation, they are not the same event, and the ordered scale
    single < heads < divided keeps them apart.
  * `membership` — a parenthesis usually marks a part whose place in the group
    is argued ("(+ sartorius)") or that only some species have ("(+ tertius in
    humans)"), not simply a further member.
  * `partsOpen` — "and relatives", "strap muscles", "series". The source is
    enumerating, not finishing, so the count is a floor.

EXCLUDED, with reasons, in EXCLUSIONS below. The fin records are excluded as a
class: their occurrence names list the tetrapod muscles each ancestral fin
muscle gave rise to, which is `derivatives`, already curated and already
reversed by the app. Recording it again as `parts` would give one fact two
homes and let them drift.
"""

import json
import pathlib
import sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent

E = "established"
D = "disputed"
V = "variable"

# `why` is the curator's justification for the call. It stays in this file and
# is never written to the dataset — almost every one of these rows already has
# an occurrence `note` saying the same thing, and copying it into a
# `divisionNote` puts the same paragraph on screen twice.
#
# `dataNote` is the exception: something the occurrence note does not already
# say, so it belongs in the data. There are four.


def p(name, membership=E, muscle=None, note=None):
    row = {"name": name}
    if membership != E:
        row["membership"] = membership
    if muscle:
        row["muscle"] = muscle
    if note:
        row["note"] = note
    return row


# (muscle id, taxon) -> division block.
# A list of pairs rather than a dict literal: a duplicate key in a dict is
# silently the last one written, which is how eight taxon blocks were lost from
# seed_occurrence_attachments.py without the script ever reporting a problem.
#
# A block is keyed on a CLADE and the data is keyed on a SPECIES, so a clade
# holding two dissected animals is ambiguous — and this script used to resolve
# that ambiguity by taking whichever row came first, which is the bug that ate
# the second loon in seed_occurrence_attachments.py. Ten blocks were landing that
# way. `species` names the animal a block describes, and the guard in main()
# refuses to apply an ambiguous block rather than guessing.
#
# What those ten had actually cost is less than it looks: eight of the second
# species already carried their own `division`, written by whichever later pass
# added them, so the stale block was landing on the first row and doing no damage.
# Two did not — both Gavia immer, and both were carrying the split inside the
# `name` string this file exists to empty. Both are now scored from McKitrick
# (1991) as blocks of their own. A clade may therefore hold more than one block,
# one per dissected animal, and the uniqueness check keys on
# (muscle, taxon, species) to allow it.
SEED: list[tuple[tuple[str, str], dict]] = [
    # ---------------- axial ----------------
    (("epaxial-musculature", "myxini"), {
        "division": "single",
        "why": "Segmental myomeres, undivided into longitudinal tracts."}),
    (("epaxial-musculature", "lepidosauria"), {
        "division": "divided",
        "parts": [p("Transversospinalis", muscle="transversospinalis"),
                  p("Longissimus", muscle="longissimus-dorsi"),
                  p("Iliocostalis", muscle="iliocostalis")]}),
    (("epaxial-musculature", "theria"), {
        "division": "divided",
        "parts": [p("Transversospinal system", muscle="transversospinalis"),
                  p("Longissimus", muscle="longissimus-dorsi"),
                  p("Iliocostalis", muscle="iliocostalis")]}),

    (("hypaxial-musculature", "caudata"), {
        "division": "divided",
        "parts": [p("Abdominal wall musculature"), p("Subvertebral musculature")]}),
    (("hypaxial-musculature", "lepidosauria"), {
        "division": "divided",
        "parts": [p("Subvertebralis"),
                  p("Obliquus externus", muscle="obliquus-externus"),
                  p("Obliquus internus"),
                  p("Transversus abdominis", muscle="transversus-abdominis"),
                  p("Rectus abdominis", muscle="rectus-abdominis"),
                  p("Intercostales", muscle="intercostales-externi")]}),


    (("transversospinalis", "theria"), {
        "division": "divided",
        "partsOpen": True,
        "why": "Schilling (2011) ties the subdivision to a mobile, rib-free "
                "lumbar region. The enumeration is open — 'and relatives'.",
        "parts": [p("Multifidus"), p("Semispinalis")]}),

    (("obliquus-externus", "lepidosauria"), {
        "division": "heads",
        "parts": [p("Obliquus externus superficialis"),
                  p("Obliquus externus profundus")]}),
    (("rectus-abdominis", "lepidosauria"), {
        "division": "heads",
        "why": "Cieri (2018) distinguishes a main ventral belly from a "
                "superficial rectus abdominis lateralis.",
        "parts": [p("Rectus abdominis ventralis"),
                  p("Rectus abdominis lateralis")]}),

    # ---------------- cranial ----------------
    (("adductor-mandibulae", "chondrichthyes"), {
        "species": "squalus-acanthias",
        "division": "single",
        "why": "Relatively undivided — the plesiomorphic gnathostome condition."}),
    (("adductor-mandibulae", "actinopterygii"), {
        "division": "variable",
        "why": "Jayaram et al. (1983) find the subdivision pattern differs "
                "between congeneric catfishes, so it varies below the clade "
                "level this dataset scores.",
        "parts": [p("A1", membership=V), p("A2", membership=V),
                  p("A3", membership=V), p("Aω", membership=V)]}),
    (("adductor-mandibulae", "anura"), {
        "species": "ascaphus-truei",
        "division": "divided",
        "parts": [p("Levator mandibulae externus",
                    muscle="adductor-mandibulae-externus"),
                  p("Levator mandibulae longus",
                    muscle="adductor-mandibulae-longus"),
                  p("Levator mandibulae articularis")]}),
    (("adductor-mandibulae", "testudines"), {
        "division": "divided",
        "parts": [p("Adductor mandibulae externus pars superficialis",
                    muscle="adductor-mandibulae-externus"),
                  p("Adductor mandibulae externus pars media"),
                  p("Adductor mandibulae externus pars profunda"),
                  p("Pseudotemporalis", muscle="adductor-mandibulae-internus"),
                  p("Zygomaticomandibularis"),
                  p("Adductor mandibulae posterior",
                    muscle="adductor-mandibulae-posterior")]}),

    (("adductor-mandibulae-externus", "lepidosauria"), {
        "division": "heads",
        "why": "Layered lateral to medial in lizards, rostral to caudal in "
                "macrostomatan snakes; Johnston (2014) reconciles the two with "
                "a folded-sheet model.",
        "parts": [p("Adductor mandibulae externus superficialis"),
                  p("Adductor mandibulae externus medialis")]}),
    (("adductor-mandibulae-externus", "testudines"), {
        "division": "heads",
        "parts": [p("Pars superficialis"), p("Pars media"), p("Pars profunda")]}),

    (("adductor-mandibulae-internus", "anura"), {
        "species": "ascaphus-truei",
        "division": "heads",
        "why": "Two parts merging into one another.",
        "parts": [p("Rostral part"), p("Caudal part")]}),
    (("adductor-mandibulae-internus", "testudines"), {
        "division": "divided",
        "parts": [p("Pseudotemporalis"), p("Pterygoideus")]}),
    (("adductor-mandibulae-internus", "lepidosauria"), {
        "division": "divided",
        "parts": [p("Pseudotemporalis"), p("Pterygoideus")]}),


    (("branchial-constrictors", "chondrichthyes"), {
        "division": "divided",
        "parts": [p("Constrictores arcuum branchialium"),
                  p("Levatores arcuum branchialium")]}),
    (("branchial-constrictors", "testudines"), {
        "division": "divided",
        "parts": [p("Levator laryngis"), p("Depressor laryngis"),
                  p("Constrictor laryngis"), p("Dilatator laryngis")]}),


    (("hypobranchial-muscles", "chondrichthyes"), {
        "species": "squalus-acanthias",
        "division": "divided",
        "parts": [p("Coracomandibularis"), p("Coracohyoideus"),
                  p("Coracobranchialis")]}),
    (("hypobranchial-muscles", "caudata"), {
        "division": "divided",
        "parts": [p("Geniohyoideus"), p("Rectus cervicis")]}),
    (("hypobranchial-muscles", "testudines"), {
        "division": "divided",
        "parts": [p("Geniohyoideus"), p("Coracohyoideus"),
                  p("Genioglossus"), p("Hyoglossus")]}),

    (("levator-arcus-palatini", "chondrichthyes"), {
        "division": "divided",
        "why": "The spiracle is the reduced first (mandibular) gill slit.",
        "parts": [p("Levator palatoquadrati"), p("Spiracularis")]}),
    (("levator-arcus-palatini", "actinopterygii"), {
        "division": "divided",
        "parts": [p("Levator arcus palatini"), p("Dilatator operculi")]}),

    # ---------------- pectoral, arm, forearm, hand ----------------
    (("protractor-pectoralis", "theria"), {
        "division": "divided",
        "why": "Subdivisions of a single cucullaris field. Their retention of "
                "CN XI innervation, despite lying entirely within neck and "
                "trunk, is the classic evidence that innervation tracks "
                "developmental origin rather than topographic position.",
        "parts": [p("Trapezius"), p("Sternocleidomastoideus")]}),

    (("rhomboideus", "aves"), {
        "species": "gallus-domesticus",
        "division": "divided",
        "why": "Sullivan (1962, 1967) report both.",
        "parts": [p("Rhomboideus superficialis"), p("Rhomboideus profundus")]}),
    (("rhomboideus", "aves"), {
        "species": "gavia-immer",
        "division": "divided",
        "why": "McKitrick (1991) describes M. rhomboideus superficialis and M. "
                "rhomboideus profundus as separate muscles in Gavia immer, the "
                "profundus lying almost entirely deep to the superficialis. Added "
                "when pinning the Gallus block exposed that the loon row carried "
                "the split in its NAME — \"'Rhomboideus' (superficialis + "
                "profundus)\" — and nowhere countable.",
        "parts": [p("Rhomboideus superficialis"), p("Rhomboideus profundus")]}),
    (("rhomboideus", "theria"), {
        "division": "divided",
        "parts": [p("Rhomboideus capitis"), p("Rhomboideus cervicis"),
                  p("Rhomboideus thoracis")]}),

    # No monotremata blocks for levator-scapulae, pectoralis or supracoracoideus.
    # All three are now authored per species in seed_gambaryan_monotremata.py,
    # from the source rather than from the clade, and all three were WRONG here:
    # the levator scapulae has three portions and not two, the pectoralis is
    # explicitly undivided in monotremes rather than split into superficialis and
    # profundus, and the supracoracoideus block asserted the very split Gambaryan
    # et al. spend their remarks rejecting.
    (("levator-scapulae", "theria"), {
        "division": "divided",
        "parts": [p("Levator scapulae"), p("Omotransversarius", membership=D)]}),

    (("supracoracoideus", "theria"), {
        "division": "divided",
        "parts": [p("Supraspinatus"), p("Infraspinatus")]}),

    (("deltoideus-clavicularis", "theria"), {
        "division": "heads",
        "parts": [p("Pars acromialis"), p("Pars clavicularis")]}),

    (("triceps-brachii", "aves"), {
        "species": "gallus-domesticus",
        "division": "heads",
        "parts": [p("Scapulotriceps"), p("Humerotriceps")]}),
    (("triceps-brachii", "aves"), {
        "species": "gavia-immer",
        "division": "heads",
        "why": "McKitrick (1991) gives both in Gavia immer, each with its own "
                "tendon of insertion. Same case as the loon rhomboideus above: "
                "the name said it and nothing counted it.",
        "parts": [p("Scapulotriceps"), p("Humerotriceps")]}),
    (("triceps-brachii", "theria"), {
        "division": "heads",
        "parts": [p("Caput longum"), p("Caput laterale"), p("Caput mediale")]}),
    (("biceps-brachii", "theria"), {
        "division": "heads",
        "parts": [p("Caput longum"), p("Caput breve")]}),

    (("brachialis", "caudata"), {
        "division": "single",
        "why": "The brachialis field is not separated from the biceps field; "
                "the single muscle is the humeroantebrachialis."}),

    (("extensor-antebrachii-carpi-radialis", "theria"), {
        "division": "divided",
        "parts": [p("Extensor carpi radialis longus"),
                  p("Extensor carpi radialis brevis")]}),
    (("flexor-digitorum-longus", "theria"), {
        "species": "galictis-cuja",
        "division": "divided",
        "why": "Staggered phalangeal insertions in two layers — a derived "
                "elaboration of a single ancestral flexor plate.",
        "parts": [p("Flexor digitorum superficialis"),
                  p("Flexor digitorum profundus")]}),
    (("contrahentes-digitorum", "theria"), {
        "division": "divided",
        "why": "The adductor pollicis is generally regarded as a surviving "
                "contrahens; the rest of the layer is lost.",
        "parts": [p("Adductor pollicis"),
                  p("Palmar interossei", membership=D)]}),

    # ---------------- pelvis, thigh, leg, foot ----------------
    (("puboischiofemoralis-internus", "anura"), {
        "division": "divided",
        "why": "Prikryl et al. (2009) letter codes, used in place of the "
                "mammalian-sounding names earlier authors applied, because "
                "those imply homologies that do not hold. The placement of "
                "'pectineus' is unresolved — Noble (1922) put it here, others "
                "in the externus.",
        "parts": [p("Puboischiofemoralis internus A"),
                  p("Puboischiofemoralis internus B"),
                  p("Puboischiofemoralis internus C"),
                  p("Puboischiofemoralis internus D")]}),
    (("puboischiofemoralis-internus", "aves"), {
        "division": "divided",
        "parts": [p("Iliofemoralis internus"),
                  p("Iliotrochantericus cranialis")]}),
    (("puboischiofemoralis-internus", "theria"), {
        "division": "divided",
        "parts": [p("Iliacus"), p("Psoas major"),
                  p("Sartorius", membership=D,
                    note="Diogo & Molnar follow Walker & Homberger (1997) in "
                         "deriving it from the anterior head of this muscle, "
                         "against the common claim that it comes from the "
                         "reptilian 'ambiens'.")]}),

    (("puboischiofemoralis-externus", "aves"), {
        "division": "divided",
        "parts": [p("Obturatorius lateralis"), p("Obturatorius medialis")]}),
    (("puboischiofemoralis-externus", "theria"), {
        "division": "divided",
        "dataNote": "The gemelli are claimed by this field and by the "
                    "ischiotrochantericus; the dataset records both claims.",
        "parts": [p("Obturator externus"), p("Quadratus femoris"),
                  p("Gemelli", membership=D)]}),
    (("ischiotrochantericus", "theria"), {
        "division": "divided",
        "dataNote": "The gemelli are claimed by this field and by the "
                    "puboischiofemoralis externus; the dataset records both claims.",
        "parts": [p("Obturator internus"), p("Gemelli", membership=D)]}),

    (("iliofemoralis", "theria"), {
        "division": "divided",
        "parts": [p("Gluteus medius"), p("Gluteus minimus")]}),

    (("caudofemoralis", "lepidosauria"), {
        "division": "divided",
        "parts": [p("Caudofemoralis longus"), p("Caudofemoralis brevis")]}),
    (("caudofemoralis", "crocodylia"), {
        "division": "divided",
        "parts": [p("Caudofemoralis longus"), p("Caudofemoralis brevis")]}),
    (("caudofemoralis", "aves"), {
        "division": "heads",
        "why": "Allen et al. (2021) split the avian muscle into pars caudalis "
                "(= crocodylian longus) and pars pelvica (= brevis). Greatly "
                "reduced with the shortening of the tail to the pygostyle.",
        "parts": [p("Pars caudalis"), p("Pars pelvica")]}),

    (("extensor-iliotibialis", "caudata"), {
        "division": "variable",
        "why": "Single-headed in Taricha, two heads usual in Cryptobranchus, "
                "Necturus, Salamandra, Pseudoeurycea, Ambystoma and "
                "Dicamptodon. The split tracks limb robustness rather than "
                "habitat or phylogeny, and Smith (1927) reported two heads in "
                "the congener Taricha granulosa.",
        "parts": [p("Pars anterior", membership=V),
                  p("Pars posterior", membership=V)]}),
    (("extensor-iliotibialis", "anura"), {
        "division": "divided",
        "parts": [p("Extensor iliotibialis A"), p("Extensor iliotibialis B")]}),
    (("extensor-iliotibialis", "lepidosauria"), {
        "species": "eublepharis-macularius",
        "division": "divided",
        "parts": [p("Iliotibialis"),
                  p("Femorotibialis", membership=D, muscle="femorotibialis"),
                  p("'Ambiens'", membership=D, muscle="ambiens")]}),
    (("extensor-iliotibialis", "aves"), {
        "division": "divided",
        "parts": [p("Iliotibialis cranialis"), p("Iliotibialis lateralis")]}),
    (("extensor-iliotibialis", "theria"), {
        "division": "divided",
        "parts": [p("Rectus femoris"), p("Tensor fasciae latae")]}),

    (("femorotibialis", "aves"), {
        "division": "divided",
        "parts": [p("Femorotibialis lateralis"), p("Femorotibialis medialis")]}),
    (("femorotibialis", "theria"), {
        "division": "divided",
        "parts": [p("Vastus lateralis"), p("Vastus medialis"),
                  p("Vastus intermedius")]}),

    (("adductor-femoris", "aves"), {
        "division": "divided",
        "parts": [p("Puboischiofemoralis medialis"),
                  p("Puboischiofemoralis lateralis")]}),
    (("adductor-femoris", "theria"), {
        "division": "divided",
        "parts": [p("Adductor magnus"), p("Adductor longus"),
                  p("Adductor brevis")]}),

    (("puboischiotibialis", "caudata"), {
        "division": "variable",
        "dataNote": "Divided into proximal and distal sections by a tendinous "
                "inscription at about the level of the acetabulum in Taricha. "
                "Francis (1934) and Mivart (1869) describe it as an undivided "
                "sheet in Salamandra and Cryptobranchus, so the inscription is "
                "not general to salamanders.",
        "parts": [p("Proximal section", membership=V),
                  p("Distal section", membership=V)]}),
    (("puboischiotibialis", "anura"), {
        "division": "heads",
        "why": "Two heads in anurans against one in mammals. Both derive from "
                "the puboischiotibialis but via different heads, so the anuran "
                "and mammalian 'gracilis' are not straightforwardly equivalent.",
        "parts": [p("Gracilis major"), p("Gracilis minor")]}),
    (("puboischiotibialis", "theria"), {
        "division": "single",
        "dataNote": "One head, against two in anurans (Prikryl et al. 2009)."}),

    (("ischioflexorius", "lepidosauria"), {
        "species": "eublepharis-macularius",
        "division": "divided",
        "parts": [p("Flexor tibialis externus"), p("Flexor tibialis internus")]}),
    (("ischioflexorius", "crocodylia"), {
        "division": "divided",
        "parts": [p("Flexor tibialis externus"), p("Flexor tibialis internus")]}),
    (("ischioflexorius", "aves"), {
        "division": "divided",
        "why": "Crocodylian flexor tibialis internus 1 is lost between "
                "Avialae and Aves — one of the few outright losses in Allen et "
                "al.'s table.",
        "parts": [p("Flexor cruris medialis"),
                  p("Flexor cruris lateralis pars pelvica")]}),
    (("ischioflexorius", "theria"), {
        "division": "divided",
        "parts": [p("Semitendinosus"), p("Semimembranosus"),
                  p("Biceps femoris")]}),

    (("fibularis-group", "lepidosauria"), {
        "species": "eublepharis-macularius",
        "division": "divided",
        "parts": [p("Fibularis longus"), p("Fibularis brevis")]}),
    (("fibularis-group", "crocodylia"), {
        "species": "caiman-yacare",
        "division": "divided",
        "parts": [p("Fibularis longus"), p("Fibularis brevis")]}),
    (("fibularis-group", "aves"), {
        "species": "struthio-camelus",
        "division": "divided",
        "parts": [p("Fibularis longus"), p("Fibularis brevis")]}),
    (("fibularis-group", "theria"), {
        "division": "variable",
        "parts": [p("Fibularis longus"), p("Fibularis brevis"),
                  p("Fibularis tertius", membership=V, note="Humans."),
                  p("Fibularis digiti quinti", membership=V, note="Rats.")]}),

    (("contrahentes-digitorum-pes", "crocodylia"), {
        "division": "divided",
        "why": "Running between successive metatarsals.",
        "parts": [p("Interdigiti dorsales"), p("Interdigiti ventrales")]}),
]

# Rows that look like subdivisions and are not, or that belong somewhere else.
EXCLUSIONS = {
    ("epaxial-musculature", "crocodylia"):
        "no row to divide — the crocodylia occurrence was lifted out of the base\n        layer, because schilling-2011 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("hypaxial-musculature", "crocodylia"):
        "no row to divide — the crocodylia occurrence was lifted out of the base\n        layer, because schilling-2011 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("hypaxial-musculature", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because schilling-2011 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("caudal-musculature", "caudata"):
        "no row to divide — the caudata occurrence was lifted out of the base\n        layer, because schilling-2011 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("adductor-mandibulae", "lepidosauria"):
        "no row to divide — the lepidosauria occurrence was lifted out of the base\n        layer, because werneburg-2011 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("adductor-mandibulae", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("adductor-mandibulae-externus", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("adductor-mandibulae-internus", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("intermandibularis", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("interhyoideus", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("branchial-constrictors", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("extraocular-muscles", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because fritzsch-2023 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("hypobranchial-muscles", "theria"):
        "no row to divide — the theria occurrence was lifted out of the base\n        layer, because ziermann-diogo-2019 examines no animal of that clade. The names it\n        enumerated are in the record's `synonyms`, which is what the search\n        index reads",
    ("abductor-superficialis", "caudata"):
        "fin record — the listed muscles are `derivatives`, not parts",
    ("abductor-profundus", "actinistia"):
        "fin record — `derivatives`",
    ("abductor-profundus", "caudata"):
        "fin record — `derivatives`",
    ("adductor-superficialis", "caudata"):
        "fin record — `derivatives`",
    ("adductor-profundus", "actinistia"):
        "fin record — `derivatives`",
    ("adductor-profundus", "caudata"):
        "fin record — `derivatives`",
    ("pterygialis-cranialis", "caudata"):
        "fin record — `derivatives`",
    ("pterygialis-caudalis", "caudata"):
        "fin record — `derivatives`",
    ("retractor-lateralis-ventralis-pectoralis", "caudata"):
        "fin record — `derivatives`",
    ("deltoideus-scapularis", "theria"):
        "'Deltoideus, pars scapularis (spinous part)' is one pars named with a "
        "gloss, not a division of this record",
    ("protractor-pectoralis", "crocodylia"):
        "'(episternocleidomastoideus, partim)' says the crocodylian muscle "
        "corresponds in part, which is a homology hedge, not a subdivision",
    ("caudal-musculature", "lepidosauria"):
        "'ilio-, ischio- and caudofemoralis series' does not expand "
        "unambiguously — iliocaudalis/ischiocaudalis and iliofemoralis/"
        "ischiofemoralis are both readings. Needs the source, not a guess",
    ("extraocular-muscles", "testudines"):
        "the name enumerates eleven units, Werneburg (2011) is quoted in the "
        "note as recording ten. Needs the source to reconcile before the count "
        "is asserted",
}


def main():
    write = "--write" in sys.argv
    files = sorted(ROOT.glob("data/muscles-*.json"))

    # Uniqueness is per (muscle, taxon, species): one clade legitimately holds
    # two blocks when it holds two dissected animals, and the `species` key is
    # what tells them apart. Without the species in the check, adding the loon
    # beside the chicken would read as a duplicate.
    seen = set()
    for key, block in SEED:
        ident = (*key, block.get("species"))
        if ident in seen:
            sys.exit(f"seed error: duplicate entry for {ident}")
        if block.get("species") is None and any(
                k == key and b.get("species") for k, b in SEED):
            sys.exit(f"seed error: {key} has both a pinned and an unpinned block")
        seen.add(ident)

    docs = {path: json.loads(path.read_text()) for path in files}
    index = {}
    for path, doc in docs.items():
        for m in doc["muscles"]:
            index[m["id"]] = (path, m)

    applied = unchanged = 0
    missing = []
    for (mid, tid), block in SEED:
        entry = index.get(mid)
        if not entry:
            missing.append(f"{mid}/{tid}: no such muscle record")
            continue
        path, muscle = entry
        candidates = [o for o in muscle.get("occurrences", [])
                      if speciesmap.clade_of(o) == tid]
        want = block.get("species")
        if want:
            candidates = [o for o in candidates if o.get("species") == want]
        if not candidates:
            missing.append(f"{mid}/{tid}: muscle has no occurrence for that taxon"
                           + (f", species '{want}'" if want else ""))
            continue
        alive = [o for o in candidates if o.get("present") != "no"]
        if not alive:
            missing.append(f"{mid}/{tid}: occurrence is present='no'")
            continue
        if len(alive) > 1:
            missing.append(
                f"{mid}/{tid}: {len(alive)} rows in that clade "
                f"({', '.join(o['species'] for o in alive)}) — add \"species\" "
                f"to this block to say which one it describes")
            continue
        occ = alive[0]

        current = {k: occ.get(k) for k in
                   ("division", "parts", "partsOpen", "divisionNote")}
        target = {"division": block["division"],
                  "parts": block.get("parts"),
                  "partsOpen": block.get("partsOpen"),
                  "divisionNote": block.get("dataNote")}
        if current == target:
            unchanged += 1
            continue

        if write:
            occ["division"] = block["division"]
            for field, value in (("parts", block.get("parts")),
                                 ("partsOpen", block.get("partsOpen")),
                                 ("divisionNote", block.get("dataNote"))):
                if value:
                    occ[field] = value
                else:
                    occ.pop(field, None)
        applied += 1

    for line in missing:
        print(f"  MISS  {line}")
    print(f"\n{len(SEED)} curated blocks: {applied} to apply, {unchanged} already current, "
          f"{len(missing)} unresolved")
    print(f"{len(EXCLUSIONS)} rows deliberately excluded — see EXCLUSIONS in this file")

    if write and applied:
        for path, doc in docs.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {len(docs)} files")
    elif not write:
        print("(dry run — pass --write to apply)")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
