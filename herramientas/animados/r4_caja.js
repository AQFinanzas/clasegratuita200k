const DUR = 17.5;
function safe(ctx, x, y, s, open, money, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s);
  // cuerpo
  ctx.fillStyle = '#3B4170'; rr(ctx, -260, -280, 520, 560, 34); ctx.fill();
  ctx.fillStyle = '#1C2050'; rr(ctx, -220, -240, 440, 480, 20); ctx.fill();
  // billetes adentro
  const n = 7;
  for (let i = 0; i < n; i++) bill(ctx, 0, 190 - i * 46, 330, clamp(money * n - i) * 0.95 + 0.05 * (money > 0), 0);
  // puerta abierta
  ctx.save(); ctx.translate(230, -260);
  const ow = lerp(440, 120, open);
  ctx.fillStyle = '#4C5389'; rr(ctx, 0, 0, ow, 520, 20); ctx.fill();
  ctx.fillStyle = '#AEB4E0'; ctx.beginPath(); ctx.arc(ow / 2, 260, 40 * (1 - open * 0.6) + 10, 0, 7); ctx.fill();
  ctx.restore();
  // patas
  ctx.fillStyle = '#2A2F5E'; rr(ctx, -220, 280, 70, 30, 8); ctx.fill(); rr(ctx, 150, 280, 70, 30, 8); ctx.fill();
  ctx.restore();
}
function draw(ctx, t) {
  ctx.fillStyle = C.cream; ctx.fillRect(0, 0, W, H);
  const ph1 = 1 - eo(prog(t, 9.4, 10.0));
  const ha = eo(prog(t, 0, 0.6)) * ph1;
  hook(ctx, ['Guardaste', ['$10.000', 'o'], 'en efectivo'], 300, ha, { size: 92, color: C.navy });
  const yr = Math.floor(lerp(0, 10, prog(t, 2.2, 7.6)));
  const val = 10000 / Math.pow(1.03, lerp(0, 10, prog(t, 2.2, 7.6)));
  if (ph1 > 0) {
    safe(ctx, 540, 1000, 0.82, eo(prog(t, 0.8, 1.6)), val / 10000 * 0.98 + 0.02, ph1);
    // contador de años
    const ya = eo(prog(t, 1.8, 2.2)) * ph1;
    ctx.save(); ctx.globalAlpha = ya; ctx.fillStyle = C.navy; rr(ctx, 380, 680, 320, 84, 42); ctx.fill(); ctx.restore();
    text(ctx, `AÑO ${yr}`, 540, 724, 46, '#fff', 900, 'center', ya, 'Inter Display');
    // valor
    const va = eo(prog(t, 2, 2.4)) * ph1;
    text(ctx, 'Lo que puedes comprar con ellos:', 540, 1330, 34, C.navy, 600, 'center', va);
    text(ctx, fmt(val), 540, 1410, 92, val < 9000 ? C.orange : C.navy, 900, 'center', va, 'Inter Display');
    const m = eo(prog(t, 7.8, 8.3)) * ph1;
    ctx.save(); ctx.globalAlpha = m; ctx.fillStyle = C.navy; rr(ctx, 110, 1480, 860, 92, 18); ctx.fill(); ctx.restore();
    text(ctx, 'El dinero quieto también se gasta.', 540, 1527, 40, '#fff', 800, 'center', m, 'Inter Display');
  }
  // fase 2: comparación
  const p2 = eo(prog(t, 9.8, 10.4));
  if (p2 > 0) {
    hook(ctx, ['¿Y si los hubieras', ['invertido?', 'o']], 330, p2, { size: 90, color: C.navy });
    // tarjeta izquierda
    ctx.save(); ctx.globalAlpha = p2; ctx.fillStyle = '#fff'; rr(ctx, 70, 640, 440, 820, 30); ctx.fill(); rr(ctx, 570, 640, 440, 820, 30); ctx.fillStyle = C.navy; ctx.fill(); ctx.restore();
    safe(ctx, 255, 960, 0.42, 0.75, 0.75, p2);
    text(ctx, 'Guardados', 290, 1230, 36, C.navy, 800, 'center', p2);
    text(ctx, '$7.441', 290, 1310, 70, C.orange, 900, 'center', p2, 'Inter Display');
    text(ctx, 'de poder de compra', 290, 1370, 26, '#6B7096', 600, 'center', p2);
    // gráfico derecha
    const cp = ease(prog(t, 10.6, 13.4));
    ctx.save(); ctx.globalAlpha = p2; ctx.strokeStyle = '#ffffff22'; ctx.lineWidth = 2;
    for (let i = 0; i < 5; i++) { ctx.beginPath(); ctx.moveTo(610, 760 + i * 80); ctx.lineTo(970, 760 + i * 80); ctx.stroke(); }
    ctx.strokeStyle = C.blue; ctx.lineWidth = 10; ctx.lineCap = 'round'; ctx.beginPath();
    const pts = []; for (let i = 0; i <= 50; i++) { const yy = i / 5; const v = 10000 * Math.pow(1.1, yy) * (1 + 0.04 * Math.sin(i * 1.7)); pts.push([610 + i / 50 * 360, 1080 - (v - 10000) / 16000 * 330]); }
    const k = Math.max(1, Math.floor(cp * 50));
    pts.slice(0, k + 1).forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.stroke();
    const lp = pts[k]; ctx.fillStyle = C.orange; ctx.beginPath(); ctx.arc(lp[0], lp[1], 14, 0, 7); ctx.fill(); ctx.restore();
    const v2 = 10000 * Math.pow(1.1, cp * 10);
    text(ctx, 'Invertidos en la', 790, 1180, 30, '#C9CDF2', 600, 'center', p2);
    text(ctx, 'bolsa de EE. UU.*', 790, 1222, 34, '#fff', 800, 'center', p2);
    text(ctx, fmt(v2), 790, 1310, 70, C.blue, 900, 'center', p2, 'Inter Display');
    text(ctx, 'en 10 años', 790, 1370, 26, '#C9CDF2', 600, 'center', p2);
    const m3 = eo(prog(t, 13.6, 14.2));
    ctx.save(); ctx.globalAlpha = m3; ctx.fillStyle = C.orange; rr(ctx, 110, 1490, 860, 92, 18); ctx.fill(); ctx.restore();
    text(ctx, 'Tu dinero tiene que trabajar.', 540, 1537, 44, '#fff', 900, 'center', m3, 'Inter Display');
    disclaimer(ctx, '*Ejemplo educativo: inflación 3 % anual y 10 % anual (promedio histórico aprox. del S&P 500). No garantiza resultados futuros.', p2, '#6B7096');
  }
  socialBar(ctx, eo(prog(t, 0.5, 1.2)) * (1 - prog(t, 7.6, 7.9)) + prog(t, 14.8, 15.2) * 0, false);
  outro(ctx, t, DUR, false);
}
