# Sánchez, Rafasquino & Portiansky (2019) — Forearm and hand of three South American felids

*Journal of Morphological Sciences* 36(1). doi:10.1055/s-0039-1681016
Source key: `sanchez-etal-2019`

## Why it was reached for, and the species it was pinned to

Hand and forearm are the two largest occurrence counts in the dataset. Seven pages,
measured **3.3** origin/insertion mentions per page — `MINING.md` called it "short but
dense" and that is exactly right, because almost every statement is a **comparison
between three named species**, which is what a species-keyed base layer exists for.

It had the wrong animal. `attribute_species.py` mapped it to *Felis catus*, which
appears in the paper **twice, as a comparison**. Its animals are *Panthera onca*,
*Leopardus pardalis* and *Leopardus geoffroyi* — three species added, and the third of
these mapping errors found this session after Sigurdsen's *Rhinella* and McKitrick's
`gavia-sp`.

**Forearm 55% → 58%. Theria 86% → 88%.** Nine rows.

## What a three-species paper buys that a one-species paper cannot

Three of the nine rows exist only to hold a disagreement:

| Character | Jaguar | Ocelot | Geoffroy's cat |
|---|---|---|---|
| palmaris longus tendons | **5** | 5 | **4** |
| lateral digital extensor bellies | **1** | 2 | **2**, medial splitting again |
| abductor digiti I longus origin | more proximal | more proximal | **less proximal** |

A division count that differs between three species of one family is something a
Theria row could not have held at all — it would have had to pick one and demote the
others to prose, which is the exact failure the species migration was for.

**One assumption is flagged rather than asserted.** Sánchez et al. do not say which
digit loses its tendon in Geoffroy's cat's four-tendon palmaris longus. The parts are
named on the assumption it is the first — the usual pattern of loss in the carnivoran
manus — and the `divisionNote` says so.

## Where a felid forearm is not bone

- The **palmaris longus** ends on the *tendons of the flexor digitorum superficialis*
  at the proximal middle phalanx, not on bone.
- A third of the **abductor digiti I longus** origin is on the *interosseous
  membrane*, so the osteological correlate understates the muscle.
- The **brachioradialis** tendon carries past the distal radius onto the *proximal row
  of the carpus*, which this record's consensus does not reach.

## The one observation a dry specimen could confirm

In the jaguar the flexor digitorum profundus belly carries **two sesamoid bones**.
Everything else here is soft-tissue dissection; that is the single character that
would survive in a museum skeleton.

## Why the hand region did not move

Coverage went up in **forearm** and not in **hand**, because the paper's hand content —
tendon counts, digital extensor tendons, insertions on the distal phalanges — sits on
forearm-region records: `palmaris-longus`, `extensor-digitorum`,
`flexor-digitorum-longus`, `abductor-pollicis-longus`. The intrinsic manus records
(`flexores-breves-profundi`, `contrahentes-digitorum`, `intermetacarpales`,
`lumbricales`) are untouched and are still the floor at 47%. **A forelimb paper is not
automatically a hand paper**, and this one is a forearm paper with tendons in the hand.

## Still in it

The pronators and the supinator, for which the paper gives development rather than
attachments — the jaguar's supinator is a flat belly spiralling around the proximal
radius from a short tendon on the lateral annular ligament, and that ligament has no
element here. Table 1's measurements, which are architecture-adjacent but are lengths
rather than the mass, fascicle length and PCSA the `architecture` block wants. And the
ocelot and Geoffroy's cat for every muscle where the paper reports "no relevant
differences" — which is most of the flexors, and which would be scoring by inheritance
rather than by observation.
