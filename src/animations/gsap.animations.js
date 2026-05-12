/**
 * 8D Hubify — GSAP Animation Library
 * Design System v1.0
 *
 * Depende de: gsap (CDN ou npm)
 * Registra ScrollTrigger e CustomEase globalmente.
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { CustomEase } from 'gsap/CustomEase';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(ScrollTrigger, CustomEase, SplitText);

/* ============================================================
   EASINGS — mapeados dos tokens de design
   ============================================================ */
CustomEase.create('8dh.smooth',  '0.25, 0.46, 0.45, 0.94');
CustomEase.create('8dh.spring',  '0.34, 1.56, 0.64, 1');
CustomEase.create('8dh.outExpo', '0.16, 1, 0.3, 1');
CustomEase.create('8dh.inOut',   '0.45, 0, 0.55, 1');

/* ============================================================
   DEFAULTS GLOBAIS
   ============================================================ */
gsap.defaults({ ease: '8dh.smooth', duration: 0.6 });

ScrollTrigger.defaults({
  toggleActions: 'play none none none',
  start: 'top 85%',
});

/* ============================================================
   FADE — utilitário base
   ============================================================ */

/**
 * fadeIn(targets, options)
 * Fade + translação vertical para cima.
 */
export function fadeIn(targets, options = {}) {
  const {
    y = 40,
    duration = 0.8,
    stagger = 0,
    delay = 0,
    ease = '8dh.outExpo',
    scrollTrigger = null,
  } = options;

  return gsap.from(targets, {
    opacity: 0,
    y,
    duration,
    stagger,
    delay,
    ease,
    scrollTrigger,
    clearProps: 'all',
  });
}

/**
 * fadeOut(targets, options)
 */
export function fadeOut(targets, options = {}) {
  const { y = -20, duration = 0.5, ease = '8dh.inOut', delay = 0 } = options;
  return gsap.to(targets, { opacity: 0, y, duration, ease, delay });
}

/* ============================================================
   TEXTO — animações tipográficas (requer SplitText)
   ============================================================ */

/**
 * revealHeading(el, options)
 * Revela título linha a linha com máscara (clip).
 */
export function revealHeading(el, options = {}) {
  const {
    duration = 1,
    stagger = 0.08,
    ease = '8dh.outExpo',
    scrollTrigger = null,
    delay = 0,
  } = options;

  const split = new SplitText(el, { type: 'lines', linesClass: 'line-wrap' });
  const inner = new SplitText(el, { type: 'lines' });

  gsap.set(split.lines, { overflow: 'hidden' });

  return gsap.from(inner.lines, {
    y: '110%',
    opacity: 0,
    duration,
    stagger,
    ease,
    delay,
    scrollTrigger,
  });
}

/**
 * typeWriter(el, options)
 * Efeito máquina de escrever por caractere.
 */
export function typeWriter(el, options = {}) {
  const { duration = 0.03, ease = 'none', delay = 0 } = options;
  const split = new SplitText(el, { type: 'chars' });

  return gsap.from(split.chars, {
    opacity: 0,
    duration,
    ease,
    delay,
    stagger: duration,
  });
}

/**
 * countUp(el, options)
 * Anima um número de `from` até o valor atual do elemento.
 */
export function countUp(el, options = {}) {
  const { from = 0, duration = 2, ease = '8dh.outExpo', suffix = '' } = options;
  const to = parseFloat(el.textContent.replace(/\D/g, ''));

  return gsap.fromTo(
    { val: from },
    { val: to },
    {
      duration,
      ease,
      onUpdate() {
        el.textContent = Math.round(this.targets()[0].val) + suffix;
      },
    }
  );
}

/* ============================================================
   SCROLL — animações disparadas por ScrollTrigger
   ============================================================ */

/**
 * scrollFadeUp(targets, options)
 * Versão de fadeIn vinculada ao scroll — uso mais comum em seções.
 */
export function scrollFadeUp(targets, options = {}) {
  return fadeIn(targets, {
    y: 60,
    stagger: 0.12,
    duration: 0.9,
    ...options,
    scrollTrigger: {
      trigger: typeof targets === 'string' ? targets : targets[0],
      start: 'top 80%',
      once: true,
      ...(options.scrollTrigger || {}),
    },
  });
}

/**
 * scrollRevealCards(container, cardSelector, options)
 * Revela cards em cascata ao entrar na viewport.
 */
export function scrollRevealCards(container, cardSelector = '.card', options = {}) {
  const cards = gsap.utils.toArray(`${container} ${cardSelector}`);

  return gsap.from(cards, {
    opacity: 0,
    y: 50,
    scale: 0.96,
    duration: 0.7,
    stagger: 0.1,
    ease: '8dh.spring',
    scrollTrigger: {
      trigger: container,
      start: 'top 75%',
    },
    ...options,
  });
}

/**
 * scrollParallax(el, options)
 * Efeito parallax simples no scroll.
 */
export function scrollParallax(el, options = {}) {
  const { speed = 0.3, start = 'top bottom', end = 'bottom top' } = options;

  return gsap.to(el, {
    yPercent: -100 * speed,
    ease: 'none',
    scrollTrigger: {
      trigger: el,
      start,
      end,
      scrub: true,
    },
  });
}

/**
 * scrollHorizontal(track, options)
 * Scroll horizontal dentro de um container fixo (carousel/strip).
 */
export function scrollHorizontal(track, options = {}) {
  const panels = gsap.utils.toArray(`${track} > *`);
  const totalWidth = panels.length * panels[0].offsetWidth;

  return gsap.to(track, {
    x: -(totalWidth - window.innerWidth),
    ease: 'none',
    scrollTrigger: {
      trigger: track,
      pin: true,
      scrub: 1,
      end: `+=${totalWidth}`,
      ...options.scrollTrigger,
    },
  });
}

/* ============================================================
   HOVER — microinterações
   ============================================================ */

/**
 * magneticHover(el, strength)
 * Efeito magnético: elemento segue o cursor levemente.
 */
export function magneticHover(el, strength = 0.4) {
  const node = typeof el === 'string' ? document.querySelector(el) : el;

  node.addEventListener('mousemove', (e) => {
    const rect = node.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) * strength;
    const dy = (e.clientY - cy) * strength;

    gsap.to(node, { x: dx, y: dy, duration: 0.4, ease: '8dh.smooth' });
  });

  node.addEventListener('mouseleave', () => {
    gsap.to(node, { x: 0, y: 0, duration: 0.6, ease: '8dh.spring' });
  });
}

/**
 * hoverScale(el, scale)
 * Scale suave no hover — ideal para cards e botões.
 */
export function hoverScale(el, scale = 1.04) {
  const nodes = typeof el === 'string'
    ? document.querySelectorAll(el)
    : [el];

  nodes.forEach((node) => {
    node.addEventListener('mouseenter', () =>
      gsap.to(node, { scale, duration: 0.3, ease: '8dh.spring' })
    );
    node.addEventListener('mouseleave', () =>
      gsap.to(node, { scale: 1, duration: 0.4, ease: '8dh.smooth' })
    );
  });
}

/**
 * hoverGlow(el, color)
 * Adiciona box-shadow glowing no hover.
 */
export function hoverGlow(el, color = 'rgba(102,51,255,0.4)') {
  const nodes = typeof el === 'string'
    ? document.querySelectorAll(el)
    : [el];

  nodes.forEach((node) => {
    node.addEventListener('mouseenter', () =>
      gsap.to(node, { boxShadow: `0 0 40px ${color}`, duration: 0.3 })
    );
    node.addEventListener('mouseleave', () =>
      gsap.to(node, { boxShadow: '0 0 0px transparent', duration: 0.5 })
    );
  });
}

/* ============================================================
   PÁGINA — transições de entrada/saída
   ============================================================ */

/**
 * pageEnter(options)
 * Anima os elementos da página na entrada — deve ser chamado
 * no DOMContentLoaded ou equivalente do framework.
 */
export function pageEnter(options = {}) {
  const {
    hero      = '[data-anim="hero"]',
    headings  = '[data-anim="heading"]',
    body      = '[data-anim="body"]',
    cta       = '[data-anim="cta"]',
    media     = '[data-anim="media"]',
  } = options;

  const tl = gsap.timeline({ defaults: { ease: '8dh.outExpo' } });

  tl.from(hero, { opacity: 0, y: 80, duration: 1.2 }, 0)
    .from(headings, { opacity: 0, y: 40, stagger: 0.08, duration: 1 }, 0.2)
    .from(body, { opacity: 0, y: 24, stagger: 0.06, duration: 0.8 }, 0.45)
    .from(cta, { opacity: 0, scale: 0.92, duration: 0.6 }, 0.65)
    .from(media, { opacity: 0, scale: 0.95, duration: 1 }, 0.1);

  return tl;
}

/**
 * pageExit(duration)
 * Fade out para transição entre páginas.
 */
export function pageExit(duration = 0.4) {
  return gsap.to('body', { opacity: 0, duration, ease: '8dh.inOut' });
}

/* ============================================================
   LOADER — tela de carregamento da marca
   ============================================================ */

/**
 * brandLoader(loaderEl, logoEl, onComplete)
 * Anima o loader de entrada da marca 8D Hubify.
 */
export function brandLoader(loaderEl, logoEl, onComplete) {
  const tl = gsap.timeline({ onComplete });

  tl.set(loaderEl, { autoAlpha: 1 })
    .from(logoEl, {
      scale: 0.6,
      opacity: 0,
      duration: 1,
      ease: '8dh.spring',
    })
    .to(logoEl, {
      scale: 1.05,
      duration: 0.4,
      ease: '8dh.smooth',
    })
    .to(loaderEl, {
      yPercent: -100,
      duration: 0.9,
      ease: '8dh.outExpo',
      delay: 0.3,
    });

  return tl;
}

/* ============================================================
   BACKGROUND — elementos decorativos animados
   ============================================================ */

/**
 * floatingOrbs(container, options)
 * Anima orbs/círculos decorativos com movimento orgânico.
 */
export function floatingOrbs(container, options = {}) {
  const { duration = 6, intensity = 30 } = options;
  const orbs = gsap.utils.toArray(`${container} [data-orb]`);

  orbs.forEach((orb, i) => {
    gsap.to(orb, {
      y: `+=${intensity * (i % 2 === 0 ? 1 : -1)}`,
      x: `+=${intensity * 0.5 * (i % 3 === 0 ? 1 : -1)}`,
      rotate: 15 * (i % 2 === 0 ? 1 : -1),
      duration: duration + i * 0.8,
      ease: 'sine.inOut',
      yoyo: true,
      repeat: -1,
    });
  });
}

/**
 * gradientShift(el, colors, duration)
 * Anima gradiente de fundo entre as cores da paleta.
 */
export function gradientShift(el, duration = 8) {
  const node = typeof el === 'string' ? document.querySelector(el) : el;
  const colors = [
    ['#6633FF', '#000033'],
    ['#000033', '#ED694B'],
    ['#ED694B', '#FFCE44'],
    ['#FFCE44', '#6633FF'],
  ];
  let index = 0;

  const animate = () => {
    const [c1, c2] = colors[index % colors.length];
    gsap.to(node, {
      background: `linear-gradient(135deg, ${c1}, ${c2})`,
      duration,
      ease: 'sine.inOut',
      onComplete: animate,
    });
    index++;
  };

  animate();
}

/* ============================================================
   CURSOR — cursor customizado
   ============================================================ */

/**
 * customCursor(cursorEl, options)
 * Cursor seguidor com blend mode e estados de hover.
 */
export function customCursor(cursorEl, options = {}) {
  const { lerp = 0.12, hoverTargets = 'a, button, [data-cursor]' } = options;
  const node = typeof cursorEl === 'string'
    ? document.querySelector(cursorEl)
    : cursorEl;

  let mx = 0, my = 0;
  let cx = 0, cy = 0;

  document.addEventListener('mousemove', (e) => {
    mx = e.clientX;
    my = e.clientY;
  });

  gsap.ticker.add(() => {
    cx += (mx - cx) * lerp;
    cy += (my - cy) * lerp;
    gsap.set(node, { x: cx, y: cy });
  });

  document.querySelectorAll(hoverTargets).forEach((el) => {
    el.addEventListener('mouseenter', () =>
      gsap.to(node, { scale: 2.5, duration: 0.3, ease: '8dh.spring' })
    );
    el.addEventListener('mouseleave', () =>
      gsap.to(node, { scale: 1, duration: 0.4, ease: '8dh.smooth' })
    );
  });
}

/* ============================================================
   BATCH SCROLL — registra múltiplas animações de uma vez
   ============================================================ */

/**
 * initScrollAnimations()
 * Lê atributos `data-anim` no DOM e registra as animações
 * correspondentes automaticamente via ScrollTrigger.batch.
 */
export function initScrollAnimations() {
  /* data-anim="fade-up" */
  ScrollTrigger.batch('[data-anim="fade-up"]', {
    onEnter: (batch) =>
      gsap.from(batch, {
        opacity: 0,
        y: 50,
        stagger: 0.1,
        duration: 0.8,
        ease: '8dh.outExpo',
        clearProps: 'all',
      }),
    start: 'top 85%',
    once: true,
  });

  /* data-anim="fade-left" */
  ScrollTrigger.batch('[data-anim="fade-left"]', {
    onEnter: (batch) =>
      gsap.from(batch, {
        opacity: 0,
        x: -60,
        stagger: 0.1,
        duration: 0.9,
        ease: '8dh.outExpo',
        clearProps: 'all',
      }),
    start: 'top 85%',
    once: true,
  });

  /* data-anim="fade-right" */
  ScrollTrigger.batch('[data-anim="fade-right"]', {
    onEnter: (batch) =>
      gsap.from(batch, {
        opacity: 0,
        x: 60,
        stagger: 0.1,
        duration: 0.9,
        ease: '8dh.outExpo',
        clearProps: 'all',
      }),
    start: 'top 85%',
    once: true,
  });

  /* data-anim="scale-in" */
  ScrollTrigger.batch('[data-anim="scale-in"]', {
    onEnter: (batch) =>
      gsap.from(batch, {
        opacity: 0,
        scale: 0.85,
        stagger: 0.1,
        duration: 0.8,
        ease: '8dh.spring',
        clearProps: 'all',
      }),
    start: 'top 85%',
    once: true,
  });

  /* data-anim="line-reveal" — requer SplitText */
  document.querySelectorAll('[data-anim="line-reveal"]').forEach((el) => {
    revealHeading(el, {
      scrollTrigger: { trigger: el, start: 'top 80%', once: true },
    });
  });

  /* data-anim="count-up" */
  document.querySelectorAll('[data-anim="count-up"]').forEach((el) => {
    ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      once: true,
      onEnter: () => countUp(el, { suffix: el.dataset.suffix || '' }),
    });
  });
}

/* ============================================================
   EXPORTS NOMEADOS — para tree-shaking
   ============================================================ */
export {
  gsap,
  ScrollTrigger,
  CustomEase,
  SplitText,
};
