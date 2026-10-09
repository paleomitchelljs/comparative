# Teaching materials

Handouts built from, but not part of, the dataset. Nothing here is read by
`scripts/build.sh` or by the app, and nothing here is generated — these are
written documents; the build never touches them.

| File | What it is |
|---|---|
| `skull-id-guide.tex` | Beginner's skull identification cheat sheet. The document. |
| `skull-id-figures.tex` | Its figures. TikZ schematics, plus guarded includes for the clipped plates. |
| `clip-plates.py` | Clips the literature plates out of the local PDFs into `plates/`. |
| `plates/` | Clipped figures. **Git-ignored.** Never committed. |

## Building

```sh
cd docs/teaching
latexmk -pdf skull-id-guide.tex
```

**The handout no longer includes the literature plates** — every figure in it is
a TikZ schematic drawn here, so `clip-plates.py` is not needed to build it. The
script and the plate list are kept because the plates are still the best
comparative images available for these clades, and `\plate{...}` is still
defined in `skull-id-figures.tex` if you want any of them back.

`python3 clip-plates.py --list` prints the plate list with sources and licences
without touching anything.

## Why the plates are not committed

Same reason `papers/` is not. The PDFs are copyrighted; this repository is
public; `.gitignore` excludes them globally. A figure clipped out of a paper is
more of the source's own expression than a sentence of its text is, so the rule
in the root `CLAUDE.md` — paraphrase and cite, never paste — applies to figures
at least as strongly.

What is committed is the *recipe*: `clip-plates.py` records which figure, from
which paper, on which page, under which licence, and what it is good for.
Anyone with the PDFs can reproduce the plates in one command; nobody without
them receives redistributed content.

The plates currently used are all openly licensed, and the credit lines the
guide prints are a condition of those licences:

| Plate | Source | Licence |
|---|---|---|
| tuatara, turtle temporal terminology | Werneburg & Preuschoft (2024) *Anat. Rec.* 307:1559–1593, fig. 1 | CC BY-NC 4.0 |
| skull morphotypes on a tree | same paper, fig. 18 | CC BY-NC 4.0 |
| pigeon skull, lateral and dorsolateral | Jones, Button, Barrett & Porro (2019) *Zool. Lett.* 5:17, fig. 3 | CC BY 4.0 |

CC BY-NC permits classroom and repository use but **not** commercial
redistribution, so do not fold these into anything sold. If that ever matters,
the two Werneburg plates are the ones to replace.

## What the compilation does not have

`papers/` is a **myology** library. It was assembled to mine muscle
attachments, and it is thin on exactly what a skull osteology handout wants:
labelled lateral views of a salamander, frog, caecilian, lizard, snake,
crocodilian or mammal skull. A scan of every figure caption in the extracted
text turned up eleven papers with any skull-in-view figure at all, and most of
those are muscle plates using the skull as a backdrop.

So the guide's schematics are drawn here. If the compilation
grows a comparative osteology source — a *Biology of the Reptilia* skull
volume, Romer's *Osteology of the Reptiles*, a lissamphibian skull atlas —
that is the gap to fill first, and `clip-plates.py` is where the new plate
goes.

## The guide and `data/skeleton.json`

They overlap and do **not** agree, and the guide is deliberately not generated
from the data.

`skeleton.json`'s `presence` field was built to answer *is there a bone here
for this muscle to attach to*, from muscle-anatomy sources. It is not a skull
character matrix, and several of its cranial entries are wrong or
unsourced if read as one:

- `nasal` is `absent: [aves]`; birds have nasal bones.
- `parasphenoid` is `present: [actinopterygii]` only; lissamphibians and most
  non-mammalian tetrapods have a large one.
- `supraoccipital` and `basisphenoid` are `default: yes` with no exceptions;
  salamanders lack the supraoccipital and no lissamphibian has a separate
  basisphenoid.
- `jugal` and `postorbital` are `absent: [theria]` (and `aves`); all three
  lissamphibian orders lack them too.
- `jugal`, `nasal`, `postorbital`, `prefrontal` and `quadratojugal` carry no
  `sources` at all.

None of that is a defect in `skeleton.json` for the job it does. It matters
only if a skull interactive is ever driven off it — see `docs/ROADMAP.md`
and the notes in the session that added this directory.
