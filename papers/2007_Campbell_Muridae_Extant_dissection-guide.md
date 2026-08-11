# Campbell — Rat dissection guide

Teaching handout, 15 pp. Not peer reviewed.
Source key: `campbell-2007`

## What it is for here

Not evidence. **Vocabulary.** The homology records were built from the comparative
literature — Abdala & Diogo, Diogo & Molnar, Ercoli et al. — which names the
mammalian shoulder in Latin partes. A student holding a rat is reading a handout
that names the same muscles in the split-word register of the North American
dissection lab, and none of those words were in the index:

```
clavotrapezius     MISS        acromiodeltoid     MISS
acromiotrapezius   MISS        spinodeltoid       MISS
spinotrapezius     MISS        cleidobrachialis   MISS
```

Every one of those now resolves. They were added as **occurrence-level synonyms
on the Theria rows**, following the file convention of naming the author with the
name, because a name belongs to a taxon-specific occurrence and not to the
homology group.

## What was added

| Lab name | Record | Theria occurrence name it attaches to |
|---|---|---|
| clavotrapezius, acromiotrapezius, spinotrapezius | `protractor-pectoralis` | Trapezius (+ sternocleidomastoideus) |
| acromiodeltoid, cleidobrachialis (+ clavodeltoid, clavobrachialis) | `deltoideus-clavicularis` | Deltoideus, pars acromialis and pars clavicularis |
| spinodeltoid | `deltoideus-scapularis` | Deltoideus, pars scapularis (spinous part) |
| pectoralis minor | `pectoralis` | Pectoralis major / pectoralis profundus |

`clavodeltoid` and `clavobrachialis` are added unattributed: they are the same
muscle under commoner spellings, but this handout uses *cleidobrachialis*, so
only that one carries the citation.

## The one that was a trap

The guide lists an **epitrochlearis**: a thin medial sheet of the upper arm that
*extends* the forearm. Search was already returning a hit for it — the
**epitrochleoanconeus**, which runs from the medial epicondyle to the olecranon
over the ulnar nerve. Two letters apart, different muscles, and the match was a
word-prefix accident rather than a homology statement.

No source held here establishes what the lab epitrochlearis is homologous to, so
it gets no record and no synonym. A disambiguation note now sits on the
`epitrochleoanconeus` Theria occurrence so the false lead is caught at the point
a reader would follow it.

## Still missing, and why

The cat-specific set has no source in this corpus:

- **xiphihumeralis** — the deepest pectoral division in the cat. Not in a rat.
- **levator scapulae ventralis** — cat; the rat guide does not name it.
- **epitrochlearis** as a scored muscle — see above.
- **cutaneous maximus / panniculus carnosus** — named in the guide, but the
  dataset has no cutaneous muscle record at all and adding one would need a
  homology assessment this handout cannot supply.
- **gluteus superficialis** — named in the guide. The dataset maps *gluteus
  medius* and *minimus* onto `iliofemoralis`; where the superficial gluteal
  belongs is a real question in Diogo & Molnar and is not settled by a lab sheet.

The nearest thing to a cat source in `papers/` is Schlough's mustelid guide,
which is a scan with no text layer and cannot be extracted automatically.

## Caution

A dissection guide is a naming authority for one animal and nothing more. Nothing
in this file was used to score presence, attachment, division or homology, and
the `role` field in `sources.json` says so.
