/* Kinematics for the muscle simulator. No DOM: the browser page and
   tests/sim.test.js load the same file.

   A MODEL is one region of one taxon: rigid segments in a parent chain, a few
   degrees of freedom (DOFs) that move them, landmarks pinned to segments, and
   muscles that are polylines through landmarks. Everything a muscle "does" is
   derived from that geometry -- a muscle shortens when moving a DOF in one
   direction brings its ends closer, and the joints it crosses are the DOFs that
   change its length. Nothing here says what a muscle does; the model data says
   where it attaches, and `tests/sim.test.js` checks that the answer agrees with
   the source.

   Coordinates are SVG user units, y down. Landmarks may carry a z (towards the
   viewer) so a transverse muscle such as the intermandibularis has a real
   length in a lateral view; z is used for lengths and never drawn.

   A POSE is { dofId: u } with u normalised: u = 1 is range[1], u = -1 is
   range[0], u = 0 is the rest posture. A DOF whose range starts at 0 cannot be
   negative. Poses are the one shared currency between panels, so a slider
   written "jaw" moves every taxon that has a jaw. */

(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SimEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------- 2D affine, [a b c d e f] as in SVG matrix() ---------- */

  const IDENT = [1, 0, 0, 1, 0, 0];
  const mul = (m, n) => [
    m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1],
    m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3],
    m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]];
  const apply = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];

  /* Positive angle is clockwise on screen, so with the snout to the right a
     positive rotation of a forward-pointing bar lowers its tip. */
  function rotAbout(deg, px, py) {
    const t = deg * Math.PI / 180, c = Math.cos(t), s = Math.sin(t);
    return [c, s, -s, c, px - (c * px - s * py), py - (s * px + c * py)];
  }
  const trans = (tx, ty) => [1, 0, 0, 1, tx, ty];
  function scaleAlong(factor, ax, ay, ux, uy) {
    const k = factor - 1;
    const a = 1 + k * ux * ux, b = k * ux * uy, d = 1 + k * uy * uy;
    return [a, b, b, d, ax - (a * ax + b * ay), ay - (b * ax + d * ay)];
  }

  /* ---------- model ---------- */

  function build(raw) {
    const m = Object.assign({}, raw);
    m.segById = new Map(raw.segments.map(s => [s.id, s]));
    m.dofById = new Map(raw.dofs.map(d => [d.id, d]));
    m.lmById = new Map(Object.entries(raw.landmarks));
    m.muscleById = new Map(raw.muscles.map(x => [x.id, x]));

    // parents before children, whatever order the file lists them in
    m.order = [];
    const seen = new Set();
    const visit = id => {
      if (seen.has(id)) return;
      const s = m.segById.get(id);
      if (!s) throw new Error(`${raw.id}: unknown segment ${id}`);
      if (s.parent) visit(s.parent);
      seen.add(id); m.order.push(s);
    };
    raw.segments.forEach(s => visit(s.id));

    m.drivesBySeg = new Map();
    for (const d of raw.dofs) {
      for (const dr of d.drives) {
        if (!m.segById.has(dr.segment)) throw new Error(`${raw.id}: dof ${d.id} drives unknown segment ${dr.segment}`);
        if (!m.drivesBySeg.has(dr.segment)) m.drivesBySeg.set(dr.segment, []);
        m.drivesBySeg.get(dr.segment).push({ dof: d, drive: dr });
      }
    }
    for (const [id, lm] of m.lmById) {
      if (!m.segById.has(lm.segment)) throw new Error(`${raw.id}: landmark ${id} on unknown segment ${lm.segment}`);
    }
    for (const mu of raw.muscles) {
      for (const path of mu.paths || []) for (const l of path) {
        if (!m.lmById.has(l)) throw new Error(`${raw.id}: muscle ${mu.id} uses unknown landmark ${l}`);
      }
    }
    m.rest = null;
    m.rest = lengths(m, {});
    return m;
  }

  const uMin = dof => (dof.range[0] < 0 ? -1 : 0);
  const clampU = (dof, u) => Math.max(uMin(dof), Math.min(1, u));

  /* normalised -> native (degrees or units) */
  function nativeValue(dof, u) {
    u = clampU(dof, u);
    return u >= 0 ? u * dof.range[1] : u * -dof.range[0];
  }

  function driveMatrix(dr, v) {
    if (dr.type === 'rotation') return rotAbout((dr.sign || 1) * v, dr.pivot[0], dr.pivot[1]);
    if (dr.type === 'translation') return trans(dr.axis[0] * v, dr.axis[1] * v);
    if (dr.type === 'scale') return scaleAlong(1 - dr.k * v, dr.anchor[0], dr.anchor[1], dr.axis[0], dr.axis[1]);
    throw new Error(`unknown drive type ${dr.type}`);
  }

  /* segment id -> matrix taking rest coordinates to current coordinates */
  function matrices(model, pose) {
    const mats = new Map();
    for (const seg of model.order) {
      let M = seg.parent ? mats.get(seg.parent) : IDENT;
      for (const { dof, drive } of model.drivesBySeg.get(seg.id) || []) {
        const u = pose[dof.id] || 0;
        if (u !== 0) M = mul(M, driveMatrix(drive, nativeValue(dof, u)));
      }
      mats.set(seg.id, M);
    }
    return mats;
  }

  function landmarkAt(model, mats, id) {
    const lm = model.lmById.get(id);
    const [x, y] = apply(mats.get(lm.segment), lm.at[0], lm.at[1]);
    return [x, y, lm.at[2] || 0];
  }

  const dist3 = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);

  /* A muscle with several fibre groups reports their mean: the lever arms are
     similar by construction and one number is what a reader can compare. */
  function muscleLength(model, mats, mu) {
    let sum = 0;
    for (const path of mu.paths) {
      const pts = path.map(l => landmarkAt(model, mats, l));
      for (let i = 1; i < pts.length; i++) sum += dist3(pts[i - 1], pts[i]);
    }
    return sum / mu.paths.length;
  }

  function lengths(model, pose) {
    const mats = matrices(model, pose);
    const out = {};
    for (const mu of model.muscles) if (mu.paths && mu.paths.length) out[mu.id] = muscleLength(model, mats, mu);
    return out;
  }

  /* Relative length: 0 at rest, -0.2 is 20% shorter. */
  function strains(model, pose) {
    const L = lengths(model, pose), out = {};
    for (const id in L) out[id] = L[id] / model.rest[id] - 1;
    return out;
  }

  /* ---------- what a muscle does ---------- */

  /* d(relative length)/du for one DOF, centred where the DOF allows it. A
     negative value means the muscle shortens as that DOF increases. */
  function slope(model, mu, pose, dofId, h = 0.02) {
    const dof = model.dofById.get(dofId);
    const u0 = pose[dofId] || 0;
    const lo = Math.max(uMin(dof), u0 - h), hi = Math.min(1, u0 + h);
    if (hi <= lo) return 0;
    const f = u => lengths(model, Object.assign({}, pose, { [dofId]: u }))[mu.id];
    return (f(hi) - f(lo)) / (hi - lo) / model.rest[mu.id];
  }

  /* Every DOF the muscle's length responds to, with the sign and size. This is
     the "joints it crosses", derived rather than asserted. */
  function effects(model, mu, pose, eps = 0.02) {
    const out = [];
    for (const dof of model.dofs) {
      // a mid-range pose for the slope, so a DOF at its stop is not read as inert
      const p = Object.assign({}, pose);
      if (!p[dof.id]) p[dof.id] = uMin(dof) < 0 ? 0 : 0.5;
      const s = slope(model, mu, p, dof.id);
      if (Math.abs(s) > eps) out.push({ dof: dof.id, slope: s, shortensWith: s < 0 ? 1 : -1 });
    }
    return out;
  }

  /* The pose in which a muscle is longest, over the joints it crosses: the
     natural place for it to start contracting. An adductor starts with the jaw
     open, not closed, because from closed there is nowhere left to shorten. */
  function stretchedPose(model, mu, base = {}) {
    const p = Object.assign({}, base);
    for (const e of effects(model, mu, base)) {
      p[e.dof] = e.slope > 0 ? 1 : uMin(model.dofById.get(e.dof));
    }
    return p;
  }

  /* The path an action takes in one DOF: [from, to] in normalised units.
     "Open" runs rest -> amount. "Close" runs amount -> rest, because a jaw has
     no negative range to close into; where there IS negative range (a labial
     cartilage that retracts as well as protracts) the negative action runs
     rest -> -amount instead. */
  function actionRange(model, dofId, dir, amount) {
    const dof = model.dofById.get(dofId);
    if (dir > 0) return [0, amount];
    return uMin(dof) < 0 ? [0, -amount] : [amount, 0];
  }

  function actionRole(model, mu, dofId, dir, amount, base = {}) {
    const [a, b] = actionRange(model, dofId, dir, amount);
    const L0 = lengths(model, Object.assign({}, base, { [dofId]: a }))[mu.id];
    const L1 = lengths(model, Object.assign({}, base, { [dofId]: b }))[mu.id];
    const rel = (L1 - L0) / L0;
    return { rel, role: rel < -0.02 ? 'shortens' : rel > 0.02 ? 'lengthens' : 'none' };
  }

  /* One muscle contracting on its own: gradient descent on its length over
     every DOF it affects, from the pose given, stopping at the joint limits or
     when it has shortened by `maxShorten`. Returns the poses along the way so a
     slider can scrub it. Unopposed, so it shows the pull and not the
     equilibrium; the DOF ranges set how far each joint is allowed to give. */
  function contraction(model, mu, start, { maxShorten = 0.22, step = 0.02, maxSteps = 120 } = {}) {
    const poses = [Object.assign({}, start)];
    const L0 = lengths(model, start)[mu.id];
    let p = Object.assign({}, start);
    for (let i = 0; i < maxSteps; i++) {
      const g = {};
      let norm = 0;
      for (const dof of model.dofs) {
        const u = p[dof.id] || 0;
        let s = slope(model, mu, p, dof.id, 0.01);
        // at a stop, a push further into it is no push
        if ((u >= 1 && s < 0) || (u <= uMin(dof) && s > 0)) s = 0;
        g[dof.id] = -s; norm += s * s;
      }
      norm = Math.sqrt(norm);
      if (norm < 1e-4) break;
      const q = Object.assign({}, p);
      for (const dof of model.dofs) {
        if (g[dof.id]) q[dof.id] = clampU(dof, (p[dof.id] || 0) + step * g[dof.id] / norm);
      }
      p = q;
      poses.push(p);
      if (lengths(model, p)[mu.id] <= L0 * (1 - maxShorten)) break;
    }
    return poses;
  }

  /* Dragging a handle: the u that puts the landmark nearest the pointer. */
  function dragSolve(model, pose, dofId, landmarkId, x, y, samples = 90) {
    const dof = model.dofById.get(dofId);
    let best = pose[dofId] || 0, bestD = Infinity;
    for (let i = 0; i <= samples; i++) {
      const u = uMin(dof) + (1 - uMin(dof)) * i / samples;
      const mats = matrices(model, Object.assign({}, pose, { [dofId]: u }));
      const [lx, ly] = landmarkAt(model, mats, landmarkId);
      const d = Math.hypot(lx - x, ly - y);
      if (d < bestD) { bestD = d; best = u; }
    }
    return best;
  }

  /* Linear blend of two poses, for animating towards a target. */
  const lerpPose = (a, b, t) => {
    const out = {};
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) out[k] = (a[k] || 0) + ((b[k] || 0) - (a[k] || 0)) * t;
    return out;
  };

  return {
    build, matrices, landmarkAt, lengths, strains, slope, effects, stretchedPose, actionRange,
    actionRole, contraction, dragSolve, lerpPose, nativeValue, clampU, uMin, muscleLength,
  };
});
