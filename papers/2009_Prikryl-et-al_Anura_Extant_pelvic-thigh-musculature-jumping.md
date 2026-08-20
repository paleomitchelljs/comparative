# Prikryl, Aerts, Havelková, Herrel & Roček (2009) — Pelvic and thigh musculature in frogs and the origin of anuran jumping locomotion

*Journal of Anatomy* 214: 100–139.
Source key: `prikryl-etal-2009`

## Why it was reached for

Anura sat at 23% with its pelvis and thigh unscored, and this paper was already in
`papers/` and already cited on those very rows — for their names. Table 1 is a
review of every pelvic and thigh muscle with an origin, an insertion and a
function, and the descriptions go finer. **Anura went 23% → 35%.**

## Taxa and material — the thing to know before planning around it

**Nine anuran species were dissected, not one**, plus three caudates as an outgroup
baseline and one further frog for a stimulation experiment:

| | |
|---|---|
| Anura | *Rana esculenta*, ***Discoglossus pictus***, *Bombina orientalis*, *Bufo guttatus*, *Pelobates fuscus*, *Xenopus laevis*, *Ascaphus truei*, *Barbourula busuangensis*, *Pipa pipa* |
| Caudata (outgroup, dissected) | *Necturus*, *Ambystoma*, *Salamandra salamandra* |
| Function only (stimulation) | *Pyxicephalus adspersus*, one subadult male |

*Discoglossus* is the baseline **because** *Rana*, the usual model, is highly
derived — and "description of other species is confined to differences from the
basic scheme observed in *Discoglossus*". Those differences sections are
first-hand observations of eight more frogs, each running several pages.

**The dataset holds three of the thirteen animals** as of 2026-08-20 — see below.
The remaining ten are the largest single piece of unmined reading in this source
and not a hard problem: the sections are short and explicitly framed as differences
from a baseline that is now complete. *Xenopus laevis*, *Necturus maculosus* and
*Ambystoma mexicanum* are already in `species.json`; the rest need adding.

## Re-mine of 2026-08-20 — *Discoglossus pictus* complete

**Table 1 lists 25 muscles. All 25 are now filed or parked.**

| | |
|---|---:|
| Muscles in Table 1 | 25 |
| Carried by a filed row | 19 |
| Parked, `record: null` | 6 |
| **Rows in the file** | **22** |

Nineteen rather than twenty-five filed rows because five records take two of the
paper's muscles each — iliacus externus + internus on
`puboischiofemoralis-internus`, cruralis + glutaeus maximus on
`extensor-iliotibialis`, gracilis major + minor on `puboischiotibialis`,
semimembranosus + semitendinosus on `ischioflexorius`, adductor longus + magnus on
`adductor-femoris` — and the caudal musculature row is an absence.

**The previous pass scored 12 of the 25** and its note listed four records as "not
scored". The four were real but the count was not: thirteen muscles were missing,
including every axial-to-pelvis muscle and both obturators.

### Added this pass

Filed: **coccygeosacralis** (`epaxial-musculature`), **coccygeoiliacus**
(`iliocaudalis`), **pyriformis** (`caudofemoralis`), **caudalipuboischiotibialis**,
**adductor longus** and **adductor magnus** (`adductor-femoris`), **sartorius**
(`pubotibialis`).

Two of those are worth calling out. **`caudalipuboischiotibialis` had exactly one
species, *Taricha torosa***; the frog and the salamander turn out to agree on a
muscle that ends inside another muscle, at the tendinous inscription of the
semimembranosus. And the **pyriformis is filed on the caudofemoralis on the
source's own synonymy** — Prikryl et al. give Francis's (1934) *caudalifemoralis*
for it — with the urostyle standing in for a caudal series that Anura does not
have, `caudal-vertebrae` being recorded absent in this clade.

Parked, with what would settle each on the row: **iliolumbaris** (axial-to-pelvis,
no record holds that), **tensor fasciae latae** (ends in fascia, no skeletal
insertion), **obturator externus** and **obturator internus** (both plausible parts
of records they cannot be shown to belong to), and **quadratus femoris** and
**gemellus**, which Prikryl et al. state were *not recognised as independent
muscles* in this animal. The last two are parked negatives: there is no record for
either muscle, so the absence cannot yet be filed as `present: "no"`, and the rows
exist to keep the observation.

### A correction to the previous pass

Eight rows opened "Discoglossus **and Ascaphus**, from Prikryl et al.'s review
table and descriptions" — two animals cited on rows sitting in a file whose name
declares one. The attachments are the *Discoglossus* condition; the provenance line
now says so. *Ascaphus* gets its own file when the other twelve animals are mined,
which is what the filename convention exists to force.

### An internal contradiction, kept

Table 1 runs the **coccygeoiliacus** from the urostyle to the iliac shaft. The
description runs it the other way — origin on the medial surface of the dorsal
crista of the iliac shaft, insertion on the ventrolateral urostyle. The rows follow
the description, being the more detailed statement, and the row records that the
table disagrees. This record's consensus happens to follow the table.

## The finding

**Five of the muscles insert on the knee aponeurosis rather than on bone.** Cruralis,
glutaeus maximus, gracilis major and minor, semitendinosus and the iliofibularis
all end in that sheet; the glutaeus maximus does not even reach it directly but
attaches to the fascia of the distal cruralis. The tensor fasciae latae, added this
pass, ends in fascia at both the fascia lata and never touches the femur at all.

A large part of the anuran thigh therefore leaves **no osteological trace at its
distal end**. That is a hard constraint on reconstructing fossil anuran thighs
from bone, and it belongs beside Leavey et al. (2024) in `METHODS.md` on what
correlates can and cannot do.

The iliofemoralis is the exception and the one to teach from: **tuber superius →
crista femoralis**, a named process at each end.

## Four elements added by the earlier pass

| Element | Why |
|---|---|
| `tuber-superius` | Dorsal prominence of the iliac shaft. Three muscles originate on it — iliofibularis and iliofemoralis share its posterolateral surface, glutaeus maximus takes the dorsolateral. Flagged `correlate` |
| `crista-femoralis` | Carries the iliofemoralis insertion. Flagged `correlate` |
| `knee-aponeurosis` | The finding above needed somewhere to point |
| `tibiofibula` | Added as `fusedFrom: [tibia, fibula]`, never `partOf` either, so an anuran-vs-other comparison reads as a skeletal fusion and not as a muscle moving — the tarsometatarsus precedent |

## Nomenclature, which is the point of the record

The occurrence names carry a tangle this paper documents: the muscle Prikryl et
al. call the **pectineus** is Hoffmann's and Iordansky & Morozov's
*puboischiofemoralis externus* — and Noble's *puboischiofemoralis internus*, so the
literature disagrees about which of the two it is, not merely what to call it.
Their **semimembranosus** is Hoffmann's *ischioflexorius* and Francis's
*caudalipuboischiotibialis*; their **semitendinosus** is Mivart's *ischioflexorius*
and Hoffmann's *puboischiotibialis*; their **gracilis major** is Mivart's
*puboischiotibialis*; their **sartorius** is Stannius's *gracilis* and Mivart's
*pubotibialis*. Two muscles share four names between them, and the same words mean
different muscles again in the mammalian literature.

**That is why the sartorius is filed on `pubotibialis`** — on the equivalence the
paper itself publishes, not on the resemblance of a name. Every source term is now
in `data/mapping/prikryl-etal-2009.json`, which is where the synonymy can be read
on its own.

## Still not scored

`gastrocnemius` and `tibialis-anterior` are leg muscles the paper's table does not
reach. Resolution is coarse throughout: Table 1 gives "Ilium", "Ischium", "Femur"
without a side for many muscles, and **no side is invented where the source gives
none** — several rows are deliberately thinner than they could be made to look.

## *Ascaphus*, *Rana* and *Xenopus* added, 2026-08-20

Four animals of thirteen. **Ten records now carry three or four frogs**, which is the
first time this dataset can show within-clade variation in the anuran hindlimb
rather than one exemplar.

*Ascaphus* is described in full rather than as differences, so it gets 18 rows;
*Rana* is written as differences from *Discoglossus* and gets 13.

### What having three frogs immediately settles

**The gemellus and quadratus femoris are not absent from anurans.** Prikryl et al.
could not recognise either as an independent muscle in *Discoglossus*; both are
fully formed in *Ascaphus* and in *Rana*, with attachments. So the *Discoglossus*
condition is the odd one, and the parked negatives on that file now have two
positives to be read against. All three remain parked — there is no `gemellus` or
`quadratus-femoris` record, and the mammalian gemelli are a contested part of
`puboischiofemoralis-externus` — but the case for filing them is now three frogs
strong rather than nil.

**The quadratus femoris and obturator externus are one field.** They are
continuous in *Ascaphus*, continuous in *Rana* (separated only by the origin of
the ventral head of the semitendinosus), and inseparable in *Discoglossus*. Three
animals saying the same thing.

**The obturator internus reaches the femur in *Ascaphus* and not in
*Discoglossus*.** That matters because the *Discoglossus* row was parked precisely
because the muscle ended on the joint capsule and so did not match
`ischiotrochantericus`, whose consensus insertion is the proximal femur. The
*Ascaphus* condition does match. Filing one and not the other would split a muscle
across two treatments on the strength of one frog, so both wait — but the reason
for waiting is now recorded on both rows.

### Two homology arguments the paper makes with its own anatomy

- **The tuber superius of *Discoglossus* is the posterior end of the dorsal crista
  of the iliac shaft in *Rana*** — Prikryl et al. identify it by the fact that the
  same three muscles arise there, the iliofibularis, iliofemoralis and glutaeus
  maximus. The *Rana* rows carry the landmark on that reasoning.
- **In *Ascaphus* the sartorius and semitendinosus are a single muscle mass**, two
  heads separated by a shallow cleft, both arising from fascia and inserting by one
  tendon. This dataset files the two on different records — `pubotibialis` and
  `ischioflexorius` — so the row is parked on `division`, which is exactly what
  that `blockedBy` value is for. Splitting the observation would assert a division
  the animal does not show.

### Where the two frogs differ from the baseline

Neither is a minor variant. In *Ascaphus* the coccygeoiliacus and coccygeosacralis
are one fan-like layer, the iliofibularis reaches bone where in *Discoglossus* it
ends in the aponeurosis, both gracilis muscles reach bone, and the pectineus takes
part of its origin from the rectus abdominis. In *Rana* the sartorius arises from
the ilium rather than the ischium, the adductor magnus wraps around the femur to
insert dorsally, and the dorsal crista of the ilium is palpable through the skin —
an external landmark for an internal muscle boundary.

### Two elements this animal needed

`epipubic-cartilage-anuran` and `dorsal-fascia-anuran`. The first pass at *Xenopus*
scored only the iliac end of three attachments for want of somewhere to put the
other end, which was the wrong call and is now the worked example in
[`MINING.md`](MINING.md#never-drop-an-attachment-for-want-of-somewhere-to-put-it):
a new element plus a `possibly-corresponds-to` edge records the observation and the
open homology question at once, where dropping the attachment records neither.

`epipubic-cartilage-anuran` carries a `possibly-corresponds-to` edge to
`epipubic-cartilage`, which is **not** mammalian — it is the turtle and lepidosaur
anterior pubic cartilage, and the case for calling the anuran structure the same
thing is positional and undemonstrated, exactly as `epipubic-cartilage` and
`epipubic-bone` already stand to each other. Prikryl et al. also use *praepubis*
for what may be the same structure and do not say whether it is; the rows follow
the paper term by term and the element's note records the question.

`dorsal-fascia-anuran` carries the whole origin of two muscles here — the outer of
the three iliacus externus layers, from the ligamentous plate thickening its
posterior margin, and the latissimus dorsi. Both had been unscored.

### *Xenopus laevis* — the most divergent of the four

Its **iliacus externus is in three layers**, the outermost arising not from bone
but from a ligamentous plate in the dorsal fascia that crosses to its counterpart
on the other side. Its **coccygeosacralis is absent**, and in its place is a short
unnamed muscle from the descending ilium to the cartilaginous epipubis — parked,
because no record holds an ilium-to-epipubis muscle, but **scored at both ends**. Its **rectus abdominis reaches
the femur**, and its **latissimus dorsi ends on two thigh muscles** — which is why
a pelvic-and-thigh paper describes a shoulder muscle at all.

It also bears on *Ascaphus*: de Sá & Hillis (1990) report partial fusion of the
sartorius and semitendinosus in *Xenopus* and *Silurana*, and *Ascaphus* has the
two completely fused. **The same complex in a pipid and in the basal-most frog** is
worth checking before either is treated as diagnostic of anything.

## Complete, 2026-08-20 — every animal filed

**`remined`. 138 rows across ten extraction files: 109 filed, 29 parked.**

| File | Filed | Parked |
|---|---:|---:|
| *Discoglossus pictus* (baseline) | 16 | 6 |
| *Barbourula busuangensis* | 15 | 4 |
| *Caudata* (generalised) | 13 | 0 |
| *Ascaphus truei* | 12 | 6 |
| *Bufo guttatus* | 10 | 2 |
| *Rana esculenta* | 10 | 3 |
| *Pelobates fuscus* | 9 | 1 |
| *Pipa pipa* | 9 | 2 |
| *Xenopus laevis* | 8 | 3 |
| *Bombina orientalis* | 7 | 2 |

**The three caudates are one file, not three.** Prikryl et al. dissected *Necturus*
(3), *Ambystoma* (3) and one adult *Salamandra salamandra*, and then wrote the
result as a caudate pattern — the text opens "In all caudates" and each muscle
carries figure references to all three at once. That is a clade description, not
three specimens, so it goes on `caudata-generalised` with every row
`speciesBasis: "generalised"`, which is what `MINING.md` prescribes and what the
validator enforces. Where they *do* separate the animals the rows say so: the
tendinous inscription in the puboischiotibialis is present in *Necturus*,
*Ambystoma*, *Salamandrella* and *Taricha* and **absent in *Salamandra***.

***Pyxicephalus adspersus* yields no rows and should not.** It appears once, as one
subadult male under deep anaesthesia in a stimulation experiment used to confirm
the functions inferred from attachments. No myology is described for it. It is not
in `species.json` and does not need to be.

### What the whole set is for

The caudate file is the outgroup the other nine are read against, and it makes the
anuran departures legible: a trunk of fish-like myomeres against a rigid trunk and
a rod; separate tibia and fibula against a tibiofibula; an ischioflexorius reaching
the **plantar aponeurosis** against one stopping at the knee. Prikryl et al. chose
the neotenic caudates deliberately, as the best available proxy for the aquatic
temnospondyl ancestors of frogs.

Across the nine frogs the same handful of muscles keep moving, and the rows now
carry it:

- **The obturator externus and quadratus femoris are one field.** Seven frogs say
  so — continuous, confluent, fused, or inseparable — and in *Pelobates* the
  **gemellus joins them**, all three sharing one origin. Still parked, because no
  `quadratus-femoris` or `gemellus` record exists, but this is as strong as
  comparative evidence gets short of a homology treatment.
- **The sartorius and semitendinosus fuse repeatedly and independently**: one mass
  in *Ascaphus*, partly fused in *Xenopus* and *Silurana* (de Sá & Hillis 1990),
  incompletely separated in *Barbourula*. Three lineages, so the complex is not
  diagnostic of any of them.
- **The pyriformis is absent in every *Pelobates* specimen** and present in
  *Discoglossus*, *Ascaphus* and *Barbourula* — an asserted absence, filed as one.
- **The tuber superius is not required for its own muscles.** *Pelobates* lacks it
  and the glutaeus maximus, iliofibularis and iliofemoralis arise in the typical
  place anyway; *Rana* and *Bombina* have Prikryl et al. identifying it in two
  different structures purely by which three muscles arise there.

### Two elements and one species record this set needed

`lung` — because *Pipa*'s **pulmonum proprius runs from the dorsolateral surface of
the lungs to the dorsal femur**, a viscus-to-limb muscle Dunlap (1960) also figured.
Parked for want of a record, but scored at both ends. Carried on the same footing
as `dorsal-fascia-anuran` and `knee-aponeurosis`: not skeletal, but a muscle
demonstrably attaches to it.

`caudata-generalised` — see above.

**Use plain `pdftotext`** if reopening this paper; the section headings are
`Genus species (Figs N–1 and N–2)`.
