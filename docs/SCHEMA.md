# Data schema

Three kinds of file live in `data/`:

| File | Holds |
|---|---|
| `taxa.json` | Operational taxa and the topology that orders them |
| `sources.json` | Bibliography, keyed by `key` |
| `muscles-*.json` | Muscle records, split by anatomical region |

`scripts/validate.py` enforces everything below. Run it before committing.

---

## The central modelling decision

A muscle record is **not** a muscle in one animal. It is a **homology group** — a
hypothesis that a set of taxon-specific muscles correspond to one another — plus
the evidence for that hypothesis.

This matters because the same muscle carries different names in different
literatures, and the same name is applied to non-homologous muscles. The
coracobrachialis appears under six naming schemes across Abdala & Diogo's Table 1;
"gluteus maximus" names non-homologous muscles in the anuran and human
literature. A schema keyed on names would encode that confusion. Keying on the
homology group and treating names as attributes of taxon-specific occurrences
dissolves it.

So each record has:

- a **consensus** description — the generalised origin/insertion/action/innervation
- a list of **occurrences** — what the muscle is called and where it attaches in
  each taxon, with a per-row source
- a **homology** block — how well supported the grouping is, what is disputed,
  and what would settle it

---

## `muscles-*.json`

```jsonc
{
  "region": "Pectoral girdle and arm",     // required, file-level label
  "note": "...",                            // optional, file-level caveat
  "muscles": [ /* records */ ]
}
```

### Muscle record

| Field | Req | Notes |
|---|---|---|
| `id` | ✔ | kebab-case, unique across **all** muscle files |
| `name` | ✔ | Preferred name. Quote it (`"'Rhomboideus'"`) when the name itself is disputed |
| `region` | ✔ | One of `cranial fin pectoral arm forearm hand pelvic thigh leg foot`. Drives sort order and the region facet |
| `subregion` | | Free text, e.g. `"axio-appendicular"` |
| `mass` | | `dorsal` / `ventral` for limb muscles (the two fundamental limb-bud masses); `branchiomeric`, `somitic`, `somitic-axial`, `extraocular` for cranial |
| `layer` | | `superficialis` · `profundus` · `preaxial` · `postaxial` · `primaxial`. With `mass`, gives the four-cell classification (abductor/adductor × superficialis/profundus) that Mansuit & Herrel (2021) use to compare architecture across the whole fin-to-limb transition. Currently populated on `region: "fin"` records; see `docs/ROADMAP.md` phase 1 |
| `arch` | | Pharyngeal arch number, or a string like `"3–7"`. Cranial records only |
| `ancestralNode` | | Where the muscle first appears, e.g. `"LCA of extant gnathostomes"`. Fin records |
| `derivatives` | | `{pectoral: [], pelvic: []}` — muscle `id`s this ancestral fin muscle gave rise to. See below |
| `developmental` | | Embryonic origin. This is often the decisive homology evidence — state it when known |
| `synonyms` | | Every other name for this muscle, **with the author who used it**. These are indexed for search, so they are how a reader arrives from an old paper |
| `consensus` | | `{origin, insertion, action, innervation}` — the generalised description |
| `attachments` | | `{origin: [], insertion: []}` — normalised skeletal element names. Drives the Attachments view; keep the vocabulary consistent (`humerus`, not `Humerus` or `the humerus`) |
| `occurrences` | ✔ | See below |
| `homology` | | See below |
| `sources` | ✔ | Array of `sources.json` keys |

### Occurrence row

One per taxon, at most. Omit a taxon entirely if no source addresses it — that is
different from a source reporting absence.

| Field | Req | Notes |
|---|---|---|
| `taxon` | ✔ | An `id` from `taxa.json` |
| `present` | | `yes` (default) · `no` · `variable` · `uncertain` · `inferred`. Use `inferred` for fossil reconstructions and `variable` when a source reports it in some species of the clade and not others |
| `name` | ✔ if present | What this muscle is called **in that taxon's literature** |
| `origin`, `insertion`, `action`, `innervation` | | Taxon-specific values. Omit when they match the consensus — the UI falls back to it |
| `note` | | Where the interesting disagreement goes |
| `sources` | ✔ if present | Per-row citation. This is what makes a claim checkable |

`present: "no"` means *this source examined this taxon and did not find the
muscle*. It does not mean the muscle is absent from the clade. Abdala & Diogo
(2010) repeatedly document muscles present in one lizard and absent in another.

### Homology block

| Field | Notes |
|---|---|
| `confidence` | `well-supported` · `moderate` · `contested` · `uncertain`. Reflects the strength of support **reported in the sources**, not your own view |
| `notes` | The assessment. Name the authors who disagree |
| `openQuestion` | What is unresolved, and ideally what evidence would resolve it |
| `related` | Muscle `id`s. Treated as an **undirected** graph — run `scripts/symmetrise_links.py --write` to close it rather than hand-curating both directions |
| `serial` | Forelimb ↔ hindlimb correspondence. See below |
| `teaching` | What this record is good for in a classroom |
| `caveat` | Source-quality warning (e.g. a non-peer-reviewed preprint) |

### `serial` — handle with care

```jsonc
"serial": {
  "forelimb": "pronator-teres",     // muscle id, or null for "no counterpart"
  "basis": "topological",           // topological | developmental | none
  "note": "...",
  "caution": "..."                  // renders as a warning callout
}
```

Diogo & Molnar (2014) reject forelimb–hindlimb serial homology in the strict
ancestral-duplication sense. A `serial` entry with `basis: "topological"` asserts
only that the two muscles occupy corresponding positions. Where the developmental
anlagen are known to differ — as for popliteus and pronator teres — say so in
`caution`. Reserve `basis: "developmental"` for correspondences that survive that
test.

### `derivatives` — fin-to-limb ancestry

```jsonc
"derivatives": {
  "pectoral": ["pectoralis", "flexor-digitorum-longus"],
  "pelvic":   ["ischioflexorius"]
}
```

Records in `data/muscles-fin.json` are the ancestral paired-fin muscles from
which the whole tetrapod appendicular musculature is derived by subdivision
(Diogo et al. 2016). `derivatives` names what each gave rise to, split by
appendage because these muscles are ancestral to both.

Unlike `related`, this edge is **directed and curated in one direction only**.
The app derives the reverse ("derived from the ancestral fin muscle") by
scanning, so a tetrapod muscle needs no field of its own — and correctly shows
multiple ancestors where they exist (the ischioflexorius has three).

Do not confuse `derivatives` with `homology.serial`. `derivatives` is ancestor →
descendant through time. `serial` is forelimb ↔ hindlimb within one animal, and
is topological rather than genealogical.

---

## `taxa.json`

`topology` is a nested tree whose depth-first traversal gives the order taxa
appear in every occurrence table. Every `taxon` referenced in the tree must be
defined in `taxa`, and vice versa — the validator checks both directions.

Taxon fields: `id`, `label` (common name), `clade`, `exemplars`, `age`, `color`,
`fossil` (bool), `notes`, and optionally `muscleCount`.

`muscleCount` is `{pectoral, pelvic, total, source}`, optionally with
`excludingAutopod`. These are the published per-appendage counts from Diogo et
al. (2016) and drive the muscle-count trajectory in the planned phylogeny view.
They are counts *reported by that source for its exemplar species*, not counts of
records in this dataset — the two will differ and should not be reconciled.

---

## `sources.json`

| Field | Notes |
|---|---|
| `key` | Cited from muscle records |
| `short` | Rendered as the inline citation chip |
| `authors`, `year`, `title`, `journal` | |
| `doi` | Makes the chip a link |
| `peerReviewed: false` | Renders a visible warning |
| `notes` | Path to the reading notes in `papers/` |
| `pdf` | Local PDF filename (git-ignored) |
| `role` | What this source is actually used for here |

---

## Adding a muscle

1. Read the source. Add it to `sources.json` if new.
2. Write the record into the matching `data/muscles-*.json`.
3. `python3 scripts/symmetrise_links.py --write`
4. `python3 scripts/validate.py` — must exit clean.
5. Reload the page. No build step.

## On wording

Paraphrase; do not paste. Anatomical facts are not copyrightable but the source's
expression is, and this repository is public. `scripts/extract_werneburg_appendix.py`
writes verbatim text to `data/raw/`, which is git-ignored for exactly this reason:
it is a curation aid, not a data feed.
