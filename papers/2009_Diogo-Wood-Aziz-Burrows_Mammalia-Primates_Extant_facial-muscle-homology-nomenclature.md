# Diogo et al. (2009) — Primate facial muscles, and a nomenclature for Mammalia

## Citation

Diogo R, Wood BA, Aziz MA, Burrows A. 2009. On the origin, homologies and evolution
of primate facial muscles, with a particular focus on hominoids and a suggested
unifying nomenclature for the facial muscles of the Mammalia. *Journal of Anatomy*
215: 300–319. doi:10.1111/j.1469-7580.2009.01111.x

## Question

Facial muscles are hyoid muscles — everything supplied by cranial nerve VII — usually
attached to freely movable skin and responsible for facial expression. Where did the
primate set come from, how does it differ from other mammals', and can the names used
by human anatomists be reconciled with those used for non-human primates and
non-primate mammals?

## What it is

Dissections of various primate and non-primate taxa plus a literature review,
including photographs of the facial muscles of gibbons and orangutans not previously
published. Out of it comes a proposed unifying nomenclature for the facial muscles of
Mammalia, **and a list of more than 300 synonyms** used in the literature for these
muscles.

## Findings

The sequence through primates is one of small gains and losses rather than wholesale
reorganisation, and the paper is precise about each step:

- **Strepsirrhines** have basically the muscles present in non-primate mammals such
  as tree-shrews, except that they often have a depressor supercilii that tree-shrews
  usually do not differentiate, and lack two that tree-shrews usually do — the
  zygomatico-orbicularis and the sphincter colli superficialis.
- **Monkeys** such as macaques usually lack the sphincter colli profundus and the
  mandibulo-auricularis, which strepsirrhines often have, but differentiate several
  muscles that non-anthropoid primates usually do not: levator labii superioris
  alaeque nasi, levator labii superioris, nasalis, depressor septi nasi, depressor
  anguli oris and depressor labii inferioris.
- **Hominoids including humans** have a risorius, auricularis anterior and
  temporoparietalis that macaques typically lack; macaques in turn differentiate a
  platysma cervicale (undifferentiated in orangutans, panins and humans) and an
  auricularis posterior (undifferentiated in orangutans).

## What it gave this dataset

**Seventeen records, split out of `interhyoideus` on Table 1.** That record carried
the whole mammalian facial musculature as `parts` of one occurrence per taxon —
fifteen on *Rattus*, fourteen on *Homo*, seven on *Ornithorhynchus* — where this
paper resolves it muscle by muscle across ten mammals.

Table 1 is the deliverable. It reads cleanly as a page image at 210 dpi (PDF p. 3;
`pdftotext` returns only the 173 footnotes, which run over four further pages). Each
row is a homology hypothesis across *Ornithorhynchus anatinus*, *Rattus norvegicus*,
*Tupaia*, *Lepilemur ruficaudatus*, *Macaca mulatta*, *Hylobates lar*, *Pongo
pygmaeus*, *Gorilla gorilla*, *Pan troglodytes* and *Homo sapiens*, with counts in
the column headers: **10 facial muscles in the platypus, 20 in the rat, 24 in a
human.**

Taken, for the three mammals this dataset holds:

`platysma-cervicale` · `platysma-myoides` · `occipitalis` · `auricularis-posterior`
· `sphincter-colli-superficialis` · `sphincter-colli-profundus` ·
`cervicalis-transversa` · `interscutularis` · `zygomaticus-major` ·
`zygomaticus-minor` · `orbicularis-oculi` · `buccinatorius` · `orbicularis-oris` ·
`mentalis` · `dilatator-nasi` · `levator-anguli-oris-facialis` ·
`interhyoideus-profundus`

Each carries `descends-from` to `interhyoideus`, so the hyoid-sheet origin of the
facial musculature stays queryable rather than being dissolved by the split.

Three of those are worth noticing on their own. **`interhyoideus-profundus` has one
cell in the whole table** — the platypus — which makes it the clearest surviving
trace of the undivided hyoid sheet. **`sphincter-colli-profundus` is absent in
*Ornithorhynchus* but present in *Tachyglossus***, so it is a monotreme character
the platypus lacks rather than a therian innovation. And the **cervicalis
transversa of the platypus and the sternofacialis of the rat are one row**, so the
rat's name is the therian name for the platypus's muscle.

## What it did not give, and why

**No attachments.** This paper averages fewer than two origin/insertion mentions per
page, because facial muscles mostly end in skin and a muscle that ends in skin has
no osteological correlate. The seventeen records carry names, presence and homology
and nothing else. **The muscles most characteristic of the group are the ones this
schema can say least about** — that is a fact about the muscles, and the `%att`
figures fall accordingly rather than incorrectly.

An earlier version of this note gave a second reason to hold off: that the corpus
has no descriptive myology for a mammalian head. **That was not the blocker.** The
homology comes from Table 1 and needs no dissection here; the missing myology would
have supplied attachments, which this group largely does not have to give.

**The rows with arrows across them are not taken.** Where one muscle in the platypus
becomes several in a primate — the naso-labialis and its derivatives, the
maxillo-naso-labialis against the nasalis, the orbito-temporo-auricularis against
the frontalis and auriculo-orbitalis — the correspondence needs the footnotes read.
Those stay as `parts` on `interhyoideus`.

## Relevance to comparative anatomy teaching

The best available answer to a student who asks whether humans have "more" facial
muscles than other animals. They have some that most mammals lack, they lack some
that macaques have, and the ones they have differentiated are concentrated around the
mouth and the ear — but a macaque differentiates a platysma cervicale that an
orangutan, a chimpanzee and a human all leave undifferentiated. The pattern is
reshuffling, not accumulation.

Pair with **Diogo et al. (2008)** for where the whole field comes from — the reptilian
sphincter colli, itself an interhyoideus derivative — and with **Gest (Anatomy
Tables)** for the human muscles under their clinical names.
