# Ercoli, Echarri, Busker, Álvarez, Morales & Turazzini (2012) — Myology of the lumbar region, tail and hind limbs of the lesser grison

*Journal of Mammalian Evolution*. doi:10.1007/s10914-012-9219-9
Source key: `ercoli-etal-2012`

## Why this one first

It closed the largest single gap in the dataset. Before this pass Theria had 81
present occurrences and 12 with taxon-specific attachments — 15%, against a
salamander column at 69% — and the hindlimb, lumbar region and tail were the bulk
of what was missing. This paper gives an origin and an insertion for every one of
them in *Galictis cuja*, in the same descriptive register as Ercoli et al. (2014)
on the forelimb, so the therian column is now scored from one animal across both
limbs rather than from two unrelated exemplars.

**Theria went from 15% to 38%.** Region effects: leg 45→67%, thigh 43→57%,
foot 73→77%, pelvic 44→51%, axial 24→28%.

## Five of these rows were on a cheetah

A blind re-mining audit found that **`extensor-iliotibialis`, `femorotibialis`,
`adductor-femoris`, `ischioflexorius` and `gastrocnemius` carried this paper's
*Galictis cuja* prose on *Acinonyx jubatus* occurrences** — while the table below
listed all five as *Galictis*, so the note and the data disagreed. Ercoli et al.
name *Acinonyx* three times: once as a cursorial contrast, once as a Fig. 1 label,
twice in the references. The co-cited Hudson et al. (2011b) measures 1.5 O/I
mentions per page and cannot be the source of an attachment either.

The cause was `attribute_species.py` rule 2 taking the **first** single-species
source in the `sources` array, with `hudson-etal-2011b` ahead of
`ercoli-etal-2012` and both inside Theria. All five rows now name *Galictis cuja*
in their own prose, which is rule 1 and survives every rebuild.

## Scored (19 occurrences, all *Galictis cuja*)

| Record | *Galictis* muscle(s) |
|---|---|
| `puboischiofemoralis-internus` | iliopsoas (psoas major + iliacus) |
| `puboischiofemoralis-externus` | obturator externus, quadratus femoris, gemelli |
| `gluteus-maximus` | gluteus superficialis |
| `extensor-iliotibialis` | rectus femoris, tensor fasciae latae |
| `femorotibialis` | vastus lateralis, medialis, intermedius |
| `adductor-femoris` | adductor magnus, brevis |
| `ischiotrochantericus` | obturator internus |
| `puboischiotibialis` | gracilis |
| `ischioflexorius` | biceps femoris, semitendinosus, semimembranosus |
| `gastrocnemius` | gastrocnemius |
| `tibialis-anterior` | tibialis cranialis |
| `extensor-digitorum-longus-hl` | extensor digitorum longus |
| `fibularis-group` | fibularis longus, fibularis brevis |
| `popliteus` | popliteus |
| `tibialis-posterior` | tibialis caudalis |
| `flexor-digitorum-longus-hl` | flexor digitorum medialis |
| `flexores-breves-superficiales-pes` | flexor digitorum brevis |
| `transversospinalis` | transversospinalis, lumbar sector |
| `caudal-musculature` | sacrocaudalis series (dorsal/ventral, medial/lateral) |

## The two findings worth arguing about

**The caudofemoralis is absent in *Galictis*.** The record already carried
`present: "variable"` for Theria with the piriformis floated as a remnant. Ercoli
et al. looked in a carnivoran with a long, well-muscled tail — where a persistent
gluteofemoralis would be least surprising — and did not find one: "m.
gluteofemoralis (m. caudofemoralis) — this muscle is absent." In **three hind
limbs** the caudal part of the gluteus superficialis divided into extra bellies,
which they suggest "could be a remnant of this muscle". That is a **second
candidate, disagreeing with the piriformis proposal**, and it is now on the record
with both.

Two corrections a later audit made here. The occurrence read **`present:
"variable"`**, which is the *clade's* answer written onto one animal — the exact
error the rollup exists to prevent, and the same one `levator-anguli-oris` had.
It is `no` now, and Theria computes `variable` on its own if a therian disagrees.
And this note said **"three of six hind limbs"**: the paper gives no denominator.
Its methods name three specimens plus a fourth for additional observations, and
its largest stated count anywhere is "in four legs". Six was arithmetic, not
evidence.

**The semitendinosus takes origin from the tail.** Its caudal belly arises from
the transverse process of caudal vertebra 2, by aponeurosis from C1 and C3, with
only the second belly on the ischial tuberosity. A thigh muscle with a caudal
head is exactly the kind of thing the hamstring/caudofemoralis boundary turns on,
and it is why `ischioflexorius` now carries `caudal-vertebrae` as an origin row
alongside the ischium.

## Not scored, and why

- ~~**`iliocostalis` (lumbar).** Named and weighed, but a table interrupts the
  description in the PDF text layer and I could not read a clean origin and
  insertion.~~ **Now scored.** The table interleaves under `pdftotext` but both
  attachments read cleanly out of a `-layout` extraction once the column offset is
  accounted for — the obstacle was the tool, not the source, and this was the
  paper's **heaviest** muscle at 10.06% of hind limb muscle mass, with "heavy
  iliocostalis" among its headline functional characters. Note the direction: the
  **pelvic end is the origin** and the ribs are the insertion.
- **`longissimus-dorsi`.** The paper describes the lumbar epaxial sector as
  iliocostalis plus transversospinalis; it does not give a separate longissimus.
- **`contrahentes-digitorum-pes`, `flexores-breves-profundi-pes`.** The intrinsic
  plantar muscles are described under names I could not confidently map to these
  homology groups without asserting one. The foot record that *was* scorable
  (flexor digitorum brevis) is done.
- **Adductor longus.** Its origin is described positionally rather than by
  attachment in the passage available; magnus and brevis carry the row.
- **The percentage dry-mass table (Table 2).** Percentages of total hind limb
  muscle mass, not PCSA, fascicle length or absolute mass. Same call as Omura et
  al. (2014): it does not fit `architecture` and forcing it there would let a
  proportion be read as force.
- **Pelvic floor and tail-base muscles** — levator ani, pubocaudalis,
  bulbospongiosus, coccygeus, intertransversarii, interspinales. Real muscles,
  described here, with no records in this dataset and no cross-taxon assessment
  behind them. Adding them is a scoping decision, not a scoring one.

## Caution on the exemplar

*Galictis cuja* is a mustelid: an elongate, short-limbed, semi-fossorial
carnivoran. Several of these attachments will be carnivoran or mustelid
specialisations rather than therian generalities — the extensor digitorum longus
arising from the **femur** rather than the tibia is standard for mammals, but the
sacrocaudal origins of gluteus superficialis and sartorius are the sort of thing a
long-tailed animal has and a human does not. The rows are scored to Theria because
that is the operational taxon available; read them as "one therian, described in
full" rather than as the mammalian condition. The same caveat already applies to
the forelimb rows from Ercoli et al. (2014), which is the same animal's relatives.
