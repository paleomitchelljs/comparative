/* Unit tests for the search index and ranking in assets/app.js.
   Run: node tests/search.test.js  (exit 0 = pass)

   These exist because widening the index to the prose fields is the change
   most likely to break quietly. Indexing an action string means a record whose
   description merely contains "flexes" competes with one actually NAMED
   "flexor", and both are word-prefix matches that the raw score cannot tell
   apart. If the penalty bands ever collapse, search still returns results —
   just the wrong ones first, which is the failure mode nobody notices. */

const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, '..', 'assets', 'app.js'), 'utf8');

/* app.js boots against the DOM at the bottom of the file; take the pure search
   half, which is everything up to the filtering section. */
const cut = src.indexOf('/* ---------- filtering ---------- */');
if (cut === -1) throw new Error('could not find the filtering section marker');

/* `const` inside a direct eval stays scoped to the eval, so app.js's own
   `const state` would be invisible here. Demote it to an implicit global so
   the test can load muscles into the same object buildIndex reads. Function
   declarations do leak out, which is why buildIndex and search need no such
   treatment. */
const head = src.slice(0, cut);
if (!/^const state = \{/m.test(head)) {
  throw new Error('app.js no longer declares `const state = {` — update this shim');
}

global.esc = s => String(s);
eval(head.replace(/^const state = \{/m, 'state = {'));
Object.assign(state, { index: [], taxaById: new Map(), elementsById: new Map() });

const MUSCLES = [
  { id: 'flexor-carpi-ulnaris', name: 'Flexor carpi ulnaris', region: 'forearm',
    consensus: { action: 'Flexes and adducts the wrist.' } },
  { id: 'iliofemoralis', name: 'Iliofemoralis', region: 'thigh', mass: 'dorsal',
    consensus: { action: 'Abducts the femur; flexes the hip.',
                 innervation: 'Femoral nerve (L2–L4).' },
    occurrences: [{ taxon: 'theria', name: 'Gluteus medius + gluteus minimus',
                    division: 'divided',
                    parts: [{ name: 'Gluteus medius' }, { name: 'Gluteus minimus' }] }] },
  { id: 'adductor-mandibulae', name: 'Adductor mandibulae', region: 'cranial',
    mass: 'branchiomeric',
    synonyms: ['Capiti-mandibularis (older usage)'],
    consensus: { innervation: 'Trigeminal nerve (CN V), mandibular division.' },
    developmental: 'Branchiomeric; first pharyngeal arch.' },
];

state.taxaById = new Map([['theria', { clade: 'Theria' }]]);
state.muscles = MUSCLES;
buildIndex();

let failures = 0;
const ok = (cond, label, detail) => {
  console.log(`  ${cond ? 'ok   ' : 'FAIL '} ${label}`);
  if (!cond) { failures++; if (detail) console.log(`          ${detail}`); }
};

console.log('Search index and ranking');

/* --- the fields that used to return nothing --- */

(() => {
  const r = search('femoral nerve');
  ok(r.length === 1 && r[0].muscle.id === 'iliofemoralis',
     'innervation is searchable', `got ${r.map(x => x.muscle.id).join(',') || '(none)'}`);
  ok(r[0] && r[0].hit.kind === 'innervation',
     'and the card can say it matched the innervation');
})();

(() => {
  const r = search('abducts');
  ok(r.length === 1 && r[0].muscle.id === 'iliofemoralis',
     'action is searchable');
})();

(() => {
  const r = search('branchiomeric');
  ok(r.length === 1 && r[0].muscle.id === 'adductor-mandibulae',
     'classification terms are searchable');
})();

(() => {
  const r = search('gluteus');
  ok(r.length === 1 && r[0].muscle.id === 'iliofemoralis',
     'a part name finds its homology group');
  ok(r[0] && r[0].hit.extra === 'Theria',
     'and reports which taxon calls it that');
})();

/* --- ranking: the reason the penalty bands exist --- */

(() => {
  const r = search('flex');
  const ids = r.map(x => x.muscle.id);
  ok(ids[0] === 'flexor-carpi-ulnaris',
     'a name beats a description containing the same word',
     `order was ${ids.join(' > ')}`);
  ok(ids.includes('iliofemoralis'),
     'but the description match is still returned');
})();

(() => {
  const r = search('mandibularis');
  ok(r[0] && r[0].muscle.id === 'adductor-mandibulae' && r[0].hit.kind === 'synonym',
     'a synonym ranks with names, not with prose');
})();

(() => {
  /* An exact match on prose must still lose to a weak match on a name, or a
     long description can hijack a query aimed at a muscle. */
  const nameHit = scoreTerm('flexor carpi ulnaris', 'flex', ['flex'], 'name');
  const proseExact = scoreTerm('flex', 'flex', ['flex'], 'action');
  ok(nameHit < proseExact,
     'the weakest name match still outranks an exact prose match',
     `name ${nameHit} vs prose ${proseExact}`);
})();

(() => {
  const unknown = scoreTerm('x', 'x', ['x'], 'something-new');
  const prose = scoreTerm('x', 'x', ['x'], 'action');
  ok(unknown === prose,
     'an unknown term kind defaults to the prose band, never to the name band');
})();

/* --- specificity: the tiebreak within a band --- */

(() => {
  /* Both are word-prefix hits on a taxon name, so the match classes are equal
     and only length separates them. An occurrence name that enumerated a dozen
     muscles used to tie with a record actually called that, and won on the
     alphabetical fallback. */
  const bare = scoreTerm('tenuissimus', 'tenuissimus', ['tenuissimus'], 'taxon-name');
  const buried = scoreTerm(
    'part of triceps extensor antebrachii et carpi ulnaris forelimb tenuissimus ' +
    'extensor cruris et tarsi fibularis hindlimb',
    'tenuissimus', ['tenuissimus'], 'taxon-name');
  ok(bare < buried, 'a bare name beats the same word buried in a long one',
     `bare ${bare} vs buried ${buried}`);
})();

(() => {
  /* And it must never reorder across bands: the longest possible name still
     outranks the shortest possible prose match. */
  const longName = scoreTerm('x'.repeat(500), 'x', ['x'], 'name');
  const shortProse = scoreTerm('x', 'x', ['x'], 'action');
  ok(longName < shortProse,
     'specificity never lets a name fall into the prose band',
     `name ${longName} vs prose ${shortProse}`);
})();

/* --- no false positives --- */

(() => {
  ok(search('zzzznotathing').length === 0, 'a miss returns nothing');
  const r = search('');
  ok(r.length === MUSCLES.length && r.every(x => x.hit === null),
     'an empty query returns everything, unranked');
})();

console.log(failures ? `\n${failures} failing` : '\nall passing');
process.exit(failures ? 1 : 0);
