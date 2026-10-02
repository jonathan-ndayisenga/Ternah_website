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
    const label = product.replace(/-/g,' ').replace(/\b\w/g, c=>c.toUpperCase());
    if(!form.message.value) form.message.value = `I'd like a demo of ${label}.`;
  }

  const rules = {
    name:    v => v ? '' : 'Please enter your name.',
    email:   v => !v ? 'Please enter your email.' : (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'That email address looks incomplete.'),
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
    el.addEventListener('input', ()=> { if(el.closest('.field').classList.contains('invalid')) check(n); });
  });

  function show(text, kind){ out.className = kind; out.textContent = text; }

  form.addEventListener('submit', async e=>{
    e.preventDefault();
    const bad = Object.keys(rules).filter(n=> !check(n));
    if(bad.length){ form.elements[bad[0]].focus(); show('Please fix the highlighted fields.', 'bad'); return; }
    if(form.website.value){ show('Thanks — your message has been sent.', 'ok'); form.reset(); return; } // bot

    const v = n => form.elements[n].value.trim();
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
      `${form.product.value ? `\nProduct: ${form.product.value}` : ''}\n\n${v('message')}`);
    show('Your email app should open with the message ready to send. If it does not, email us directly at ' + form.dataset.email + '.', 'ok');
    window.location.href = `mailto:${form.dataset.email}?subject=${subject}&body=${body}`;
  });
})();

/* ---- article modals ---- */
(function(){
  let lastTrigger = null;
  function openModal(trigger){
    const modal = document.getElementById('modal-' + trigger.dataset.open);
    if(!modal) return;
    lastTrigger = trigger;
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    modal.querySelector('.modal-close')?.focus();
  }
  function closeModal(modal){
    modal.classList.remove('open');
    document.body.style.overflow = '';
    lastTrigger?.focus();
  }
  document.querySelectorAll('[data-open]').forEach(trigger=>{
    trigger.addEventListener('click', ()=> openModal(trigger));
    trigger.addEventListener('keydown', e=>{
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openModal(trigger); }
    });
  });
  document.querySelectorAll('.modal-close').forEach(btn=>{
    btn.addEventListener('click', ()=> closeModal(btn.closest('.modal-overlay')));
  });
  document.querySelectorAll('.modal-overlay').forEach(overlay=>{
    overlay.addEventListener('click', e=>{ if(e.target === overlay) closeModal(overlay); });
  });
  document.addEventListener('keydown', e=>{
    if(e.key === 'Escape') document.querySelectorAll('.modal-overlay.open').forEach(closeModal);
  });
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
