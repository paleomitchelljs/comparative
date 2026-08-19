# Werneburg (2011) — The cranial musculature of turtles

## Citation

Werneburg I. 2011. The cranial musculature of turtles. *Palaeontologia Electronica*
14(2): 15A, 99 pp.

## Question

The paper opens on the problem this whole repository is built around: **there is no
common reference system for vertebrate muscle nomenclature.** Werneburg gives three
reasons — traditions dominated by human medical anatomy, typological "box-like"
approaches, and simplifications that follow each author's own taxonomic and
topographical focus. The result is terminological and homologisation confusion that
blocks evolutionary and developmental analysis.

His answer is a traceable approach to muscular terminology, applied to turtles.

## What it is

**More than 100 references on turtle cranium-associated musculature, critically
reviewed**, from which he identifies a set of **88 adult "muscular units"** — the
smallest parts of macroscopic muscular structures — demonstrated on a side-necked
turtle. Homologies are defined by explicit criteria taken together: innervation,
spatial characteristics, and ontogeny.

He also records what most descriptive myology leaves out: **adult arrangement
variability between specimens, fusions of muscular units, and drop-like apoptosis**.
He reads these as the result of fluid pattern formation, driven initially by neural
crest stream patterning in ontogeny — which is the argument for why muscle
boundaries are not always crisp and should not always be forced.

## The species problem, and how these rows are scored

**This is a catalogue across turtles, not a dissection of one.** His own animal is
*Emydura subglobosa*; the appendix compiles across species.

That distinction was got wrong here once and is worth stating plainly: ten rows had
been scored on *Trachemys scripta*, an animal this paper does not dissect. They are
now on **`testudines-generalised`**, with `speciesBasis: "generalised"` — the state
reserved for a source that describes a clade rather than an animal. The validator
enforces it in both directions.

The general rule is in `MINING.md`: **check the methods section before scoring,
every time.** A citation records where a claim was read, not where it was observed.

## Scored

10 occurrence rows on `testudines-generalised`, plus one on *Ascaphus truei*: the
adductor mandibulae complex and its externus, internus and posterior divisions, the
depressor mandibulae, intermandibularis, interhyoideus, branchial constrictors,
extraocular and hypobranchial muscles.

**The attachment rows aggregate his units.** `adductor-mandibulae-externus` carries
fourteen attachment rows because it aggregates the seven units Werneburg resolves —
pars superficialis, media, profunda and their subdivisions — so the element list is
the union across those units, not one belly's attachments. The wide origin over the
skull roof and braincase, and the redirection of the line of action over the otic
process, are what the turtle trochlear arrangement buys.

He lists **13 synonyms for the depressor mandibulae alone**, which is the kind of
thing the search index exists to absorb.

## Not done

**The dataset's cranial records are coarser than this source.** The adductor
mandibulae is one record here covering a complex Werneburg resolves into a dozen
units in turtles alone. `scripts/extract_werneburg_appendix.py` parses Appendix 1
into structured units and is the route to splitting the record further; the output
is git-ignored.

**One row is deliberately left without a division.** The turtle extraocular row
names eleven units while its own note quotes Werneburg recording ten. The
discrepancy is recorded rather than resolved — reconcile against the source before
asserting a count.

## Relevance to comparative anatomy teaching

The clearest statement in the corpus of *why* comparative nomenclature is a mess,
written by someone who then does the work of fixing it for one clade. The three
causes he names — medical-anatomy tradition, typological thinking, and each
author's own focus — are worth giving a student before they open any two papers on
the same muscle. Pair with **Johnston (2011, 2014)** on the jaw adductors, where
attachment beats innervation as the homology criterion, and with **Schumacher
(1973)** for the chelonian and crocodylian head together.
