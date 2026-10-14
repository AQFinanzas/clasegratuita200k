import pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
A = (D.parent / "assets").resolve()
LOGO_C = f"file://{A}/logo-aq-color-transparente.png"
LOGO_W = f"file://{A}/logo-aq-blanco-transparente.png"

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased}
.h{font-family:'Inter Display','Inter',sans-serif;font-weight:800;letter-spacing:-0.022em;line-height:1.02}
.o{color:#F04A03}
"""

# ---------- 1. CLARO EDUCATIVO ----------
P1 = f"""<html><head><style>{BASE}
body{{background:#F5F7FC;position:relative;color:#01005A}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#01005A0A 1px,transparent 1px),linear-gradient(90deg,#01005A0A 1px,transparent 1px);background-size:54px 54px;
 -webkit-mask-image:radial-gradient(ellipse at 50% 40%,#000 30%,transparent 80%)}}
.top{{position:absolute;top:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}}
.top img{{height:74px}}
.tag{{font:600 20px Inter;letter-spacing:.14em;color:#01005A;border:2px solid #01005A22;padding:12px 22px;border-radius:100px;background:#fff}}
.title{{position:absolute;top:200px;left:72px;right:72px;text-align:center}}
.title .h{{font-size:88px;color:#01005A}}
.title .h.big{{font-size:124px;color:#F04A03;display:inline-block;margin-top:8px;position:relative}}
.title .big:after{{content:'';position:absolute;left:4%;right:4%;bottom:6px;height:18px;background:#F04A0322;border-radius:10px;z-index:-1}}
.sub{{font:500 28px/1.4 Inter;color:#4A4E7A;margin-top:22px}}
.cards{{position:absolute;top:660px;left:72px;right:72px;display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.card{{background:#fff;border-radius:32px;padding:44px 40px;box-shadow:0 30px 60px -30px #01005A40,0 0 0 1px #01005A0D}}
.card.b{{background:linear-gradient(160deg,#01005A,#11168A);color:#fff;box-shadow:0 30px 60px -25px #01005A99}}
.ico{{width:84px;height:84px;border-radius:24px;display:flex;align-items:center;justify-content:center;margin-bottom:28px}}
.a .ico{{background:#EEF1FA}} .b .ico{{background:#F04A03}}
.card h3{{font:800 44px 'Inter Display';letter-spacing:-.02em;margin-bottom:22px}}
.card li{{list-style:none;font:500 27px/1.35 Inter;padding-left:38px;position:relative;margin-bottom:16px}}
.a li{{color:#4A4E7A}} .b li{{color:#DCE4FF}}
.card li:before{{content:'';position:absolute;left:0;top:13px;width:16px;height:16px;border-radius:50%}}
.a li:before{{background:#C5CBE0}} .b li:before{{background:#2A94F8}}
.foot{{position:absolute;bottom:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid #01005A14;padding-top:32px}}
.q{{font:800 40px 'Inter Display';letter-spacing:-.02em}}
.handle{{font:600 24px Inter;color:#6B7096}}
</style></head><body><div class="grid"></div>
<div class="top"><img src="{LOGO_C}"><div class="tag">EDUCACIÓN FINANCIERA</div></div>
<div class="title"><div class="h">Tu dinero ahorrado<br>vs. tu dinero</div><div class="h big o">invertido</div>
<div class="sub">No es cuánto ganas. Es qué haces con lo que guardas.</div></div>
<div class="cards">
 <div class="card a"><div class="ico"><svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#01005A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
  <h3>Ahorrado</h3><ul><li>Se queda quieto</li><li>La inflación le resta valor cada año</li><li>No construye patrimonio</li></ul></div>
 <div class="card b"><div class="ico"><svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg></div>
  <h3>Invertido</h3><ul><li>Trabaja con un método</li><li>Decisiones con reglas, no emociones</li><li>Crece con disciplina y tiempo</li></ul></div>
</div>
<div class="foot"><div class="q">¿Cuánto te cuesta <span class="o">no empezar?</span></div><div class="handle">@aqfinanzas</div></div>
</body></html>"""

# ---------- 2. OSCURO PREMIUM ----------
candles = ""
import random
random.seed(7)
y = 520; x = 40
for i in range(26):
    o = y; c = y + random.randint(-40, 30) - 6
    hi = min(o, c) - random.randint(10, 40); lo = max(o, c) + random.randint(10, 40)
    up = c < o
    col = "#2A94F8" if up else "#3A3F7A"
    candles += f'<line x1="{x+9}" y1="{hi}" x2="{x+9}" y2="{lo}" stroke="{col}" stroke-width="2"/><rect x="{x}" y="{min(o,c)}" width="18" height="{max(abs(o-c),6)}" rx="3" fill="{col}"/>'
    y = c; x += 40
P2 = f"""<html><head><style>{BASE}
body{{background:radial-gradient(ellipse 900px 700px at 85% 10%,#1B2A8C 0%,transparent 60%),radial-gradient(ellipse 700px 500px at 0% 100%,#F04A0326 0%,transparent 60%),#05061C;color:#fff;position:relative}}
.chart{{position:absolute;left:0;top:120px;opacity:.55}}
.fade{{position:absolute;inset:0;background:linear-gradient(180deg,transparent 30%,#05061Cdd 58%,#05061C 75%)}}
.top{{position:absolute;top:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}}
.top img{{height:80px}}
.kick{{font:600 20px Inter;letter-spacing:.18em;color:#9FB3FF}}
.body{{position:absolute;left:72px;right:72px;top:500px}}
.h{{font-size:100px}}
.h .o{{font-size:150px;display:block;margin-top:6px;letter-spacing:-.04em}}
.sub{{font:400 32px/1.4 Inter;color:#B9C1E8;margin-top:28px;max-width:820px}}
.pillars{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:56px}}
.p{{border:1px solid #ffffff1F;background:linear-gradient(180deg,#ffffff10,#ffffff04);border-radius:24px;padding:28px 26px}}
.p b{{display:block;font:800 40px 'Inter Display';letter-spacing:.16em;color:#F04A03;margin-bottom:12px}}
.p span{{font:700 30px 'Inter Display';letter-spacing:-.01em}}
.foot{{position:absolute;bottom:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}}
.pill{{font:600 26px Inter;padding:20px 32px;border-radius:100px;border:2px solid #F04A03;color:#fff}}
.pill i{{font-style:normal;color:#F04A03}}
.handle{{font:600 24px Inter;color:#8B93C4}}
</style></head><body>
<svg class="chart" width="1080" height="700">{candles}
<polyline points="40,600 200,560 360,590 520,470 680,500 840,380 1040,300" fill="none" stroke="#F04A03" stroke-opacity=".45" stroke-width="4" stroke-linejoin="round"/></svg>
<div class="fade"></div>
<div class="top"><img src="{LOGO_W}"><div class="kick">MÉTODO RCR</div></div>
<div class="body"><div class="h">Tu inversión<br>necesita un<span class="o">método.</span></div>
<div class="sub">Comprar por impulso no es una estrategia. Las reglas claras sí.</div>
<div class="pillars"><div class="p"><b>R</b><span>Rentabilidad</span></div><div class="p"><b>C</b><span>Consistencia</span></div><div class="p"><b>R</b><span>Riesgo</span></div></div></div>
<div class="foot"><div class="pill">Primero el método. <i>Después, la inversión.</i></div><div class="handle">@aqfinanzas</div></div>
</body></html>"""

# ---------- 3. CARRUSEL NÚMERO GIGANTE ----------
P3 = f"""<html><head><style>{BASE}
body{{background:linear-gradient(155deg,#2A94F8 0%,#1550D6 45%,#01005A 100%);color:#fff;position:relative}}
.num{{position:absolute;right:-60px;top:120px;font:900 1100px/0.8 'Inter Display';letter-spacing:-.06em;color:transparent;-webkit-text-stroke:3px #ffffff38}}
.glow{{position:absolute;width:700px;height:700px;right:-200px;bottom:-200px;background:radial-gradient(#F04A0355,transparent 65%)}}
.top{{position:absolute;top:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}}
.top img{{height:70px}}
.cnt{{font:700 22px Inter;background:#ffffff22;padding:12px 22px;border-radius:100px;letter-spacing:.06em}}
.body{{position:absolute;left:72px;right:200px;top:430px}}
.kick{{font:700 22px Inter;letter-spacing:.18em;color:#CFE2FF;margin-bottom:28px}}
.h{{font-size:112px}}
.h .o{{display:block;font-size:150px;margin-top:10px;color:#fff;background:#F04A03;padding:4px 28px 18px;border-radius:22px;width:max-content;letter-spacing:-.04em;box-shadow:0 30px 60px -20px #F04A03aa}}
.sub{{font:500 32px/1.4 Inter;color:#E2ECFF;margin-top:44px;max-width:640px}}
.foot{{position:absolute;bottom:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}}
.swipe{{font:700 28px Inter;display:flex;align-items:center;gap:16px}}
.swipe span{{width:64px;height:64px;border-radius:50%;background:#fff;color:#01005A;display:flex;align-items:center;justify-content:center;font-size:32px}}
.handle{{font:600 24px Inter;color:#CFE2FF}}
</style></head><body><div class="num">5</div><div class="glow"></div>
<div class="top"><img src="{LOGO_W}"><div class="cnt">1 / 6</div></div>
<div class="body"><div class="kick">GUÁRDALO PARA DESPUÉS</div>
<div class="h">5 errores que<br>te impiden<span class="o">invertir</span></div>
<div class="sub">El número 3 lo comete casi todo el mundo al empezar.</div></div>
<div class="foot"><div class="swipe">Desliza <span>→</span></div><div class="handle">@aqfinanzas</div></div>
</body></html>"""

# ---------- 4. EDITORIAL DE AUTORIDAD ----------
P4 = f"""<html><head><style>{BASE}
body{{background:#FBF8F2;color:#01005A;position:relative}}
.mast{{position:absolute;top:0;left:0;right:0;height:120px;background:#01005A;display:flex;align-items:center;justify-content:space-between;padding:0 72px}}
.mast img{{height:72px}}
.mast span{{font:600 20px Inter;letter-spacing:.2em;color:#A9B4F0}}
.qm{{position:absolute;top:170px;left:56px;font:700 380px/1 Lora;color:#F04A03}}
.quote{{position:absolute;top:430px;left:72px;right:60px;font:500 104px/1.1 Lora;letter-spacing:-.015em}}
.quote em{{font-style:italic;color:#F04A03;white-space:nowrap}}
.rule{{position:absolute;top:960px;left:72px;width:120px;height:6px;background:#F04A03;border-radius:3px}}
.who{{position:absolute;top:1000px;left:72px}}
.who b{{display:block;font:800 44px 'Inter Display';letter-spacing:-.02em}}
.who span{{display:block;font:400 28px/1.5 Inter;color:#5A5F86;margin-top:8px}}
.foot{{position:absolute;bottom:56px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #01005A22;padding-top:28px}}
.foot div{{font:600 22px Inter;letter-spacing:.12em;color:#6B7096}}
</style></head><body>
<div class="mast"><img src="{LOGO_W}"><span>CRITERIO · INVERSIÓN</span></div>
<div class="qm">“</div>
<div class="quote">Invertir sin método no es invertir. <em>Es apostar.</em></div>
<div class="rule"></div>
<div class="who"><b>Alejandro Quiñones</b><span>Estratega de inversión · Creador del Método RCR<br>Autor de <i>La Arquitectura del Dinero</i></span></div>
<div class="foot"><div>@AQFINANZAS</div><div>GUARDA ESTA IDEA</div></div>
</body></html>"""

pages = {"propuesta-1-claro-educativo": P1, "propuesta-2-oscuro-premium": P2,
         "propuesta-3-carrusel-numero": P3, "propuesta-4-editorial": P4}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for name, html in pages.items():
        f = D / f"{name}.html"; f.write_text(html, encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(D / f"{name}.png"))
        print("ok", name)
    b.close()
