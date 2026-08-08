# Mansuit & Herrel 2021 — appendicular muscle architecture across the fin-to-limb transition

## Citation

Mansuit R, Herrel A. 2021. The evolution of appendicular muscles during the fin-to-limb transition: possible insights through studies of soft tissues, a perspective. *Frontiers in Ecology and Evolution* 9: 702576. DOI: 10.3389/fevo.2021.702576. **Open access, CC-BY.** Edited by Ingmar Werneburg; reviewed by Virginia Abdala and David Marjanović.

**Article type: Perspective.** This is a framing piece and literature meta-analysis, not a primary data paper. The authors are explicit that their analyses are "a proof of concept" and that the data are too sparse to test statistically.

## Question

The anatomy and homology of appendicular muscles across the fin-to-limb transition is well studied (Diogo et al. 2016; Molnar et al. 2018, 2020). The **architecture** — muscle mass, fibre length, pennation angle, physiological cross-sectional area — is not. Since the transition involves a new locomotor mode and a proposed shift from pectoral to pelvic dominance ("front-wheel to rear-wheel drive"), architecture should carry a signal. Does it?

## Method

Literature meta-analysis. No new dissection. Muscles were binned into **four intrinsic groups** following the homology scheme of Diogo et al. (2016) and Molnar et al. (2018, 2020):

- abductor superficialis
- abductor profundus
- adductor superficialis
- adductor profundus

The caudofemoralis is deliberately **excluded** as an axial-derived muscle, not a limb muscle *sensu stricto*.

Taxa compiled: actinopterygians (*Cryptopsaras*, *Antennarius*, *Carassius*); *Latimeria chalumnae* (the only sarcopterygian fish with architecture data, via Huby et al. 2021); *Alligator mississippiensis*; varanid lizards; several mammals (*Isoodon*, *Galictis*, *Taxidea*, *Dasypus*, *Marmota*, *Equus*). Birds excluded as too derived for flight.

## Findings

1. **Appendage muscle mass increases sharply relative to body mass.** In actinopterygians and *Latimeria*, each appendage is **< 1%** of body mass. In tetrapods it is **> 1.7%**, reaching **8.5%** in the short-nosed bandicoot *Isoodon*.

2. **The pectoral→pelvic dominance shift is corroborated.** *Latimeria*: pectoral fin muscle mass **0.43%** of body mass vs pelvic **0.30%**. In tetrapods the relationship inverts — hindlimb heavier than forelimb. This is the "front- to rear-wheel drive" shift, previously argued from skeletal anatomy alone, now with a soft-tissue line of evidence.

3. **The deep-to-superficial investment shift.** In actinopterygians and in *Latimeria*, the **deep** groups (abductor/adductor profundus) contribute most of the appendage muscle mass, in both appendages. In tetrapods the **superficial** groups (abductor/adductor superficialis) dominate, in both fore- and hindlimb. The single exception in the dataset is the horse *Equus caballus*, where adductor profundus exceeds adductor superficialis.

4. **Functional reading.** Fish propulsion comes from axial undulation and the caudal fin; paired fins mainly do manoeuvring. Tetrapod limbs must both support the body against gravity and generate thrust. Supporting evidence: *Polypterus* raised in terrestrial conditions develops a longer, more robust pectoral endoskeleton (Standen et al. 2014); benthic walking anglerfish (*Antennarius*) have pectoral fin muscles about four times stronger than pelagic swimming relatives.

## Limitations

Stated forcefully by the authors:

- **No single study compares pectoral and pelvic fin architecture in the same fish species.** Actinopterygian data are stitched across papers.
- Only four taxa in the whole dataset permit a within-species pectoral/pelvic comparison (coelacanth, alligator, varanid, bandicoot).
- *Galictis* data are given as proportions of within-limb muscle mass, not body mass, so the two limbs cannot be compared.
- Several taxa contribute only one appendage (*Taxidea*, *Dasypus*, *Marmota* forelimb only; *Equus* hindlimb only).
- *Latimeria* is not the closest living relative of tetrapods; it is used because it is the only sarcopterygian fish with architecture data at all.
- The trends are not statistically testable with available data. The paper's own stated purpose is to provoke systematic quantitative dissection work.

## Relevance to this project

Two uses.

**First, it names the gap.** The README lists "no muscle architecture data" as a known gap. This paper is the framing reference for closing it, and it identifies the primary sources that hold the numbers (Allen et al. 2010; Ercoli et al. 2013, 2015; Dick & Clemente 2016; Huby et al. 2021; Payne et al. 2005; Moore et al. 2013; Olson et al. 2016; Rupert et al. 2015; Warburton et al. 2015; Martin et al. 2019). Several of these are already in `papers/`.

**Second, and more useful, it validates a four-cell classification as a comparative unit.** By binning every appendicular muscle in every taxon from bichir to horse into `{abductor, adductor} × {superficialis, profundus}`, the authors extract a real evolutionary signal across the whole fin-to-limb transition. That is direct empirical support for organising the interface around **developmental mass and layer** rather than around individual muscles or attachment sites — see `docs/ROADMAP.md`. The same four cells are already encoded in this dataset as `mass` plus the superficialis/profundus distinction.

Note the authors' exclusion of caudofemoralis on developmental grounds. The dataset follows the same logic: `mass: "somitic-axial"` versus the limb-bud `dorsal`/`ventral` masses.
