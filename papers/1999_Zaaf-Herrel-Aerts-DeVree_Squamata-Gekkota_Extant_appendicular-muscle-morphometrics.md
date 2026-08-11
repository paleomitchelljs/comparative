# Zaaf, Herrel, Aerts & De Vree (1999) — Morphology and morphometrics of the appendicular musculature in geckoes with different locomotor habits

*Zoomorphology* 119:9–22.
Source key: `zaaf-etal-1999`

## Why this one second

Lepidosauria was the largest remaining taxon gap after Ercoli et al. (2012) — 62
unscored occurrences — and the forearm and hand were the largest region gaps.
Tables 2 and 3 give an explicit origin and insertion for **every** fore- and
hindlimb muscle, which is rare: most of the lepidosaur column came from Abdala &
Diogo's cross-taxon survey, which tabulates presence far more than attachment.

**Lepidosauria went from 29% to 53%.** Forearm 24→31%, hand 19→24%, and the
dataset overall from 39% to 43%.

## Sample, and why it needs saying twice

Two species, two specimens each:

- ***Eublepharis macularius*** — ground-dwelling, the base column in both tables
- ***Gekko gecko*** — a specialised climber, recorded as *differences from* the
  base column

Every row scored here is *Eublepharis*, with the *Gekko* difference carried in
`attachmentNote`. That structure is worth preserving because several of the
differences are **attachment differences between two geckos**, which is a direct
warning about reading any single lizard as Lepidosauria:

| Muscle | *Eublepharis* | *Gekko* |
|---|---|---|
| extensor carpi ulnaris | mainly the **ulnare** | restricted to the **pisiform** |
| latissimus dorsi | proximal **dorsal** humerus | shifted to the **lateral** humerus |
| ischiotrochantericus | **proximal** edge of trochanter | **distal** edge |
| extensor digitorum brevis | distalmost phalanx | antepenultimate phalanx |

Two of those are a different bone, not a different part of one. The dataset's
`variable` machinery exists for exactly this, and the shift diff will read them as
real moves if the second species is ever scored as its own column.

## Scored (21 occurrences)

**Forelimb (13):** `deltoideus-scapularis`, `latissimus-dorsi`, `brachialis`,
`supinator`, `extensor-digitorum`, `extensor-antebrachii-carpi-ulnaris`,
`flexor-carpi-ulnaris`, `flexor-carpi-radialis`, `flexor-digitorum-longus`,
`abductor-pollicis-longus`, `extensores-digitorum-breves`,
`flexores-breves-superficiales`, `abductor-digiti-minimi`

**Hindlimb (8):** `extensor-iliotibialis`, `ischiotrochantericus`,
`puboischiotibialis`, `ischioflexorius`, `tibialis-anterior`, `fibularis-group`,
`popliteus`, `flexores-breves-superficiales-pes`

Two name mappings worth recording, because both are the sort of thing this
dataset exists to make legible:

- **M. extensor ossis metacarpi pollicis → `abductor-pollicis-longus`.** The
  squamate name and the mammalian name for one muscle.
- **M. popliteus → `popliteus`,** whose Lepidosauria occurrence is named
  *interosseus cruris* after Abdala & Diogo. Same tibiofibular muscle, two
  literatures.

## Not scored, and why

- **The whole axio-appendicular series** — protractor pectoralis, serratus
  anterior, levator scapulae, costocoracoideus, scapulohumeralis anterior and
  posterior, teres major. Table 3 begins at the muscles inserting on the humerus
  and does not cover the girdle-to-axial-skeleton muscles.
- **`brachioradialis`.** Zaaf et al. have *M. supinator longus*, which some
  authors equate with the brachioradialis. That is a homology claim the table does
  not make, so both supinators went to `supinator` and `brachioradialis` stays
  unscored.
- **`tibialis-posterior`.** Not in Table 2. The nearest candidates — *M. pronator
  profondus* and *M. flexor tarsi* — would each be an assertion.
- **`puboischiofemoralis-internus` / `-externus`.** Not among the muscles Table 2
  lists as inserting on the femur.
- **The intrinsic hand and foot groups** beyond the three scored —
  `contrahentes-digitorum`, `flexores-breves-profundi`, `lumbricales`,
  `intermetacarpales`, `dorsometacarpales`, `abductor-pollicis-brevis`, and their
  pedal counterparts. *Mm. interossei dorsales* are listed with **no origin or
  insertion at all** ("well developed, see Russell 1975"), and mapping *Mm.
  interossei plantares* onto `flexores-breves-profundi-pes` would be a homology
  call the table does not support.
- **Tables 4–6, the morphometrics.** Mass, mean fibre length, physiological
  cross-section and pennation angle for the major limb muscles of all four
  specimens. **This is real architecture data in the schema's sense** — unlike the
  proportional masses in Omura et al. (2014) or Ercoli et al. (2012) — and would
  be the first for any lepidosaur. It is not entered yet: the `architecture` block
  is per-occurrence with one species, and these are two species with two specimens
  each and a locomotor contrast that is the paper's actual point. Entering it well
  means deciding how the schema holds an intraspecific pair, which is a design
  question, not data entry.

## Caution

Geckoes are not generalised lizards. *Gekko gecko* is a specialised climber with
adhesive toepads and *Eublepharis* is a ground-dwelling eublepharid; the paper's
purpose is the contrast between them. These rows sit in a Lepidosauria column
otherwise built on varanids, *Iguana* and Abdala & Diogo's survey, and where they
disagree with those, the disagreement is between families and not evidence that
one is wrong.
