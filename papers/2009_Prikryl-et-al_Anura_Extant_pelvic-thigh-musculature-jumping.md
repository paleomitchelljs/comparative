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

**The dataset holds one of the thirteen animals.** That is the largest single piece
of unmined reading in this source and it is not a hard problem — the sections are
short and explicitly framed as differences from a baseline that is now complete.
*Ascaphus truei*, *Xenopus laevis*, *Necturus maculosus* and *Ambystoma mexicanum*
are already in `species.json`; the other seven would need adding.

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

The source stays `not-started`: one animal of thirteen is done.
