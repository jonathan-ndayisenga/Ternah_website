/* =========================================================
   TERNAH — shared site script
   ========================================================= */

/* ---- header scroll state ---- */
const hdr = document.getElementById('hdr');
function updateHeader(){ if(hdr) hdr.classList.toggle('scrolled', window.scrollY > 20); }
window.addEventListener('scroll', updateHeader, {passive:true});
updateHeader();

/* ---- mobile burger ---- */
const burger = document.getElementById('burger');
const navlinks = document.getElementById('navlinks');
if(burger && navlinks){
  burger.addEventListener('click', ()=>{
    const open = navlinks.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
    // animate burger → X
    burger.querySelectorAll('span').forEach((s,i)=>{
      s.style.transform = open
        ? [' rotate(45deg) translate(5px,5px)',' opacity:0',' rotate(-45deg) translate(5px,-5px)'][i] : '';
      s.style.opacity   = (open && i===1) ? '0' : '';
    });
  });
  // close nav when any link is tapped
  navlinks.querySelectorAll('a').forEach(a=>{
    a.addEventListener('click', ()=>{
      navlinks.classList.remove('open');
      burger.setAttribute('aria-expanded', false);
      burger.querySelectorAll('span').forEach(s=>{ s.style.transform=''; s.style.opacity=''; });
    });
  });
  // close nav on outside tap
  document.addEventListener('click', e=>{
    if(!burger.contains(e.target) && !navlinks.contains(e.target)){
      navlinks.classList.remove('open');
      burger.setAttribute('aria-expanded', false);
      burger.querySelectorAll('span').forEach(s=>{ s.style.transform=''; s.style.opacity=''; });
    }
  });
}

/* ---- mark active nav link (by data-page on <body>) ---- */
(function(){
  const page = document.body.dataset.page;
  document.querySelectorAll('.navlinks a[data-nav]').forEach(a=>{
    a.classList.toggle('active', a.dataset.nav === page);
  });
})();

/* ---- footer year ---- */
const yr = document.getElementById('yr');
if(yr) yr.textContent = new Date().getFullYear();

/* ---- scroll reveal ---- */
(function(){
  const els = document.querySelectorAll('.reveal');
  if(!els.length) return;
  const io = new IntersectionObserver(entries=>{
    entries.forEach(en=>{ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
  },{threshold:.12, rootMargin:'0px 0px -8% 0px'});
  els.forEach(el=>io.observe(el));
})();

/* ---- contact form (opens email app, no backend) ---- */
(function(){
  const btn = document.getElementById('sendBtn');
  if(!btn) return;
  btn.addEventListener('click', ()=>{
    const v = id => (document.getElementById(id)?.value || '').trim();
    const name=v('f_name'), email=v('f_email'), co=v('f_co'), msg=v('f_msg');
    const out=document.getElementById('formMsg');
    if(!name||!email||!msg){ out.style.color='#ff9c9c'; out.textContent='Please fill in your name, email, and message.'; return; }
    const subject=encodeURIComponent(`New project enquiry — ${name}`);
    const body=encodeURIComponent(`Name: ${name}\nEmail: ${email}\nCompany: ${co||'—'}\n\n${msg}`);
    out.style.color='var(--blue-soft)'; out.textContent='Opening your email app…';
    window.location.href=`mailto:ternah22@gmail.com?subject=${subject}&body=${body}`;
  });
})();

/* ---- article modals ---- */
(function(){
  // open
  document.querySelectorAll('[data-open]').forEach(trigger=>{
    trigger.addEventListener('click', ()=>{
      const modal = document.getElementById('modal-' + trigger.dataset.open);
      if(!modal) return;
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      modal.querySelector('.modal-close')?.focus();
    });
  });

  // close helpers
  function closeModal(modal){
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  // close button
  document.querySelectorAll('.modal-close').forEach(btn=>{
    btn.addEventListener('click', ()=> closeModal(btn.closest('.modal-overlay')));
  });

  // click outside modal box
  document.querySelectorAll('.modal-overlay').forEach(overlay=>{
    overlay.addEventListener('click', e=>{
      if(e.target === overlay) closeModal(overlay);
    });
  });

  // Escape key
  document.addEventListener('keydown', e=>{
    if(e.key === 'Escape'){
      document.querySelectorAll('.modal-overlay.open').forEach(closeModal);
    }
  });
})();

/* ---- shared: scroll to a card by id ---- */
function scrollToCard(id){
  const el = document.getElementById(id);
  if(!el) return;
  const headerH = document.getElementById('hdr')?.offsetHeight || 72;
  const top = el.getBoundingClientRect().top + window.scrollY - headerH - 20;
  window.scrollTo({top, behavior:'smooth'});
  // pulse highlight
  el.classList.remove('card-highlight');
  void el.offsetWidth; // force reflow so animation restarts
  el.classList.add('card-highlight');
  el.addEventListener('animationend', ()=> el.classList.remove('card-highlight'), {once:true});
}

/* ---- hero tags → scroll to solution card ---- */
(function(){
  document.querySelectorAll('.tag[data-scroll]').forEach(tag=>{
    tag.addEventListener('click', ()=> scrollToCard(tag.dataset.scroll));
  });
})();

/* ---- solution filter pills → filter + scroll to card ---- */
(function(){
  const bar = document.getElementById('solFilter');
  const grid = document.getElementById('solGrid');
  if(!bar || !grid) return;
  const pills = bar.querySelectorAll('.pill');
  const cards = grid.querySelectorAll('.card[data-filter]');

  pills.forEach(pill=>{
    pill.addEventListener('click', ()=>{
      pills.forEach(p=>p.classList.remove('active'));
      pill.classList.add('active');

      const filter = pill.dataset.filter;
      cards.forEach(card=>{
        const match = filter === 'all' || card.dataset.filter === filter;
        card.style.transition = 'opacity .3s, transform .3s';
        card.style.opacity    = match ? '1' : '0.25';
        card.style.transform  = match ? 'scale(1)' : 'scale(0.96)';
        card.style.pointerEvents = match ? '' : 'none';
      });

      // scroll to first matching card
      if(filter !== 'all'){
        const target = grid.querySelector(`.card[data-filter="${filter}"]`);
        if(target) setTimeout(()=> scrollToCard(target.id), 80);
      } else {
        // scroll to grid top
        const headerH = document.getElementById('hdr')?.offsetHeight || 72;
        const top = grid.getBoundingClientRect().top + window.scrollY - headerH - 20;
        window.scrollTo({top, behavior:'smooth'});
      }
    });
  });
})();

