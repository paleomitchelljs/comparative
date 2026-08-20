# Hattori & Tsuihiji (2021) — Homology and osteological correlates of pedal muscles among extant sauropsids

*Journal of Anatomy* 238: 365–399. doi:10.1111/joa.13307. Open access, PMC7812136.

## Why it was reached for

It ranked first when the density check in `MINING.md` was run over the whole
backlog at once rather than one paper at a time: 9.7 origin/insertion mentions per
page over 35 pages. The dataset had been citing it for four years and had three
scored rows out of it. A citation is not a mining, and this is the paper that made
the point.

It is also the first source in the corpus to give one region in **all four extant
sauropsid clades at once**. Everything else covers one clade well, and the foot had
been assembled a column at a time.

## The animals

Seven, dissected, two per clade except Testudines: *Iguana iguana* and *Varanus
indicus*; *Chelydra serpentina*; *Paleosuchus palpebrosus* and *Crocodylus
porosus*; *Gallus gallus* and *Grus japonensis*. Origin, insertion, innervation and
an osteological correlate for each of 26 pedal muscles.

**Two animals per clade, and the sameness is data.** Where the paper describes
*Iguana* beside *Varanus* and records no difference, that is an observation of
sameness in two animals rather than a description of one, so both get rows — the
precedent is Zaaf's two geckos. Where they do distinguish, and they do for the
tibialis anterior origin and the short extensor slips in the two squamates, the
rows differ.

## The homology revision, which is the point of the paper

The classical assignments of the anterior tibial muscles are **swapped**. Avian
*m. tibialis cranialis* is the homologue of the non-avian *m. extensor digitorum
longus*, and avian *EDL* of the non-avian *m. tibialis anterior*.

The argument is parsimony of attachment. The classical scheme — descending from
Romer (1923–27) and, they note, used uncritically by palaeontologists for a century
— requires the extensor digitorum longus origin to jump the knee joint and the
tibialis cranialis to lose its metatarsal I insertion. Theirs requires neither.

Worth flagging as a methodological disagreement rather than a result: Hattori &
Tsuihiji weight morphological and functional congruence **over innervation**, on
the grounds that nerve–muscle specificity is itself variable across taxa. That is
the reverse of the priority used elsewhere in this dataset. Both positions are
defensible and the dataset now holds both — `tibialis-anterior` and
`extensor-digitorum-longus-hl` are `contested`, and the *Struthio* rows stay
`uncertain` rather than picking a side.

Allen et al. (2021) independently corroborate it, equating the crocodylian extensor
digitorum longus with the avian *m. tibialis cranialis*. The two papers work on
different problems — homology versus moment arms — so the agreement is not
circular. The records stay `contested`; the balance of evidence has moved.

## A second revision, which needed a new record

The muscles running from one metatarsal onto the digit lateral to it have been read
as part of the short digital extensors in lepidosaurs and turtles (Walker 1973;
Russell & Bauer 2008). Hattori & Tsuihiji separate them: distinct slips, stout
tendons, a consistent origin one metatarsal medial to the digit of insertion, and
in crocodilians a distinct innervation.

Scoring them onto `extensores-digitorum-breves-pes` would reproduce the error they
correct, and `intermetatarsales` is a different muscle — metatarsal to metatarsal,
web-forming, lateral plantar nerve. Hence `interossei-dorsales-pes`.

## What it closed

46 occurrence rows across 6 records and 10 species, all leg and foot. Testudines
finally moved off 26%, and foot and leg became the two best-covered regions in the
dataset.

More than rows, it closed **osteological correlates**. `WORKLIST.md` tracks
correlates carrying no muscle; three of them close here. The avian tibialis
cranialis takes the cranial and lateral cnemial crests, and the avian *m. abductor
digiti II* takes the fossa metatarsi I. Those are landmarks a palaeontologist reads
first, and the dataset had said nothing about what pulled on them.

## §3.2.8, taken 2026-08-20 for a record that did not exist

The first muscle out of the plantar half, and it came off the back of the Gest human
re-mine rather than off this paper's own queue. Gest's four human pedal lumbricals
had nowhere to go — `lumbricales` is a hand record — so `lumbricales-pes` was
created, and this paper is what makes it a homology group rather than a place to put
a human muscle.

Hattori & Tsuihiji unify four sauropsid muscles on it: the lepidosaurian **mm.
lumbricales**, the testudine **m. flexor digitorum communis sublimis** of Walker
(1973), the crocodilian **mm. lumbricales**, and the avian **m. lumbricalis**. The
argument is the paper's usual one and is worth stating because it runs against the
names: an origin on or immediately beside the flexor plate of the long digital
flexors, an insertion plantarly on non-ungual phalanges, and tibial or plantar
innervation throughout. Walker's turtle name says *flexor digitorum*, and the muscle
is a lumbrical.

Three rows scored from their own dissections — *Iguana iguana*, *Varanus indicus*,
*Chelydra serpentina*. The two lepidosaurs carry the same two-bellied arrangement,
medial belly from the aponeurosis between the flexor digitorum longus tendons of
digits II and III onto digit III, lateral belly from the lateral margin of the digit
III tendon onto digit IV.

**The *Varanus* innervation is the row to read.** The plantar nerve supplies the
medial belly and the tibial nerve the lateral one — two bellies of one muscle in one
animal on different branches. Hattori & Tsuihiji say plainly that innervation is
plastic enough in both crocodilians and lepidosaurs that they rest this homology on
origin and insertion instead, which is the opposite weighting to Diogo & Molnar
(2014) and the reason this paper is worth reading beside them.

The avian and crocodilian descriptions in §3.2.8 are reported from Suzuki et al.
(2011), Vanden Berge (1975), Cracraft (1971), McGowan (1979) and Gangl et al. (2004)
rather than dissected here. They are not scored: under the `after:` rule they would
be filed under the workers who made them, and none of those papers is in this corpus.

## Not done

**The rest of the plantar half, §3.2 — 15 more muscles in the same structure.** This
pass took the dorsal half, §3.1.1 to §3.1.13, and §3.2.8. The remainder is still the
largest piece of scorable description left in any paper already in `papers/`.

## Relevance to comparative anatomy teaching

The cleanest example in the corpus of a homology argument decided on attachment
parsimony against a century of inherited nomenclature, with the losing reading kept
and named. Pair it with Allen et al. (2021) for independent corroboration from a
different method, and with Diogo & Molnar (2014) for the opposite methodological
weighting, where innervation carries the homology and attachment is the labile
character.
