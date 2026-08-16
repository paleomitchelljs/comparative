/* Bone-first navigation and attachment-shift analysis.
   Loaded after app.js; shares the `state` object. */

/* ---------- attachment rows ---------- */

/* An attachment row is { element, side?, landmark? }. The landmark is always
   inside the element, so a row reads bone -> side -> landmark and a muscle
   touching several sides or landmarks of one bone contributes several rows. */

const rowKey = r => `${r.element}|${r.side || ''}|${r.landmark || ''}`;

/* Every element a row touches, bone and landmark alike — used for lookup so
   asking about the humerus finds muscles recorded on the deltopectoral crest. */
const rowElements = r => [r.element, r.landmark].filter(Boolean);

function rowLabel(r) {
  const el = state.elementsById.get(r.element);
  const lm = r.landmark ? state.elementsById.get(r.landmark) : null;
  const bone = esc(el?.label || r.element);
  if (!lm && !r.side) return bone;
  const bits = [];
  if (r.side) bits.push(`<span class="side">${esc(r.side)}</span>`);
  if (lm) bits.push(`<span class="landmark">${esc(lm.label)}</span>`);
  return `${bone} <span class="rowsep">›</span> ${bits.join(' <span class="rowsep">›</span> ')}`;
}

/* ---------- attachment resolution ---------- */

/* An occurrence either carries its own structured attachments (documented for
   that taxon) or falls back to the muscle-level consensus. The distinction is
   surfaced, never silently collapsed: `inherited` means nobody has recorded
   attachments for that taxon, not that they are known to match. */
function attachmentsFor(muscle, taxonId) {
  /* A clade may hold several rows now — one per species — so "the attachments
     for Aves" is a question with more than one answer. Take the first SCORED
     row: a clade whose species disagree about where a muscle attaches is a
     finding, and the muscle page's by-species table is where it is shown, not
     here. Selecting the species instead gives that species' rows exactly. */
  const rows = (muscle.occurrences || []).filter(
    o => o.species === taxonId || o.taxon === taxonId);
  const occ = rows.find(o => o.attachments) || rows[0];
  if (occ && occ.attachments) {
    return { ...occ.attachments, inherited: false, note: occ.attachmentNote, sources: occ.sources };
  }
  const cons = muscle.attachments || {};

  // Inheriting the consensus into a taxon that lacks the bone would assert
  // something false — that a mammal's coracobrachialis arises from a coracoid.
  // Drop those and report them, so the interface can say the attachment is
  // unrecorded for this taxon rather than quietly inventing it.
  if (!taxonId) {
    return { origin: cons.origin || [], insertion: cons.insertion || [], inherited: true };
  }
  const rowOK = r => rowElements(r).every(id => elementPresentIn(id, taxonId) !== 'no');
  const keep = list => (list || []).filter(rowOK);
  const dropped = [...(cons.origin || []), ...(cons.insertion || [])].filter(r => !rowOK(r));

  return {
    origin: keep(cons.origin),
    insertion: keep(cons.insertion),
    inherited: true,
    unresolved: dropped
  };
}

/* The plesiomorphic reference for a shift comparison: the earliest taxon on the
   topology with recorded attachments. Caudata held that place for most of the
   forelimb until the stem-tetrapodomorph column was scored from Molnar et al.
   (2018), and now thirteen muscles are diffed against a fossil instead — which
   is the intended behaviour, since a Devonian scar is genuinely earlier evidence
   than a salamander dissection, and the heading names the reference either way.

   `uncertain` rows are excluded. That state means the source itself declines to
   call the identification settled — for Eusthenopteron, Molnar et al. report
   "no compelling evidence" that the latissimus dorsi, coracobrachialis or
   subcoracoscapularis existed as separate muscles — and making such a row the
   baseline would report every tetrapod as having shifted away from an attachment
   nobody stands behind. This is the same rule phylogeny.js applies when it
   refuses to let `uncertain` drive a transition; `inferred` stays eligible,
   because a reconstruction is a positive claim about a specimen. */
function referenceTaxonFor(muscle) {
  const documented = (muscle.occurrences || [])
    .filter(o => o.attachments && o.present !== 'uncertain')
    .sort((a, b) => (state.taxonOrder.get(a.taxon) ?? 99) - (state.taxonOrder.get(b.taxon) ?? 99));
  return documented.length ? documented[0].taxon : null;   // clade-level reference
}

/* Ancestor chain through partOf, inclusive of the element itself. */
function elementLineage(id) {
  const out = [];
  let cur = id;
  while (cur) {
    out.push(cur);
    cur = state.elementsById.get(cur)?.partOf;
  }
  return out;
}

const isWithin = (a, b) => elementLineage(a).includes(b);

/* Everything that went into an element, transitively. Distinct from
   `elementLineage`: `partOf` is containment within one bone, `fusedFrom` is
   several bones having become one. Conflating them is what made a bird's
   tarsometatarsal insertion read as a more precise version of a crocodylian
   metatarsal one. */
function fusionComponents(id) {
  const out = new Set();
  (function walk(x) {
    for (const c of state.elementsById.get(x)?.fusedFrom || []) {
      if (out.has(c)) continue;
      out.add(c);
      walk(c);
    }
  })(id);
  return out;
}

/* True where `compound` absorbed `part` — directly, or through a component that
   itself contains it. The second case matters: the tarsometatarsus is fused
   from the metatarsals, so an attachment on the fossa metatarsi I is inside
   something the tarsometatarsus absorbed. */
const absorbed = (compound, part) => {
  for (const c of fusionComponents(compound)) {
    if (c === part || isWithin(part, c)) return true;
  }
  return false;
};

/* ---------- fission ---------- */

/* `derivedFrom` is the third element relation and the only one nothing used to
   traverse. It runs ancestor → descendant through evolutionary time: one bone
   became two, as the scapulocoracoid became the scapula and the coracoid.

   It is emphatically NOT containment, and must never be folded into `isWithin`.
   A scapula is not a part of a scapulocoracoid, it IS one — the later half of
   the same thing — and treating the pair as coarse-and-fine would make a
   fish-to-tetrapod comparison report as one author being more precise than
   another. That is the mistake `fusedFrom` was pulled out of `partOf` to avoid,
   and it has its own category here for the same reason.

   Siblings are deliberately excluded. The scapula and the coracoid both descend
   from the scapulocoracoid, but a muscle moving between them within tetrapods
   has genuinely moved, and equating them would erase the therian
   supracoracoideus shift — the best-documented attachment change in the set. */
function fissionLine(id) {
  const cache = state._fissionLine || (state._fissionLine = new Map());
  if (cache.has(id)) return cache.get(id);
  const out = new Set([id]);
  for (let cur = state.elementsById.get(id)?.derivedFrom, guard = 0;
       cur && !out.has(cur) && guard++ < 20;
       cur = state.elementsById.get(cur)?.derivedFrom) out.add(cur);
  (function descend(x) {
    for (const e of state.elements) {
      if (e.derivedFrom !== x || out.has(e.id)) continue;
      out.add(e.id);
      descend(e.id);
    }
  })(id);
  cache.set(id, out);
  return out;
}

/* Ancestor-or-descendant across the fission edge, in either direction. */
const sameFissionLine = (a, b) => a !== b && fissionLine(a).has(b);

/* `skeleton.json.sides` is four independent axes, not one flat vocabulary.
   Terms are only comparable within an axis: "proximal" and "posterior" are not
   alternatives, they answer different questions about the same attachment. */
const SIDE_AXES = [
  ['proximal', 'distal'],
  ['anterior', 'posterior'],
  ['medial', 'lateral'],
  ['dorsal', 'ventral'],
];

/* Returns the taxa whose attachments differ from the reference, with the
   specific elements gained and lost on each side. This is the computed
   character — derived from the data, not hand-authored.

   The diff is hierarchy-aware. "Greater tubercle" against "humerus" is not a
   move, it is the same attachment recorded at finer resolution, and reporting
   it as a gain plus a loss would invent a transition that never happened. Those
   pairs are reported separately as refinements. */
function attachmentShifts(muscle) {
  const ref = referenceTaxonFor(muscle);
  if (!ref) return null;
  const base = attachmentsFor(muscle, ref);

  const shifts = [];
  for (const occ of muscle.occurrences || []) {
    if (occ.taxon === ref || !occ.attachments) continue;   // one row per species
    const here = occ.attachments;

    /* Compared at the finest element each row names, so a move from the bone
       generally to a specific landmark on it reads as a refinement, not a
       gain plus a loss. */
    const finest = r => r.landmark || r.element;

    /* The sides recorded for one element, as a set. An absent `side` means
       unrecorded — never "no side" — so it contributes nothing. */
    const sidesOf = (rows, id) => new Set(
      rows.filter(r => finest(r) === id).map(r => r.side).filter(Boolean));

    const diff = side => {
      const A = base[side] || [], B = here[side] || [];
      const a = A.map(finest), b = B.map(finest);
      const gained = [], lost = [], refined = [], moved = [], fused = [], split = [];

      /* One entry per element, not per row: a bone named on three rows because
         three of its surfaces are scored is still one bone gained or lost. */
      const seenB = new Set();
      for (const r of B) {
        const x = finest(r);
        if (a.includes(x) || seenB.has(x)) continue;
        seenB.add(x);
        /* Fusion before containment. The muscle has not moved and nobody has
           been more precise — the bone it attaches to has absorbed its
           neighbours, which is a fact about the skeleton, not the muscle.
           Checked both ways round, because the reference taxon is whichever
           one happens to be scored first and may be the fused one. */
        const absorbedFrom = a.find(y => absorbed(x, y));
        if (absorbedFrom) {
          fused.push({ from: absorbedFrom, to: x, row: r, separated: false });
          continue;
        }
        const compound = a.find(y => absorbed(y, x));
        if (compound) {
          fused.push({ from: compound, to: x, row: r, separated: true });
          continue;
        }
        /* Fission, on the same footing as fusion and for the same reason: the
           scapulocoracoid became the scapula, so a muscle on one and then the
           other has not gone anywhere. The bone under it divided. Reported, and
           not counted as a substantive shift. */
        const ancestral = a.find(y => sameFissionLine(x, y));
        if (ancestral) {
          split.push({ from: ancestral, to: x, row: r });
          continue;
        }
        const coarser = a.find(y => isWithin(x, y));
        if (coarser) refined.push({ from: coarser, to: x, row: r });
        else gained.push({ id: x, row: r });
      }
      const seenA = new Set();
      for (const r of A) {
        const y = finest(r);
        if (b.includes(y) || seenA.has(y)) continue;
        seenA.add(y);
        if (refined.some(k => k.from === y)) continue;
        if (fused.some(k => k.from === y)) continue;
        if (split.some(k => k.from === y)) continue;
        /* The reference names a finer element and this taxon names something it
           sits inside — usually one source describing the same site more coarsely
           than the other, which is a difference in wording, not in anatomy.
           Unless the taxon does not HAVE the finer element: then the muscle
           genuinely is somewhere else. The salamander deltoideus scapularis
           arises from the suprascapular cartilage, crocodylians have no
           suprascapula, and the move onto the scapula proper is exactly the kind
           of attachment shift forced by a vanished bone that this table exists
           to surface. */
        if (b.some(x => isWithin(y, x)) && elementPresentIn(y, occ.taxon) !== 'no') continue;
        /* The reverse case: the reference names a compound and this taxon names
           one of its components, i.e. the element is unfused here. */
        if (b.some(x => absorbed(y, x))) continue;
        lost.push({ id: y, row: r });
      }

      /* Same element in both taxa, different surface of it. This is a real
         attachment shift and the element-level diff cannot see it, because both
         taxa name the same bone.

         Compared one axis at a time. `side` runs on four independent axes and
         a term from one says nothing about another: a fibular attachment
         recorded as "posterior" in a salamander and "proximal" in a lizard has
         not migrated, it has been described along a different axis by each
         source. Only where both taxa name a side on the SAME axis is there
         anything to compare.

         Within an axis, disjoint sets — ventral against dorsal — are a
         migration across the bone. Overlapping but unequal sets are at least as
         likely to be one source describing the attachment more fully than the
         other, so they are reported without counting as substantive. */
      for (const id of new Set(a.filter(x => b.includes(x)))) {
        const from = sidesOf(A, id), to = sidesOf(B, id);
        if (!from.size || !to.size) continue;
        for (const axis of SIDE_AXES) {
          const f = axis.filter(s => from.has(s)), t = axis.filter(s => to.has(s));
          if (!f.length || !t.length) continue;
          const shared = f.filter(s => t.includes(s));
          if (shared.length === f.length && shared.length === t.length) continue;
          moved.push({ id, from: f, to: t, substantive: shared.length === 0 });
        }
      }

      return { gained, lost, refined, moved, fused, split };
    };

    const o = diff('origin'), i = diff('insertion');
    /* A fusion is a change in the skeleton, not in where the muscle attaches,
       so it is reported but does not make the row a substantive muscle shift. */
    const real = d => d.gained.length || d.lost.length || d.moved.some(mv => mv.substantive);
    const any = d => real(d) || d.refined.length || d.moved.length
      || d.fused.length || d.split.length;
    if (any(o) || any(i)) {
      shifts.push({
        taxon: occ.taxon, species: occ.species, origin: o, insertion: i,
        substantive: real(o) || real(i),
        note: occ.attachmentNote
      });
    }
  }
  return shifts.length ? { reference: ref, shifts } : null;
}

/* ---------- joints ---------- */

/* Joints are edges in a graph whose nodes are bones, so the joints a muscle
   crosses can be DERIVED from its attachments instead of asserted. A muscle
   running from the ilium to the tibia crosses the hip and the knee, and nobody
   has to write that down — which matters because writing it down twice is how
   the two drift apart.

   Serial joints (intervertebral, interphalangeal) name the same element on both
   sides. They form no edge and are excluded here: a long digital flexor reaches
   the interphalangeal joints through the metacarpophalangeal joint, and the
   graph would have no way to represent that. Actions may still point at them. */
function jointGraph() {
  if (state._jointGraph) return state._jointGraph;
  const adj = new Map();
  const link = (a, b, joint) => {
    if (!adj.has(a)) adj.set(a, []);
    adj.get(a).push({ to: b, joint });
  };
  for (const j of state.joints || []) {
    const p = new Set((j.proximal || []).map(r => r.element));
    const d = new Set((j.distal || []).map(r => r.element));
    for (const a of p) for (const b of d) {
      if (a === b) continue;                 // serial joint: no edge
      link(a, b, j.id);
      link(b, a, j.id);
    }
  }
  return (state._jointGraph = adj);
}

/* An attachment names a bone or a landmark on one; walk up `partOf` until
   reaching something the joint graph knows about. The deltopectoral crest
   resolves to the humerus, the ilium to the pelvic girdle. */
function jointNode(elementId) {
  const adj = jointGraph();
  let cur = elementId, guard = 0;
  while (cur && guard++ < 20) {
    if (adj.has(cur)) return cur;
    cur = state.elementsById.get(cur)?.partOf;
  }
  return null;
}

/* Shortest path between two bones; the joints crossed are the edges on it. */
function jointsBetween(fromId, toId) {
  const adj = jointGraph();
  const a = jointNode(fromId), b = jointNode(toId);
  if (!a || !b || a === b) return [];
  const prev = new Map([[a, null]]);
  const queue = [a];
  while (queue.length) {
    const cur = queue.shift();
    if (cur === b) break;
    for (const edge of adj.get(cur) || []) {
      if (prev.has(edge.to)) continue;
      prev.set(edge.to, { from: cur, joint: edge.joint });
      queue.push(edge.to);
    }
  }
  if (!prev.has(b)) return [];
  const out = [];
  for (let cur = b; prev.get(cur); cur = prev.get(cur).from) out.unshift(prev.get(cur).joint);
  return out;
}

/* Every joint this muscle spans, over whichever attachments are on record for
   the taxon — the consensus when a taxon has none of its own. */
function jointsCrossed(muscle, taxonId) {
  const att = attachmentsFor(muscle, taxonId);
  const ends = side => [...new Set((att[side] || [])
    .map(r => r.landmark || r.element).filter(Boolean))];
  const out = new Set();
  for (const o of ends('origin')) {
    for (const i of ends('insertion')) {
      jointsBetween(o, i).forEach(j => out.add(j));
    }
  }
  return [...out];
}

const jointLabel = (id, taxonId) => {
  const j = state.jointsById.get(id);
  if (!j) return id;
  if (!taxonId || !j.taxonNames) return j.label;
  const t = cladeOf(taxonId);
  return j.taxonNames.find(tn => (tn.taxa || []).includes(t))?.name || j.label;
};

/* ---------- element presence ---------- */

/* The taxon picker offers species as well as clades, but the skeleton is scored
   at CLADE level: `presence`, `taxonNames` and the joint names all key on the
   operational taxa in `taxa.json`, because that is the grain the sources score
   a skeleton at. A species id therefore has to be resolved to its clade before
   any of those lookups, and every one of them below goes through `cladeOf`.

   Skipping that step does not fail loudly — it falls through to `presence.default`
   and confidently answers the wrong question. `coracoid` is `default: yes` with
   `absent: [theria]`, so asking about *Galictis cuja* rather than Theria returned
   "yes": a mammal with a coracoid, which is the one girdle character every student
   is taught mammals lack. The inverse cost the cheetah its scapular spine and both
   fossae, which are `default: no` with `present: [theria]` — and with them the
   supraspinatus and infraspinatus. It ran to 2026 wrong answers over 91 of the
   92 species, and always in the direction of the anatomy the reader was NOT
   looking at, since a species is only worth selecting where it differs.

   Attachment resolution is deliberately NOT normalised: `attachmentsFor` matches
   `o.species` first, so picking a species still gets that animal's own rows. Only
   the skeleton's own clade-scored fields are widened. */

/* What this element is called in a given taxon. Elements are homology groups —
   the hyomandibula of a shark and the stapes of a mammal are one element — so the
   label shown has to follow the taxon being viewed. */
function elementLabel(elementId, taxonId) {
  const e = state.elementsById.get(elementId);
  if (!e) return elementId;
  if (!taxonId || !e.taxonNames) return e.label;
  const t = cladeOf(taxonId);
  const hit = e.taxonNames.find(tn => (tn.taxa || []).includes(t));
  return hit ? hit.name : e.label;
}

function elementPresentIn(elementId, taxonId) {
  const e = state.elementsById.get(elementId);
  if (!e) return 'unknown';
  const t = cladeOf(taxonId);
  const p = e.presence || {};
  if ((p.absent || []).includes(t)) return 'no';
  if ((p.present || []).includes(t)) return 'yes';
  if ((p.partial || []).includes(t)) return 'partial';
  if ((p.reduced || []).includes(t)) return 'reduced';
  if ((p.variable || []).includes(t)) return 'variable';
  return p.default || 'unknown';
}

/* Muscles attaching to an element, optionally narrowed to one taxon.
   Each hit carries whether it was RECORDED for that taxon or inherited from the
   consensus, because the two are different claims and the bone-first view used
   to render them identically. Inheriting was the majority case when this was
   written — 69 of Theria's 81 muscles, 18 of Chondrichthyes' 19 — and collapsing
   the distinction turned the consensus into four hundred observations nobody
   made. It is now the minority, 185 of 593 muscle-by-clade cells, and the
   distinction matters for the opposite reason: a fallback that is the exception
   reads as an observation unless it is marked.

   `mode` is `recorded` (drop inherited hits) or `all` (keep and mark them). */
function musclesAtElement(elementId, taxonId, mode) {
  const src = mode || state.skeletonSource || 'all';
  const cacheKey = `${elementId}|${taxonId || ''}|${src}`;
  const cache = state._maeCache || (state._maeCache = new Map());
  if (cache.has(cacheKey)) return cache.get(cacheKey);

  const origin = [], insertion = [];
  for (const m of state.muscles) {
    const taxa = taxonId ? [taxonId] : (m.occurrences || []).map(o => o.taxon);
    let oRec = false, oInh = false, iRec = false, iInh = false;
    for (const t of taxa) {
      /* `presenceFor` rather than the first matching row: it resolves a species
         to its own row and a clade to the rollup over its species, so a clade
         whose first-listed species happens to lack the muscle no longer hides
         it from every bone it attaches to in the others. */
      if (taxonId) {
        const p = presenceFor(m, t);
        if (p === null || p === 'no') continue;
      }
      const a = attachmentsFor(m, t);
      const touches = rows => (rows || []).some(r => rowElements(r).includes(elementId));
      /* Across all taxa combined, one taxon having it on record is enough to
         call the hit recorded — the consensus is only the answer where nothing
         better exists anywhere. */
      if (touches(a.origin)) { if (a.inherited) oInh = true; else oRec = true; }
      if (touches(a.insertion)) { if (a.inherited) iInh = true; else iRec = true; }
    }
    const keep = (rec, inh) => rec ? { muscle: m, inherited: false }
      : (inh && src !== 'recorded') ? { muscle: m, inherited: true } : null;
    const o = keep(oRec, oInh), i = keep(iRec, iInh);
    if (o) origin.push(o);
    if (i) insertion.push(i);
  }
  const out = { origin, insertion };
  cache.set(cacheKey, out);
  return out;
}

/* ---------- skeleton view ---------- */

/* Skeletal elements before soft tissue, then alphabetical. File order is a
   record of when things were added, which is not a useful browse order. */
const KIND_RANK = { group: 0, bone: 1, cartilage: 2, ligament: 3, aponeurosis: 4,
                    membrane: 5, fascia: 6, soft: 7 };

function skeletonRoots() {
  return state.elements.filter(e => !e.partOf).sort((a, b) =>
    (KIND_RANK[a.kind] ?? 9) - (KIND_RANK[b.kind] ?? 9) || a.label.localeCompare(b.label));
}

const childrenOf = id => state.elements.filter(e => e.partOf === id).sort((a, b) =>
  (KIND_RANK[a.kind] ?? 9) - (KIND_RANK[b.kind] ?? 9) || a.label.localeCompare(b.label));

/* Count muscles on this element AND everything nested inside it, so a collapsed
   parent still tells you whether it is worth opening. Counted under the same
   `mode` the body will render, or the badge promises rows that are not there. */
function subtreeCount(elementId, taxonId, mode) {
  const here = musclesAtElement(elementId, taxonId, mode);
  let n = here.origin.length + here.insertion.length;
  for (const c of childrenOf(elementId)) n += subtreeCount(c.id, taxonId, mode);
  return n;
}

/* Elements the taxon lacks that also carry no muscle are noise at full weight:
   under Theria the pectoral girdle opens on anocleithrum, cleithrum, coracoid,
   extracleithrum, furcula and interclavicle — six empty nodes, alphabetically
   ahead of the scapula. That the coracoid is gone is worth saying, so they are
   demoted to one line rather than hidden. A search overrides the demotion, so
   looking for the cleithrum still finds it. */
function partitionAbsent(els, taxonId, q, mode) {
  if (!taxonId || q) return { shown: els, absent: [] };
  const shown = [], absent = [];
  for (const e of els) {
    const gone = elementPresentIn(e.id, taxonId) === 'no'
      && subtreeCount(e.id, taxonId, mode) === 0;
    (gone ? absent : shown).push(e);
  }
  return { shown, absent };
}

function absentLine(absent, taxonId) {
  if (!absent.length) return '';
  /* Named for the clade even when a species is selected, because that is the
     grain the absence was actually scored at — saying "absent in Galictis cuja"
     would credit a single dissection with a statement about all of Theria. */
  const clade = state.taxaById.get(cladeOf(taxonId))?.clade || taxonId;
  return `<p class="cellnote absentlist">Absent in ${esc(clade)}: ${absent.map(e =>
    `<a href="#element=${encodeURIComponent(e.id)}">${esc(e.label)}</a>`).join(', ')}</p>`;
}

function renderSkeleton() {
  const taxonId = state.taxon;
  const mode = state.skeletonSource;
  const q = normalise(state.query);

  const controls = `
    <div class="taxonbar">
      <label for="skel-source">${taxonId
        ? `Attachments in <strong>${esc(selectionLabel(taxonId))}</strong>, showing`
        : 'Attachments across all taxa, showing'}</label>
      <select id="skel-source">
        <option value="recorded" ${mode === 'recorded' ? 'selected' : ''}>only what a source records</option>
        <option value="all" ${mode === 'all' ? 'selected' : ''}>plus the consensus where unrecorded</option>
      </select>
    </div>`;

  const note = mode === 'recorded'
    ? `<p class="viewnote">Showing only attachments a source states for the selected taxon.
         Most taxa are scored for a minority of their muscles, so these lists are short
         by design — switch to <em>plus the consensus</em> for the generalised attachment
         of the rest, marked as unrecorded.</p>`
    : `<p class="viewnote">Entries marked <span class="inh-tag">unrecorded</span> are the
         consensus standing in for an observation nobody has made in this taxon. They are
         not evidence of anything: the shift table on a muscle page ignores them, and so
         should you.</p>`;

  const regions = ['pectoral', 'forelimb', 'pelvic', 'hindlimb', 'axial', 'cranial', 'fin'];
  const byRegion = new Map(regions.map(r => [r, []]));
  skeletonRoots().forEach(e => {
    if (!byRegion.has(e.region)) byRegion.set(e.region, []);
    byRegion.get(e.region).push(e);
  });

  let body = '';
  for (const [region, roots] of byRegion) {
    if (!roots.length) continue;
    const n = roots.reduce((acc, e) => acc + subtreeCount(e.id, taxonId, mode), 0);
    /* A region a taxon has nothing in — the fin under Theria — is a heading over
       an empty box. Drop it rather than make it look like a finding. */
    if (!n && taxonId && !q) continue;
    const { shown, absent } = partitionAbsent(roots, taxonId, q, mode);
    const cards = shown.map(e => renderElementNode(e, taxonId, q, 0)).filter(Boolean).join('');
    if (!cards && !absent.length) continue;
    body += `<details class="elnode region"${q ? ' open' : ''}>
      <summary><span class="elname">${esc(region)}</span><span class="count">${n}</span></summary>
      <div class="elbody">${cards ? `<div class="skeltree">${cards}</div>` : ''}
        ${absentLine(absent, taxonId)}</div></details>`;
  }

  return controls + renderBoneLookup(taxonId, mode) + note + (body ||
    `<div class="empty">No skeletal element matches “${esc(state.query)}”.</div>`);
}

/* ---------- find a muscle by the two bones it spans ---------- */

/* The question a student in a lab actually has. They can see which two bones a
   muscle runs between long before they can tell origin from insertion, so the
   lookup takes the pair unordered and reports which end is which, rather than
   making them guess first and get nothing.

   Search cannot answer this: every indexed term is one label, so no term can
   contain two bone names and `scapula humerus` matches on stray prose instead
   of on the deltoideus scapularis. */

/* Only elements something actually attaches to. The rest can only ever return
   nothing, and there are 41 of them. */
function attachedElementIds() {
  if (state._attachedEls) return state._attachedEls;
  const s = new Set();
  const eat = a => ['origin', 'insertion'].forEach(k =>
    (a?.[k] || []).forEach(r => rowElements(r).forEach(x => s.add(x))));
  for (const m of state.muscles) {
    eat(m.attachments);
    (m.occurrences || []).forEach(o => eat(o.attachments));
  }
  return (state._attachedEls = s);
}

/* An attachment on the deltopectoral crest is an attachment on the humerus, so
   the test runs up and down the `partOf` chain. Both directions: picking the
   bone finds muscles scored on its landmarks, and picking a landmark finds
   muscles scored only on the bone as a whole.

   With `fission` on it also crosses `derivedFrom`, so asking for the scapula
   reaches the fin muscles scored on the scapulocoracoid. That is the whole
   point of the pair lookup at the fin-to-limb boundary: without it a shark's
   girdle and a salamander's are unrelated bones to every query in the app,
   which is the hyomandibula/stapes mistake wearing a different hat. */
const rowTouches = (rows, sel, fission = false) => (rows || []).some(r =>
  rowElements(r).some(x => {
    const hit = h => h === sel || isWithin(h, sel) || isWithin(sel, h);
    if (hit(x)) return true;
    return fission && [...fissionLine(x)].some(hit);
  }));

function musclesBetween(aId, bId, taxonId, mode) {
  const out = [];
  for (const m of state.muscles) {
    const taxa = taxonId ? [taxonId] : (m.occurrences || []).map(o => o.taxon);
    const roles = { a: new Set(), b: new Set() };
    const hitTaxa = [];
    let anyRecorded = false, viaFission = false;
    for (const t of taxa) {
      const p = presenceFor(m, t);
      if (p === null || p === 'no') continue;
      const att = attachmentsFor(m, t);
      if (att.inherited && mode === 'recorded') continue;
      const role = (sel, fission) => {
        const r = [];
        if (rowTouches(att.origin, sel, fission)) r.push('origin');
        if (rowTouches(att.insertion, sel, fission)) r.push('insertion');
        return r;
      };
      const ra = role(aId, true), rb = aId === bId ? role(aId, true) : role(bId, true);
      if (!ra.length || !rb.length) continue;
      /* Whether this taxon needed the fission edge to match. A row that only
         connects because the scapulocoracoid became the scapula is a homology
         statement, not an attachment on the bone the reader picked, and saying
         so is the difference between a cross-reference and a false positive. */
      const strict = role(aId, false).length &&
        (aId === bId || role(bId, false).length);
      if (!strict) viaFission = true;
      ra.forEach(x => roles.a.add(x));
      rb.forEach(x => roles.b.add(x));
      hitTaxa.push(t);
      if (!att.inherited) anyRecorded = true;
    }
    if (hitTaxa.length) {
      out.push({ muscle: m, roles, taxa: hitTaxa,
                 inherited: !anyRecorded, viaFission });
    }
  }
  return out.sort((x, y) =>
    regionRank(x.muscle.region) - regionRank(y.muscle.region) ||
    x.muscle.name.localeCompare(y.muscle.name));
}

function renderBoneLookup(taxonId, mode) {
  /* Only bones the selected taxon HAS. Offering a salamander's shoulder the
     furcula, sternal keel, interclavicle and tarsometatarsus is a menu of
     guaranteed empty results, and it quietly teaches the wrong skeleton. */
  const ids = [...attachedElementIds()]
    .filter(id => !taxonId || elementPresentIn(id, taxonId) !== 'no');
  const REGION_ORDER_EL = ['pectoral', 'forelimb', 'pelvic', 'hindlimb', 'axial', 'cranial', 'fin'];
  const opts = sel => {
    const byRegion = new Map();
    for (const id of ids) {
      const e = state.elementsById.get(id);
      if (!e) continue;
      const r = e.region || 'other';
      if (!byRegion.has(r)) byRegion.set(r, []);
      byRegion.get(r).push(e);
    }
    const groups = [...byRegion.entries()].sort((a, b) =>
      (REGION_ORDER_EL.indexOf(a[0]) + 1 || 99) - (REGION_ORDER_EL.indexOf(b[0]) + 1 || 99));
    return `<option value="">— any —</option>` + groups.map(([r, els]) =>
      `<optgroup label="${esc(r)}">${els
        .sort((a, b) => elementLabel(a.id, taxonId).localeCompare(elementLabel(b.id, taxonId)))
        .map(e => `<option value="${esc(e.id)}" ${e.id === sel ? 'selected' : ''}>${esc(elementLabel(e.id, taxonId))}</option>`)
        .join('')}</optgroup>`).join('');
  };

  /* A selection the current taxon has no option for would run a query against a
     control reading "— any —". Ignore it rather than answer an invisible question. */
  const live = new Set(ids);
  const a = live.has(state.boneA) ? state.boneA : '';
  const b = live.has(state.boneB) ? state.boneB : '';
  let results = '';

  if (a && b) {
    const rows = musclesBetween(a, b, taxonId, mode);
    const head = `<th>${esc(elementLabel(a, taxonId))}</th><th>${esc(elementLabel(b, taxonId))}</th>`;
    const cell = set => set.size
      ? [...set].sort().reverse().join(' + ')
      : '<span class="sep">—</span>';
    results = rows.length
      ? `<div class="tablewrap"><table class="occ bonepair">
          <thead><tr><th>Muscle</th>${head}${taxonId ? '' : '<th>Recorded in</th>'}</tr></thead>
          <tbody>${rows.map(r => {
            const label = muscleLabel(r.muscle, taxonId);
            return `<tr class="${r.inherited ? 'inh' : ''}">
              <td><a data-goto="${r.muscle.id}" href="#${esc(r.muscle.id)}">${esc(clip(label, 64))}</a>
                ${r.inherited ? `<span class="inh-tag" title="Consensus attachment — no source records this taxon">unrecorded</span>` : ''}
                ${r.viaFission ? `<span class="inh-tag fis-tag" title="Matched across a derivedFrom edge — the bone this attaches to is the ancestor or descendant of the one you picked, not the same element">via homologue</span>` : ''}
                ${label !== r.muscle.name ? `<span class="groupname">group: ${esc(r.muscle.name)}</span>` : ''}</td>
              <td class="a-kind">${cell(r.roles.a)}</td>
              <td class="a-kind">${cell(r.roles.b)}</td>
              ${taxonId ? '' : `<td class="bp-taxa">${r.taxa
                .map(t => esc(state.taxaById.get(t)?.clade || t)).join(', ')}</td>`}
            </tr>`;
          }).join('')}</tbody></table></div>`
      : `<p class="cellnote">Nothing on record attaches to both${taxonId
          ? ` in ${esc(state.taxaById.get(taxonId)?.clade || taxonId)}`
          : ''}${mode === 'recorded' ? ' — try the consensus fallback in the bar above' : ''}.</p>`;
  }

  return `<div class="bonelookup">
    <div class="taxonbar">
      <label for="bone-a">Find a muscle attaching to</label>
      <select id="bone-a">${opts(a)}</select>
      <label for="bone-b">and to</label>
      <select id="bone-b">${opts(b)}</select>
    </div>
    ${results}
  </div>`;
}

function renderElementNode(e, taxonId, q, depth) {
  const mode = state.skeletonSource;
  const kids = childrenOf(e.id);
  const here = musclesAtElement(e.id, taxonId, mode);
  const total = subtreeCount(e.id, taxonId, mode);

  const matches = !q || normalise(e.label).includes(q) ||
    (e.synonyms || []).some(s => normalise(s).includes(q));
  const { shown: kidsShown, absent: kidsAbsent } = partitionAbsent(kids, taxonId, q, mode);
  const kidHtml = kidsShown.map(k => renderElementNode(k, taxonId, q, depth + 1)).filter(Boolean).join('');
  if (q && !matches && !kidHtml) return '';

  const presence = taxonId ? elementPresentIn(e.id, taxonId) : (e.presence || {}).default;
  const absentHere = taxonId && (presence === 'no');

  /* The taxon's own name for the muscle, not the homology group's label. With
     Theria selected this is the difference between reading "Subscapularis" and
     "Subcoracoscapularis"; the group name stays in the tooltip. */
  const list = arr => arr.length
    ? arr.map(({ muscle: m, inherited }) => {
        const label = muscleLabel(m, taxonId);
        const title = label === m.name ? m.name : `${label} — ${m.name}`;
        return `<a data-goto="${m.id}" href="#${esc(m.id)}" class="${inherited ? 'inh' : ''}"
          title="${esc(title)}${inherited ? ' (consensus — not recorded for this taxon)' : ''}"
          >${esc(clip(label, 52))}</a>${inherited ? '<span class="inh-tag">unrecorded</span>' : ''}`;
      }).join('<span class="sep">, </span>')
    : '<span class="sep">—</span>';

  const badges = [
    e.correlate ? `<span class="chip corr" title="Leaves a recognisable osteological trace">osteological correlate</span>` : '',
    absentHere ? `<span class="chip conf-contested">absent in this taxon</span>` : '',
    presence === 'partial' ? `<span class="chip conf-moderate">incipient</span>` : '',
    presence === 'reduced' ? `<span class="chip conf-moderate">reduced</span>` : '',
    e.fusedFrom ? `<span class="chip fuse" title="Formed by fusion — its components stay findable">fused element</span>` : ''
  ].join('');

  /* Both directions of the fusion edge. The forward one is curated on the
     compound; the reverse is derived by scanning, the same way the app derives
     a tetrapod muscle's fin ancestry rather than storing it twice. */
  const elLink = id =>
    `<a href="#element=${encodeURIComponent(id)}">${esc(elementLabel(id, taxonId))}</a>`;
  const fusedInto = state.elements.filter(x => (x.fusedFrom || []).includes(e.id));
  const fusionLines = [
    e.fusedFrom ? `Fused from ${e.fusedFrom.map(elLink).join(', ')}.` : '',
    fusedInto.length ? `Incorporated into ${fusedInto.map(x => elLink(x.id)).join(', ')}
      in ${esc(fusedInto.flatMap(x => (x.presence || {}).present || [])
        .map(t => state.taxaById.get(t)?.clade || t).join(', ') || 'some taxa')}.` : ''
  ].filter(Boolean).join(' ');

  /* The fission edge, both ways — curated on the descendant, reversed by
     scanning. Without this the drill-down never says that the bone you are
     looking at used to be part of another one, which is the question the whole
     fin-to-limb section of the dataset is about. */
  const splitInto = state.elements.filter(x => x.derivedFrom === e.id);
  const fissionLines = [
    e.derivedFrom ? `Split from ${elLink(e.derivedFrom)} when the ancestral girdle divided.` : '',
    splitInto.length ? `Divided into ${splitInto.map(x => elLink(x.id)).join(' and ')}
      in tetrapods.` : ''
  ].filter(Boolean).join(' ');

  const note = (e.presence || {}).note;
  const alias = taxonId && elementLabel(e.id, taxonId) !== e.label ? e.label : null;
  const open = q ? ' open' : '';

  return `<details class="elnode d${depth}"${open}>
    <summary>
      <span class="elname">${esc(elementLabel(e.id, taxonId))}</span>
      <span class="elkind">${esc(e.kind)}</span>
      ${badges}
      <span class="count">${total}</span>
    </summary>
    <div class="elbody">
      ${absentHere ? `<p class="cellnote">Absent in ${esc(state.taxaById.get(taxonId).clade)}.</p>` : ''}
      ${alias ? `<p class="cellnote">Elsewhere: ${esc(alias)}</p>` : ''}
      ${note ? `<p class="cellnote">${emph(note)}</p>` : ''}
      ${fusionLines ? `<p class="cellnote fusion">${fusionLines}</p>` : ''}
      ${fissionLines ? `<p class="cellnote fission">${fissionLines}</p>` : ''}
      ${e.transformation ? `<p class="cellnote">${esc(e.transformation)}</p>` : ''}
      ${(here.origin.length || here.insertion.length) ? `
        <div class="grp"><b>Origin of (${here.origin.length})</b>${list(here.origin)}</div>
        <div class="grp"><b>Insertion of (${here.insertion.length})</b>${list(here.insertion)}</div>` : ''}
      ${kidHtml ? `<div class="elkids">${kidHtml}</div>` : ''}
      ${absentLine(kidsAbsent, taxonId)}
    </div>
  </details>`;
}

/* ---------- hierarchy view (mass / layer / segment) ---------- */

const MASS_LABEL = {
  dorsal: 'Dorsal mass — adductor in fins, extensor in limbs',
  ventral: 'Ventral mass — abductor in fins, flexor in limbs',
  'somitic-axial': 'Somitic, axial-derived',
  branchiomeric: 'Branchiomeric (pharyngeal arch)',
  somitic: 'Somitic',
  extraocular: 'Extraocular (prechordal)'
};

function renderHierarchy() {
  const q = normalise(state.query);
  const taxonId = state.taxon;
  const groups = new Map();

  for (const m of state.muscles) {
    if (q && !state.index.find(e => e.muscle === m)?.terms.some(t => t.norm.includes(q))) continue;
    /* Same taxon rule as the muscle list: no row means unaddressed, `no` means
       a source ruled it out. Neither belongs in this taxon's homology spine. */
    if (taxonId) {
      const p = presenceFor(m, taxonId);
      if (p === null || p === 'no') continue;
    }
    const key = m.region === 'cranial' ? `arch:${m.arch ?? '—'}` : `mass:${m.mass || '—'}`;
    if (!groups.has(key)) groups.set(key, new Map());
    const layerKey = m.layer || 'layer not assigned';
    const g = groups.get(key);
    if (!g.has(layerKey)) g.set(layerKey, new Map());
    const segKey = m.segment || '—';
    if (!g.get(layerKey).has(segKey)) g.get(layerKey).set(segKey, []);
    g.get(layerKey).get(segKey).push(m);
  }

  if (!groups.size) {
    return `<div class="empty">Nothing matches “${esc(state.query)}”${taxonId
      ? ` in ${esc(state.taxaById.get(taxonId).clade)}` : ''}.</div>`;
  }

  const SEG_ORDER = ['fin', 'girdle', 'stylopod', 'zeugopod', 'autopod', 'cranial', 'axial', '—'];

  let out = '';

  const massKeys = [...groups.keys()].sort();
  for (const key of massKeys) {
    const [kind, val] = key.split(':');
    const label = kind === 'arch' ? `Pharyngeal arch ${val}` : (MASS_LABEL[val] || val);
    const layers = groups.get(key);
    const n = [...layers.values()].reduce((a, s) => a + [...s.values()].reduce((b, l) => b + l.length, 0), 0);

    out += `<details class="elnode d0"${q ? ' open' : ''}>
      <summary><span class="elname">${esc(label)}</span><span class="count">${n}</span></summary>
      <div class="elbody">`;

    for (const [layer, segs] of [...layers.entries()].sort()) {
      const ln = [...segs.values()].reduce((a, l) => a + l.length, 0);
      out += `<details class="elnode d1"${q ? ' open' : ''}>
        <summary><span class="elname">${esc(layer)}</span><span class="count">${ln}</span></summary>
        <div class="elbody">`;
      const segEntries = [...segs.entries()].sort(
        (a, b) => SEG_ORDER.indexOf(a[0]) - SEG_ORDER.indexOf(b[0]));
      for (const [seg, list] of segEntries) {
        out += `<div class="grp"><b>${esc(seg)} (${list.length})</b>
          ${list.map(m => {
            const label = muscleLabel(m, taxonId);
            return `<a data-goto="${m.id}" title="${esc(label === m.name ? m.name : `${label} — ${m.name}`)}"
              >${esc(clip(label, 52))}</a>`;
          }).join('<span class="sep">, </span>')}</div>`;
      }
      out += `</div></details>`;
    }
    out += `</div></details>`;
  }
  return out;
}


/* ---------- muscle architecture ---------- */

/* PCSA is the force proxy, fascicle length the excursion/velocity proxy. Showing
   them side by side is the point: a short-fascicled, high-PCSA muscle and a
   long-fascicled, low-PCSA one do different jobs at the same joint. */
function renderArchitecture(m) {
  const rows = (m.occurrences || [])
    .filter(o => o.architecture)
    .sort((a, b) => (state.taxonOrder.get(a.taxon) ?? 99) - (state.taxonOrder.get(b.taxon) ?? 99));
  if (!rows.length) return '';

  let out = `<section class="block"><h3>Architecture</h3>`;
  for (const occ of rows) {
    const a = occ.architecture;
    const t = state.taxaById.get(occ.taxon) || { clade: occ.taxon };
    const num = v => v && typeof v.mean === 'number'
      ? `${v.mean}<span class="sd"> ± ${v.sd ?? '—'}</span>` : '<span class="sep">—</span>';
    out += `<p class="synonyms" style="margin:.2rem 0 .5rem">
        <strong>${esc(t.clade)}</strong> — ${esc(a.species || '')}${a.n ? `, n = ${a.n}` : ''}${a.bodyMass_kg ? `, ${a.bodyMass_kg} kg` : ''}
        ${(a.sources || []).map(k => sourceLink(k)).join(' ')}</p>
      <div class="tablewrap"><table class="occ archtable">
        <thead><tr><th>Part</th><th>Mass (g)</th><th>Fascicle (mm)</th><th>Pennation (°)</th><th>PCSA (cm²)</th><th>F<sub>max</sub> (N)</th></tr></thead><tbody>
        ${(a.parts || []).map(pt => `<tr>
          <td>${esc(pt.name)}${pt.abbr ? ` <span class="sep">(${esc(pt.abbr)})</span>` : ''}</td>
          <td class="numcell">${num(pt.mass_g)}</td>
          <td class="numcell">${num(pt.fascicleLength_mm)}</td>
          <td class="numcell">${num(pt.pennation_deg)}</td>
          <td class="numcell">${num(pt.pcsa_cm2)}</td>
          <td class="numcell">${num(pt.maxIsometricForce_N)}</td></tr>`).join('')}
      </tbody></table></div>`;
    if (a.note) out += `<p class="viewnote">${emph(a.note)}</p>`;
    if (a.comparison) {
      out += `<p class="viewnote">vs ${esc(a.comparison.species)}${a.comparison.n ? `, n = ${a.comparison.n}` : ''}</p>`;
    }
  }
  return out + `</section>`;
}

/* ---------- attachment block for the muscle detail page ---------- */

function renderAttachmentBlock(m) {
  const cons = m.attachments || {};
  if (!(cons.origin || []).length && !(cons.insertion || []).length) return '';

  const rowsTable = rows => rows.length
    ? `<table class="attach"><tbody>${rows.map(r => `<tr>
         <td class="a-bone"><a href="#element=${encodeURIComponent(r.element)}">${esc(state.elementsById.get(r.element)?.label || r.element)}</a></td>
         <td class="a-side">${r.side ? esc(r.side) : '<span class="sep">—</span>'}</td>
         <td class="a-lm">${r.landmark
             ? `<a href="#element=${encodeURIComponent(r.landmark)}">${esc(state.elementsById.get(r.landmark)?.label || r.landmark)}</a>`
             + (state.elementsById.get(r.landmark)?.correlate ? ' <span class="chip corr">correlate</span>' : '')
             : '<span class="sep">—</span>'}</td>
       </tr>`).join('')}</tbody></table>`
    : '<span class="sep">—</span>';

  let out = `<section class="block"><h3>Attachments</h3>
    <div class="attachgrid">
      <div><h4 class="attach-h">Origin</h4>${rowsTable(cons.origin || [])}</div>
      <div><h4 class="attach-h">Insertion</h4>${rowsTable(cons.insertion || [])}</div>
    </div>`;

  /* Per-taxon rows. This is where the element/side/landmark structure pays off:
     one taxon can attach to several sides or landmarks of the same bone, and
     each gets its own row rather than being flattened into a list. */
  const documented = (m.occurrences || [])
    .filter(o => o.attachments && (o.present || 'yes') !== 'no')
    .sort((a, b) => (state.taxonOrder.get(a.taxon) ?? 99) - (state.taxonOrder.get(b.taxon) ?? 99));

  if (documented.length) {
    out += `<h4 class="attach-h" style="margin-top:1.25rem">By taxon</h4>
      <div class="tablewrap"><table class="occ attachmatrix">
      <thead><tr><th>Taxon</th><th>Type</th><th>Bone</th><th>Side</th><th>Landmark</th></tr></thead><tbody>`;
    for (const occ of documented) {
      const t = state.taxaById.get(occ.taxon) || { clade: occ.taxon, color: '#999' };
      const kinds = [['origin', occ.attachments.origin || []], ['insertion', occ.attachments.insertion || []]];
      const span = kinds.reduce((n, [, rows]) => n + Math.max(rows.length, 0), 0) || 1;
      let first = true;
      for (const [kind, rows] of kinds) {
        rows.forEach((r, i) => {
          const lm = r.landmark ? state.elementsById.get(r.landmark) : null;
          out += `<tr>
            ${first ? `<td rowspan="${span}"><div class="taxoncell">
                 <span class="swatch" style="background:${esc(t.color)}"></span>
                 <span class="clade">${esc(t.clade)}</span></div></td>` : ''}
            ${i === 0 ? `<td rowspan="${rows.length}" class="a-kind">${kind}</td>` : ''}
            <td class="a-bone"><a href="#element=${encodeURIComponent(r.element)}">${esc(elementLabel(r.element, occ.taxon))}</a></td>
            <td class="a-side">${r.side ? esc(r.side) : '<span class="sep">—</span>'}</td>
            <td class="a-lm">${lm
              ? `<a href="#element=${encodeURIComponent(r.landmark)}">${esc(elementLabel(r.landmark, occ.taxon))}</a>`
                + (lm.correlate ? ' <span class="chip corr">correlate</span>' : '')
              : '<span class="sep">—</span>'}</td>
          </tr>`;
          first = false;
        });
      }
    }
    out += `</tbody></table></div>`;
  }

  const analysis = attachmentShifts(m);
  if (analysis) {
    const refName = state.taxaById.get(analysis.reference)?.clade || analysis.reference;
    out += `<h4 class="attach-h" style="margin-top:1.25rem">Shifts from ${esc(refName)}</h4>
      <div class="tablewrap"><table class="occ">
      <colgroup><col class="c-taxon"><col class="c-body"></colgroup>
      <thead><tr><th>Taxon</th><th>Change from ${esc(refName)}</th></tr></thead><tbody>`;

    const label = x => esc(state.elementsById.get(x)?.label || x);

    for (const s of analysis.shifts) {
      const t = state.taxaById.get(s.taxon) || { clade: s.taxon, color: '#999' };
      const sp = state.speciesById?.get(s.species);
      const line = (side, d) => {
        const bits = [];
        if (d.gained.length) bits.push(`<span class="gain">+ ${d.gained.map(g => label(g.id)).join(', ')}</span>`);
        if (d.lost.length) bits.push(`<span class="loss">− ${d.lost.map(l => label(l.id)).join(', ')}</span>`);
        if (d.refined.length) bits.push(`<span class="refine">${d.refined
          .map(r => `${label(r.from)} → ${label(r.to)}`).join('; ')}</span>`);
        d.moved.forEach(mv => bits.push(
          `<span class="${mv.substantive ? 'move' : 'refine'}">${label(mv.id)}: ` +
          `${esc(mv.from.join('/'))} → ${esc(mv.to.join('/'))}</span>`));
        if (d.fused.length) bits.push(`<span class="fusedin">${d.fused
          .map(f => f.separated
            ? `${label(f.to)} unfused from ${label(f.from)}`
            : `${label(f.from)} fused into ${label(f.to)}`).join('; ')}</span>`);
        if (d.split.length) bits.push(`<span class="fusedin">${d.split
          .map(f => `${label(f.from)} divided into ${label(f.to)}`).join('; ')}</span>`);
        return bits.length ? `<div><b>${side}</b> ${bits.join(' ')}</div>` : '';
      };
      out += `<tr${s.substantive ? '' : ' class="absent"'}>
        <td><div class="taxoncell"><span class="swatch" style="background:${esc(t.color)}"></span>
          <span class="clade">${esc(t.clade)}</span></div>
          ${sp ? `<span class="common"><i>${esc(sp.binomial)}</i></span>` : ''}
          ${s.substantive ? '' : '<span class="common">resolution only</span>'}</td>
        <td><div class="microdl">${line('origin', s.origin)}${line('insertion', s.insertion)}</div>
          ${s.note ? `<div class="cellnote">${emph(s.note)}</div>` : ''}</td>
      </tr>`;
    }
    out += `</tbody></table></div>`;
  }
  return out + `</section>`;
}
