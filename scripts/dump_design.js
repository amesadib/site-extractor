// Paste/run inside Claude-in-Chrome javascript_tool on the target page.
// Returns compact JSON of the live design system. No full DOM dump.
(() => {
  const els = [...document.querySelectorAll('body *')].slice(0, 4000);
  const bag = { colors:{}, bg:{}, fonts:{}, sizes:{}, weights:{}, radius:{}, shadow:{}, transition:{}, animation:{} };
  const bump = (o,k)=>{ if(!k||k==='none'||k==='normal') return; o[k]=(o[k]||0)+1; };
  for (const el of els) {
    const s = getComputedStyle(el);
    bump(bag.colors, s.color);
    bump(bag.bg, s.backgroundColor);
    bump(bag.fonts, s.fontFamily);
    bump(bag.sizes, s.fontSize);
    bump(bag.weights, s.fontWeight);
    bump(bag.radius, s.borderRadius);
    bump(bag.shadow, s.boxShadow);
    bump(bag.transition, s.transition);
    bump(bag.animation, s.animationName);
  }
  const top = (o,n=25)=>Object.entries(o).sort((a,b)=>b[1]-a[1]).slice(0,n);
  const vars = {};
  for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) {
    if (r.style) for (const p of r.style) if (p.startsWith('--')) vars[p]=r.style.getPropertyValue(p).trim();
  }} catch(e){} }
  const libs = [];
  if (window.gsap) libs.push('GSAP'); if (window.ScrollTrigger) libs.push('ScrollTrigger');
  if (window.lottie||window.bodymovin) libs.push('Lottie'); if (window.THREE) libs.push('Three.js');
  if (window.Swiper) libs.push('Swiper'); if (window.Lenis||window.LocomotiveScroll) libs.push('SmoothScroll');
  if (document.querySelector('[data-framer-name],[data-projectid]')) libs.push('Framer');
  return JSON.stringify({
    colors:top(bag.colors), bg:top(bag.bg), fonts:top(bag.fonts), sizes:top(bag.sizes),
    weights:top(bag.weights), radius:top(bag.radius), shadow:top(bag.shadow),
    transition:top(bag.transition,15), animation:top(bag.animation,15),
    cssVars:vars, motionLibs:libs
  }, null, 0);
})();
