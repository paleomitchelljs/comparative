# Gest — Medical Gross Anatomy: Anatomy Tables (muscles)

## Citation

Gest TR. *Medical Gross Anatomy — Anatomy Tables: muscles*. Texas Tech University
Health Sciences Center. Teaching resource, web. Origin, insertion, action,
innervation and arterial supply for 279 human muscles across seven regions.

No PDF is held. This is a web resource and the repository has no archived
snapshot of it, which is the one real risk attached to the source: the rows in
`data/` are the only in-repo record of what it said. A stable archive link is
worth adding.

## What it is

The distillation of human gross anatomy as taught from the dissecting room. The
attachments in it are dissection-derived in exactly the sense the comparative
monographs in this corpus are — the difference is that the human body is the most
dissected animal there has ever been, so the table states a condition confirmed
across a vastly larger sample than any single-specimen description here rests on.
It is treated accordingly: **its statements about human anatomy carry the same
weight as any other dissection-based source in this dataset.**

The one thing it is not is a comparative source. It describes one animal and
makes no homology claims across taxa, so it carries no `homologyScope` — the
same standing as Cunningham (1882) on the thylacine or Osawa (1898) on the
tuatara. Where a later comparative treatment homologises differently, that
treatment governs the homology and Gest still governs the attachment, which is
the general rule in this repository and not a judgement about this source.

## Why the human column exists

**To be the baseline.** It is the anatomy most readers already carry, and every
other column can be read against it. Pick *Homo sapiens* in the taxon selector
and the shoulder reads *supraspinatus and infraspinatus* where a lizard reads
*supracoracoideus*, the jaw reads *masseter, temporalis and the pterygoids* where
a shark reads *adductor mandibulae*, and the pelvic floor turns out to be tail
musculature.

## Scored

**Re-mined to exhaustion 2026-08-20. 239 distinct muscles: 222 filed, 17 parked.**
The arithmetic is in the region table further down and the pass is described region
by region under it.

277 filed rows across 130 records and all six muscle files, plus 15 parked. The
count of *rows* exceeds the count of *muscles filed* because the pre-existing
summary rows are kept alongside the per-muscle rows that were added under them, and
falls short of it where one record takes several of Gest's names.

| Region | Rows | | Region | Rows |
|---|---:|---|---|---:|
| cranial | 85 | | leg | 18 |
| axial | 46 | | thigh | 18 |
| forearm | 30 | | hand | 15 |
| pectoral | 21 | | arm | 4 |
| pelvic | 21 | | | |
| foot | 18 | | | |

253 rows are `yes`, 17 `no`, 5 `uncertain`.

Before the re-mine this was 105 rows on 105 records, all of them group rows
carrying a lumped name and the union of a group's attachments. Those rows are still
here and still carry the comparative argument; what changed is that the muscles they
named now have attachments of their own.

**17 rows are scored `present: "no"`, and they are the most useful thing the
source gave.** An absence stated against a table of 279 muscles is an observation,
not a silence, and these are the rows that let a human column participate in the
phylogeny view instead of dropping out of it. The pattern they trace is a hand
that has lost muscles a foot kept: no `flexor-accessorius-lateralis` in the hand
while the foot keeps it as quadratus plantae, no `contrahentium-caput-longum` in
either, no `pronator-profundus-pes` because a human leg has no pronator — the
tibia and fibula do not rotate on each other.

**5 rows are `uncertain`, and all five are the same problem**: the human
interossei are one set of muscles that the comparative scheme resolves into
several records (`flexores-breves-profundi`, `intermetacarpales`,
`dorsometacarpales`, and their pedal counterparts). They are scored once, on the
record that carries them, and the others say so rather than double-counting.

## Where a human name is not the muscle this dataset calls by that name

This is the source's sharpest contribution and it is a nomenclature problem, not a
reliability one. Human clinical names collide with comparative ones:

- **`levator-anguli-oris`** — a human has a muscle of that name. It is not this
  record. The row is `present: "no"` and says why.
- **The human sartorius is deliberately given no home**, because Diogo & Molnar
  (2014) reject the equation with the reptilian 'ambiens' that would give it one.
  `ambiens` is scored absent in humans with the note about the muscle it is not.
- **The erector spinae group is regional labelling, not muscle identity.** Gest's
  iliocostalis, longissimus, spinalis and semispinalis are subdivisions of one
  segmentally supplied field running from the top of the neck to the sacrum.

Getting these three wrong would put a human muscle on a record it is not
homologous with, which is the failure mode the whole dataset is built to avoid.

## Relevance to comparative anatomy teaching

The reference column. Its value is not that it is unusual but that it is the one
anatomy a student already has, so every comparative statement in the dataset can
be delivered as a difference from it. The 17 absences are the teaching material:
each one is a muscle some other vertebrate has and the reader does not, which is
a more memorable fact than a list of what humans do have.

## Two files removed, 2026-08-20 — a human table cited on a cheetah and a rat

**Gest describes 279 human muscles and examines no other animal.** It was cited on
three non-human occurrences:

- *Acinonyx jubatus* on `cricoarytenoideus-lateralis`, sourced to **this table
  alone**. Its own `speciesBasis` was `default` — the schema's word for "nothing
  better, the clade's first exemplar, and a guess" — and its note is written about
  a *human* row: "Diogo et al. (2008) Table 3 gives this muscle only to the rat
  ... so the human row here rests on the descriptive source". A human observation
  had landed on a cheetah. The occurrence is deleted; nothing is lost, because the
  human reading it describes is in the table and will be filed under *Homo
  sapiens*.
- *Rattus norvegicus* on `musculus-uvulae` and `vocalis`. Both also cite
  `diogo-etal-2008-head`, which genuinely covers the rat, so removing this source
  leaves both rows properly sourced by the survey that made the observation.

Fifth instance of the failure `MINING.md` opens with, after Werneburg, Johnston,
Cieri and Molnar.

## Scope of the human re-mine — measured, not estimated

`muscles_alpha.html` is the complete alphabetical table and the one to work from;
the seven regional files are subsets of it. Parsed, it holds **272 muscles**, each
with origin, insertion, action, innervation, arterial supply and a comment column.

| | |
|---|---:|
| Muscles in the table | 272 |
| Already carrying a row of that name | 48 |
| Missing, and an existing record's id, name or synonym matches | 25 |
| **Missing, and no record matches by name** | **199** |

The dataset holds 116 rows on *Homo sapiens* from this source, under 94 distinct
names, so the gap is not a few stragglers — **it is most of the human body**.

The 199 are not all hard. Many will map on inspection: `deltoid` onto the
deltoideus records, `extensor carpi radialis longus` and `brevis` onto
`extensor-antebrachii-carpi-radialis`, the four `rectus capitis posterior` and
`obliquus capitis` muscles onto the suboccipital part of the epaxial series. But
**each is a homology call**, which is the expensive part and cannot be batched.
Expect to park a real fraction on `no-record`: the human table is finer than this
dataset's records in the hand, the foot, the perineum and the larynx.

To reproduce the diff, parse `<tr>` rows out of `muscles_alpha.html`, take cells
`[name, origin, insertion, action, nerve, artery, comment]`, normalise the name to
lowercase letters and spaces, and compare against the `name` fields in
`data/observations/homo-sapiens__gest-anatomy-tables.json`.

**The 272 was an undercount, and the parse that produced it is worth fixing before
anyone repeats it.** Five `<tr>` elements in `muscles_alpha.html` are unclosed, so
their cells run on into the next muscle's row and a naive `len(cells) == 8` filter
drops everything after the first. Chunk any row whose cell count is a multiple of
eight, and the table yields **274 named entries**: 273 muscles and one
cross-reference (`peroneus mm.`, pointing at `fibularis mm.`). Of the 273, **33 are
the same muscle listed twice under both orderings of its name** — `anterior scalene`
and `scalene, anterior`, `rectus, inferior` and `inferior rectus` — which is a
courtesy of the alphabetical listing, not two muscles. Detect them by grouping on
identical origin and insertion text; one pair that survives that test,
`linguae, transversus` and `linguae, verticalis`, is two real muscles sharing a
table entry.

**239 distinct muscles**, plus the one cross-reference. The per-region split is in
the table below and does not match a naive count of the seven regional files, which
between them repeat several muscles.

## The re-mine, region by region

Started 2026-08-20. Gest's seven regions are worked one at a time and each is
committed on its own, because a homology call is the expensive part and a region is
the largest batch whose calls are about the same thing.

The rows already in the file are **summary rows**: one per record, carrying a
grouped name, a `parts` list and the union of the group's attachments. They came
out of the old storage and they are why the human column looks fuller than it is —
`Masseter, temporalis, the pterygoids and the tensors` is one row standing for four
muscles, none of which has its own origin and insertion recorded. The re-mine keeps
those rows, which carry curated comparative argument, and adds **a row per muscle**
carrying only `name`, `attachments` and its own paragraph. The join merges them into
the one occurrence the schema allows per (record, species): attachments union, the
paragraphs concatenate, the established label and division stay put. So the pass
buys three things at once — the mapping layer gains a key per human muscle name, the
occurrence gains the attachment rows the summary lacked, and the reading is on the
page under the name Gest used.

A merging row therefore sets **only** `name`, `present`, `attachments` and
`attachmentNote`. Setting `action`, `innervation`, `division` or `parts` on it would
stop the build, and correctly: those fields have to agree across the rows that make
one occurrence.

| Region | Entries | Distinct | Filed | Parked | State |
|---|---:|---:|---:|---:|---|
| Back | 16 | 16 | 16 | 0 | **done** |
| Thorax | 7 | 7 | 7 | 0 | **done** |
| Abdomen | 13 | 11 | 10 | 1 | **done** |
| Pelvis and perineum | 21 | 17 | 7 | 10 | **done** |
| Upper limb | 54 | 52 | 51 | 1 | **done** |
| Lower limb | 58 | 53 | 52 | 1 | **done** |
| Head and neck | 105 | 83 | 79 | 4 | **done** |
| **total** | **274** | **239** | **222** | **17** | **done** |

Pelvis counts bulbospongiosus and sphincter urethrae twice, once per sex, which is
how Gest lists them; they are 15 muscles and get one row each, so eight parked rows
cover ten distinct entries.

### Back, done

Sixteen entries, sixteen filed, nothing parked. Three were already rows —
iliocostalis, longissimus and the erector spinae umbrella; twelve are new; and the
suboccipital four were named in an existing `parts` list without ever having an
attachment recorded.

The splits follow the assignment the human `epaxial-musculature` row already argued
for and did not implement. Splenius and the four suboccipital muscles go to the
umbrella record, because the dataset has no spinotransversal tract to put them on.
Semispinalis, multifidus, rotatores, interspinales, intertransversarii and spinalis
go to `transversospinalis`, which the record defines as the *medial* epaxial tract
rather than by fibre direction — spinalis and interspinales run spine-to-spine and
are scored there anyway, and their rows say so.

Two things came out of it worth keeping:

- **`mastoid-process` is a new skeletal element** (`partOf: otic-capsule`, therian).
  Four human muscles end on it and all four were scored on `occiput`, which puts a
  petrosal attachment on the occipital bone. The longissimus row's own note said it
  was doing this and named the missing element; it has been corrected. The other
  three are in the head and neck region and are not yet touched.
- **The intertransversarii may not belong on an epaxial record at all.** Gest gives
  the whole series dorsal rami, so the row follows him, but most accounts supply the
  cervical and lumbar members at least partly from ventral rami. If that is right the
  row lumps an epaxial and a hypaxial muscle under one name. The row says so.

### Thorax and abdomen, done

Twenty entries, eighteen distinct after the two obliques' double listing. Twelve
rows added, one parked, and three existing rows corrected.

**The diaphragm was the point of the batch.** It had been described in the
`hypaxial-musculature` note since that row was written — xiphoid, costal margin,
arcuate ligaments, the crura on L1-L3, all onto the central tendon — and carried
**not one attachment row**, because three of its five sites had no element. It has
them now. Read as an itinerary the origin is the muscle's own history: cervical
myotome dragged caudally with the phrenic nerve paying out behind it from C3-C5,
ending up arising from the fascia of two lumbar muscles and inserting on nothing but
itself.

Five new elements, four of them for muscle ends that had been dropped rather than
recorded: `arcuate-ligaments`, `central-tendon-diaphragm`, `xiphoid-process`,
`inguinal-ligament`, `spermatic-cord`. The inguinal ligament is the one worth
noticing — it is made by the external oblique aponeurosis and then carries the
origins of the two layers underneath it, so a ligament built by one body-wall sheet
is the attachment site of the next two. The internal oblique and transversus
abdominis rows had both been scored without it.

Three calls that could have gone the other way:

- **Transversus thoracis is on `intercostales-interni`,** following Gest, who groups
  it with subcostalis and the innermost intercostals as the deepest thoracic layer.
  On the developmental account it is the thoracic continuation of transversus
  abdominis and belongs on that record. The two readings disagree about whether the
  innermost thoracic layer goes with the intercostals or with the transversus sheet,
  and nothing in this source decides it. In the note, not resolved.
- **Psoas minor is a body-wall muscle, not half of the iliopsoas.** It ends on the
  iliopubic eminence and never reaches the femur, so it is on
  `hypaxial-musculature` with quadratus lumborum — which is also the pairing
  Schilling's mammalian ventrovertebral series makes, already quoted in that
  record's homology note. Psoas *major* goes to
  `puboischiofemoralis-internus` with iliacus, because the iliopsoas tendon is what
  makes them one muscle.
- **Dartos is parked, and the reason generalises.** It is smooth muscle — Gest calls
  it modified arrector pili — driven by postganglionic sympathetic fibres. Every
  record here is a striated somatic muscle, so no record can be right and creating
  one would put a second tissue type in the same table. Trachealis, the detrusor and
  the intrinsic muscles of the iris are the same case and are still to come in the
  head and neck.

The interfoveolar muscle is filed on `transversus-abdominis` with **no** attachment
rows, which is the one place in this pass that the never-drop-an-attachment rule was
knowingly not followed. Its two ends are the parent muscle itself and the anterior
lamina of the femoral sheath; adding a `femoral-sheath` element for one inconstant
human slip would put a piece of inguinal fascia in a controlled vocabulary that no
other column can use. Both ends are in the row's prose.

### Pelvis and perineum, done — and half of it parks

Twenty-one entries, fifteen muscles: four are the alphabetical listing's own
duplicates, and bulbospongiosus and sphincter urethrae each appear twice, once per
sex. Seven filed, **eight parked** — the highest parked fraction of any region so
far, and the reason was predictable from the first pass's warning that this dataset
is coarser than the human table in the perineum.

**Filed.** Levator ani and its four named slips — pubococcygeus, puborectalis,
pubovaginalis, levator prostatae — go to `iliocaudalis`, which is where the
iliococcygeus row already said they belonged and named them. Coccygeus was already
on `ischiocaudalis`. The pelvic floor of an animal with no tail is the tail
musculature of one that has, and both records now carry the whole sheet.

**Parked, and why it is a real gap rather than a hard call.** Six perineal muscles —
external anal sphincter, bulbospongiosus, ischiocavernosus, the two transverse
perinei, sphincter urethrae — are cloacal sphincter derivatives: skeletal muscle on
the pudendal nerve, encircling openings instead of moving bones. There is no record
for that series. Forcing them onto `ischiocaudalis` would have put six muscles on a
tail record because it is nearby.

**The first version of that park said no cited source addressed the perineum, and
that was wrong.** It was checked by grepping titles and `notes` in `sources.json`,
which is a weaker test than the claim it was used for. Grepping the extracted paper
texts the same day turned up two: **Osawa (1898) gives *Sphenodon* an *M. transversus
perinei* and an *M. sphincter cloacae***, and **Ercoli et al. (2012) describe an
ischiocavernosus and a bulbospongiosus in *Galictis cuja***. An outgroup and a
mammal, described independently, with nothing joining them — so the parks stand,
because a `sphincter-cloacae` record built on those two alone would assert a homology
neither author makes. What is missing is a comparative treatment, not a description.
The rows now say so, and name both papers.

Two more park as smooth muscle, following the Dartos row: the internal anal
sphincter and the detrusor. The internal sphincter is worth having for the contrast
Gest sets up by listing it beside the external one — the same opening closed by two
muscles of different tissue types on different nervous systems, one voluntary and
one not.

Three new elements, all soft: `perineal-body`, `anococcygeal-raphe`,
`perineal-membrane`. The perineal body takes six muscles from four directions and is
the busiest soft-tissue site in the human column.

Puborectalis is the odd row. Its origin is the pubis and its insertion is the
puborectalis of the other side, so it is scored `{"muscle": "iliocaudalis"}` —
ending on the record it is part of. That is what the muscle does: the sling behind
the rectum is two muscles meeting, and the anorectal angle it holds is why
continence is a skeletal-muscle problem.

### Upper limb, done — 51 of 52 filed

Fifty-four entries, fifty-two muscles after the interossei's double listing.
Twenty-seven rows added; one parked. This is the region the dataset was already
strongest in, and the pass was mostly a matter of splitting group rows into their
members, which is where the attachments were being lost: `supracoracoideus` carried
both fossae and both facets in one union, so nothing said which muscle used which.

**Serratus posterior superior and inferior are the find.** Gest lists them in the
upper limb region — they are met in the back dissection — and gives both **ventral
rami**, calling them respiratory muscles embryologically related to the intercostals
rather than to the deep back. They are filed on `hypaxial-musculature`, not on any
epaxial record. A muscle's address is not its address.

**Deltoid gets no row of its own, and cannot.** Gest has one entry; this dataset
splits it into `deltoideus-clavicularis` and `deltoideus-scapularis`, and the
extraction key is `(species, source, name, region)`, which the validator requires to
name exactly one record. That is the case its comment describes and the fix is
already in place — the two halves carry names that tell them apart. The three
origins Gest gives are on the two rows between them.

Three per-muscle rows record something the group rows could not:

- **Flexor digitorum profundus takes two nerves**, median to the radial half and
  ulnar to the ulnar half, **and the lumbricals arising from its tendons split the
  same way**. A nerve boundary running through one muscle, inherited by another that
  grows off its tendons.
- **The first palmar interosseous is often fused with adductor pollicis**, which
  this dataset scores on `contrahentes-digitorum`. One human muscle straddling two
  records, on the source's own statement.
- **Extensor pollicis brevis and abductor pollicis longus share a record because
  they share an origin field on the radius**, not because they make the borders of
  the snuffbox together. The clinical grouping and the homological one agree here by
  accident, and the row says which is doing the work.

**Palmaris brevis is the one parked row**, on `homology` rather than `no-record`:
two records could take it and nothing in this table chooses. `flexores-breves-super-
ficiales` already names it as a candidate for that layer and is scored *uncertain* in
a human because of it, so filing it there would settle by fiat the question that
record's own note says is open. The other candidate is the dermal musculature — a
muscle that ends in skin is doing what a panniculus carnosus does.

### Lower limb, done — 51 of 53 filed

Fifty-eight entries, one of them a cross-reference (`peroneus mm.`), four of them
the alphabetical listing repeating itself: 53 muscles. Thirty-seven rows added, two
parked.

Almost every call here was already made and written down by whoever wrote the group
rows, and the pass is mostly the work of acting on notes that named muscles they
could not score. Three of them are worth restating because they cut against the
obvious grouping:

- **Fibularis tertius goes with the long extensors, not with the fibularis group
  whose name it carries.** Gest puts it in the anterior compartment on the deep
  fibular nerve while longus and brevis are lateral-compartment muscles on the
  superficial fibular nerve. The `fibularis-group` record's assessment already said
  the innervation cut against the name; the row is what acting on that looks like.
- **Pectineus has two nerves and that is the whole interest of it.** Femoral and the
  anterior division of the obturator — one from the dorsal divisions of the plexus
  and one from the ventral — so a muscle lying in the ventral adductor mass is
  supplied in part from the dorsal side. It stays on `adductor-femoris`, where the
  existing row already put it in prose.
- **The gemelli end on another muscle.** Both insert on the obturator internus
  tendon and neither reaches the femur, so both rows are scored
  `{"muscle": "ischiotrochantericus"}` — filed on `puboischiofemoralis-externus`,
  ending on a record they are not part of. Their nerves come from either side of
  that boundary: superior takes the nerve to obturator internus, inferior the nerve
  to quadratus femoris.

**Quadriceps femoris gets no row**, for the same reason deltoid does not: it is one
Gest entry spanning `extensor-iliotibialis` (rectus femoris) and `femorotibialis`
(the three vasti), and the extraction key must name one record. The rectus crossing
the hip and the vasti not is the tell, and both rows say so.

**Sartorius parks on `homology`,** which preserves a decision rather than making
one. `ambiens` scores it absent with the argument — Diogo & Molnar reject the
'ambiens'-to-sartorius equation because the 'ambiens' is a dorsal muscle in a ventral
position — while `puboischiofemoralis-internus` carries the competing derivation in
its synonyms and does not act on it either. Parking holds the attachments without
choosing.

**Lumbricals of the foot parked on `no-record`, and that was an omission rather
than a judgement.** `lumbricales` is a hand record and a row's region must equal its
record's, so the four pedal lumbricals had nowhere to go, while every other intrinsic
group in this dataset was already doubled — `flexores-breves-superficiales-pes`,
`contrahentes-digitorum-pes`, `extensores-digitorum-breves-pes`,
`abductor-digiti-minimi-pes`. **`lumbricales-pes` was created on 2026-08-20 and the
row is promoted**, which is the whole point of parking: the reading was on the page
and cost nothing to file once the record existed.

One new element, `knee-capsule`, for the articularis genu: a few fascicles deep to
vastus intermedius that stop at the capsule instead of running on to the patella,
and pull it clear as the knee extends. The smallest thing in this dataset that still
counts as a muscle, and the only one ending on a joint capsule.

### Head and neck, done — 79 of 83 filed

A hundred and five entries and 83 muscles; 22 of the entries are the alphabetical
listing giving one muscle both orderings of its name. Seventy-five rows added, four
parked. The largest region, and the one where the dataset's records are at their
finest and its coverage was at its thinnest: `cranial` attachment coverage went from
42% of present occurrences to 50%, and the number of cranial records carrying any
attachment at all from 27 of 51 to 46 of 51.

**Eleven facial-muscle records had no attachments for any species.** Diogo et al.
(2009) gave `zygomaticus-major`, `orbicularis-oculi`, `buccinatorius`, `mentalis`,
`occipitalis`, `platysma-myoides`, `auricularis-posterior`,
`levator-anguli-oris-facialis` and the rest a human occurrence apiece and no origin
or insertion anywhere on the record. Gest's are the first. That is the shape of gap
a comparative survey leaves and a dissecting-room table fills, and it is the
argument for holding both.

The facial muscles with no record of their own — risorius, the two depressors, the
levators of the upper lip, corrugator, procerus, the nasalis group, frontalis — go
to `interhyoideus`, the ancestral hyoid-arch sheet, which is where that record's
human row already lumped them and named five as parts. Thirteen more join them with
their attachments.

Four things worth keeping:

- **The tensor tympani row is the mammalian middle ear written as jaw anatomy.**
  `articular` and `malleus` are one element here, so the row records a muscle on the
  mandibular trigeminal pulling on the bone that was the reptilian jaw joint. It
  stays on `adductor-mandibulae` following Diogo et al. (2008) against Gest, who
  puts it on the mylohyoid — which is why the part carries `membership: "disputed"`
  and names the other claimant.
- **Three records got their first human row**: `vocalis`, `musculus-uvulae` and
  `cricoarytenoideus-lateralis`. The last is the one whose only occurrence was the
  cheetah deleted in August 2026, on a note written about a human. That reading is
  now filed under the animal it was made in, which is what the deletion promised.
- **The eyelid is opened by an eye muscle and closed by a face muscle.** Levator
  palpebrae superioris is on `extraocular-muscles` because it takes the oculomotor
  nerve; orbicularis oculi is on its own facial-nerve record. Two fields, two
  nerves, one eyelid.
- **The prevertebral muscles are the mirror of the suboccipital ones.** Rectus
  capitis anterior runs atlas-to-occiput on the *ventral* ramus of C1 and rectus
  capitis posterior minor runs atlas-to-occiput on the *dorsal* ramus of the same
  nerve. Same two bones, a few millimetres apart, and they land on
  `hypaxial-musculature` and `epaxial-musculature` respectively. Nothing but the
  nerve separates them.

Four parked, all smooth muscle, all following the Dartos row: trachealis, the
ciliary muscle, and the sphincter and dilator pupillae. The iris pair is worth
having parked rather than dropped — antagonists driven by the two divisions of the
autonomic system, and the ciliary muscle is why a third-nerve palsy takes
accommodation and the pupil along with the eye movements.

Nine new elements for the head: `mastoid-process` (from the back region),
`galea-aponeurotica`, `auricle`, `alisphenoid`, `auditory-tube-cartilage`,
`palatine-aponeurosis`, `pterygomandibular-raphe`, `epiglottic-cartilage`,
`vocal-ligament`. `alisphenoid` carries a `possibly-corresponds-to` edge to
`epipterygoid`: the mammalian greater wing of the sphenoid is widely held to
incorporate the ossified epipterygoid, nothing cited here demonstrates it, and if it
holds then the lateral pterygoid and tensor tympani arise from a bone a lizard
carries as a strut of its jaw suspension.

## The accounting closes

**239 distinct muscles in `muscles_alpha.html`: 222 filed, 17 parked, none dropped.**

Five entries are filed as their halves and are worth naming so the arithmetic can be
checked. `epicranius` and `occipitofrontalis` are frontalis plus occipitalis;
`quadriceps femoris` is rectus femoris plus the three vasti; `deltoid` is the
clavicular plus the scapular deltoid; `digastric` is the anterior belly on
`intermandibularis` plus the posterior belly on `depressor-mandibulae`.

**Each spans two records, and until 2026-08-20 that meant no row at all.** The
extraction key `(species, source, name, region)` has to resolve to one record, so
the five commonest names in the table — a clinician would use every one of them —
were unfindable. They now have `covers` rows: no observation of their own, the
halves still carrying it, and the word resolving to both. Searching *digastric*
returns the intermandibularis and the depressor mandibulae, and each card names the
other.

**The seven regional files were parsed and checked against the alphabetical one.**
They carry 283 names between them and not one that the alphabetical table lacks, so
the first pass's claim that they are subsets — made without testing — holds. The
check costs a minute, and this repository's own experience is that an untested claim
in a reading note is the least reliable thing in it.

### The name-disagreement warning was firing on one source

`validate.py` warned whenever a (record, species) occurrence carried more than one
name, on the reasoning that which label a reader sees should not be an accident of
merge order. That is right when two studies disagree. It is wrong when **one** source
uses several names for a group this dataset lumps, which is the normal case and
exactly what per-muscle rows produce: Gest alone puts five names on
`intercostales-interni` and four on `hypaxial-musculature`. The check now requires
the names to come from different sources. It dropped 16 warnings, and 9 of them
predate this pass — Prikryl's two iliacus rows, Liparini's PIFI 1 and 2, and the
anuran adductor pairs were all being reported as synonymy disputes with themselves.

**Do not paste the table's prose into `data/`.** It is a copyrighted teaching
resource; paraphrase the attachments into element rows as everywhere else, and let
the citation carry the rest.
