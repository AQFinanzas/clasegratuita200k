const DUR = 17.5;
const BASE = 1290, SC = 1.1, FX = 540;
function waterLevel(t) {
  // nivel del agua (y); menor = más alto
  if (t < 1.4) return 960;
  if (t < 2.0) return lerp(960, 1215, eo(prog(t, 1.4, 2.0)));
  if (t < 6.0) return lerp(1215, 930, ease(prog(t, 2.2, 6.0)));
  if (t < 6.6) return lerp(930, 1215, eo(prog(t, 6.0, 6.6)));
  if (t < 9.6) return lerp(1215, 930, ease(prog(t, 6.8, 9.4)));
  if (t < 11.4) return 930;
  return lerp(930, 1500, ease(prog(t, 11.6, 13.2)));
}
function day(t) {
  if (t < 2.2) return 0; if (t < 6.0) return Math.ceil(lerp(1, 15, prog(t, 2.2, 6.0)));
  if (t < 6.8) return 0; if (t < 9.6) return Math.ceil(lerp(1, 15, prog(t, 6.8, 9.4))); return 15;
}
function draw(ctx, t) {
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#05061C'); g.addColorStop(1, '#0B0E3A'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  const wl = waterLevel(t);
  const free = eo(prog(t, 11.6, 13.0));
  const fy = BASE - free * 260;
  // suelo
  ctx.fillStyle = '#020317'; ctx.fillRect(0, 1450, W, H - 1450);
  // figura
  const payday = (t > 1.6 && t < 2.8) || (t > 6.2 && t < 7.2) || t > 12;
  stick(ctx, FX, fy, SC, '#E8ECFF', { arms: payday ? 1 : 0.15 });
  // cadenas
  const brk = prog(t, 11.4, 12.2);
  [[-1, 'DEUDAS'], [1, 'GASTOS']].forEach(([s, lab]) => {
    const ax = FX + s * 38 * SC, ay = fy + 110 * SC, bx = FX + s * 230, by = 1450;
    ctx.save(); ctx.strokeStyle = C.orange; ctx.lineWidth = 7;
    const n = 7;
    for (let i = 0; i < n; i++) {
      const p = i / n, x = lerp(ax, bx, p), y = lerp(ay, by, p) + Math.sin(p * Math.PI) * 30;
      const fly = brk > 0 && i >= 3 ? brk : 0;
      ctx.globalAlpha = 1 - fly;
      ctx.beginPath(); ctx.ellipse(x + s * fly * 120, y + fly * 160, 16, 10, Math.atan2(by - ay, bx - ax) + fly * 3, 0, 7); ctx.stroke();
    }
    ctx.restore();
    text(ctx, lab, bx, 1490, 30, C.orange, 900, 'center', 1 - brk, 'Inter Display');
  });
  // agua
  if (wl < 1460) {
    ctx.save(); ctx.globalAlpha = 0.82;
    const wg = ctx.createLinearGradient(0, wl, 0, 1450); wg.addColorStop(0, '#2A94F8'); wg.addColorStop(1, '#0F3FC4'); ctx.fillStyle = wg;
    ctx.beginPath(); ctx.moveTo(0, 1450); ctx.lineTo(0, wl);
    for (let x = 0; x <= W; x += 20) ctx.lineTo(x, wl + Math.sin(x / 70 + t * 3) * 10);
    ctx.lineTo(W, 1450); ctx.fill(); ctx.restore();
    // burbujas si está sumergido
    const headY = fy - 150 * SC;
    if (wl < headY - 40) for (let i = 0; i < 6; i++) {
      const ph = (t * 0.9 + i / 6) % 1, by = headY - ph * (headY - wl), bx = FX + 20 + Math.sin(ph * 9 + i) * 18;
      ctx.save(); ctx.globalAlpha = 0.7 * (1 - ph); ctx.strokeStyle = '#CFE3FF'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(bx, by, 6 + i % 3 * 3, 0, 7); ctx.stroke(); ctx.restore();
    }
  }
  // contador de días
  const d = day(t), ca = t < 10.2 ? eo(prog(t, 1.4, 1.8)) : 1 - prog(t, 10.2, 10.6);
  if (ca > 0) {
    const pay = d === 0 && t > 1.4;
    ctx.save(); ctx.globalAlpha = ca; ctx.font = "900 46px 'Inter Display'"; const s = pay ? '¡Llegó la quincena!' : `Día ${d} de 15`; const w = ctx.measureText(s).width + 50;
    ctx.fillStyle = pay ? C.green : C.navy; rr(ctx, W / 2 - w / 2, 640, w, 84, 42); ctx.fill(); ctx.restore();
    text(ctx, pay ? '¡Llegó la quincena!' : `Día ${d} de 15`, W / 2, 684, 46, '#fff', 900, 'center', ca, 'Inter Display');
  }
  // gancho
  const ha = eo(prog(t, 0, 0.6)) * (1 - prog(t, 9.8, 10.3));
  hook(ctx, ['Así vive quien', ['no controla', 'o'], 'su dinero'], 300, ha, { size: 92 });
  // mensajes finales
  const m1 = eo(prog(t, 10.2, 10.8)) * (1 - prog(t, 11.4, 11.8));
  hook(ctx, ['Gastas todo lo que ganas…', 'y vuelves a hundirte.'], 330, m1, { size: 70 });
  const m2 = eo(prog(t, 12.2, 12.9));
  hook(ctx, ['Rompe la cadena:', ['crea excedente', 'o'], ['e invierte', 'o']], 300, m2, { size: 86 });
  socialBar(ctx, eo(prog(t, 0.5, 1.2)));
  outro(ctx, t, DUR);
}
