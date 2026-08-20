# Data schema

Three kinds of file live in `data/`:

| File | Holds |
|---|---|
| `taxa.json` | Operational taxa and the topology that orders them. **Derived data** — every clade-level statement is computed from the species below |
| `species.json` | The unit of observation: one record per animal anybody dissected |
| `sources.json` | Bibliography, keyed by `key` |
| `observations/` | **The source of truth.** One file per study per animal: what that study says about that animal. `record` names the homology group each row was assigned to, `null` means unassigned |
| `mapping/` | **Derived.** A read-only view of the homology layer: per source, `name\|region` → `{record, species[]}` |
| `skeleton.json` | Skeletal/soft attachment sites: `partOf` hierarchy, per-taxon presence, osteological-correlate flags |
| `nerves.json` | Nerves as homology groups: `partOf` chain to the plexus, limb-bud division, per-taxon names |
| `joints.json` | Joints as homology groups: which bone surfaces articulate, and what motions happen there |
| `muscles-*.json` | Muscle records, split by anatomical region |

`scripts/validate.py` enforces everything below. Run it before committing.

---

## The other central decision: species are the unit of observation

An occurrence is **one species**, observed by one set of sources. It is not a
clade. `Aves` is not a row anybody wrote — it is what *Gallus*, the ostrich, the
tinamou, the crane, the penguin and the loon are computed to agree on.

This replaced a model in which each clade had one row standing for whichever
animal its source happened to dissect, and that model was actively losing data:

- Zaaf et al.'s two geckos insert the extensor carpi ulnaris on **different
  carpals** — the ulnare in *Eublepharis*, the pisiform in *Gekko*. Under one
  Lepidosauria row, one of those observations had to be demoted to prose.
- Ercoli et al.'s rows are *Galictis cuja*, a semi-fossorial mustelid, and had to
  carry a written warning not to read them as the mammalian condition.
- A penguin and a whooping crane could not both be scored, because "the Aves
  column" could only hold one of them — so descriptive sources were **turned
  away** for being too derived, which is not a judgement a dataset should make.

### What a clade rollup computes

| Field | Rule |
|---|---|
| `present` | Species agree → that state. Observed **yes** against observed **no** → `variable`. No species scored → `null`, unrecorded |
| `division` | The same rule |
| name | A clade has none. Its species' names are shown |
| attachments | Not synthesised. The by-species table shows each; the muscle-level `attachments` remains the hand-written cross-tetrapod consensus |

**`variable` is now a result, not a judgement.** It used to be typed in by
whoever noticed that a source found a muscle in one lizard and not another. It is
now what the rows say when they disagree, so it cannot be forgotten, applied
inconsistently, or asserted without evidence.

### `species.json`

| Field | Notes |
|---|---|
| `id` | kebab-case, unique |
| `binomial` | ✔ As the sources write it |
| `clade` | ✔ The operational taxon in `taxa.json` this rolls up into |
| `common` | Vernacular name, where there is one |
| `fossil` | `true` for extinct species |
| `generalised` | `true` where the record stands for a **clade rather than an animal** — `teleostei-generalised`, `amphisbaenia-generalised`. Every occurrence on such a record must use `speciesBasis: "generalised"`, and no other record may. Enforced both ways, including a binomial reading "(generalised)" without the flag, so a placeholder cannot arrive looking like a specimen. Mutually exclusive with `fossil` |
| `note` | Why this animal is in the corpus, and what it is *not* representative of |

### `speciesBasis`

Every occurrence records **how** it was attributed to its species, because the
migration that created them could not be certain for all 630:

| Basis | Means |
|---|---|
| `note` | The row's own prose names the species. Strongest |
| `source` | It cites a single-species study |
| `survey` | It cites a multi-taxon survey, and that survey names an exemplar for this clade (Abdala & Diogo dissected *Timon lepidus*, *Caiman latirostris*, *Gallus*) |
| `default` | Nothing better. The clade's first exemplar, and a guess — the interface labels these |
| `generalised` | **Not a specimen.** The source describes a clade rather than an animal, so no one dissection stands behind the row. Only valid on a species record carrying `generalised: true`, and required on every row that uses one — the validator enforces both directions. Winterbottom's teleost synonymy is the case it exists for: 93 pages reconciling names across the group, dissecting nobody. Those rows previously claimed `source`, which this table defines as citing a *single-species* study, so the rows that were least like an observation were asserting the opposite |

**`speciesBasis` is now historical.** It recorded how strongly a row's species attribution was evidenced, back when the species had to be inferred from a row's prose and its sources. The extraction file's name declares the animal, so there is nothing left to infer; `attribute_species.py` is deleted and the values already in the data are kept as a record of how they were arrived at.

**`taxon` is never stored on an occurrence.** It is derived from
`species.clade` at load. Storing it would be a second home for a fact that
already has one, which is the thing this schema is most careful about.

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
| `developmental` | | Embryonic origin. This is often the decisive homology evidence — state it when known |
| `synonyms` | | Every other name for this muscle, **with the author who used it**. These are indexed for search, so they are how a reader arrives from an old paper |
| `consensus` | | `{origin, insertion, action, innervation}` — the generalised description |
| `attachments` | | `{origin: [row], insertion: [row]}` where a row is `{element, side?, landmark?}` — see below. Also valid on **occurrence** rows, which is where taxon-specific attachment is recorded |
| `occurrences` | ✔ | See below |
| `homology` | | See below |
| `sources` | ✔ | Array of `sources.json` keys |

### Occurrence row

One per **species**, at most — a muscle may carry several rows for one clade, and
their agreement is what produces the clade's state. Omit a species entirely if no
source addresses it; that is different from a source reporting absence.

| Field | Req | Notes |
|---|---|---|
| `species` | ✔ | An `id` from `species.json`. The clade is derived from it and is never stored |
| `speciesBasis` | ✔ | How the attribution was made — see above |
| `present` | | `yes` (default) · `no` · `variable` · `uncertain` · `inferred`. Use `inferred` for fossil reconstructions. **`variable` is a clade rollup, not a species observation** — at species level use `yes`/`no`/`uncertain` and put within-species variation in the note. `validate.py` warns if a `variable` row also carries attachments, since somebody who wrote down where the muscle attached did not find its presence variable |
| `name` | ✔ if present | What this muscle is called **in that taxon's literature** |
| ~~`origin`, `insertion`~~ | | **Removed.** Attachment lives in `attachments` as element/side/landmark rows and its prose in `attachmentNote`. These fields held free strings that no code read, that duplicated the structured rows, and that in the therian column were **human textbook anatomy** — "lateral third of the clavicle", "linea aspera", "scaphoid and trapezium" — carrying a citation to papers that never said it. 551 of them were deleted; the eleven rows that had prose and no structured attachment kept theirs in `attachmentNote` |
| `action`, `innervation` | | Taxon-specific prose, and **live input**: `seed_actions.py` and `seed_nerves.py` derive the structured `actions` and `nerves` rows from them, so deleting them would orphan those rows. Keep them free of human-only detail — a spinal root level such as "(C5–C6)" is a textbook value, not an observation, and `validate.py` warns on it |
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

**Every division was read off its row's own `name` and `note`; none is split by
rule.** The content used to live inside the name as prose — `"Iliacus + psoas
major (+ sartorius)"` — which is readable and uncountable. A regex would not have
drawn the distinctions above, and where the prose will not settle one, the row
carries a `divisionNote` saying so and no `division`: the Komodo dragon's "ilio-,
ischio- and caudofemoralis series" expands two ways, and the turtle extraocular
row names eleven units where its own note quotes Werneburg recording ten.

**Do not use `parts` on fin records.** Their occurrence names list the tetrapod
muscles each ancestral fin muscle gave rise to, which is a `descends-from`
correspondence on each of those muscles — already curated, and already reversed
by the app. Recording it twice gives one fact two homes.

### Homology block

| Field | Notes |
|---|---|
| `confidence` | `well-supported` · `moderate` · `contested` · `uncertain`. Reflects the strength of support **reported in the sources**, not your own view |
| `notes` | The assessment. Name the authors who disagree |
| `openQuestion` | What is unresolved, and ideally what evidence would resolve it |
| `related` | Muscle `id`s. Treated as an **undirected** graph — run `scripts/symmetrise_links.py --write` to close it rather than hand-curating both directions |
| `correspondences` | Typed homology claims about other records — serial, ancestry, partial. See below |
| `teaching` | What this record is good for in a classroom |
| `caveat` | Source-quality warning (e.g. a non-peer-reviewed preprint) |
| `caution` | *(on a correspondence)* What is known to be wrong with an edge kept anyway. See below |
| `authority` | Whose homology scheme this record follows. **Derived** — see below |

### `authority` — recency governs homology, not attachment

```jsonc
"authority": {
  "source": "molnar-diogo-2021",   // must carry `homologyScope` in sources.json
  "basis": "computed"              // computed | curated
}
```

An attachment is an observation and does not age; a homology is an
interpretation and does. So this is the **most recent** source cited anywhere on
the record whose stated purpose includes homology, synonymy or nomenclature
across more than one taxon. `scripts/seed_homology_authority.py --write` writes
it and `validate.py` recomputes it, erroring on drift — adding a newer
comparative source to a record cannot leave that record following the older
scheme by inattention.

`basis: "curated"` opts out and **requires a `note`** saying why the older scheme
is kept, normally that the newer source does not examine the taxa the record
turns on. A record citing no homology-scope source has no `authority` and draws a
warning: its homology rests on descriptive work alone.

The reasoning, and why the rule deliberately does not apply to attachments, is in
[`docs/METHODS.md`](METHODS.md).

### `correspondences` — typed claims about other records

```jsonc
"correspondences": [
  { "relation": "serial", "to": "branchial-constrictors",
    "axis": "pharyngeal-arch", "basis": "developmental",
    "sources": ["diogo-etal-2008-head"], "confidence": "well-supported",
    "note": "..." },

  { "relation": "descends-from", "to": "abductor-superficialis", "girdle": "pelvic" },

  { "relation": "corresponds-to-part-of", "to": "intermandibularis",
    "fromPart": "Tensor tympani", "taxa": ["monotremata", "theria"],
    "sources": ["diogo-etal-2008-head"], "confidence": "contested" }
]
```

One muscle here corresponding to several muscles there is not an edge case — 450
of the 1480 occurrence rows carry `parts` for exactly that reason. `parts` handles
it **inside** a record. This array handles it **between** records.

| relation | Means | Direction |
|---|---|---|
| `serial` | Same series, different segment. `axis` says which | Symmetric — `symmetrise_links.py --write` closes it |
| `no-counterpart` | **Asserted absence** on that axis. Takes `axis`, no `to` | — |
| `descends-from` | Ancestor → descendant through evolutionary time | Directed, stored on the **descendant** |
| `corresponds-to-part-of` | This record, or a named part of it, is part of that one | Directed |

`axis` is `forelimb-hindlimb` or `pharyngeal-arch`. `basis` is `topological`,
`developmental` or `none` — Diogo & Molnar (2014) reject forelimb–hindlimb serial
homology in the strict ancestral-duplication sense, so `topological` asserts only
corresponding position, and `developmental` is reserved for correspondences that
survive knowing the anlagen. `girdle` is `pectoral` or `pelvic` on ancestry edges,
because the ancestral fin muscles are ancestral to both.

**The group is emergent, not stored.** A muscle corresponding to a *group* of
others is several edges sharing a `to`; the inverse is several sharing a source
record. There is no group object, because a stored group would need its own
identity and would go stale the moment a record splits.

**`to` must not be this record.** A part that subdivides differently between two
taxa of one record is a division fact and belongs in `parts` and `divisionNote`.

**`no-counterpart` is a claim, not a blank.** The same distinction `present: "no"`
draws: five records assert there is no forelimb counterpart, and the
caudofemoralis note calls itself a clean falsification of any expectation of
one-to-one fore/hindlimb correspondence. Omitting the relation means unrecorded.

**`sources` and `confidence` are expected but not enforced.** The edges migrated
out of the old `homology.serial` and `derivatives` fields carry neither, because
those fields had no per-edge attribution; `validate.py` reports the running count
once rather than warning on each.

**`caution` records what is known to be wrong with an edge that is kept anyway.**
A known anlage mismatch under `basis: "developmental"`, or a correspondence the
record's own authority denies. It is not a hedge — `confidence` is the hedge. An
edge whose caution says the governing source rejects it is a live disagreement the
data is carrying deliberately, and it should say whose.

**A `serial` edge's source does not set `homology.authority`.** The other two
relations' do. `serial` is symmetric and topological rather than genealogical, so
it says these two muscles are one series in different segments, not what either
muscle *is* — and feeding it into authority hands forelimb records to hindlimb
papers and vice versa, in both directions at once. See
`scripts/seed_homology_authority.py`.

### `related` is not a correspondence

`related` survives alongside this array and means something different:
topologically or developmentally adjacent, untyped, no claim attached, 386 edges
across 128 of the 129 records. Adjacency and correspondence are different
questions. If you can name the relation and cite it, it is a correspondence; if
you are recording that two muscles sit next to each other, it is `related`.

### `after` — this source reports someone else's observation

```jsonc
{ "species": "sphenodon-punctatus",
  "sources": ["russell-bauer-2008", "osawa-1898"],
  "after": "Osawa 1898; Günther 1868; Ribbing 1911, 1938; Haines 1939; Holmes 1977",
  "note": "…what the reporting source adds" }
```

A review states what somebody else dissected. Russell & Bauer give *Sphenodon* on
Miner (1925) and Byerly (1925); Burch gives her extant bracket on Jasinoski et al.
(2006). Without a way to say so the options were to file the row under the
reporting source — claiming an observation it never made, which is the error that
put Dick & Clemente's compiled table on a monitor nobody dissected — or to drop
it. The 2026-08-19 audit found roughly 650 statements across two sources sitting
in that gap.

| | |
|---|---|
| **Value** | A source `key` when the underlying work is in the bibliography; otherwise a citation **with a year**. Most are nineteenth-century papers nobody holds, and demanding a key would mean inventing entries for them |
| **`sources`** | Still the source you actually read. `after` does not replace it |
| **`note`** | Expected. Say what the reporting source *adds* — a synonymy, a correction, a comparison — or the row reads as its own observation |

**It does not lower a row's standing.** An observation reported accurately by a
comparative worker is still an observation; what changes is that the dataset can
now say whose. It is also what makes review-shaped sources minable at all, which
is most of `WORKLIST.md`'s acquisition table.

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
| `homologyScope: true` | This source can adjudicate **what a muscle is**, because establishing homology, synonymy or nomenclature across more than one taxon is part of its stated purpose. Any source may report where a muscle attaches; only these decide what it is. Describing one animal superbly does not qualify — Cunningham (1882) and Osawa (1898) are deliberately not flagged. Drives `homology.authority` |

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
| `correspondences` | Two elements that **may** be one, with nothing showing it. See below |
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

### `correspondences` — the relation that asserts nothing

```jsonc
"correspondences": [
  { "relation": "possibly-corresponds-to",
    "to": "epipubic-bone",
    "basis": "positional",              // positional | developmental
    "confidence": "undemonstrated",
    "sources": ["walker-1973", "cunningham-1882", "reilly-white-2003"],
    "note": "…the case for it, and what is missing" }   // required
]
```

`partOf`, `derivedFrom` and `fusedFrom` each state a fact about the skeleton.
This one states that two elements **might** be one element and that **no cited
source has shown it**, which is a different kind of claim and needs its own
vocabulary or it gets rounded to one of the other three.

It exists because both alternatives were wrong. `epipubis` held the turtle
epipubic cartilage and the mammalian epipubic bone as a single element on
position alone — the same shape of error as `hyomandibula`/`stapes`, run
backwards: there two names for one element were split, here two elements were
merged on a homology nobody demonstrated. But splitting them with no vocabulary
to link them would have thrown away the real observation that they may
correspond.

The `note` is **required**, and must say what the positional case is and what is
missing from it. An undemonstrated correspondence with no note is a shrug with a
schema around it.

**Record the edge once.** The reverse is derived by scanning, exactly as with
fusion and fission; `validate.py` errors if both directions are stored. The
interface renders it in both directions under a *homology undemonstrated* chip,
styled apart from fusion and fission so it does not read as a third kind of
transformation.

`presence` is what lets the interface say a muscle's attachment *had to move*
rather than silently dropping a row. It is also enforced: attaching a muscle to
an element its taxon lacks fails validation.

## `observations/` — the extraction files

**The source of truth.** One file per study per animal, named
`<species>__<source>.json`, holding what that study says about that animal.
`muscles-*.json` is generated from these by `build_observations.py --join`, which
is step 0 of the build. The filename carries the species and the source, so no row
restates either.

```jsonc
{
  "species": "grus-americana",
  "source": "fisher-goodman-1955",
  "status": "remined",              // must equal remine-status.json. Enforced
  "observations": [
    { "name": "M. flexor carpi ulnaris",         // the SOURCE's name, not ours
      "region": "forearm",                       // with `name`, the mapping key
      "record": "flexor-carpi-ulnaris",          // the homology group…
      "present": "yes",
      "speciesBasis": "source",
      "attachments": { "origin": [...], "insertion": [...] },
      "attachmentNote": "…" },

    { "name": "M. pronator brevis",
      "region": "forearm",
      "record": null,                            // …or null: nobody has decided
      "blockedBy": "nomenclature",               // required with record: null
      "blockedNote": "…what is missing, and what would settle it",
      "attachments": { "origin": [...] },
      "muscle": null }                           // set when the record is decided
  ]
}
```

A row with a `record` becomes an occurrence inside it; everything on the row
except `record`, `region` and the `blocked*` fields travels through unchanged, and
`species` and `sources` are reconstructed from the filename. `region` must equal
the record's own region — the mapping view is keyed on `name|region` and the join
drops the field, so a wrong one files the source's name under a key nobody will
look it up by. Enforced.

**One occurrence per (record, species), whatever the number of sources.** Two
studies of the same muscle in the same animal are two rows in two files, and the
join takes the **union** of what they say. It will not choose between them: a
field both rows set to different values stops the build and names the record, the
animal, the field and both sources. That is deliberate — two workers disagreeing
about a muscle is what this dataset exists to hold, and it belongs in an
`attachmentNote` under both names rather than being decided by which filename
sorts first.

Three underscore fields — `_occ`, `_keys`, `_srcs` — are round-trip machinery
written by `--split`: the occurrence's order within its record, its original field
order and its original source order, which together make the join byte-identical.
**A row written by hand needs none of them.** It sorts after the rows that have
one, and its own field order is used.

### Rows with `record: null` — parked

An occurrence has to sit inside a muscle record, so an observation whose record was
unsettled had nowhere to live and was not extracted at all. That gated mining on
homology and meant a paper had to be read again once the synonymy was worked out.
The reading is the expensive part, so these rows exist to make extraction
exhaustive: **score what maps cleanly, park the rest, and never read the paper
twice.** The rule is stated in [`MINING.md`](MINING.md).

| Field | Notes |
|---|---|
| `name` | **Required.** The source's own name — that name is the reason the row cannot be filed |
| `blockedBy` | **Required.** `nomenclature`, `homology`, `no-record`, `division`, `partial` or `occupied` |
| `blockedNote` | **Required with `blockedBy`.** What is missing and what would settle it, normally a specific paper |
| `attachments` | Same `element`/`side`/`landmark` rows as an occurrence, and **held to the same rules** |
| `after` | Whose observation it is, where the study is reporting another worker's. A source key or a citation with a year |
| `muscle` | The record, once decided. The validator then warns until the row is promoted |

**These rows carry no coverage weight.** They are not occurrences: they move no
`%att`, no region or taxon table, no `present` count. `STATUS.md` reports them on
their own, because the figure that matters about them is how much re-reading has
been avoided.

**Held to the same attachment rules as an occurrence** — elements resolve,
landmarks sit inside their element, the taxon actually has the bone. A parked row
with a bad element is not parked, it is wrong, and parking it unchecked would only
move the error later.

**Promotion is one-way and watched.** Set `muscle` and the validator warns until
the row is moved into that record's `occurrences`, so a resolved observation cannot
sit here unnoticed. The validator also warns if a record already carries an
occurrence for the same source, species and name — the two stores must not both
hold the same reading.

## `nerves.json`

Nerves are homology groups, like skeletal elements: one record, names as
per-taxon attributes. The supracoracoid nerve of a lizard and the suprascapular
nerve of a mammal are one record, because they supply one field.

| Field | Notes |
|---|---|
| `id`, `label`, `kind` | `kind` from the file's `kinds` list |
| `region` | `cranial` · `axial` · `forelimb` · `hindlimb` |
| `cn` | Cranial nerve number |
| `arch` | Pharyngeal arch supplied — the criterion that survives relocation |
| `partOf` | Parent nerve or plexus. Builds the chain; cycles are an error |
| `division` | `dorsal` / `ventral` limb-bud division, **inherited** down `partOf` |
| `taxonNames`, `synonyms`, `note` | |

**There is no `presence` block, deliberately.** Scoring 19 taxa against 49
nerves would be 700 assertions these sources do not make: the named peripheral
nerves are tetrapod descriptions and the homologous fin nerves are not
individually named in this literature. Absent means unrecorded, as everywhere
else.

### On a muscle

```jsonc
"nerves": [ { "nerve": "radial-deep", "segments": "C7–C8", "note": "…" } ]
```

Placement follows `attachments`: on the muscle it is the consensus, on an
occurrence it is what a source records for that taxon. The prose `innervation`
stays and is not replaced — it says things ids cannot, such as which half of a
muscle takes which nerve, or that a contribution is variable.

`segments` is attached only where a string names one nerve, because a string
naming two nerves and one range does not say which is which.

### Why it earns its place

`division` is inherited down `partOf`, so the deep branch of the radial is
dorsal because the radial is. That gives a **cross-check the dataset can run on
itself**: a limb muscle's nerve should sit in the division matching its
`mass`, since both track the limb bud. The validator warns where they disagree.

It currently tests 75 limb muscles and 75 agree. Getting there corrected two
things — the suprascapular nerve was filed under the dorsal division when it
leaves the upper trunk before the divisions split, and the caudofemoralis had
been given an inferior gluteal supply by a seed rule reading a phrase that only
located its mammalian homologue. One genuine exception survives, at occurrence
level: the short head of biceps femoris is the one hamstring on the dorsal
division.

## `joints.json`

A joint is a homology group like everything else: the salamander's knee and the
human's are one record. It is stored as two sides, each a list of
element/side/landmark rows in **exactly the form attachments use**.

```jsonc
{
  "id": "knee",
  "kind": "synovial",
  "proximal": [{ "element": "femur", "side": "distal" }],
  "distal":   [{ "element": "tibia", "side": "proximal" },
               { "element": "fibula", "side": "proximal" }],
  "motions": ["flexion", "extension", "rotation-medial", "rotation-lateral"],
  "taxonNames": [{ "taxa": ["aves"], "name": "Femorotibial joint" }]
}
```

`proximal`/`distal` runs outward from the body axis. In the axial and cranial
joints, where that has no clear meaning, `proximal` holds the more axial element
by convention — the pairing is what matters, not the labels.

No `presence` block: a joint exists where its bones exist, and `skeleton.json`
already says where that is.

### Joints are edges, so crossings are derived

Ordering the two sides makes the joints a graph over bones, and the joints a
muscle crosses then fall out of its attachments by shortest path. A muscle from
the ilium to the tibia crosses hip and knee, and **nobody writes that down** —
which matters, because writing it down twice is how two facts drift apart.

`crossing` marks the joints that are not chain links and must be exempt from any
"does it span this?" test:

| `crossing` | Means |
|---|---|
| `chain` (default) | A normal link between two bones |
| `serial` | Both sides name the same element — intervertebral, interphalangeal. A long digital flexor reaches the IP joints *through* the MCP joint |
| `parallel` | The two bones of one segment — radioulnar, tibiofibular. The biceps supinates by rotating the radius against the ulna while attaching only to the radius |

### `actions` on a muscle

```jsonc
"actions": [ { "joint": "knee", "motion": "flexion" },
             { "joint": "hip",  "motion": "extension" } ]
```

Placement follows `attachments` and `nerves`: record level is the consensus,
occurrence level is what a source records for that taxon. The prose `action`
stays — it carries the qualifications that do not survive reduction to a verb,
such as an action holding only in sprawling posture.

`stabilisation` is resisting movement rather than a direction of it, so it
applies to any joint and is not listed per joint.

### The check this buys

An action's joint should be one the muscle spans. The two are independent — a
claim from a source against a derivation from attachments — so the comparison is
a real check, and `actions.csv` exports it as `spans`.

Four muscles currently fail it and all four are correct: the contrahentium caput
longum, both flexor accessorii and the abductor digiti minimi (pes) act on the
digits **through another muscle's tendons**, which the graph cannot follow. That
is also why the seed reports mismatches instead of correcting them. An earlier
version reassigned any unspanned action to the single spanned joint permitting
that motion; it fixed the triceps and broke the contrahentium, replacing a right
answer with a confident wrong one.

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

`joints.csv` is the joint ontology in long form — one row per joint × side ×
element, which is what "the distal femur articulates with the proximal tibia"
looks like as data. `actions.csv` is one row per muscle × scope × joint ×
motion, with `spans` recording whether the attachments cross that joint.

`innervation.csv` is one row per muscle × scope × nerve, carrying the inherited
`division`, the `chain` up to the plexus, and `division_agrees` — the mass
cross-check, as a filterable column.

`division.csv` is the differentiation character: one row per muscle × taxon with
`division_rank` (0 single, 1 heads, 2 divided; blank for `variable`) and the two
part counts. `parts.csv` is the long form beneath it, one row per named subunit,
so disputed parts can be included or excluded by filtering.

## On wording

Paraphrase; do not paste. Anatomical facts are not copyrightable but the source's
expression is, and this repository is public. `scripts/extract_werneburg_appendix.py`
writes verbatim text to `data/raw/`, which is git-ignored for exactly this reason:
it is a curation aid, not a data feed.
