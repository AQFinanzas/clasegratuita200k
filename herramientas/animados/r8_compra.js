const DUR = 18;
function car(ctx, x, y, s, wear, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s);
  const col = wear > 0.5 ? '#7A7F99' : '#2A94F8';
  ctx.fillStyle = col; rr(ctx, -170, -40, 340, 80, 26); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-100, -40); ctx.lineTo(-60, -100); ctx.lineTo(70, -100); ctx.lineTo(115, -40); ctx.fill();
  ctx.fillStyle = '#CFE3FF'; ctx.beginPath(); ctx.moveTo(-82, -45); ctx.lineTo(-52, -90); ctx.lineTo(0, -90); ctx.lineTo(0, -45); ctx.fill();
  ctx.beginPath(); ctx.moveTo(12, -45); ctx.lineTo(12, -90); ctx.lineTo(62, -90); ctx.lineTo(95, -45); ctx.fill();
  ctx.fillStyle = '#111'; [-100, 100].forEach(w => { ctx.beginPath(); ctx.arc(w, 40, 34, 0, 7); ctx.fill(); ctx.fillStyle = '#999'; ctx.beginPath(); ctx.arc(w, 40, 14, 0, 7); ctx.fill(); ctx.fillStyle = '#111'; });
  if (wear > 0.3) { ctx.strokeStyle = '#3B3F55'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(-120, -10); ctx.lineTo(-80, 10); ctx.lineTo(-50, -5); ctx.moveTo(40, -20); ctx.lineTo(80, 5); ctx.stroke(); }
  ctx.restore();
}
function panel(ctx, y, h, label, a, accent) {
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#12164A'; rr(ctx, 50, y, 980, h, 30); ctx.fill(); ctx.strokeStyle = accent; ctx.lineWidth = 4; ctx.stroke();
  ctx.font = "800 30px 'Inter'"; const w = ctx.measureText(label).width + 50; ctx.fillStyle = accent; rr(ctx, 80, y + 26, w, 56, 28); ctx.fill(); ctx.restore();
  text(ctx, label, 105, y + 55, 30, '#fff', 800, 'left', a);
}
function draw(ctx, t) {
  ctx.fillStyle = C.dark; ctx.fillRect(0, 0, W, H);
  hook(ctx, ['Compra lo que te paga.', ['Luego, lo que quieres.', 'o']], 280, eo(prog(t, 0, .5)), { size: 72 });
  const yrs = lerp(0, 5, ease(prog(t, 3.0, 9.5)));
  // panel 1: carro
  const a1 = eo(prog(t, 0.7, 1.2));
  panel(ctx, 520, 470, 'COMPRA UN CARRO · $10.000', a1, '#D93B3B');
  stick(ctx, 220, 860, 0.8, '#fff', { arms: yrs > 4 ? 0.6 : 0.1 });
  car(ctx, 640, 900, 1.05, yrs / 5, a1);
  const v1 = 10000 * Math.pow(0.85, yrs);
  text(ctx, 'VALE HOY', 860, 640, 26, '#C9CDF2', 700, 'center', a1);
  text(ctx, fmt(v1), 860, 700, 62, '#FF6B6B', 900, 'center', a1, 'Inter Display');
  // panel 2: activo
  const a2 = eo(prog(t, 1.4, 1.9));
  panel(ctx, 1030, 470, 'COMPRA UN ACTIVO · $10.000', a2, C.green);
  stick(ctx, 220, 1370, 0.8, C.orange, { arms: yrs > 1 ? 1 : 0.2 });
  // gráfico creciente
  ctx.save(); ctx.globalAlpha = a2; ctx.strokeStyle = C.green; ctx.lineWidth = 10; ctx.lineCap = 'round'; ctx.beginPath();
  const n = Math.max(1, Math.floor(yrs / 5 * 40));
  for (let i = 0; i <= n; i++) { const yy = i / 8; const v = Math.pow(1.1, yy) * (1 + 0.03 * Math.sin(i * 1.9)); const px = 420 + i * 12, py = 1420 - (v - 1) * 300; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
  ctx.stroke(); ctx.restore();
  // monedas saliendo del activo
  if (yrs > 0.5) for (let i = 0; i < 4; i++) { const ph = (t * 0.8 + i / 4) % 1; coin(ctx, 330 + ph * 40, 1260 - ph * 120, 16, a2 * (1 - ph)); }
  const v2 = 10000 * Math.pow(1.1, yrs);
  text(ctx, 'VALE HOY*', 860, 1150, 26, '#C9CDF2', 700, 'center', a2);
  text(ctx, fmt(v2), 860, 1210, 62, C.green, 900, 'center', a2, 'Inter Display');
  // contador de años
  const ya = eo(prog(t, 2.6, 3.0));
  ctx.save(); ctx.globalAlpha = ya; ctx.fillStyle = C.orange; rr(ctx, 400, 450, 280, 60, 30); ctx.fill(); ctx.restore();
  text(ctx, `AÑO ${Math.floor(yrs + 0.001)} de 5`, 540, 481, 32, '#fff', 900, 'center', ya, 'Inter Display');
  // remate
  const m = eo(prog(t, 10.2, 10.8));
  ctx.save(); ctx.globalAlpha = m; ctx.fillStyle = C.orange; rr(ctx, 70, 1525, 940, 66, 18); ctx.fill(); ctx.restore();
  text(ctx, 'El activo te paga el carro. Al revés, no.', 540, 1559, 38, '#fff', 900, 'center', m, 'Inter Display');
  disclaimer(ctx, '*Ejemplo ilustrativo: carro pierde 15 % al año; inversión al 10 % anual (promedio histórico aprox. del S&P 500). No garantiza resultados futuros.', a2);
  socialBar(ctx, eo(prog(t, 0.5, 1.2)) * (1 - prog(t, 9.8, 10.2)));
  outro(ctx, t, DUR);
}
