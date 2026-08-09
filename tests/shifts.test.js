/* Unit tests for the attachment-shift diff in assets/skeleton.js.
   Run: node tests/shifts.test.js  (exit 0 = pass)

   These exist because the diff compared elements only. `side` was dropped
   before comparison, so a muscle migrating from the ventral to the dorsal face
   of the same bone — a real shift, and one the row form was built to record —
   reported as no change at all. That is the failure mode worth pinning: a wrong
   answer that looks like a clean one. */

const fs = require('fs');
const path = require('path');

/* A small skeleton: humerus with two landmarks, plus an unrelated bone. */
const ELEMENTS = [
  { id: 'humerus', label: 'Humerus' },
  { id: 'deltopectoral-crest', label: 'Deltopectoral crest', partOf: 'humerus' },
  { id: 'greater-tubercle', label: 'Greater tubercle', partOf: 'humerus' },
  { id: 'scapula', label: 'Scapula' },
  { id: 'coracoid', label: 'Coracoid' },
];

global.esc = s => String(s);
global.state = {
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
