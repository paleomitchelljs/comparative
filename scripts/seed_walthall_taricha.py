#!/usr/bin/env python3
"""Integrate Walthall & Ashley-Ross (2006), postcranial myology of Taricha torosa.

Caudata is the reference taxon for the plesiomorphic tetrapod condition
throughout this dataset and was, before this source, among the thinnest columns
for attachment detail — 7 of 79 occurrences scored. This paper states an origin
and an insertion for every postcranial muscle it describes, so the salamander
column can be scored bone-by-bone instead of inheriting the consensus.

Three things this script does beyond adding rows:

* **Records a disagreement rather than resolving it.** Walthall & Ashley-Ross
  describe a discrete m. opercularis in Taricha. Abdala & Diogo (2010), following
  Hetherington & Tugaoen (1990), hold that the urodele structure is topologically
  part of the levator scapulae and not an independent muscle. The occurrence
  keeps `present: "no"` — one dissection does not overturn the homology argument —
  and the note now carries both positions.

* **Moves misfiled pedal data.** Three forelimb records carried attachment rows
  their own notes flagged as "recorded from the FOOT", parked there because no pes
  counterpart record existed. Creating those records lets the rows move to the
  limb they were observed in.

* **Marks the Caudata-only records as unsampled, not novel.** A record scored in
  one taxon optimises as a gain on that branch. Each new occurrence says in its
  note that the muscle is not yet scored elsewhere, so a salamander-only row reads
  as thin sampling rather than a salamander apomorphy.

The pubo-ischiac plate is scored as `pubis` and `ischium`; see
seed_walthall_skeleton.py for why.

    python3 scripts/seed_walthall_taricha.py           # report
    python3 scripts/seed_walthall_taricha.py --write   # apply
"""

import json
import pathlib
import sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "walthall-ashley-ross-2006"

UNSAMPLED = ("Described here from Taricha torosa; not yet scored in other taxa in "
             "this dataset, so its absence elsewhere is unsampled rather than "
             "observed.")


def o(element, side=None, landmark=None):
    row = {"element": element}
    if side:
        row["side"] = side
    if landmark:
        row["landmark"] = landmark
    return row


# ---------------------------------------------------------------------------
# 1. Consensus rows that name the wrong limb's phalanges. Copied across from the
#    forelimb counterpart when these records were created.
# ---------------------------------------------------------------------------
CONSENSUS_FIX = {
    "extensor-digitorum-longus-hl": ("insertion", "phalanges-manus", "phalanges-pes"),
    "flexor-digitorum-longus-hl": ("insertion", "phalanges-manus", "phalanges-pes"),
    "flexores-breves-superficiales-pes": ("insertion", "phalanges-manus", "phalanges-pes"),
    "contrahentes-digitorum-pes": ("insertion", "phalanges-manus", "phalanges-pes"),
    "flexores-breves-profundi-pes": ("insertion", "phalanges-manus", "phalanges-pes"),
}

# ---------------------------------------------------------------------------
# 2. Pedal observations parked on forelimb records. Their attachment rows are
#    declared in seed_occurrence_attachments.py, which has been repointed at the
#    pes records created below; this table strips the stale rows the forelimb
#    records still carry and guarantees the destination occurrence exists for the
#    seed to land on. Declared rather than derived, so re-running is a no-op.
# ---------------------------------------------------------------------------
STRIP = [
    ("flexores-breves-superficiales", "anura"),
    ("extensores-digitorum-breves", "crocodylia"),
    ("abductor-digiti-minimi", "anura"),
    ("contrahentium-caput-longum", "anura"),
]

PES_OCCURRENCES = {
    "extensores-digitorum-breves-pes": [
        {"species": "caiman-yacare", "name": "Extensor digitorum brevis superficialis + profundus",
         "present": "yes",
         "note": "Recorded by Pereyra et al. (2024) in the foot. Previously filed on the "
                 "manus record of the same name for want of a pes counterpart.",
         "sources": ["pereyra-etal-2024", "abdala-diogo-2010"]},
    ],
    "abductor-digiti-minimi-pes": [
        {"species": "triprion-petasatus", "name": "M. abductor digiti minimi", "present": "yes",
         "note": "Recorded by Blotto et al. (2020) in the foot, where it is a large muscle "
                 "lying lateral to the extensor digitorum longus. Previously filed on the "
                 "manus record of the same name; Blotto et al. describe a distinct abductor "
                 "digiti minimi in the hand, fused with the abductor secundus digiti V, "
                 "which is the muscle that record now carries.",
         "sources": ["blotto-etal-2020", "abdala-diogo-2010"]},
    ],
    "contrahentium-caput-longum-pes": [
        {"species": "triprion-petasatus", "name": "M. contrahentium caput longum", "present": "yes",
         "note": "Recorded by Blotto et al. (2020) in the foot. Previously filed on the "
                 "forelimb record of the same name.",
         "sources": ["blotto-etal-2020", "abdala-diogo-2010"]},
    ],
}

# ---------------------------------------------------------------------------
# 3. Caudata occurrences on existing records.
# ---------------------------------------------------------------------------
OCC = {
    # ---- body wall ----------------------------------------------------------
    "rectus-abdominis": {
        "name": "Rectus abdominis",
        "origin": "Anterior border of the pubo-ischiac plate and the ypsiloid cartilage.",
        "insertion": "Sternum and pericardium superficially; the deep portion runs on as the rectus cervicis profundus to the hyoid.",
        "action": "Prevents the trunk sagging between the girdles during walking, and draws the pelvic and pectoral girdles toward each other.",
        "attachments": {"origin": [o("pubis", "anterior"), o("ypsiloid-cartilage")],
                        "insertion": [o("sternum"), o("hyoid")]},
        "attachmentNote": "Divided into superficial and deep portions, the halves separated at the midline by the linea alba and segmented by tendinous inscriptions. The lateral fibres of the superficial portion attach to the pectoralis rather than to bone, which is why the pectoralis takes part of its own origin from those inscriptions.",
    },
    "obliquus-externus": {
        "name": "Obliquus externus",
        "origin": "Epaxial muscular fascia.",
        "insertion": "A midline aponeurosis crossing deep to the rectus abdominis.",
        "action": "Resists long-axis torsion generated by limb support during walking; bends the body during swimming.",
        "attachments": {"insertion": [o("linea-alba")]},
        "attachmentNote": "Fibres run dorsoanterior to ventroposterior at about 50 degrees to the body axis. Neither end reaches bone — both attachments are fascial, which is why the layer leaves no osteological correlate.",
        "note": "Fibre angle is measured, not estimated: roughly 50 degrees to the body axis against roughly 145 degrees for the internal oblique, so the two layers cross at close to a right angle.",
    },
    "transversus-abdominis": {
        "name": "Transversus abdominis",
        "origin": "Transverse processes of the trunk vertebrae.",
        "insertion": "Crosses the ventral midline to the corresponding attachment of the opposite side.",
        "action": "Resists long-axis torsion during walking, bends the body during swimming, and powers exhalation.",
        "attachments": {"origin": [o("thoracic-vertebrae", landmark="thoracic-transverse-processes")],
                        "insertion": [o("linea-alba")]},
        "attachmentNote": "The deepest of the three oblique layers, with dorsoventral fibres. The only one of them reaching the vertebral column.",
    },
    # ---- pectoral girdle ----------------------------------------------------
    "pectoralis": {
        "origin": "Midline aponeurosis, sternum, and the tendinous inscriptions of the rectus abdominis.",
        "insertion": "Crista ventralis of the humerus.",
        "attachments": {"origin": [o("sternum"), o("linea-alba")],
                        "insertion": [o("humerus", landmark="deltopectoral-crest")]},
        "attachmentNote": "The insertion resolves to the crista ventralis — the salamander name for the deltopectoral crest — rather than to the proximal humerus generally. A refinement in resolution, not a shift.",
    },
    "supracoracoideus": {
        "origin": "Ventral superficial surface of the coracoid cartilage.",
        "insertion": "Crista ventralis of the humerus, adjacent to the pectoralis insertion.",
        "attachments": {"origin": [o("coracoid", "ventral")],
                        "insertion": [o("humerus", landmark="deltopectoral-crest")]},
        "attachmentNote": "Fan-shaped and parallel-fibred, its posterior part lying deep to the pectoralis and inserting beside it on the same crest. In salamanders the supracoracoideus is still a ventral adductor; the dorsal, wing-elevating role it takes in birds requires the triosseal canal, which does not exist here.",
    },
    "deltoideus-clavicularis": {
        "origin": "Procoracoid cartilage.",
        "insertion": "Anterior surface of the proximal humerus.",
        "attachments": {"origin": [o("procoracoid")], "insertion": [o("humerus", "anterior")]},
        "attachmentNote": "The most anterior of the girdle-to-humerus muscles. Sigurdsen et al. (2012) take this single procoracoid slip as the plesiomorphic condition from which the subdivided anuran deltoid — and the enlarged, laterally deflected deltopectoral crest that goes with it — is derived.",
    },
    "deltoideus-scapularis": {
        "origin": "Dorsolateral surface of the suprascapular cartilage.",
        "insertion": "Crista ventralis of the humerus.",
        "attachments": {"origin": [o("suprascapula", "dorsal")],
                        "insertion": [o("humerus", landmark="deltopectoral-crest")]},
        "attachmentNote": "The fibres pass around the anterior side of the humerus to reach a ventral crest — a dorsal girdle muscle with a ventral insertion, which is what lets it elevate the humerus.",
    },
    "latissimus-dorsi": {
        "origin": "Dorsal fascia.",
        "insertion": "Posterior surface of the crista ventralis of the humerus, by a strong tendon.",
        "attachments": {"insertion": [o("humerus", "posterior", landmark="deltopectoral-crest")]},
        "attachmentNote": "The largest dorsal shoulder muscle, but its origin is entirely fascial — no bony attachment, so no correlate. The insertion is on the posterior face of the same crest that receives the pectoralis and supracoracoideus.",
    },
    "protractor-pectoralis": {
        "origin": "Dorsal fascia and the posterior surface of the skull.",
        "insertion": "Anterior head onto the lateral surfaces of the procoracoid and scapula; posterior head onto the anterolateral border of the scapula.",
        "attachments": {"origin": [o("neurocranium", "posterior")],
                        "insertion": [o("procoracoid", "lateral"), o("scapula", "lateral"),
                                      o("scapula", "anterior")]},
        "attachmentNote": "Two heads arising together and diverging posteriorly. The anterior head lands between the procoracohumeralis and the dorsalis scapulae, which is the topological fix on its identity.",
    },
    "opercularis": {
        "present": None,  # deliberately unchanged
        "note": "The structure called 'opercularis' in urodeles is topologically part of the levator scapulae, not an independent muscle (Hetherington & Tugaoen 1990). Walthall & Ashley-Ross (2006) disagree in practice, describing a discrete strap-like m. opercularis in Taricha running from the cartilaginous operculum of the otic capsule to the anterior edge of the suprascapula — and assigning it the opposite origin and insertion to the anuran record here. Presence is left at 'no' because a single dissection does not settle the homology argument, but the disagreement is the point: the same structure is a muscle or a part of one depending on which criterion is applied.",
    },
    # ---- arm ----------------------------------------------------------------
    "triceps-brachii": {
        "name": "Triceps brachii (anconaeus group)",
        "origin": "Four heads: coracoid (anconaeus coracoideus, by a long tendon); scapula posterior to the glenoid and the joint capsule (anconaeus scapularis medialis); proximal two-thirds of the lateral face of the humerus (anconaeus humeralis lateralis); the whole posterior face of the humerus (anconaeus humeralis medialis).",
        "insertion": "Olecranon process of the ulna.",
        "attachments": {"origin": [o("coracoid"), o("scapula", "posterior"), o("glenoid"),
                                   o("humerus", "lateral"), o("humerus", "posterior")],
                        "insertion": [o("ulna", landmark="olecranon")]},
        "attachmentNote": "Four separately named heads, two girdle and two humeral, converging on one olecranon insertion. The coracoid and scapular heads unite about midway along the humerus. This is the clearest case in the dataset of a muscle whose head count is a naming decision: Mivart (1869) and Davison (1895) called the whole complex 'triceps', Francis (1934) named all four.",
    },
    "brachialis": {
        "origin": "Anterior surface of the proximal humerus.",
        "insertion": "Proximal end of the radius.",
        "attachments": {"origin": [o("humerus", "anterior")], "insertion": [o("radius", "proximal")]},
        "attachmentNote": "Thick and parallel-fibred, crossing only the elbow. It has no girdle head, which is the difference from the amniote biceps brachii and the reason the two are not interchangeable.",
    },
    "coracobrachialis": {
        "origin": "Posterolateral surface of the coracoid.",
        "insertion": "Medial face of the distal end of the humerus.",
        "attachments": {"origin": [o("coracoid", "posterior")], "insertion": [o("humerus", "medial")]},
        "attachmentNote": "Its fibres run along the axis of the humerus to a distal insertion, so it retracts rather than adducts. Walthall & Ashley-Ross call it coracobrachialis longus; Abdala & Diogo record longus and superficialis as the same muscle.",
    },
    # ---- forearm ------------------------------------------------------------
    "extensor-antebrachii-carpi-radialis": {
        "origin": "Proximal part of the lateral epicondyle of the humerus.",
        "insertion": "Almost the whole anterolateral surface of the radius, and the lateral surface of the radiale.",
        "attachments": {"origin": [o("humerus", landmark="lateral-epicondyle")],
                        "insertion": [o("radius", "lateral"), o("radiale", "lateral")]},
        "attachmentNote": "Spans the elbow and the wrist. The salamander forearm muscles almost all cross more than one joint, which is why their actions cannot be read off a single joint.",
    },
    "extensor-antebrachii-carpi-ulnaris": {
        "origin": "Distal part of the lateral epicondyle of the humerus.",
        "insertion": "Posterolateral face of the ulna, and the ulnare and intermedium.",
        "attachments": {"origin": [o("humerus", landmark="lateral-epicondyle")],
                        "insertion": [o("ulna", "lateral"), o("ulnare"), o("intermedium-manus")]},
        "attachmentNote": "The postaxial mirror of the extensor antebrachii et carpi radialis, taking the distal part of the same epicondyle where that muscle takes the proximal part.",
    },
    "extensor-digitorum": {
        "origin": "Lateral epicondyle of the humerus.",
        "insertion": "Dorsal surfaces of the proximal phalanges of digits II, III and IV, by paired tendons.",
        "attachments": {"origin": [o("humerus", landmark="lateral-epicondyle")],
                        "insertion": [o("phalanges-manus", "dorsal")]},
        "attachmentNote": "The most superficial forearm muscle in dorsal view. It serves digits II-IV only — the salamander manus has four digits, digit V having been lost.",
    },
    "flexor-digitorum-longus": {
        "origin": "Medial epicondyle of the humerus.",
        "insertion": "Palmar aponeurosis, continuing as four tendons to the proximal end of the distal phalanx of each digit.",
        "attachments": {"origin": [o("humerus", landmark="medial-epicondyle")],
                        "insertion": [o("palmar-aponeurosis"), o("phalanges-manus", "ventral")]},
        "attachmentNote": "Walthall & Ashley-Ross use flexor digitorum communis; Francis (1934) called the same muscle flexor primordialis communis, the name used for its hindlimb counterpart here. The aponeurosis, not the bone, is the functional insertion — the tendons are its continuation.",
    },
    "flexor-carpi-radialis": {
        "origin": "Proximal portion of the medial epicondyle of the humerus.",
        "insertion": "Anterior face of the radius, with a slip crossing the wrist to the radiale.",
        "attachments": {"origin": [o("humerus", landmark="medial-epicondyle")],
                        "insertion": [o("radius", "anterior"), o("radiale")]},
        "attachmentNote": "Obscured along most of its length by the flexor digitorum communis. Preaxial member of the pair that divides the medial epicondyle between them.",
    },
    "flexor-carpi-ulnaris": {
        "origin": "Distal portion of the medial epicondyle of the humerus.",
        "insertion": "Much of the posterior edge of the ulna, with a slip to the lateral faces of the ulnare and intermedium.",
        "attachments": {"origin": [o("humerus", landmark="medial-epicondyle")],
                        "insertion": [o("ulna", "posterior"), o("ulnare", "lateral"),
                                      o("intermedium-manus", "lateral")]},
        "attachmentNote": "Described as the mirror image of the flexor antebrachii et carpi radialis. The four muscles taking the two epicondyles — two flexors medially, two extensors laterally, each pair split proximal and distal — are the clearest instance of the dorsal/ventral mirroring the paper reports for the antebrachium.",
    },
    "pronator-quadratus": {
        "origin": "Medial side of the ulna, the ulnare and the intermedium.",
        "insertion": "Radiale and the base of the first metacarpal.",
        "attachments": {"origin": [o("ulna", "medial"), o("ulnare"), o("intermedium-manus")],
                        "insertion": [o("radiale"), o("metacarpals", "proximal")]},
        "attachmentNote": "Recorded as m. pronator profundus. It crosses from the postaxial to the preaxial side of the wrist, which is what makes it a pronator rather than a flexor.",
    },
    "contrahentium-caput-longum": {
        "origin": "Internal surface of the ulna and the fascia connecting radius and ulna.",
        "insertion": "An extensive tendon connecting the carpal bones.",
        "attachments": {"origin": [o("ulna", "medial")], "insertion": [o("carpals")]},
        "attachmentNote": "Its insertion tendon is itself the origin of the contrahentes digitorum, so the two form a chain from the zeugopod to the phalanges.",
    },
    "flexor-accessorius-lateralis": {
        "origin": "Distal end of the ulna, the ulnare and the intermedium.",
        "insertion": "Dorsal surface of the palmar fascia.",
        "attachments": {"origin": [o("ulna", "distal"), o("ulnare"), o("intermedium-manus")],
                        "insertion": [o("palmar-aponeurosis", "dorsal")]},
        "attachmentNote": "Fibres run diagonally toward the radius and first digit. Inserting on the deep face of an aponeurosis is what lets it tension the palm rather than move a bone.",
    },
    "flexor-accessorius-medialis": {
        "origin": "Approximately the distal third of the ulna, the ulnare and the intermedium.",
        "insertion": "Dorsal side of the palmar fascia.",
        "attachments": {"origin": [o("ulna", "distal"), o("ulnare"), o("intermedium-manus")],
                        "insertion": [o("palmar-aponeurosis", "dorsal")]},
        "attachmentNote": "Distinguished from the lateral accessory only by a more extensive origin — the two are otherwise parallel-fibred straps with the same insertion.",
    },
    "flexores-breves-superficiales": {
        "origin": "Dorsal surface of the palmar fascia.",
        "insertion": "Lateral edges of the distal ends of the metacarpals.",
        "attachments": {"origin": [o("palmar-aponeurosis", "dorsal")],
                        "insertion": [o("metacarpals", "distal")]},
        "attachmentNote": "Slips lie on both sides of the metacarpals of digits II and III, but only on the medial side for digits I and IV — an asymmetry across the hand that tracks the axis of the manus.",
    },
    "intermetacarpales": {
        "origin": "Radial side of each metacarpal.",
        "insertion": "Ulnar side of the adjacent metacarpal.",
        "attachments": {"origin": [o("metacarpals")], "insertion": [o("metacarpals")]},
        "attachmentNote": "Roughly triangular, spanning metacarpal to metacarpal without reaching a phalanx.",
    },
    "extensores-digitorum-breves": {
        "origin": "Carpals at the bases of digits II, III and IV.",
        "insertion": "Dorsal surface of the proximal end of the terminal phalanx of each digit, by long tendons.",
        "attachments": {"origin": [o("carpals")], "insertion": [o("phalanges-manus", "dorsal")]},
        "attachmentNote": "Serves digits II-IV, matching the extensor digitorum communis and reflecting the four-digit salamander manus.",
    },
    "abductor-pollicis-longus": {
        "origin": "Radiale and intermedium.",
        "insertion": "Distal end of the first metacarpal.",
        "attachments": {"origin": [o("radiale"), o("intermedium-manus")],
                        "insertion": [o("metacarpals", "distal")]},
        "attachmentNote": "Recorded as m. abductor et extensor digiti I. Wholly intrinsic to the hand — it takes no origin in the forearm, unlike the amniote abductor pollicis longus, which is why the name transfers badly.",
    },
    "abductor-digiti-minimi": {
        "origin": "Ulnare and intermedium.",
        "insertion": "Lateral edge of the fourth metacarpal.",
        "attachments": {"origin": [o("ulnare"), o("intermedium-manus")],
                        "insertion": [o("metacarpals", "lateral")]},
        "attachmentNote": "Recorded as m. extensor lateralis digiti IV. It serves digit IV because digit V is absent from the salamander manus — the same postaxial position as the amniote abductor digiti minimi on digit V, one digit over. A case where matching by digit number and matching by position give different answers.",
    },
    "contrahentes-digitorum": {
        "origin": "The insertion tendon of the contrahentium caput longum, and the carpals.",
        "insertion": "Proximal end of the proximal phalanx of each digit.",
        "attachments": {"origin": [o("carpals")], "insertion": [o("phalanges-manus", "proximal")]},
        "attachmentNote": "Lies deep to the insertion tendons of the flexores breves superficiales. Part of its origin is tendinous rather than skeletal, on the contrahentium caput longum tendon.",
    },
    "flexores-breves-profundi": {
        "origin": "Carpals at the bases of their respective digits.",
        "insertion": "Chiefly the metacarpal, and also the proximal end of the proximal phalanx, of each digit.",
        "attachments": {"origin": [o("carpals")],
                        "insertion": [o("metacarpals"), o("phalanges-manus", "proximal")]},
        "attachmentNote": "The deepest of the short flexor layers.",
    },
    # ---- pelvis and thigh ---------------------------------------------------
    "puboischiofemoralis-internus": {
        "origin": "Internal (dorsal) face of the pubo-ischiac plate.",
        "insertion": "Extensively on the femur — the anterior face, extending dorsally and ventrally — anterior to the puboischiofemoralis externus.",
        "attachments": {"origin": [o("pubis", "dorsal"), o("ischium", "dorsal")],
                        "insertion": [o("femur", "anterior")]},
        "attachmentNote": "Passes anterior to the ilium to reach the hip. The pubo-ischiac plate is the fused ventral pelvic plate; it is scored here as pubis plus ischium, following the paper's own gloss of the ischium as the plate's posterior portion.",
    },
    "puboischiofemoralis-externus": {
        "origin": "Much of the ventral surface of the pubo-ischiac plate.",
        "insertion": "Ventral surface of the femur, over nearly two-thirds of the bone's length.",
        "attachments": {"origin": [o("pubis", "ventral"), o("ischium", "ventral")],
                        "insertion": [o("femur", "ventral")]},
        "attachmentNote": "An insertion covering two-thirds of the femoral shaft. Extensive fleshy attachments like this one are why femoral muscle scars in salamanders are poor guides to muscle boundaries.",
    },
    "caudofemoralis": {
        "origin": "Transverse processes of the fourth and fifth caudal vertebrae.",
        "insertion": "Crista ventralis of the femur, by a strong tendon.",
        "attachments": {"origin": [o("caudal-vertebrae", landmark="caudal-transverse-processes")],
                        "insertion": [o("femur", "ventral")]},
        "attachmentNote": "The origin has a countable segmental address — caudals four and five — which is rare in this dataset and is what makes the caudofemoralis tractable in fossils. The insertion is given as the femoral crista ventralis; whether that ridge is the same structure as the amniote fourth trochanter is not settled here, so no landmark is asserted.",
    },
    "extensor-iliotibialis": {
        "origin": "Lateral surface of the ilium above the acetabulum.",
        "insertion": "Spine of the tibia, by a long strong tendon.",
        "attachments": {"origin": [o("ilium", "lateral")], "insertion": [o("tibia", "anterior")]},
        "attachmentNote": "Crosses both hip and knee. Recorded with a single head in Taricha; the tibial insertion is on the anterior proximal tibia, which the paper calls the spine and which may or may not be the cnemial crest of amniotes — left unasserted.",
        "note": "Single-headed in Taricha, against the two heads (pars anterior and posterior) usual in Cryptobranchus, Necturus, Salamandra, Pseudoeurycea, Ambystoma and Dicamptodon. The split tracks limb robustness rather than habitat or phylogeny: slender-limbed salamanders (Amphiuma, Typhlomolge, Bolitoglossa, Taricha) have one head, robust-limbed ones two, and aquatic and terrestrial species occur in both groups. Smith (1927) reported two heads in the congener Taricha granulosa, so the character may vary within the genus.",
    },
    "iliofibularis": {
        "name": "Iliofibularis",
        "present": "yes",
        "origin": "External face of the ilium, just posterior to the extensor iliotibialis.",
        "insertion": "Posterior side of the proximal end of the fibula, by a tendon.",
        "action": "Elevates the femur and flexes the knee.",
        "attachments": {"origin": [o("ilium", "lateral")], "insertion": [o("fibula", "posterior")]},
        "attachmentNote": "Runs parallel to the extensor iliotibialis but slightly deeper and posterior, crossing both hip and knee. The insertion is the site the iliofibular tubercle marks in taxa that have one; no landmark is asserted here because the paper does not name a tubercle.",
    },
    "adductor-femoris": {
        "origin": "Anterior and ventral surface of the pubo-ischiac plate, anterior to the puboischiofemoralis externus.",
        "insertion": "Ventral face of the femur, anterior and distal to the puboischiofemoralis externus but posterior to the puboischiofemoralis internus.",
        "attachments": {"origin": [o("pubis", "ventral"), o("pubis", "anterior")],
                        "insertion": [o("femur", "ventral")]},
        "attachmentNote": "Recorded as m. pubifemoralis. The three ventral pelvis-to-femur muscles are separated by their sequence along the femur rather than by distinct attachment sites — internus anterior, pubifemoralis next, externus posterior.",
    },
    "ischiotrochantericus": {
        "origin": "Lateral border of the ischium — the posterior portion of the pubo-ischiac plate.",
        "insertion": "Posterior face of the head of the femur.",
        "attachments": {"origin": [o("ischium", "lateral")], "insertion": [o("femur", "posterior")]},
        "attachmentNote": "Recorded as m. ischiofemoralis, and the passage that fixes the plate's composition: the paper equates the ischium with the plate's posterior portion, which is what licenses scoring the plate as pubis plus ischium throughout.",
    },
    "puboischiotibialis": {
        "origin": "Pubo-ischiac plate, lateral to the midline.",
        "insertion": "Anterior surface of the tibia.",
        "attachments": {"origin": [o("pubis", "ventral"), o("ischium", "ventral")],
                        "insertion": [o("tibia", "anterior")]},
        "attachmentNote": "The most superficial muscle over the pelvis in ventral view, divided into proximal and distal sections by a tendinous inscription at about the level of the acetabulum. Francis (1934) and Mivart (1869) describe it as an undivided sheet in Salamandra and Cryptobranchus, so the inscription is not general to salamanders.",
    },
    "ischioflexorius": {
        "origin": "Posterior and lateral edge of the ischium, behind the puboischiotibialis.",
        "insertion": "Plantar aponeurosis overlying the flexor primordialis communis.",
        "attachments": {"origin": [o("ischium", "posterior"), o("ischium", "lateral")],
                        "insertion": [o("plantar-aponeurosis")]},
        "attachmentNote": "Runs from the pelvis to the sole without a bony insertion — the longest muscle chain in the hindlimb, and one whose action cannot be read from any single joint.",
        "note": "Only the distal section is fully separable from the puboischiotibialis in Taricha; the proximal section is incompletely divided from it and resists mechanical separation. Pseudoeurycea, Bolitoglossa, Paramesotriton and Onychodactylus share this. The character does not follow salamander phylogeny and must have arisen or been lost more than once.",
    },
    # ---- crus and foot ------------------------------------------------------
    "tibialis-anterior": {
        "origin": "Tibial (medial) epicondyle of the femur.",
        "insertion": "Extensively on the anterodorsal and anteroventral faces of the tibia.",
        "attachments": {"origin": [o("femur", landmark="femoral-epicondyle-medial")],
                        "insertion": [o("tibia", "dorsal"), o("tibia", "ventral"),
                                      o("tibia", "anterior")]},
        "attachmentNote": "Recorded as m. extensor cruris tibialis. Visible from both ventral and dorsal views as it fans from the femoral epicondyle across the anterior face of the tibia — three rows for one muscle on one bone, because it wraps.",
    },
    "extensor-digitorum-longus-hl": {
        "origin": "Lateral epicondyle of the femur, anterior to the extensor cruris et tarsi fibularis; sometimes a few fibres from the tibial spine.",
        "insertion": "Bases of the metatarsals, by many small tendons.",
        "attachments": {"origin": [o("femur", landmark="femoral-epicondyle-lateral")],
                        "insertion": [o("metatarsals", "proximal")]},
        "attachmentNote": "Thin, lying on the dorsal crus between the extensor tarsi tibialis and the extensor cruris et tarsi fibularis. Unlike its forelimb counterpart it stops at the metatarsals rather than reaching the phalanges.",
    },
    "flexor-digitorum-longus-hl": {
        "origin": "Chiefly the posteroventral face of the fibula, with part arising by tendon from the fibular epicondyle of the femur.",
        "insertion": "Plantar aponeurosis, which divides into five tendons to the proximal end of the terminal phalanx of each digit.",
        "attachments": {"origin": [o("fibula", "posterior"), o("fibula", "ventral"),
                                   o("femur", landmark="femoral-epicondyle-lateral")],
                        "insertion": [o("plantar-aponeurosis"), o("phalanges-pes", "ventral")]},
        "attachmentNote": "Recorded as m. flexor primordialis communis. Five tendons, against four in the hand — the pes retains digit V. Its function is given as pressing the sole against the ground rather than flexing the digits.",
    },
    "gastrocnemius": {
        "note": "Walthall & Ashley-Ross describe no discrete gastrocnemius in Taricha. The flexor primordialis communis occupies the position and takes the femoral epicondylar origin that the amniote gastrocnemius takes, and the paper treats it as one muscle. Recorded here without changing the presence state, since other sources score a gastrocnemius in Caudata; what this source shows is that the boundary between the two is a division that not every author makes.",
    },
    "flexores-breves-superficiales-pes": {
        "origin": "Dorsal side of the plantar fascia.",
        "insertion": "For digits II-V, the ventral side of the distal ends of the metatarsals and the ventral surface of the proximal end of the proximal phalanx; for digit I, the distal end of the metatarsal only.",
        "attachments": {"origin": [o("plantar-aponeurosis", "dorsal")],
                        "insertion": [o("metatarsals", "distal"), o("phalanges-pes", "proximal")]},
        "attachmentNote": "Tripartite for every digit except the first, which lacks the phalangeal connection. The manus counterpart differs: there the slips flank the metacarpals of digits II and III but not I and IV.",
    },
    "contrahentes-digitorum-pes": {
        "origin": "The flat tendon of the caput longum musculorum contrahentium, and the tarsal bones.",
        "insertion": "Proximal phalanx of each digit.",
        "attachments": {"origin": [o("tarsals"), o("distal-tarsals")],
                        "insertion": [o("phalanges-pes", "proximal")]},
        "attachmentNote": "Passes from the tarsals along the ventral axis of the metatarsals. As in the hand, part of the origin is on the caput longum tendon rather than on bone.",
    },
}

# ---------------------------------------------------------------------------
# 4. New records. Muscles the paper describes that the dataset had no row for.
# ---------------------------------------------------------------------------
def record(mid, name, region, file, subregion, segment, mass, layer, developmental,
           cons, att, occ, homology=None, synonyms=None):
    r = {"id": mid, "name": name, "region": region, "subregion": subregion,
         "segment": segment, "mass": mass, "developmental": developmental}
    if layer:
        r["layer"] = layer
    if synonyms:
        r["synonyms"] = synonyms
    r["consensus"] = cons
    r["attachments"] = att
    r["occurrences"] = occ
    if homology:
        r["homology"] = homology
    r["sources"] = sorted({s for x in occ for s in x.get("sources", [])})
    r["_file"] = file
    return r


def caudata(name, origin, insertion, note=None, att=None, attachmentNote=None, unsampled=True):
    occ = {"species": "taricha-torosa", "name": name, "present": "yes",
           "origin": origin, "insertion": insertion,
           "note": ((note + " " if note else "") + UNSAMPLED) if unsampled else note,
           "sources": [SRC]}
    if att:
        occ["attachments"] = att
    if attachmentNote:
        occ["attachmentNote"] = attachmentNote
    return {k: v for k, v in occ.items() if v is not None}


NEW = [
    record("obliquus-internus", "Obliquus internus", "axial", "axial",
           "lateral body wall", "axial", "somitic-axial", None,
           "Hypaxial; lateral plate of the body wall, deep to the external oblique.",
           {"origin": "Connective tissue deep to the obliquus externus.",
            "insertion": "A midline aponeurosis.",
            "action": "Resists long-axis torsion generated by limb support; bends the body during swimming.",
            "innervation": "Ventral rami of the spinal nerves."},
           {"insertion": [o("linea-alba")]},
           [caudata("Obliquus internus",
                    "Connective tissue deep to the obliquus externus.",
                    "An aponeurosis crossing the ventral midline.",
                    note="Fibres run ventroanterior to dorsoposterior at about 145 degrees to the body axis, close to perpendicular to those of the external oblique.",
                    att={"insertion": [o("linea-alba")]},
                    attachmentNote="Neither attachment is skeletal. The middle of the three oblique layers, thinner than the external oblique.")],
           homology={"confidence": "well-supported",
                     "related": ["obliquus-externus", "transversus-abdominis", "intercostales-interni"],
                     "notes": "The middle layer of the tetrapod body wall. The dataset previously carried the external oblique and the transversus but not the layer between them."}),
    record("ypsiloideus", "Ypsiloideus", "axial", "axial",
           "ventral body wall", "axial", "somitic-axial", "superficialis",
           "Hypaxial; posterior continuation of the superficial rectus abdominis.",
           {"origin": "Anterior edge of the medial pubis.",
            "insertion": "Arms of the ypsiloid cartilage.",
            "action": "Assists the rectus abdominis in preventing the trunk from sagging.",
            "innervation": "Ventral rami of the posterior trunk spinal nerves."},
           {"origin": [o("pubis", "anterior")], "insertion": [o("ypsiloid-cartilage")]},
           [caudata("Ypsiloideus",
                    "Anterior edge of the medial pubis.",
                    "Arms of the ypsiloid cartilage.",
                    note="Appears to be the posterior continuation of the part of the superficial rectus abdominis spanning ypsiloid cartilage and pelvic girdle, and is separated from it only formally.",
                    att={"origin": [o("pubis", "anterior")], "insertion": [o("ypsiloid-cartilage")]},
                    attachmentNote="Both attachments are on structures with no amniote counterpart — the ypsiloid cartilage is a salamander apomorphy, which is why this muscle has no homologue outside the group.")],
           homology={"confidence": "moderate",
                     "related": ["rectus-abdominis"],
                     "notes": "Tied to the ypsiloid cartilage and so restricted to salamanders. Whether it is a discrete muscle or a named part of the rectus abdominis is a matter of convention, as the paper concedes."}),
    record("pubotibialis", "Pubotibialis", "thigh", "hindlimb",
           "ventral thigh", "stylopod", "ventral", "superficialis",
           "Somitic; ventral (flexor) muscle mass of the hindlimb bud.",
           {"origin": "Anterior edge and anterior ventral face of the pelvis.",
            "insertion": "Anterior face of the proximal tibia.",
            "action": "Supports the body during walking and flexes the knee.",
            "innervation": "Ventral division of the lumbosacral plexus."},
           {"origin": [o("pubis", "anterior")], "insertion": [o("tibia", "anterior")]},
           [caudata("Pubotibialis",
                    "Anterior edge and anterior ventral face of the pubo-ischiac plate.",
                    "Anterior face of the proximal end of the tibia.",
                    att={"origin": [o("pubis", "anterior"), o("pubis", "ventral")],
                         "insertion": [o("tibia", "anterior", landmark=None)]},
                    attachmentNote="Its parallel fibres pass anterior to the puboischiotibialis to a proximal tibial insertion. Function attributed on the strength of Ashley-Ross (1995) electromyography in Dicamptodon, not inferred from geometry.")],
           homology={"confidence": "moderate",
                     "related": ["puboischiotibialis", "ischioflexorius", "ambiens"],
                     "notes": "A pelvis-to-tibia muscle anterior to the puboischiotibialis. Its relation to the amniote ambiens is not established here."}),
    record("femorofibularis", "Femorofibularis", "thigh", "hindlimb",
           "ventral thigh", "stylopod", "ventral", "profundus",
           "Somitic; ventral (flexor) muscle mass of the hindlimb bud.",
           {"origin": "Ventral face of the distal end of the femur.",
            "insertion": "Posterolateral face of the fibula.",
            "action": "Flexes the knee.",
            "innervation": "Ventral division of the lumbosacral plexus; branches of the same nerve serve the distal ischioflexorius."},
           {"origin": [o("femur", "ventral"), o("femur", "distal")],
            "insertion": [o("fibula", "posterior")]},
           [caudata("Femorofibularis",
                    "Ventral face of the distal end of the femur.",
                    "Posterolateral face of the fibula.",
                    note="Robust in Taricha, against the thin narrow muscle usual in salamanders. Ashley-Ross (1992) found a size trade-off with the ischioflexorius: Dicamptodon and newly metamorphosed Ambystoma have a large ischioflexorius and a slender femorofibularis, older Ambystoma the reverse, and Darevsky & Salomatina (1989) report the same trade-off in Paramesotriton. Francis (1934) noted that branches of one nerve supply the distal ischioflexorius and the femorofibularis, which is the basis for treating them as alternative solutions to one mechanical demand.",
                    att={"origin": [o("femur", "ventral"), o("femur", "distal")],
                         "insertion": [o("fibula", "posterior")]},
                    attachmentNote="A short femur-to-fibula strap crossing only the knee, against the ischioflexorius which runs from the pelvis to the sole. Two muscles of very different span substituting for one another in size is a caution against reading function from length.")],
           homology={"confidence": "moderate",
                     "related": ["ischioflexorius", "flexor-digitorum-longus-hl"],
                     "teaching": "A reciprocal size relationship between two muscles that share a nerve branch but not a span. The trade-off shows up across species and within one species across ontogeny.",
                     "notes": "No amniote counterpart is established. Shared innervation with the distal ischioflexorius is the strongest evidence bearing on its identity."}),
    record("caudalipuboischiotibialis", "Caudalipuboischiotibialis", "pelvic", "hindlimb",
           "tail to hindlimb", "girdle", "ventral", "superficialis",
           "Somitic; caudal hypaxial series recruited to the hindlimb.",
           {"origin": "Transverse process of the fourth caudal vertebra.",
            "insertion": "The tendinous inscription dividing the puboischiotibialis.",
            "action": "Assists the puboischiotibialis in limb retraction and flexes the tail laterally.",
            "innervation": "Ventral rami of the anterior caudal spinal nerves."},
           {"origin": [o("caudal-vertebrae", landmark="caudal-transverse-processes")],
            "insertion": []},
           [caudata("Caudalipuboischiotibialis",
                    "Transverse process of the fourth caudal vertebra.",
                    "The tendinous inscription dividing the proximal and distal portions of the puboischiotibialis — not bone.",
                    note="Coactive with the puboischiotibialis during walking (Ashley-Ross 1995).",
                    att={"origin": [o("caudal-vertebrae", landmark="caudal-transverse-processes")]},
                    attachmentNote="A muscle with a skeletal origin and no skeletal insertion: it ends on another muscle's tendinous inscription. Salamandra and Cryptobranchus lack that inscription altogether, so in those genera the insertion has nothing to attach to.")],
           homology={"confidence": "moderate",
                     "related": ["puboischiotibialis", "caudofemoralis", "ischiocaudalis"],
                     "notes": "One of three tail-to-pelvis muscles. Its insertion on a tendinous inscription rather than bone means it cannot be reconstructed from a skeleton."}),
    record("iliocaudalis", "Iliocaudalis", "pelvic", "hindlimb",
           "tail to pelvis", "girdle", "somitic-axial", None,
           "Somitic; caudal epaxial series reaching the pelvic girdle.",
           {"origin": "The first several caudal vertebrae.",
            "insertion": "Ilium.",
            "action": "Draws the tail laterally.",
            "innervation": "Dorsal rami of the anterior caudal spinal nerves."},
           {"origin": [o("caudal-vertebrae")], "insertion": [o("ilium")]},
           [caudata("Iliocaudalis",
                    "The first several caudal vertebrae.",
                    "Ilium.",
                    note="Its fibres run parallel to the epaxial muscles and it is distinguishable from them only by its insertion.",
                    att={"origin": [o("caudal-vertebrae")], "insertion": [o("ilium")]},
                    attachmentNote="A muscle identified by where it ends rather than by any visible boundary — the clearest case in this source of an attachment doing the work of delimiting a muscle.")],
           homology={"confidence": "moderate",
                     "related": ["ischiocaudalis", "caudal-musculature", "caudofemoralis"],
                     "teaching": "Where a muscle has no visible border with its neighbours, its insertion is the only thing that makes it a muscle at all."}),
    record("ischiocaudalis", "Ischiocaudalis", "pelvic", "hindlimb",
           "tail to pelvis", "girdle", "ventral", "superficialis",
           "Somitic; caudal hypaxial series reaching the pelvic girdle.",
           {"origin": "Transverse process of the fourth caudal vertebra.",
            "insertion": "Posterior border of the ischium.",
            "action": "Draws the tail laterally.",
            "innervation": "Ventral rami of the anterior caudal spinal nerves."},
           {"origin": [o("caudal-vertebrae", landmark="caudal-transverse-processes")],
            "insertion": [o("ischium", "posterior")]},
           [caudata("Ischiocaudalis",
                    "Transverse process of the fourth caudal vertebra.",
                    "Posterior border of the ischium.",
                    note="The most medial of the three ventral muscles connecting tail and pelvic girdle.",
                    att={"origin": [o("caudal-vertebrae", landmark="caudal-transverse-processes")],
                         "insertion": [o("ischium", "posterior")]},
                    attachmentNote="Flat, thin and strap-like. With the caudalipuboischiotibialis and caudofemoralis it forms a series of three, all from the anterior caudal transverse processes, differing in where they end.")],
           homology={"confidence": "moderate",
                     "related": ["iliocaudalis", "caudalipuboischiotibialis", "caudal-musculature"]}),
    record("extensor-tarsi-tibialis", "Extensor tarsi tibialis", "leg", "hindlimb",
           "dorsal crus", "zeugopod", "dorsal", None,
           "Somitic; dorsal (extensor) muscle mass of the hindlimb bud.",
           {"origin": "Tibial epicondyle of the femur.",
            "insertion": "Ventral surface of the tibiale.",
            "action": "Supinates the foot.",
            "innervation": "Dorsal division of the lumbosacral plexus."},
           {"origin": [o("femur", landmark="femoral-epicondyle-medial")],
            "insertion": [o("tibiale", "ventral")]},
           [caudata("Extensor tarsi tibialis",
                    "Tibial epicondyle of the femur, next to the extensor cruris tibialis.",
                    "Ventral surface of the tibiale.",
                    att={"origin": [o("femur", landmark="femoral-epicondyle-medial")],
                         "insertion": [o("tibiale", "ventral")]},
                    attachmentNote="Crosses knee and ankle to reach a proximal tarsal. Function presumed from geometry, not measured.")],
           homology={"confidence": "moderate",
                     "related": ["tibialis-anterior", "extensor-cruris-et-tarsi-fibularis"]}),
    record("extensor-cruris-et-tarsi-fibularis", "Extensor cruris et tarsi fibularis", "leg", "hindlimb",
           "dorsal crus", "zeugopod", "dorsal", None,
           "Somitic; dorsal (extensor) muscle mass of the hindlimb bud.",
           {"origin": "Fibular epicondyle of the femur.",
            "insertion": "Posterodorsal and posteroventral faces of the fibula, with a portion on the fibulare.",
            "action": "Extends the knee.",
            "innervation": "Dorsal division of the lumbosacral plexus."},
           {"origin": [o("femur", landmark="femoral-epicondyle-lateral")],
            "insertion": [o("fibula", "dorsal"), o("fibula", "ventral"), o("fibulare")]},
           [caudata("Extensor cruris et tarsi fibularis",
                    "Fibular epicondyle of the femur.",
                    "Much of the posterodorsal and posteroventral faces of the fibula, with a portion inserting on the fibulare.",
                    note="The postaxial complement of the extensor cruris tibialis: the two wrap the tibia and fibula respectively from the two femoral epicondyles.",
                    att={"origin": [o("femur", landmark="femoral-epicondyle-lateral")],
                         "insertion": [o("fibula", "dorsal"), o("fibula", "ventral"), o("fibulare")]},
                    attachmentNote="Three rows on two bones for one muscle, because it wraps the fibula from dorsal to ventral and continues onto the proximal tarsus.")],
           homology={"confidence": "moderate",
                     "related": ["tibialis-anterior", "extensor-tarsi-tibialis", "fibularis-group"]}),
    record("interosseus-cruris", "Interosseus cruris", "leg", "hindlimb",
           "between tibia and fibula", "zeugopod", "dorsal", "profundus",
           "Somitic; deep layer between the zeugopodial elements.",
           {"origin": "Proximal part of the fibula.",
            "insertion": "Distal portion of the tibia.",
            "action": "Stabilises the two long bones of the crus against one another.",
            "innervation": "Dorsal division of the lumbosacral plexus."},
           {"origin": [o("fibula", "proximal")], "insertion": [o("tibia", "distal")]},
           [caudata("Interosseus cruris",
                    "Proximal part of the fibula, on the medial side.",
                    "Distal portion of the tibia.",
                    att={"origin": [o("fibula", "proximal", landmark=None)],
                         "insertion": [o("tibia", "distal")]},
                    attachmentNote="Joins the medial sides of tibia and fibula. Its serial counterpart in the forelimb is the pronator profundus, which in salamanders runs the other way — from the ulna across to the radial side — and acts as a pronator rather than a strut.")],
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "pronator-quadratus", "basis": "topological"},
                     "related": ["pronator-quadratus"],
                     "notes": "Occupies the position of the amniote interosseous membrane as a muscle rather than a ligament."}),
    record("pronator-profundus-pes", "Pronator profundus (pes)", "foot", "hindlimb",
           "deep plantar layer", "autopod", "ventral", "profundus",
           "Somitic; deep ventral intrinsic layer of the pes.",
           {"origin": "Medial side of the fibula.",
            "insertion": "Lateral face of the distal tibia, the tibiale, and the base of the first metatarsal.",
            "action": "Pronates the foot.",
            "innervation": "Tibial nerve."},
           {"origin": [o("fibula", "medial")],
            "insertion": [o("tibia", "distal"), o("tibiale"), o("metatarsals", "proximal")]},
           [caudata("Pronator profundus",
                    "Medial side of the fibula.",
                    "Lateral face of the distal end of the tibia, the tibiale, and the base of the first metatarsal.",
                    att={"origin": [o("fibula", "medial")],
                         "insertion": [o("tibia", "distal"), o("tibiale"),
                                       o("metatarsals", "proximal")]},
                    attachmentNote="Roughly triangular, converging from the postaxial to the preaxial side of the ankle — the same crossing course as its counterpart in the hand.")],
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "pronator-quadratus", "basis": "topological"},
                     "related": ["interosseus-cruris", "flexor-accessorius-medialis-pes"],
                     "notes": "Walthall & Ashley-Ross give the same name to this muscle and to its counterpart in the hand, which is why the two are separate records here."}),
    record("contrahentium-caput-longum-pes", "Contrahentium caput longum (pes)",
           "foot", "hindlimb", "deep plantar layer", "autopod", "ventral", "profundus",
           "Somitic; deep ventral intrinsic layer of the pes.",
           {"origin": "Distal portion of the fibula.",
            "insertion": "A flat tendon attaching to the distal tarsal bones.",
            "action": "Flexes the tarsus.",
            "innervation": "Tibial nerve."},
           {"origin": [o("fibula", "distal")], "insertion": [o("distal-tarsals")]},
           [caudata("Caput longum musculorum contrahentium",
                    "Distal portion of the fibula, on the medial side.",
                    "A flat tendon attaching to the distal tarsal bones.",
                    att={"origin": [o("fibula", "distal", landmark=None)],
                         "insertion": [o("distal-tarsals")]},
                    attachmentNote="Thin, lying deep to the plantar fascia. Its insertion tendon is in turn the origin of the contrahentes digitorum, the same chained arrangement the hand shows.")],
           # the anuran occurrence arrives via RELOCATE
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "contrahentium-caput-longum", "basis": "topological"},
                     "related": ["contrahentes-digitorum-pes"],
                     "notes": "Separated from the forelimb record of the same name because Blotto et al. (2020) and Walthall & Ashley-Ross (2006) both describe hand and foot muscles under this one name."}),
    record("flexor-accessorius-lateralis-pes", "Flexor accessorius lateralis (pes)", "foot", "hindlimb",
           "deep plantar layer", "autopod", "ventral", "profundus",
           "Somitic; deep ventral intrinsic layer of the pes.",
           {"origin": "Lateral edge of the fibulare.",
            "insertion": "Dorsal side of the plantar fascia.",
            "action": "Pronates the foot.",
            "innervation": "Tibial nerve."},
           {"origin": [o("fibulare", "lateral")], "insertion": [o("plantar-aponeurosis", "dorsal")]},
           [caudata("Flexor accessorius lateralis",
                    "Lateral edge of the fibulare.",
                    "Dorsal side of the plantar fascia.",
                    att={"origin": [o("fibulare", "lateral")],
                         "insertion": [o("plantar-aponeurosis", "dorsal")]},
                    attachmentNote="Fibres run diagonally toward the anterior side of the foot. The forelimb counterpart takes the distal ulna as well as the carpals; this one is confined to the tarsus.")],
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "flexor-accessorius-lateralis", "basis": "topological"},
                     "related": ["flexor-accessorius-medialis-pes"]}),
    record("flexor-accessorius-medialis-pes", "Flexor accessorius medialis (pes)", "foot", "hindlimb",
           "deep plantar layer", "autopod", "ventral", "profundus",
           "Somitic; deep ventral intrinsic layer of the pes.",
           {"origin": "Distal fibula, the fibulare and the intermedium.",
            "insertion": "Plantar fascia.",
            "action": "Pronates the foot.",
            "innervation": "Tibial nerve."},
           {"origin": [o("fibula", "distal"), o("fibulare"), o("intermedium-pes")],
            "insertion": [o("plantar-aponeurosis")]},
           [caudata("Flexor accessorius medialis",
                    "Distal region of the fibula, the fibulare and the intermedium.",
                    "Plantar fascia.",
                    att={"origin": [o("fibula", "distal"), o("fibulare"), o("intermedium-pes")],
                         "insertion": [o("plantar-aponeurosis")]},
                    attachmentNote="Parallel to the lateral accessory and sharing its insertion, differing only in taking a more proximal origin that reaches the fibula.")],
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "flexor-accessorius-medialis", "basis": "topological"},
                     "related": ["flexor-accessorius-lateralis-pes"]}),
    record("intermetatarsales", "Intermetatarsales", "foot", "hindlimb",
           "between metatarsals", "autopod", "ventral", "intermediate",
           "Somitic; ventral intrinsic layer of the pes.",
           {"origin": "Metatarsal of one digit.",
            "insertion": "Metatarsal of the adjacent digit.",
            "action": "Adducts the metatarsals and the digits attached to them.",
            "innervation": "Lateral plantar nerve (tibial)."},
           {"origin": [o("metatarsals")], "insertion": [o("metatarsals")]},
           [caudata("Intermetatarsales",
                    "Metatarsals of adjacent digits.",
                    "Metatarsals of adjacent digits.",
                    note="These muscles form the web-like structures between the digits.",
                    att={"origin": [o("metatarsals")], "insertion": [o("metatarsals")]},
                    attachmentNote="Extend further distally on the fibular side of each metatarsal — an asymmetry the intermetacarpales of the hand do not show.")],
           homology={"confidence": "well-supported",
                     "serial": {"forelimb": "intermetacarpales", "basis": "topological"},
                     "related": ["flexores-breves-profundi-pes"]}),
    record("extensores-digitorum-breves-pes", "Extensores digitorum breves (pes)", "foot", "hindlimb",
           "dorsal intrinsic layer", "autopod", "dorsal", None,
           "Somitic; dorsal intrinsic layer of the pes.",
           {"origin": "Distal tarsals at the base of each digit.",
            "insertion": "Dorsal surface of the proximal end of the terminal phalanx, by long tendons.",
            "action": "Extends the digits.",
            "innervation": "Deep fibular nerve."},
           {"origin": [o("distal-tarsals")], "insertion": [o("phalanges-pes", "dorsal")]},
           [caudata("Extensores digitorum breves",
                    "Distal tarsal bones at the base of each digit.",
                    "Dorsal surface of the proximal end of the terminal phalanx of each digit, by a long tendon.",
                    note="Five slips, one per digit. The muscular part reaches only about two-thirds along the metatarsal; the tendon continues to the terminal phalanx.",
                    att={"origin": [o("distal-tarsals")], "insertion": [o("phalanges-pes", "dorsal")]},
                    attachmentNote="Five slips against three in the manus, which serves digits II-IV only. The difference is the salamander hand's missing digit V, not a difference in the muscle layer.")],
           homology={"confidence": "well-supported",
                     "serial": {"forelimb": "extensores-digitorum-breves", "basis": "topological"},
                     "related": ["extensor-digitorum-longus-hl"]}),
    record("abductor-et-extensor-digiti-i-pes", "Abductor et extensor digiti I (pes)", "foot", "hindlimb",
           "preaxial intrinsic layer", "autopod", "dorsal", None,
           "Somitic; dorsal intrinsic layer of the pes, preaxial margin.",
           {"origin": "Proximal tarsals of the preaxial ankle.",
            "insertion": "Lateral face of the first metatarsal and its phalanx.",
            "action": "Abducts and extends the first metatarsal and its digit.",
            "innervation": "Deep fibular nerve."},
           {"origin": [o("intermedium-pes"), o("centrale-pes")],
            "insertion": [o("metatarsals", "lateral"), o("phalanges-pes")]},
           [caudata("Abductor et extensor digiti I",
                    "Intermedium and centrale.",
                    "Lateral face of the first metatarsal, with a small slip to the phalanx.",
                    note="The paper's text calls these 'bones of the wrist' in the hindlimb section, evidently a slip for the ankle; the muscle is figured in the pes.",
                    att={"origin": [o("intermedium-pes"), o("centrale-pes")],
                         "insertion": [o("metatarsals", "lateral"), o("phalanges-pes")]},
                    attachmentNote="The preaxial counterpart of the abductor digiti minimi at the other margin of the foot. Its forelimb equivalent takes the radiale and intermedium.")],
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "abductor-pollicis-longus", "basis": "topological"},
                     "related": ["abductor-digiti-minimi-pes", "extensores-digitorum-breves-pes"]}),
    record("abductor-digiti-minimi-pes", "Abductor digiti minimi (pes)", "foot", "hindlimb",
           "postaxial intrinsic layer", "autopod", "ventral", None,
           "Somitic; intrinsic layer of the pes, postaxial margin.",
           {"origin": "Distal fibula and the fibulare.",
            "insertion": "Fibulare, the postaxial distal tarsal, and the base of the fifth metatarsal.",
            "action": "Abducts the fifth metatarsal and its digit.",
            "innervation": "Lateral plantar nerve (tibial)."},
           {"origin": [o("fibula", "distal"), o("fibulare")],
            "insertion": [o("distal-tarsals"), o("metatarsals", "proximal")]},
           [caudata("Abductor digiti V",
                    "Ventral surface of the distal end of the fibula.",
                    "Fleshy attachment to the posterior side of the fibulare, basale V, and the base of the fifth metatarsal.",
                    note="Basale V is scored as a distal tarsal; the paper's more specific term is kept here rather than given its own element.",
                    att={"origin": [o("fibula", "distal", landmark=None), o("fibula", "ventral")],
                         "insertion": [o("fibulare", "posterior"), o("distal-tarsals"),
                                       o("metatarsals", "proximal")]},
                    attachmentNote="An extensive fleshy insertion across three skeletal elements. The manus counterpart serves digit IV, because the salamander hand has lost digit V — the same muscle at the same margin, on a differently numbered digit.")],
           homology={"confidence": "moderate",
                     "serial": {"forelimb": "abductor-digiti-minimi", "basis": "topological"},
                     "related": ["abductor-et-extensor-digiti-i-pes", "flexores-breves-profundi-pes"],
                     "teaching": "Postaxial position and digit number disagree between hand and foot in salamanders. Matching by number would pair this muscle with nothing; matching by position pairs it with the manual extensor lateralis digiti IV."}),
]

# The placeholder None in the CLMC record's occurrence list is removed here.
for r in NEW:
    r["occurrences"] = [x for x in r["occurrences"] if x]

FILE_OF = {"axial": "data/muscles-axial.json", "hindlimb": "data/muscles-hindlimb.json"}


def main(write: bool) -> int:
    docs = {}
    for key, rel in FILE_OF.items():
        docs[rel] = json.loads((ROOT / rel).read_text())
    for rel in ("data/muscles-pectoral.json", "data/muscles-forearm-hand.json"):
        docs[rel] = json.loads((ROOT / rel).read_text())

    index = {}
    for rel, doc in docs.items():
        for m in doc["muscles"]:
            index[m["id"]] = (m, rel)

    log = []

    # 1. consensus limb fixes
    for mid, (side, wrong, right) in CONSENSUS_FIX.items():
        m = index.get(mid, (None,))[0]
        if not m:
            continue
        for row in m.get("attachments", {}).get(side, []):
            if row.get("element") == wrong:
                row["element"] = right
                log.append(f"fix   {mid}: consensus {side} {wrong} -> {right}")

    # 2. strip pedal attachment rows from the forelimb records they were parked on
    for src_mid, taxon in STRIP:
        m = index.get(src_mid, (None,))[0]
        if not m:
            continue
        for occ in m.get("occurrences", []):
            if speciesmap.clade_of(occ) != taxon or not occ.get("attachments"):
                continue
            occ.pop("attachments", None)
            occ.pop("attachmentNote", None)
            log.append(f"strip {src_mid}/{taxon} pedal attachment rows")

    pending = {k: [dict(x) for x in v] for k, v in PES_OCCURRENCES.items()}

    # 3. new records
    for r in NEW:
        rel = FILE_OF[r.pop("_file")]
        if r["id"] in index:
            log.append(f"skip  {r['id']} already exists")
            continue
        r["occurrences"].extend(pending.pop(r["id"], []))
        r["sources"] = sorted({s for x in r["occurrences"] for s in x.get("sources", [])})
        docs[rel]["muscles"].append(r)
        index[r["id"]] = (r, rel)
        log.append(f"new   {r['id']} ({rel.split('-')[-1][:-5]}, {len(r['occurrences'])} occurrences)")
    # Destinations that already existed keep their occurrence rows; add any that
    # are missing so seed_occurrence_attachments.py has somewhere to land.
    for mid, occs in pending.items():
        entry = index.get(mid)
        if not entry:
            log.append(f"WARN  no destination record {mid}")
            continue
        m = entry[0]
        have = {speciesmap.clade_of(x) for x in m.get("occurrences", [])}
        for occ in occs:
            if speciesmap.clade_of(occ) in have:
                continue
            m.setdefault("occurrences", []).append(occ)
            m["sources"] = sorted(set(m.get("sources", [])) | set(occ["sources"]))
            log.append(f"occ+  {mid}/{occ['species']} created (relocated from the forelimb record)")

    # 4. caudata occurrences on existing records
    for mid, patch in OCC.items():
        entry = index.get(mid)
        if not entry:
            log.append(f"WARN  {mid} not found")
            continue
        m = entry[0]
        occ = next((x for x in m.get("occurrences", []) if speciesmap.clade_of(x) == "caudata"), None)
        if occ is None:
            occ = {"species": "taricha-torosa", "present": patch.get("present") or "yes", "sources": []}
            m.setdefault("occurrences", []).append(occ)
            log.append(f"occ+  {mid}/caudata created")
        for k, v in patch.items():
            if k == "present":
                continue  # never rewritten by this script
            occ[k] = v
        occ.setdefault("sources", [])
        if SRC not in occ["sources"]:
            occ["sources"].append(SRC)
        if SRC not in m.get("sources", []):
            m.setdefault("sources", []).append(SRC)
            m["sources"] = sorted(set(m["sources"]))
        log.append(f"occ   {mid}/caudata "
                   f"{'+attachments' if patch.get('attachments') else '+note'}")

    for line in log:
        print(f"    {line}")
    print(f"\n{len(log)} changes")

    if not write:
        print("Dry run. Re-run with --write to apply.")
        return 0
    for rel, doc in docs.items():
        (ROOT / rel).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
