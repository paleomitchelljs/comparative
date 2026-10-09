/* Muscle simulator page. All the mechanics are in engine.js; this file is the
   controls, the SVG, and the comparison table.

   Poses are global and keyed by degree-of-freedom id, so one "open the jaw"
   drives every panel whose animal has a jaw. A mode decides where each panel's
   pose comes from:
     pose    the sliders and dragged handles (S.pose)
     action  S.pose with one joint overridden, run from rest to its target
     muscle  one muscle group contracting alone, from a stretched start */

(() => {
  'use strict';
  const E = window.SimEngine;
  const SVGNS = 'http://www.w3.org/2000/svg';

  const $ = (sel, root = document) => root.querySelector(sel);
  const esc = s => String(s ?? '').replace(/[&<>"']/g,
    c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fetchJSON = url => fetch(url).then(r => {
    if (!r.ok) throw new Error(`${url}: ${r.status}`);
    return r.json();
  });
  function svg(tag, attrs = {}) {
    const n = document.createElementNS(SVGNS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));

  const S = {
    index: null, sources: new Map(), scored: new Map(),
    models: new Map(), region: 'cranial', slots: [],
    pose: {}, mode: 'pose', action: null, amount: 1, sel: null,
    t: 0, playing: false, dir: 1, loop: false,
    startFrom: 'stretched', labels: true, bones: false, strain: true,
    panels: [], runCache: new Map(), colors: null,
  };

  /* ---------- colour ---------- */

  function palette() {
    if (S.colors) return S.colors;
    const cs = getComputedStyle(document.body);
    const hex = n => {
      const v = cs.getPropertyValue(n).trim().replace('#', '');
      return [0, 2, 4].map(i => parseInt(v.slice(i, i + 2), 16));
    };
    return (S.colors = { rest: hex('--rest'), short: hex('--short'), long: hex('--long') });
  }
  const mix = (a, b, t) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`;
  function strainColor(eps) {
    const p = palette();
    if (!S.strain) return mix(p.rest, p.rest, 0);
    const t = clamp(eps / 0.18, -1, 1);
    return t < 0 ? mix(p.rest, p.short, -t) : mix(p.rest, p.long, t);
  }

  /* ---------- lookups ---------- */

  const jointInfo = id => S.index.joints.find(j => j.id === id);
  const groupInfo = id => S.index.groups.find(g => g.id === id);
  const regionInfo = () => S.index.regions.find(r => r.id === S.region);
  const models = () => S.slots.map(id => S.models.get(id));
  const shortSource = key => S.sources.get(key) || key;

  function poseFor(model) {
    const p = Object.assign({}, S.pose);
    if (S.mode === 'action' && S.action && model.dofById.has(S.action.joint)) {
      const [a, b] = E.actionRange(model, S.action.joint, S.action.dir, S.amount);
      p[S.action.joint] = a + (b - a) * S.t;
    } else if (S.mode === 'muscle') {
      const run = muscleRun(model);
      if (run) {
        const f = S.t * (run.length - 1), i = Math.floor(f), j = Math.min(i + 1, run.length - 1);
        return E.lerpPose(run[i], run[j], f - i);
      }
    }
    return p;
  }

  /* The muscle in this model that the selected group contracts, and its run. */
  function groupMuscles(model) {
    return model.muscles.filter(m => m.group === S.sel && m.paths && m.paths.length);
  }
  function muscleRun(model) {
    const mu = groupMuscles(model)[0];
    if (!mu) return null;
    const key = `${model.id}|${mu.id}|${S.startFrom}|${S.startFrom === 'current' ? JSON.stringify(S.pose) : ''}`;
    if (!S.runCache.has(key)) {
      const base = S.startFrom === 'current' ? S.pose : {};
      const start = S.startFrom === 'current' ? Object.assign({}, S.pose) : E.stretchedPose(model, mu, base);
      S.runCache.set(key, E.contraction(model, mu, start));
    }
    return S.runCache.get(key);
  }

  /* ---------- panels ---------- */

  function makePanel(model, index) {
    const fig = document.createElement('figure');
    fig.className = 'panel';
    fig.innerHTML = `<header><h3><i>${esc(model.label)}</i> <span class="common">${esc(model.common)}</span></h3>
      <span class="tags">${esc(model.group)} · ${esc(model.suspension)}</span></header>`;

    const root = svg('svg', {
      viewBox: model.viewBox.join(' '), class: 'simsvg', role: 'img',
      'aria-label': `${model.label}: schematic ${model.view} view of the skull with its jaw muscles`,
    });
    const gBones = svg('g'), gLinks = svg('g'), gMus = svg('g'), gMarks = svg('g'), gHandles = svg('g');
    root.append(gBones, gLinks, gMus, gMarks, gHandles);

    const segG = new Map();
    for (const seg of model.segments) {
      const g = svg('g');
      const title = svg('title'); title.textContent = seg.label + (seg.element ? ` (${seg.element})` : '');
      g.append(title);
      for (const p of seg.paths) g.append(svg('path', { d: p.d, class: p.class }));
      if (seg.labelAt) {
        const t = svg('text', { x: seg.labelAt[0], y: seg.labelAt[1], class: 'bonelabel', 'text-anchor': 'middle' });
        t.textContent = seg.label.replace(/ \(.*\)$/, '');
        g.append(t);
      }
      gBones.append(g); segG.set(seg.id, g);
    }

    const links = (model.links || []).map(l => {
      const bg = svg('line', { class: 'link-bg', 'stroke-width': l.width + 3 });
      const ln = svg('line', { class: 'link', 'stroke-width': l.width - 3 });
      const title = svg('title'); title.textContent = l.label;
      ln.append(title);
      gLinks.append(bg, ln);
      return { l, bg, ln };
    });

    const mus = [];
    for (const mu of model.muscles) {
      if (!mu.paths || !mu.paths.length) continue;
      const g = svg('g', { class: 'muscle' });
      const halo = svg('path', { class: 'm-halo' });
      const line = svg('path', { class: 'm-line' });
      const hit = svg('path', { class: 'm-hit' });
      const title = svg('title');
      title.textContent = `${mu.label} — ${mu.actionText}`;
      hit.append(title);
      const label = svg('text', { class: 'mlabel', 'text-anchor': 'middle' });
      label.textContent = mu.short;
      g.append(halo, line, hit, label);
      g.addEventListener('click', ev => { ev.stopPropagation(); selectGroup(S.sel === mu.group ? null : mu.group); });
      gMus.append(g);

      const marks = mu.paths.map(path => {
        const o = svg('circle', { class: 'mark-o', r: 4.5 }), i = svg('circle', { class: 'mark-i', r: 3.4 });
        gMarks.append(o, i);
        return { o, i, path };
      });
      mus.push({ mu, g, halo, line, hit, label, marks });
    }

    const handles = model.dofs.filter(d => d.handle).map(dof => {
      const c = svg('circle', { class: 'handle', r: 9 });
      const title = svg('title');
      const j = jointInfo(dof.id);
      title.textContent = `Drag to ${j ? j.pos.toLowerCase() : 'move'} / ${j ? j.neg.toLowerCase() : 'return'}`;
      c.append(title);
      wireDrag(c, root, model, dof);
      gHandles.append(c);
      return { dof, c };
    });

    root.addEventListener('click', () => { if (S.sel) selectGroup(null); });

    const readout = document.createElement('div');
    readout.className = 'readout';

    const about = document.createElement('details');
    const undrawn = model.muscles.filter(m => !m.paths || !m.paths.length);
    about.innerHTML = `<summary>About this model</summary>
      <p>${esc(model.summary)}</p>
      <p>${esc(model.note)}</p>
      <p>Sources: ${model.sources.map(s => esc(shortSource(s))).join('; ')}.</p>
      ${undrawn.length ? `<p>Recorded but not drawn:</p><ul>${undrawn.map(m =>
        `<li><b>${esc(m.label)}</b>${m.status === 'absent' ? ' (absent)' : m.status === 'contested' ? ' (contested)' : ''} — ${esc(m.reason)}</li>`).join('')}</ul>` : ''}`;

    fig.append(root, readout, about);
    return { model, fig, root, segG, links, mus, handles, readout, index };
  }

  function wireDrag(circle, root, model, dof) {
    let on = false;
    circle.addEventListener('click', ev => ev.stopPropagation());
    circle.addEventListener('pointerdown', ev => {
      on = true; circle.setPointerCapture(ev.pointerId); circle.classList.add('drag');
      // freeze whatever is on screen as the pose, so the drag continues from it
      for (const p of S.panels) {
        const eff = poseFor(p.model);
        for (const d of p.model.dofs) S.pose[d.id] = eff[d.id] || 0;
      }
      setMode('pose');
      ev.preventDefault();
    });
    circle.addEventListener('pointermove', ev => {
      if (!on) return;
      const m = root.getScreenCTM().inverse();
      const pt = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m);
      S.pose[dof.id] = E.dragSolve(model, S.pose, dof.id, dof.handle, pt.x, pt.y);
      frame(); syncPoseSliders();
    });
    const up = () => { on = false; circle.classList.remove('drag'); };
    circle.addEventListener('pointerup', up);
    circle.addEventListener('pointercancel', up);
  }

  function updatePanel(panel) {
    const { model } = panel;
    const pose = poseFor(model);
    const mats = E.matrices(model, pose);

    for (const seg of model.segments) {
      panel.segG.get(seg.id).setAttribute('transform', `matrix(${mats.get(seg.id).join(' ')})`);
    }
    for (const { l, bg, ln } of panel.links) {
      const a = E.landmarkAt(model, mats, l.from), b = E.landmarkAt(model, mats, l.to);
      for (const n of [bg, ln]) { n.setAttribute('x1', a[0]); n.setAttribute('y1', a[1]); n.setAttribute('x2', b[0]); n.setAttribute('y2', b[1]); }
    }

    const selected = S.sel;
    panel.root.classList.toggle('has-sel', !!selected && panel.mus.some(m => m.mu.group === selected));
    for (const el of panel.root.querySelectorAll('.bonelabel')) el.style.display = S.bones ? '' : 'none';

    for (const m of panel.mus) {
      const { mu } = m;
      const pts = mu.paths.map(path => path.map(l => E.landmarkAt(model, mats, l)));
      const d = pts.map(p => 'M' + p.map(q => `${q[0].toFixed(1)} ${q[1].toFixed(1)}`).join(' L')).join(' ');
      const eps = E.muscleLength(model, mats, mu) / model.rest[mu.id] - 1;
      const w = (mu.width || 5) * clamp(Math.pow(1 / (1 + eps), 0.6), 0.75, 1.5);
      m.line.setAttribute('d', d); m.hit.setAttribute('d', d); m.halo.setAttribute('d', d);
      m.line.setAttribute('stroke-width', w.toFixed(2));
      m.halo.setAttribute('stroke-width', (w + 5).toFixed(2));
      m.line.setAttribute('stroke', strainColor(eps));
      m.eps = eps;

      const isSel = selected === mu.group;
      m.g.classList.toggle('sel', isSel);
      const a0 = pts[0][0], a1 = pts[0][pts[0].length - 1];
      m.label.setAttribute('x', ((a0[0] + a1[0]) / 2).toFixed(1)); m.label.setAttribute('y', ((a0[1] + a1[1]) / 2 - 6).toFixed(1));
      m.label.style.display = (S.labels || isSel) ? '' : 'none';
      for (const k of m.marks) {
        const a = k.path[0], z = k.path[k.path.length - 1];
        const pa = E.landmarkAt(model, mats, a), pz = E.landmarkAt(model, mats, z);
        k.o.setAttribute('cx', pa[0]); k.o.setAttribute('cy', pa[1]);
        k.i.setAttribute('cx', pz[0]); k.i.setAttribute('cy', pz[1]);
        k.o.style.display = k.i.style.display = isSel ? '' : 'none';
      }
    }

    for (const { dof, c } of panel.handles) {
      const p = E.landmarkAt(model, mats, dof.handle);
      c.setAttribute('cx', p[0]); c.setAttribute('cy', p[1]);
    }

    panel.readout.innerHTML = model.dofs.map(d => {
      const j = jointInfo(d.id);
      const v = E.nativeValue(d, pose[d.id] || 0);
      return `<span>${esc(j ? j.label : d.id)} <b>${v.toFixed(0)}${esc(d.unit)}</b></span>`;
    }).join('');
  }

  /* ---------- table, detail, controls ---------- */

  function groupsPresent() {
    const ids = new Set();
    for (const m of models()) for (const mu of m.muscles) ids.add(mu.group);
    return S.index.groups.filter(g => ids.has(g.id));
  }

  const pct = x => `${x > 0 ? '+' : x < 0 ? '−' : ''}${Math.abs(x * 100).toFixed(0)}%`;

  function cellFor(model, group) {
    const ms = model.muscles.filter(m => m.group === group.id);
    if (!ms.length) return { html: '<span class="gap" title="Not recorded in this animal\'s source table">·</span>' };
    const drawn = ms.filter(m => m.paths && m.paths.length);
    if (!drawn.length) {
      const m = ms[0];
      const cls = m.status === 'absent' ? 'absent' : m.status === 'contested' ? 'contested' : 'undrawn';
      const txt = m.status === 'absent' ? 'absent' : m.status === 'contested' ? 'contested' : 'not drawn';
      return { html: `<span class="chip ${cls}" title="${esc(m.reason || '')}">${txt}</span>` };
    }
    if (S.mode === 'action' && S.action) {
      const { joint, dir } = S.action;
      if (!model.dofById.has(joint)) return { html: '<span class="chip none" title="This animal has no such joint in the model">no joint</span>' };
      const roles = drawn.map(mu => E.actionRole(model, mu, joint, dir, S.amount));
      const best = roles.reduce((a, b) => Math.abs(b.rel) > Math.abs(a.rel) ? b : a);
      const cls = best.role === 'shortens' ? 'short' : best.role === 'lengthens' ? 'long' : 'none';
      const txt = best.role === 'none' ? 'no change' : `${best.role} ${pct(best.rel)}`;
      return { html: `<span class="chip ${cls}">${txt}</span>` };
    }
    return { live: true, html: '<span class="chip none">–</span>' };
  }

  function renderTable() {
    const box = $('#compare');
    const gs = groupsPresent();
    const ms = models();
    if (!ms.length) { box.innerHTML = ''; return; }
    const head = ms.map(m => `<th><i>${esc(m.label)}</i></th>`).join('');
    const title = S.mode === 'action' && S.action
      ? `Which muscles ${jointInfo(S.action.joint)[S.action.dir > 0 ? 'pos' : 'neg'].toLowerCase()} the ${jointInfo(S.action.joint).label.toLowerCase()}, from rest`
      : 'Length change of each muscle, live';
    const rows = gs.map(g => {
      const cells = ms.map(m => {
        const c = cellFor(m, g);
        return `<td data-model="${esc(m.id)}" data-group="${esc(g.id)}"${c.live ? ' data-live="1"' : ''}>${c.html}</td>`;
      }).join('');
      return `<tr data-group="${esc(g.id)}" class="${S.sel === g.id ? 'sel' : ''}"><th scope="row">${esc(g.label)}</th>${cells}</tr>`;
    }).join('');
    box.innerHTML = `<h2>${esc(title)}</h2><table class="cmp"><thead><tr><th></th>${head}</tr></thead><tbody>${rows}</tbody></table>`;
    box.querySelectorAll('tbody tr').forEach(tr =>
      tr.addEventListener('click', () => selectGroup(S.sel === tr.dataset.group ? null : tr.dataset.group)));
  }

  /* The live cells: current length change per muscle, refreshed every frame. */
  function updateLiveCells() {
    for (const td of document.querySelectorAll('#compare td[data-live]')) {
      const panel = S.panels.find(p => p.model.id === td.dataset.model);
      if (!panel) continue;
      const ms = panel.mus.filter(m => m.mu.group === td.dataset.group);
      if (!ms.length) continue;
      const best = ms.reduce((a, b) => Math.abs(b.eps) > Math.abs(a.eps) ? b : a);
      const e = best.eps;
      const cls = e < -0.02 ? 'short' : e > 0.02 ? 'long' : 'none';
      td.innerHTML = `<span class="chip ${cls}">${Math.abs(e) < 0.005 ? '0%' : pct(e)}</span>`;
    }
  }

  function renderDetail() {
    const box = $('#detail');
    if (!S.sel) {
      box.innerHTML = '<h2>Muscle detail</h2><p class="hint">Click a muscle in a diagram, a row in the table, or the list on the left to see its attachments, what the source says it does, and what the model derives from the geometry.</p>';
      return;
    }
    const g = groupInfo(S.sel);
    const cards = [];
    for (const model of models()) {
      for (const mu of model.muscles.filter(m => m.group === S.sel)) {
        const drawn = mu.paths && mu.paths.length;
        let badge;
        if (mu.record === null) badge = '<span class="badge park">No muscle record yet — parked in the dataset</span>';
        else if (mu.status === 'absent') badge = '<span class="badge park">Recorded absent</span>';
        else if ((S.scored.get(mu.record) || new Set()).has(model.species)) badge = '<span class="badge ok">Scored for this animal in the dataset</span>';
        else badge = '<span class="badge gap">On the record, not yet scored for this animal</span>';

        const lm = id => (model.lmById.get(id) || {}).label || id;
        let origin = '', ins = '', derived = '';
        if (drawn) {
          const first = mu.paths[0];
          origin = lm(first[0]); ins = lm(first[first.length - 1]);
          const eff = E.effects(model, mu, {}).sort((a, b) => Math.abs(b.slope) - Math.abs(a.slope));
          derived = eff.map(e => {
            const j = jointInfo(e.dof);
            const verb = e.shortensWith > 0 ? j.pos : j.neg;
            const size = Math.abs(e.slope) > 0.25 ? 'strongly' : Math.abs(e.slope) > 0.1 ? 'moderately' : 'slightly';
            return `${esc(j.label)} → <b>${esc(verb.toLowerCase())}</b>, ${size}`;
          }).join('<br>') || 'No joint changes its length.';
        }
        cards.push(`<article class="dcard"><h3>${esc(mu.label)} <i>${esc(model.label)}</i></h3>${badge}
          <dl>
            ${drawn ? `<dt>Origin</dt><dd>${esc(origin)}</dd><dt>Insertion</dt><dd>${esc(ins)}</dd>` : ''}
            <dt>Source says</dt><dd>${esc(mu.actionText)}</dd>
            ${drawn ? `<dt>Shortening it</dt><dd>${derived}</dd>` : `<dt>Not drawn</dt><dd class="reason">${esc(mu.reason)}</dd>`}
            ${mu.note ? `<dt>Note</dt><dd>${esc(mu.note)}</dd>` : ''}
            <dt>Cited</dt><dd>${mu.sources.map(s => esc(shortSource(s))).join('; ')}</dd>
          </dl>
          ${mu.record ? `<a href="index.html#${encodeURIComponent(mu.record)}">Open the record in the muscle lookup →</a>` : ''}</article>`);
      }
    }
    box.innerHTML = `<h2>${esc(g ? g.label : S.sel)}</h2>${cards.join('')}`;
  }

  function renderSlots() {
    const info = regionInfo();
    const avail = info.models;
    const ol = $('#slots');
    ol.innerHTML = '';
    S.slots.forEach((id, i) => {
      const li = document.createElement('li');
      const opts = avail.map(mid => {
        const m = S.models.get(mid);
        const taken = S.slots.includes(mid) && mid !== id;
        return `<option value="${esc(mid)}"${mid === id ? ' selected' : ''}${taken ? ' disabled' : ''}>${esc(m.label)} — ${esc(m.common)}</option>`;
      }).join('');
      li.innerHTML = `<select aria-label="Taxon ${i + 1}">${opts}</select>
        <button title="Remove" aria-label="Remove this taxon"${S.slots.length === 1 ? ' disabled' : ''}>×</button>`;
      $('select', li).addEventListener('change', ev => { S.slots[i] = ev.target.value; rebuild(); });
      $('button', li).addEventListener('click', () => { S.slots.splice(i, 1); rebuild(); });
      ol.append(li);
    });
    const cap = Math.min(S.index.maxTaxa, avail.length);
    $('#add-taxon').disabled = S.slots.length >= cap;
    $('#taxa-count').textContent = `${S.slots.length} of up to ${S.index.maxTaxa}` + (avail.length < S.index.maxTaxa ? ` · ${avail.length} available` : '');
  }

  function jointsPresent() {
    const ids = new Set();
    for (const m of models()) for (const d of m.dofs) ids.add(d.id);
    return S.index.joints.filter(j => j.region === S.region && ids.has(j.id));
  }

  function renderActions() {
    const js = jointsPresent();
    const sel = $('#act-joint');
    const cur = sel.value && js.some(j => j.id === sel.value) ? sel.value : (js[0] && js[0].id);
    sel.innerHTML = js.map(j => {
      const n = models().filter(m => m.dofById.has(j.id)).length;
      return `<option value="${esc(j.id)}"${j.id === cur ? ' selected' : ''}>${esc(j.label)}${n < S.slots.length ? ` (${n} of ${S.slots.length})` : ''}</option>`;
    }).join('');
    const j = js.find(x => x.id === cur);
    const box = $('#act-btns');
    box.innerHTML = '';
    if (!j) return;
    for (const dir of [1, -1]) {
      const b = document.createElement('button');
      b.className = 'ghost';
      b.textContent = dir > 0 ? j.pos : j.neg;
      b.setAttribute('aria-pressed', String(S.mode === 'action' && S.action && S.action.joint === j.id && S.action.dir === dir));
      b.addEventListener('click', () => runAction(j.id, dir));
      box.append(b);
    }
  }

  function renderMuscleList() {
    const ul = $('#mlist');
    ul.innerHTML = '';
    for (const g of groupsPresent()) {
      const n = models().filter(m => m.muscles.some(mu => mu.group === g.id)).length;
      const li = document.createElement('li');
      li.innerHTML = `<button aria-pressed="${S.sel === g.id}"><span>${esc(g.label)}</span><span class="n">${n}/${S.slots.length}</span></button>`;
      $('button', li).addEventListener('click', () => selectGroup(S.sel === g.id ? null : g.id));
      ul.append(li);
    }
    const ms = $('#muscle-select');
    ms.innerHTML = '<option value="">Muscle…</option>' + groupsPresent().map(g =>
      `<option value="${esc(g.id)}"${S.sel === g.id ? ' selected' : ''}>${esc(g.label)}</option>`).join('');
    ms.onchange = () => selectGroup(ms.value || null);
  }

  function renderPoseSliders() {
    const box = $('#pose');
    box.innerHTML = '';
    for (const j of jointsPresent()) {
      const two = models().some(m => m.dofById.has(j.id) && E.uMin(m.dofById.get(j.id)) < 0);
      const lab = document.createElement('label');
      lab.innerHTML = `<span>${esc(j.label)}</span><input type="range" min="${two ? -100 : 0}" max="100" step="1" value="${Math.round((S.pose[j.id] || 0) * 100)}" data-joint="${esc(j.id)}" aria-label="${esc(j.label)}: ${esc(j.neg)} to ${esc(j.pos)}"><output>${Math.round((S.pose[j.id] || 0) * 100)}%</output>`;
      $('input', lab).addEventListener('input', ev => {
        S.pose[j.id] = +ev.target.value / 100;
        $('output', lab).textContent = `${ev.target.value}%`;
        setMode('pose'); frame();
      });
      box.append(lab);
    }
  }
  function syncPoseSliders() {
    for (const inp of document.querySelectorAll('#pose input')) {
      const v = Math.round((S.pose[inp.dataset.joint] || 0) * 100);
      inp.value = v; inp.nextElementSibling.textContent = `${v}%`;
    }
  }

  /* ---------- state changes ---------- */

  function setMode(mode) {
    if (S.mode === mode) return;
    S.mode = mode;
    if (mode === 'pose') { S.playing = false; syncTransport(); }
    renderTable(); renderActions(); renderMuscleList(); writeHash();
  }

  function runAction(joint, dir) {
    S.mode = 'action'; S.action = { joint, dir }; S.sel = null;
    S.t = 0; S.dir = 1; S.playing = true;
    afterModeChange();
  }

  function selectGroup(id) {
    S.sel = id;
    if (id) { S.mode = 'muscle'; S.t = 0; S.dir = 1; S.playing = true; }
    else { S.mode = 'pose'; S.playing = false; }
    afterModeChange();
  }

  function afterModeChange() {
    renderTable(); renderActions(); renderMuscleList(); renderDetail(); syncTransport(); writeHash(); frame();
  }

  function rebuild() {
    // the set of animals changed: panels, controls and anything that names them
    S.runCache.clear();
    if (S.sel && !models().some(m => m.muscles.some(mu => mu.group === S.sel))) { S.sel = null; if (S.mode === 'muscle') S.mode = 'pose'; }
    if (S.mode === 'action' && !models().some(m => m.dofById.has(S.action.joint))) S.mode = 'pose';
    const box = $('#panels');
    box.dataset.n = String(S.slots.length);
    box.innerHTML = '';
    S.panels = models().map((m, i) => makePanel(m, i));
    S.panels.forEach(p => box.append(p.fig));
    renderSlots(); renderActions(); renderMuscleList(); renderPoseSliders();
    renderTable(); renderDetail(); syncTransport(); writeHash(); frame();
  }

  function frame() {
    for (const p of S.panels) updatePanel(p);
    updateLiveCells();
    $('#playhead').value = Math.round(S.t * 1000);
    $('#status').innerHTML = statusText();
  }

  function statusText() {
    if (S.mode === 'action' && S.action) {
      const j = jointInfo(S.action.joint);
      return `<b>${esc(j[S.action.dir > 0 ? 'pos' : 'neg'])} — ${esc(j.label.toLowerCase())}</b>, ${Math.round(S.amount * 100)}% of the range. Muscles are coloured by whether they shorten or stretch.`;
    }
    if (S.mode === 'muscle' && S.sel) {
      const g = groupInfo(S.sel);
      const n = models().filter(m => groupMuscles(m).length).length;
      return `<b>${esc(g ? g.label : S.sel)}</b> contracting alone${S.startFrom === 'stretched' ? ' from a stretched start' : ' from the current pose'}, in ${n} of ${S.slots.length} animals. Nothing opposes it.`;
    }
    return 'Free pose. Drag a ringed point on a diagram, move a slider below, or pick an action or a muscle.';
  }

  /* ---------- transport ---------- */

  function syncTransport() {
    const b = $('#play');
    b.textContent = S.playing ? '❚❚ Pause' : '▶ Play';
    b.setAttribute('aria-pressed', String(S.playing));
    $('#playhead').disabled = S.mode === 'pose';
  }

  let last = 0;
  function tick(now) {
    if (S.playing) {
      const dt = Math.min(0.05, (now - last) / 1000);
      S.t += S.dir * dt / (S.mode === 'muscle' ? 2.2 : 1.6);
      if (S.t >= 1) { S.t = 1; if (S.loop) S.dir = -1; else { S.playing = false; syncTransport(); } }
      else if (S.t <= 0) { S.t = 0; if (S.loop) S.dir = 1; else { S.playing = false; syncTransport(); } }
      frame();
    }
    last = now;
    requestAnimationFrame(tick);
  }

  /* ---------- hash ---------- */

  function writeHash() {
    const p = new URLSearchParams();
    p.set('r', S.region);
    if (!S.lite) p.set('v', 'full');
    p.set('t', S.slots.map(id => id.slice(S.region.length + 1)).join(','));
    if (S.mode === 'action' && S.action) p.set('a', `${S.action.joint}:${S.action.dir}`);
    if (S.sel) p.set('m', S.sel);
    history.replaceState(null, '', '#' + p.toString());
  }
  function readHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    return { v: p.get('v'), r: p.get('r'), t: (p.get('t') || '').split(',').filter(Boolean), a: p.get('a'), m: p.get('m') };
  }

  /* ---------- boot ---------- */

  async function loadRegion(id) {
    const info = S.index.regions.find(r => r.id === id);
    S.region = id;
    await Promise.all(info.models.filter(m => !S.models.has(m)).map(async m => {
      S.models.set(m, E.build(await fetchJSON(`data/sim/${m}.json`)));
    }));
    for (const f of info.records || []) {
      const d = await fetchJSON(`data/${f}`);
      for (const mu of d.muscles) {
        for (const o of mu.occurrences || []) {
          if (o.species && o.present !== 'no') {
            if (!S.scored.has(mu.id)) S.scored.set(mu.id, new Set());
            S.scored.get(mu.id).add(o.species);
          }
        }
      }
    }
  }

  async function boot() {
    const [index, sources] = await Promise.all([fetchJSON('data/sim/index.json'), fetchJSON('data/sources.json')]);
    S.index = index;
    for (const s of sources.sources) S.sources.set(s.key, s.short || s.key);

    const h = readHash();
    S.lite = h.v !== 'full';
    document.body.classList.toggle('lite', S.lite);
    const tog = $('#view-toggle');
    const syncToggle = () => { tog.textContent = S.lite ? 'Full version' : 'Text-light version'; };
    syncToggle();
    tog.addEventListener('click', ev => {
      ev.preventDefault();
      S.lite = !S.lite;
      document.body.classList.toggle('lite', S.lite);
      syncToggle(); writeHash();
    });
    const startRegion = index.regions.find(r => r.id === h.r && r.status === 'available') ? h.r : 'cranial';
    await loadRegion(startRegion);

    const info = regionInfo();
    const fromHash = h.t.map(sp => `${S.region}-${sp}`).filter(id => info.models.includes(id));
    S.slots = (fromHash.length ? fromHash : info.models).slice(0, index.maxTaxa);

    const sel = $('#region');
    sel.innerHTML = index.regions.map(r =>
      `<option value="${esc(r.id)}"${r.id === S.region ? ' selected' : ''}${r.status !== 'available' ? ' disabled' : ''}>${esc(r.label)}${r.status !== 'available' ? ' (planned)' : ''}</option>`).join('');
    sel.addEventListener('change', async ev => {
      await loadRegion(ev.target.value);
      S.slots = regionInfo().models.slice(0, S.index.maxTaxa);
      S.pose = {}; S.sel = null; S.mode = 'pose'; S.playing = false;
      rebuild();
    });

    $('#add-taxon').addEventListener('click', () => {
      const next = regionInfo().models.find(m => !S.slots.includes(m));
      if (next && S.slots.length < S.index.maxTaxa) { S.slots.push(next); rebuild(); }
    });
    $('#act-joint').addEventListener('change', renderActions);
    $('#act-amount').addEventListener('input', ev => {
      S.amount = +ev.target.value / 100;
      $('#act-amount-out').textContent = `${ev.target.value}%`;
      if (S.mode === 'action') { renderTable(); frame(); }
    });
    document.querySelectorAll('input[name="startfrom"]').forEach(r => r.addEventListener('change', ev => {
      S.startFrom = ev.target.value; S.runCache.clear(); if (S.mode === 'muscle') { S.t = 0; S.playing = true; syncTransport(); frame(); }
    }));
    $('#opt-labels').addEventListener('change', ev => { S.labels = ev.target.checked; frame(); });
    $('#opt-bones').addEventListener('change', ev => { S.bones = ev.target.checked; frame(); });
    $('#opt-strain').addEventListener('change', ev => { S.strain = ev.target.checked; frame(); });

    $('#play').addEventListener('click', () => {
      if (S.mode === 'pose') return;
      if (!S.playing && S.t >= 1) { S.t = 0; S.dir = 1; }
      S.playing = !S.playing; syncTransport();
    });
    $('#reset').addEventListener('click', () => {
      S.pose = {}; S.sel = null; S.mode = 'pose'; S.action = null; S.t = 0; S.playing = false;
      syncPoseSliders(); afterModeChange();
    });
    $('#playhead').addEventListener('input', ev => { S.t = +ev.target.value / 1000; S.playing = false; syncTransport(); frame(); });
    $('#loop').addEventListener('change', ev => { S.loop = ev.target.checked; });

    $('#btn-theme').addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : cur === 'light' ? '' : 'dark';
      if (next) document.documentElement.setAttribute('data-theme', next);
      else document.documentElement.removeAttribute('data-theme');
      S.colors = null; frame();
    });
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { S.colors = null; frame(); });

    rebuild();
    if (h.m) selectGroup(h.m);
    else if (h.a) {
      const [joint, dir] = h.a.split(':');
      if (jointInfo(joint)) runAction(joint, +dir === -1 ? -1 : 1);
    }
    requestAnimationFrame(tick);
    window.__sim = S;
  }

  boot().catch(err => {
    $('#simmain').innerHTML = `<div class="empty-sim">The simulator could not load its data: ${esc(err.message)}</div>`;
    console.error(err);
  });
})();
