const DUR = 1.8;
window.MODE = 'hook1';
function draw(ctx, t) {
  ctx.clearRect(0, 0, W, H);
  if (MODE === 'outro') { outro(ctx, DUR - 0.01 + 0 * t + (t - DUR + 0.01) , DUR); return; }
  const g = ctx.createLinearGradient(0, 120, 0, 700); g.addColorStop(0, '#000000aa'); g.addColorStop(1, '#00000000'); ctx.fillStyle = g; ctx.fillRect(0, 120, W, 600);
  if (MODE === 'hook1') hook(ctx, ['Así se construye', ['un patrimonio', 'o']], 330, 1, { size: 92 });
  if (MODE === 'hook2') hook(ctx, ['Capa por capa.', ['Mes a mes.', 'o']], 330, 1, { size: 96 });
  const g2 = ctx.createLinearGradient(0, 1500, 0, 1720); g2.addColorStop(0, '#00000000'); g2.addColorStop(1, '#000000aa'); ctx.fillStyle = g2; ctx.fillRect(0, 1500, W, 220);
  socialBar(ctx, 1);
}
