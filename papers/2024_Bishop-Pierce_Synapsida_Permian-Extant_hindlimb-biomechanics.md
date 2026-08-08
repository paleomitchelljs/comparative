# Bishop & Pierce 2024 — Late acquisition of erect hindlimb posture and function in the forerunners of therian mammals

## Citation
Bishop PJ, Pierce SE. 2024. Late acquisition of erect hindlimb posture and function in the forerunners of therian mammals. *Science Advances* 10: eadr2722. doi:10.1126/sciadv.adr2722.

## Question
The synapsid-to-mammal transition involved a shift from "sprawled" (reptile-like, limbs out to the side) to "erect" (therian, limbs under the body) hindlimb posture. **When** across 320+ Myr of synapsid evolution did this happen, and did it follow a simple linear trajectory from sprawled pelycosaurs to erect mammals?

> "The evolutionary transition from early synapsids to therian mammals involved profound reorganization in locomotor anatomy, centered around a shift from 'sprawled' to 'erect' limb postures."

> "By quantifying the global actions of major hip muscle groups indicates a protracted juxtaposition of functional redeployment and conservatism, highlighting the intricate interplay between anatomical reorganization and function across postural transitions."

## Taxa and material
**13 taxa** spanning the synapsid grade ladder + extant brackets:
- **Extant sprawling/intermediate**: *Salvator merianae* (tegu, Squamata), *Alligator mississippiensis* (Crocodylia), *Tachyglossus aculeatus* (echidna, Monotremata).
- **Extant erect**: *Didelphis virginiana* (Virginia opossum, Marsupialia), *Canis familiaris* (domestic dog, Placentalia).
- **Extinct sprawling**: *Ophiacodon retroversus* (Ophiacodontidae, Early Permian, 296.4 Ma), *Dimetrodon milleri* (Sphenacodontidae, 290.1 Ma).
- **Extinct intermediate/transitional**: *Oudenodon bainii* (Dicynodontia, 259.9 Ma), *Lycaenops ornatus* (Gorgonopsia, 259.9 Ma), *Regisaurus jacobi* (Therocephalia, 252.2 Ma), *Massetognathus pascuali* (Cynognathia, 242 Ma), *Megazostrodon rudnerae* (Morganucodontidae, 201.3 Ma), *Vincelestes neuquenianus* (stem therian, Cladotheria, 129.4 Ma).

Focal specimens listed in Table 1 with hindlimb completeness, body mass, and institutional provenance (AMNH, FMNH, MCZ, NHMUK, MACN, BP).

## Time frame
Early Permian (Ophiacodontidae, ~296 Ma) → Early Cretaceous (*Vincelestes*, 129 Ma) → Extant. The transition is mapped across ~170 Myr of synapsid stem-group evolution.

## Methods
- **3D musculoskeletal model per taxon** in OpenSim 3.3: pelvis + right hindlimb, with hip (3 DOF) + knee (1 DOF) + ankle (1 DOF) joints. Muscle attachments drawn from published reconstructions and extant bracket inference.
- **Feasible Force Space (FFS)** as the main performance metric. The FFS is a 3D envelope that delineates the range of forces the whole hindlimb can apply to the external environment at a given posture, across all possible muscle recruitment patterns. Volume of the FFS (cube root, CRV) quantifies total force-generating capacity; partitioning into six cardinal directions (ventral = weight support; dorsal; anterior; posterior = propulsion; medial; lateral = turning/agility) quantifies functional specialization.
- **Postures sampled**: adduction 0° (fully erect) to 90° (fully sprawled) in 10° steps × 3 flexion levels (crouched, intermediate, extended) × ±15° forward-back pitch. Only **osteologically viable postures** (no joint disarticulation, no bone collision) included.
- **Muscle strengths (F_max)** for extinct taxa derived from allometric scaling equations fit to dissection data from *Salvator*, *Alligator*, *Tachyglossus*, *Didelphis*, *Canis*. F_max normalized to "muscle strength units" (MSU) so force values are comparable across body masses ranging from *Megazostrodon* (35 g) to *Ophiacodon* (88 kg).
- **Kinematic Potentials (KP)** for four major hip muscle groups (iliofemoralis → gluteals IF/GLUT; anterior iliotibialis → rectus femoris ITa/RF; ambiens → sartorius AMB/SART; puboischiofemoralis internus → iliopsoas PIFI/ILPS) computed across all postures. KPs describe how a muscle tends to move the foot in global space.
- **Ancestral state reconstruction** of hindlimb performance along the synapsid stem lineage using squared-change parsimony.
- **Hyperdimensional performance profiles** clustered by Pearson-correlation dendrogram to classify each taxon as "therian," "sprawling," or "nonsprawling" style without imposing posture-based categories a priori.

## Findings (numbered)

1. **Erect therian-like hindlimb function is a late innovation, not a linear outcome.** The performance profiles that cluster with the extant therians *Canis* + *Didelphis* are restricted to just those two taxa (Figs. 2, 3, 4B). *Vincelestes* — a stem therian only ~25 Myr before crown Theria — still sits outside the therian cluster. Therefore **erect locomotion proper evolved within the ~50 Myr preceding crown Theria**, probably within cladotherians.

> "Quantifying major hip muscle groups identifies divergent patterns of functional change and conservatism, underscoring the intricate interplay between anatomical reorganization, posture, and function throughout synapsid evolution."

2. **There was a transient peak of hindlimb force capacity in therapsids + early cynodonts, followed by a reversal.** CRV (total force capacity) increases monotonically from Ophiacodontidae → Sphenacodontidae → Neotherapsida → Theriodontia, peaks at Eucynodontia (around *Massetognathus*), then **declines** through Mammaliaformes (*Megazostrodon*) and Prototribosphenida (*Vincelestes*) before rising again in crown mammals (Fig. 5). The posterior (propulsive) component is the only metric that keeps increasing monotonically on the stem.

3. ***Massetognathus*** **is most similar in performance profile to *Alligator***, not to modern therians. Both can use a range of postures; both have high adduction-angle flexibility; both show broadly comparable CRV partitioning. This is consistent with Kemp's longstanding "postural flexibility" hypothesis for advanced therapsids + cynodonts — they were **facultatively erect**, like extant crocodilians.

4. **Hierarchical clustering gives two major categories**, not a linear grade series (Fig. 4B): "Sprawling" (pelycosaurs + nontherian mammaliaforms including *Megazostrodon* + *Tachyglossus*) and "Nonsprawling" (therapsids + cynodonts + *Vincelestes* + therians, subdivided into "Therian" *Canis* + *Didelphis*). This rejects a simple Hennigian-comb model where every stem node is more therian-like than its ancestor. The eucynodont-to-mammaliaform reversal is real and unexpected.

5. **Four major hip-muscle transformations show three contrasting themes** (Figs. 6, 7):
   - **Functional redeployment** (iliotibialis → rectus femoris, ambiens → sartorius): IF-derived muscles shift origin close to the acetabulum, becoming a forceful knee extensor during stance; AMB origin shifts to anterior ilium to become a swing-phase hip protractor. **Same muscle bundle, completely new global action.**
   - **Posture-dependent function without anatomical change** (iliofemoralis → gluteals): the IF acts as limb elevator in sprawled postures (swing phase) and as limb abductor in erect postures (stance phase). **Same anatomy, different posture, different function** — the muscle does not "evolve" in any naive sense; the body around it moves.
   - **Global functional conservation under major anatomical change** (puboischiofemoralis internus → iliopsoas): origin shifts dorsally from pubis to lumbar vertebrae; insertion shifts on femur; greater trochanter vs. lesser trochanter change. Despite all that, PIFI/ILPS remains a swing-phase hip protractor throughout the entire 170 Myr transition. **Different anatomy, same job.**

6. **Implication for fossil interpretation.** Muscle-by-muscle comparisons across deep time without a whole-limb framework are **misleading**. The same IF action (limb elevator) can be recovered in a sprawler by swing-phase recruitment or in an erect animal by stance-phase recruitment of a homologous but relocated muscle. This means direction-of-causality arguments (e.g., "the greater trochanter evolved to support erect posture") are not supported by this dataset; the anatomical change may be a **passive consequence** of postural evolution, not its driver.

7. **Ectaxonic manus/pes asymmetry reconciled.** Sprawling squamates + salamanders have digit IV as longest; therians have broadly symmetric pedes. *Vincelestes* + cladotherians were the first to shift toward symmetry, consistent with the proposed late acquisition of erect posture. Retention of a large lesser trochanter in monotremes + most nontherian mammaliaforms (Fig. S6) physically **precludes strongly adducted limb postures** — trochanter collision with the pelvis limits erect posture, a direct osteological argument.

8. **Coevolution with forelimb reorganization is asymmetric.** Hindlimb force capacity reverses in eucynodonts, coinciding with the forelimb reorganization Lai, Biewener & Pierce 2018 documented for *Massetognathus* (pectoral girdle bones decoupling, glenoid reorientation, sternum appearance). Forelimb and hindlimb were therefore **not coevolving in lockstep**; the hindlimb may have been "along for the ride" during the major cynodont forelimb rewiring.

## Key figures
- **Fig. 1** — The study taxon phylogeny with musculoskeletal hindlimb models for each, plus the Feasible Force Space concept illustrated on *Massetognathus*.
- **Fig. 2** — Extant taxa force-capacity envelopes across posture continuum: *Salvator*, *Alligator*, *Tachyglossus*, *Didelphis*, *Canis* (left → right). Yellow bars mark habitually used in vivo postures. CRV peaks at the habitual posture in 4/5 taxa.
- **Fig. 3** — Same panel structure for the 8 extinct taxa: *Ophiacodon*, *Dimetrodon*, *Oudenodon*, *Lycaenops*, *Regisaurus*, *Massetognathus*, *Megazostrodon*, *Vincelestes*. Visualizes the transient peak.
- **Fig. 4** — The classification panel: (A) phyloplot of optimal adduction angle vs. Pearson correlation with *Canis*, showing the early-cynodont reversal; (B) dendrogram of performance profiles — "Sprawling" (pelycosaurs + mammaliaforms + *Salvator*) vs. "Nonsprawling" (therapsids + *Vincelestes* + therians). The single best one-slide result.
- **Fig. 5** — Ancestral-state reconstruction of force capacity along the stem: total CRV + six cardinal partitions. Non-monotonic — peaks at Eucynodontia, dips at Mammaliaformes, rises again in Mammalia.
- **Fig. 6** — Kinematic Potentials for four major hip-muscle groups on a Mollweide unit-sphere projection, per taxon. Reveals where each muscle can move the foot; color-coded by adduction angle.
- **Fig. 7** — The headline muscle-function figure: five-stage schematic (pelycosaur → therapsid → eucynodont → mammaliamorph → crown therian) showing GLUT, ITa/RF, AMB/SART, PIFI/ILPS arrows in swing vs. stance phase, with a 2×2 long-axis-rotation summary per stage.

## Limitations
- **FFS is a maximal-envelope metric** — it quantifies what the limb **could** do, not what each taxon **actually did**. Muscle recruitment in life probably never reached the envelope boundary.
- Muscle strength in extinct taxa is estimated via allometric scaling from five extant anchors; the authors run sensitivity analyses (±20% perturbation) and recover the same patterns, but the absolute values are uncertain.
- Muscles are modeled as forces along lines of action, **excluding force-length-velocity relationships** — a necessary simplification given the lack of fiber-architecture data from fossils.
- Joint translational offsets are not modeled; only rotational DOFs.
- **Thirteen taxa** is a small sample for a 170-Myr transition. Any single clade (e.g., Gorgonopsia) rests on one individual. Additional stem-therian specimens would directly test the late-acquisition hypothesis.
- The pes is modeled as a single rigid entity (with notes on specimen-specific ankle joint handling). Digit-level and proximal-distal tarsal mobility is not resolved.

## Relevance to comparative anatomy teaching
This is the most rigorous recent treatment of the sprawled-to-erect transition and deserves a place in the synapsid locomotion lecture. Four teaching uses:

1. **The transition was not linear and not early.** Too many intro textbooks still draw a tidy pelycosaur → therapsid → cynodont → mammal ladder of increasingly upright limbs. This paper shows that full erect hindlimb function appears only in the last ~50 Myr before crown Theria, after a transient peak in therapsid/cynodont performance that then **reversed** in mammaliaforms. The Fig. 4B dendrogram is the one-slide correction.

2. **Same anatomy, different posture, different function (and vice versa).** The IF/GLUT and PIFI/ILPS cases in Fig. 7 are the cleanest examples of how whole-limb biomechanics decouples muscle anatomy from muscle function. Useful slide for introducing the concept that a muscle's **job** is set by its body context, not just its attachments.

3. **Musculoskeletal modelling as a fossil-interpretation tool.** The FFS + KP framework is transferable. Pair with Dick & Clemente 2016 (varanid architecture), Allen et al. 2014 (crocodilian architecture), Fahn-Lai et al. 2020 (tegu-opossum shoulder bracket for *Massetognathus*), Regnault & Pierce 2018 (echidna shoulder model) for the library's full "computational comparative biomechanics" teaching module.

4. **Forelimb and hindlimb did not coevolve in lockstep.** Lai, Biewener & Pierce 2018 + Fahn-Lai et al. 2020 + Abdala & Diogo 2010 document the major cynodont forelimb reorganization; this paper argues the hindlimb was still flexibly sprawled in cynodonts. Useful for teaching that body-part-level modularity is real in macroevolution.

Pair with Bendel et al. 2022 (gorgonopsian multipartite sternum — a thoracic parallel of this hindlimb story, with functional-reorganization-preceding-anatomical-change logic), Crompton et al. 2018 (mammaliaform braincase), Molnar et al. 2018 (sarcopterygian pectoral muscles), Smith-Paredes et al. 2022 (amniote forelimb cleavage) for a full axial-and-appendicular synapsid-to-mammal teaching unit.
