# Freitas et al. (2017) — Pectoral girdle and forelimb muscles of *Iguana iguana*

## Citation

Freitas LM, Pereira DKS, Pereira KF, Santos OP, Lima FC. 2017. Muscular anatomy of
the pectoral girdle and forelimb of *Iguana i. iguana* (Squamata: Iguanidae).
*Bioscience Journal* 33(5): 1284–1294.

## Why it was reached for

**The only source here that dissects *Iguana* specifically.** The lepidosaur column
is otherwise built on varanids, on Osawa's tuatara, and on Abdala & Diogo's survey,
whose lepidosaur exemplar is *Timon lepidus*. An iguanid dissection is a different
animal, and under species-level scoring it gets its own rows rather than displacing
anyone.

## Taxa and material

**Two adult female *Iguana iguana***, post mortem, donated from a scientific
breeding facility and dissected — skin reflected, fasciae removed, muscles
individualised, fixed in 10% formaldehyde. One locality, so nothing here on
variation. The authors name Moro & Abdala (2004, 2006) and Jenkins & Goslow (1983)
for lizard nomenclature and Meers (2003) for crocodilian.

## Re-mine of 2026-08-20 — the accounting

**21 muscles identified, 20 filed, 1 parked.**

| | |
|---|---:|
| Muscles in tables 1–3, with an origin and an insertion | 20 |
| Identified in a figure and absent from the tables (`M. flexor carpi ulnaris`) | 1 |
| **Total the paper identifies** | **21** |
| Filed onto a record | 20 |
| Parked, `record: null` | 1 |

The parked row is `M. serratus thoracis`, on `blockedBy: "nomenclature"`. Freitas et
al. take it from the first two ribs to the caudal margin of the scapula; Russell &
Bauer's *Iguana* serratus complex is entirely cervical and ends on the suprascapula.
Either they number the anterior ribs differently, or this animal has a thoracic
serratus distinct from the cervical one. Abdala & Diogo (2010) Tables 1–3 would
settle it. Filing it on `serratus-anterior` would be assigning a record on the
strength of the word "serratus".

`M. flexor carpi ulnaris` is filed as present with **no attachments**, because the
paper labels it in figure 2 and omits it from table 3. An empty attachment set
reads as unrecorded; copying Russell & Bauer's origin onto a Freitas row would
assert an observation these authors did not publish.

### What the previous pass did, and why it was wrong

**It scored one row and wrote down a reason.** The note said most of what the paper
describes "was already scored for *Iguana* from Russell & Bauer (2008), which covers
the same animal in the same region at higher resolution", and that Freitas et al.
"confirm and supply a second observer rather than opening new ground".

Both halves of that are mistaken. The second observer *is* the ground: an
attachment is an observation, and `CLAUDE.md` is explicit that two workers who each
dissected an animal do not compete. And they do not merely confirm — on eight of
the twenty muscles the two dissections of this one animal disagree:

| Muscle | Russell & Bauer | Freitas et al. |
|---|---|---|
| Pectoralis | Two portions, superficial and deep; no rib but the posteriormost mesosternal | **Three** parts, ascendant/transverse/descendent; cranial margin of rib VI |
| Deltoideus clavicularis | Clavicle | **Interclavicle** |
| Deltoideus scapularis | Scapula, suprascapula and clavicle | Scapula only |
| Trapezius | One unit with the episternocleidomastoideus, skull → girdle | Trapezius alone, thoracodorsal fascia → cranial scapula |
| Latissimus dorsi | Neural spines only | Neural spines **and ribs I–V** |
| Levator scapulae | Transverse process of the atlas | Cervical ribs **and vertebral processes** |
| Biceps brachii | Digastric, one coracoid origin | **Two heads, the proximal from the humerus** |
| Extensor digitorum longus | Metacarpals | **Distal phalanges I–III** |
| Extensor carpi radialis | Two heads | Undivided |

None of that was recoverable from the dataset before this pass. The rows now carry
both readings — the join unions the attachments and keeps each source's paragraph —
so the disagreements are visible on the record rather than lost to whichever paper
was read first.

### What the paper is actually for

**The tendinous arc.** Freitas et al. report the long caudal head of the triceps
arising by a tendinous arc on the lateral surface of the shoulder, spanning scapula
to deltopectoral crest. That origin had been described **only in crocodilians**,
where the arc spans scapula to coracoid (Meers 2003; Romão et al. 2016). This is its
first report in a lizard, and it is the paper's own headline. It was entirely absent
from this dataset.

Two further points worth having:

- **They use Meers's crocodilian names for the four triceps heads**, deliberately,
  because they judge this animal's triceps closer to the crocodilian arrangement
  than the lizard one. That is why `triceps-brachii` now carries five names for one
  iguana muscle, and why the mapping layer matters: Russell & Bauer's scapular,
  coracoid, lateral humeral and medial humeral heads are the same four bellies.
- **They argue the group may not be a triceps at all**, and that deciding it needs
  ontogeny and innervation rather than topography.

### Read with care

- The **pronator teres** row in table 3 prints an insertion along the caudal margin
  of the humerus as well as on the radius. A pronator teres cannot insert on the
  bone it arises from and the discussion names only the radius, so the humeral
  phrase is not scored and the row says so.
- The **flexor digitorum longus** contradicts itself: the table gives two distinct
  origins, humeral and ulnar, and the discussion says no clear division into heads
  was observed. Both origins are scored — the muscle reaches both bones however few
  bellies it has — and the row records the tension.
- The **triceps brevis intermedius** is given a second tendon arising medially on
  the sternum. No other source here gives a triceps head a girdle origin. It is
  scored because the table states it plainly at both ends, and flagged on the row.
- "Cranial epicondyle" and "caudal epicondyle" are scored as ectepicondyle
  (`lateral-epicondyle`) and entepicondyle (`medial-epicondyle`). That is not a
  fresh inference: Freitas et al. equate their cranial epicondyle with the
  crocodilian origin Meers describes, and Russell & Bauer's rows for this same
  animal already put the extensors on the ectepicondyle and the flexors and
  pronators on the entepicondyle.
- "Episternum" is the interclavicle, and the pectoralis row carries it as such.

## Limitations

- **Two specimens, one locality.** Nothing here on variation.
- **Written as a descriptive anatomy paper**, not a comparative one, so it makes no
  homology claims and carries no `homologyScope`. Where it discusses other taxa it
  is reporting Jenkins & Goslow, Romer, Zaaf et al., Meers, Moro & Abdala, Casals et
  al. and Romão et al., not observing them; none of that is scored here.

## Relevance to comparative anatomy teaching

The green iguana is a common teaching animal and this is the paper that describes
its shoulder as such. It is also the best demonstration in the corpus of why one
source per animal is not enough: two competent dissections of the same species,
eight years apart, disagree about which bone the deltoid arises from. Pair with
**Russell & Bauer (2008)** for the same region across normal-limbed squamates and
the tuatara, and with **Zaaf et al. (1999)** for what varies between two geckos.
