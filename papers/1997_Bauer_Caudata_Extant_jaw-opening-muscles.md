# Bauer (1997) — Visceral jaw-opening muscles of urodeles

*Journal of Morphology* 233:77–97. Source key: `bauer-1997`

## Why it was reached for

Ziermann & Diogo (2013) flagged the **ceratomandibularis** as genuinely variable
across urodeles — distinct in some obligate neotenes, fused to the branchiohyoideus
and/or the depressor mandibulae in others, missing altogether in others — and this
paper is about it. **The dataset had no record for it**, so the muscle Bauer spends 21
pages on had nowhere to be.

Measured **3.5** origin/insertion mentions per page against the 3.6 recorded — the
closest the density figure has come this session. *Necturus maculosus* is his fully
described adult; *Triturus vulgaris*, *Taricha torosa* and *granulosa*,
*Notophthalmus viridescens*, *Hydromantes italicus*, *Euproctus asper* and three
*Triturus* species are treated comparatively.

**Cranial 57% → 58%, Caudata 76%, and a 127th muscle record.** (Both figures moved again on 2026-08-20; see below.)

## The new record

`ceratomandibularis` — hyoid arch, CN VII, origin on the anterior surface of the first
ceratobranchial. Bauer's argument for its arch identity is neurological: the facial
nerve puts it in arch 2 with the depressor mandibulae, and **against the branchial
muscles it lies among**.

Its interest is that **it opens the jaw by pulling against the hyobranchial apparatus
rather than against the skull.** Two CN VII jaw openers, two different anchors — which
is why the urodele jaw-opening system cannot be read as one muscle, and why this is
the counterexample to "jaw opening is the depressor mandibulae".

## A muscle that reaches its bone indirectly

Most of the ceratomandibularis inserts onto the **hyomandibular ligament**, together
with the depressor mandibulae posterior, and so reaches the gonial only *indirectly*.
Two elements were added to keep that distinction scoreable:

- `gonial`, the small posterior bone of the urodele lower jaw that every jaw opener
  here ends on — scoring them on `mandible` would have lost Bauer's point;
- `hyomandibular-ligament`, which belongs with the shark's midventral raphe and the
  loon's humeral feather tract as a muscle end that leaves no osteological trace.

Two fibre bundles of the ceratomandibularis fuse with the depressor mandibulae
posterior outright, and its ventralmost fibres reach the caudal surface of the
upturned dorsal ceratohyal.

## A muscle boundary that exists at the surface and not in depth

Bauer reports something no earlier worker did: the deep fibres of the
ceratomandibularis **intermingle** with those of the ceratohyoideus externus in two
places — caudally where both attach to the ceratobranchial, and rostrally near the
posteroventral ceratohyal — while superficially the two are thoroughly separate. And
the muscle is partly split by the fascia of origin of the interhyoideus posterior,
whose medial layer pierces it.

That observation is why the record's `openQuestion` asks whether the urodeles reported
to *lack* the ceratomandibularis have lost it or merely fused it. At the level of gross
dissection the question may not have a clean answer.

## Two divisions in one dataset column

`depressor-mandibulae` is now `divided` for *Necturus* — anterior and posterior — and
`single` for the axolotl, where Ziermann & Diogo find the levator hyoideus integrated
into an undivided muscle. Same record, same clade, two states, both from a named
animal. Bauer traces the DMA/DMP names to the constantly divided depressor of adult
bolitoglossine plethodontids, all of which develop directly, and 'depressor
mandibulae' itself to Humphry (1871), who applied it to only the caudal part of the
muscle in a metamorphosed *Andrias*.

## Three earlier descriptions corrected, and none of them scored

- **No fibres on the parietal**, against Fischer (1864).
- **No origins on the neck vertebrae**, against Ruge (1897).
- Kesteven (1942–45) put the whole depressor mandibulae posterior insertion on the
  ceratohyal; Bauer finds that condition among urodeles **only in *Siren***.

All three are in the `attachmentNote` rather than as rows, which is the point of
having a note: the corrections are as much a part of the record as the attachments.

## ~~Still in it~~ — finished 2026-08-20, and the file had 1 animal of 12

The note above named what was left and the answer was most of the paper. **Bauer's
Materials and Methods lists 12 species across four families** — *Hydromantes
italicus*; *Necturus maculosus*; *Euproctus asper*, *Notophthalmus viridescens*,
*Salamandra salamandra*, *Taricha granulosa*, *T. torosa*, *Triturus cristatus*, *T.
helveticus*, *T. karelini*, *T. marmoratus*, *T. vulgaris* — and this file held
*Necturus*. **A paper that describes N animals should produce N columns**, which is
the rule `MINING.md` says is broken most often, and this is the second source in two
days to break it.

**Now: 10 adults and 3 larval columns filed, 18 rows, nothing parked, `remined`.** Nine species
added to `species.json`. Caudata attachment coverage 76% → 79%, cranial 51% → 52%.

### Four of these muscles had never been described

*Taricha granulosa*, *Triturus helveticus*, *T. karelini* and *T. marmoratus* —
Bauer says so of the first three outright, and *T. karelini*'s case is nomenclatural:
it was a subspecies of *T. cristatus* until the 1980s, so the older literature has
nothing under that name. First descriptions are the rows most worth having and the
easiest to leave in a paper, because a comparative section reads like commentary.

### What the ten columns are actually for

The genus *Triturus* is the reason to score them separately rather than write "the
salamandrid condition":

| Species | Squamosal | Occipito-otic | Cucullaris relation | Insertion |
|---|---|---|---|---|
| *T. vulgaris* | only | — | none | gonioarticular |
| *T. helveticus* | yes | posterior + deep fibres | — | common tendon of all fibres |
| *T. karelini* | yes | caudal fibres | **deep to ventral cucullaris fibres** | gonioarticular |
| *T. marmoratus* | yes | posterior + deep fibres | none | **single short tendon, all fibres** |

Three of the four take occipito-otic fibres that **Özeti & Wake (1969) did not
mention**, which is a correction to the standard reference on salamandrid jaw muscles
and is invisible unless the four animals are separate rows.

### Negatives, which is what this paper is unusually good at

- ***Notophthalmus***: Kesteven's split of the muscle into anteromedial and
  posterolateral parts **could not be detected** — the very division Bauer does find
  in *Salamandra* and *Hydromantes*.
- ***Taricha torosa***: Smith's (1927) posterior slip from the dorsal fascia was not
  confirmed by Özeti & Wake, by Kesteven, or by Bauer. Three failures to find a
  described slip.
- ***Hydromantes***: **no origin from the quadrate**, against L. Adams (1942), who
  gave the whole anterior muscle to that bone; and **no attachment to the gonial**,
  which every salamandrid here has.

### Two muscles that arise off other muscles

*Salamandra*'s superficial slip comes off the fascia cephalodorsalis over the epaxial
musculature, and *Hydromantes*'s entire depressor mandibulae posterior does — **no
skull attachment at all**. Both are scored as attachments onto `epaxial-musculature`,
because a fascia over a muscle is that muscle's surface. So a plethodontid has two
jaw openers pulling from two anchors, one cranial and one axial, which is the same
functional split the ceratomandibularis makes in *Necturus* against the hyobranchial
apparatus.

### ~~The larvae are parked~~ — filed 2026-08-20, and they are why `stage` exists

Bauer's Results open with larvae and state that *Salamandra salamandra*, *Triturus
cristatus* and *T. vulgaris* show **no noteworthy differences among their depressor
muscles**. The larval muscle is two separate muscles where the salamandrid adult's is
one, and an occurrence carried no ontogenetic stage — so a larval row would either
collide with the adult row on `division` or stand in for the species. Six rows parked
on `occupied` for want of one field.

**The field exists now.** An occurrence is one per (record, species, *stage*), and
these six are the rows it was added for. *Salamandra salamandra* carries two rows on
`depressor-mandibulae`: **larval, `divided`, two separate muscles**, and **adult,
`heads`, two slips of one**. That transformation is the paper's subject and the
dataset could not hold it a day ago.

*Triturus cristatus* is now a larval column and nothing else, which is exactly right
— Bauer describes its larva and takes his adult *Triturus* from four other species.

The larval posterior muscle is the one to read: anterior fibres from the squamosal,
posterior fibres **from the fascia of the anterior muscle itself** — scored as an
attachment onto this same record — converging with it onto the ligamentum
hyomandibulare. A jaw opener that arises partly off its own partner, and the same
ligament most of *Necturus*'s ceratomandibularis inserts on, so two muscles of two
different arches share a tendon and neither reaches the mandible directly.

The larval posterior muscle is the one to read: anterior fibres from the squamosal,
posterior fibres **from the fascia of the anterior muscle itself**, converging with it
onto the ligamentum hyomandibulare. A jaw opener that arises partly off its own
partner.

### Still not in it

*Proteus*, whose simple ceratomandibularis is the neotene comparison the Discussion
turns on — Bauer discusses it from Drüner and Eaton rather than dissecting it, so it
would be an `after:` row on somebody else's observation and is left.
