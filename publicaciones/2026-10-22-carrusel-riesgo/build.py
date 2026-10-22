import pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent.resolve()
F = f"file://{D}/fonts"
LW = f"file://{D}/logo-aq-blanco-transparente.png"
LC = f"file://{D}/logo-aq-color-transparente.png"
FOTO = f"file://{D}/foto.png"
N = 7
NAR, AZ, MAR = "#F04A03", "#2A94F8", "#01005A"

FONTS = "".join(f"@font-face{{font-family:'{fam}';src:url('{F}/{f}');font-weight:{w}}}" for fam, f, w in [
    ("Inter", "Inter-Regular.ttf", 400), ("Inter", "Inter-Medium.ttf", 500), ("Inter", "Inter-SemiBold.ttf", 600),
    ("Inter", "Inter-Bold.ttf", 700), ("Inter Display", "InterDisplay-Bold.ttf", 700),
    ("Inter Display", "InterDisplay-ExtraBold.ttf", 800), ("Inter Display", "InterDisplay-Black.ttf", 900)])
BASE = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'Inter';-webkit-font-smoothing:antialiased;position:relative}
.h{font-family:'Inter Display';font-weight:800;letter-spacing:-0.022em;line-height:1.02}
.top{position:absolute;top:60px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.top img{height:76px}
.pill{font:600 20px Inter;letter-spacing:.14em;padding:12px 22px;border-radius:100px}
.foot{position:absolute;bottom:58px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.sw{display:flex;align-items:center;gap:14px;font:700 26px Inter}
.sw i{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:26px}
.handle{font:600 24px Inter}
"""

def portada():
    import random
    random.seed(11)
    # velas: suben, caen hacia el stop y rebotan
    pts=[620,600,575,590,560,540,560,600,640,670,690,660,640,610,590,560,530,500,470,450]
    velas=""; x=40
    for i,c in enumerate(pts):
        o = pts[i-1] if i else c+15
        up = c < o
        top, bot = min(o,c), max(o,c)
        col = "#ffffff" if up else "#01005A"
        velas += f'<line x1="{x+15}" y1="{top-22}" x2="{x+15}" y2="{bot+22}" stroke="{col}" stroke-width="4" opacity=".9"/>'
        velas += f'<rect x="{x}" y="{top}" width="30" height="{max(10,bot-top)}" rx="5" fill="{col}" opacity=".95"/>'
        x += 50
    return f"""<html><head><style>{BASE}
body{{background:linear-gradient(165deg,#FF7A3D 0%,{NAR} 45%,#C23A00 100%)}}
.giant{{position:absolute;top:120px;left:-24px;font:900 300px 'Inter Display';letter-spacing:-.04em;color:#ffffff14;line-height:.9;white-space:nowrap}}
.chart{{position:absolute;left:0;right:0;top:-40px}}
.stoplbl{{position:absolute;right:72px;top:{-40+700-62}px;background:#01005A;color:#fff;font:800 26px Inter;letter-spacing:.12em;padding:12px 22px;border-radius:14px}}
.txt{{position:absolute;left:72px;right:72px;bottom:170px;color:#fff;z-index:4}}
.tag{{font:700 22px Inter;letter-spacing:.16em;color:#FFE1D3;margin-bottom:22px}}
.txt .h{{font-size:86px}}
.blk{{display:inline-block;background:{MAR};color:#fff;padding:0 22px 6px;border-radius:18px;margin-top:10px}}
.pill{{color:#fff;border:2px solid #ffffff55}}
.sw i{{background:#fff;color:{NAR}}} .sw,.handle{{color:#fff}}
</style></head><body>
<div class="giant">RIESGO<br>RIESGO</div>
<svg class="chart" width="1080" height="760" viewBox="0 0 1080 760">
<line x1="40" y1="700" x2="1040" y2="700" stroke="#01005A" stroke-width="6" stroke-dasharray="22 14"/>
{velas}
</svg>
<div class="stoplbl">STOP LOSS</div>
<div class="top"><img src="{LW}"><div class="pill">1/{N}</div></div>
<div class="txt"><div class="tag">MÉTODO RCR · LA R DE RIESGO</div>
<div class="h">Antes de pensar cuánto vas a ganar, define cuánto puedes<br><span class="blk">perder.</span></div></div>
<div class="foot"><div class="sw">Desliza <i>→</i></div><div class="handle">@aqfinanzas</div></div>
</body></html>"""

def interior(k, num, titulo, cuerpo, extra="", etiqueta="MÉTODO RCR"):
    return f"""<html><head><style>{BASE}
body{{background:#FBF8F2;color:{MAR}}}
.band{{position:absolute;left:0;top:0;bottom:0;width:14px;background:{NAR}}}
.pill{{color:{MAR};border:2px solid #01005A1F;background:#fff}}
.num{{position:absolute;top:210px;left:66px;font:900 230px 'Inter Display';letter-spacing:-.05em;color:transparent;-webkit-text-stroke:4px {NAR};line-height:1}}
.cont{{position:absolute;top:470px;left:72px;right:72px}}
.cont .h{{font-size:74px;color:{MAR}}}
.cont .h em{{font-style:normal;color:{NAR}}}
.line{{width:120px;height:8px;border-radius:8px;background:{NAR};margin:36px 0 34px}}
.body{{font:500 36px/1.42 Inter;color:#3D4166}}
.body b{{color:{MAR};font-weight:700}}
.sw i{{background:{MAR};color:#fff}} .sw{{color:{MAR}}} .handle{{color:#6B7096}}
.ctr{{font:700 22px Inter;color:#6B7096;letter-spacing:.1em}}
{extra}
</style></head><body><div class="band"></div>
<div class="top"><img src="{LC}"><div class="pill">{etiqueta} · {k}/{N}</div></div>
<div class="num">{num}</div>
<div class="cont"><div class="h">{titulo}</div><div class="line"></div><div class="body">{cuerpo}</div></div>
<div class="foot"><div class="sw">Desliza <i>→</i></div><div class="handle">@aqfinanzas</div></div>
</body></html>"""

VIS_CAPITAL = """
.vis{position:absolute;left:72px;right:72px;bottom:150px;display:grid;grid-template-columns:1fr 1fr;gap:24px}
.c{border-radius:28px;padding:30px 32px;background:#fff;box-shadow:0 0 0 2px #01005A12}
.c.n{background:#01005A;color:#fff}
.c small{display:block;font:700 20px Inter;letter-spacing:.12em;color:#8A8FB3;margin-bottom:10px}
.c.n small{color:#9FB4FF}
.c b{font:800 40px 'Inter Display';letter-spacing:-.02em}
.c .bar{height:16px;border-radius:10px;background:#EEE6DA;margin-top:20px;overflow:hidden}
.c .bar span{display:block;height:100%;background:#F04A03;border-radius:10px}
"""
def vis_capital():
    return """<div class="vis">
<div class="c"><small>STOP CERCA</small><b>Más capital</b><div class="bar"><span style="width:100%"></span></div></div>
<div class="c n"><small>STOP LEJOS</small><b>Menos capital</b><div class="bar" style="background:#ffffff22"><span style="width:50%"></span></div></div></div>"""

VIS_FASES = """
.vis{position:absolute;left:72px;right:72px;bottom:140px;height:300px;background:#fff;border-radius:28px;box-shadow:0 0 0 2px #01005A12}
"""
def vis_fases():
    # precio sube por fases; el stop sube una fase por detrás
    return """<div class="vis"><svg width="936" height="300" viewBox="0 0 936 300">
<g font-family="Inter" font-weight="700" font-size="18" fill="#8A8FB3">
<text x="28" y="252">ENTRADA</text><text x="28" y="196">FASE 1</text><text x="28" y="140">FASE 2</text><text x="28" y="84">FASE 3</text></g>
<g stroke="#01005A18" stroke-width="2"><line x1="130" y1="246" x2="900" y2="246"/><line x1="130" y1="190" x2="900" y2="190"/><line x1="130" y1="134" x2="900" y2="134"/><line x1="130" y1="78" x2="900" y2="78"/></g>
<polyline points="140,250 230,230 300,240 380,186 450,200 540,132 610,150 700,90 780,104 880,60" fill="none" stroke="#2A94F8" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
<polyline points="140,286 380,286 380,246 540,246 540,190 700,190 700,134 900,134" fill="none" stroke="#F04A03" stroke-width="6" stroke-dasharray="14 10"/>
<g font-family="Inter" font-weight="700" font-size="20"><text x="760" y="168" fill="#F04A03">STOP</text><text x="760" y="40" fill="#2A94F8">PRECIO</text></g>
</svg></div>"""

def cierre():
    return f"""<html><head><style>{BASE}
body{{background:#FBF8F2;color:{MAR}}}
.band{{position:absolute;left:0;top:0;bottom:0;width:14px;background:{NAR}}}
.pill{{color:{MAR};border:2px solid #01005A1F;background:#fff}}
.cont{{position:absolute;top:230px;left:72px;right:72px}}
.chips{{display:flex;gap:18px;margin-bottom:56px}}
.chip{{flex:1;border-radius:24px;padding:26px 26px;background:#fff;box-shadow:0 0 0 2px #01005A12}}
.chip b{{display:block;font:900 54px 'Inter Display';color:#C5CBE0}}
.chip span{{font:700 24px Inter;color:#8A8FB3}}
.chip.on{{background:{NAR}}} .chip.on b,.chip.on span{{color:#fff}}
.h{{font-size:80px}} .h em{{font-style:normal;color:{NAR}}}
.sub{{font:500 34px/1.42 Inter;color:#3D4166;margin-top:30px}}
.cta{{position:absolute;left:72px;right:72px;bottom:150px;background:{MAR};border-radius:30px;padding:36px 40px;color:#fff;display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;text-align:center}}
.cta div{{font:700 26px Inter}} .cta div i{{display:block;font-style:normal;font-size:40px;margin-bottom:8px}}
.handle{{color:#6B7096}}
</style></head><body><div class="band"></div>
<div class="top"><img src="{LC}"><div class="pill">MÉTODO RCR · {N}/{N}</div></div>
<div class="cont">
<div class="chips"><div class="chip"><b>R</b><span>Rentabilidad</span></div><div class="chip"><b>C</b><span>Consistencia</span></div><div class="chip on"><b>R</b><span>Riesgo</span></div></div>
<div class="h">Invertir no es adivinar cuánto vas a ganar. Es <em>decidir cuánto estás dispuesto a perder.</em></div>
<div class="sub">El riesgo se define primero. Todo lo demás viene después.</div></div>
<div class="cta"><div><i>📌</i>Guárdalo</div><div><i>🔁</i>Compártelo</div><div><i>👤</i>Sígueme</div></div>
<div class="foot"><div></div><div class="handle">@aqfinanzas</div></div>
</body></html>"""

SLIDES = [
    portada(),
    interior(2, "!", "El error que <em>más veo</em>",
             "Comprar pensando solo en <b>cuánto puede subir</b>.<br><br>Nadie decide qué hará si baja… y cuando baja, las decisiones las toma el miedo."),
    interior(3, "01", "Tu stop loss <em>va primero</em>",
             "Antes de entrar defines el precio donde aceptas que <b>te equivocaste</b>.<br><br>Se decide con la cabeza fría, no en medio de la caída."),
    interior(4, "02", "El stop decide <em>cuánto capital</em> usas",
             "Si el stop queda lejos, entras con <b>menos capital</b>. Así una pérdida nunca te saca del juego.",
             VIS_CAPITAL).replace("</body>", vis_capital() + "</body>"),
    interior(5, "03", "No lo muevas <em>por esperanza</em>",
             "Bajar el stop “para darle más espacio” convierte una <b>pérdida pequeña</b> en una grande.<br><br>La regla se respeta, aunque duela."),
    interior(6, "04", "Después, <em>protege lo ganado</em>",
             "El stop sube <b>una fase por detrás</b> del precio. Al llegar a la Fase 1, lo llevo al punto de entrada.",
             VIS_FASES).replace("</body>", vis_fases() + "</body>"),
    cierre(),
]

out = D / "out"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, html in enumerate(SLIDES, 1):
        f = D / f"_l{i}.html"; f.write_text(html, encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"lamina-{i}.png"))
    b.close()
print("ok")
