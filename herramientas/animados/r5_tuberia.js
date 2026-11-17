const DUR = 17.5;
const PY = 860; // altura del tubo
const XE = 180, XA = 540, XD = 880; // empleado, accionista, dueño
function pipe(ctx, pts, w, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.strokeStyle = '#5B6290'; ctx.lineWidth = w; ctx.beginPath(); pts.forEach((p, i) => i ? ctx.lineTo(...p) : ctx.moveTo(...p)); ctx.stroke();
  ctx.strokeStyle = '#8D93C0'; ctx.lineWidth = w * 0.25; ctx.beginPath(); pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1] - w * 0.22) : ctx.moveTo(p[0], p[1] - w * 0.22)); ctx.stroke();
  ctx.restore();
}
function along(pts, f) { // punto a fracción f del recorrido
  let L = 0; const seg = []; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(d); L += d; }
  let r = f * L; for (let i = 0; i < seg.length; i++) { if (r <= seg[i]) { const k = r / seg[i]; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; } r -= seg[i]; }
  return pts[pts.length - 1];
}
function desk(ctx, x, y) { ctx.fillStyle = '#2A2F5E'; rr(ctx, x - 110, y, 220, 26, 8); ctx.fill(); ctx.fillRect(x - 96, y + 26, 16, 110); ctx.fillRect(x + 80, y + 26, 16, 110); }
function chair(ctx, x, y) { ctx.fillStyle = '#3B4170'; rr(ctx, x - 90, y - 150, 180, 250, 26); ctx.fill(); ctx.fillStyle = '#2A2F5E'; rr(ctx, x - 110, y + 60, 220, 60, 18); ctx.fill(); }
function draw(ctx, t) {
  ctx.fillStyle = C.dark; ctx.fillRect(0, 0, W, H);
  const main = [[XE, 1080], [XE, PY], [XD, PY], [XD, 1040]];
  const br = eo(prog(t, 9.6, 10.6));
  const branch = [[XA, PY], [XA, lerp(PY, 1040, br)]];
  // dueño
  chair(ctx, XD, 1250);
  stick(ctx, XD, 1215, 0.95, '#fff', { tie: 1, arms: 0.35 });
  // monedas acumuladas del dueño
  const pile = Math.floor(clamp(t / 9) * 14 + clamp((t - 10) / 6) * 8);
  for (let i = 0; i < pile; i++) coin(ctx, XD - 90 + (i % 7) * 30, 1380 - Math.floor(i / 7) * 16, 16);
  // empleado trabajando
  desk(ctx, XE, 1210);
  const bob = Math.sin(t * 10) * 6;
  stick(ctx, XE, 1240 + bob, 0.95, '#fff', { arms: 0.45 + Math.sin(t * 10) * 0.08 });
  // sudor
  if (t < 9.5) for (let i = 0; i < 2; i++) { const ph = (t * 1.3 + i * .5) % 1; ctx.save(); ctx.globalAlpha = 1 - ph; ctx.fillStyle = C.blue; ctx.beginPath(); ctx.arc(XE + 46 + i * 10, 1080 + ph * 60, 7, 0, 7); ctx.fill(); ctx.restore(); }
  // tubos
  pipe(ctx, main, 46);
  if (br > 0) pipe(ctx, branch, 40, br);
  // monedas viajando
  const rate = 3;
  for (let i = 0; i < 12; i++) {
    const f = ((t * 0.22 + i / 12) % 1); const p = along(main, f);
    if (t > 0.8) coin(ctx, p[0], p[1], 15, clamp((t - 0.8) * 2));
  }
  if (br > 0.9) for (let i = 0; i < 6; i++) {
    const f = ((t * 0.5 + i / 6) % 1); coin(ctx, XA, lerp(PY, 1040, f), 15);
  }
  // caída al final del tubo
  for (let i = 0; i < 3; i++) { const ph = (t * 1.5 + i / 3) % 1; if (t > 1.5) coin(ctx, XD + Math.sin(i) * 20, 1040 + ph * 100, 15, 1 - ph); }
  // sueldo: gota pequeña al empleado
  if (t > 2) { const ph = (t * 0.35) % 1; coin(ctx, XE + 60, 1080 + ph * 130, 10, 1 - ph); }
  // accionista
  if (br > 0) {
    stick(ctx, XA, 1240, 0.95, C.orange, { arms: 0.9 });
    const ap = Math.floor(clamp((t - 10.6) / 5) * 10);
    for (let i = 0; i < ap; i++) coin(ctx, XA - 60 + (i % 5) * 30, 1380 - Math.floor(i / 5) * 16, 16);
  }
  // etiquetas
  const la = eo(prog(t, 1, 1.6));
  text(ctx, 'TU TRABAJO', XE, 1440, 30, '#C9CDF2', 900, 'center', la, 'Inter Display');
  text(ctx, 'DUEÑO', XD, 1440, 30, '#C9CDF2', 900, 'center', la, 'Inter Display');
  text(ctx, 'GANANCIAS', 530, PY - 60, 30, '#FFC233', 900, 'center', la * (1 - br), 'Inter Display');
  text(ctx, 'TÚ, ACCIONISTA', XA, 1440, 30, C.orange, 900, 'center', br, 'Inter Display');
  // textos
  const h1 = eo(prog(t, 0, .6)) * (1 - prog(t, 5.6, 6.0));
  hook(ctx, ['¿Para quién', ['trabajas', 'o'], 'de verdad?'], 300, h1, { size: 96 });
  const h2 = eo(prog(t, 6.0, 6.5)) * (1 - prog(t, 9.4, 9.8));
  hook(ctx, ['Tú pones las horas.', ['El dueño se lleva', 'b'], 'la ganancia.'], 300, h2, { size: 78 });
  const h3 = eo(prog(t, 10, 10.5));
  hook(ctx, ['Con una acción,', ['tú también', 'o'], 'eres dueño.'], 300, h3, { size: 90 });
  const m = eo(prog(t, 12, 12.6));
  ctx.save(); ctx.globalAlpha = m; ctx.fillStyle = C.navy; rr(ctx, 90, 1500, 900, 86, 18); ctx.fill(); ctx.restore();
  text(ctx, 'Desde $50 en la bolsa de EE. UU.', 540, 1544, 42, '#fff', 800, 'center', m, 'Inter Display');
  socialBar(ctx, eo(prog(t, 0.5, 1.2)) * (1 - prog(t, 11.6, 12)));
  outro(ctx, t, DUR);
}
