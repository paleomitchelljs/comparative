# Jones, Button, Barrett & Porro (2019) — Digital dissection of the pigeon head

*Zoological Letters* 5:17. doi:10.1186/s40851-019-0129-z. Open access.
Source key: `jones-etal-2019`

## Why it was reached for

Cranial was the thinnest region in the dataset and **Aves had no cranial attachment
data at all** — what was there had come from a turtle paper and was lifted out in the
base-layer pass. Measured 5.0 origin/insertion mentions per page against the 6.3
recorded in `MINING.md`; still comfortably a descriptive myology, and its structure
is better than the density suggests, because every muscle gets an explicit
`Origin:` / `Path:` / `Insertion:` / `Function:`.

**Cranial 35% → 46%. Aves 42% → 49%.**

## One specimen, and the authors' own caution about it

A deceased, previously frozen adult *Columba livia* of 242 g, contrast-enhanced and
CT scanned three times. Their caution is worth carrying into the species note: *C.
livia* includes some 350 breeds, so "the pigeon" is a wide target, and their
descriptions differ in places from earlier accounts **of the same species**.

## Scored (10 rows, 33 named parts)

| Record | Pigeon name | Parts |
|---|---|---:|
| `adductor-mandibulae` | the complex | 4 |
| `adductor-mandibulae-externus` | m. AME | 3 |
| `adductor-mandibulae-posterior` | m. AMP | — |
| `adductor-mandibulae-internus` | pseudotemporalis + pterygoideus | 4 |
| `levator-arcus-palatini` | m. protractor pterygoidei et quadrati | — |
| `depressor-mandibulae` | m. DM | — |
| `intermandibularis` | m. mylohyoideus | — |
| `interhyoideus` | serpihyoideus + stylohyoideus | 2 |
| `hypobranchial-muscles` | the tongue and throat series | 8 |
| `extraocular-muscles` | recti, obliqui, palpebrae, nictitans | 11 |

Eight bellies makes `hypobranchial-muscles` the most divided this record is in any
taxon, and eleven makes the same true of `extraocular-muscles`.

## What the CT adds that a dissection did not

**The nerve's course through the muscle.** The m. AME lies lateral to both CN V2 and
CN V3 in this specimen, where in amniotes it usually lies *between* them; the
pseudotemporalis profundus bifurcates around CN V3 close to its insertion, which is
how the nerve reaches the Meckelian groove. Both are in the occurrence notes.

**Boundaries earlier workers could not separate.** The m. AMEP is distinct from the
m. AMP on both sides (contra van Gennip 1986), and the AMP is clearly separate from
the pseudotemporalis profundus, unlike the arrangement reported for *Columba
palumbus*. They also record that the homology of the externus partes across amniotes
has been questioned outright — the same caution Johnston (2011, 2014) raises.

## Two judgement calls, both recorded in the rows

**The postorbital process is scored on the squamosal.** The pars medialis arises by
three aponeuroses, one from the postorbital process and two from the zygomatic
process. Birds have no separate postorbital *bone*, and `skeleton.json` records it
as absent in Aves — so a row on `postorbital` would have been a validation error
rather than an observation. The processes are named in the note.

**The m. protractor pterygoidei et quadrati went on `levator-arcus-palatini`**, whose
other rows are a shark's levator palatoquadrati and spiracularis. It is the record's
first amniote row and the identification rests on position and CN V innervation
rather than on any source here asserting the homology, which the note says. Its
function has no counterpart in the record's other taxa: it protracts the
pterygoid–quadrate–maxillopalatine complex and opens the **upper** jaw.

## Where a bird's head is not bone

Three attachments deliberately stop short of a landmark:

- the **depressor mandibulae** also arises from the postorbital *ligament*, and
  inserts over an area of the jaw wider than the retroarticular process the record's
  consensus names;
- the **mylohyoideus** inserts into the *median raphe*, exactly as the shark's
  intermandibularis does in Huber et al. — two of the three taxa on that record now
  end at a raphe, which is why the muscle is invisible to osteological
  reconstruction at its medial end in any clade;
- most **recti** arise from a thickened periorbital *membrane*, so the orbit rows are
  the bony frame of the origin rather than the origin.

## One element added

`paraglossum` (entoglossum), `partOf` the hyoid and present in Aves — the tongue
skeleton the intrinsic lingual muscles attach to.

## Still in it

The neck muscles, which are a large part of the paper and would pair with Boumans et
al. (2015) on *Tyto*; the glands and the ten ligaments of Tables 2–3, including L2,
which carries part of the depressor mandibulae origin; and the ceratohyoideus and
branchiomandibularis, currently folded into the hypobranchial row as parts because no
source here separates them as homology groups.
