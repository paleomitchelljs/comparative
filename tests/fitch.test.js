/* Unit tests for the Fitch parsimony implementation in assets/phylogeny.js.
   Run: node tests/fitch.test.js  (exit 0 = pass)

   These exist because the first implementation silently reported "no change"
   whenever the root state was ambiguous, which is the one failure mode that
   looks like a clean result. */

const fs = require('fs');
const path = require('path');

global.state = { taxa: [], taxaById: new Map(), taxonOrder: new Map(), muscles: [], topology: null };
global.esc = s => String(s);
global.regionRank = () => 0;
eval(fs.readFileSync(path.join(__dirname, '..', 'assets', 'phylogeny.js'), 'utf8'));

const TREE = { name: 'root', children: [
  { name: 'AB', children: [{ name: 'A', taxon: 'a' }, { name: 'B', taxon: 'b' }] },
  { name: 'CD', children: [{ name: 'C', taxon: 'c' }, { name: 'D', taxon: 'd' }] }] };

let failures = 0;

function check(label, states, expected, { steps } = {}) {
  const root = annotateTree(structuredClone(TREE));
  const muscle = { occurrences: Object.entries(states).map(([taxon, present]) => ({ taxon, present })) };
  const { events } = transitionsFor(muscle, root);
  const got = events.map(e => `${e.kind}@${e.node.name}`).sort().join(',') || '(none)';
  const okEvents = got === expected;
  const okSteps = steps === undefined || events.length === steps;
  if (okEvents && okSteps) { console.log(`  ok    ${label}`); return; }
  failures++;
  console.log(`  FAIL  ${label}`);
  console.log(`          got      ${got}${steps !== undefined ? ` (${events.length} steps)` : ''}`);
  console.log(`          expected ${expected}${steps !== undefined ? ` (${steps} steps)` : ''}`);
}

console.log('Fitch parsimony over ((A,B),(C,D))');

check('all present — no change', { a: 'yes', b: 'yes', c: 'yes', d: 'yes' }, '(none)');
check('single absent tip — one loss on that tip', { a: 'yes', b: 'yes', c: 'yes', d: 'no' }, 'loss@D');

/* The point of parsimony: ONE change on a stem, not two on the tips. Which stem
   is genuinely ambiguous here — "gained in AB" and "lost in CD" both cost one
   step — so the absent-root convention decides, and the step count is what the
   test actually pins down. */
check('clade split — one change on a stem, not two on tips',
      { a: 'yes', b: 'yes', c: 'no', d: 'no' }, 'gain@AB', { steps: 1 });

check('present in one clade only — one gain on that stem',
      { a: 'no', b: 'no', c: 'yes', d: 'yes' }, 'gain@CD', { steps: 1 });

// Missing data must not become evidence of absence.
check('unsampled tip constrains nothing', { a: 'yes', b: 'yes', c: 'yes' }, '(none)');
check('all unsampled — nothing inferred', {}, '(none)');

// Polymorphic tips inherit rather than forcing a transition.
check('variable tip forces nothing', { a: 'yes', b: 'yes', c: 'yes', d: 'variable' }, '(none)');
check('inferred tip forces nothing', { a: 'no', b: 'no', c: 'no', d: 'inferred' }, '(none)');
check('uncertain tip forces nothing', { a: 'yes', b: 'yes', c: 'yes', d: 'uncertain' }, '(none)');

/* Genuinely ambiguous: two gains and two losses both cost two steps. The
   documented convention is an ABSENT root, so this must resolve to gains — and
   both must be flagged equivocal so the interface can say the placement is a
   convention. */
check('ambiguous 2–2 split resolves to gains under the absent-root convention',
      { a: 'no', b: 'yes', c: 'yes', d: 'no' }, 'gain@B,gain@C', { steps: 2 });

(function equivocalFlagged() {
  const root = annotateTree(structuredClone(TREE));
  const muscle = { occurrences: [
    { taxon: 'a', present: 'no' }, { taxon: 'b', present: 'yes' },
    { taxon: 'c', present: 'yes' }, { taxon: 'd', present: 'no' }] };
  const { events } = transitionsFor(muscle, root);
  const allFlagged = events.length > 0 && events.every(e => e.equivocal);
  console.log(`  ${allFlagged ? 'ok   ' : 'FAIL '} ambiguous placements are flagged equivocal`);
  if (!allFlagged) failures++;
})();

(function unambiguousNotFlagged() {
  const root = annotateTree(structuredClone(TREE));
  const muscle = { occurrences: [
    { taxon: 'a', present: 'yes' }, { taxon: 'b', present: 'yes' },
    { taxon: 'c', present: 'yes' }, { taxon: 'd', present: 'no' }] };
  const { events } = transitionsFor(muscle, root);
  const clean = events.length === 1 && !events[0].equivocal;
  console.log(`  ${clean ? 'ok   ' : 'FAIL '} unambiguous placements are not flagged`);
  if (!clean) failures++;
})();

console.log(failures ? `\n${failures} failing` : '\nall passing');
process.exit(failures ? 1 : 0);
