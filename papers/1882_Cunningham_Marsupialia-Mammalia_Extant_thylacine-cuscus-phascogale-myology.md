# Cunningham (1882) — Anatomy of the Thylacine, Cuscus and Phascogale

*Report on the Scientific Results of the Voyage of H.M.S. Challenger*, **Zoology
5, part XVI**: 1–192, 13 plates. Received 28 March 1882.

Source key: `cunningham-1882`. English, 192 pages.

## What was acquired

`https://www.19thcenturyscience.org/HMSC/HMSC-Reports/Zool-16/` — David Bossard's
2004 electronic edition, prepared from Dartmouth's holdings. The HTML pages are
page images, but each page also exists as a one-page PDF at
`PDFpages/NNNN.pdf` **carrying an OCR text layer**, which is what made this
mineable. Printed page number equals PDF page number, offset zero. Pages 1–149
were fetched; 150–170 are thoracic viscera and genito-urinary organs and 171–192
are plate explanations, none of which this dataset scores.

The OCR is Victorian-typeface OCR and misreads accordingly — *Phcscoçjale*,
*tUl)erOsity*, *cla'cricular*, *Juscus* for *Cuscus*. It is legible throughout
but nothing should be quoted from it without checking the page image.

## The animals

Cunningham received all the marsupials the *Challenger* brought home: four
*Phalangista vulpina*, three *Dasyurus viverrinus*, two *Thylacinus
cynocephalus*, one *Phalangista maculata*, one *Phascogale calura*. He chose the
thylacine, the cuscus and the phascogale for full description.

| his name | scored as | limbs described |
|---|---|---|
| Thylacine, *Thylacinus cynocephalus* | `thylacinus-cynocephalus` | fore and hind |
| Cuscus, *Phalangista maculata* | `spilocuscus-maculatus` | fore and hind |
| Phascogale, *Phascogale calura* | `phascogale-calura` | **fore only** |
| Vulpine phalanger, *Phalangista vulpina* | `trichosurus-vulpecula` | hand and pes only |
| *Dasyurus viverrinus* | `dasyurus-viverrinus` | hand and pes only |

**The phascogale has no hindlimb rows because it has no hindlimb data.** Its
pelvis and hind limbs were "so shattered with shot that it was impossible to
conduct a proper examination". Leaving the rows out is the correct reading of
that; scoring `present: "no"` would not be.

He also states his dissection counts for the hand: four of the thylacine's, two
of the cuscus's, one of the phascogale's. That is why the within-species
variation he reports is nearly all in the thylacine.

## Structure

| pages | what |
|---|---|
| 1 | introduction and the specimen list |
| 2–31 | myology of the anterior limb (forearm 13, intrinsic hand 19, nerves 26) |
| 32–47 | myology of the hind limb (gluteal 32, hamstrings 35, calf 40, shin 44) |
| 48–139 | **intrinsic muscles of the mammalian pes**, comparative |
| 140–149 | nerves of the hind limb |
| 150–170 | thoracic viscera, genito-urinary organs |

## Why it was worth mining

Theria was a placental column — human, rat, four cats, a grison, a vole. This is
its first marsupial data, and `monodelphis-domestica` had been sitting in
`species.json` with nothing on it. **153 rows mined**, the second-largest
single-source pass in the dataset after Gest's human tables, and the largest that
is a dissection rather than a teaching table.

Its second value is that the three animals disagree with each other and
Cunningham says which is which, so the rows carry contrast rather than
repetition. His running concordance against Macalister, Owen, Meckel, Haughton,
Young and Cuvier & Laurillard's plates covers the wombat, koala, Tasmanian devil,
both kangaroos, wallaby, bandicoot, brushtail possum and opossum — none of them
scorable from here, but all of them recorded in the notes as what the reported
range looks like.

## The observations that made it into rows

- **The thylacine's clavicle is a vestige**, a two-inch curved rod embedded in the
  cephalo-humeral muscle with no attachment to the acromion, joined to the
  sternum only by an ill-defined raphe. Its subclavius has left the bone
  entirely: from the first costal cartilage it straps over the humeral
  tuberosities and ends in the fascia over the supraspinatus. Cunningham agrees
  with Macalister that this "sterno-scapular" is a variety of the subclavius.
- **The teres minor is absent in the phascogale, on nerve evidence.** He looked
  for the part of the infraspinatus that might represent it and could trace no
  twig of the circumflex nerve into any of it — the same criterion that
  identified the muscle in the other two.
- **The extensor carpi ulnaris is two muscles in the male thylacine and one in
  the female.** Scored `variable` for that reason, from two dissections of the
  same species by the same worker.
- **The extensor brevis digitorum is caught mid-migration.** Ruge had traced it
  from a wholly fibular peroneal muscle in monotremes to a wholly pedal one in
  man. The thylacine's is still entirely on the fibula in three bellies; the
  cuscus's has landed the index and medius portion on the dorsum of the foot and
  left the outer two digits' portion on the bone.
- **The peroneus longus straddles Ruge's sequence too.** The thylacine keeps the
  primitive slight attachment to the base of the fifth metatarsal; the cuscus's
  tendon lies free in its sheath with no attachment but the first metatarsal.
- **No osseous patella in either the thylacine or the cuscus** — the quadriceps
  and sartorius form a tendinous expansion Cunningham compares to fibrocartilage.
  Noted on the element, which stays scored present for Theria as a clade.
- **The flexor brevis digitorum has left the foot in the cuscus**, arising from
  the flexor longus hallucis while still in the leg, and Cunningham settles the
  identification by nerve: a recurrent branch of the internal plantar, where the
  deep portion beside it takes the internal popliteal.
- **The cuscus has a plantar cartilage instead of a heel** — a plate in the sole
  replacing the plantar fascia, taking the plantaris tendon behind, fixed to the
  cuboid laterally and to a sesamoid gliding on the internal cuneiform medially,
  each of those giving origin to short digital muscles.
- **There is no musculus accessorius in the foot of either animal**, stated in a
  footnote and scored `present: "no"` on `flexor-accessorius-lateralis-pes`, whose
  human row is the quadratus plantae.
- **The cuscus's adductor longus is absent, identified by a nerve**: the obturator
  nerve lies on the superficial aspect of the adductor brevis, which it could not
  do if the longus were in front of it.

## Disagreements recorded, not resolved

- **The gemelli.** Cunningham puts them with the obturator internus, into whose
  tendon they insert and in whose groove it runs; this dataset's
  `puboischiofemoralis-externus` synonymy puts them with the obturator externus
  and quadratus femoris. His rows are on `ischiotrochantericus` and both records
  carry the note.
- **The agitator caudae.** Caudal transverse processes to posterior femur — the
  attachments of a caudofemoralis — but Cunningham groups it with the gluteus
  maximus on plane and shared nerve, and describes a separate piriformis in the
  same two animals. Both cannot be the caudofemoralis.
- **The gluteus quartus** is scored a `disputed` part of `iliofemoralis` on
  Cunningham's own authority: he could not make out its nerve supply, says its
  homologies cannot be considered established until that is done, and adds that
  though usually grouped with the gluteals it seems closer to the extensors.
- **The gracilis and the marsupial bone.** Macalister reported the gracilis
  attached to the epipubic bone in every marsupial he examined; in neither of
  Cunningham's two is it attached at all.

## Skeletal consequence

`epipubis` gained Theria and Monotremata. That groups the turtle epipubic
cartilage with the mammalian epipubic bone on position, which is the usual
reading but is not demonstrated by either source on the element — flagged as a
working decision in `docs/GAPS.md` §3, with Reilly & White (2003) named as the
unmined source that bears on it.

## Not mined

**Pages 48–139, the comparative pes**, and pages 140–149, the hindlimb nerves.
The pes section is a survey of the intrinsic foot muscles and plantar nerves
across some two dozen mammals — echidna, platypus, dingo, cat, puma, badger,
polecat, walrus, otter, *Myrmecophaga*, *Dasypus*, *Hyrax*, *Elephas*,
*Bathyergus*, *Pteropus*, *Macacus*, *Pithecia*, *Lemur*, plus his own three
marsupials and *Dasyurus* — six of the feet supplied to him by the Challenger
Commission and the rest from Edinburgh's anatomical museum. It is the only
dissection in this bibliography that puts monotreme and marsupial foot muscles on
the same page, and it would land on records this dataset already has
(`abductor-et-extensor-digiti-i-pes`, `abductor-digiti-minimi-pes`,
`contrahentes-digitorum-pes`, `flexores-breves-profundi-pes`).

**Two of his muscles have no record to land on**: the pedal lumbricales, and his
*ischio-femoral*, which he explicitly declines to call the quadratus femoris.
Both are in `docs/GAPS.md` §2.
