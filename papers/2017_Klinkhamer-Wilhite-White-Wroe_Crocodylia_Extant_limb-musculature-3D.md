# Klinkhamer et al. 2017 — digital dissection of *Crocodylus porosus* limb musculature

## Citation

Klinkhamer AJ, Wilhite DR, White MA, Wroe S. 2017. Digital dissection and three-dimensional interactive models of limb musculature in the Australian estuarine crocodile (*Crocodylus porosus*). *PLoS ONE*. DOI: 10.1371/journal.pone.0175079. **Open access.**

## Question

Can digital dissection deliver limb muscle anatomy in a form that is both more detailed and more reusable than a traditional destructive dissection?

## Taxa and material

*Crocodylus porosus*, fore- and hindlimb, segmented into interactive 3D models.
**Two** sub-adult males: XCb Cp4 (2.1 m), which was scanned, and XCb Cp5, which
was dissected fresh. Both from Koorana Crocodile Farm, Queensland.

**The method is CT plus MRI, not contrast-enhanced CT.** This note and
`sources.json` both said contrast-enhanced for a while; the paper says the
opposite in as many words — "since it was not possible to use the iodine staining
method in this study due to the size of the specimens" — and its discussion
contrasts the combined CT/MRI approach with "digital dissections using
contrast-enhancing agents like iodine". The distinction matters for how much
weight the attachment margins carry: MRI "does limit the capacity to identify
small structures like tendons", which the authors say was "particularly evident
when assessing the muscles of the hand and foot and in identifying attachment
sites".

## The limitation that governs how this paper can be scored

Some muscles are missing from it for reasons of preparation, not anatomy, and
their absence here is **not** evidence of absence in the animal:

> "During the fresh-tissue dissection it became obvious that some of the large
> superficial dorsal muscles of the forelimb had been removed during the skinning
> process for both animals. It was therefore not possible to identify or model
> these muscles."

Those are the **trapezius, latissimus dorsi, rhomboideus and serratus ventralis
cervicis**. In the hindlimb the same skinning cost the **flexor digitorum brevis,
pronator quadratus and extensor hallucis longus**.

And the reason so many distal attachments read as "the manus" or "the pes":

> "Some muscles stretching into the manus and pes did retain their insertions even
> with skinning. Therefore we have included specific detail about insertions of
> those muscles, but for the muscles whose insertions were compromised we have
> left the description more general, simply describing insertion as 'into the
> manus/pes'."

So **"the dorsal manus" is a record of a severed insertion, not a coarse one.**
Reading a carpal or a metacarpal out of it asserts what the authors were careful
not to. `flexor-carpi-ulnaris` and `extensor-antebrachii-carpi-ulnaris` had done
exactly that — one landing on `carpals`, the other on `metacarpals`, from the same
phrase — and now carry no insertion row, which reads correctly as unrecorded.
Where they *do* name a site (pronator teres on the ventral carpals, fibularis
brevis on metatarsal 3, tibialis anterior on digits 2 and 3), it is scored.

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

## The findings, which this note used to omit entirely

Klinkhamer et al. report their differences from other crocodilians explicitly, and
every one of them is a scoreable observation:

| | *C. porosus* | Compared with |
|---|---|---|
| **Triceps longus medialis** | **one** tendon of origin, scapular | scapular **+ coracoid** in *Alligator* and other taxa. **Their only forelimb difference** |
| **Ambiens** | **one** head | two in *A. mississippiensis* — but they attribute this to **sub-adult specimens, not species**, so it must not be recorded as a *C. porosus* character |
| **Iliofibularis** | no secondary tendon | a secondary tendon to gastrocnemius internus in *Alligator*, *C. latirostris* |
| **Pubo-ischio-femoralis internus 2** | **one** insertion | two in *Caiman* |
| **Gastrocnemius externus** | origin on the **caudofemoralis longus tendon** | lateral condyle of the femur in *Alligator* |
| **Extensor digitorum brevis** | origin on the **distal fibula** | the astragalus in *Alligator* |
| **Flexor digitorum longus** (hl) | **one** part | two in some *A. mississippiensis* accounts |
| **Flexor cruris group** | **four** parts (FTI1–4) | three in some *Alligator*/*C. latirostris* accounts |

Two of these are still unscored and are the obvious next bite: the gastrocnemius
externus origin (a muscle taking origin from another muscle's tendon, so possibly
no skeletal origin row at all) and the extensor digitorum brevis shift.

## Limitations

- One species; two specimens, both sub-adult males, so no account of adult
  morphology — which is what the ambiens head count turns on.
- **Muscles destroyed in skinning, and severed distal insertions** — see above. This
  is the limitation that most constrains scoring, and it was missing from this note.
- CT plus MRI resolves muscle bellies well but attachment *margins* less sharply
  than a scalpel does; the aspect terms are more reliable than the precise
  boundaries, and the authors say so for the hand and foot in particular.
- No architectural data (PCSA, fascicle length, pennation), so it does not close the architecture gap.

## Relevance to this project

Primary source for crocodylian `side` values on the supracoracoideus, coracobrachialis, levator scapulae, serratus anterior, costocoracoideus and scapulohumeralis posterior. Together with Allen et al. (2014) it makes Crocodylia one of the better-attested attachment columns.
