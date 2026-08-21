# Huber, Soares & de Carvalho (2011) — Cranial muscles of chondrichthyans

*Encyclopedia of Fish Physiology*, ch. 238. doi:10.1016/B978-0-12-374553-8.00238-0
Source key: `huber-etal-2011`

## ~~Requested~~: elements and species — all applied 2026-08-20

**All applied.** Both species and all eight elements are in `data/species.json`
and `data/skeleton.json`, and the three presence widenings are made; the rows
below validate. Kept here as the record of what one pass needed, and because
`propterygium`'s `partOf` is still provisional — see its note.

*Hydrolagus colliei* turned out to exist already, cited by Anderson (2008); only
*Rhinobatos percellens* was new.

**Species**

```jsonc
{ "id": "rhinobatos-percellens", "binomial": "Rhinobatos percellens", "clade": "chondrichthyes",
  "common": "Southern guitarfish",
  "note": "Huber et al.'s batoid exemplar, described alongside Squalus acanthias and Hydrolagus colliei in the same paper. The existing version of this note called it 'Rhinoptera percellens' — wrong genus (Rhinoptera is the cownose-ray genus); Huber et al. write Rhinobatos throughout, and Figure 6's caption confirms it." }
```

**New elements**

```jsonc
{ "id": "propterygium", "label": "Propterygium", "kind": "cartilage",
  "region": "fin", "segment": "fin", "partOf": "fin-radials",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Anteriormost basal pectoral-fin cartilage. Rhinobatos percellens's cucullaris, ventral superficial branchial constrictor and branchial trematic constrictor all attach here — its expanded pectoral fin reaches forward to the head. `partOf: fin-radials` is a placement guess pending a batoid fin-skeleton reference; it may belong beside `preaxial-radials` instead." }

{ "id": "rostrum", "label": "Rostrum", "kind": "cartilage",
  "region": "cranial", "segment": "cranial", "partOf": "neurocranium",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Anterior chondrocranial extension, labelled 'RO' in Huber et al.'s Table 1 and figured for both Squalus and Rhinobatos. Insertion of Rhinobatos's depressor rostri and levator rostri, both parked here for want of a record." }

{ "id": "nasal-capsule", "label": "Nasal capsule", "kind": "cartilage",
  "region": "cranial", "segment": "cranial", "partOf": "neurocranium",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Cartilaginous nasal-capsule region of the chondrocranium, named in all three of Huber et al.'s tables. Not `nasal`, the dermal bone — the same collision MINING.md warns of for autopalatine/palatine. Origin of Rhinobatos's preorbitalis and part of its levator rostri insertion, both parked." }

{ "id": "opercular-flap", "label": "Opercular flap (holocephalan)", "kind": "soft",
  "region": "cranial", "segment": "cranial",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Single soft covering over all gill openings in holocephalans, unlike the separate elasmobranch gill slits (`gill-slits`). Not `opercle` (bony, actinopterygii-only) or `operculum` (the amphibian otic operculum) — same caution MINING.md gives for those two. This taxonomy has no node finer than chondrichthyes, so presence is scoped there though the structure is holocephalan-only; narrow if a Holocephali node is ever added. Insertion of Hydrolagus's constrictor operculi dorsalis/ventralis, both parked." }

{ "id": "inferior-maxillary-cartilage", "label": "Inferior maxillary cartilage (holocephalan)", "kind": "cartilage",
  "region": "cranial", "segment": "cranial",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Holocephalan jaw-region cartilage, origin of Hydrolagus's intermandibularis — distinct from Meckel's cartilage, which the same table uses for the same species' adductor mandibulae. Holocephalan-specific within chondrichthyes; see opercular-flap's note on clade granularity." }

{ "id": "premandibular-cartilage", "label": "Premandibular cartilage (holocephalan)", "kind": "cartilage",
  "region": "cranial", "segment": "cranial",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Paired fibrocartilage at the holocephalan lower-jaw symphysis, the intermandibularis insertion. Holocephalan-specific within chondrichthyes." }

{ "id": "premaxillary-cartilage", "label": "Premaxillary cartilage (holocephalan)", "kind": "cartilage",
  "region": "cranial", "segment": "cranial",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Holocephalan labial-series cartilage, origin of the (parked) labialis anterior. Not `premaxilla`, the dermal bone. Holocephalan-specific within chondrichthyes." }

{ "id": "superior-maxillary-cartilage", "label": "Superior maxillary cartilage (holocephalan)", "kind": "cartilage",
  "region": "cranial", "segment": "cranial",
  "presence": { "default": "no", "present": ["chondrichthyes"], "sources": ["huber-etal-2011"],
    "note": "Holocephalan labial-series cartilage: insertion of the labialis anterior (parked) and of the levator anguli oris anterior/posterior (filed on `levator-anguli-oris`). Not `maxilla`. Holocephalan-specific within chondrichthyes." }
```

**Presence widenings on existing elements** — all currently `present: ["actinopterygii"]` only, so a chondrichthyan attachment to them errors:

```jsonc
// epihyal: add "chondrichthyes"
"note": "Huber et al. (2011) name an epihyal cartilage as the Hydrolagus colliei levator hyoideus insertion (parked, no-record — the muscle's home is unsettled, but the bone is real). Holocephalan-specific within chondrichthyes; no source here shows one in elasmobranchs."

// pharyngobranchials: add "chondrichthyes"
"note": "Huber et al. (2011) name pharyngobranchial cartilages in the Hydrolagus colliei adductor arcuum branchialium origin (parked, no-record)."

// ceratobranchials: add "chondrichthyes"
"note": "Huber et al. (2011) name ceratobranchial cartilages as the Hydrolagus colliei constrictor branchialis insertion (filed on `branchial-constrictors`) and the adductor arcuum branchialium insertion (parked). Needed for the filed row to validate."
```

## Why it was reached for

Top of `MINING.md` on density — 7.1 origin/insertion mentions per page — against
the thinnest column in the dataset. **Chondrichthyes went 5% → 37%.** Cranial,
its largest region gap, went from 10 unscored to 4.

## The paper describes three animals, not two

**Checked against the paper itself, not the note, per `MINING.md`'s standing
rule.** Huber et al. (2011) is not a *Squalus* paper with a batoid aside. It has
three fully-worked sections, each with its own table of origins, insertions and
actions and its own figures: **Shark Musculature** (*Squalus acanthias*, Table 2,
29 muscles, Figures 1–5), **Batoid Musculature** (*Rhinobatos percellens*, Table
3, 29 muscles, Figures 6, 9–11), and **Holocephalan Musculature** (*Hydrolagus
colliei*, Table 4, 24 muscles, Figures 12–14). The introduction states this
directly: "Among the elasmobranchs, sharks are represented by the spiny dogfish
*Squalus acanthias* and batoids by the southern guitarfish *Rhinobatos
percellens*. The holocephalans are represented by the spotted ratfish
*Hydrolagus colliei*."

**The version of this note that stood until today missed the third animal
entirely.** It said batoid coverage "would need its own species row" — true, but
silent on Hydrolagus, which has a complete table and text section of its own and
is a different subclass (Holocephali) from both other exemplars. It also named
the batoid "*Rhinoptera percellens*" — the cownose ray genus, not the guitarfish
Huber et al. actually describe (*Rhinobatos*). Neither the missing animal nor the
wrong genus was caught before this pass, which is exactly the failure
`MIGRATION-STATE.md` catalogues under "does the paper describe more animals than
the file does?" — the fourth instance of it in this dataset now, after Freitas et
al., Přikryl et al., and (within Huber et al. itself, below) the shark table's own
under-mining.

**Squalus's own table is also far from exhausted**, which the old note did not
say either. It listed only `stapedius` (depressor hyomandibulae) and
`extraocular-muscles` as "not scored," but Table 2 names 29 muscles and the six
filed rows touch at most 13 of them, several imperfectly:
- The row named "Constrictor hyoideus ventralis" (filed on `interhyoideus`) has
  attachments (ceratohyal → midventral raphe) and an attachmentNote lifted from
  Huber et al.'s **Interhyoideus** paragraph, not their Constrictor hyoideus
  ventralis one (raphe of first gill slit → tendinous sheath over the hyomandibula,
  Table 2). The two are different rows in Huber et al.'s own table. This dataset's
  true "Interhyoideus" for Squalus is filed under the wrong name; the true
  "Constrictor hyoideus ventralis" was never filed at all.
- The row named "Constrictor hyoideus dorsalis (levator hyomandibulae)" (filed on
  `depressor-mandibulae`) compresses two separate Table 2 entries — Constrictor
  hyoideus dorsalis (chondrocranium+cucullaris → tendinous sheath over the
  hyomandibula, compresses the gill pouch) and Levator hyomandibulae
  (chondrocranium+epibranchial muscles → hyomandibula, elevates it) — into one
  occurrence with one set of attachments.
- Never touched at all: branchial adductor, branchial trematic constrictor,
  coracoarcualis, coracobranchialis, coracohyoideus, coracomandibularis,
  cucullaris, dorsal interarcual, epibranchial (the cranial epaxial-extension
  muscle), hyoid trematic constrictor, interbranchial, lateral interarcual and
  preorbitalis — thirteen more names, several of which this pass also had to park
  for Rhinobatos and Hydrolagus for want of a record, so parking them for Squalus
  too would not need new reading, only new rows in the existing file.

**This pass did not touch `squalus-acanthias__huber-etal-2011.json`** — outside
its brief, which was the two missing animals — so none of the above is fixed.
It is recorded here so the next pass does not have to re-derive it by reading the
paper a third time. A proper Squalus re-mine, correcting the two mislabelled rows
above and filing or parking the other thirteen names, is worth doing before this
source can be marked `remined`; on the count above it would move the source from
"6 rows on one of three animals" to something close to complete.

## The finding: the ventral sheet is not skeletal

Both the intermandibularis and the interhyoideus insert on the **midventral
raphe**, not on cartilage. The intermandibularis has no bony attachment at either
end at the midline. So the entire ventral sheet of the mandibular and hyoid
arches — the muscles that elevate the floor of the mouth and drive hydraulic
transport through the oropharyngeal cavity — leaves nothing for a fossil to
record.

That is the chondrichthyan counterpart of the anuran knee aponeurosis found in
Prikryl et al., and it belongs with it in whatever eventually gets written about
the limits of osteological reconstruction.

## Three elements added (first pass)

`midventral-raphe`, `gill-slits`, `spiracular-cartilage`. All soft or cartilage,
all attachment fields that had no home. (Eight more are requested above, from
this second pass.)

## Worth teaching from

The adductor mandibulae row runs **palatoquadrate → Meckel's cartilage**. Both
are homology groups here: `palatoquadrate-quadrate` is one record covering the
shark's palatoquadrate, the lizard's quadrate and the mammalian incus. So the
shark's jaw adductor and the mammal's masseter are visibly attached to
descendants of the same element, which is exactly what merging those records was
for.

## Second pass, 2026-08-20 — the other two animals mined

**New files**: `data/observations/rhinobatos-percellens__huber-etal-2011.json`
(30 rows: 19 filed, 11 parked) and
`data/observations/hydrolagus-colliei__huber-etal-2011.json` (24 rows: 18 filed,
6 parked). Between them every one of the 53 muscle names in Tables 3 and 4 is
either filed or parked, plus one prose-only absence (Rhinobatos's branchial
adductor, explicitly stated not found in this species) — **54 muscle statements,
37 filed, 17 parked, arithmetic closed for both files.**

**Filed cleanly** using this dataset's own synonym lists or an already-established
occurrence on the same record and species (Anderson 2008, already in the corpus
for Hydrolagus): the three-part adductor mandibulae complex in both animals, both
animals' six extrinsic eye muscles (`extraocular-muscles`), the hyoid
constrictors' ventral half (`interhyoideus`) and dorsal-arch levator/depressor
pair (`levator-arcus-palatini`, `depressor-mandibulae`), the superficial branchial
constrictors and Hydrolagus's constrictor branchialis (`branchial-constrictors`),
the cucullaris in both animals (`protractor-pectoralis`), Rhinobatos's depressor
hyomandibularis (`stapedius`), the coracomandibularis/coracohyoideus/
coracobranchialis set (`hypobranchial-muscles`), Hydrolagus's intermandibularis
(`intermandibularis`) and its two-part levator anguli oris (`levator-anguli-oris`).

**Parked rather than guessed**, each with a `blockedNote` naming what would settle
it: Rhinobatos's coracoarcualis, coracohyomandibularis, depressor rostri and its
"depressor mandibulae" division, dorsal hyoid constrictor, epaxialis (the cranial
epibranchial-equivalent), interbranchial, levator rostri and preorbitalis, plus
the branchial trematic constrictor (nomenclature not yet bridged) and the stated
absence of the branchial adductor; Hydrolagus's adductor arcuum branchialium,
both opercular constrictors, the cranial epibranchial-equivalent, labialis
anterior and levator hyoideus.

**Two of the parks are worth flagging specifically, because they resist an
easy guess that the data already half-suggests:**

- **"Depressor mandibulae" in Rhinobatos is not this dataset's `depressor-mandibulae`
  record.** Huber et al. state outright that it "appears to be a division of the
  depressor rostri" — a hypobranchial-derived, midline-raphe muscle that abducts
  the jaw from below, not the tetrapod arch-2 (CN VII) jaw-opener this record is
  built around. Filing it here on name alone would be the exact trap `MINING.md`
  warns about ("the names simply look alike"). It is parked with `depressor
  rostri`, its parent muscle, which also has no record.
- **"Dorsal hyoid constrictor" sits between two records and neither bridge is
  clean.** `depressor-mandibulae`'s own synonym list carries "constrictor hyoideus
  dorsalis (partim)" — hedged, partial only — and a brand-new record,
  `constrictor-hyoideus-dorsalis`, was created the same day this pass ran,
  specifically to hold "the dorsal division of the hyoid constrictor" that "this
  dataset had no record of at all." But that record is built entirely from
  Winterbottom's (1973) teleost synonymy, its consensus attachments are teleost
  bones (parasphenoid, prootic, metapterygoid, opercle) with no chondrichthyan
  attachment scored anywhere on it, and nothing cited here extends it to
  chondrichthyans. Picking either record would be picking between a hedge and an
  unextended one — parked instead, and the same unresolved choice already sits
  silently inside the existing Squalus row (see above), which chose
  `depressor-mandibulae` without addressing it.

**The Interhyoideus contradiction — recorded, not resolved.** Huber et al. give
Hydrolagus colliei a full interhyoideus: "originates upon the symphysis of the
lower jaw and inserts onto the ceratohyal cartilages... abduct[ing] the hyoid
arch" (Table 4, Meckel's cartilage → ceratohyal). Anderson (2008), already filed
on this exact record and species, reads the opposite: "No homologous
interhyoideus in *Hydrolagus colliei*... he reads a secondary loss in
chimaeroids." Both are recorded as this source states them — Huber et al.'s row is
filed present: "yes" with structured attachments, Anderson's stands as present:
"no" — because withholding either to avoid the collision would be worse than the
collision. This is `MINING.md`'s "structural disagreement" case exactly: "the
build stops and names both sources, because that is a decision somebody has to
take and write down." It has not been taken here. Whether Huber et al.
misidentify some other muscle as an interhyoideus, whether Anderson's reading of
loss is wrong, or whether the two chimaeroid specimens genuinely differ is a call
for whoever next works the holocephalan cranial column, ideally with Didier
(1987) — the holocephalan myology thesis already flagged as unread on the
`levator-arcus-palatini` record — or Miyake et al. (1992), both in Huber et al.'s
own further reading.

**Two more reconciliation points, lower stakes, flagged for the same reason:**
Hydrolagus's adductor mandibulae anterior/posterior and its
coracomandibularis/coracohyoideus/coracobranchialis set both land on records
that already carry an Anderson (2008) occurrence for this species, written as one
hand-parted row with no structured attachments (`division: "divided"`, parts
named as compound strings like "Adductor mandibulae anterior + posterior" and,
for the hypobranchial set, an extra muscle — mandibulohyoideus — that Huber et
al. do not mention at all). This pass wrote per-muscle rows with structured
attachments, per `MINING.md`'s standing instruction not to hand-author `parts`
now that per-part attachments derive automatically. The two treatments will need
reconciling at build time; neither row was edited to pre-empt it.

**No new elements were needed for anything already in `skeleton.json`** beyond
the eight requested above and the three presence widenings — everything else
(mandible/Meckel's cartilage, palatoquadrate-quadrate, hyomandibula-stapes,
scapulocoracoid and its scapular process, the branchial-arch series, the hyoid
and its ceratohyal/epihyal/corpus hyoidei, midventral-raphe, neurocranium and its
otic capsule and orbit, spiracle and spiracular cartilage, eye-bulbus,
pectoral-girdle, vertebral-column) already existed and, in several cases
(gill-slits, epibranchials, scapular-process, midventral-raphe, spiracular-cartilage),
were already scoped to chondrichthyes from the first pass on Squalus.

## Not scored, and why (supersedes the previous version of this section)

`stapedius` (depressor hyomandibulae) and `extraocular-muscles` for *Squalus*
specifically remain unfiled — this pass did not touch the Squalus file (see
above). For Rhinobatos and Hydrolagus, "not scored" now means the seventeen
parked rows listed above, each with a citable reason in its `blockedNote` rather
than a blanket note here. Batoid coverage is no longer "by difference from
Squalus" — Rhinobatos percellens has its own full table, now mined, and is
requested as its own species record at the top of this note. *Rhinoptera
percellens*, named in the previous version of this note, does not appear in this
paper at all and was a wrong genus.


## Integration, 2026-08-20 — one conflict resolved, one left standing

This pass was mined as a delegated job under the rules in `MINING.md`: observation
files and this note written by the miner, elements and species requested rather
than added, nothing generated touched, nothing committed. Two things needed an
integrator.

**The interhyoideus of *Hydrolagus* is parked, and the repository's own rule
decides it.** Huber et al. Table 4 name one and give it attachments — jaw symphysis
to ceratohyal. Anderson (2008) says there is **no homologous interhyoideus** in this
animal, against its presence in the other four gnathostomes he compares, and reads a
secondary loss in chimaeroids. The build refused the pair, correctly.

Recency governs homology — but the governing source has to be a comparative one.
**Anderson (2008) carries `homologyScope`; Huber et al. (2011), an encyclopedia
chapter describing three chondrichthyans, does not.** So Anderson governs whether the
muscle Huber describes *is* the interhyoideus, and the row cannot sit on that record
while his occurrence says the animal has none. It is parked on `homology` with both
its ends intact. Nothing is lost; what is unsettled is the muscle's name.

**The dorsal hyoid constrictor of *Rhinobatos* is left parked**, as the miner left
it. `constrictor-hyoideus-dorsalis` was created the same day from Winterbottom's
teleost synonymy and carries no chondrichthyan attachment; Huber's shark table names
a *constrictor hyoideus dorsalis* too, which is the same Edgeworth field by name. But
name-matching is what `MINING.md` forbids, and no cited source states the
chondrichthyan-to-teleost equation. It stays parked until one does — and that is now
the most valuable single homology call outstanding in the fish columns.