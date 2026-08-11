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
SEED: list[tuple[tuple[str, str], dict]] = [
    # ---------------- axial ----------------
    (("epaxial-musculature", "petromyzontida"), {
        "division": "single",
        "why": "Segmental myomeres, undivided into longitudinal tracts."}),
    (("epaxial-musculature", "lepidosauria"), {
        "division": "divided",
        "parts": [p("Transversospinalis", muscle="transversospinalis"),
                  p("Longissimus", muscle="longissimus-dorsi"),
                  p("Iliocostalis", muscle="iliocostalis")]}),
    (("epaxial-musculature", "crocodylia"), {
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
    (("hypaxial-musculature", "crocodylia"), {
        "division": "divided",
        "partsOpen": True,
        "parts": [p("Subvertebralis"), p("Abdominal wall series")]}),
    (("hypaxial-musculature", "theria"), {
        "division": "divided",
        "parts": [p("Quadratus lumborum"), p("Psoas minor"),
                  p("Obliquus externus", muscle="obliquus-externus"),
                  p("Obliquus internus"),
                  p("Transversus abdominis", muscle="transversus-abdominis"),
                  p("Rectus abdominis", muscle="rectus-abdominis"),
                  p("Intercostales", muscle="intercostales-externi")]}),

    (("caudal-musculature", "caudata"), {
        "division": "divided",
        "partsOpen": True,
        "parts": [p("Caudal epaxial series"), p("Caudal hypaxial series")]}),

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
    (("adductor-mandibulae", "lepidosauria"), {
        "division": "divided",
        "why": "Johnston (2014): the boundaries between the named parts differ "
                "substantially between authors.",
        "parts": [p("Adductor mandibulae externus",
                    muscle="adductor-mandibulae-externus"),
                  p("Pseudotemporalis", muscle="adductor-mandibulae-internus"),
                  p("Pterygomandibularis")]}),
    (("adductor-mandibulae", "theria"), {
        "division": "divided",
        "parts": [p("Masseter"), p("Temporalis"),
                  p("Pterygoideus medialis"), p("Pterygoideus lateralis")]}),

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
    (("adductor-mandibulae-externus", "theria"), {
        "division": "divided",
        "parts": [p("Masseter"), p("Temporalis")]}),

    (("adductor-mandibulae-internus", "anura"), {
        "division": "heads",
        "why": "Two parts merging into one another.",
        "parts": [p("Rostral part"), p("Caudal part")]}),
    (("adductor-mandibulae-internus", "testudines"), {
        "division": "divided",
        "parts": [p("Pseudotemporalis"), p("Pterygoideus")]}),
    (("adductor-mandibulae-internus", "lepidosauria"), {
        "division": "divided",
        "parts": [p("Pseudotemporalis"), p("Pterygoideus")]}),
    (("adductor-mandibulae-internus", "theria"), {
        "division": "divided",
        "parts": [p("Pterygoideus medialis"), p("Pterygoideus lateralis")]}),

    (("intermandibularis", "theria"), {
        "division": "divided",
        "why": "The middle-ear muscles are arch identity surviving radical "
                "functional relocation.",
        "parts": [p("Mylohyoid"), p("Digastricus, anterior belly"),
                  p("Tensor tympani"), p("Tensor veli palatini")]}),
    (("interhyoideus", "theria"), {
        "division": "divided",
        "partsOpen": True,
        "why": "The facial expression apparatus is a hyoid-arch sheet that "
                "migrated onto the face; universal CN VII innervation is why a "
                "facial nerve lesion paralyses one whole side.",
        "parts": [p("Muscles of facial expression"), p("Platysma"),
                  p("Stylohyoid"), p("Stapedius")]}),

    (("branchial-constrictors", "chondrichthyes"), {
        "division": "divided",
        "parts": [p("Constrictores arcuum branchialium"),
                  p("Levatores arcuum branchialium")]}),
    (("branchial-constrictors", "testudines"), {
        "division": "divided",
        "parts": [p("Levator laryngis"), p("Depressor laryngis"),
                  p("Constrictor laryngis"), p("Dilatator laryngis")]}),
    (("branchial-constrictors", "theria"), {
        "division": "divided",
        "partsOpen": True,
        "why": "The stylopharyngeus is the only mammalian muscle innervated by "
                "CN IX — the sole surviving arch 3 muscle.",
        "parts": [p("Pharyngeal constrictors"), p("Stylopharyngeus"),
                  p("Cricothyroid"), p("Intrinsic laryngeal muscles")]}),

    (("extraocular-muscles", "theria"), {
        "division": "divided",
        "parts": [p("Rectus superior"), p("Rectus inferior"),
                  p("Rectus medialis"), p("Rectus lateralis"),
                  p("Obliquus superior"), p("Obliquus inferior"),
                  p("Levator palpebrae superioris"),
                  p("Retractor bulbi", membership=V,
                    note="Retained in many mammals, lost in humans and other "
                         "primates.")]}),

    (("hypobranchial-muscles", "chondrichthyes"), {
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
    (("hypobranchial-muscles", "theria"), {
        "division": "divided",
        "partsOpen": True,
        "why": "The palatoglossus is the exception that confirms the rule: the "
                "only 'tongue' muscle on CN X, because it is a soft-palate "
                "(arch 4) muscle rather than a hypobranchial one.",
        "parts": [p("Genioglossus"), p("Hyoglossus"), p("Styloglossus"),
                  p("Intrinsic tongue muscles"), p("Geniohyoid"),
                  p("Infrahyoid strap muscles")]}),

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
        "division": "divided",
        "why": "Sullivan (1962, 1967) report both.",
        "parts": [p("Rhomboideus superficialis"), p("Rhomboideus profundus")]}),
    (("rhomboideus", "theria"), {
        "division": "divided",
        "parts": [p("Rhomboideus capitis"), p("Rhomboideus cervicis"),
                  p("Rhomboideus thoracis")]}),

    (("levator-scapulae", "monotremata"), {
        "division": "divided",
        "parts": [p("Levator scapulae"),
                  p("Levator scapulae ventralis / omotransversarius",
                    membership=D)]}),
    (("levator-scapulae", "theria"), {
        "division": "divided",
        "parts": [p("Levator scapulae"), p("Omotransversarius", membership=D)]}),

    (("pectoralis", "monotremata"), {
        "division": "divided",
        "parts": [p("Pectoralis superficialis"), p("Pectoralis profundus")]}),

    (("supracoracoideus", "monotremata"), {
        "division": "divided",
        "why": "The critical intermediate: the scapular spine is incipient and "
                "the field only partly divided.",
        "parts": [p("Supraspinatus"), p("Infraspinatus"),
                  p("Supracoracoideus remnant", membership=D)]}),
    (("supracoracoideus", "theria"), {
        "division": "divided",
        "parts": [p("Supraspinatus"), p("Infraspinatus")]}),

    (("deltoideus-clavicularis", "theria"), {
        "division": "heads",
        "parts": [p("Pars acromialis"), p("Pars clavicularis")]}),

    (("triceps-brachii", "aves"), {
        "division": "heads",
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
        "division": "divided",
        "parts": [p("Fibularis longus"), p("Fibularis brevis")]}),
    (("fibularis-group", "crocodylia"), {
        "division": "divided",
        "parts": [p("Fibularis longus"), p("Fibularis brevis")]}),
    (("fibularis-group", "aves"), {
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

    seen = {}
    for key, _ in SEED:
        if key in seen:
            sys.exit(f"seed error: duplicate entry for {key}")
        seen[key] = True

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
        occ = next((o for o in muscle.get("occurrences", []) if speciesmap.clade_of(o) == tid), None)
        if occ is None:
            missing.append(f"{mid}/{tid}: muscle has no occurrence for that taxon")
            continue
        if occ.get("present") == "no":
            missing.append(f"{mid}/{tid}: occurrence is present='no'")
            continue

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
