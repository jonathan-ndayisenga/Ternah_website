/* =========================================================
   TERNAH — shared site script
   ========================================================= */
document.documentElement.classList.remove('no-js');

/* ---- header border once scrolled ---- */
const hdr = document.getElementById('hdr');
function updateHeader(){ if(hdr) hdr.classList.toggle('scrolled', window.scrollY > 8); }
window.addEventListener('scroll', updateHeader, {passive:true});
updateHeader();

/* ---- mobile menu ---- */
const burger = document.getElementById('burger');
const navlinks = document.getElementById('navlinks');
if(burger && navlinks){
  const setOpen = open => {
    navlinks.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
  };
  burger.addEventListener('click', ()=> setOpen(!navlinks.classList.contains('open')));
  navlinks.querySelectorAll('a').forEach(a=> a.addEventListener('click', ()=> setOpen(false)));
  document.addEventListener('click', e=>{
    if(!burger.contains(e.target) && !navlinks.contains(e.target)) setOpen(false);
  });
  document.addEventListener('keydown', e=>{ if(e.key === 'Escape') setOpen(false); });
}

/* ---- mark active nav link (by data-page on <body>) ---- */
(function(){
  const page = document.body.dataset.page;
  document.querySelectorAll('.navlinks a[data-nav]').forEach(a=>{
    a.classList.toggle('active', a.dataset.nav === page);
  });
})();

/* ---- scroll reveal ---- */
(function(){
  const els = document.querySelectorAll('.reveal');
  if(!els.length) return;
  if(!('IntersectionObserver' in window)){ els.forEach(el=>el.classList.add('in')); return; }
  const io = new IntersectionObserver(entries=>{
    entries.forEach(en=>{ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
  },{threshold:.12, rootMargin:'0px 0px -8% 0px'});
  els.forEach(el=>io.observe(el));
})();

/* ---- contact form: inline validation, honeypot, endpoint or email fallback ---- */
(function(){
  const form = document.getElementById('contactForm');
  if(!form) return;
  const out = document.getElementById('formMsg');
  const btn = document.getElementById('sendBtn');

  // "Book a demo" links arrive as contact.html?product=<key>
  const product = new URLSearchParams(location.search).get('product');
  if(product){
    form.product.value = product;
    form.need.value = 'demo';
    const names = JSON.parse(form.dataset.products || '{}');
    const label = names[product] || product.replace(/-/g,' ').replace(/\b\w/g, c=>c.toUpperCase());
    if(!form.message.value) form.message.value = `I'd like a demo of ${label}.`;
  }

  const rules = {
    name:    v => v ? '' : 'Please enter your name.',
    email:   v => !v ? 'Please enter your email.' : (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'That email address looks incomplete.'),
    need:    v => v ? '' : 'Please choose what you need.',
    message: v => v ? '' : 'Please tell us a little about what you need.',
  };
  function check(name){
    const el = form.elements[name];
    const msg = rules[name](el.value.trim());
    const wrap = el.closest('.field');
    wrap.classList.toggle('invalid', !!msg);
    el.setAttribute('aria-invalid', msg ? 'true' : 'false');
    document.getElementById(name + '_err').textContent = msg;
    return !msg;
  }
  Object.keys(rules).forEach(n=>{
    const el = form.elements[n];
    el.addEventListener('blur', ()=> { if(el.value.trim()) check(n); });
    el.addEventListener(el.tagName === 'SELECT' ? 'change' : 'input', ()=> { if(el.closest('.field').classList.contains('invalid')) check(n); });
  });

  function show(text, kind){ out.className = kind; out.textContent = text; }

  form.addEventListener('submit', async e=>{
    e.preventDefault();
    const bad = Object.keys(rules).filter(n=> !check(n));
    if(bad.length){ form.elements[bad[0]].focus(); show('Please fix the highlighted fields.', 'bad'); return; }
    if(form.website.value){ show('Thanks — your message has been sent.', 'ok'); form.reset(); return; } // bot

    const v = n => (form.elements[n]?.value || '').trim(); // the home page form has no phone or organisation
    const endpoint = form.getAttribute('action');
    if(endpoint){
      btn.disabled = true;
      show('Sending…', '');
      try{
        const res = await fetch(endpoint, {method:'POST', body:new FormData(form), headers:{'Accept':'application/json'}});
        if(!res.ok) throw new Error(res.status);
        form.reset();
        show(`Thanks, ${v('name') || 'we have it'}. Your message has been sent and we'll reply within one working day.`, 'ok');
      }catch(err){
        show(`Sorry, that didn't go through. Please email ${form.dataset.email} or message us on WhatsApp.`, 'bad');
      }finally{ btn.disabled = false; }
      return;
    }
    // No endpoint configured: open the visitor's email app pre-filled.
    const subject = encodeURIComponent(`New project enquiry from ${v('name')}`);
    const body = encodeURIComponent(
      `Name: ${v('name')}\nEmail: ${v('email')}\nPhone: ${v('phone') || '-'}\nOrganisation: ${v('organisation') || '-'}` +
      `\nNeeds: ${form.need.selectedOptions[0].text}` +
      `${form.product.value ? `\nProduct: ${form.product.value}` : ''}\n\n${v('message')}`);
    show('Your email app should open with the message ready to send. If it does not, email us directly at ' + form.dataset.email + '.', 'ok');
    window.location.href = `mailto:${form.dataset.email}?subject=${subject}&body=${body}`;
  });
})();

/* ---- articles used to open as pop-ups at insights.html#<slug>; send old links to the article page ---- */
(function(){
  const slug = location.hash.slice(1);
  const card = slug && document.querySelector(`[data-slug="${CSS.escape(slug)}"]`);
  if(card) location.replace(card.getAttribute('href'));
})();

/* ---- solutions filter pills ---- */
(function(){
  const bar = document.getElementById('solFilter');
  const grid = document.getElementById('solGrid');
  if(!bar || !grid) return;
  const pills = bar.querySelectorAll('.pill');
  const cards = grid.querySelectorAll('.card[data-filter]');
  pills.forEach(pill=>{
    pill.addEventListener('click', ()=>{
      pills.forEach(p=>{ p.classList.toggle('active', p === pill); p.setAttribute('aria-pressed', String(p === pill)); });
      const filter = pill.dataset.filter;
      cards.forEach(card=>{
        const match = filter === 'all' || card.dataset.filter === filter;
        card.style.transition = 'opacity .3s, transform .3s';
        card.style.opacity = match ? '1' : '0.3';
        card.style.pointerEvents = match ? '' : 'none';
      });
      if(filter !== 'all'){
        const target = grid.querySelector(`.card[data-filter="${filter}"]`);
        if(target){
          target.classList.remove('card-highlight'); void target.offsetWidth; target.classList.add('card-highlight');
          target.scrollIntoView({behavior:'smooth', block:'center'});
        }
      }
    });
  });
})();

/* ---- hero product switcher: tabs, arrow keys, gentle auto-advance ---- */
(function(){
  const root = document.getElementById('showcase');
  if(!root) return;
  const tabs = [...root.querySelectorAll('[role=tab]')];
  const panels = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));
  let current = 0, auto = !matchMedia('(prefers-reduced-motion: reduce)').matches, paused = false, timer;

  function select(i, focus){
    current = (i + tabs.length) % tabs.length;
    tabs.forEach((t, k) => {
      const on = k === current;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      panels[k].hidden = !on;
    });
    if(focus) tabs[current].focus();
    schedule();
  }
  function schedule(){
    clearTimeout(timer);
    if(auto && !paused) timer = setTimeout(() => select(current + 1), 9000);  // slides carry a brief, so give time to read it
  }
  function stop(){ auto = false; clearTimeout(timer); }

  tabs.forEach((t, i) => t.addEventListener('click', () => { stop(); select(i); }));
  root.querySelector('[role=tablist]').addEventListener('keydown', e => {
    const moves = {ArrowRight: current + 1, ArrowLeft: current - 1, Home: 0, End: tabs.length - 1};
    if(e.key in moves){ e.preventDefault(); stop(); select(moves[e.key], true); }
  });
  root.addEventListener('mouseenter', () => { paused = true; clearTimeout(timer); });
  root.addEventListener('mouseleave', () => { paused = false; schedule(); });
  root.addEventListener('focusin', () => { paused = true; clearTimeout(timer); });
  root.addEventListener('focusout', e => { if(!root.contains(e.relatedTarget)){ paused = false; schedule(); } });
  schedule();
})();
