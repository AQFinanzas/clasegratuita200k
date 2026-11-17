const DUR = 15.5;
const COLS = [
  { n: 'Sin empleo', v: [1, 0.1, 0.2], pose: { arms: 0 } },
  { n: 'Empleado', v: [0.25, 0.5, 0.25], pose: { tie: 1 } },
  { n: 'Independiente', v: [0.1, 0.75, 0.45], pose: { arms: 0.3 } },
  { n: 'Inversionista', v: [1, 1, 1], pose: { arms: 1 } },
];
const ROWS = ['Tiempo', 'Dinero', 'Libertad'];
const CX = [318, 524, 730, 936], RY = [1010, 1150, 1290];

function battery(ctx, x, y, lvl, a) {
  const w = 150, h = 66; ctx.save(); ctx.globalAlpha = a;
  ctx.strokeStyle = '#ffffffcc'; ctx.lineWidth = 6; rr(ctx, x - w / 2, y - h / 2, w, h, 12); ctx.stroke();
  ctx.fillStyle = '#ffffffcc'; rr(ctx, x + w / 2 + 3, y - 14, 10, 28, 4); ctx.fill();
  const col = lvl < 0.3 ? C.orange : lvl < 0.7 ? C.yellow : C.green;
  const segs = 4, fill = lvl * segs;
  for (let i = 0; i < segs; i++) {
    const f = clamp(fill - i); if (f <= 0) break;
    ctx.fillStyle = col; rr(ctx, x - w / 2 + 10 + i * 33, y - h / 2 + 10, 29 * f, h - 20, 5); ctx.fill();
  }
  ctx.restore();
}

function draw(ctx, t) {
  ctx.fillStyle = C.dark; ctx.fillRect(0, 0, W, H);
  // rejilla sutil
  ctx.strokeStyle = '#ffffff08'; ctx.lineWidth = 2;
  for (let x = 0; x < W; x += 60) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
  for (let y = 0; y < H; y += 60) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

  hook(ctx, ['Solo hay', ['4 tipos', 'o'], 'de personas'], 290, eo(prog(t, 0, 0.6)), { size: 100 });

  const ga = eo(prog(t, 0.8, 1.4));
  // filas
  ROWS.forEach((r, i) => text(ctx, r, 52, RY[i], 34, '#B9BEE0', 700, 'left', ga));
  COLS.forEach((c, j) => {
    const s = 1.2 + j * 2.1; const ap = eo(prog(t, s, s + 0.5));
    const hi = j === 3 ? eo(prog(t, s, s + 0.6)) : 0;
    if (hi > 0) { ctx.save(); ctx.globalAlpha = hi; ctx.strokeStyle = C.orange; ctx.lineWidth = 6; rr(ctx, CX[j] - 104, 640, 208, 720, 26); ctx.stroke(); ctx.fillStyle = '#F04A0318'; ctx.fill(); ctx.restore(); }
    ctx.save(); ctx.globalAlpha = Math.max(ga * 0.35, ap);
    stick(ctx, CX[j], 800 + (1 - ap) * 20, 0.62, j === 3 ? C.orange : '#fff', c.pose);
    ctx.restore();
    text(ctx, c.n, CX[j], 905, 26, j === 3 ? C.orange : '#fff', 800, 'center', Math.max(ga * 0.35, ap));
    c.v.forEach((v, i) => {
      const fp = eo(prog(t, s + 0.3 + i * 0.25, s + 1.1 + i * 0.25));
      battery(ctx, CX[j], RY[i], v * fp, Math.max(ga * 0.5, ap));
    });
  });

  const m = eo(prog(t, 10, 10.6)), m2 = eo(prog(t, 11.2, 11.8));
  text(ctx, 'El inversionista no trabaja más horas.', W / 2, 1450, 42, '#fff', 800, 'center', m, 'Inter Display');
  ctx.save(); ctx.globalAlpha = m2; ctx.font = "900 50px 'Inter Display'"; const s2 = 'Pone su dinero a trabajar.'; const w2 = ctx.measureText(s2).width + 40;
  ctx.fillStyle = C.orange; rr(ctx, W / 2 - w2 / 2, 1490, w2, 76, 14); ctx.fill(); ctx.restore();
  text(ctx, 'Pone su dinero a trabajar.', W / 2, 1530, 50, '#fff', 900, 'center', m2, 'Inter Display');

  socialBar(ctx, eo(prog(t, 0.5, 1.2)) * (1 - prog(t, 10, 10.4)));
  outro(ctx, t, DUR);
}
