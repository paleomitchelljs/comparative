/* Tests for the muscle simulator: the kinematics engine, and the models in
   data/sim/ against the sources they claim to follow.
   Run: node tests/sim.test.js  (exit 0 = pass)

   The engine derives what a muscle does from where it attaches, so a model can
   be internally consistent and still wrong -- a drawing in which the
   preorbitalis opens the jaw would animate perfectly. What stops that is the
   `expect` list on each muscle: the action the cited source credits it with.
   This test moves every degree of freedom and checks that the geometry
   reproduces every expectation, so a landmark nudged for looks cannot quietly
   reverse a muscle.

   It also checks the references: every record, element, joint, group and
   source a model names must exist, because the page would render a dangling
   one without complaint. */

const fs = require('fs');
const path = require('path');
const E = require('../assets/sim/engine.js');

const ROOT = path.join(__dirname, '..');
const load = p => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));

let failures = 0;
const check = (label, ok, detail) => {
  console.log(`  ${ok ? 'ok   ' : 'FAIL '} ${label}`);
  if (!ok) { if (detail) console.log(`        ${detail}`); failures++; }
};

/* ---------- engine ---------- */

console.log('Engine');

const toy = E.build({
  id: 'toy',
  segments: [
    { id: 'base', parent: null, paths: [] },
    { id: 'arm', parent: 'base', paths: [] },
    { id: 'slider', parent: 'arm', paths: [] },
  ],
  dofs: [
    { id: 'hinge', range: [0, 90], drives: [{ segment: 'arm', type: 'rotation', pivot: [0, 0], sign: 1 }] },
    { id: 'slide', range: [0, 10], drives: [{ segment: 'slider', type: 'translation', axis: [1, 0] }] },
    { id: 'both', range: [-30, 30], drives: [{ segment: 'arm', type: 'rotation', pivot: [0, 0], sign: 1 }] },
  ],
  landmarks: {
    anchor: { segment: 'base', at: [0, -10, 0] },
    tip: { segment: 'arm', at: [10, 0, 0] },
    ride: { segment: 'slider', at: [10, 0, 0] },
    off: { segment: 'base', at: [0, 0, 5] },
  },
  muscles: [{ id: 'm', paths: [['anchor', 'tip']] }],
});

const near = (a, b, tol = 1e-6) => Math.abs(a - b) < tol;
{
  const m1 = E.matrices(toy, { hinge: 1 });
  const [x, y] = E.landmarkAt(toy, m1, 'tip');
  // positive rotation is clockwise on screen, so +x swings to +y
  check('positive rotation is clockwise (y down)', near(x, 0, 1e-9) && near(y, 10, 1e-9), `got ${x}, ${y}`);
}
{
  const m1 = E.matrices(toy, { hinge: 1, slide: 1 });
  const [x, y] = E.landmarkAt(toy, m1, 'ride');
  // the slider is in the arm's frame, so it rides the rotation
  check('a child segment carries its parent\'s rotation', near(x, 0, 1e-9) && near(y, 20, 1e-9), `got ${x}, ${y}`);
}
check('u = 1 is range[1]', near(E.nativeValue(toy.dofById.get('hinge'), 1), 90));
check('a one-sided range has no negative u', E.clampU(toy.dofById.get('hinge'), -1) === 0);
check('a two-sided range reaches range[0]', near(E.nativeValue(toy.dofById.get('both'), -1), -30));
check('z counts towards length',
  near(E.muscleLength(toy, E.matrices(toy, {}), { paths: [['off', 'tip']] }), Math.hypot(10, 5)));

{
  const mu = toy.muscleById.get('m');
  const s = E.slope(toy, mu, { hinge: 0.5 }, 'hinge');
  // swinging the tip away from the anchor lengthens the muscle
  check('slope: rotating away from the anchor lengthens', s > 0, `slope ${s}`);
  const path = E.contraction(toy, mu, { hinge: 1 });
  const last = path[path.length - 1];
  check('contraction runs towards a shorter muscle', last.hinge < 1, JSON.stringify(last));
  check('contraction stops at the joint limit', last.hinge >= 0);
  // 'hinge' is already at its stop, so only the two-sided 'both' can give
  const stuck = E.contraction(toy, mu, { hinge: 0 });
  check('at a joint limit only the free joint moves',
    (stuck[stuck.length - 1].both || 0) < 0 && !stuck[stuck.length - 1].hinge);
}

/* ---------- models against the dataset ---------- */

const index = load('data/sim/index.json');
const skeleton = new Set(load('data/skeleton.json').elements.map(e => e.id));
const sources = new Set(load('data/sources.json').sources.map(s => s.key));
const joints = new Set(load('data/joints.json').joints.map(j => j.id));
const records = new Set();
for (const f of fs.readdirSync(path.join(ROOT, 'data')).filter(f => /^muscles-.*\.json$/.test(f))) {
  for (const m of load(`data/${f}`).muscles) records.add(m.id);
}
const species = new Set(load('data/species.json').species.map(s => s.id));
const jointIds = new Set(index.joints.map(j => j.id));
const groupIds = new Set(index.groups.map(g => g.id));

console.log('\nRegistry');
{
  const dupes = index.regions.map(r => r.id).filter((id, i, a) => a.indexOf(id) !== i);
  check('region ids are unique', dupes.length === 0, dupes.join(', '));
  for (const j of index.joints) {
    if (j.joint) check(`joint ${j.id} names a joint in joints.json`, joints.has(j.joint), j.joint);
  }
  check('no more than four taxa can be compared and at least two are offered per available region',
    index.maxTaxa === 4 && index.regions.filter(r => r.status === 'available').every(r => r.models.length >= 2));
}

for (const region of index.regions.filter(r => r.status === 'available')) {
  for (const id of region.models) {
    const raw = load(`data/sim/${id}.json`);
    console.log(`\n${id}`);

    let model;
    try { model = E.build(raw); check('builds', true); }
    catch (e) { check('builds', false, e.message); continue; }

    check('file name matches id and region', raw.id === id && id.startsWith(raw.region + '-') && raw.region === region.id);
    check('species exists', species.has(raw.species), raw.species);
    check('every source is in sources.json', raw.sources.every(s => sources.has(s)),
      raw.sources.filter(s => !sources.has(s)).join(', '));

    const els = [
      ...raw.segments.map(s => s.element),
      ...(raw.links || []).map(l => l.element),
      ...Object.values(raw.landmarks).map(l => l.element),
    ].filter(Boolean);
    const badEls = els.filter(e => !skeleton.has(e));
    check('every element resolves in skeleton.json', badEls.length === 0, badEls.join(', '));

    check('every DOF is a known joint', raw.dofs.every(d => jointIds.has(d.id)),
      raw.dofs.filter(d => !jointIds.has(d.id)).map(d => d.id).join(', '));
    check('every handle is a landmark', raw.dofs.every(d => !d.handle || model.lmById.has(d.handle)));

    const dofIds = new Set(raw.dofs.map(d => d.id));
    for (const mu of raw.muscles) {
      const tag = mu.id;
      check(`${tag}: group is in the registry`, groupIds.has(mu.group), mu.group);
      check(`${tag}: record resolves`, mu.record === null || records.has(mu.record), mu.record);
      check(`${tag}: sources are in sources.json`, (mu.sources || []).length > 0 && mu.sources.every(s => sources.has(s)));

      const simulated = mu.paths && mu.paths.length > 0;
      if (!simulated) {
        check(`${tag}: a muscle that is not drawn says why`, !!mu.reason);
        check(`${tag}: status is one of recorded, contested, absent`, ['recorded', 'contested', 'absent'].includes(mu.status));
        continue;
      }
      check(`${tag}: a drawn muscle is recorded and has an expected action`,
        mu.status === 'recorded' && Array.isArray(mu.expect) && mu.expect.length > 0);

      // 1. the geometry reproduces the action the source credits
      const eff = E.effects(model, mu, {});
      for (const x of mu.expect || []) {
        check(`${tag}: ${x.dir > 0 ? 'moves' : 'returns'} ${x.dof} the way ${mu.sources[0]} says`,
          dofIds.has(x.dof) && eff.some(e => e.dof === x.dof && e.shortensWith === x.dir),
          `effects: ${eff.map(e => `${e.dof}:${e.slope.toFixed(2)}`).join(' ') || 'none'}`);
      }

      // 2. unopposed from its stretched state, it moves each expected joint the right way
      const stretched = E.stretchedPose(model, mu);
      const run = E.contraction(model, mu, stretched);
      const end = run[run.length - 1];
      for (const x of mu.expect || []) {
        const moved = ((end[x.dof] || 0) - (stretched[x.dof] || 0)) * x.dir;
        check(`${tag}: contracting from stretch moves ${x.dof} ${x.dir > 0 ? 'up' : 'down'}`, moved > 0.05,
          `moved ${moved.toFixed(3)}`);
      }

      // 3. nothing degenerate across the whole range of motion
      const allMax = {}, allMin = {};
      for (const d of raw.dofs) { allMax[d.id] = 1; allMin[d.id] = E.uMin(d); }
      const bad = [allMax, allMin].some(p => {
        const L = E.lengths(model, p)[mu.id];
        return !Number.isFinite(L) || L < 4;
      });
      check(`${tag}: stays a sensible length across the range`, !bad);
    }
  }
}

console.log(failures ? `\n${failures} failing` : '\nall passing');
process.exit(failures ? 1 : 0);
