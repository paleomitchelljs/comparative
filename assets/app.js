/* Vertebrate muscle homology & topology browser.
   No build step, no dependencies. Data lives in ../data/*.json. */

/* Proximal-to-distal within each appendage, head first. Alphabetical order would
   scatter the forelimb series across the list. */
const REGION_ORDER = ['cranial', 'axial', 'fin', 'pectoral', 'arm', 'forearm', 'hand', 'pelvic', 'thigh', 'leg', 'foot'];
const regionRank = r => { const i = REGION_ORDER.indexOf(r); return i === -1 ? 99 : i; };

/* Species are the unit of observation and clades are rolled up from them, so a
   muscle may carry several rows for one clade — Gallus, an ostrich, a tinamou, a
   penguin — and Aves is what they agree on. Nothing in the data stores a clade
   on an occurrence; `_taxon` is derived at boot from species.json and is the one
   piece of denormalisation in the app, kept because two dozen call sites read it
   and because it can never drift: it is recomputed on every load. */
const DATA_FILES = [
  'data/muscles-axial.json',
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
  species: [],
  speciesById: new Map(),
  speciesByClade: new Map(),
  taxonOrder: new Map(),
  sources: new Map(),
  elements: [],
  elementsById: new Map(),
  nerves: [],
  nervesById: new Map(),
  joints: [],
  jointsById: new Map(),
  /* ONE taxon, shared by every view. It used to be two — a `taxon` facet in the
     sidebar and a separate select in the Skeleton view — which meant picking
     Caudata in the muscle list and clicking Skeleton landed on "all taxa
     combined". The animal on the bench does not change when you change tab. */
  taxon: '',
  /* `recorded` shows only attachments a source states for the selected taxon;
     `all` falls back to the consensus where nobody has recorded one. Recorded
     is the default because the fallback is an assumption, not an observation.
     It once covered most of the dataset; it is now 185 of 593 muscle-by-clade
     cells, which changes the size of the problem and not the principle. */
  skeletonSource: 'recorded',
  boneA: '',
  boneB: '',
  topology: null,
  phyloScope: 'all',
  index: [],
  query: '',
  // Keys must match FACET_MATCH — filtered() iterates these. Taxon is NOT one
  // of them: it is global (state.taxon) and scopes every view, not just this list.
  filters: { region: null, spans: null, segment: null, mass: null, layer: null,
             confidence: null },
  view: 'browse',        // browse | detail | skeleton | hierarchy | phylogeny
  current: null
};

/* ---------- boot ---------- */

async function boot() {
  const [taxaDoc, speciesDoc, sourcesDoc, skeletonDoc, nervesDoc, jointsDoc, ...muscleDocs] = await Promise.all([
    fetchJSON('data/taxa.json'),
    fetchJSON('data/species.json'),
    fetchJSON('data/sources.json'),
    fetchJSON('data/skeleton.json'),
    fetchJSON('data/nerves.json'),
    fetchJSON('data/joints.json'),
    ...DATA_FILES.map(fetchJSON)
  ]);

  state.topology = taxaDoc.topology;
  state.elements = skeletonDoc.elements;
  skeletonDoc.elements.forEach(e => state.elementsById.set(e.id, e));

  state.nerves = nervesDoc.nerves;
  nervesDoc.nerves.forEach(n => state.nervesById.set(n.id, n));

  state.joints = jointsDoc.joints;
  jointsDoc.joints.forEach(j => state.jointsById.set(j.id, j));

  state.taxa = taxaDoc.taxa;
  taxaDoc.taxa.forEach(t => state.taxaById.set(t.id, t));

  state.species = speciesDoc.species;
  speciesDoc.species.forEach(sp => {
    state.speciesById.set(sp.id, sp);
    if (!state.speciesByClade.has(sp.clade)) state.speciesByClade.set(sp.clade, []);
    state.speciesByClade.get(sp.clade).push(sp);
  });
  flattenTopology(taxaDoc.topology, state.taxonOrder);
  sourcesDoc.sources.forEach(s => state.sources.set(s.key, s));

  muscleDocs.forEach(doc => {
    doc.muscles.forEach(m => {
      m._regionLabel = doc.region;
      /* Derived, never stored. `taxon` is kept as the property name so the
         views can go on asking "which clade is this row in" unchanged. */
      (m.occurrences || []).forEach(o => {
        o.taxon = state.speciesById.get(o.species)?.clade || null;
      });
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

    /* The descriptive fields. The page has always claimed these are searchable
       — "origin, insertion, action, innervation" is in the meta description —
       and two of the four returned nothing at all: "femoral nerve" matched no
       record, "abduct" matched nine of the eighteen that describe it.

       These are prose, not labels, so they are scored with a penalty (see
       scoreTerm). A muscle whose NAME starts with "flexor" must outrank one
       whose action happens to contain "flexes". */
    const c = m.consensus || {};
    push(c.action, 'action');
    push(c.innervation, 'innervation');
    push(c.origin, 'origin');
    push(c.insertion, 'insertion');
    push(m.developmental, 'development');

    /* Classification terms, so "somitic", "profundus" or "zeugopod" find their
       records from the search box as well as from the facets. */
    push(m.subregion, 'group');
    push(m.mass, 'group');
    push(m.layer, 'group');
    push(m.segment, 'group');

    /* Taxon-specific descriptions, which is where the disagreements live. */
    (m.occurrences || []).forEach(o => {
      const clade = state.taxaById.get(o.taxon)?.clade || o.taxon;
      ['action', 'innervation', 'origin', 'insertion'].forEach(k => push(o[k], k, clade));
      (o.parts || []).forEach(p => push(p.name, 'part', clade));
    });

    /* Nerves, each with its whole ancestor chain, so "radial nerve" finds the
       supinator (which is on the deep branch) and "brachial plexus" finds
       everything below it. Synonyms and per-taxon names come too, which is how
       "supracoracoid nerve" reaches the mammalian supraspinatus — a name that
       appears in no prose string on that record. Prose search alone could do
       none of this: it can only match the words a description happens to use. */
    const nerveIds = new Set();
    const addNerve = id => {
      let cur = id, guard = 0;
      while (cur && !nerveIds.has(cur) && guard++ < 20) {
        nerveIds.add(cur);
        cur = state.nervesById.get(cur)?.partOf;
      }
    };
    (m.nerves || []).forEach(r => addNerve(r.nerve));
    (m.occurrences || []).forEach(o => (o.nerves || []).forEach(r => addNerve(r.nerve)));
    nerveIds.forEach(id => {
      const n = state.nervesById.get(id);
      if (!n) return;
      push(n.label, 'nerve');
      (n.synonyms || []).forEach(s => push(s, 'nerve'));
      (n.taxonNames || []).forEach(tn => push(tn.name, 'nerve'));
    });

    /* Joints, both those acted on and those the attachments say it spans, plus
       the motion terms. "flexion" and "knee" both reach the femorotibialis,
       and the per-taxon joint names come too — searching "mesotarsal" finds
       the avian ankle muscles, whose own descriptions never use the word. */
    const jointIds = new Set((m.actions || []).map(a => a.joint));
    if (typeof jointsCrossed === 'function') {
      jointsCrossed(m, null).forEach(j => jointIds.add(j));
    }
    jointIds.forEach(id => {
      const j = state.jointsById.get(id);
      if (!j) return;
      push(j.label, 'joint');
      (j.taxonNames || []).forEach(tn => push(tn.name, 'joint'));
    });
    (m.actions || []).forEach(a => push(a.motion, 'motion'));

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
      const s = scoreTerm(t.norm, q, words, t.kind);
      if (s !== null && s < bestScore) { bestScore = s; best = t; }
    }
    if (best) out.push({ muscle: entry.muscle, score: bestScore, hit: best });
  }
  out.sort((a, b) => a.score - b.score || a.muscle.name.localeCompare(b.muscle.name));
  return out;
}

/* What kind of text matched, as a penalty band. A name is what the reader
   typed at; a description merely contains their word. Without this, indexing
   the prose fields would let "flexor carpi ulnaris" be outranked by any record
   whose action string happens to say "flexes", because both are word-prefix
   matches and the raw score cannot tell them apart.

   Bands are wider than the 0-4 match scale so they never interleave: every
   name match beats every description match, whatever the match quality. */
const KIND_PENALTY = {
  name: 0, synonym: 0, 'taxon-name': 0,
  attachment: 10, part: 10, group: 10, nerve: 10, joint: 10, motion: 10,
  origin: 20, insertion: 20, action: 20, innervation: 20, development: 20,
};

/* How much of the matched term the query did NOT account for. A fraction, always
   under 1, so it orders equally-classed matches without ever crossing a band.

   Specificity, in other words: "tenuissimus" matching a bare `Tenuissimus` is a
   better answer than the same word buried in a 125-character string, and the
   raw match classes cannot tell them apart — both are word-prefix hits. Ranking
   them equal is how an occurrence name that listed a dozen muscles came back as
   the top hit for any one of them. */
const specificity = (norm, q) => Math.min(0.9, Math.max(0, norm.length - q.length) / 200);

/* Lower score = better. Exact < prefix < word-prefix < substring < all-words-present. */
function scoreTerm(norm, q, words, kind) {
  const base = (KIND_PENALTY[kind] ?? 20) + specificity(norm, q);
  if (norm === q) return 0 + base;
  if (norm.startsWith(q)) return 1 + base;
  if (norm.split(' ').some(w => w.startsWith(q))) return 2 + base;
  if (norm.includes(q)) return 3 + base;
  if (words.length > 1 && words.every(w => norm.includes(w))) return 4 + base;
  return null;
}

/* ---------- filtering ---------- */

/* One predicate per facet, shared by the filter and the sidebar counts so the
   two cannot drift apart about what a facet means.

   The classification facets test for equality against a field that may be
   absent. That is deliberate: `layer` is recorded for 56% of records, and a
   muscle with no layer belongs under no layer button. Unrecorded is not a
   value, and putting those records everywhere or nowhere-but-visible would
   both misreport it. */
const FACET_MATCH = {
  region: (m, v) => m.region === v,
  /* Not a classification facet but a derived one, and the only filter here that
     asks about the muscle's geometry rather than its filing. */
  spans: (m, v) => v === 'crosses' ? !!(m.spans && m.spans.crosses)
                 : v === 'within' ? !!(m.spans && !m.spans.crosses)
                 : !m.spans,
  segment: (m, v) => m.segment === v,
  mass: (m, v) => m.mass === v,
  layer: (m, v) => m.layer === v,
  confidence: (m, v) => (m.homology || {}).confidence === v,
};

/* Narrow a result set to one taxon, splitting off the muscles a source examined
   that taxon for and did NOT find.

   Three outcomes, and they are three different claims:
     no occurrence row  — nobody addressed this taxon. Not a candidate, dropped.
     present: "no"      — a source looked and found nothing. That is a finding,
                          not a candidate: it belongs at the foot of the list,
                          not among the muscles you might be holding.
     anything else      — a candidate.

   The middle case is why this exists. The taxon facet used to keep those rows
   in the grid, so filtering to Caudata offered Teres major, 'Rhomboideus' and
   Scapulohumeralis anterior as things to identify in a salamander, with nothing
   on the card to say the source had ruled them out. The Skeleton view already
   handles absent BONES this way (partitionAbsent / absentLine); this is the
   same treatment for muscles. */
function scopeToTaxon(rows, taxonId) {
  if (!taxonId) return { rows, absent: [] };
  const kept = [], absent = [];
  for (const r of rows) {
    const p = presenceFor(r.muscle, taxonId);
    if (p === null) continue;
    (p === 'no' ? absent : kept).push(p === 'no' ? r.muscle : r);
  }
  return { rows: kept, absent };
}

function filtered() {
  let rows = search(state.query);
  for (const [key, val] of Object.entries(state.filters)) {
    if (val) rows = rows.filter(r => FACET_MATCH[key](r.muscle, val));
  }
  const scoped = scopeToTaxon(rows, state.taxon);
  // Rank by relevance when searching; alphabetically within region when browsing.
  if (!state.query) {
    scoped.rows.sort((a, b) =>
      regionRank(a.muscle.region) - regionRank(b.muscle.region) ||
      a.muscle.name.localeCompare(b.muscle.name));
  }
  return scoped;
}

/* Every row a clade has. There may be several — one per species — and that is
   the point: Aves is Gallus AND the ostrich AND the tinamou AND the penguin. */
const occurrencesIn = (m, id) => (m.occurrences || []).filter(o => o.taxon === id);

/* A clade's presence, computed from its species rather than authored.

   This is the change species-level scoring buys. `variable` used to be a
   judgement someone typed in after reading that a source found a muscle in one
   lizard and not another; now it is what the rows say when they disagree, and
   it cannot be forgotten or applied inconsistently. A clade nobody has scored
   returns null — unrecorded, as everywhere else. */
function presenceFor(m, id) {
  if (state.speciesById.has(id)) {                     // a species, not a clade
    const o = (m.occurrences || []).find(x => x.species === id);
    return o ? (o.present || 'yes') : null;
  }
  const rows = occurrencesIn(m, id);
  if (!rows.length) return null;
  const states = new Set(rows.map(o => o.present || 'yes'));
  if (states.size === 1) return [...states][0];
  // Observed presence set against observed absence IS the variable case.
  if (states.has('yes') && states.has('no')) return 'variable';
  // Otherwise the disagreement is between hedges; report the weakest claim.
  for (const s of ['variable', 'uncertain', 'inferred', 'yes', 'no']) {
    if (states.has(s)) return s;
  }
  return null;
}

/* Which species disagree, for the interface to show rather than hide. */
function presenceSplit(m, id) {
  const rows = occurrencesIn(m, id);
  const by = new Map();
  for (const o of rows) {
    const p = o.present || 'yes';
    if (!by.has(p)) by.set(p, []);
    by.get(p).push(state.speciesById.get(o.species));
  }
  return by;
}

/* The clade the current selection belongs to, or the selection itself. */
const cladeOf = id => state.speciesById.get(id)?.clade || id;

/* What to call the current selection in prose: a binomial for a species, the
   clade name for a clade. */
const selectionLabel = id =>
  state.speciesById.get(id)?.binomial || state.taxaById.get(id)?.clade || id;

/* Muscles a source records for this taxon, absences excluded. Drives the counts
   in the taxon picker, so the number beside "Caudata" is the number of cards
   selecting Caudata will actually produce. */
const recordedCount = id => state.muscles.reduce((n, m) => {
  const p = presenceFor(m, id);
  return n + (p !== null && p !== 'no' ? 1 : 0);
}, 0);

/* ---------- naming ---------- */

/* A name belongs to an occurrence, not to the homology group, so any view with
   a taxon selected has to show that taxon's name. The group's preferred label
   is a fallback and nothing more: a student with a cat open in front of them
   should read "Subscapularis", not "Subcoracoscapularis", and "Teres minor",
   not "Scapulohumeralis anterior". Both are already in the record. */
function muscleLabel(m, id) {
  if (!id) return m.name;
  if (state.speciesById.has(id)) {
    const o = (m.occurrences || []).find(x => x.species === id);
    return (o && o.name) ? o.name : m.name;
  }
  /* A clade has no name of its own — its species do. Take the first row that
     carries one; where they disagree, the occurrence table shows all of them. */
  const named = occurrencesIn(m, id).find(o => o.name);
  return named ? named.name : m.name;
}

/* Some occurrence names are a list of the taxon's muscles rather than one name
   — the therian hypobranchials run to eleven — so anywhere the name sits in a
   dense list it is clipped, with the whole string kept in the tooltip. */
const clip = (s, n = 110) => s.length <= n ? s
  : s.slice(0, s.lastIndexOf(' ', n) + 1 || n).trimEnd() + '…';

/* ---------- rendering ---------- */

/* Re-rendering usually makes the document shorter (a search narrows the list, a
   view switch replaces it). Without this the browser keeps the old scroll offset
   and the user lands on blank space below the new content. */
function resetScroll() {
  if (window.scrollY > 0) window.scrollTo({ top: 0, behavior: 'auto' });
}

function render({ keepScroll = false } = {}) {
  /* Every path that changes `state.view` ends in a render, so syncing the nav
     here is the only way it cannot drift. Doing it at the call sites missed
     four of them — openMuscle, the breadcrumb, typing in the search box and
     clicking a facet — so opening a muscle from the Skeleton view left
     "Skeleton" lit while a detail page was on screen. */
  syncViewButtons();
  renderSidebar();
  const main = document.getElementById('main');

  if (state.view === 'phylogeny') { main.innerHTML = renderPhylogeny(); }
  else if (state.view === 'skeleton') { main.innerHTML = renderSkeleton(); }
  else if (state.view === 'hierarchy') { main.innerHTML = renderHierarchy(); }
  else if (state.view === 'detail' && state.current) { main.innerHTML = renderDetail(state.current); }
  else { main.innerHTML = renderList(); }

  /* Every select in a view body writes one state key and re-renders in place.
     Keeping the scroll position matters here: changing the taxon or the
     attachment source is a comparison, and being thrown back to the top of a
     long tree makes it impossible to see what changed. */
  const bindSelect = (id, key) => {
    const el = main.querySelector('#' + id);
    if (el) el.addEventListener('change', () => {
      state[key] = el.value; render({ keepScroll: true });
    });
  };
  bindSelect('phylo-scope', 'phyloScope');
  bindSelect('skel-source', 'skeletonSource');
  bindSelect('bone-a', 'boneA');
  bindSelect('bone-b', 'boneB');

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
  const { rows, absent } = filtered();
  const taxonId = state.taxon;
  const clade = taxonId ? esc(selectionLabel(taxonId)) : '';

  if (!rows.length) {
    /* An empty query with filters on is a real dead end — Myxini plus the thigh
       — and quoting the empty search box at the reader ("No muscle matches “”")
       names the wrong culprit. Say which constraint is doing the excluding. */
    const what = state.query ? `matches “${esc(state.query)}”` : 'is on record';
    const where = [taxonId && `in <strong>${clade}</strong>`, activeFilterLabel()]
      .filter(Boolean).join(' · ');
    return `<div class="empty">No muscle ${what}${where ? ` ${where}` : ''}.<br>
            Try a synonym (<em>dorsalis scapulae</em>), a bone (<em>coracoid</em>), ${
              taxonId ? 'another taxon, ' : ''}or clear the filters.</div>`
           + absentBlock(absent, taxonId);
  }

  const scope = [taxonId && `recorded in <strong>${clade}</strong>`, activeFilterLabel()]
    .filter(Boolean).join(' · ');
  const bar = `<div class="resultbar"><strong>${rows.length}</strong> ${rows.length === 1 ? 'muscle' : 'muscles'}
    ${state.query ? `matching “${esc(state.query)}”` : ''}
    ${scope}</div>`;

  const HIT_LABEL = {
    'taxon-name': 'name', synonym: 'also known as', attachment: 'attaches to',
    part: 'part', group: 'group', development: 'development',
    joint: 'crosses', motion: 'motion',
    origin: 'origin', insertion: 'insertion',
    action: 'action', innervation: 'innervation',
  };
  /* With a taxon selected the card is about that taxon, so it takes that
     taxon's name for the muscle and demotes the group label to the sub-line.
     Without one there is no taxon to name it in, and the group label leads. */
  const cards = rows.map(({ muscle: m, hit }) => {
    const conf = (m.homology || {}).confidence;
    const nTaxa = (m.occurrences || []).filter(o => (o.present || 'yes') !== 'no').length;
    const local = muscleLabel(m, taxonId);
    const renamed = local !== m.name;
    /* `yes` is the unmarked case and needs no chip. The others are hedged
       records — some species of the clade, a flagged identification, a fossil
       reconstruction — and a card that looks identical to a scored one would
       pass all three off as observations. */
    const pres = taxonId ? presenceFor(m, taxonId) : null;
    const presChip = pres && pres !== 'yes'
      ? `<span class="pres-tag pres-${esc(pres)}">${esc(pres)}</span>` : '';
    let hitLine = '';
    if (hit && hit.kind !== 'name') {
      /* Say which field matched. Without this a prose hit is baffling — the
         card shows a muscle whose name has nothing to do with what was typed
         and gives no reason. `extra` carries the clade for taxon-specific
         rows, so a hit on the therian innervation says so. */
      const base = HIT_LABEL[hit.kind] || 'also known as';
      const label = hit.extra ? `${esc(hit.extra)} ${base}` : base;
      hitLine = `<div class="hit">${label}: <em>${esc(clip(hit.text))}</em></div>`;
    }
    return `<article class="mcard" data-goto="${m.id}" tabindex="0">
      <h4 title="${esc(local)}">${esc(clip(local, 64))}${presChip}</h4>
      ${renamed ? `<div class="groupname">group: ${esc(m.name)}</div>` : ''}
      <div class="sub">${esc(m._regionLabel)}${m.subregion ? ` · ${esc(m.subregion)}` : ''} · present in ${nTaxa} ${nTaxa === 1 ? 'taxon' : 'taxa'}${conf ? ` · ${esc(conf)}` : ''}</div>
      ${hitLine}
    </article>`;
  }).join('');

  return bar + `<div class="cardgrid">${cards}</div>` + absentBlock(absent, taxonId);
}

/* The muscles a source examined this taxon for and did not find. Kept, because
   "the salamander has no teres major" is a result worth reading, and demoted,
   because it is not an answer to "what am I looking at". */
function absentBlock(absent, taxonId) {
  if (!absent.length || !taxonId) return '';
  const clade = esc(selectionLabel(taxonId));
  const links = absent
    .sort((a, b) => regionRank(a.region) - regionRank(b.region) || a.name.localeCompare(b.name))
    .map(m => `<a data-goto="${m.id}" href="#${esc(m.id)}">${esc(m.name)}</a>`)
    .join('<span class="sep">, </span>');
  return `<p class="cellnote absentlist"><strong>${absent.length}</strong> further
    ${absent.length === 1 ? 'record was' : 'records were'} examined in ${clade}
    and reported absent: ${links}</p>`;
}

function activeFilterLabel() {
  const f = state.filters, parts = [];
  if (f.region) parts.push(`in <strong>${esc(f.region)}</strong>`);
  if (f.segment) parts.push(`segment <strong>${esc(f.segment)}</strong>`);
  if (f.mass) parts.push(`<strong>${esc(f.mass)}</strong> mass`);
  if (f.layer) parts.push(`layer <strong>${esc(f.layer)}</strong>`);
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
    spanChip(m),
    h.confidence && `<span class="chip conf-${esc(h.confidence)}">homology: ${esc(h.confidence)}</span>`
  ].filter(Boolean).join('');

  const oia = `<dl class="oia">
    ${defRow('Origin', c.origin)}
    ${defRow('Insertion', c.insertion)}
    ${defRow('Action', c.action)}
    ${renderActions(m)}
    ${defRow('Innervation', c.innervation)}
    ${renderNerves(m)}
    ${defRow('Development', m.developmental)}
  </dl>`;

  /* Which scheme the names below are reconciled under. Synonyms accumulate and
     never expire, but when two workers homologise a muscle differently the more
     recent comparative treatment governs — so the reader needs to know whose it
     is. Rendered with the synonyms because that is the claim it qualifies. */
  const auth = h.authority && h.authority.source
    ? `<p class="cellnote">Homology follows ${sourceLink(h.authority.source)}${
        h.authority.basis === 'curated'
          ? ` — <em>${esc(h.authority.note || 'kept against a more recent source')}</em>`
          : ''}</p>` : '';

  const syn = ((m.synonyms || []).length || auth)
    ? `<section class="block"><h3>Also called</h3>
       ${(m.synonyms || []).length
         ? `<p class="synonyms">${m.synonyms.map(s => `<code>${esc(s)}</code>`).join(' ')}</p>`
         : ''}
       ${auth}</section>` : '';

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

/* The nerve's own name, plus the chain it descends through. The chain is the
   informative part: it is what says the supinator's supply is a dorsal-division
   nerve, and therefore agrees with the muscle sitting in the dorsal limb-bud
   mass. Shown as a trail rather than a single chip so that agreement — or a
   disagreement worth arguing about — is legible without leaving the page. */
function nerveTrail(id) {
  const out = [];
  let cur = id, guard = 0;
  while (cur && guard++ < 20) {
    const n = state.nervesById.get(cur);
    if (!n) break;
    out.unshift(n);
    cur = n.partOf;
  }
  return out;
}

function nerveDivision(id) {
  return nerveTrail(id).reverse().find(n => n.division)?.division || null;
}

/* Actions as joint + motion, alongside the joints the attachments say the
   muscle spans. The two are independent: actions come from what a source
   claims, spanning from where the muscle attaches. Showing them together is
   the point — a muscle listed as acting on a joint it does not span is either
   a scoring error or one that acts through another muscle's tendon, and both
   are worth seeing. */
function renderActions(m, taxonId) {
  const rows = m.actions;
  const spans = typeof jointsCrossed === 'function' ? jointsCrossed(m, taxonId || null) : [];
  if (!rows && !spans.length) return '';

  const acted = new Set((rows || []).map(r => r.joint));
  const byJoint = new Map();
  for (const r of rows || []) {
    if (!byJoint.has(r.joint)) byJoint.set(r.joint, []);
    byJoint.get(r.joint).push(r.motion);
  }

  const acts = [...byJoint].map(([jid, motions]) => {
    const off = spans.length && !spans.includes(jid);
    return `<li class="act${off ? ' act-unspanned' : ''}"
      ${off ? 'title="Acts here without spanning the joint — through a tendon, or a scoring error"' : ''}>
      <span class="act-joint">${esc(jointLabel(jid, taxonId))}</span>
      <span class="act-motion">${motions.map(esc).join(', ')}</span></li>`;
  }).join('');

  /* Joints it spans but is not recorded as acting on. Not an error — most
     muscles cross a joint they do not move — but it is what makes the list
     readable as "these are the joints in play". */
  const passive = spans.filter(j => !acted.has(j));

  return `<dt>Joints</dt><dd>
    ${acts ? `<ul class="acts">${acts}</ul>` : ''}
    ${passive.length ? `<div class="spans">also crosses
      ${passive.map(j => `<span class="chip">${esc(jointLabel(j, taxonId))}</span>`).join(' ')}</div>` : ''}
  </dd>`;
}

function renderNerves(holder, taxonId) {
  const rows = holder.nerves;
  if (!rows || !rows.length) return '';
  const items = rows.map(r => {
    const trail = nerveTrail(r.nerve);
    if (!trail.length) return '';
    const leaf = trail[trail.length - 1];
    const label = taxonId
      ? (leaf.taxonNames || []).find(tn => (tn.taxa || []).includes(taxonId))?.name || leaf.label
      : leaf.label;
    const div = nerveDivision(r.nerve);
    return `<li>
      <span class="nerve-name">${esc(label)}</span>
      ${r.segments ? `<span class="nerve-seg">${esc(r.segments)}</span>` : ''}
      ${div ? `<span class="nerve-div nerve-div-${esc(div)}">${esc(div)}</span>` : ''}
      ${trail.length > 1
        ? `<span class="nerve-trail">${trail.slice(0, -1).map(n => esc(n.label)).join(' › ')}</span>`
        : ''}
      ${r.note ? `<span class="cellnote">${emph(r.note)}</span>` : ''}
    </li>`;
  }).join('');
  return `<dt>Nerve</dt><dd><ul class="nerves">${items}</ul></dd>`;
}

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
    (a, b) => (state.taxonOrder.get(a.taxon) ?? 99) - (state.taxonOrder.get(b.taxon) ?? 99)
           || String(a.species).localeCompare(String(b.species)));
  if (!occ.length) return `<p class="cellnote">No taxon-level records yet.</p>`;

  const rows = occ.map(o => {
    const t = state.taxaById.get(o.taxon) || { clade: o.taxon, label: '', color: '#999' };
    const present = o.present || 'yes';
    const absent = present === 'no';

    const micro = ['origin', 'insertion', 'action', 'innervation']
      .filter(k => o[k])
      .map(k => `<div><b>${k}</b> ${esc(o[k])}</div>`).join('');

    const cites = (o.sources || []).map(k => sourceLink(k)).join(' ');

    /* An ancestral fin muscle has no name in a tetrapod because it is not one
       muscle there — it is the field that became several. Those several name it
       with `descends-from`, rendered once under Fin-to-limb ancestry; naming them here
       too would give one fact two homes, which is what `parts` exists to stop. */
    const subdivided = !o.name && !absent && state.muscles.some(f =>
      ((f.homology || {}).correspondences || [])
        .some(e => e.relation === 'descends-from' && e.to === m.id));

    /* The species is the observation; the clade is what it rolls up into. Showing
       the binomial here is the difference between "birds have this" and "somebody
       looked at an ostrich". */
    const sp = state.speciesById.get(o.species);
    return `<tr class="${absent ? 'absent' : ''}">
      <td><div class="taxoncell"><span class="swatch" style="background:${esc(t.color)}"></span>
        <span class="clade">${esc(t.clade)}</span></div>
        ${sp ? `<span class="binomial">${esc(sp.binomial)}</span>` : ''}
        <span class="common">${esc((sp && sp.common) || t.label || '')}</span>
        ${o.speciesBasis && o.speciesBasis !== 'note' && o.speciesBasis !== 'source'
          ? `<span class="basis${o.speciesBasis === 'generalised' ? ' basis-gen' : ''}"
              title="How this row was attributed to a species: ${
              o.speciesBasis === 'survey'
                ? 'the survey it cites names this species as its exemplar for the clade'
                : o.speciesBasis === 'generalised'
                ? 'NOT a specimen. The source describes the clade rather than an animal, so this row is a generalisation and no one dissection stands behind it'
                : 'no better evidence — the clade default, and a guess'}">${esc(o.speciesBasis)}</span>` : ''}</td>
      <td><span class="pres pres-${esc(present)}">${esc(present)}</span></td>
      <td>${o.name ? `<span class="localname">${esc(o.name)}</span>`
          : subdivided ? `<span class="localname subdiv">No single homologue — subdivided;
              see <em>Fin-to-limb ancestry</em> below</span>`
          : '<span class="pres-no">—</span>'}
        ${renderDivision(o)}
        ${o.nerves ? `<dl class="oia occ-nerves">${renderNerves(o, o.taxon)}</dl>` : ''}
        ${micro ? `<div class="microdl">${micro}</div>` : ''}
        ${o.note ? `<div class="cellnote">${emph(o.note)}</div>` : ''}
        ${cites ? `<div class="cites">${cites}</div>` : ''}</td>
    </tr>`;
  }).join('');

  return `<div class="tablewrap"><table class="occ">
    <colgroup><col class="c-taxon"><col class="c-pres"><col class="c-body"></colgroup>
    <thead><tr><th>Taxon</th><th>Present</th><th>Local name, attachments, notes and source</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`;
}

/* How far the homology group is split in this taxon.

   `single` is a claim — a source looked and found one muscle — so it is shown,
   not treated as the empty case. An occurrence with no `division` says nothing
   either way and renders nothing, the same convention `present` follows.

   Parts whose membership is argued or varies are marked rather than dropped:
   the sartorius and the gemelli are each claimed by two fields, and hiding that
   would make the count look settled when it is not. */
const DIVISION_LABEL = {
  single: 'undivided',
  heads: 'one muscle, several heads',
  divided: 'divided into separate muscles',
  variable: 'division varies within the clade',
};

/* A part's own origin and insertion, where the join could work out which rows
   belong to it. Before this existed an occurrence held one union of attachment
   rows, so a record that is one muscle in a salamander and six in a human could
   say that six sites are used and never which muscle used which. Rendered as
   one line per part rather than a table: the table for the whole occurrence is
   already below, and this is the breakdown of it. */
function partAttachments(part, taxon) {
  const a = part.attachments;
  if (!a || (!(a.origin || []).length && !(a.insertion || []).length)) return '';
  const site = r => {
    const label = esc(taxon ? elementLabel(r.element, taxon)
                            : state.elementsById.get(r.element)?.label || r.element);
    const link = `<a href="#element=${encodeURIComponent(r.element)}">${label}</a>`;
    const lm = r.landmark
      ? `<span class="sep"> · </span><a href="#element=${encodeURIComponent(r.landmark)}">${esc(taxon ? elementLabel(r.landmark, taxon)
          : state.elementsById.get(r.landmark)?.label || r.landmark)}</a>` : '';
    return link + (r.side ? ` <span class="sep">${esc(r.side)}</span>` : '') + lm;
  };
  const end = rows => rows.length
    ? rows.map(r => r.muscle
        ? `<a class="pill flat" data-goto="${esc(r.muscle)}">${esc(state.byId.get(r.muscle)?.name || r.muscle)}</a>`
        : site(r)).join('<span class="sep">, </span>')
    : '<span class="sep">—</span>';
  return `<span class="partatt">${end(a.origin || [])}
      <span class="sep">&rarr;</span> ${end(a.insertion || [])}</span>`;
}

/* Where a muscle starts and where it ends, in body regions, derived in the build
   from the elements it attaches to. `region` says where the record is FILED and
   has to be a single value because it is half the extraction key; it cannot also
   say where the muscle goes. For a muscle that stays put the two ends read the
   same and the chip is a tautology worth showing anyway, because the reader
   cannot otherwise tell that from an unrecorded span. For a boundary crosser it
   is the whole point: the human latissimus dorsi is filed under `pectoral` and
   runs from vertebrae, ribs and ilium to the humerus. */
function spanChip(holder) {
  const s = holder.spans;
  if (!s || !s.origin || !s.insertion) return '';
  const j = a => a.join(' + ');
  return `<span class="chip span${s.crosses ? ' crosses' : ''}" title="${
    s.crosses ? 'crosses a region boundary' : 'stays within one region'}">${
    esc(j(s.origin))} &rarr; ${esc(j(s.insertion))}</span>`;
}

function renderDivision(o) {
  if (!o.division) return '';
  const firm = (o.parts || []).filter(x => (x.membership || 'established') === 'established');
  /* A "+" means the firm count is a floor — either some parts are disputed or
     the source stopped short of a full list — so the count reads as a range and
     takes the plural regardless. */
  const open = o.parts && (o.parts.length !== firm.length || o.partsOpen);
  const count = o.parts
    ? `<span class="chip">${firm.length}${open ? '+' : ''} part${firm.length === 1 && !open ? '' : 's'}</span>`
    : '';

  const parts = (o.parts || []).map(x => {
    const mem = x.membership || 'established';
    const rec = x.muscle ? state.byId.get(x.muscle) : null;
    const body = rec
      ? `<a class="pill" data-goto="${esc(rec.id)}">${esc(x.name)}</a>`
      : `<span class="pill flat">${esc(x.name)}</span>`;
    const tag = mem === 'established' ? ''
      : `<span class="memtag mem-${esc(mem)}" title="${esc(x.note || mem)}">${esc(mem)}</span>`;
    return `<li>${body}${tag}${partAttachments(x, o.taxon)}${x.note ? `<span class="cellnote">${emph(x.note)}</span>` : ''}</li>`;
  }).join('');

  return `<div class="division div-${esc(o.division)}">
    <span class="divstate">${esc(DIVISION_LABEL[o.division] || o.division)}</span> ${count}
    ${parts ? `<ul class="parts">${parts}</ul>` : ''}
    ${o.partsOpen ? `<span class="cellnote">The source's list is open — the count is a floor.</span>` : ''}
    ${o.divisionNote ? `<div class="cellnote">${emph(o.divisionNote)}</div>` : ''}
  </div>`;
}

/* One array, four relations, and the direction of each is the point. `serial` is
   symmetric and the build closes it; `descends-from` and `corresponds-to-part-of`
   are directed, so the reverse edge is found by scanning rather than stored —
   storing it would let the two directions drift apart. A muscle corresponding to
   a GROUP of others is simply several edges sharing a target; there is no group
   object, because a stored group goes stale the moment a record splits. */
const AXIS_LABEL = {
  'forelimb-hindlimb': 'forelimb ↔ hindlimb',
  'pharyngeal-arch': 'pharyngeal arch series',
};

function renderCorrespondences(m, h) {
  const own = h.correspondences || [];
  const pill = id => {
    const t = state.byId.get(id);
    return t ? `<a class="pill" data-goto="${t.id}">${esc(t.name)}</a>` : '';
  };
  const chips = e => {
    let c = '';
    if (e.basis) c += ` <span class="chip">basis: ${esc(e.basis)}</span>`;
    if (e.confidence) c += ` <span class="chip">${esc(e.confidence)}</span>`;
    if ((e.taxa || []).length) c += ` <span class="chip">${e.taxa.map(esc).join(', ')}</span>`;
    if ((e.sources || []).length) c += ' ' + e.sources.map(k => sourceLink(k)).join(' ');
    return c;
  };
  const para = e => {
    let s = '';
    if (e.note) s += `<p>${emph(e.note)}</p>`;
    return s;
  };

  let out = '';

  const serial = own.filter(e => e.relation === 'serial');
  const none = own.filter(e => e.relation === 'no-counterpart');
  if (serial.length || none.length) {
    out += `<div class="callout"><h4>Serial correspondence</h4>`;
    for (const axis of new Set([...serial, ...none].map(e => e.axis))) {
      const hits = serial.filter(e => e.axis === axis);
      const nil = none.find(e => e.axis === axis);
      out += `<p class="synonyms" style="margin:.4rem 0 .3rem"><strong>${esc(AXIS_LABEL[axis] || axis)}</strong></p>`;
      if (hits.length) {
        out += `<div class="pills">${hits.map(e => pill(e.to)).join('')}</div>`;
        out += hits.map(e => chips(e) ? `<p class="synonyms">${chips(e)}</p>` : '').join('');
        out += hits.map(para).join('');
      }
      /* An asserted absence is a claim, not a blank. */
      if (nil) out += `<p><strong>No counterpart.</strong>${chips(nil)}</p>` + para(nil);
    }
    out += `</div>`;
  }

  const partOf = own.filter(e => e.relation === 'corresponds-to-part-of');
  const claimedHere = state.muscles.flatMap(o =>
    ((o.homology || {}).correspondences || [])
      .filter(e => e.relation === 'corresponds-to-part-of' && e.to === m.id)
      .map(e => ({ e, from: o })));
  if (partOf.length || claimedHere.length) {
    out += `<div class="callout open"><h4>Partial correspondence</h4>`;
    for (const e of partOf) {
      const what = e.fromPart ? `<strong>${esc(e.fromPart)}</strong>` : 'This muscle';
      const where = e.toPart ? ` — ${esc(e.toPart)}` : '';
      out += `<p>${what} corresponds to part of ${pill(e.to)}${where}${chips(e)}</p>` + para(e);
    }
    for (const { e, from } of claimedHere) {
      const what = e.fromPart ? `<strong>${esc(e.fromPart)}</strong>` : from.name;
      out += `<p>${pill(from.id)}${e.fromPart ? ` — ${esc(e.fromPart)}` : ''} is claimed as part of this muscle${chips(e)}</p>`;
    }
    out += `</div>`;
  }

  return out;
}

function renderHomologyBlock(m, h) {
  if (!h.notes && !h.openQuestion && !h.teaching &&
      !(h.correspondences || []).length) return '';
  let out = `<section class="block"><h3>Homology</h3>`;
  if (h.notes) out += `<div class="callout"><h4>Assessment</h4><p>${emph(h.notes)}</p></div>`;
  if (h.openQuestion) out += `<div class="callout open"><h4>Open question</h4><p>${esc(h.openQuestion)}</p></div>`;

  out += renderCorrespondences(m, h);
  if (h.caveat) out += `<div class="callout caution"><h4>Source caveat</h4><p>${esc(h.caveat)}</p></div>`;
  if (h.teaching) out += `<div class="callout teach"><h4>Teaching use</h4><p>${esc(h.teaching)}</p></div>`;
  return out + `</section>`;
}

/* Ancestry is stored once, on the descendant, pointing back. The forward view —
   what an ancestral fin muscle gave rise to — is found by scanning, which is the
   reverse of how `derivatives` did it. Storing it on the descendant is what lets
   one tetrapod muscle claim several ancestors: `ischioflexorius` has three. */
function descendsFrom(m) {
  return ((m.homology || {}).correspondences || [])
    .filter(e => e.relation === 'descends-from');
}

function renderAncestry(m) {
  const ancestors = descendsFrom(m);

  /* Everything that names this record as its ancestor, grouped by girdle. */
  const children = {};
  for (const o of state.muscles) {
    for (const e of descendsFrom(o)) {
      if (e.to !== m.id) continue;
      (children[e.girdle || 'appendicular'] ||= []).push(o.id);
    }
  }
  const hasForward = Object.keys(children).length;

  if (!ancestors.length && !hasForward && !m.ancestralNode) return '';

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
    for (const [girdle, ids] of Object.entries(children)) {
      out += `<p class="synonyms" style="margin:.5rem 0 .3rem"><strong>${esc(girdle)}</strong></p>
        <div class="pills" style="margin-bottom:.5rem">${ids.sort().map(link).join('')}</div>`;
    }
  }

  if (ancestors.length) {
    out += `<p class="synonyms" style="margin-bottom:.4rem">Derived from the ancestral fin muscle:</p>
      <div class="pills">${ancestors.map(e => link(e.to)).join('')}</div>`;
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
  /* Counted over the taxon-scoped set, not the whole dataset. With Caudata
     selected the list can only ever show what Caudata has, so a Region badge
     reading the global figure would promise cards that cannot appear. */
  const rows = scopeToTaxon(search(state.query), state.taxon).rows;
  const el = document.getElementById('sidebar');

  const count = (key, val) => rows.filter(r => FACET_MATCH[key](r.muscle, val)).length;

  const regions = [...new Set(state.muscles.map(m => m.region))]
    .sort((a, b) => regionRank(a) - regionRank(b));
  const confs = ['well-supported', 'moderate', 'contested', 'uncertain'];

  /* Proximodistal for segment, superficial-to-deep then axis for layer: these
     vocabularies have their own order and alphabetising them would hide it.
     Values present in the data but missing from these lists still appear, at
     the end, so a new term shows up rather than silently vanishing. */
  const ordered = (field, order) => {
    const found = new Set(state.muscles.map(m => m[field]).filter(Boolean));
    return [...order.filter(v => found.has(v)),
            ...[...found].filter(v => !order.includes(v)).sort()];
  };
  const segments = ordered('segment',
    ['cranial', 'axial', 'girdle', 'stylopod', 'zeugopod', 'autopod', 'fin']);
  const masses = ordered('mass',
    ['dorsal', 'ventral', 'somitic', 'somitic-axial', 'branchiomeric', 'extraocular']);
  const layers = ordered('layer',
    ['superficialis', 'intermediate', 'profundus', 'preaxial', 'postaxial', 'primaxial']);

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

  const plain = v => ({ value: v, label: v });
  el.innerHTML =
    facet('Region', 'region', regions.map(plain)) +
    facet('Region span', 'spans', [
      { value: 'crosses', label: 'crosses a boundary' },
      { value: 'within', label: 'stays within one' },
      { value: 'none', label: 'no attachments scored' }]) +
    facet('Segment', 'segment', segments.map(plain)) +
    facet('Developmental mass', 'mass', masses.map(plain)) +
    facet('Layer', 'layer', layers.map(plain)) +
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

/* The global taxon. Built once — the option list and its counts do not change —
   and restored between sessions, because a student works through one animal
   over several sittings and re-picking it every time is friction for nothing. */
function wireTaxonPicker() {
  const sel = document.getElementById('taxon');
  if (!sel) return;

  const sorted = [...state.taxa].sort(
    (a, b) => (state.taxonOrder.get(a.id) ?? 99) - (state.taxonOrder.get(b.id) ?? 99));

  /* Clades AND the species under them. A clade is a rollup and reads as one —
     "Aves (consensus of 5 species)" — while a species is a single animal
     somebody dissected. Picking the species is how you see what that animal
     actually has, rather than what its clade agrees on. */
  sel.innerHTML = `<option value="">All taxa — no animal selected</option>` +
    sorted.map(t => {
      const kids = (state.speciesByClade.get(t.id) || [])
        .filter(sp => recordedCount(sp.id) > 0)
        .sort((a, b) => recordedCount(b.id) - recordedCount(a.id));
      const n = recordedCount(t.id);
      const head = `<option value="${esc(t.id)}">${t.fossil ? '† ' : ''}${esc(t.clade)} — ${esc(t.label)} (${n}${
        kids.length > 1 ? `, consensus of ${kids.length} species` : ''})</option>`;
      const rows = kids.map(sp => `<option value="${esc(sp.id)}">    ${sp.fossil ? '† ' : ''}${
        esc(sp.binomial)}${sp.common ? ` — ${esc(sp.common)}` : ''} (${recordedCount(sp.id)})</option>`).join('');
      return `<optgroup label="${esc(t.clade)}">${head}${rows}</optgroup>`;
    }).join('');

  let saved = '';
  try { saved = localStorage.getItem('taxon') || ''; } catch {}
  if (saved && state.taxaById.has(saved)) state.taxon = saved;
  sel.value = state.taxon;
  sel.classList.toggle('on', !!state.taxon);

  sel.addEventListener('change', () => {
    state.taxon = sel.value;
    sel.classList.toggle('on', !!state.taxon);
    try { localStorage.setItem('taxon', state.taxon); } catch {}
    /* A bone the new taxon lacks is no longer in the pair-lookup dropdowns, so
       leaving the id in state would run a query against a control showing
       "— any —". Drop the selection rather than the explanation. */
    if (state.taxon && typeof elementPresentIn === 'function') {
      for (const k of ['boneA', 'boneB']) {
        if (state[k] && elementPresentIn(state[k], state.taxon) === 'no') state[k] = '';
      }
    }
    render();
  });
}

function wireUI() {
  wireTaxonPicker();

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
      render();
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
}

/* ---------- utils ---------- */

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/* The prose fields are written in the notes as Markdown and were rendered with
   `esc` alone, so 46 strings across the dataset showed their asterisks: the
   acromion's "**Scored on topological correspondence**", the prepollex's
   "**Monotremes have one too**". The emphasis is doing real work in these notes —
   it marks the sentence the author wants read first — and printing it as
   punctuation buried that sentence in the paragraph.

   Escapes FIRST and only then introduces tags, so no note can inject markup:
   any `<` in the source is already `&lt;` by the time the patterns run.
   Deliberately just bold, italic and `code` — these are captions, not documents,
   and a fuller Markdown pass would be a parser nobody needs here. */
function emph(s) {
  return esc(s)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(—-])\*([^*\s][^*]*)\*(?=$|[\s.,;:)?!—-])/g, '$1<em>$2</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

boot().catch(err => {
  document.getElementById('main').innerHTML =
    `<div class="empty">Could not load the data files.<br><code>${esc(err.message)}</code><br><br>
     If you opened <code>index.html</code> directly from disk, browsers block <code>fetch</code> on
     <code>file://</code> URLs. Run a local server instead:<br>
     <code>python3 -m http.server 8000</code></div>`;
  console.error(err);
});
