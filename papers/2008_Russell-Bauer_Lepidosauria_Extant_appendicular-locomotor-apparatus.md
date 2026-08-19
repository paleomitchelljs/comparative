# Russell & Bauer (2008) — The appendicular locomotor apparatus of *Sphenodon* and normal-limbed squamates

*Biology of the Reptilia* **21** (Morphology I), ch. 1, pp. 1–465. Society for the
Study of Amphibians and Reptiles. Volume co-editors Gaunt and Adler.

Source key: `russell-bauer-2008`.

## What was acquired, and what was not

The Gans Collections and Charitable Fund released all 22 volumes free at
[carlgans.org](https://carlgans.org/biology-reptilia-full-content/). The viewer
serves **one PDF per page**:

```
https://carlgans.org/wp-content/bor/21/BotR21-page{N}.pdf
```

`N` is the PDF page. **The offset for this volume is +5** — chapter page 1 is
`page6`, chapter page 5 is `page10`.

**The PDF in `papers/` is 222 pages, not the whole 465-page chapter.** Only the
myology and the synonymy appendix were fetched, because the osteology and the
locomotion chapters are not what this dataset scores:

| chapter pp. | PDF pages | what |
|---|---|---|
| 192–208 | 197–213 | VIII. General Aspects of Myology — nomenclature, homology, subdivision, architecture |
| 209–319 | 214–324 | IX. Myology of the Forelimb — axial muscles acting on the girdle, then intrinsic |
| 320–394 | 325–399 | X. Myology of the Hindlimb — thigh, crus, pes |
| 404–422 | 409–427 | Appendix B. Synonymy List of Muscles of the Locomotor System |

Not fetched: I–VII (introduction, classification, limb orientation, development,
locomotion, and both osteology sections, chapter pp. 1–191), Appendix A
(phalangeal formulae), and the references. **Page 1 of the local PDF is chapter
page 192.** Any page reference taken from this file must be read off the running
head, not off the PDF page counter.

Fetched at ~1 s intervals with each file checked by `file` before it counted:
222 requested, 222 returned as PDFs, 0 Cloudflare interstitials. The host does
return a "Just a moment…" HTML page under HTTP 200 when hammered, which is why
the check exists.

## The finding that matters before anything is scored

**The descriptive baseline of this monograph is *Iguana iguana*, not a
generalised lizard.** Every muscle account opens with a paragraph keyed
`Iguana:` giving that animal's origin and insertion, and only then a
`General discussion:` surveying the literature across genera. There are **74
such `Iguana:` paragraphs** and about 65 distinct muscle headings across the
forelimb and hindlimb.

This is exactly the check the base-layer rule exists to force, and here it comes out
the *opposite* way to the four cases catalogued there: the paper does name an
animal, and it is one already in `species.json`. `iguana-iguana` currently
carries **7 rows**. Nearly the whole appendicular musculature of that species is
in this file.

**Sphenodon is a different matter.** It is named 114 times, but in the
`General discussion:` paragraphs — Russell & Bauer are reporting Perrin (1895),
Osawa (1898), Miner (1925) and Haines rather than dissecting a tuatara
themselves. `sphenodon-punctatus` has been in `species.json` with zero rows
waiting for this paper, and it will only partly be filled by it: tuatara rows
must be scored where the text states the tuatara condition and attributed to
whoever observed it, not taken as this paper's own observations.

**Do not attribute anything here to *Timon lepidus*.** That is Abdala & Diogo's
exemplar, and 27 of the 36 unscored lepidosaur rows sit on it. Those rows are
not closed by this acquisition; a second, differently-named column is.

## Muscle headings present

Forelimb: episternocleidomastoideus, trapezius, serratus anterior (+
superficialis), levator scapulae, episternohyoideus, omohyoideus,
sternocoracoideus internus and externus, costocoracoideus, latissimus dorsi,
subcoracoscapularis, scapulohumeralis posterior and anterior, clavodeltoideus,
scapulodeltoideus, humeroradialis, triceps complex, pectoralis, supracoracoideus,
coracobrachialis complex (longus + brevis), biceps brachii, brachialis anticus,
extensor digitorum longus, supinator longus, extensor carpi radialis and ulnaris,
anconaeus quartus, supinator manus, flexor digitorum longus, flexor carpi
radialis and ulnaris, pronator teres, epitrochleoanconeus, pronator accessorius,
pronator profundus, extensores digitores breves (superficialis et profundi),
flexores digitores breves, abductor digiti quinti, lumbricales, interossei
ventrales and dorsales.

Hindlimb: iliofibularis, iliofemoralis, iliotibialis, femorotibialis, quadriceps
femoris, ambiens, puboischiofemoralis internus and externus, puboischiotibialis,
flexor tibialis internus and externus, caudifemoralis longus and brevis,
ischiotrochantericus, adductor femoris, pubotibialis, peroneus longus and brevis,
tibialis anterior, femorotibial and femoral gastrocnemius, popliteus, interosseus
cruris, adductor et extensor hallucis et indicus, adductor digiti quinti, flexor
hallucis, contrahentes, interossei plantares.

## Appendix B is a second deliverable

The synonymy list carries **656 numbered synonym references**, each keyed to a
numbered bibliography of about a hundred works — Alix 1874, Brooks 1890,
Fürbringer 1870, Camp 1923, Davis 1934 and so on. This dataset's whole premise is
that the literature has no stable nomenclature, and this is the largest
name-to-name concordance for the lepidosaur locomotor system in the
bibliography. It belongs in `synonyms` fields, not in occurrence rows.

Russell & Bauer also reprint Davis's (1936) seven guidelines for muscle naming —
never publish a new name without saying it is new, never rename without reason,
do not name specialised slips of a parent muscle separately — and then note that
few authors have followed them, which is why the synonymy list is as long as it is.

## Measured density

477 attachment statements over the 222 acquired pages, 2.1 per page. That is
lower than a short focused paper such as Matsuoka & Hasegawa (5.9) because most
of the text is comparative discussion rather than description — but the
description that is there is per-muscle, per-animal, and states both ends.
