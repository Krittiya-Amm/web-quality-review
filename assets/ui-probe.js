/**
 * ui-probe.js — เก็บค่า UI จริงจากหน้าเว็บที่เรนเดอร์แล้ว
 * ใช้กับ skill web-quality-review เพื่อให้คะแนนกลุ่ม 🎨 UI มีความหมาย
 *
 * รันได้ 3 ทาง (ผลลัพธ์เหมือนกัน):
 *   1) Claude Code / playwright :  await page.evaluate(uiProbe)
 *   2) Claude in Chrome         :  javascript_tool → วาง IIFE นี้
 *   3) มือ                      :  วางใน DevTools Console
 *
 * รันซ้ำที่ 375 / 768 / 1440 / 1920 px แล้วเทียบผลแต่ละ breakpoint
 */
(function uiProbe() {
  const round = (n, d = 2) => Math.round(n * 10 ** d) / 10 ** d;

  /* ---------- helper: สี ---------- */
  const parseRGB = (s) => {
    if (!s) return null;
    const m = s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
    if (!m) return null;
    return { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] };
  };
  const toHex = (c) =>
    '#' + [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
  const relLum = (c) => {
    const f = (v) => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  };
  const contrast = (a, b) => {
    const [l1, l2] = [relLum(a), relLum(b)].sort((x, y) => y - x);
    return round((l1 + 0.05) / (l2 + 0.05));
  };
  /* หาสีพื้นหลังจริง โดยไล่ขึ้นไปหา ancestor ที่ไม่โปร่งใส */
  const effectiveBg = (el) => {
    let node = el;
    while (node && node !== document.documentElement) {
      const bg = parseRGB(getComputedStyle(node).backgroundColor);
      if (bg && bg.a > 0.05) return bg;
      node = node.parentElement;
    }
    return { r: 255, g: 255, b: 255, a: 1 };
  };

  const bump = (map, key) => { if (key) map[key] = (map[key] || 0) + 1; };
  const sortMap = (m) =>
    Object.fromEntries(Object.entries(m).sort((a, b) => b[1] - a[1]));

  const colors = {}, bgColors = {}, fonts = {}, sizes = {},
        lineHeights = {}, radii = {}, shadows = {}, spacing = {};
  const contrastFails = [], smallTargets = [], overflowing = [];

  const all = document.querySelectorAll('*');
  all.forEach((el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const rect = el.getBoundingClientRect();

    bump(fonts, cs.fontFamily.split(',')[0].replace(/["']/g, '').trim());
    bump(radii, cs.borderRadius);
    if (cs.boxShadow && cs.boxShadow !== 'none') bump(shadows, cs.boxShadow);
    [cs.marginTop, cs.marginBottom, cs.paddingTop, cs.paddingBottom]
      .forEach((v) => { if (v && v !== '0px') bump(spacing, v); });

    const bg = parseRGB(cs.backgroundColor);
    if (bg && bg.a > 0.05) bump(bgColors, toHex(bg));

    /* ตรวจเฉพาะ element ที่มีข้อความของตัวเอง */
    const ownText = Array.from(el.childNodes)
      .filter((n) => n.nodeType === 3)
      .map((n) => n.textContent.trim())
      .join(' ')
      .trim();

    if (ownText.length > 1 && rect.width > 0) {
      const fg = parseRGB(cs.color);
      bump(colors, fg ? toHex(fg) : null);
      bump(sizes, cs.fontSize);
      bump(lineHeights, cs.lineHeight);

      if (fg && fg.a > 0.5) {
        const ratio = contrast(fg, effectiveBg(el));
        const px = parseFloat(cs.fontSize);
        const bold = parseInt(cs.fontWeight, 10) >= 700;
        const large = px >= 24 || (px >= 18.66 && bold);
        const need = large ? 3 : 4.5;
        if (ratio < need) {
          contrastFails.push({
            text: ownText.slice(0, 45),
            fg: toHex(fg), bg: toHex(effectiveBg(el)),
            fontSize: cs.fontSize, ratio, need,
            sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
              ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''),
          });
        }
      }
    }

    /* element ล้นขอบจอ */
    if (rect.right > document.documentElement.clientWidth + 2 && rect.width > 8) {
      overflowing.push({
        sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
          ? '.' + el.className.trim().split(/\s+/)[0] : ''),
        right: round(rect.right), viewport: document.documentElement.clientWidth,
      });
    }
  });

  /* touch target */
  document.querySelectorAll('a,button,input,select,textarea,[role="button"]').forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.width < 44 || r.height < 44) {
      smallTargets.push({
        tag: el.tagName.toLowerCase(),
        label: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 30),
        w: round(r.width), h: round(r.height),
      });
    }
  });

  /* รูป */
  const imgs = Array.from(document.images);
  const media = {
    total: imgs.length,
    broken: imgs.filter((i) => i.complete && i.naturalWidth === 0)
      .map((i) => i.currentSrc || i.src || '(src ว่าง)'),
    missingAlt: imgs.filter((i) => !i.hasAttribute('alt')).map((i) => i.src.split('/').pop()),
    emptyAlt: imgs.filter((i) => i.getAttribute('alt') === '').length,
    noDimensions: imgs.filter((i) => !i.getAttribute('width') || !i.getAttribute('height')).length,
    notLazy: imgs.filter((i) => i.loading !== 'lazy').length,
    formats: imgs.reduce((a, i) => {
      const m = (i.currentSrc || i.src || '').split('?')[0].match(/\.(\w{2,5})$/);
      if (m) a[m[1].toLowerCase()] = (a[m[1].toLowerCase()] || 0) + 1;
      return a;
    }, {}),
  };

  /* heading + meta */
  const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'))
    .map((h) => +h.tagName[1]);
  let headingJumps = 0;
  headings.forEach((lv, i) => { if (i && lv - headings[i - 1] > 1) headingJumps++; });

  const meta = (sel, attr = 'content') => {
    const el = document.querySelector(sel);
    return el ? el.getAttribute(attr) : null;
  };

  return {
    viewport: { w: window.innerWidth, h: window.innerHeight, dpr: window.devicePixelRatio },
    horizontalScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    scrollWidth: document.documentElement.scrollWidth,
    elementCount: all.length,

    /* ---- UI1 Design System ---- */
    tokens: {
      textColors: sortMap(colors),
      bgColors: sortMap(bgColors),
      fontFamilies: sortMap(fonts),
      borderRadii: sortMap(radii),
      shadows: Object.keys(shadows).length,
      spacingValues: Object.keys(spacing).length,
      uniqueCounts: {
        textColors: Object.keys(colors).length,
        bgColors: Object.keys(bgColors).length,
        fonts: Object.keys(fonts).length,
        radii: Object.keys(radii).length,
        shadows: Object.keys(shadows).length,
        spacing: Object.keys(spacing).length,
      },
    },

    /* ---- UI2 Responsive ---- */
    overflowing: overflowing.slice(0, 20),
    smallTargets: smallTargets.slice(0, 25),
    smallTargetCount: smallTargets.length,

    /* ---- UI3 Typography, Contrast & Media ---- */
    typography: {
      fontSizes: sortMap(sizes),
      lineHeights: sortMap(lineHeights),
      bodyBelow16: Object.entries(sizes)
        .filter(([k]) => parseFloat(k) < 16)
        .reduce((a, [k, v]) => (a[k] = v, a), {}),
    },
    contrastFails: contrastFails.slice(0, 30),
    contrastFailCount: contrastFails.length,
    media,
    headings: { counts: { h1: document.querySelectorAll('h1').length }, order: headings, jumps: headingJumps },

    /* ---- T1 SEO ---- */
    seo: {
      title: document.title,
      description: meta('meta[name="description"]'),
      canonical: meta('link[rel="canonical"]', 'href'),
      ogImage: meta('meta[property="og:image"]'),
      ogTitle: meta('meta[property="og:title"]'),
      twitterCard: meta('meta[name="twitter:card"]'),
      favicon: !!document.querySelector('link[rel*="icon"]'),
      jsonLd: document.querySelectorAll('script[type="application/ld+json"]').length,
      lang: document.documentElement.lang || null,
      viewportMeta: meta('meta[name="viewport"]'),
    },
  };
})();
