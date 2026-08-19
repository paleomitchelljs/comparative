# Regnault & Pierce (2018) — Echidna pectoral girdle and forelimb function

## Citation

Regnault S, Pierce SE. 2018. Pectoral girdle and forelimb musculoskeletal function
in the echidna (*Tachyglossus aculeatus*): insights into mammalian locomotor
evolution. *Royal Society Open Science* 5: 181400. doi:10.1098/rsos.181400.
Open access.

## Question

The synapsid forelimb was reorganised over roughly 300 million years — from the
bulky U-shaped pectoral girdle, screw-shaped glenohumeral joint and sprawling limb
of the earliest synapsids to the reduced mobile girdle, ball-and-socket shoulder and
parasagittal limb of therians. The sequence of anatomical changes and their
functional consequences are unclear. Monotremes sit at an informative point on that
line, so: what can an echidna shoulder actually do?

## What it is

**A three-dimensional musculoskeletal computer model**, built to estimate ranges of
motion at each joint axis and moment arms for the muscles crossing the shoulder.

## Findings

The echidna's skeletal morphology **restricts** scapulocoracoid mobility and
glenohumeral flexion–extension relative to therians. The estimated ranges of motion
and moment arms indicate a girdle and forelimb optimised for **humeral adduction and
internal rotation**, which agrees with the limited *in vivo* data available. More
muscles act to produce humeral long-axis rotation here than in therians, and the
authors attribute that to differences in muscle geometry rather than to different
muscles.

## Why it yields no rows, and a correction

**This paper did not dissect an echidna.** The specimen was kept intact for a future
study and was not available at the time of model-building. Muscle origin and
insertion data were taken from **Gambaryan et al. (2015)**, specifically their
figures 19B1–B2, 20B1–B2, 21B1–B4 and 22B1–B4: markers were placed on the bone
surfaces at the approximate centroid of each shaded attachment area in those
figures, **judged by eye**, and those coordinates defined the muscle lines of action.

So it is not an independent third treatment of the echidna shoulder beside Gambaryan
et al. (2015) and Fahn-Lai et al. (2020) — `docs/WORKLIST.md` said it was, before
the methods section was read, and that claim has been removed. **Its attachments are
Gambaryan et al.'s attachments**, at one remove and coarsened to a centroid. Scoring
them here would put the same observation into the dataset twice under two source
keys, which is the failure mode the `speciesBasis` vocabulary exists to prevent.

This is the case `MINING.md` has in mind when it says to check the methods section
before scoring, every time. A citation records where a claim was read, not where it
was observed.

## What it is good for

The same thing Hutchinson et al. (2015) and Allen et al. (2021) are good for:
**function that attachment data alone will not give you.** The moment-arm result —
that the echidna's shoulder is built for adduction and internal rotation, and that
long-axis rotation is produced by more muscles than in a therian because of how the
muscles are arranged rather than which muscles are present — is not derivable from
the attachment rows on `data/muscles-pectoral.json`, and it is the kind of statement
those rows exist to be set against.

Pair with **Gambaryan et al. (2015)** for the attachments this model runs on, with
**Fahn-Lai et al. (2020)** for the shoulder architecture measured from real
specimens, and with **Gambaryan et al. (2002)** for the hind limb of the same animal
— where an equivalent lever-arm analysis, done by hand on an articulated skeleton,
reaches the parallel conclusion that the femur pronates rather than retracts.

## Relevance to comparative anatomy teaching

Worth showing to a student alongside its own methods section. The model is careful,
the figures are clear, the conclusion is well supported — and the muscle attachments
in it were placed by eye from another paper's shaded diagrams. That is normal and
honest practice, stated plainly by the authors, and it is also exactly why a
reference database has to record where an observation was made and not merely where
it was read.
