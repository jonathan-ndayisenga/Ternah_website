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

/* ---- welcome modal ---- */
(function(){
  const overlay = document.getElementById('welcomeOverlay');
  if(!overlay) return;

  // show once per session
  if(sessionStorage.getItem('ternah_welcomed')) return;

  function closeWelcome(){
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    sessionStorage.setItem('ternah_welcomed','1');
  }

  // open after short delay so page has rendered
  setTimeout(()=>{
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }, 900);

  // skip button
  document.getElementById('welcomeSkip')?.addEventListener('click', closeWelcome);

  // close on backdrop click
  overlay.addEventListener('click', e=>{ if(e.target === overlay) closeWelcome(); });

  // Escape key
  document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeWelcome(); });

  // WhatsApp send
  document.getElementById('welcomeWa')?.addEventListener('click', ()=>{
    const msg = (document.getElementById('welcomeMsg')?.value || '').trim();
    const text = msg
      ? `Hi Ternah, I need your services for: ${msg}`
      : 'Hi Ternah, I would like to know more about your services.';
    window.open(`https://wa.me/256787770007?text=${encodeURIComponent(text)}`, '_blank');
    closeWelcome();
  });

  // Email send
  document.getElementById('welcomeEmail')?.addEventListener('click', ()=>{
    const msg = (document.getElementById('welcomeMsg')?.value || '').trim();
    const subject = encodeURIComponent('New enquiry via Ternah website');
    const body = encodeURIComponent(
      msg
        ? `Hi Ternah,\n\nI need your services for:\n${msg}`
        : 'Hi Ternah,\n\nI would like to know more about your services.'
    );
    window.location.href = `mailto:ternah22@gmail.com?subject=${subject}&body=${body}`;
    closeWelcome();
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

/* ---- solution filter pills ---- */
(function(){
  const bar = document.getElementById('solFilter');
  const grid = document.getElementById('solGrid');
  if(!bar || !grid) return;
  const pills = bar.querySelectorAll('.pill');
  const cards = grid.querySelectorAll('.card[data-filter]');

  pills.forEach(pill=>{
    pill.addEventListener('click', ()=>{
      // update active pill
      pills.forEach(p=>p.classList.remove('active'));
      pill.classList.add('active');

      const filter = pill.dataset.filter;
      cards.forEach(card=>{
        const match = filter === 'all' || card.dataset.filter === filter;
        card.style.transition = 'opacity .3s, transform .3s';
        card.style.opacity  = match ? '1' : '0.25';
        card.style.transform = match ? 'scale(1)' : 'scale(0.96)';
        card.style.pointerEvents = match ? '' : 'none';
      });
    });
  });
})();

/* ---- animated wavy hero (only runs if #waves exists) ---- */
(function(){
  const c = document.getElementById('waves');
  if(!c) return;
  const ctx = c.getContext('2d');
  let W,H,dpr;
  function resize(){
    dpr = Math.min(window.devicePixelRatio||1, 2);
    W = c.clientWidth; H = c.clientHeight;
    c.width = W*dpr; c.height = H*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  resize();
  window.addEventListener('resize', resize);

  let t = 0;
  const LINES = 46;
  function frame(){
    ctx.clearRect(0,0,W,H);
    const cx = W*0.5, cy = H*0.46;
    const g = ctx.createRadialGradient(cx,cy,0, cx,cy, Math.max(W,H)*0.75);
    g.addColorStop(0,  'rgba(61,91,255,0.95)');
    g.addColorStop(0.35,'rgba(47,76,255,0.55)');
    g.addColorStop(0.7, 'rgba(13,20,48,0.20)');
    g.addColorStop(1,   'rgba(7,10,31,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0,0,W,H);

    const spacing = H / LINES;
    for(let i=0;i<LINES;i++){
      const baseY = i*spacing;
      const distFromCore = Math.abs(baseY - cy) / (H*0.6);
      const amp = 12 + 30*(1-Math.min(distFromCore,1));
      const alpha = 0.07 + 0.55*(1-Math.min(distFromCore,1));
      const speed = 0.6 + (i%5)*0.05;
      ctx.beginPath();
      for(let x=0;x<=W;x+=8){
        const k = x/W;
        const y = baseY
          + Math.sin(k*Math.PI*4 + t*speed + i*0.35)*amp
          + Math.sin(k*Math.PI*2 - t*0.4)*amp*0.4;
        x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
      }
      const core = 1-Math.min(distFromCore,1);
      const r = Math.round(150 + 105*core);
      const gg= Math.round(170 + 85*core);
      ctx.strokeStyle = `rgba(${r},${gg},255,${alpha})`;
      ctx.lineWidth = 1.1;
      ctx.stroke();
    }
    t += 0.018;
    requestAnimationFrame(frame);
  }
  frame();
})();
