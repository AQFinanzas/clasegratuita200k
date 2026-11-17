const DUR = 17.5;
const T = [['AAPL', -1.5], ['NVDA', -9.0], ['TSLA', -10.8], ['META', -3.9], ['MSFT', -3.6], ['AMZN', -2.2], ['GOOGL', -2.2]];
const POS = [[200, 760], [540, 760], [880, 760], [140, 1010], [400, 1010], [680, 1010], [940, 1010]];
function tile(ctx, x, y, s, a, rot, sym, pct, red) {
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  ctx.fillStyle = '#fff'; ctx.shadowColor = '#00000055'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 10; rr(ctx, -115, -85, 230, 150, 24); ctx.fill();
  ctx.shadowColor = 'transparent'; ctx.strokeStyle = red ? '#D93B3B' : C.green; ctx.lineWidth = 6; rr(ctx, -115, -85, 230, 150, 24); ctx.stroke();
  ctx.fillStyle = C.navy; ctx.font = "900 50px 'Inter Display'"; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(sym, 0, -12);
  ctx.fillStyle = red ? '#D93B3B' : C.green; rr(ctx, -80, 80, 160, 52, 26); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = "800 30px 'Inter'"; ctx.fillText((pct > 0 ? '+' : '') + pct.toFixed(1).replace('.', ',') + ' %', 0, 107);
  ctx.restore();
}
function draw(ctx, t) {
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#0B0E3A'); g.addColorStop(1, C.dark); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  // fase 1: día rojo
  const p1 = 1 - prog(t, 7.2, 7.7);
  hook(ctx, ['Si las 7 gigantes de EE. UU.', ['caen el mismo día', 'o'], '¿qué haces?'], 290, eo(prog(t, 0, .5)) * p1, { size: 76 });
  if (p1 > 0) {
    T.forEach(([s, p], i) => {
      const a = eo(prog(t, 0.6 + i * 0.25, 1.0 + i * 0.25)) * p1;
      const shake = t > 2.8 && t < 3.6 ? Math.sin(t * 60 + i) * 4 : 0;
      tile(ctx, POS[i][0] + shake, POS[i][1], i < 3 ? 1.15 : 1.0, a, (i % 2 ? 0.05 : -0.04) * (i > 2), s, p, true);
    });
    const ca = eo(prog(t, 2.8, 3.3)) * p1;
    ctx.save(); ctx.globalAlpha = ca; ctx.fillStyle = '#1B1E4A'; rr(ctx, 90, 1210, 900, 190, 26); ctx.fill(); ctx.strokeStyle = '#D93B3B'; ctx.lineWidth = 4; ctx.stroke(); ctx.restore();
    text(ctx, 'LA MAYORÍA…', 540, 1270, 34, '#C9CDF2', 800, 'center', ca);
    text(ctx, 'Vende por miedo', 540, 1340, 64, '#FF6B6B', 900, 'center', ca, 'Inter Display');
    const n = eo(prog(t, 4.0, 4.4)) * p1;
    text(ctx, 'Ejemplo ilustrativo de un día de caída', 540, 1450, 26, '#8A90C0', 600, 'center', n);
  }
  // fase 2: lo que pasó después (S&P 500)
  const p2 = eo(prog(t, 7.5, 8.0));
  if (p2 > 0) {
    hook(ctx, ['Las caídas son', ['parte del camino', 'o']], 300, p2, { size: 84 });
    text(ctx, 'S&P 500 · variación de cada año', 540, 640, 34, '#C9CDF2', 700, 'center', p2);
    const data = [['2022', -19.4], ['2023', 24.2], ['2024', 23.3]];
    const base = 1020, sc = 12;
    ctx.save(); ctx.globalAlpha = p2; ctx.strokeStyle = '#ffffff44'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(150, base); ctx.lineTo(930, base); ctx.stroke(); ctx.restore();
    data.forEach(([y, v], i) => {
      const bp = ease(prog(t, 8.3 + i * 0.9, 9.1 + i * 0.9)); const x = 260 + i * 280, h = Math.abs(v) * sc * bp;
      ctx.save(); ctx.globalAlpha = p2; ctx.fillStyle = v < 0 ? '#D93B3B' : C.green; rr(ctx, x - 80, v < 0 ? base : base - h, 160, Math.max(1, h), 14); ctx.fill(); ctx.restore();
      text(ctx, (v > 0 ? '+' : '') + v.toFixed(1).replace('.', ',') + ' %', x, v < 0 ? base + h + 50 : base - h - 45, 46, v < 0 ? '#FF6B6B' : C.green, 900, 'center', bp, 'Inter Display');
      text(ctx, y, x, v < 0 ? base - 40 : base + 45, 34, '#fff', 800, 'center', p2);
    });
    const m = eo(prog(t, 11.6, 12.2));
    ctx.save(); ctx.globalAlpha = m; ctx.fillStyle = C.orange; rr(ctx, 90, 1370, 900, 170, 24); ctx.fill(); ctx.restore();
    text(ctx, 'El que vendió por miedo, se lo perdió.', 540, 1425, 40, '#fff', 800, 'center', m, 'Inter Display');
    text(ctx, 'El método te dice qué hacer.', 540, 1490, 44, '#fff', 900, 'center', m, 'Inter Display');
    disclaimer(ctx, 'Variación anual del precio del S&P 500 (sin dividendos). Fines educativos. Resultados pasados no garantizan resultados futuros.', p2);
  }
  socialBar(ctx, eo(prog(t, 0.5, 1.2)) * (1 - prog(t, 11.3, 11.6)));
  outro(ctx, t, DUR);
}
