/* Unit tests for the attachment-shift diff in assets/skeleton.js.
   Run: node tests/shifts.test.js  (exit 0 = pass)

   These exist because the diff compared elements only. `side` was dropped
   before comparison, so a muscle migrating from the ventral to the dorsal face
   of the same bone — a real shift, and one the row form was built to record —
   reported as no change at all. That is the failure mode worth pinning: a wrong
   answer that looks like a clean one. */

const fs = require('fs');
const path = require('path');

/* A small skeleton: humerus with two landmarks, plus unrelated bones and one
   fusion product standing in for the tarsometatarsus. */
const ELEMENTS = [
  { id: 'humerus', label: 'Humerus' },
  { id: 'deltopectoral-crest', label: 'Deltopectoral crest', partOf: 'humerus' },
  { id: 'greater-tubercle', label: 'Greater tubercle', partOf: 'humerus' },
  { id: 'scapula', label: 'Scapula', derivedFrom: 'scapulocoracoid' },
  /* Inside the scapula, and absent in the comparison taxon — the pair that
     separates "described more coarsely" from "the site is gone". */
  { id: 'suprascapula', label: 'Suprascapula', partOf: 'scapula',
    presence: { default: 'yes', absent: ['lepidosauria'] } },
  { id: 'coracoid', label: 'Coracoid', derivedFrom: 'scapulocoracoid' },
  /* Fission: one ancestral bone became two. Not containment, and not fusion. */
  { id: 'scapulocoracoid', label: 'Scapulocoracoid' },
  { id: 'metatarsals', label: 'Metatarsals' },
  { id: 'fossa-metatarsi-i', label: 'Fossa metatarsi I', partOf: 'metatarsals' },
  { id: 'distal-tarsals', label: 'Distal tarsals' },
  { id: 'tarsometatarsus', label: 'Tarsometatarsus',
    fusedFrom: ['distal-tarsals', 'metatarsals'] },
];

global.esc = s => String(s);
global.state = {
  elements: ELEMENTS,                      // fissionLine scans this for derivedFrom
  elementsById: new Map(ELEMENTS.map(e => [e.id, e])),
  taxonOrder: new Map([['caudata', 0], ['lepidosauria', 1], ['theria', 2]]),
};
eval(fs.readFileSync(path.join(__dirname, '..', 'assets', 'skeleton.js'), 'utf8'));

let failures = 0;

/* Builds a two-taxon muscle: caudata is always the reference (first on the
   taxon order), the second taxon is the one being compared against it. */
function shiftFor(refRows, cmpRows) {
  const muscle = { occurrences: [
    { taxon: 'caudata', attachments: refRows },
    { taxon: 'lepidosauria', attachments: cmpRows },
  ] };
  const analysis = attachmentShifts(muscle);
  return analysis ? analysis.shifts[0] || null : null;
}

function check(label, refRows, cmpRows, expected) {
  const s = shiftFor(refRows, cmpRows);
  const fmt = d => [
    ...d.gained.map(g => `+${g.id}`),
    ...d.lost.map(l => `-${l.id}`),
    ...d.refined.map(r => `~${r.from}>${r.to}`),
    ...d.moved.map(m => `${m.substantive ? '!' : '?'}${m.id}:${m.from.join('/')}>${m.to.join('/')}`),
    ...d.fused.map(f => `${f.separated ? '/' : '@'}${f.from}>${f.to}`),
    ...d.split.map(f => `%${f.from}>${f.to}`),
  ].join(',');
  const got = !s ? '(none)'
    : [`o[${fmt(s.origin)}]`, `i[${fmt(s.insertion)}]`,
       s.substantive ? 'substantive' : 'resolution-only'].join(' ');
  if (got === expected) { console.log(`  ok    ${label}`); return; }
  failures++;
  console.log(`  FAIL  ${label}`);
  console.log(`          got      ${got}`);
  console.log(`          expected ${expected}`);
}

console.log('Attachment shift diff');

/* --- what the diff already got right, pinned so it stays right --- */

check('identical attachments — no shift',
  { origin: [{ element: 'scapula' }], insertion: [{ element: 'humerus' }] },
  { origin: [{ element: 'scapula' }], insertion: [{ element: 'humerus' }] },
  '(none)');

check('different bone — gain and loss',
  { origin: [{ element: 'scapula' }] },
  { origin: [{ element: 'coracoid' }] },
  'o[+coracoid,-scapula] i[] substantive');

check('bone to landmark on that bone — a refinement, not a move',
  { insertion: [{ element: 'humerus' }] },
  { insertion: [{ element: 'humerus', landmark: 'greater-tubercle' }] },
  'o[] i[~humerus>greater-tubercle] resolution-only');

check('two landmarks on one bone — both reported',
  { origin: [{ element: 'humerus' }] },
  { origin: [{ element: 'humerus', landmark: 'greater-tubercle' },
             { element: 'humerus', landmark: 'deltopectoral-crest' }] },
  'o[~humerus>greater-tubercle,~humerus>deltopectoral-crest] i[] resolution-only');

/* The reverse of a refinement: the reference names the finer element and the
   comparison taxon names the bone it sits in. The finer element is NOT reported
   lost — one source simply described the site more coarsely than the other.

   (The bone is still reported gained, so a coarsening reads as a one-sided
   change. That asymmetry predates these tests and is pinned here rather than
   asserted to be right: `refined` has no reverse category.) */
check('landmark to the bone containing it — the landmark is not reported lost',
  { origin: [{ element: 'humerus', landmark: 'greater-tubercle' }] },
  { origin: [{ element: 'humerus' }] },
  'o[+humerus] i[] substantive');

/* Unless the taxon HAS no such landmark, in which case the loss is real and must
   survive. The salamander deltoideus scapularis arises from the suprascapular
   cartilage; crocodylians have no suprascapula, so its origin on the scapula
   proper is an attachment forced onto a new site by a vanished bone — the exact
   transition this table exists to surface. Suppressing it as "one source was
   vaguer" would delete the finding. */
check('landmark to its bone, where the taxon lacks the landmark — a real loss',
  { origin: [{ element: 'scapula', landmark: 'suprascapula' }] },
  { origin: [{ element: 'scapula' }] },
  'o[+scapula,-suprascapula] i[] substantive');

/* --- side: the reason this file exists --- */

check('same bone, opposite surfaces — a substantive move',
  { insertion: [{ element: 'humerus', side: 'ventral' }] },
  { insertion: [{ element: 'humerus', side: 'dorsal' }] },
  'o[] i[!humerus:ventral>dorsal] substantive');

check('same bone, same surface — no shift',
  { insertion: [{ element: 'humerus', side: 'ventral' }] },
  { insertion: [{ element: 'humerus', side: 'ventral' }] },
  '(none)');

/* An absent `side` means unrecorded, never "no side". Reading it as a
   difference would turn a gap in the literature into an evolutionary event. */
check('side recorded on one taxon only — unrecorded, not a move',
  { insertion: [{ element: 'humerus', side: 'ventral' }] },
  { insertion: [{ element: 'humerus' }] },
  '(none)');

check('neither taxon records a side — nothing to compare',
  { insertion: [{ element: 'humerus' }] },
  { insertion: [{ element: 'humerus' }] },
  '(none)');

/* Overlapping sets are as likely to be uneven reporting as a real narrowing,
   so they are shown but must not count as substantive. */
check('overlapping surfaces on one axis — reported, not substantive',
  { insertion: [{ element: 'humerus', side: 'dorsal' },
                { element: 'humerus', side: 'ventral' }] },
  { insertion: [{ element: 'humerus', side: 'dorsal' }] },
  'o[] i[?humerus:dorsal/ventral>dorsal] resolution-only');

/* --- side terms live on four independent axes --- */

/* The case that made this necessary: iliofibularis on the fibula, recorded
   "posterior" in Caudata and "proximal" in Lepidosauria. Treating the two as
   alternatives reported a migration that no source claims — one author named a
   surface, the other named a position along the bone. */
check('sides on different axes — not comparable, no move',
  { insertion: [{ element: 'humerus', side: 'posterior' }] },
  { insertion: [{ element: 'humerus', side: 'proximal' }] },
  '(none)');

check('two axes each disjoint — one move per axis',
  { origin: [{ element: 'humerus', side: 'dorsal' },
             { element: 'humerus', side: 'proximal' }] },
  { origin: [{ element: 'humerus', side: 'ventral' },
             { element: 'humerus', side: 'distal' }] },
  'o[!humerus:proximal>distal,!humerus:dorsal>ventral] i[] substantive');

/* One axis agrees, the other is recorded on one taxon only. Nothing to report:
   the agreeing axis is unchanged and the other is simply unrecorded. */
check('one axis agrees, the other unrecorded in one taxon — no move',
  { origin: [{ element: 'humerus', side: 'posterior' },
             { element: 'humerus', side: 'lateral' }] },
  { origin: [{ element: 'humerus', side: 'posterior' }] },
  '(none)');

/* --- one element, several rows: count bones, not rows --- */

/* Three rows for one bone because three of its surfaces are scored is still
   one bone lost. The old diff printed "− Humerus, Humerus, Humerus". */
check('bone scored on three surfaces then lost — reported once',
  { insertion: [{ element: 'humerus', side: 'dorsal' },
                { element: 'humerus', side: 'ventral' },
                { element: 'humerus', side: 'anterior' }] },
  { insertion: [{ element: 'scapula' }] },
  'o[] i[+scapula,-humerus] substantive');

check('bone gained on three surfaces — reported once',
  { insertion: [{ element: 'scapula' }] },
  { insertion: [{ element: 'humerus', side: 'dorsal' },
                { element: 'humerus', side: 'ventral' },
                { element: 'humerus', side: 'anterior' }] },
  'o[] i[+humerus,-scapula] substantive');

/* --- fusion: the skeleton changed, not the attachment --- */

/* The live case. Tibialis anterior inserts on the metatarsals in a crocodylian
   and on the tarsometatarsus in a bird. While the tarsometatarsus hung off the
   metatarsals by `partOf`, this reported as a refinement — the same category as
   humerus to greater tubercle, i.e. one author being more precise. It is a bone
   that has absorbed its neighbours. */
check('component to the compound that absorbed it — a fusion, not a refinement',
  { insertion: [{ element: 'metatarsals' }] },
  { insertion: [{ element: 'tarsometatarsus' }] },
  'o[] i[@metatarsals>tarsometatarsus] resolution-only');

check('landmark inside an absorbed component — still a fusion',
  { insertion: [{ element: 'metatarsals', landmark: 'fossa-metatarsi-i' }] },
  { insertion: [{ element: 'tarsometatarsus' }] },
  'o[] i[@fossa-metatarsi-i>tarsometatarsus] resolution-only');

/* Reading it the other way round must not invent a gain plus a loss. The
   reference taxon is whichever one is scored first on the topology, so it is
   often the fused one and the comparison runs backwards. */
check('compound to component — unfused here, not a gain and a loss',
  { insertion: [{ element: 'tarsometatarsus' }] },
  { insertion: [{ element: 'metatarsals' }] },
  'o[] i[/tarsometatarsus>metatarsals] resolution-only');

/* A fusion is a fact about the skeleton. It must not be dressed up as the
   muscle having moved, or every avian hindlimb record would report a shift. */
check('fusion alone is never substantive',
  { origin: [{ element: 'distal-tarsals' }], insertion: [{ element: 'metatarsals' }] },
  { origin: [{ element: 'tarsometatarsus' }], insertion: [{ element: 'tarsometatarsus' }] },
  'o[@distal-tarsals>tarsometatarsus] i[@metatarsals>tarsometatarsus] resolution-only');

/* But a real move alongside a fusion still counts. */
check('a genuine gain alongside a fusion stays substantive',
  { insertion: [{ element: 'metatarsals' }] },
  { insertion: [{ element: 'tarsometatarsus' }, { element: 'scapula' }] },
  'o[] i[+scapula,@metatarsals>tarsometatarsus] substantive');

/* Unrelated bones must not be swept into the fusion just because the compound
   exists in the same skeleton. */
check('an unabsorbed bone is still a gain and a loss',
  { insertion: [{ element: 'humerus' }] },
  { insertion: [{ element: 'tarsometatarsus' }] },
  'o[] i[+tarsometatarsus,-humerus] substantive');

/* --- fission: `derivedFrom`, the third element relation --- */

/* The scapulocoracoid became the scapula and the coracoid. A muscle scored on
   one and then the other has not moved — the bone under it divided — so this is
   a change in the skeleton, exactly like a fusion, and must not count as an
   attachment shift. Before `derivedFrom` was traversable this reported as a
   gain plus a loss at the fin-to-limb boundary. */
check('ancestral element to one of its fission products — a split, not a move',
  { origin: [{ element: 'scapulocoracoid' }] },
  { origin: [{ element: 'scapula' }] },
  'o[%scapulocoracoid>scapula] i[] resolution-only');

check('and the other way round, since the reference may be the divided one',
  { origin: [{ element: 'scapula' }] },
  { origin: [{ element: 'scapulocoracoid' }] },
  'o[%scapula>scapulocoracoid] i[] resolution-only');

/* Siblings are NOT the same element. Both descend from the scapulocoracoid, but
   a muscle moving from the coracoid to the scapula inside tetrapods has really
   moved — that is the therian supracoracoideus, the best-documented attachment
   change in the dataset, and folding the two together would erase it. */
check('between two products of the same fission — a real move',
  { origin: [{ element: 'coracoid' }] },
  { origin: [{ element: 'scapula' }] },
  'o[+scapula,-coracoid] i[] substantive');

/* --- reference selection --- */

(function referenceIsEarliestScored() {
  const muscle = { occurrences: [
    { taxon: 'theria', attachments: { origin: [{ element: 'scapula' }] } },
    { taxon: 'caudata', attachments: { origin: [{ element: 'coracoid' }] } },
  ] };
  const a = attachmentShifts(muscle);
  const ok = a && a.reference === 'caudata';
  console.log(`  ${ok ? 'ok   ' : 'FAIL '} reference is the earliest taxon with data, not file order`);
  if (!ok) failures++;
})();

(function singleScoredTaxonYieldsNothing() {
  const muscle = { occurrences: [
    { taxon: 'caudata', attachments: { origin: [{ element: 'scapula' }] } },
    { taxon: 'theria' },
  ] };
  const ok = attachmentShifts(muscle) === null;
  console.log(`  ${ok ? 'ok   ' : 'FAIL '} one scored taxon yields no shift`);
  if (!ok) failures++;
})();

console.log(failures ? `\n${failures} failing` : '\nall passing');
process.exit(failures ? 1 : 0);
