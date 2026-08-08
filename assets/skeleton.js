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
  const occ = (muscle.occurrences || []).find(o => o.taxon === taxonId);
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

/* The plesiomorphic reference for a shift comparison. Caudata is the standard
   proxy for the ancestral tetrapod condition in every source here; for muscles
   with no salamander row we fall back to the earliest taxon on the topology. */
function referenceTaxonFor(muscle) {
  const documented = (muscle.occurrences || [])
    .filter(o => o.attachments)
    .sort((a, b) => (state.taxonOrder.get(a.taxon) ?? 99) - (state.taxonOrder.get(b.taxon) ?? 99));
  return documented.length ? documented[0].taxon : null;
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
    if (occ.taxon === ref || !occ.attachments) continue;
    const here = occ.attachments;

    /* Compared at the finest element each row names, so a move from the bone
       generally to a specific landmark on it reads as a refinement, not a
       gain plus a loss. */
    const finest = r => r.landmark || r.element;

    const diff = side => {
      const A = base[side] || [], B = here[side] || [];
      const a = A.map(finest), b = B.map(finest);
      const gained = [], lost = [], refined = [];

      for (const r of B) {
        const x = finest(r);
        if (a.includes(x)) continue;
        const coarser = a.find(y => isWithin(x, y));
        if (coarser) refined.push({ from: coarser, to: x, row: r });
        else gained.push({ id: x, row: r });
      }
      for (const r of A) {
        const y = finest(r);
        if (b.includes(y)) continue;
        if (refined.some(k => k.from === y)) continue;
        if (b.some(x => isWithin(y, x))) continue;
        lost.push({ id: y, row: r });
      }
      return { gained, lost, refined };
    };

    const o = diff('origin'), i = diff('insertion');
    const real = d => d.gained.length || d.lost.length;
    if (real(o) || real(i) || o.refined.length || i.refined.length) {
      shifts.push({
        taxon: occ.taxon, origin: o, insertion: i,
        substantive: real(o) || real(i),
        note: occ.attachmentNote
      });
    }
  }
  return shifts.length ? { reference: ref, shifts } : null;
}

/* ---------- element presence ---------- */

function elementPresentIn(elementId, taxonId) {
  const e = state.elementsById.get(elementId);
  if (!e) return 'unknown';
  const p = e.presence || {};
  if ((p.absent || []).includes(taxonId)) return 'no';
  if ((p.present || []).includes(taxonId)) return 'yes';
  if ((p.partial || []).includes(taxonId)) return 'partial';
  if ((p.reduced || []).includes(taxonId)) return 'reduced';
  if ((p.variable || []).includes(taxonId)) return 'variable';
  return p.default || 'unknown';
}

/* muscles attaching to an element, optionally narrowed to one taxon */
function musclesAtElement(elementId, taxonId) {
  const origin = [], insertion = [];
  for (const m of state.muscles) {
    const taxa = taxonId ? [taxonId] : (m.occurrences || []).map(o => o.taxon);
    let hitO = false, hitI = false;
    for (const t of taxa) {
      if (taxonId) {
        const occ = (m.occurrences || []).find(o => o.taxon === t);
        if (!occ || (occ.present || 'yes') === 'no') continue;
      }
      const a = attachmentsFor(m, t);
      const touches = rows => (rows || []).some(r => rowElements(r).includes(elementId));
      if (touches(a.origin)) hitO = true;
      if (touches(a.insertion)) hitI = true;
    }
    if (hitO) origin.push(m);
    if (hitI) insertion.push(m);
  }
  return { origin, insertion };
}

/* ---------- skeleton view ---------- */

function skeletonRoots() {
  return state.elements.filter(e => !e.partOf);
}

const childrenOf = id => state.elements.filter(e => e.partOf === id);

/* Count muscles on this element AND everything nested inside it, so a collapsed
   parent still tells you whether it is worth opening. */
function subtreeCount(elementId, taxonId) {
  const here = musclesAtElement(elementId, taxonId);
  let n = here.origin.length + here.insertion.length;
  for (const c of childrenOf(elementId)) n += subtreeCount(c.id, taxonId);
  return n;
}

function renderSkeleton() {
  const taxonId = state.skeletonTaxon;
  const q = normalise(state.query);

  const taxonPicker = `
    <div class="taxonbar">
      <label for="skel-taxon">Show attachments as recorded in</label>
      <select id="skel-taxon">
        <option value="">all taxa combined</option>
        ${[...state.taxa]
          .sort((a, b) => (state.taxonOrder.get(a.id) ?? 99) - (state.taxonOrder.get(b.id) ?? 99))
          .map(t => `<option value="${t.id}" ${t.id === taxonId ? 'selected' : ''}>${esc(t.clade)} — ${esc(t.label)}</option>`).join('')}
      </select>
    </div>`;

  const regions = ['pectoral', 'forelimb', 'pelvic', 'hindlimb', 'axial', 'cranial', 'fin'];
  const byRegion = new Map(regions.map(r => [r, []]));
  skeletonRoots().forEach(e => {
    if (!byRegion.has(e.region)) byRegion.set(e.region, []);
    byRegion.get(e.region).push(e);
  });

  let body = '';
  for (const [region, roots] of byRegion) {
    if (!roots.length) continue;
    const cards = roots.map(e => renderElementNode(e, taxonId, q, 0)).filter(Boolean).join('');
    if (!cards) continue;
    body += `<section class="block"><h3>${esc(region)}</h3><div class="skeltree">${cards}</div></section>`;
  }

  const hint = taxonId
    ? `Showing the attachments recorded for <strong>${esc(state.taxaById.get(taxonId).clade)}</strong>.
       Elements that taxon lacks are marked; a muscle listed on a parent element is one whose
       attachment is recorded only at that coarser level.`
    : `Showing every attachment in the dataset, pooled across taxa. Pick a taxon to see one animal's arrangement.`;

  return taxonPicker +
    `<div class="resultbar">${hint}</div>` + (body || `<div class="empty">No skeletal element matches “${esc(state.query)}”.</div>`);
}

function renderElementNode(e, taxonId, q, depth) {
  const kids = childrenOf(e.id);
  const here = musclesAtElement(e.id, taxonId);
  const total = subtreeCount(e.id, taxonId);

  const matches = !q || normalise(e.label).includes(q) ||
    (e.synonyms || []).some(s => normalise(s).includes(q));
  const kidHtml = kids.map(k => renderElementNode(k, taxonId, q, depth + 1)).filter(Boolean).join('');
  if (q && !matches && !kidHtml) return '';

  const presence = taxonId ? elementPresentIn(e.id, taxonId) : (e.presence || {}).default;
  const absentHere = taxonId && (presence === 'no');

  const list = arr => arr.length
    ? arr.map(m => `<a data-goto="${m.id}">${esc(m.name)}</a>`).join('<span class="sep">, </span>')
    : '<span class="sep">—</span>';

  const badges = [
    e.correlate ? `<span class="chip corr" title="Leaves a recognisable osteological trace">osteological correlate</span>` : '',
    absentHere ? `<span class="chip conf-contested">absent in this taxon</span>` : '',
    presence === 'partial' ? `<span class="chip conf-moderate">incipient</span>` : '',
    presence === 'reduced' ? `<span class="chip conf-moderate">reduced</span>` : ''
  ].join('');

  const note = (e.presence || {}).note;
  const open = depth < 1 || q ? ' open' : '';

  return `<details class="elnode d${depth}"${open}>
    <summary>
      <span class="elname">${esc(e.label)}</span>
      <span class="elkind">${esc(e.kind)}</span>
      ${badges}
      <span class="count">${total}</span>
    </summary>
    <div class="elbody">
      ${absentHere ? `<p class="cellnote">This element does not exist in ${esc(state.taxaById.get(taxonId).clade)}. Any muscle that attached here in other taxa has had to attach somewhere else.</p>` : ''}
      ${note ? `<p class="cellnote">${esc(note)}</p>` : ''}
      ${(here.origin.length || here.insertion.length) ? `
        <div class="grp"><b>Origin of (${here.origin.length})</b>${list(here.origin)}</div>
        <div class="grp"><b>Insertion of (${here.insertion.length})</b>${list(here.insertion)}</div>` : ''}
      ${kidHtml ? `<div class="elkids">${kidHtml}</div>` : ''}
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
  const groups = new Map();

  for (const m of state.muscles) {
    if (q && !state.index.find(e => e.muscle === m)?.terms.some(t => t.norm.includes(q))) continue;
    const key = m.region === 'cranial' ? `arch:${m.arch ?? '—'}` : `mass:${m.mass || '—'}`;
    if (!groups.has(key)) groups.set(key, new Map());
    const layerKey = m.layer || 'layer not assigned';
    const g = groups.get(key);
    if (!g.has(layerKey)) g.set(layerKey, new Map());
    const segKey = m.segment || '—';
    if (!g.get(layerKey).has(segKey)) g.get(layerKey).set(segKey, []);
    g.get(layerKey).get(segKey).push(m);
  }

  if (!groups.size) return `<div class="empty">Nothing matches “${esc(state.query)}”.</div>`;

  const SEG_ORDER = ['fin', 'girdle', 'stylopod', 'zeugopod', 'autopod', 'cranial', 'axial', '—'];

  let out = `<div class="resultbar">Grouped by developmental origin, then layer, then proximodistal segment.
    This is the axis that survives deep transitions — the dorsal/ventral split is confirmed independently
    by innervation, and every tetrapod limb muscle is a subdivision of an ancestral fin mass.</div>`;

  const massKeys = [...groups.keys()].sort();
  for (const key of massKeys) {
    const [kind, val] = key.split(':');
    const label = kind === 'arch' ? `Pharyngeal arch ${val}` : (MASS_LABEL[val] || val);
    const layers = groups.get(key);
    const n = [...layers.values()].reduce((a, s) => a + [...s.values()].reduce((b, l) => b + l.length, 0), 0);

    out += `<details class="elnode d0" ${q ? 'open' : ''}>
      <summary><span class="elname">${esc(label)}</span><span class="count">${n}</span></summary>
      <div class="elbody">`;

    for (const [layer, segs] of [...layers.entries()].sort()) {
      const ln = [...segs.values()].reduce((a, l) => a + l.length, 0);
      out += `<details class="elnode d1" open>
        <summary><span class="elname">${esc(layer)}</span><span class="count">${ln}</span></summary>
        <div class="elbody">`;
      const segEntries = [...segs.entries()].sort(
        (a, b) => SEG_ORDER.indexOf(a[0]) - SEG_ORDER.indexOf(b[0]));
      for (const [seg, list] of segEntries) {
        out += `<div class="grp"><b>${esc(seg)} (${list.length})</b>
          ${list.map(m => `<a data-goto="${m.id}">${esc(m.name)}</a>`).join('<span class="sep">, </span>')}</div>`;
      }
      out += `</div></details>`;
    }
    out += `</div></details>`;
  }
  return out;
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
            <td class="a-bone"><a href="#element=${encodeURIComponent(r.element)}">${esc(state.elementsById.get(r.element)?.label || r.element)}</a></td>
            <td class="a-side">${r.side ? esc(r.side) : '<span class="sep">—</span>'}</td>
            <td class="a-lm">${lm
              ? `<a href="#element=${encodeURIComponent(r.landmark)}">${esc(lm.label)}</a>`
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
    out += `<div class="callout"><h4>Attachment shifts</h4>
      <p>Computed by comparing each taxon's recorded attachments against
      <strong>${esc(refName)}</strong>, the earliest taxon here with attachments on record.</p></div>
      <div class="tablewrap"><table class="occ">
      <colgroup><col class="c-taxon"><col class="c-body"></colgroup>
      <thead><tr><th>Taxon</th><th>Change from ${esc(refName)}</th></tr></thead><tbody>`;

    const label = x => esc(state.elementsById.get(x)?.label || x);

    for (const s of analysis.shifts) {
      const t = state.taxaById.get(s.taxon) || { clade: s.taxon, color: '#999' };
      const line = (side, d) => {
        const bits = [];
        if (d.gained.length) bits.push(`<span class="gain">+ ${d.gained.map(g => label(g.id)).join(', ')}</span>`);
        if (d.lost.length) bits.push(`<span class="loss">− ${d.lost.map(l => label(l.id)).join(', ')}</span>`);
        if (d.refined.length) bits.push(`<span class="refine">${d.refined
          .map(r => `${label(r.from)} → ${label(r.to)}`).join('; ')}</span>`);
        return bits.length ? `<div><b>${side}</b> ${bits.join(' ')}</div>` : '';
      };
      out += `<tr${s.substantive ? '' : ' class="absent"'}>
        <td><div class="taxoncell"><span class="swatch" style="background:${esc(t.color)}"></span>
          <span class="clade">${esc(t.clade)}</span></div>
          ${s.substantive ? '' : '<span class="common">resolution only</span>'}</td>
        <td><div class="microdl">${line('origin', s.origin)}${line('insertion', s.insertion)}</div>
          ${s.note ? `<div class="cellnote">${esc(s.note)}</div>` : ''}</td>
      </tr>`;
    }
    out += `</tbody></table></div>`;
  }
  return out + `</section>`;
}
