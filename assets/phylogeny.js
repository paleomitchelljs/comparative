/* Phylogeny view: character mapping over the taxon topology.
   Loaded after app.js and skeleton.js; shares the `state` object. */

/* ---------- the tree ---------- */

/* taxa.json holds the topology as nested objects. Everything here works on that
   directly rather than on a flattened list, because branch inference needs
   parents and children. */
function treeRoot() {
  return state.topology;
}

function annotateTree(node, depth = 0) {
  node._depth = depth;
  node._children = node.children || [];
  node._children.forEach(c => { c._parent = node; annotateTree(c, depth + 1); });
  node._tips = node.taxon ? [node] : node._children.flatMap(c => c._tips);
  return node;
}

function allNodes(node, out = []) {
  out.push(node);
  (node._children || []).forEach(c => allNodes(c, out));
  return out;
}

/* ---------- character states ---------- */

/* The dataset's five presence values do not reduce cleanly to present/absent.
   `variable` means a source found the muscle in some species of the clade and
   not others — scoring it either way would manufacture a transition. `inferred`
   is a fossil reconstruction, not an observation. Both are treated as
   POLYMORPHIC/UNKNOWN for optimisation: they constrain nothing and inherit
   whatever the rest of the tree implies. */
const STATE_PRESENT = 1, STATE_ABSENT = 0;

function tipStates(muscle) {
  const out = new Map();
  for (const occ of muscle.occurrences || []) {
    const p = occ.present || 'yes';
    if (p === 'yes') out.set(occ.taxon, new Set([STATE_PRESENT]));
    else if (p === 'no') out.set(occ.taxon, new Set([STATE_ABSENT]));
    else out.set(occ.taxon, new Set([STATE_ABSENT, STATE_PRESENT]));   // variable / uncertain / inferred
  }
  return out;
}

/* Fitch parsimony, two passes over a fixed topology.

   Down-pass: a node's state set is the intersection of its children's sets, or
   their union if the intersection is empty (a union marks a change on one of the
   child branches). Up-pass: resolve each node against its parent where possible.

   This is genuinely ancestral-state optimisation rather than eyeballing the
   column, which matters because the alternative — reading gains and losses
   straight off the tip states — invents transitions wherever a taxon simply was
   not sampled. Taxa with no occurrence row are left unscored and contribute
   nothing, which is the correct treatment of missing data. */
function fitch(root, tips) {
  const down = new Map();

  (function downPass(n) {
    if (n.taxon) {
      down.set(n, tips.get(n.taxon) || null);          // null = not scored
      return down.get(n);
    }
    const kids = n._children.map(downPass).filter(Boolean);
    if (!kids.length) { down.set(n, null); return null; }
    if (kids.length === 1) { down.set(n, new Set(kids[0])); return down.get(n); }
    const inter = kids.reduce((a, b) => new Set([...a].filter(x => b.has(x))));
    const set = inter.size ? inter : kids.reduce((a, b) => new Set([...a, ...b]));
    down.set(n, set);
    return set;
  })(root);

  /* At the root the down-pass set is often {absent, present} — both states are
     equally parsimonious and Fitch cannot choose. Defaulting to ABSENT is the
     defensible convention here: these are muscles, acquired along lineages, and
     the alternative (assume the vertebrate ancestor had everything) would turn
     every appearance into a loss somewhere else. The choice is recorded so the
     interface can say so. */
  const rootSet = down.get(root);
  const rootAmbiguous = !!rootSet && rootSet.size > 1;
  const rootState = !rootSet ? null
    : rootSet.has(STATE_ABSENT) ? STATE_ABSENT : [...rootSet][0];

  const final = new Map();
  const equivocal = new Set();

  (function upPass(n, parentState) {
    const mine = down.get(n);
    if (!mine) { final.set(n, null); (n._children || []).forEach(c => upPass(c, parentState)); return; }
    let resolved;
    if (parentState == null) {
      resolved = mine.size === 1 ? [...mine][0] : rootState;
    } else if (mine.has(parentState)) {
      resolved = parentState;                      // parent forces it: not ambiguous
    } else {
      // Neither state is implied by the parent. If more than one is available we
      // are choosing, and that choice is a convention rather than a result.
      if (mine.size > 1) equivocal.add(n);
      resolved = mine.size === 1 ? [...mine][0] : parentState;
    }
    final.set(n, resolved);
    (n._children || []).forEach(c => upPass(c, resolved));
  })(root, null);

  return { states: final, equivocal, rootAmbiguous, rootState };
}

/* Branch-level changes for one muscle: where along the tree did it appear or
   disappear, given the optimisation above. A change on a branch whose parent or
   child state was equivocal is flagged, because its exact placement is a
   convention rather than a result. */
function transitionsFor(muscle, root) {
  const { states, equivocal, rootAmbiguous } = fitch(root, tipStates(muscle));

  const events = [];
  for (const n of allNodes(root)) {
    const parent = n._parent;
    if (!parent) continue;
    const a = states.get(parent), b = states.get(n);
    if (a == null || b == null || a === b) continue;
    events.push({
      node: n,
      kind: b === STATE_PRESENT ? 'gain' : 'loss',
      /* An ambiguous root makes every event for this character
         convention-dependent: flip the root state and gains become losses
         elsewhere at the same cost. */
      equivocal: rootAmbiguous || equivocal.has(n)
    });
  }
  return { states, events, rootAmbiguous };
}

/* Subdivision events come from the curated `derivatives` edges, not from
   optimisation: an ancestral fin muscle giving rise to several tetrapod muscles
   is a claim in the sources, not something inferable from a presence column. */
function subdivisionsAt(node) {
  if (node.taxon) return [];
  return [];
}

/* ---------- aggregate over a selected set of muscles ---------- */

function phyloSummary(muscles) {
  const root = annotateTree(structuredClone(treeRoot()));
  const byNode = new Map();
  const ensure = n => byNode.get(n) || byNode.set(n, { gains: [], losses: [], equivocal: 0 }).get(n);
  let equivocalTotal = 0;

  for (const m of muscles) {
    const { events } = transitionsFor(m, root);
    for (const e of events) {
      const slot = ensure(e.node);
      slot[e.kind === 'gain' ? 'gains' : 'losses'].push(m);
      if (e.equivocal) { slot.equivocal++; equivocalTotal++; }
    }
  }
  return { root, byNode, equivocalTotal };
}

/* ---------- layout ---------- */

/* Rectangular cladogram. Tips are evenly spaced on y; x is depth. Sixteen tips
   is small enough that a plain recursive layout beats anything cleverer. */
function layout(root, { rowH = 34, colW = 148, padX = 12, padY = 26 } = {}) {
  const tips = root._tips;
  tips.forEach((t, i) => { t._y = padY + i * rowH; });
  const maxDepth = Math.max(...allNodes(root).map(n => n._depth));

  (function place(n) {
    n._x = padX + n._depth * colW;
    if (n.taxon) return n._y;
    const ys = n._children.map(place);
    n._y = (Math.min(...ys) + Math.max(...ys)) / 2;
    return n._y;
  })(root);

  // Tips sit flush at the right so the taxon labels line up.
  const tipX = padX + maxDepth * colW;
  tips.forEach(t => { t._x = tipX; });

  return { width: tipX, height: padY * 2 + (tips.length - 1) * rowH, tipX };
}

/* ---------- rendering ---------- */

function renderPhylogeny() {
  const scope = state.phyloScope || 'all';
  const muscles = phyloMuscles(scope);
  const { root, byNode, equivocalTotal } = phyloSummary(muscles);
  const dims = layout(root);
  const nodes = allNodes(root);

  const maxEvents = Math.max(1, ...nodes.map(n => {
    const e = byNode.get(n); return e ? e.gains.length + e.losses.length : 0;
  }));

  const edges = nodes.filter(n => n._parent).map(n => {
    const p = n._parent;
    const e = byNode.get(n) || { gains: [], losses: [] };
    const total = e.gains.length + e.losses.length;
    const w = 1.5 + 4.5 * (total / maxEvents);
    const net = e.gains.length - e.losses.length;
    const stroke = total === 0 ? 'var(--rule-strong)'
      : net > 0 ? 'var(--ok)' : net < 0 ? 'var(--warn)' : 'var(--mod)';
    return `<path d="M${p._x} ${p._y} L${p._x} ${n._y} L${n._x} ${n._y}"
      fill="none" stroke="${stroke}" stroke-width="${total ? w : 1.5}"
      stroke-linejoin="round" opacity="${total ? 1 : 0.55}"/>`;
  }).join('');

  const badges = nodes.filter(n => n._parent).map(n => {
    const e = byNode.get(n); if (!e) return '';
    const total = e.gains.length + e.losses.length;
    if (!total) return '';
    const mx = (n._parent._x + n._x) / 2;
    const label = [e.gains.length ? `+${e.gains.length}` : '', e.losses.length ? `−${e.losses.length}` : '']
      .filter(Boolean).join(' ');
    const eq = e.equivocal === total && total > 0;   // every change here is convention-dependent
    return `<g class="phylo-badge${eq ? ' equivocal' : ''}" data-node="${esc(nodeKey(n))}" tabindex="0">
      <rect x="${mx - 26}" y="${n._y - 20}" width="52" height="15" rx="7"></rect>
      <text x="${mx}" y="${n._y - 9}" text-anchor="middle">${esc(label)}${eq ? '?' : ''}</text></g>`;
  }).join('');

  const labels = nodes.map(n => {
    if (n.taxon) {
      const t = state.taxaById.get(n.taxon) || {};
      const mc = t.muscleCount ? ` <tspan class="mc">${t.muscleCount.total}</tspan>` : '';
      return `<g class="phylo-tip" data-taxon="${esc(n.taxon)}">
        <rect x="${n._x + 6}" y="${n._y - 9}" width="8" height="8" rx="2" fill="${esc(t.color || '#999')}"/>
        <text x="${n._x + 20}" y="${n._y + 4}">${esc(n.name)}${mc}</text></g>`;
    }
    return `<text class="phylo-internal" x="${n._x + 5}" y="${n._y - 7}">${esc(n.name)}</text>`;
  }).join('');

  const svg = `<svg viewBox="0 0 ${dims.width + 260} ${dims.height}"
      width="100%" style="max-width:${dims.width + 260}px" class="phylotree"
      role="img" aria-label="Cladogram with muscle gains and losses per branch">
      ${edges}${badges}${labels}</svg>`;

  return `
    ${renderPhyloControls(scope, muscles.length)}
    <div class="callout caution"><h4>What this is, and is not</h4>
      <p>Branch states are optimised by <strong>Fitch parsimony</strong> over the fixed
      topology in <code>taxa.json</code>, not read off the tip states. A muscle with no
      occurrence row for a taxon is left unscored and constrains nothing — treating
      absence of data as absence of the muscle would invent losses wherever sampling
      is thin, which is most of the fish end of this tree.</p>
      <p><strong>Polymorphic tips.</strong> <code>variable</code>, <code>uncertain</code> and
      <code>inferred</code> are scored as {absent, present} rather than forced either way.
      <code>variable</code> means a source found the muscle in some species of a clade and
      not others; <code>inferred</code> is a fossil reconstruction. Neither is an observation
      of presence, and neither should push a transition onto a branch by itself.</p>
      <p><strong>Equivocal placements</strong> are marked with <code>?</code> on the tree and
      flagged in the table below. They arise where the state at the root of the tree is
      itself ambiguous — both states cost the same number of steps — so the convention
      used here (absent at the root, since muscles are acquired rather than primitively
      universal) decides where the change is drawn. Flip that assumption and the gains
      become losses elsewhere at identical cost.
      ${equivocalTotal ? `<strong>${equivocalTotal}</strong> of the changes shown are equivocal in this sense.` : ''}</p>
      <p><strong>One topology, no support.</strong> The tree is a pragmatic consensus —
      including Abdala &amp; Diogo's placement of turtles as archosauromorphs — and the
      counts would change under a different one. There are no branch supports here
      because none are computed.</p>
    </div>
    <div class="tablewrap phylowrap">${svg}</div>
    ${renderPhyloLegend()}
    ${renderPhyloDetail(root, byNode)}
    ${renderCountTrajectory()}`;
}

const nodeKey = n => n.taxon || `int:${n.name}`;

function phyloMuscles(scope) {
  if (scope === 'all') return state.muscles;
  const [kind, val] = scope.split(':');
  return state.muscles.filter(m =>
    kind === 'region' ? m.region === val :
    kind === 'mass' ? m.mass === val :
    kind === 'segment' ? m.segment === val : true);
}

function renderPhyloControls(scope, n) {
  const opt = (v, label) => `<option value="${esc(v)}" ${v === scope ? 'selected' : ''}>${esc(label)}</option>`;
  const regions = [...new Set(state.muscles.map(m => m.region))].sort(
    (a, b) => regionRank(a) - regionRank(b));
  const masses = [...new Set(state.muscles.map(m => m.mass).filter(Boolean))].sort();
  return `<div class="taxonbar">
    <label for="phylo-scope">Map</label>
    <select id="phylo-scope">
      ${opt('all', `all ${state.muscles.length} muscles`)}
      <optgroup label="by region">${regions.map(r => opt(`region:${r}`, r)).join('')}</optgroup>
      <optgroup label="by developmental mass">${masses.map(m => opt(`mass:${m}`, m)).join('')}</optgroup>
    </select>
    <span class="sep">${n} muscle${n === 1 ? '' : 's'} mapped</span>
  </div>`;
}

const renderPhyloLegend = () => `
  <div class="phylolegend">
    <span><i style="background:var(--ok)"></i> net gains on branch</span>
    <span><i style="background:var(--warn)"></i> net losses</span>
    <span><i style="background:var(--mod)"></i> equal gains and losses</span>
    <span><i style="background:var(--rule-strong)"></i> no inferred change</span>
    <span class="sep">Branch thickness scales with the number of changes.</span>
  </div>`;

function renderPhyloDetail(root, byNode) {
  const rows = allNodes(root).filter(n => n._parent && byNode.get(n))
    .map(n => ({ n, e: byNode.get(n) }))
    .filter(r => r.e.gains.length + r.e.losses.length)
    .sort((a, b) => (b.e.gains.length + b.e.losses.length) - (a.e.gains.length + a.e.losses.length));
  if (!rows.length) return `<p class="cellnote">No transitions inferred for this selection.</p>`;

  const pill = m => `<a class="pill" data-goto="${m.id}">${esc(m.name)}</a>`;
  return `<section class="block"><h3>Inferred changes by branch</h3>
    <div class="tablewrap"><table class="occ">
      <colgroup><col style="width:22%"><col style="width:78%"></colgroup>
      <thead><tr><th>Branch leading to</th><th>Changes</th></tr></thead><tbody>
      ${rows.map(({ n, e }) => `<tr>
        <td><span class="clade">${esc(n.name)}</span>
          <span class="common">${e.gains.length} gain${e.gains.length === 1 ? '' : 's'},
            ${e.losses.length} loss${e.losses.length === 1 ? '' : 'es'}</span>
          ${e.equivocal ? `<span class="chip conf-moderate">${e.equivocal} equivocal</span>` : ''}</td>
        <td>
          ${e.gains.length ? `<div class="grp"><b class="gain">gained</b>
            <div class="pills">${e.gains.map(pill).join('')}</div></div>` : ''}
          ${e.losses.length ? `<div class="grp"><b class="loss">lost</b>
            <div class="pills">${e.losses.map(pill).join('')}</div></div>` : ''}
        </td></tr>`).join('')}
    </tbody></table></div></section>`;
}

/* The published per-appendage muscle counts, which tell a story the presence
   matrix cannot: the big jump happens BEFORE the sarcopterygian LCA, not at the
   origin of tetrapods. */
function renderCountTrajectory() {
  const withCounts = [...state.taxa].filter(t => t.muscleCount)
    .sort((a, b) => (state.taxonOrder.get(a.id) ?? 99) - (state.taxonOrder.get(b.id) ?? 99));
  if (!withCounts.length) return '';
  const max = Math.max(...withCounts.map(t => t.muscleCount.total));

  return `<section class="block"><h3>Published muscle counts per appendage pair</h3>
    <div class="counttraj">
      ${withCounts.map(t => {
        const c = t.muscleCount;
        const w = 100 * c.total / max;
        return `<div class="ctrow">
          <span class="ctname">${esc(t.clade)}</span>
          <span class="ctbar"><i style="width:${w}%;background:${esc(t.color)}"></i></span>
          <span class="ctval">${c.total}<span class="sep"> = ${c.pectoral} + ${c.pelvic}</span>
            ${c.excludingAutopod ? `<span class="sep"> · ${c.excludingAutopod.total} excl. autopod</span>` : ''}</span>
        </div>`;
      }).join('')}
    </div>
    <p class="cellnote">Counts are Diogo et al. (2016) for their exemplar species, not counts of
    records in this dataset. The interesting comparison is <em>Polypterus</em> → <em>Latimeria</em>
    (a jump of 23) against <em>Latimeria</em> → <em>Ambystoma</em> excluding the autopod
    (a jump of 20): most of the change had already happened before the sarcopterygian
    last common ancestor.</p>
  </section>`;
}
