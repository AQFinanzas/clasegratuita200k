// Utilidades comunes para reels animados AQ Finanzas (1080x1920)
const W = 1080, H = 1920;
const C = { navy: '#01005A', orange: '#F04A03', blue: '#2A94F8', dark: '#05061C', cream: '#FBF8F2', light: '#F5F7FC', green: '#22C55E', yellow: '#FFC233' };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const prog = (t, a, b) => clamp((t - a) / (b - a));
const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eo = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const fmt = n => '$' + Math.round(n).toLocaleString('es-CO');

const IMG = {};
function loadImg(k, src) { return new Promise(r => { const i = new Image(); i.onload = () => { IMG[k] = i; r(); }; i.src = src; }); }

function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }

// Texto con varias líneas; cada línea es [texto, estilo] donde estilo 'o' = bloque naranja, 'n' normal
function hook(ctx, lines, y, a, opt = {}) {
  const size = opt.size || 84, col = opt.color || '#fff', lh = size * 1.18;
  ctx.save(); ctx.globalAlpha = a; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.font = `900 ${size}px 'Inter Display'`;
  lines.forEach((l, i) => {
    const [txt, st] = Array.isArray(l) ? l : [l, 'n'];
    const yy = y + i * lh + (1 - a) * 30;
    if (st === 'o' || st === 'b') {
      const w = ctx.measureText(txt).width + 44;
      ctx.fillStyle = st === 'o' ? C.orange : C.navy; rr(ctx, W / 2 - w / 2, yy - lh / 2 + 4, w, lh - 8, 18); ctx.fill();
      ctx.fillStyle = '#fff';
    } else ctx.fillStyle = col;
    ctx.fillText(txt, W / 2, yy + 4);
  });
  ctx.restore();
}

function text(ctx, s, x, y, size, color, weight = 700, align = 'center', a = 1, fam = 'Inter') {
  ctx.save(); ctx.globalAlpha = a; ctx.font = `${weight} ${size}px '${fam}'`; ctx.fillStyle = color; ctx.textAlign = align; ctx.textBaseline = 'middle'; ctx.fillText(s, x, y); ctx.restore();
}

// Barra de redes dentro del recuadro del feed (y ~1600)
function socialBar(ctx, a = 1, dark = true) {
  const y = 1610, fg = dark ? '#fff' : C.navy;
  ctx.save(); ctx.globalAlpha = a * 0.92;
  ctx.font = "700 34px 'Inter'"; const label = '@aqfinanzas'; const tw = ctx.measureText(label).width;
  const total = 3 * 52 + 2 * 18 + 26 + tw; let x = W / 2 - total / 2;
  ctx.strokeStyle = fg; ctx.fillStyle = fg; ctx.lineWidth = 4;
  // Instagram
  rr(ctx, x, y - 24, 48, 48, 14); ctx.stroke(); ctx.beginPath(); ctx.arc(x + 24, y, 11, 0, 7); ctx.stroke(); ctx.beginPath(); ctx.arc(x + 37, y - 13, 3, 0, 7); ctx.fill();
  x += 52 + 18;
  // Facebook
  ctx.beginPath(); ctx.arc(x + 24, y, 24, 0, 7); ctx.fill(); ctx.fillStyle = dark ? C.dark : '#fff'; ctx.font = "900 34px 'Inter'"; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('f', x + 26, y + 4); ctx.fillStyle = fg;
  x += 52 + 18;
  // TikTok (nota)
  ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x + 28, y - 22); ctx.lineTo(x + 28, y + 10); ctx.stroke();
  ctx.beginPath(); ctx.arc(x + 18, y + 12, 10, 0, 7); ctx.lineWidth = 6; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x + 28, y - 22); ctx.quadraticCurveTo(x + 32, y - 8, x + 46, y - 8); ctx.lineWidth = 6; ctx.stroke();
  x += 52 + 26;
  ctx.font = "700 34px 'Inter'"; ctx.textAlign = 'left'; ctx.fillText(label, x, y + 2);
  ctx.restore();
}

// Cierre con logo (últimos ~1.6 s)
function outro(ctx, t, dur, dark = true) {
  const p = prog(t, dur - 1.7, dur - 1.2); if (p <= 0) return;
  ctx.save(); ctx.globalAlpha = p; ctx.fillStyle = dark ? C.dark : '#fff'; ctx.fillRect(0, 0, W, H);
  const img = dark ? IMG.logoW : IMG.logoC; const s = lerp(0.85, 1, eo(p)); const w = 420 * s, h = w * img.height / img.width;
  ctx.drawImage(img, W / 2 - w / 2, 860 - h / 2, w, h);
  text(ctx, 'Comenta APP', W / 2, 1120, 64, C.orange, 900, 'center', p, 'Inter Display');
  text(ctx, 'y te envío gratis mi app', W / 2, 1200, 38, dark ? '#C9CDF2' : C.navy, 600, 'center', p);
  ctx.restore(); socialBar(ctx, p, dark);
}

// Figura de palitos
function stick(ctx, x, y, s, color, pose = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 14; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.arc(0, -150, 34, 0, 7); ctx.fill();
  const arm = pose.arms || 0; // 0 abajo, 1 arriba
  ctx.beginPath(); ctx.moveTo(0, -110); ctx.lineTo(0, 0); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, -95); ctx.lineTo(-55, lerp(-30, -170, arm)); ctx.moveTo(0, -95); ctx.lineTo(55, lerp(-30, -170, arm)); ctx.stroke();
  const leg = pose.leg || 0;
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-38 + leg * 20, 110); ctx.moveTo(0, 0); ctx.lineTo(38 - leg * 20, 110); ctx.stroke();
  if (pose.tie) { ctx.fillStyle = C.orange; ctx.beginPath(); ctx.moveTo(-8, -108); ctx.lineTo(8, -108); ctx.lineTo(4, -55); ctx.lineTo(0, -45); ctx.lineTo(-4, -55); ctx.fill(); }
  ctx.restore();
}

function coin(ctx, x, y, r = 18, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#FFC233'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  ctx.strokeStyle = '#E09A00'; ctx.lineWidth = r * 0.18; ctx.stroke(); ctx.fillStyle = '#B87400'; ctx.font = `900 ${r * 1.2}px Inter`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('$', x, y + 1); ctx.restore();
}

function bill(ctx, x, y, w, a = 1, rot = 0) {
  const h = w * 0.45; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(rot);
  ctx.fillStyle = '#7BC98A'; rr(ctx, -w / 2, -h / 2, w, h, 8); ctx.fill(); ctx.strokeStyle = '#3E8F52'; ctx.lineWidth = 4; rr(ctx, -w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 6); ctx.stroke();
  ctx.fillStyle = '#3E8F52'; ctx.beginPath(); ctx.arc(0, 0, h * 0.28, 0, 7); ctx.fill(); ctx.fillStyle = '#CDEFD5'; ctx.font = `900 ${h * 0.36}px Inter`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('$', 0, 2);
  ctx.restore();
}

function disclaimer(ctx, s, a = 1, color = '#9AA0C8') { const i = s.indexOf('. '); const l1 = s.slice(0, i + 1), l2 = s.slice(i + 2); text(ctx, l1, W / 2, 1690, 22, color, 500, 'center', a); text(ctx, l2, W / 2, 1722, 22, color, 500, 'center', a); }
