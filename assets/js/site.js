/* موثّق — behaviour for the الحرز world. No dependencies; every feature degrades to plain HTML. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const REL = document.body.dataset.rel || '';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch {} },
    sget(k) { try { return sessionStorage.getItem(k); } catch { return null; } },
    sset(k, v) { try { sessionStorage.setItem(k, v); } catch {} },
  };
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const norm = (s) => String(s ?? '').toLowerCase()
    .replace(/[ً-ٰٟـ]/g, '').replace(/[أإآٱ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه')
    .replace(/ؤ/g, 'و').replace(/ئ/g, 'ي').replace(/[()«»"'،,.:؛]/g, ' ').replace(/\s+/g, ' ').trim();

  /* ---------- toasts ---------- */
  function toast(msg, state = 'whole') {
    const box = $('#toasts'); if (!box) return;
    const t = document.createElement('div');
    t.className = 'toast'; t.setAttribute('role', 'status');
    t.innerHTML = `<svg class="seal" viewBox="0 0 40 40" aria-hidden="true"><use href="#s-${state}"/></svg><span>${msg}</span>`;
    box.append(t);
    setTimeout(() => { t.style.transition = 'opacity .3s'; t.style.opacity = '0'; setTimeout(() => t.remove(), 320); }, 4200);
  }
  window.mwToast = toast;

  /* ---------- headline lines: home.js opens them after the intro; never leave them hidden ---------- */
  const lines = $('[data-lines]');
  if (lines) setTimeout(() => lines.classList.add('is-in'), 4200);
  if (lines && !document.querySelector('script[src*="home.js"]')) lines.classList.add('is-in');

  /* ---------- smooth scrolling on fine pointers ---------- */
  if (window.Lenis && !reduce && matchMedia('(pointer: fine)').matches) {
    const lenis = new Lenis({ duration: 1.05, easing: (t) => 1 - Math.pow(1 - t, 3.2), anchors: { offset: -88 } });
    window.mwLenis = lenis;
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    if (window.ScrollTrigger) lenis.on('scroll', () => ScrollTrigger.update());
  }

  /* ---------- prototype note ---------- */
  const proto = $('#proto');
  if (proto && store.get('mw-proto') === 'hidden') proto.hidden = true;
  $$('[data-dismiss="proto"]').forEach((b) => b.addEventListener('click', () => { proto.hidden = true; store.set('mw-proto', 'hidden'); }));

  /* ---------- masthead ---------- */
  const mast = $('#mast');
  const onScroll = () => mast && mast.classList.toggle('is-stuck', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const menuBtn = $('.menu-btn'), nav = $('#nav');
  if (menuBtn && nav) {
    const setOpen = (open) => { nav.classList.toggle('is-open', open); menuBtn.setAttribute('aria-expanded', String(open)); };
    menuBtn.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); menuBtn.focus(); } });
    document.addEventListener('click', (e) => { if (nav.classList.contains('is-open') && !nav.contains(e.target) && !menuBtn.contains(e.target)) setOpen(false); });
  }

  /* ---------- search ---------- */
  const INDEX = (window.MW_INDEX || []).map((r) => ({ ...r, _n: norm([r.title, r.sub, r.id, r.k].join(' ')) }));
  const TYPES = { person: 'ملفات الأشخاص', incident: 'الوقائع', evidence: 'الأدلة', report: 'التقارير والوثائق', rule: 'القواعد القانونية', page: 'صفحات' };
  function search(q, limit = 40) {
    const n = norm(q); if (!n) return [];
    const words = n.split(' ');
    const scored = [];
    for (const r of INDEX) {
      if (!words.every((w) => r._n.includes(w))) continue;
      let s = 0;
      const t = norm(r.title);
      if (t.startsWith(n)) s += 6; else if (t.includes(n)) s += 3;
      if (norm(r.id) === n) s += 10;
      s += { person: 2, incident: 1.5, rule: 1.2, report: 1, evidence: .6, page: .4 }[r.type] || 0;
      scored.push([s, r]);
    }
    return scored.sort((a, b) => b[0] - a[0]).slice(0, limit).map((x) => x[1]);
  }
  window.mwSearch = search;

  $$('[data-find]').forEach((form) => {
    const input = $('input', form), list = $('.find-list', form);
    let opts = [], active = -1;
    const close = () => { list.hidden = true; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); active = -1; };
    const render = () => {
      const q = input.value.trim();
      if (!q) { close(); return; }
      const res = search(q, 9);
      if (!res.length) {
        list.innerHTML = `<div class="find-empty">لا توجد نتائج لـ«${esc(q)}». جرب اسما أو رقم ملف مثل <span class="mono">P-0001</span> أو مادة مثل «المادة 8».</div>`;
      } else {
        const groups = {};
        res.forEach((r) => (groups[r.type] = groups[r.type] || []).push(r));
        let i = 0;
        list.innerHTML = Object.entries(groups).map(([t, rs]) => `<div class="find-group" role="presentation">${TYPES[t] || ''}</div>` +
          rs.map((r) => `<a class="find-opt" role="option" id="${form.dataset.find}-o${i++}" href="${REL}${r.url}" aria-selected="false"><b>${esc(r.title)}</b><small>${esc(r.sub || '')}</small><span class="mono">${esc(r.id)}</span></a>`).join('')).join('') +
          `<a class="find-all" href="${REL}search.html?q=${encodeURIComponent(q)}">كل النتائج لـ«${esc(q)}»</a>`;
      }
      opts = $$('.find-opt', list); active = -1;
      list.hidden = false; input.setAttribute('aria-expanded', 'true');
    };
    const move = (d) => {
      if (!opts.length) return;
      if (active >= 0) opts[active].setAttribute('aria-selected', 'false');
      active = (active + d + opts.length) % opts.length;
      opts[active].setAttribute('aria-selected', 'true');
      opts[active].scrollIntoView({ block: 'nearest' });
      input.setAttribute('aria-activedescendant', opts[active].id);
    };
    input.addEventListener('input', render);
    input.addEventListener('focus', () => input.value && render());
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); if (list.hidden) render(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); location.href = opts[active].href; }
      else if (e.key === 'Escape') { close(); }
    });
    document.addEventListener('click', (e) => { if (!form.contains(e.target)) close(); });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName)) {
      const i = $$('[data-find] input').find((x) => x.offsetParent); if (i) { e.preventDefault(); i.focus(); }
    }
  });

  /* full results page */
  const results = $('#results');
  if (results) {
    const params = new URLSearchParams(location.search);
    const q = params.get('q') || '';
    const box = $('#q-page'); if (box) box.value = q;
    const types = $$('#q-types input');
    const start = $('#search-start');
    const IDX = window.MW_INDEX || [];
    /* totals per type come from the index itself, so the panel always matches what search can find */
    types.forEach((inp) => { inp.dataset.total = inp.value ? IDX.filter((r) => r.type === inp.value).length : IDX.length; });
    const totalEl = $('.panel .stamp-total b'); if (totalEl) totalEl.textContent = IDX.length;
    const draw = () => {
      const val = box ? box.value.trim() : q;
      const type = ($('#q-types input:checked') || {}).value || '';
      const all = val ? search(val, 400) : [];
      types.forEach((inp) => {
        const n = val ? all.filter((r) => !inp.value || r.type === inp.value).length : +inp.dataset.total;
        const opt = inp.closest('.facet-opt'); $('.facet-n', opt).textContent = n;
        opt.classList.toggle('is-zero', n === 0 && !inp.checked);
      });
      const res = type ? all.filter((r) => r.type === type) : all;
      $('#results-count').innerHTML = val ? `<b>${res.length}</b> نتيجة لـ«${esc(val)}»` : '';
      results.innerHTML = res.slice(0, 200).map((r) => `<li><a class="row" href="${REL}${r.url}"><span class="row-thumb is-blank" aria-hidden="true"><svg class="seal" viewBox="0 0 40 40"><use href="#s-${r.seal || 'whole'}"/></svg></span><span class="row-body"><span class="tag-kind">${TYPES[r.type] || ''}</span><h3>${esc(r.title)}</h3><span class="row-meta">${esc(r.sub || '')}</span></span><span class="row-end"><span class="mono">${esc(r.id)}</span></span></a></li>`).join('');
      results.hidden = !res.length;
      if (start) start.hidden = !!val;
      if (box && val !== q) history.replaceState(null, '', val ? '?q=' + encodeURIComponent(val) : location.pathname);
    };
    if (box) box.addEventListener('input', draw);
    types.forEach((inp) => inp.addEventListener('change', draw));
    $$('[data-try]').forEach((b) => b.addEventListener('click', () => { box.value = b.dataset.try; draw(); box.focus(); }));
    draw();
  }

  /* ---------- list filters ---------- */
  /* on phones and tablets the filters fold under the search; the fold shows how many are set */
  const narrow = matchMedia('(max-width: 1024px)');
  $$('[data-filt]').forEach((d) => {
    const fit = () => { d.open = !narrow.matches; };
    fit(); narrow.addEventListener('change', fit);
    const form = d.closest('form'), n = $('[data-filt-n]', d);
    const count = () => {
      const k = $$('select', d).filter((s) => s.value).length + $$('fieldset input:checked', d).filter((i) => i.value).length;
      n.textContent = k; n.hidden = !k;
    };
    form.addEventListener('change', count); form.addEventListener('reset', () => setTimeout(count));
  });

  $$('[data-filter]').forEach((form) => {
    const list = document.getElementById(form.dataset.filter);
    const count = document.getElementById(form.dataset.count);
    const items = $$(':scope > li', list);
    const empty = document.getElementById(form.dataset.empty);
    const has = (li, key, v) => !v || (li.dataset[key] || '').split(' ').includes(v);
    const picked = (f) => ($('input:checked', f) || {}).value || '';
    const apply = () => {
      const q = norm(($('[data-q]', form) || {}).value || '');
      const sels = $$('select[data-key]', form);
      const facets = $$('fieldset[data-key]', form);
      /* a record passes every filter except, when asked, one facet: that facet's counts are then "if you picked this" */
      const passes = (li, skip) => (!q || norm(li.dataset.text || li.textContent).includes(q)) &&
        sels.every((s) => has(li, s.dataset.key, s.value)) && facets.every((f) => f === skip || has(li, f.dataset.key, picked(f)));
      let shown = 0;
      items.forEach((li) => { const ok = passes(li); li.hidden = !ok; if (ok) shown++; });
      facets.forEach((f) => $$('input', f).forEach((inp) => {
        const n = items.filter((li) => passes(li, f) && has(li, f.dataset.key, inp.value)).length;
        const opt = inp.closest('.facet-opt');
        $('.facet-n', opt).textContent = n;
        opt.classList.toggle('is-zero', n === 0 && !inp.checked);
      }));
      if (count) count.innerHTML = `يظهر <b>${shown}</b> من ${items.length}`;
      if (empty) empty.hidden = shown !== 0;
    };
    form.addEventListener('input', apply); form.addEventListener('change', apply);
    form.addEventListener('reset', () => setTimeout(apply));
    form.addEventListener('submit', (e) => e.preventDefault());
    apply();
  });

  /* ---------- exhibit opening ---------- */
  $$('[data-open]').forEach((el) => {
    const key = 'mw-open:' + location.pathname;
    if (reduce || store.sget(key)) return;
    store.sset(key, '1');
    el.classList.add('is-opening');
  });

  /* ---------- home: switch the exhibit on the table ---------- */
  $$('[data-exhibits]').forEach((box) => {
    const tabs = $$('[role="tab"]', box), panels = $$('[role="tabpanel"]', box);
    const show = (i, focus) => {
      tabs.forEach((t, k) => { t.setAttribute('aria-selected', String(k === i)); t.tabIndex = k === i ? 0 : -1; });
      panels.forEach((p, k) => {
        const on = k === i; p.hidden = !on;
        if (on && !reduce) { p.classList.remove('is-opening'); void p.offsetWidth; p.classList.add('is-opening'); }
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => show(i));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowLeft: 1, ArrowRight: -1, Home: -99, End: 99 }[e.key];
        if (d === undefined) return;
        e.preventDefault();
        const cur = tabs.findIndex((x) => x.getAttribute('aria-selected') === 'true');
        show(d === -99 ? 0 : d === 99 ? tabs.length - 1 : (cur + d + tabs.length) % tabs.length, true);
      });
    });
  });

  /* ---------- contents: mark the section being read ---------- */
  const tocLinks = $$('.toc a');
  if (tocLinks.length) {
    const map = new Map(tocLinks.map((a) => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { tocLinks.forEach((a) => a.classList.remove('is-here')); map.get(e.target.id)?.classList.add('is-here'); }
    }), { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((_, id) => { const h = document.getElementById(id); h && io.observe(h); });
  }

  /* ---------- copy ---------- */
  $$('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
    const text = b.dataset.copy === 'url' ? location.href : (document.getElementById(b.dataset.copy) || {}).textContent || b.dataset.copy;
    try { await navigator.clipboard.writeText(text.trim()); toast(b.dataset.done || 'نسخ النص.'); }
    catch { toast('تعذر النسخ من المتصفح؛ حدد النص وانسخه يدويا.', 'crack'); }
  }));

  /* ---------- integrity check: hash a file locally, compare with the recorded fingerprint ---------- */
  $$('[data-verify]').forEach((box) => {
    const want = (box.dataset.verify || '').toLowerCase();
    const input = $('input[type=file]', box), out = $('[data-verify-out]', box), sealEl = $('[data-verify-seal] use', box);
    const zone = $('.drop', box);
    const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
    async function check(file) {
      if (!file) return;
      if (!(window.crypto && crypto.subtle)) { out.innerHTML = 'متصفحك لا يتيح حساب البصمة هنا. افتح الصفحة عبر <span class="mono">https</span>.'; return; }
      out.textContent = 'تحسب البصمة على جهازك…';
      const got = hex(await crypto.subtle.digest('SHA-256', await file.arrayBuffer()));
      const ok = got === want;
      box.classList.remove('is-ok', 'is-bad'); void box.offsetWidth;
      box.classList.add(ok ? 'is-ok' : 'is-bad');
      if (sealEl) sealEl.setAttribute('href', ok ? '#s-whole' : '#s-crack');
      out.innerHTML = ok
        ? `<b>الختم سليم.</b> بصمة «${esc(file.name)}» تطابق البصمة المسجلة في هذا الحرز.<span class="mono hash">${got}</span>`
        : `<b>الختم مكسور.</b> بصمة الملف لا تطابق البصمة المسجلة؛ الملف ليس النسخة المحفوظة نفسها أو عدل بعد حفظها.<span class="mono hash">${got}</span>`;
      toast(ok ? 'تطابقت البصمة: الختم سليم.' : 'لم تتطابق البصمة: الختم مكسور.', ok ? 'whole' : 'crack');
    }
    input.addEventListener('change', () => check(input.files[0]));
    if (zone) {
      ['dragenter', 'dragover'].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add('is-over'); }));
      ['dragleave', 'drop'].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove('is-over'); }));
      zone.addEventListener('drop', (e) => check(e.dataTransfer.files[0]));
    }
  });

  /* ---------- forms (nothing leaves the browser) ---------- */
  function validate(scope) {
    let first = null;
    $$('.field', scope).forEach((f) => {
      const el = $('input, select, textarea', f); if (!el || el.closest('[hidden]')) return;
      let bad = false;
      if (el.type === 'checkbox') bad = el.required && !el.checked;
      else if (el.type === 'radio') bad = el.required && !$$(`input[name="${el.name}"]`, scope).some((r) => r.checked);
      else bad = !el.checkValidity();
      const group = f.dataset.group ? $$('input', f).every((c) => !c.checked) : false;
      bad = bad || group;
      f.classList.toggle('is-invalid', bad);
      el.setAttribute('aria-invalid', String(bad));
      if (bad && !first) first = el;
    });
    if (first) { first.focus(); first.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' }); }
    return !first;
  }
  const MONTHS = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'];
  const ref = () => 'MW-' + new Date().getFullYear() + '-' + Math.random().toString(36).slice(2, 7).toUpperCase();

  $$('[data-wizard]').forEach((form) => {
    const steps = $$('[data-step]', form), bar = $$('[data-progress] li', form.parentElement);
    let i = 0;
    const go = (n) => {
      i = n; steps.forEach((s, k) => (s.hidden = k !== i));
      bar.forEach((b, k) => { b.classList.toggle('is-tied', k < i); b.classList.toggle('is-now', k === i); b.querySelector('span')?.setAttribute('aria-current', k === i ? 'step' : 'false'); });
      const h = $('h2, legend', steps[i]); if (h) { h.tabIndex = -1; h.focus({ preventScroll: true }); }
      form.parentElement.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
      if (steps[i].dataset.step === 'review') {
        const fd = new FormData(form), lines = [];
        $$('[data-review]', form).forEach((el) => {
          let v = el.type === 'checkbox' ? (el.checked ? 'نعم' : '—') : (el.tagName === 'SELECT' ? el.selectedOptions[0]?.textContent : fd.getAll(el.name).join('، '));
          if (el.type === 'date' && el.value) { const [y, m, d] = el.value.split('-'); v = `${+d} ${MONTHS[+m - 1]} ${y}`; }
          if (!lines.find((l) => l[0] === el.dataset.review)) lines.push([el.dataset.review, v || '—']);
        });
        $('[data-review-out]', form).innerHTML = lines.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('');
      }
    };
    $$('[data-next]', form).forEach((b) => b.addEventListener('click', () => { if (validate(steps[i])) go(i + 1); }));
    $$('[data-back]', form).forEach((b) => b.addEventListener('click', () => go(i - 1)));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!validate(steps[i])) return;
      const done = document.getElementById(form.dataset.wizard);
      $('[data-ref]', done).textContent = ref();
      form.hidden = true; done.hidden = false;
      const p = form.parentElement.querySelector('[data-progress]'); if (p) p.hidden = true;
      done.classList.add('is-opening'); done.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
      $('h2', done).tabIndex = -1; $('h2', done).focus({ preventScroll: true });
    });
    go(0);
  });

  $$('[data-simple-form]').forEach((form) => form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!validate(form)) return;
    const out = document.getElementById(form.dataset.simpleForm);
    out.hidden = false; const r = $('[data-ref]', out); if (r) r.textContent = ref();
    out.focus?.(); toast(form.dataset.done || 'سجل الطلب في هذا المتصفح فقط.');
    form.reset();
  }));

  /* file list for uploads (local only) */
  $$('[data-files]').forEach((input) => {
    const list = document.getElementById(input.dataset.files);
    const ok = ['image/jpeg', 'image/png', 'application/pdf', 'video/mp4', 'video/webm'];
    input.addEventListener('change', () => {
      list.innerHTML = [...input.files].slice(0, 5).map((f) => {
        const good = ok.includes(f.type) && f.size <= 25 * 1048576;
        return `<li class="${good ? '' : 'is-bad'}"><span>${esc(f.name)}</span><span class="mono">${(f.size / 1048576).toFixed(1)} MB</span>${good ? '' : '<b>نوع أو حجم غير مقبول</b>'}</li>`;
      }).join('');
    });
  });
  const contactRadios = $$('input[name="contact"]');
  contactRadios.forEach((r) => r.addEventListener('change', () => {
    const f = $('#contact-field'); if (f) f.hidden = $('input[name="contact"]:checked').value !== 'yes';
  }));

  /* identity: replay the motion demos */
  $$('[data-replay]').forEach((b) => b.addEventListener('click', () => {
    const d = $(`[data-demo="${b.dataset.replay}"]`); if (!d) return;
    if (b.dataset.replay === 'cord') { d.classList.toggle('is-taut'); return; }
    d.classList.remove('is-play'); void d.offsetWidth; d.classList.add('is-play');
  }));

  /* donate (gateway inactive) */
  $$('[data-donate]').forEach((form) => {
    const custom = $('#d-custom', form), btn = $('[data-donate-btn]', form);
    const sync = () => {
      const pick = $('input[name="amount"]:checked', form);
      const v = pick && pick.value !== 'other' ? pick.value : (custom.value || '');
      custom.closest('.field').hidden = !(pick && pick.value === 'other');
      const freq = $('input[name="freq"]:checked', form)?.value === 'monthly' ? ' شهريا' : '';
      btn.textContent = v ? `متابعة التبرع: ${v} دولار${freq}` : 'متابعة التبرع';
    };
    form.addEventListener('change', sync); custom.addEventListener('input', sync); sync();
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const out = document.getElementById(form.dataset.donate); out.hidden = false; out.focus?.();
      toast('بوابة الدفع غير مفعلة في هذا النموذج؛ لم يحصل أي مبلغ.', 'tied');
    });
  });
})();
