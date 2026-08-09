# Data schema

Three kinds of file live in `data/`:

| File | Holds |
|---|---|
| `taxa.json` | Operational taxa and the topology that orders them |
| `sources.json` | Bibliography, keyed by `key` |
| `skeleton.json` | Skeletal/soft attachment sites: `partOf` hierarchy, per-taxon presence, osteological-correlate flags |
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
| `region` | ✔ | One of `cranial axial fin pectoral arm forearm hand pelvic thigh leg foot`. Drives sort order and the region facet. Enforced |
| `subregion` | | Free text, e.g. `"axio-appendicular"` |
| `mass` | | `dorsal` / `ventral` for limb muscles (the two fundamental limb-bud masses); `branchiomeric`, `somitic`, `somitic-axial`, `extraocular` for cranial and axial. Enforced |
| `layer` | | `superficialis` · `profundus` · `preaxial` · `postaxial` · `primaxial`. With `mass`, gives the four-cell classification (abductor/adductor × superficialis/profundus) that Mansuit & Herrel (2021) use to compare architecture across the whole fin-to-limb transition. Currently populated on `region: "fin"` records; see `docs/ROADMAP.md` phase 1 |
| `arch` | | Pharyngeal arch number, or a string like `"3–7"`. Cranial records only |
| `ancestralNode` | | Where the muscle first appears, e.g. `"LCA of extant gnathostomes"`. Fin records |
| `derivatives` | | `{pectoral: [], pelvic: []}` — muscle `id`s this ancestral fin muscle gave rise to. See below |
| `developmental` | | Embryonic origin. This is often the decisive homology evidence — state it when known |
| `synonyms` | | Every other name for this muscle, **with the author who used it**. These are indexed for search, so they are how a reader arrives from an old paper |
| `consensus` | | `{origin, insertion, action, innervation}` — the generalised description |
| `attachments` | | `{origin: [row], insertion: [row]}` where a row is `{element, side?, landmark?}` — see below. Also valid on **occurrence** rows, which is where taxon-specific attachment is recorded |
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
| `division` | | How far this homology group is split in this taxon. See below |
| `parts` | | The named subunits. Required by `division` states other than `single` |
| `partsOpen` | | `true` where the source's enumeration is explicitly incomplete |
| `divisionNote` | | Why the division is what it is, or who disputes it |
| `note` | | Where the interesting disagreement goes |
| `sources` | ✔ if present | Per-row citation. This is what makes a claim checkable |

`present: "no"` means *this source examined this taxon and did not find the
muscle*. It does not mean the muscle is absent from the clade. Abdala & Diogo
(2010) repeatedly document muscles present in one lizard and absent in another.

### `division` — how far the group has split in this taxon

A homology group is one muscle in a salamander and four in a mammal. That
difference is the differentiation signal the dataset exists to capture, and it
used to live inside the occurrence `name` as prose — `"Iliacus + psoas major (+
sartorius)"` — where nothing could count it.

```jsonc
"division": "divided",
"parts": [
  { "name": "Iliacus" },
  { "name": "Psoas major" },
  { "name": "Sartorius", "membership": "disputed",
    "note": "Diogo & Molnar derive it from the anterior head of this muscle, "
            "against the common claim that it comes from the reptilian 'ambiens'." }
],
"divisionNote": "…"
```

| State | Means |
|---|---|
| `single` | A source examined this taxon and found **one** undivided muscle |
| `heads` | One muscle with several named heads or partes — the biceps |
| `divided` | Several **separate** named muscles — iliacus, psoas major, sartorius |
| `variable` | The clade contains more than one of the above |

`single`, `heads` and `divided` are **ordered**: a field that is single in a
salamander, heads in a frog and divided in a mammal has differentiated twice.
`variable` is polymorphic and deliberately unranked. **Omitting `division`
entirely means unrecorded** — the same distinction `present` draws, and for the
same reason: absence of a statement is not a statement of absence, and scoring an
unexamined taxon as `single` would manufacture a differentiation event on the
branch leading to whichever taxon someone happened to study.

Part fields: `name` (required), `membership`, `muscle`, `note`, `sources`.

`membership` is `established` (default), `disputed` or `variable`. It exists
because parenthetical parts in the literature are usually contested rather than
merely additional. The gemelli are claimed by both the puboischiofemoralis
externus and the ischiotrochantericus; the fibularis tertius is human and the
fibularis digiti quinti is rat. Dropping either would make the count look settled.
This is why the export gives `n_parts_firm` and `n_parts_max` rather than one
number.

`muscle` optionally links a part to its own homology-group record where the
dataset has one. It stays optional and is never inferred from the name — a part
is a name in a taxon, not a record.

**Do not use `parts` on fin records.** Their occurrence names list the tetrapod
muscles each ancestral fin muscle gave rise to, which is `derivatives` — already
curated, and already reversed by the app. Recording it twice gives one fact two
homes.

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

### `attachments` — element / side / landmark rows

```jsonc
"attachments": {
  "origin": [
    { "element": "scapula", "side": "lateral", "landmark": "supraspinous-fossa" },
    { "element": "scapula", "side": "lateral", "landmark": "infraspinous-fossa" }
  ],
  "insertion": [
    { "element": "humerus", "side": "proximal", "landmark": "greater-tubercle" }
  ]
}
```

- `element` — required, an `id` from `skeleton.json`. Always the **bone**, never a
  subsite; subsites go in `landmark`.
- `side` — optional, from `skeleton.json.sides`. Absent means *unrecorded*, not
  *no side*. Never guess it.
- `landmark` — optional, an `id` whose `partOf` chain reaches `element`. The
  validator enforces containment, because a landmark filed under the wrong bone
  silently corrupts the bone-first drill-down.

A muscle touching several sides or landmarks of one bone gets **several rows**.
That is the whole point of the row form: a flat list could not say that the
therian supracoracoideus arises from two distinct fossae.

**Placement decides meaning.** On a muscle, `attachments` is the *consensus*. On
an occurrence, it is what a source records *for that taxon*. Only the second
kind is evidence of a shift, which is why the app computes shifts by diffing
occurrence rows and never by diffing against the consensus.

The diff is hierarchy-aware: `humerus` → `greater-tubercle` is reported as a
**refinement**, not a gain plus a loss, because it is the same attachment at
finer resolution.

Attachments to elements a taxon lacks are a validation **error**. That check
caught a real mistake during authoring — a crocodylian "deltoideus clavicularis"
recorded as arising from a clavicle, which crocodylians do not have.

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

## `skeleton.json`

| Field | Notes |
|---|---|
| `id`, `label`, `kind` | `kind` from the file's `kinds` list |
| `region`, `segment` | `segment` from the file's `segments` list |
| `partOf` | Parent element. Builds the bone-first drill-down; cycles are an error |
| `correlate` | `true` if the site leaves a recognisable osteological trace — the entry point for fossil reconstruction |
| `presence` | `{default, present[], absent[], partial[], reduced[], variable[], note, sources}` |
| `taxonNames` | `[{taxa: [], name}]` — what this element is called in each taxon. See below |
| `transformation` | What happens to the element across the tree; shown on the element |
| `derivedFrom` | Another element this one splits off from (fission, not renaming) |
| `fusedFrom` | The elements that merged to form this one. The inverse of `derivedFrom`. Never combine with `partOf` |
| `synonyms` | |

### Elements are homology groups too

`hyomandibula` and `stapes` were once separate entries with perfectly
complementary presence — fish and tetrapods. That is the signature of **one
element recorded under two names**, and it is exactly the mistake the muscle
records exist to avoid. It also broke the interface: the shark's depressor
hyomandibulae and the mammal's stapedius appeared to attach to different bones,
when the whole point is that they attach to the same one.

So an element is a homology group, with names as per-taxon attributes:

```jsonc
{
  "id": "hyomandibula-stapes",
  "label": "Hyomandibula / stapes",          // neutral cross-taxon label
  "taxonNames": [
    { "taxa": ["chondrichthyes", "actinopterygii"], "name": "Hyomandibula" },
    { "taxa": ["lepidosauria", "aves"], "name": "Columella (stapes)" },
    { "taxa": ["theria"], "name": "Stapes" }
  ],
  "transformation": "One element throughout. …"
}
```

The interface shows the taxon's own name when a taxon is selected, and the
neutral label otherwise. A taxon may appear in only one `taxonNames` entry.

Currently merged: hyomandibula/columella/stapes, palatoquadrate/quadrate/incus,
articular/malleus, angular/ectotympanic.

**`derivedFrom` is for fission, not renaming.** The scapula and coracoid each
`derivedFrom` the `scapulocoracoid`: one ancestral element became two, so they
cannot be merged into one record the way a rename can.

**`fusedFrom` is the inverse — several elements became one.** The tarsometatarsus
is `fusedFrom` the distal tarsals and metatarsals; the tibiotarsus from the tibia
and proximal tarsals.

```jsonc
{
  "id": "tarsometatarsus",
  "fusedFrom": ["distal-tarsals", "metatarsals"],
  "presence": { "default": "no", "present": ["aves"] }
}
```

It must **never** be written as `partOf` a component, and the validator rejects
carrying both. `partOf` means containment within one bone and the attachment
diff reads it as such, so filing the tarsometatarsus under the metatarsals made
an avian insertion on it report as a *refinement* of a crocodylian metatarsal
insertion — the same category as humerus → greater tubercle. The diff now has a
category for fusion, in both directions (a taxon may be the unfused one), and
treats it as a change in the skeleton rather than a shift of the muscle.

Only the compound carries the edge. The reverse — "this bone was incorporated
into that one" — is derived by scanning, the same way a tetrapod muscle's fin
ancestry is derived rather than stored twice.

`presence` is what lets the interface say a muscle's attachment *had to move*
rather than silently dropping a row. It is also enforced: attaching a muscle to
an element its taxon lacks fails validation.

## Adding a muscle

1. Read the source. Add it to `sources.json` if new.
2. Write the record into the matching `data/muscles-*.json`.
3. `./scripts/build.sh --write` — runs migrations, seeds and validation in order.
4. Reload the page. No build step for the site itself.

## Getting the data out

`python3 scripts/export_matrix.py` writes long-format CSVs to `export/`
(git-ignored): `attachments.csv`, `presence.csv`, `division.csv`, `parts.csv`,
`elements.csv`, `muscles.csv`.

`attachments.csv` is one row per muscle × taxon × origin/insertion × element ×
landmark, carrying `side`, `is_correlate`, `inherited` and `sources`. Filter
`inherited == FALSE` for observed data only. `presence.csv` is the character
matrix in long form, ready for comparative methods.

`division.csv` is the differentiation character: one row per muscle × taxon with
`division_rank` (0 single, 1 heads, 2 divided; blank for `variable`) and the two
part counts. `parts.csv` is the long form beneath it, one row per named subunit,
so disputed parts can be included or excluded by filtering.

## On wording

Paraphrase; do not paste. Anatomical facts are not copyrightable but the source's
expression is, and this repository is public. `scripts/extract_werneburg_appendix.py`
writes verbatim text to `data/raw/`, which is git-ignored for exactly this reason:
it is a curation aid, not a data feed.
