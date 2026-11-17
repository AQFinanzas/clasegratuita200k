const DUR = 18;
function jean(ctx, x, y, s, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = '#2F5DA8'; ctx.beginPath(); ctx.moveTo(-120, -200); ctx.lineTo(120, -200); ctx.lineTo(150, 220); ctx.lineTo(30, 220); ctx.lineTo(0, -40); ctx.lineTo(-30, 220); ctx.lineTo(-150, 220); ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#244A88'; ctx.fillRect(-120, -200, 240, 40);
  ctx.strokeStyle = '#F5B34A'; ctx.lineWidth = 4; ctx.setLineDash([10, 8]); ctx.beginPath(); ctx.moveTo(-110, -140); ctx.quadraticCurveTo(-60, -90, -20, -140); ctx.moveTo(110, -140); ctx.quadraticCurveTo(60, -90, 20, -140); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#F5B34A'; ctx.beginPath(); ctx.arc(0, -180, 8, 0, 7); ctx.fill();
  // etiqueta de precio
  ctx.rotate(0.15); ctx.fillStyle = '#fff'; rr(ctx, 70, -110, 150, 70, 12); ctx.fill(); ctx.strokeStyle = C.navy; ctx.lineWidth = 4; ctx.stroke();
  ctx.fillStyle = C.navy; ctx.font = "900 44px 'Inter Display'"; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('$40', 145, -73);
  ctx.restore();
}
function clock(ctx, x, y, r, hours, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y);
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fill(); ctx.strokeStyle = C.navy; ctx.lineWidth = 12; ctx.stroke();
  // sector consumido
  ctx.fillStyle = '#F04A0333'; ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, r - 10, -Math.PI / 2, -Math.PI / 2 + (hours % 12) / 12 * Math.PI * 2 + (hours >= 12 ? 0 : 0)); ctx.fill();
  for (let i = 0; i < 12; i++) { const an = i / 12 * Math.PI * 2; ctx.fillStyle = C.navy; ctx.beginPath(); ctx.arc(Math.sin(an) * (r - 28), -Math.cos(an) * (r - 28), 6, 0, 7); ctx.fill(); }
  const ha = hours / 12 * Math.PI * 2, ma = hours * Math.PI * 2;
  ctx.strokeStyle = C.navy; ctx.lineCap = 'round'; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.sin(ha) * r * 0.5, -Math.cos(ha) * r * 0.5); ctx.stroke();
  ctx.strokeStyle = C.orange; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.sin(ma) * r * 0.75, -Math.cos(ma) * r * 0.75); ctx.stroke();
  ctx.fillStyle = C.navy; ctx.beginPath(); ctx.arc(0, 0, 12, 0, 7); ctx.fill();
  ctx.restore();
}
function card(ctx, y, a, left, right, sub) {
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#fff'; ctx.shadowColor = '#01005A22'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 12; rr(ctx, 90 + (1 - a) * 60, y, 900, 150, 26); ctx.fill(); ctx.restore();
  text(ctx, left, 140, y + 52, 40, C.navy, 800, 'left', a, 'Inter Display');
  text(ctx, sub, 140, y + 104, 28, '#6B7096', 600, 'left', a);
  text(ctx, right, 940, y + 75, 54, C.orange, 900, 'right', a, 'Inter Display');
}
function draw(ctx, t) {
  ctx.fillStyle = C.light; ctx.fillRect(0, 0, W, H);
  const p1 = 1 - prog(t, 6.6, 7.0);
  const h1 = eo(prog(t, 0, 0.5)) * (1 - prog(t, 2.6, 3.0));
  hook(ctx, ['Ese jean', 'no te costó $40'], 330, h1, { size: 96, color: C.navy });
  const h2 = eo(prog(t, 3.0, 3.5)) * p1;
  hook(ctx, ['Te costó', ['8 horas', 'o'], 'de tu vida'], 300, h2, { size: 96, color: C.navy });
  if (p1 > 0) {
    const jx = lerp(540, 340, eo(prog(t, 2.8, 3.6)));
    jean(ctx, jx, 1020, 1.25, eo(prog(t, 0.2, 0.8)) * p1);
    const ca = eo(prog(t, 3.2, 3.8)) * p1;
    const hrs = lerp(0, 8, ease(prog(t, 3.6, 6.0)));
    clock(ctx, 780, 980, 170, hrs, ca);
    text(ctx, `${Math.round(hrs)} h`, 780, 1210, 64, C.orange, 900, 'center', ca, 'Inter Display');
    const ia = eo(prog(t, 4.2, 4.7)) * p1;
    ctx.save(); ctx.globalAlpha = ia; ctx.fillStyle = C.navy; rr(ctx, 120, 1380, 840, 96, 48); ctx.fill(); ctx.restore();
    text(ctx, 'Si ganas $800 al mes, tu hora vale $5', 540, 1428, 36, '#fff', 700, 'center', ia);
  }
  // fase 2: lista
  const p2 = eo(prog(t, 6.8, 7.3)) * (1 - prog(t, 11.4, 11.8));
  if (p2 > 0) {
    hook(ctx, ['Haz la cuenta', ['con todo', 'o']], 330, p2, { size: 96, color: C.navy });
    card(ctx, 640, eo(prog(t, 7.2, 7.7)) * p2, 'Jean', '8 horas', '$40');
    card(ctx, 830, eo(prog(t, 7.9, 8.4)) * p2, 'Cena fuera', '12 horas', '$60');
    card(ctx, 1020, eo(prog(t, 8.6, 9.1)) * p2, 'Celular nuevo', '200 horas', '$1.000 · 25 días de trabajo');
    const q = eo(prog(t, 9.6, 10.1)) * p2;
    text(ctx, 'Gastar no está mal.', 540, 1290, 46, C.navy, 800, 'center', q, 'Inter Display');
    text(ctx, 'Gastar sin pensar, sí.', 540, 1360, 46, C.orange, 900, 'center', q, 'Inter Display');
  }
  // fase 3: invertir los $40
  const p3 = eo(prog(t, 11.6, 12.1));
  if (p3 > 0) {
    hook(ctx, ['¿Y si esos $40', ['los inviertes', 'o'], 'cada mes?'], 300, p3, { size: 90, color: C.navy });
    const v = 28730 * ease(prog(t, 12.4, 14.4));
    ctx.save(); ctx.globalAlpha = p3; ctx.fillStyle = C.navy; rr(ctx, 120, 760, 840, 560, 36); ctx.fill(); ctx.restore();
    text(ctx, 'En 20 años, en la bolsa de EE. UU.*', 540, 860, 36, '#C9CDF2', 600, 'center', p3);
    text(ctx, fmt(v), 540, 1000, 130, '#fff', 900, 'center', p3, 'Inter Display');
    text(ctx, 'Pusiste $9.600', 540, 1130, 36, '#C9CDF2', 600, 'center', p3);
    const q = eo(prog(t, 14.6, 15.1));
    ctx.save(); ctx.globalAlpha = q; ctx.fillStyle = C.orange; rr(ctx, 170, 1200, 740, 84, 16); ctx.fill(); ctx.restore();
    text(ctx, 'Tu dinero también puede trabajar', 540, 1242, 36, '#fff', 800, 'center', q, 'Inter Display');
    disclaimer(ctx, '*Ejemplo educativo: aporte mensual y 10 % anual (promedio histórico aprox. del S&P 500). No garantiza resultados futuros.', p3, '#6B7096');
  }
  socialBar(ctx, eo(prog(t, 0.5, 1.2)), false);
  outro(ctx, t, DUR, false);
}
