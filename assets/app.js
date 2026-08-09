/* Vertebrate muscle homology & topology browser.
   No build step, no dependencies. Data lives in ../data/*.json. */

/* Proximal-to-distal within each appendage, head first. Alphabetical order would
   scatter the forelimb series across the list. */
const REGION_ORDER = ['cranial', 'fin', 'pectoral', 'arm', 'forearm', 'hand', 'pelvic', 'thigh', 'leg', 'foot'];
const regionRank = r => { const i = REGION_ORDER.indexOf(r); return i === -1 ? 99 : i; };

const DATA_FILES = [
  'data/muscles-fin.json',
  'data/muscles-pectoral.json',
  'data/muscles-forearm-hand.json',
  'data/muscles-hindlimb.json',
  'data/muscles-cranial.json'
];

const state = {
  muscles: [],
  byId: new Map(),
  taxa: [],
  taxaById: new Map(),
  taxonOrder: new Map(),
  sources: new Map(),
  elements: [],
  elementsById: new Map(),
  skeletonTaxon: '',
  topology: null,
  phyloScope: 'all',
  index: [],
  query: '',
  filters: { region: null, taxon: null, confidence: null },
  view: 'browse',        // browse | detail | skeleton | hierarchy | phylogeny
  current: null
};

/* ---------- boot ---------- */

async function boot() {
  const [taxaDoc, sourcesDoc, skeletonDoc, ...muscleDocs] = await Promise.all([
    fetchJSON('data/taxa.json'),
    fetchJSON('data/sources.json'),
    fetchJSON('data/skeleton.json'),
    ...DATA_FILES.map(fetchJSON)
  ]);

  state.topology = taxaDoc.topology;
  state.elements = skeletonDoc.elements;
  skeletonDoc.elements.forEach(e => state.elementsById.set(e.id, e));

  state.taxa = taxaDoc.taxa;
  taxaDoc.taxa.forEach(t => state.taxaById.set(t.id, t));
  flattenTopology(taxaDoc.topology, state.taxonOrder);
  sourcesDoc.sources.forEach(s => state.sources.set(s.key, s));

  muscleDocs.forEach(doc => {
    doc.muscles.forEach(m => {
      m._regionLabel = doc.region;
      state.muscles.push(m);
      state.byId.set(m.id, m);
    });
  });

  buildIndex();
  wireUI();
  applyHash();
  render();
}

const fetchJSON = url => fetch(url).then(r => {
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.json();
});

/* Depth-first walk of the taxon topology yields the phylogenetic sort order. */
function flattenTopology(node, out) {
  if (node.taxon) out.set(node.taxon, out.size);
  (node.children || []).forEach(c => flattenTopology(c, out));
}

/* ---------- search index ---------- */

/* Each muscle contributes several searchable strings: its own name, every
   synonym, and every taxon-specific name from its occurrence rows. The label
   that matched is reported back so the result card can show WHY it matched —
   which is the whole point when the literature uses six names per muscle. */
function buildIndex() {
  state.index = state.muscles.map(m => {
    const terms = [];
    const push = (text, kind, extra) => {
      if (!text) return;
      terms.push({ text, norm: normalise(text), kind, extra });
    };

    push(m.name, 'name');
    (m.synonyms || []).forEach(s => push(s, 'synonym'));
    (m.occurrences || []).forEach(o => {
      if (o.name && normalise(o.name) !== normalise(m.name)) {
        push(o.name, 'taxon-name', state.taxaById.get(o.taxon)?.clade || o.taxon);
      }
      (o.synonyms || []).forEach(s => push(s, 'synonym'));
    });

    /* Index every skeletal element the muscle touches, in every taxon — both the
       bone and any landmark — so a search for "humerus" finds muscles recorded
       only on the deltopectoral crest, and searching a landmark works too. */
    const els = new Set();
    const collect = att => ['origin', 'insertion'].forEach(side =>
      (att?.[side] || []).forEach(r => {
        if (!r) return;
        if (typeof r === 'string') { els.add(r); return; }
        if (r.element) els.add(r.element);
        if (r.landmark) els.add(r.landmark);
      }));
    collect(m.attachments);
    (m.occurrences || []).forEach(o => collect(o.attachments));
    els.forEach(id => push(state.elementsById.get(id)?.label || id, 'attachment'));

    return { muscle: m, terms };
  });
}

const normalise = s => s.toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();

function search(qRaw) {
  const q = normalise(qRaw);
  if (!q) return state.index.map(e => ({ muscle: e.muscle, score: 0, hit: null }));
  const words = q.split(' ').filter(Boolean);

  const out = [];
  for (const entry of state.index) {
    let best = null, bestScore = Infinity;
    for (const t of entry.terms) {
      const s = scoreTerm(t.norm, q, words);
      if (s !== null && s < bestScore) { bestScore = s; best = t; }
    }
    if (best) out.push({ muscle: entry.muscle, score: bestScore, hit: best });
  }
  out.sort((a, b) => a.score - b.score || a.muscle.name.localeCompare(b.muscle.name));
  return out;
}

/* Lower score = better. Exact < prefix < word-prefix < substring < all-words-present. */
function scoreTerm(norm, q, words) {
  const kindPenalty = 0;
  if (norm === q) return 0 + kindPenalty;
  if (norm.startsWith(q)) return 1 + kindPenalty;
  if (norm.split(' ').some(w => w.startsWith(q))) return 2 + kindPenalty;
  if (norm.includes(q)) return 3 + kindPenalty;
  if (words.length > 1 && words.every(w => norm.includes(w))) return 4 + kindPenalty;
  return null;
}

/* ---------- filtering ---------- */

function filtered() {
  let rows = search(state.query);
  const f = state.filters;
  if (f.region) rows = rows.filter(r => r.muscle.region === f.region);
  if (f.confidence) rows = rows.filter(r => (r.muscle.homology || {}).confidence === f.confidence);
  if (f.taxon) rows = rows.filter(r => presenceFor(r.muscle, f.taxon) !== null);
  // Rank by relevance when searching; alphabetically within region when browsing.
  if (!state.query) {
    rows.sort((a, b) =>
      regionRank(a.muscle.region) - regionRank(b.muscle.region) ||
      a.muscle.name.localeCompare(b.muscle.name));
  }
  return rows;
}

function presenceFor(m, taxonId) {
  const o = (m.occurrences || []).find(x => x.taxon === taxonId);
  if (!o) return null;
  return o.present || 'yes';
}

/* ---------- rendering ---------- */

/* Re-rendering usually makes the document shorter (a search narrows the list, a
   view switch replaces it). Without this the browser keeps the old scroll offset
   and the user lands on blank space below the new content. */
function resetScroll() {
  if (window.scrollY > 0) window.scrollTo({ top: 0, behavior: 'auto' });
}

function render({ keepScroll = false } = {}) {
  renderSidebar();
  const main = document.getElementById('main');

  if (state.view === 'phylogeny') { main.innerHTML = renderPhylogeny(); }
  else if (state.view === 'skeleton') { main.innerHTML = renderSkeleton(); }
  else if (state.view === 'hierarchy') { main.innerHTML = renderHierarchy(); }
  else if (state.view === 'detail' && state.current) { main.innerHTML = renderDetail(state.current); }
  else { main.innerHTML = renderList(); }

  const scope = main.querySelector('#phylo-scope');
  if (scope) scope.addEventListener('change', () => {
    state.phyloScope = scope.value; render({ keepScroll: true });
  });

  const picker = main.querySelector('#skel-taxon');
  if (picker) picker.addEventListener('change', () => {
    state.skeletonTaxon = picker.value; render({ keepScroll: true });
  });

  main.querySelectorAll('[data-goto]').forEach(el => {
    el.addEventListener('click', ev => { ev.preventDefault(); openMuscle(el.dataset.goto); });
  });
  main.querySelectorAll('[data-back]').forEach(el => {
    el.addEventListener('click', () => { state.view = 'browse'; state.current = null; setHash(''); render(); });
  });

  if (!keepScroll) resetScroll();

  const total = state.muscles.length;
  const occ = state.muscles.reduce((n, m) => n + (m.occurrences || []).length, 0);
  document.getElementById('footcount').textContent =
    ` · ${total} muscles · ${occ} occurrences · ${state.sources.size} sources · ${state.taxa.length} taxa`;
}

function renderList() {
  const rows = filtered();
  if (!rows.length) {
    return `<div class="empty">No muscle matches “${esc(state.query)}”.<br>
            Try a synonym (<em>dorsalis scapulae</em>), a bone (<em>coracoid</em>), or clear the filters.</div>`;
  }

  const bar = `<div class="resultbar"><strong>${rows.length}</strong> ${rows.length === 1 ? 'muscle' : 'muscles'}
    ${state.query ? `matching “${esc(state.query)}”` : ''}
    ${activeFilterLabel()}</div>`;

  const cards = rows.map(({ muscle: m, hit }) => {
    const conf = (m.homology || {}).confidence;
    const nTaxa = (m.occurrences || []).filter(o => (o.present || 'yes') !== 'no').length;
    let hitLine = '';
    if (hit && hit.kind !== 'name') {
      const label = hit.kind === 'taxon-name' ? `${esc(hit.extra)} name`
                  : hit.kind === 'attachment' ? 'attaches to'
                  : 'also known as';
      hitLine = `<div class="hit">${label}: <em>${esc(hit.text)}</em></div>`;
    }
    return `<article class="mcard" data-goto="${m.id}" tabindex="0">
      <h4>${esc(m.name)}</h4>
      <div class="sub">${esc(m._regionLabel)} · ${esc(m.subregion || '')} · present in ${nTaxa} taxa${conf ? ` · ${esc(conf)}` : ''}</div>
      ${hitLine}
    </article>`;
  }).join('');

  return bar + `<div class="cardgrid">${cards}</div>`;
}

function activeFilterLabel() {
  const f = state.filters, parts = [];
  if (f.region) parts.push(`in <strong>${esc(f.region)}</strong>`);
  if (f.taxon) parts.push(`recorded for <strong>${esc(state.taxaById.get(f.taxon).clade)}</strong>`);
  if (f.confidence) parts.push(`homology <strong>${esc(f.confidence)}</strong>`);
  return parts.join(' · ');
}

function renderDetail(m) {
  const h = m.homology || {};
  const c = m.consensus || {};

  const chips = [
    m._regionLabel && `<span class="chip">${esc(m._regionLabel)}</span>`,
    m.subregion && `<span class="chip">${esc(m.subregion)}</span>`,
    m.mass && `<span class="chip">${esc(m.mass)} mass</span>`,
    m.layer && `<span class="chip">${esc(m.layer)}</span>`,
    m.arch != null && `<span class="chip">arch ${esc(String(m.arch))}</span>`,
    h.confidence && `<span class="chip conf-${esc(h.confidence)}">homology: ${esc(h.confidence)}</span>`
  ].filter(Boolean).join('');

  const oia = `<dl class="oia">
    ${defRow('Origin', c.origin)}
    ${defRow('Insertion', c.insertion)}
    ${defRow('Action', c.action)}
    ${defRow('Innervation', c.innervation)}
    ${defRow('Development', m.developmental)}
  </dl>`;

  const syn = (m.synonyms || []).length
    ? `<section class="block"><h3>Also called</h3>
       <p class="synonyms">${m.synonyms.map(s => `<code>${esc(s)}</code>`).join(' ')}</p></section>` : '';

  return `
  <div class="crumb"><button data-back>← All muscles</button><span>/</span><span>${esc(m.name)}</span></div>
  <div class="detail">
    <div class="detail-head">
      <h2>${esc(m.name)}</h2>
      <div class="chips">${chips}</div>
    </div>
    <div class="detail-body">
      <section class="block"><h3>Consensus description</h3>${oia}</section>
      ${syn}
      <section class="block"><h3>Occurrence by taxon</h3>${renderOccTable(m)}</section>
      ${renderAttachmentBlock(m)}
      ${renderArchitecture(m)}
      ${renderHomologyBlock(m, h)}
      ${renderAncestry(m)}
      ${renderRelated(m, h)}
      ${renderSources(m)}
    </div>
  </div>`;
}

const defRow = (label, val) => val
  ? `<dt>${label}</dt><dd>${esc(val)}</dd>` : '';

/* Inline citation for a table cell. Links to the DOI where we have one so the
   claim is one click from its source. */
function sourceLink(key) {
  const s = state.sources.get(key);
  if (!s) return `<span class="chip">${esc(key)}</span>`;
  const label = esc(s.short);
  return s.doi
    ? `<a class="chip" href="https://doi.org/${esc(s.doi)}" target="_blank" rel="noopener"
         title="${esc(s.title)}">${label}</a>`
    : `<span class="chip" title="${esc(s.title)}">${label}</span>`;
}

function renderOccTable(m) {
  const occ = [...(m.occurrences || [])].sort(
    (a, b) => (state.taxonOrder.get(a.taxon) ?? 99) - (state.taxonOrder.get(b.taxon) ?? 99));
  if (!occ.length) return `<p class="cellnote">No taxon-level records yet.</p>`;

  const rows = occ.map(o => {
    const t = state.taxaById.get(o.taxon) || { clade: o.taxon, label: '', color: '#999' };
    const present = o.present || 'yes';
    const absent = present === 'no';

    const micro = ['origin', 'insertion', 'action', 'innervation']
      .filter(k => o[k])
      .map(k => `<div><b>${k}</b> ${esc(o[k])}</div>`).join('');

    const cites = (o.sources || []).map(k => sourceLink(k)).join(' ');

    return `<tr class="${absent ? 'absent' : ''}">
      <td><div class="taxoncell"><span class="swatch" style="background:${esc(t.color)}"></span>
        <span class="clade">${esc(t.clade)}</span></div>
        <span class="common">${esc(t.label || '')}</span></td>
      <td><span class="pres pres-${esc(present)}">${esc(present)}</span></td>
      <td>${o.name ? `<span class="localname">${esc(o.name)}</span>` : '<span class="pres-no">—</span>'}
        ${micro ? `<div class="microdl">${micro}</div>` : ''}
        ${o.note ? `<div class="cellnote">${esc(o.note)}</div>` : ''}
        ${cites ? `<div class="cites">${cites}</div>` : ''}</td>
    </tr>`;
  }).join('');

  return `<div class="tablewrap"><table class="occ">
    <colgroup><col class="c-taxon"><col class="c-pres"><col class="c-body"></colgroup>
    <thead><tr><th>Taxon</th><th>Present</th><th>Local name, attachments, notes and source</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`;
}

function renderHomologyBlock(m, h) {
  if (!h.notes && !h.openQuestion && !h.teaching && !h.serial) return '';
  let out = `<section class="block"><h3>Homology</h3>`;
  if (h.notes) out += `<div class="callout"><h4>Assessment</h4><p>${esc(h.notes)}</p></div>`;
  if (h.openQuestion) out += `<div class="callout open"><h4>Open question</h4><p>${esc(h.openQuestion)}</p></div>`;

  if (h.serial) {
    const s = h.serial;
    const target = s.forelimb ? state.byId.get(s.forelimb) : null;
    let body = target
      ? `Topological counterpart in the forelimb: <a class="pill" data-goto="${target.id}">${esc(target.name)}</a>`
      : `No counterpart in the other limb.`;
    if (s.basis) body += ` <span class="chip">basis: ${esc(s.basis)}</span>`;
    out += `<div class="callout ${s.caution ? 'caution' : ''}"><h4>Serial correspondence</h4><p>${body}</p>`;
    if (s.note) out += `<p>${esc(s.note)}</p>`;
    if (s.caution) out += `<p><strong>Caution.</strong> ${esc(s.caution)}</p>`;
    out += `</div>`;
  }
  if (h.caveat) out += `<div class="callout caution"><h4>Source caveat</h4><p>${esc(h.caveat)}</p></div>`;
  if (h.teaching) out += `<div class="callout teach"><h4>Teaching use</h4><p>${esc(h.teaching)}</p></div>`;
  return out + `</section>`;
}

/* Ancestry runs both ways from one curated edge: a fin muscle lists what it gave
   rise to, and every tetrapod muscle finds its ancestor by scanning for itself. */
function renderAncestry(m) {
  const d = m.derivatives || {};
  const hasForward = (d.pectoral || []).length || (d.pelvic || []).length;

  const ancestors = state.muscles.filter(f =>
    ['pectoral', 'pelvic'].some(k => ((f.derivatives || {})[k] || []).includes(m.id)));

  if (!hasForward && !ancestors.length) return '';

  const link = id => {
    const t = state.byId.get(id);
    return t ? `<a class="pill" data-goto="${t.id}">${esc(t.name)}</a>` : '';
  };

  let out = `<section class="block"><h3>Fin-to-limb ancestry</h3>`;

  if (m.ancestralNode) {
    out += `<div class="callout"><h4>First appears</h4><p>${esc(m.ancestralNode)}</p></div>`;
  }

  if (hasForward) {
    out += `<p class="synonyms" style="margin-bottom:.4rem">Subdivided in tetrapods into:</p>`;
    for (const [appendage, ids] of Object.entries(d)) {
      if (!ids.length) continue;
      out += `<p class="synonyms" style="margin:.5rem 0 .3rem"><strong>${esc(appendage)}</strong></p>
        <div class="pills" style="margin-bottom:.5rem">${ids.map(link).join('')}</div>`;
    }
  }

  if (ancestors.length) {
    out += `<p class="synonyms" style="margin-bottom:.4rem">Derived from the ancestral fin muscle:</p>
      <div class="pills">${ancestors.map(a => link(a.id)).join('')}</div>`;
  }

  return out + `</section>`;
}

function renderRelated(m, h) {
  const rel = (h.related || []).map(id => state.byId.get(id)).filter(Boolean);
  if (!rel.length) return '';

  let out = `<section class="block"><h3>Connections</h3>`;
  if (rel.length) {
    out += `<p class="synonyms" style="margin-bottom:.4rem">Topologically or developmentally adjacent:</p>
      <div class="pills" style="margin-bottom:1rem">
      ${rel.map(r => `<a class="pill" data-goto="${r.id}">${esc(r.name)}</a>`).join('')}</div>`;
  }
  return out + `</section>`;
}

function renderSources(m) {
  const keys = new Set(m.sources || []);
  (m.occurrences || []).forEach(o => (o.sources || []).forEach(k => keys.add(k)));
  if (!keys.size) return '';
  const items = [...keys].map(k => state.sources.get(k)).filter(Boolean)
    .sort((a, b) => a.year - b.year)
    .map(s => `<li><strong>${esc(s.authors)}</strong> (${s.year}). ${esc(s.title)}. <em>${esc(s.journal)}</em>.
      ${s.doi ? `<a href="https://doi.org/${esc(s.doi)}" target="_blank" rel="noopener">doi:${esc(s.doi)}</a>` : ''}
      ${s.peerReviewed === false ? ' <span class="chip conf-uncertain">not peer reviewed</span>' : ''}
      <span class="meta">${esc(s.role || '')}${s.notes ? ` · notes: ${esc(s.notes)}` : ''}</span></li>`).join('');
  return `<section class="block"><h3>Sources</h3><ol class="refs">${items}</ol></section>`;
}

/* ---------- sidebar ---------- */

function renderSidebar() {
  const rows = search(state.query);
  const el = document.getElementById('sidebar');

  const count = (key, val) => rows.filter(r =>
    key === 'region' ? r.muscle.region === val
    : key === 'confidence' ? (r.muscle.homology || {}).confidence === val
    : presenceFor(r.muscle, val) !== null).length;

  const regions = [...new Set(state.muscles.map(m => m.region))]
    .sort((a, b) => regionRank(a) - regionRank(b));
  const confs = ['well-supported', 'moderate', 'contested', 'uncertain'];
  const taxaSorted = [...state.taxa].sort(
    (a, b) => (state.taxonOrder.get(a.id) ?? 99) - (state.taxonOrder.get(b.id) ?? 99));

  const facet = (title, key, items) => `
    <div class="facet"><h3>${title}</h3><ul>
      ${items.map(it => {
        const n = count(key, it.value);
        const on = state.filters[key] === it.value;
        return `<li><button data-facet="${key}" data-value="${esc(it.value)}"
          aria-pressed="${on}" ${n === 0 && !on ? 'style="opacity:.4"' : ''}>
          ${it.color ? `<span class="swatch" style="background:${esc(it.color)}"></span>` : ''}
          <span>${esc(it.label)}</span><span class="count">${n}</span></button></li>`;
      }).join('')}
    </ul></div>`;

  el.innerHTML =
    facet('Region', 'region', regions.map(r => ({ value: r, label: r }))) +
    facet('Recorded in taxon', 'taxon', taxaSorted.map(t => ({ value: t.id, label: t.clade, color: t.color }))) +
    facet('Homology confidence', 'confidence', confs.map(c => ({ value: c, label: c })));

  const active = Object.values(state.filters).filter(Boolean).length;
  const fb = document.getElementById('btn-filters');
  if (fb) fb.textContent = active ? `Filters · ${active}` : 'Filters';

  el.querySelectorAll('[data-facet]').forEach(btn => {
    btn.addEventListener('click', () => {
      const k = btn.dataset.facet, v = btn.dataset.value;
      state.filters[k] = state.filters[k] === v ? null : v;
      if (state.view === 'detail') state.view = 'browse';
      render();
    });
  });
}

/* ---------- navigation ---------- */

function openMuscle(id) {
  const m = state.byId.get(id);
  if (!m) return;
  state.current = m; state.view = 'detail';
  setHash(id);
  render();
}

const setHash = id => { history.replaceState(null, '', id ? `#${id}` : location.pathname); };

function applyHash() {
  const h = decodeURIComponent(location.hash.slice(1));
  if (!h) return;
  if (h.startsWith('element=')) {
    const el = state.elementsById.get(h.slice(8));
    state.view = 'skeleton';
    state.query = el ? el.label : h.slice(8);
    document.getElementById('search').value = state.query;
    syncViewButtons();
    return;
  }
  if (state.byId.has(h)) { state.current = state.byId.get(h); state.view = 'detail'; }
}

function syncViewButtons() {
  const on = v => String(state.view === v);
  document.getElementById('btn-browse').setAttribute('aria-pressed',
    String(state.view === 'browse' || state.view === 'detail'));
  document.getElementById('btn-skeleton').setAttribute('aria-pressed', on('skeleton'));
  document.getElementById('btn-hierarchy').setAttribute('aria-pressed', on('hierarchy'));
  document.getElementById('btn-phylogeny').setAttribute('aria-pressed', on('phylogeny'));
}

function wireUI() {
  const input = document.getElementById('search');
  let t;
  input.addEventListener('input', () => {
    clearTimeout(t);
    t = setTimeout(() => {
      state.query = input.value;
      if (state.view === 'detail') state.view = 'browse';
      render();
    }, 90);
  });

  const nav = { 'btn-browse': 'browse', 'btn-skeleton': 'skeleton',
                'btn-hierarchy': 'hierarchy', 'btn-phylogeny': 'phylogeny' };
  for (const [id, view] of Object.entries(nav)) {
    document.getElementById(id).addEventListener('click', () => {
      state.view = view; state.current = null;
      if (view === 'browse') setHash('');
      syncViewButtons(); render();
    });
  }

  const shell = document.getElementById('shell');
  const filtersBtn = document.getElementById('btn-filters');
  const setFilters = on => {
    shell.classList.toggle('filters-open', on);
    filtersBtn.setAttribute('aria-pressed', String(on));
    try { localStorage.setItem('filtersOpen', on ? '1' : '0'); } catch {}
  };
  setFilters((() => { try { return localStorage.getItem('filtersOpen') === '1'; } catch { return false; } })());
  filtersBtn.addEventListener('click', () =>
    setFilters(!shell.classList.contains('filters-open')));

  const themeBtn = document.getElementById('btn-theme');
  themeBtn.addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme');
    const next = cur === 'dark' ? 'light' : cur === 'light' ? '' : 'dark';
    if (next) document.documentElement.setAttribute('data-theme', next);
    else document.documentElement.removeAttribute('data-theme');
  });

  window.addEventListener('hashchange', () => { applyHash(); render(); });

  document.addEventListener('keydown', ev => {
    if (ev.key === '/' && document.activeElement !== input) { ev.preventDefault(); input.focus(); }
    if (ev.key === 'Escape') { input.blur(); }
  });

  document.addEventListener('keydown', ev => {
    if (ev.key !== 'Enter') return;
    const card = ev.target.closest?.('.mcard');
    if (card) openMuscle(card.dataset.goto);
  });

  syncViewButtons();
}

/* ---------- utils ---------- */

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

boot().catch(err => {
  document.getElementById('main').innerHTML =
    `<div class="empty">Could not load the data files.<br><code>${esc(err.message)}</code><br><br>
     If you opened <code>index.html</code> directly from disk, browsers block <code>fetch</code> on
     <code>file://</code> URLs. Run a local server instead:<br>
     <code>python3 -m http.server 8000</code></div>`;
  console.error(err);
});
