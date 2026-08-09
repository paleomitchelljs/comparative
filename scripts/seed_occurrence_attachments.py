#!/usr/bin/env python3
"""Seed taxon-specific `attachments` on occurrence rows.

Muscle-level `attachments` is a consensus. It cannot express the thing that is
often the actual result — that a muscle's attachment MOVED. This adds structured
per-taxon attachments for cases the sources document explicitly, so the app can
diff them against the plesiomorphic condition and surface the shift.

Only documented shifts are seeded. Occurrences left alone inherit the consensus,
and the app marks them as inherited rather than observed. Every entry below
carries the source that supports it.

    python3 scripts/seed_occurrence_attachments.py           # report
    python3 scripts/seed_occurrence_attachments.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# muscle id -> taxon id -> {origin, insertion, sources, shiftNote}
SEED = {
    # --- Fish paired-fin attachments, Diogo et al. (2016) Supplementary Tables
    # S1-S4 (Neoceratodus pectoral/pelvic, Latimeria pectoral/pelvic). These take
    # the sarcopterygian fish columns from no attachment data at all to the
    # best-attested part of the fin record. `appendage` in each note says which
    # fin the attachment is recorded from, because the fin muscle records are
    # ancestral to both and Neoceratodus differs sharply between them.
    "adductor-superficialis": {
        "dipnoi": {"origin": ["cleithrum", "scapulocoracoid"], "insertion": ["fin-radials", "fin-rays"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "Pectoral fin: arises from the cleithrum and the scapulocoracoid dorsal to the articular process, inserting by aponeurosis onto the distal radials and the bases of the lepidotrichia. The sheet is divided by tendinous partitions that land on the joints between axial elements — Gadow's proximo-distal partitioning, visible in a living fish."},
        "actinistia": {"origin": ["cleithrum"], "insertion": ["fin-rays", "preaxial-radials"],
                       "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                       "shiftNote": "Pectoral fin: from the posteromedial cleithrum between anocleithrum and endoskeleton, by a broad tendon onto the bases of the lepidotrichia, with bundles joining pronators 2-3 onto the preaxial radials."},
    },
    "adductor-profundus": {
        "dipnoi": {"origin": ["scapulocoracoid"], "insertion": ["fin-axial-elements"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "Pectoral fin: from the scapulocoracoid dorsal to the articular process onto the dorsal face of the first axial element."},
        "actinistia": {"origin": ["cleithrum", "scapulocoracoid"], "insertion": ["fin-axial-elements"],
                       "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                       "shiftNote": "Pectoral fin: from the medial cleithrum and endoskeleton at the articular process, onto the deep face of the adductor superficialis. In Latimeria this deep layer has given rise to the pronator series along the axis."},
    },
    "abductor-superficialis": {
        "dipnoi": {"origin": ["clavicle", "cleithrum", "scapulocoracoid"], "insertion": ["fin-radials", "fin-rays"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "Pectoral fin: from the lateral faces of clavicle, cleithrum and scapulocoracoid ventral to the articular process. The ventral mirror of the adductor superficialis, and likewise partitioned by tendinous sheets at the axial joints."},
        "actinistia": {"origin": ["cleithrum", "extracleithrum", "clavicle"], "insertion": ["fin-rays", "preaxial-radials"],
                       "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                       "shiftNote": "Pectoral fin: from the medial faces of cleithrum, extracleithrum and clavicle ventral to the articular process, by broad aponeurosis onto the lepidotrichial bases."},
    },
    "abductor-profundus": {
        "dipnoi": {"origin": ["scapulocoracoid"], "insertion": ["fin-axial-elements"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "Pectoral fin: from the scapulocoracoid adjacent and ventral to the articular process, onto the postaxial border of the first axial element."},
        "actinistia": {"origin": ["scapulocoracoid"], "insertion": ["fin-axial-elements"],
                       "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                       "shiftNote": "Pectoral fin: from the medial endoskeleton ventral to the articular process, onto the deep face of the abductor superficialis. Source of the supinator series in Latimeria."},
    },
    "pterygialis-cranialis": {
        "dipnoi": {"origin": ["pubic-ramus"], "insertion": ["preaxial-radials"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "Recorded from the PELVIC fin — the dipnoan pectoral fin is secondarily simplified to five muscles and lacks it. From the caudolateral face of the pubic ramus to the distal end of the first preaxial radial."},
        "actinistia": {"origin": ["pelvic-lateral-process"], "insertion": ["fin-rays"],
                       "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                       "shiftNote": "Pelvic fin: from the ventral face of the lateral process of the pelvis, running along the preaxial border to the preaxial lepidotrichial bases. In the pectoral fin it arises instead from the abductor superficialis itself."},
    },
    "pterygialis-caudalis": {
        "dipnoi": {"origin": ["midline-raphe"], "insertion": ["fin-axial-elements"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "Recorded from the PELVIC fin. From a midline raphe shared with its contralateral partner to the distal medial edge of the first axial element."},
        "actinistia": {"origin": ["fin-axial-elements"], "insertion": ["fin-rays"],
                       "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                       "shiftNote": "Pectoral fin: from the postaxial borders of the first to third axial elements together with pronators and supinators 2-4, inserting on the postaxial border between the adductor and abductor superficialis aponeuroses — a postaxial muscle sitting between the dorsal and ventral sheets."},
    },
    "retractor-lateralis-ventralis-pectoralis": {
        "dipnoi": {"origin": ["ribs"], "insertion": ["cleithrum"],
                   "sources": ["diogo-etal-2016", "diogo-etal-2016-si"],
                   "shiftNote": "From a cranial rib to the medial face of the cleithrum — the only muscle connecting axial skeleton to pectoral girdle in the dipnoan, which is the basis for homologising it with the tetrapod serratus anterior and levator scapulae."},
    },
    # --- Turtle cranial attachments, from Werneburg (2011) Appendix 1 via
    # scripts/extract_werneburg_appendix.py. Each entry aggregates the several
    # numbered muscular units Werneburg resolves for that muscle, so the element
    # lists are the union across those units, not one belly's attachments.
    "adductor-mandibulae-externus": {
        "testudines": {"origin": ["parietal", "squamosal", "postorbital", "palatoquadrate-quadrate", "quadratojugal",
                                  "jugal", "prootic", "opisthotic", "supraoccipital"],
                       "insertion": ["coronar-aponeurosis", "surangular", "coronoid", "dentary", "angular"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "Aggregated across the seven units Werneburg resolves (pars superficialis, media, profunda and their subdivisions). The wide origin over the skull roof and braincase, and the redirection of the line of action over the otic process, are what the turtle trochlear arrangement buys."},
    },
    "adductor-mandibulae-posterior": {
        "testudines": {"origin": ["palatoquadrate-quadrate", "parietal", "postorbital", "prootic"],
                       "insertion": ["articular"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "One to two heads arising anteromedially on the quadrate, medial to the adductor mandibulae externus; inserts partly directly and partly by its own tendon. Insertion on the articular puts it at the centre of the inverted U formed by the other components (Johnston 2011)."},
    },
    "depressor-mandibulae": {
        "testudines": {"origin": ["squamosal", "palatoquadrate-quadrate", "quadratojugal", "opisthotic", "jugal"],
                       "insertion": ["articular", "angular"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "One to two heads from the caudal, lateral and dorsal squamosal, occasionally the quadrate or quadratojugal; inserts partly by tendon on the posterior and ventral articular and the retroarticular process. Werneburg lists 13 synonyms for this muscle alone."},
    },
    "intermandibularis": {
        "testudines": {"origin": ["dentary"], "insertion": ["midline-raphe"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "Werneburg resolves a pars principalis and a further unit; both run from the medial dentary to the midline."},
    },
    "interhyoideus": {
        "testudines": {"origin": ["squamosal", "supraoccipital", "hyoid"], "insertion": ["midline-raphe"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "The constrictor colli complex, six units in Werneburg's scheme. Its spread from the hyoid onto the posterior skull is the sheet that in mammals becomes the facial musculature."},
    },
    "extraocular-muscles": {
        "testudines": {"origin": ["optic-foramen", "interorbital-septum", "frontal", "basisphenoid"],
                       "insertion": ["eye-bulbus"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "Eight units around the optic foramen and the anterodorsal optic cavity, all inserting on the eyeball. Werneburg additionally records intraocular muscles (ciliaris, sphincter and dilatator pupillae, transversalis oculi) that most vertebrate accounts omit; turtles, like birds, have striated intraocular muscle."},
    },
    # --- Avian pectoral attachments, Matsuoka & Hasegawa (2007) on Cygnus cygnus.
    # Organised by bone in the original, and written for palaeontologists working
    # back from fossils, so the attachment descriptions are unusually precise.
    # --- Anuran hand and foot, Blotto et al. (2020). The autopod regions had
    # zero taxon-specific attachments before this; the monograph describes every
    # intrinsic muscle of Triprion petasatus with explicit origin and insertion.
    "contrahentes-digitorum": {
        "anura": {"origin": ["distal-carpals"], "insertion": ["phalanges-manus"],
                  "sources": ["blotto-etal-2020", "abdala-diogo-2010"],
                  "shiftNote": "The contrahens indicis arises by tendon from the mediodistal distal carpal 3-4-5 and inserts on the lateropalmar surface of the basal phalanx of digit II; the contrahens digiti V arises lateral to it. A separate contrahens serves the prepollex."},
    },
    "flexores-breves-profundi": {
        "anura": {"origin": ["distal-carpals"], "insertion": ["metacarpals", "prepollex"],
                  "sources": ["blotto-etal-2020"],
                  "shiftNote": "The medial flexor indicis brevis profundus arises by tendon from the medial distal carpal 3-4-5 and inserts fleshily on the mediopalmar metacarpal II and on the ligament connecting the prepollex."},
    },
    "lumbricales": {
        "anura": {"origin": ["distal-carpals", "flexor-tendons"], "insertion": ["metacarpals", "phalanges-manus"],
                  "sources": ["blotto-etal-2020"],
                  "shiftNote": "Blotto et al. separate lumbricales breves (from distal carpal 3-4-5, inserting at the metacarpophalangeal joint) from lumbricales longi (from the tendines superficiales, in medial and lateral slips) — a distinction the amniote literature does not make."},
    },
    "abductor-pollicis-brevis": {
        "anura": {"origin": ["distal-carpals"], "insertion": ["prepollex"],
                  "sources": ["blotto-etal-2020", "abdala-diogo-2010"],
                  "shiftNote": "In anurans the preaxial muscles serve the PREPOLLEX, not digit 1 — the adductor pollicis arises tendinously from distal carpal 3-4-5 and inserts on the palmar and distal prepollex. Digit 1 is absent, and the muscles that would serve it attach to the preaxial element instead."},
    },
    "abductor-digiti-minimi-pes": {
        "anura": {"origin": ["fibulare"], "insertion": ["metatarsals"],
                  "sources": ["blotto-etal-2020", "abdala-diogo-2010"],
                  "shiftNote": "A large muscle with fleshy origin over almost the whole dorsolateral fibulare, inserting by short tendon on the dorsal and proximal metatarsal V."},
    },
    "extensores-digitorum-breves": {
        "anura": {"origin": ["radiale", "carpals"], "insertion": ["phalanges-manus"],
                  "sources": ["blotto-etal-2020", "abdala-diogo-2010"],
                  "shiftNote": "The extensor indicis brevis superficialis arises continuously from the radiale and the short ligament joining radiale and ulnare, lateral to the extensor carpi radialis tendon that attaches to element Y."},
    },
    "contrahentium-caput-longum-pes": {
        "anura": {"origin": ["ligamentum-calcanei"], "insertion": ["tibiale"],
                  "sources": ["blotto-etal-2020", "abdala-diogo-2010"],
                  "shiftNote": "A single muscle from the medial ligamentum calcanei, inserting fleshily along the distal three-quarters of the ventral tibiale, independent of the tibialis posterior."},
    },
    # --- Varanid hindlimb, Dick & Clemente (2016) Table 1, compiled from Snyder,
    # Gans et al., Reilly and Anzai et al. The leg region had no taxon-specific
    # attachments at all before this.
    "adductor-femoris": {
        "lepidosauria": {"origin": ["puboischiadic-ligament"], "insertion": ["femur"],
                         "sources": ["dick-clemente-2016", "diogo-molnar-2014"],
                         "shiftNote": "From the puboischiadic ligament to the ventral femoral shaft; adducts and protracts the femur, active in both stance and swing."},
    },
    # --- Caiman yacare crural and pedal muscles, Pereyra et al. (2024).
    # Crocodylia had nothing in the leg or foot regions before this.
    "gastrocnemius": {
        "lepidosauria": {"origin": ["tibia"], "insertion": ["phalanges-pes"],
                         "sources": ["dick-clemente-2016", "diogo-molnar-2014"],
                         "shiftNote": "From the ventral proximal tibia and the distal ventral tibial crest, by a broad aponeurosis onto the proximolateral margins of the first three phalanges — not onto a calcaneum, unlike the mammalian condition."},
        "crocodylia": {"origin": ["femoral-epicondyle-lateral", "tibia"], "insertion": ["calcaneum"],
                       "sources": ["pereyra-etal-2024", "diogo-molnar-2014"],
                       "shiftNote": "Externus arises by a tendon shared with the caudofemoralis longus and from the posterolateral femoral epicondyle, which bears a scattered striated surface; internus from the proximoposterior tibia. Both insert on the calcaneum by a broad tendon."},
    },
    "tibialis-anterior": {
        "crocodylia": {"origin": ["tibia"], "insertion": ["metatarsals"],
                       "sources": ["pereyra-etal-2024", "diogo-molnar-2014"],
                       "shiftNote": "From the proximomedial tibia to the dorsolateral proximal metatarsals I-II; the metatarsal bases carry coarse rugosities marking the insertion."},
    },
    "fibularis-group": {
        "crocodylia": {"origin": ["fibula", "iliofibular-tubercle"], "insertion": ["metatarsals"],
                       "sources": ["pereyra-etal-2024", "diogo-molnar-2014"],
                       "shiftNote": "Fibularis longus arises on the fibular shaft distal to the iliofibular tubercle; brevis from the distal fibular shaft and the anterior tibial aponeurosis. Both insert on the anterior surface of metatarsal V."},
    },
    "extensor-digitorum-longus-hl": {
        "crocodylia": {"origin": ["femoral-extensor-fossa", "femoral-epicondyle-lateral"], "insertion": ["metatarsals"],
                       "sources": ["pereyra-etal-2024", "diogo-molnar-2014"],
                       "shiftNote": "From the lateral femoral extensor fossa and lateral condyle onto the proximodorsal metatarsals III-IV, which bear a smooth bump at the insertion. Note that this is a femoral origin, not a tibial one — relevant to the Hattori & Tsuihiji (2021) dispute over which anterior tibial muscle is which."},
    },
    "flexor-digitorum-longus-hl": {
        "lepidosauria": {"origin": ["femoral-epicondyle-lateral"], "insertion": ["phalanges-pes"],
                         "sources": ["dick-clemente-2016", "diogo-molnar-2014"],
                         "shiftNote": "From the lateral femoral epicondyle; distally a stout tendon serving digits I-IV. Ankle plantarflexor, active in stance."},
        "crocodylia": {"origin": ["femoral-epicondyle-lateral", "femur"], "insertion": ["ungual-phalanges"],
                       "sources": ["pereyra-etal-2024", "diogo-molnar-2014"],
                       "shiftNote": "From the ventral distal femur and lateral condyle, which carries parallel striae aligned with the femoral long axis, onto the proximoventral unguals I-III."},
    },
    "flexores-breves-superficiales-pes": {
        "anura": {"origin": ["aponeurosis-plantaris", "tarsals"], "insertion": ["phalanges-pes"],
                  "sources": ["blotto-etal-2020"],
                  "shiftNote": "Despite the plural name, a single muscular body in Triprion, on the lateroplantar tarsal surface and ventrally concealed by the aponeurosis plantaris."},
        "crocodylia": {"origin": ["calcaneum"], "insertion": ["phalanges-pes"],
                       "sources": ["pereyra-etal-2024"],
                       "shiftNote": "Flexor digitorum brevis superficialis, digits I-IV, from the ventral calcaneum with digit-specific variation. Layer 1 of the seven-layer pedal scheme Pereyra et al. set out."},
    },
    "flexores-breves-profundi-pes": {
        "anura": {"origin": ["metatarsals", "tarsals"], "insertion": ["phalanges-pes", "prehallux"],
                  "sources": ["blotto-etal-2020"]},
        "crocodylia": {"origin": ["metatarsals", "metatarsal-striae", "calcaneum"], "insertion": ["phalanges-pes"],
                       "sources": ["pereyra-etal-2024"],
                       "shiftNote": "Flexor digitorum brevis profundus, digits I-IV, from metatarsals I-III and V and the distal calcaneum. The metatarsal origins are marked by fine striae — the pedal correlates Pereyra et al. identify for the first time."},
    },
    "extensores-digitorum-breves-pes": {
        "crocodylia": {"origin": ["astragalus", "calcaneum"], "insertion": ["phalanges-pes"],
                       "sources": ["pereyra-etal-2024", "abdala-diogo-2010"],
                       "shiftNote": "Extensor digitorum brevis superficialis arises from the astragalar hollow and lateral calcaneum; the deep layer arises from the proximodorsal metatarsals, whose fine striations run parallel to the metatarsal long axis."},
    },
    "contrahentes-digitorum-pes": {
        "anura": {"origin": ["tarsals"], "insertion": ["phalanges-pes"],
                  "sources": ["blotto-etal-2020"],
                  "shiftNote": "Blotto et al. record a full contrahens series in the anuran foot, including one serving the prehallux."},
        "crocodylia": {"origin": ["metatarsals", "metatarsal-striae"], "insertion": ["metatarsals"],
                       "sources": ["pereyra-etal-2024"],
                       "shiftNote": "The interdigiti dorsales and ventrales of Pereyra et al., running between successive metatarsals; their origins are marked by longitudinally oriented fine striae on the proximolateral metatarsal surfaces."},
    },
    "supracoracoideus": {
        "caudata":      {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "testudines":   {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "crocodylia": {"origin": ["coracoid"], "insertion": ["deltopectoral-crest"], "sources": ["abdala-diogo-2010", "klinkhamer-etal-2017"],
                       "shiftNote": "Fleshy origin on the proximo-lateral coracoid, covering the entire humeral head; fleshy insertion on the ventro-lateral humerus at the deltopectoral crest. Broad and triangular, forming much of the shoulder (Klinkhamer et al. 2017)."},
        "aves": {"origin": ["sternal-keel"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                 "shiftNote": "Origin restricted to the sternal keel and the tendon rerouted dorsally through the foramen triosseum, so a ventrally placed muscle produces the upstroke."},
        "monotremata": {"origin": ["coracoid", "scapula"], "insertion": ["greater-tubercle"], "sources": ["gambaryan-etal-2015", "fahn-lai-etal-2020"],
                        "shiftNote": "The scapular spine is only incipient, so the supracoracoideus field is just beginning to divide into supraspinatus and infraspinatus. The readable intermediate."},
        "theria": {"origin": ["supraspinous-fossa", "infraspinous-fossa"], "insertion": ["greater-tubercle"], "sources": ["ercoli-etal-2014", "fahn-lai-etal-2020"],
                   "shiftNote": "Origin has migrated off the coracoid — which no longer exists as a separate bone — onto the lateral scapula, where the new scapular spine splits it into supraspinatus and infraspinatus."},
    },
    "subcoracoscapularis": {
        "testudines":   {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "crocodylia":   {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "aves":         {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["subscapular-fossa"], "insertion": ["lesser-tubercle"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "The coracoid head is gone with the coracoid itself; only the scapular head persists, which is why the mammalian muscle is 'subscapularis' rather than 'subcoraco-scapularis'."},
    },
    "pectoralis": {
        "caudata":    {"origin": ["sternum", "body-wall"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["sternum", "interclavicle", "ribs"], "insertion": ["deltopectoral-crest"], "sources": ["abdala-diogo-2010", "freitas-etal-2017"]},
        "aves": {"origin": ["sternal-keel", "furcula", "ribs"], "insertion": ["deltopectoral-crest"],
                 "sources": ["abdala-diogo-2010", "matsuoka-hasegawa-2007"],
                 "shiftNote": "In Cygnus the origin is in three overlapping layers — shallow clavicle, deep clavicle plus carina, and sternal plane plus rib cage — all fusing distally onto the crista pectoralis, the avian name for the deltopectoral crest. The rib attachment is indirect, onto the surface of underlying muscle. Both pectoralis muscles together are about 11% of body mass."},
        "monotremata": {"origin": ["sternum", "interclavicle", "clavicle"], "insertion": ["deltopectoral-crest"], "sources": ["gambaryan-etal-2015"],
                        "shiftNote": "More extensive origin than in therians because monotremes retain the interclavicle."},
        "theria": {"origin": ["sternum", "clavicle", "ribs"], "insertion": ["greater-tubercle"], "sources": ["ercoli-etal-2014"]},
    },
    "deltoideus-clavicularis": {
        "caudata":      {"origin": ["procoracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                         "shiftNote": "Called procoracohumeralis in amphibians purely because the origin sits on the procoracoid."},
        "anura":        {"origin": ["procoracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "testudines":   {"origin": ["clavicle"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["clavicle"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "crocodylia": {"origin": ["scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                       "shiftNote": "Crocodylians have no clavicle, so despite the name the origin sits on the scapula — which is why Fürbringer (1876) called this muscle the scapularis inferior."},
        "theria": {"origin": ["acromion", "clavicle"], "insertion": ["deltopectoral-crest"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "The muscle is renamed at every step for the bone that happens to carry its origin, though the muscle itself is continuous across Tetrapoda."},
    },
    "extensor-antebrachii-carpi-radialis": {
        "caudata": {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"],
                    "shiftNote": "Plesiomorphic tetrapod condition: insertion stops at the radius and proximal carpals."},
        "anura": {"origin": ["lateral-epicondyle"], "insertion": ["metacarpals"], "sources": ["abdala-diogo-2010"],
                  "shiftNote": "In Phyllomedusa and other grasping tree frogs the insertion has shifted distally onto the metacarpals — the same shift mammals made, independently."},
        "testudines":   {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"]},
        "crocodylia":   {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["supracondylar-ridge", "lateral-epicondyle"], "insertion": ["metacarpals"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "Distal migration onto the metacarpals, correlated with finer digital control — and convergent with the anuran condition."},
    },
    "latissimus-dorsi": {
        "caudata":    {"origin": ["body-wall"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "testudines": {"origin": ["ribs"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                       "shiftNote": "Origin transferred onto the internal surface of the carapace, which is built from the ribs."},
        "aves": {"origin": ["thoracic-neural-spines"], "insertion": ["scapula", "clavicle"],
                 "sources": ["abdala-diogo-2010", "matsuoka-hasegawa-2007"],
                 "shiftNote": "Pars cranialis is the most superficial back muscle, arising aponeurotically over the neural spines of three thoracic vertebrae rather than directly from bone, and inserting on the medial margins of the dorsal clavicle and the scapula."},
        "theria": {"origin": ["thoracolumbar-fascia", "thoracic-neural-spines", "ribs"], "insertion": ["humerus"], "sources": ["ercoli-etal-2014"]},
    },
    "sternocoracoideus": {
        "lepidosauria": {"origin": ["sternum"], "insertion": ["coracoid"], "sources": ["abdala-diogo-2010"]},
        "aves": {"origin": ["sternum", "ribs"], "insertion": ["coracoid"],
                 "sources": ["abdala-diogo-2010", "matsuoka-hasegawa-2007"],
                 "shiftNote": "The only muscle on the internal surface of the thoracic cavity. From the dorsal surface of the craniolateral sternum (processus craniolateralis) and the first rib, to a large depression on the dorsal surface of the coracoid base. Matsuoka & Hasegawa suggest it keeps the coracoid-sternum connection flexible."},
        "monotremata":  {"origin": ["sternum"], "insertion": ["coracoid"], "sources": ["gambaryan-etal-2015"]},
        "theria": {"origin": ["ribs"], "insertion": ["clavicle"], "sources": ["abdala-diogo-2010"],
                   "shiftNote": "As the subclavius. With the coracoid gone the insertion transfers to the clavicle — Howell's (1937b) basis for the homology."},
    },
    "caudofemoralis": {
        "lepidosauria": {"origin": ["caudal-vertebrae"], "insertion": ["femoral-trochanter"],
                         "sources": ["diogo-molnar-2014", "dick-clemente-2016"],
                         "shiftNote": "Longus arises from the proximal third of the tail and caudal vertebrae 4-14, inserting by broad tendon on the femoral trochanter plus a second tendon onto the lateral menisci of the knee; brevis arises from the transverse processes of the four most anterior postsacral vertebrae. Femur retraction and long-axis rotation, active in stance."},
        "crocodylia": {"origin": ["caudal-vertebrae", "ilium"], "insertion": ["fourth-trochanter"], "sources": ["diogo-molnar-2014", "allen-etal-2014", "klinkhamer-etal-2017"],
                       "shiftNote": "Klinkhamer et al. distinguish caudofemoralis longus (caudal vertebrae) from brevis (ilium); both converge on the fourth trochanter."},
        "testudines":   {"origin": ["caudal-vertebrae"], "insertion": ["femur"], "sources": ["diogo-molnar-2014"]},
        "synapsida-stem": {"origin": ["caudal-vertebrae"], "insertion": ["fourth-trochanter"], "sources": ["bishop-pierce-2024"],
                           "shiftNote": "Progressive reduction of the fourth trochanter along the synapsid stem tracks the loss of tail-driven femoral retraction."},
    },
    "opercularis": {
        "anura": {"origin": ["suprascapula"], "insertion": ["operculum"], "sources": ["abdala-diogo-2010"],
                  "shiftNote": "A pectoral girdle muscle inserting on the ear. Anuran-only, and only in anurans is it a discrete muscle."},
    },
    "triceps-brachii": {
        "caudata":    {"origin": ["scapula", "humerus"], "insertion": ["olecranon"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["scapula", "coracoid", "humerus"], "insertion": ["olecranon"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["scapula", "humerus"], "insertion": ["olecranon"], "sources": ["ercoli-etal-2014"]},
    },
    "biceps-brachii": {
        "lepidosauria": {"origin": ["coracoid"], "insertion": ["radius"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["scapula", "coracoid-process"], "insertion": ["radial-tuberosity"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "The short head arises from the coracoid process — the fused remnant of the coracoid — rather than from a coracoid bone."},
    },
    "coracobrachialis": {
        "caudata":      {"origin": ["coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "aves": {"origin": ["sternum", "coracoid"], "insertion": ["tuberculum-ventrale"],
                 "sources": ["abdala-diogo-2010", "matsuoka-hasegawa-2007"],
                 "shiftNote": "Coracobrachialis caudalis: one of two deep tongue-like muscles from the sternum, arising from the craniolateral corner of the sternal plane and the ventrolateral coracoid base, inserting on a shallow notch on the tuberculum ventrale of the proximal humerus."},
        "theria": {"origin": ["coracoid-process"], "insertion": ["humerus"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "Origin transfers to the coracoid process as the coracoid bone is lost."},
    },
    "hypobranchial-muscles": {
        "testudines": {"origin": ["hyoid", "dentary"], "insertion": ["corpus-hyoidei", "hyoid"],
                       "sources": ["werneburg-2011"],
                       "shiftNote": "Aggregated across eight units (genioglossus, geniohyoideus, coracohyoideus, hyoglossus and their parts). Werneburg records CN XII for these, confirming their somitic rather than branchiomeric origin."},
        "chondrichthyes": {"origin": ["pectoral-girdle"], "insertion": ["mandible", "hyoid", "branchial-arches"], "sources": ["ziermann-etal-2014", "diogo-ziermann-2015"],
                           "shiftNote": "Origin on the coracoid bar ties the feeding apparatus mechanically to the pectoral girdle. Loosening that link is a precondition for a neck."},
        "theria": {"origin": ["sternum", "clavicle", "scapula", "hyoid"], "insertion": ["hyoid", "tongue"], "sources": ["ziermann-diogo-2019"],
                   "shiftNote": "With the coracoid gone the infrahyoid muscles take origin from sternum, clavicle and scapula instead."},
    },
    # --- Crocodylus porosus, from Klinkhamer et al. (2017) digital dissection.
    # Their descriptions name an explicit aspect for nearly every attachment,
    # which is the densest source of `side` values in the dataset.
    "levator-scapulae": {
        "crocodylia": {"origin": ["ribs"], "insertion": ["scapula"], "sources": ["klinkhamer-etal-2017"],
                       "shiftNote": "Origin with the neck muscles on the lateral cervical ribs; fleshy insertion running the anterior scapular border from its anterodistal tip to the glenohumeral joint."},
    },
    "costocoracoideus": {
        "crocodylia": {"origin": ["ribs"], "insertion": ["coracoid"], "sources": ["klinkhamer-etal-2017"],
                       "shiftNote": "Klinkhamer et al. separate a costocoracoideus profundus originating on the lateral margin of the first few ribs."},
    },
    "serratus-anterior": {
        "crocodylia": {"origin": ["ribs"], "insertion": ["scapula"], "sources": ["klinkhamer-etal-2017"],
                       "shiftNote": "Originates from the ventrolateral ribs and inserts by tendon along the entire medio-posterior scapular margin — a broad, thin girdle extensor."},
    },
    "scapulohumeralis-posterior": {
        "crocodylia": {"origin": ["scapula"], "insertion": ["humerus"], "sources": ["klinkhamer-etal-2017", "abdala-diogo-2010"],
                       "shiftNote": "Origin on the proximo-lateral and posterior scapula, insertion on the proximo-lateral humeral head, both fleshy. Klinkhamer et al. equate it with teres minor, which bears on the unresolved scapulohumeralis/teres minor question."},
    },
    "femorotibialis": {
        "lepidosauria": {"origin": ["femur"], "insertion": ["cnemial-crest"],
                         "sources": ["dick-clemente-2016", "diogo-molnar-2014"],
                         "shiftNote": "Fleshy origin along the entire femoral shaft; joins the iliotibialis tendon to insert on the cnemial crest. Knee extensor, active in both stance and swing."},
        "crocodylia": {"origin": ["femur"], "insertion": ["cnemial-crest"], "sources": ["klinkhamer-etal-2017"],
                       "shiftNote": "Externus arises fleshy about a third of the way down the dorsal femur and inserts on the proximo-lateral cnemial crest; internus arises by tendon on the dorso-proximal femur, distal and anterior to iliofemoralis, and joins the same tendon at insertion."},
    },
    "ambiens": {
        "lepidosauria": {"origin": ["acetabulum-ventral-edge", "pubis"], "insertion": ["intertrochanteric-notch"],
                         "sources": ["tomanska-etal-2025", "diogo-molnar-2014", "dick-clemente-2016"],
                         "shiftNote": "In Varanus komodoensis the muscle has dorsal and ventral heads; the dorsal attaches to the ventral edge of the acetabulum and the ventral lies anteriorly, both converging on the femur at the intertrochanteric fossa."},
        "crocodylia": {"origin": ["pubis"], "insertion": ["tibia"], "sources": ["klinkhamer-etal-2017", "diogo-molnar-2014"],
                       "shiftNote": "Tendinous origin on the proximo-lateral pubis, becoming tendinous distally along the anterior surface."},
    },
    "ischioflexorius": {
        "crocodylia": {"origin": ["ischium", "ilium"], "insertion": ["tibia"], "sources": ["klinkhamer-etal-2017", "diogo-molnar-2014"],
                       "shiftNote": "Flexor tibialis internus is four-part in Crocodylus: FTI1 from the postero-lateral ischium to the proximo-medial tibia by a long tendon shared with puboischiotibialis; FTI2 fleshy from the postero-ventral ilium; FTI3 from the proximo-lateral ischium."},
    },
    "extensor-iliotibialis": {
        "crocodylia": {"origin": ["ilium"], "insertion": ["femur"], "sources": ["klinkhamer-etal-2017", "diogo-molnar-2014"],
                       "shiftNote": "Iliotibialis 3 arises deep to iliotibialis 2 on the central lateral ilium by tendon and inserts fleshy onto the distal third of the dorso-lateral femur."},
    },
    "iliofemoralis": {
        "lepidosauria": {"origin": ["ilium"], "insertion": ["femur"], "sources": ["diogo-molnar-2014", "dick-clemente-2016"],
                         "shiftNote": "From the anterior iliac blade, sharing an intramuscular septum with the puboischiotibialis; the belly wraps the posterior femoral border to insert proximally. Femur abductor, active in swing."},
        "crocodylia": {"origin": ["ilium"], "insertion": ["femur"], "sources": ["klinkhamer-etal-2017", "diogo-molnar-2014"],
                       "shiftNote": "Origin on the lateral ilium; the femorotibialis internus tendon arises distal and anterior to it, which is the landmark Klinkhamer et al. use to separate the two."},
        "synapsida-stem": {"origin": ["ilium", "iliac-crest"], "insertion": ["greater-trochanter"], "sources": ["bishop-pierce-2024"],
                           "shiftNote": "Expansion of the iliac blade along the synapsid stem tracks the enlargement of this field and the shift toward erect posture."},
        "theria": {"origin": ["ilium", "iliac-crest"], "insertion": ["greater-trochanter"], "sources": ["diogo-molnar-2014"],
                   "shiftNote": "Same muscle, same nerve, same attachments — but in a parasagittal limb it becomes the principal pelvic stabiliser during single-limb support."},
    },
}


def main(write: bool) -> int:
    skel = json.loads((ROOT / "data/skeleton.json").read_text())
    elements = {e["id"]: e for e in skel["elements"]}

    docs, added, problems = {}, 0, []
    index = {}
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            index[m["id"]] = m

    for mid, per_taxon in SEED.items():
        m = index.get(mid)
        if not m:
            problems.append(f"unknown muscle '{mid}'")
            continue
        occs = {o["taxon"]: o for o in m.get("occurrences", [])}
        for tid, spec in per_taxon.items():
            occ = occs.get(tid)
            if not occ:
                problems.append(f"{mid}: no occurrence row for taxon '{tid}'")
                continue
            for side in ("origin", "insertion"):
                for ref in spec.get(side, []):
                    if ref not in elements:
                        problems.append(f"{mid}/{tid}: '{ref}' not in skeleton.json")
                        continue
                    pres = elements[ref].get("presence", {})
                    ok = tid not in pres.get("absent", []) and (
                        pres.get("default") != "no"
                        or tid in pres.get("present", []) + pres.get("partial", []) + pres.get("reduced", []))
                    if not ok:
                        problems.append(f"{mid}/{tid}: '{ref}' is recorded absent in that taxon")
            occ["attachments"] = {"origin": spec["origin"], "insertion": spec["insertion"]}
            if spec.get("shiftNote"):
                occ["attachmentNote"] = spec["shiftNote"]
            occ["sources"] = sorted(set(occ.get("sources", [])) | set(spec["sources"]))
            added += 1

    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(f"  {p}")
        return 1

    print(f"{added} occurrence rows seeded with structured attachments "
          f"across {len(SEED)} muscles")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"rewrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
