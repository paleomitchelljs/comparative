# Klinkhamer et al. 2017 — digital dissection of *Crocodylus porosus* limb musculature

## Citation

Klinkhamer AJ, Wilhite DR, White MA, Wroe S. 2017. Digital dissection and three-dimensional interactive models of limb musculature in the Australian estuarine crocodile (*Crocodylus porosus*). *PLoS ONE*. DOI: 10.1371/journal.pone.0175079. **Open access.**

## Question

Can digital dissection — contrast-enhanced CT plus segmentation — deliver limb muscle anatomy in a form that is both more detailed and more reusable than a traditional destructive dissection?

## Taxa and material

*Crocodylus porosus*, fore- and hindlimb, segmented into interactive 3D models.

## What it contributes here

The value for this project is not the 3D models but the **prose descriptions**, which name an explicit anatomical aspect for nearly every attachment. That makes it the densest available source of `side` values, and crocodylians were previously among the thinnest columns for attachment detail. Examples:

| Muscle | Origin | Insertion |
|---|---|---|
| Levator scapulae | lateral cervical ribs, with the neck muscles | anterior scapular border, anterodistal tip to glenohumeral joint, fleshy |
| Serratus (costoscapularis) | ventrolateral ribs | entire **medio-posterior** scapular margin, by tendon |
| Costocoracoideus profundus | lateral margin of the first few ribs | coracoid |
| Supracoracoideus | **proximo-lateral** coracoid, fleshy, covering the humeral head | **ventro-lateral** humerus at the deltopectoral crest, fleshy |
| Coracobrachialis brevis dorsalis | **antero-lateral and proximal** scapula, fleshy | proximal third of the **anterior** humerus near the deltopectoral crest |
| Scapulohumeralis caudalis | **proximo-lateral and posterior** scapula, fleshy | **proximo-lateral** humeral head, fleshy |

Functional attributions are given per muscle (shoulder extensor, abductor, joint stabiliser), which is a useful cross-check on the `action` fields.

## A homology note worth flagging

Klinkhamer et al. equate **scapulohumeralis caudalis with teres minor** (citing refs 11 and 23). That bears directly on this dataset's `scapulohumeralis-anterior` record, where the teres minor correspondence is marked `uncertain` and set against Romer's (1924) competing derivation from the procoracohumeralis. Their usage supports a scapulohumeralis derivation but does not settle which of anterior or posterior is involved, so the record's uncertainty stands.

## Limitations

- One species, and — as with any single-specimen digital dissection — no account of intraspecific variation.
- Contrast-enhanced CT resolves muscle bellies well but attachment *margins* less sharply than a scalpel does; the aspect terms are more reliable than the precise boundaries.
- No architectural data (PCSA, fascicle length, pennation), so it does not close the architecture gap.

## Relevance to this project

Primary source for crocodylian `side` values on the supracoracoideus, coracobrachialis, levator scapulae, serratus anterior, costocoracoideus and scapulohumeralis posterior. Together with Allen et al. (2014) it makes Crocodylia one of the better-attested attachment columns.
