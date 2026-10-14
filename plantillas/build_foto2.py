import pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
A = (D.parent / "assets").resolve()
F = lambda n: f"file://{A}/fotos/{n}"
LC = f"file://{A}/logo-aq-color-transparente.png"
LW = f"file://{A}/logo-aq-blanco-transparente.png"

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;position:relative}
.h{font-family:'Inter Display','Inter',sans-serif;font-weight:800;letter-spacing:-0.022em;line-height:1.02}
.o{color:#F04A03}.n{color:#01005A}
.top{position:absolute;top:60px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:9}
.top img{height:76px}
.tag{font:600 20px Inter;letter-spacing:.16em}
.handle{font:600 24px Inter}
.serif{font-family:Lora,serif}
"""
P = {}

# 1. BLANCO TOTAL
P["v1-blanco-total"] = f"""<style>{BASE}
body{{background:#fff;color:#01005A}}
.arc{{position:absolute;right:-260px;top:300px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(#F4F6FB,#E9EDF7 70%)}}
.photo{{position:absolute;right:-330px;bottom:0;height:940px;filter:drop-shadow(0 30px 50px #01005A30)}}
.txt{{position:absolute;left:72px;top:250px;width:470px;z-index:5}}
.h{{font-size:82px}} .h .o{{display:block}}
.line{{width:90px;height:6px;background:#F04A03;border-radius:3px;margin:40px 0 28px}}
.sub{{font:400 30px/1.45 Inter;color:#4A4E7A}}
.foot{{position:absolute;left:72px;bottom:64px;z-index:5}}
</style><div class="arc"></div><img class="photo" src="{F('alejandro-luminoso.png')}">
<div class="top"><img src="{LC}"><div class="tag n">EDUCACIÓN FINANCIERA</div></div>
<div class="txt"><div class="h">Invertir es una decisión,<span class="o">no una emoción.</span></div><div class="line"></div>
<div class="sub">Cuando tienes reglas claras, el miedo y la euforia dejan de decidir por ti.</div></div>
<div class="foot handle" style="color:#6B7096">@aqfinanzas</div>"""

# 2. DUOTONO AZUL
P["v2-duotono-azul"] = f"""<style>{BASE}
body{{background:linear-gradient(170deg,#2A94F8,#0F3FC4 55%,#01005A);color:#fff}}
.big{{position:absolute;left:-20px;right:-20px;top:300px;text-align:center;font:900 178px/1 'Inter Display';letter-spacing:-.04em;color:#ffffff22}}
.photo{{position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:900px}}
.box{{position:absolute;left:72px;right:72px;bottom:72px;background:#fff;border-radius:30px;padding:40px 44px;color:#01005A;box-shadow:0 30px 60px -20px #00003a99}}
.box .h{{font-size:58px}}
.box p{{font:500 26px/1.4 Inter;color:#4A4E7A;margin-top:14px}}
.tag{{color:#DCE9FF}}
</style><div class="big">PATRIMONIO</div><img class="photo" src="{F('alejandro-duotono-azul.png')}">
<div class="top"><img src="{LW}"><div class="tag">MÉTODO RCR</div></div>
<div class="box"><div class="h">El patrimonio no se improvisa. <span class="o">Se diseña.</span></div><p>Rentabilidad, Consistencia y Riesgo: las 3 preguntas antes de cada inversión.</p></div>"""

# 3. PRIMER PLANO · PRESENTACIÓN
P["v3-primer-plano-presentacion"] = f"""<style>{BASE}
body{{background:#F5F2EC;color:#01005A}}
.pic{{position:absolute;top:0;right:0;width:560px;height:1350px;background:linear-gradient(180deg,#01005A,#1D3FD0);overflow:hidden}}
.pic img{{position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:1150px}}
.pic:after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 60%,#01005Acc)}}
.name{{position:absolute;right:40px;bottom:60px;z-index:3;color:#fff;text-align:right}}
.name b{{display:block;font:800 40px 'Inter Display'}} .name span{{font:500 22px Inter;color:#C9D6FF}}
.txt{{position:absolute;left:72px;top:230px;width:400px}}
.hola{{font:italic 500 44px Lora;color:#F04A03}}
.h{{font-size:76px;margin-top:14px}}
ul{{margin-top:44px}} li{{list-style:none;font:500 27px/1.4 Inter;color:#4A4E7A;padding:18px 0;border-top:1px solid #01005A1f}}
li b{{color:#01005A}}
.foot{{position:absolute;left:72px;bottom:64px}}
.top{{right:auto}}
</style><div class="pic"><img src="{F('alejandro-traje-recortado-1500.png')}"><div class="name"><b>Alejandro Quiñones</b><span>Estratega de inversión</span></div></div>
<div class="top"><img src="{LC}"></div>
<div class="txt"><div class="hola">Hola, soy Alejandro.</div><div class="h">Te enseño a invertir <span class="o">con método.</span></div>
<ul><li><b>+15 años</b> en finanzas</li><li>Creador del <b>Método RCR</b></li><li>Autor de <b><i>La Arquitectura del Dinero</i></b></li></ul></div>
<div class="foot handle" style="color:#6B7096">@aqfinanzas</div>"""

# 4. CÍRCULO NARANJA + CREDENCIALES
P["v4-circulo-naranja"] = f"""<style>{BASE}
body{{background:#01005A;color:#fff}}
.circle{{position:absolute;left:50%;top:400px;width:760px;height:760px;margin-left:-380px;border-radius:50%;background:radial-gradient(#FF6A26,#F04A03 60%,#C93A00)}}
.ring{{position:absolute;left:50%;top:360px;width:840px;height:840px;margin-left:-420px;border-radius:50%;border:2px dashed #ffffff30}}
.mask{{position:absolute;left:50%;top:0;width:760px;height:1160px;margin-left:-380px;border-radius:0 0 380px 380px;overflow:hidden}}
.mask img{{position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:800px}}
.title{{position:absolute;top:200px;left:72px;right:72px;text-align:center}}
.title .h{{font-size:62px}}
.chips{{position:absolute;bottom:72px;left:72px;right:72px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.chip{{background:#ffffff12;border:1px solid #ffffff22;border-radius:22px;padding:22px 20px;text-align:center}}
.chip b{{display:block;font:800 34px 'Inter Display';color:#F04A03}} .chip span{{font:500 21px Inter;color:#C9D6FF}}
</style><div class="ring"></div><div class="circle"></div><div class="mask"><img src="{F('alejandro-traje-recortado-1500.png')}"></div>
<div class="top"><img src="{LW}"><div class="handle" style="color:#A9C4FF">@aqfinanzas</div></div>
<div class="title"><div class="h">Tu dinero merece <span class="o">un estratega.</span></div></div>
<div class="chips"><div class="chip"><b>+15</b><span>años en finanzas</span></div><div class="chip"><b>RCR</b><span>método propio</span></div><div class="chip"><b>Autor</b><span>La Arquitectura del Dinero</span></div></div>"""

# 5. SPLIT B/N + LISTA
P["v5-split-lista"] = f"""<style>{BASE}
body{{background:#01005A;color:#fff}}
.left{{position:absolute;left:0;top:0;bottom:0;width:470px;background:#E9E6E0;overflow:hidden}}
.left img{{position:absolute;bottom:0;left:-180px;height:1050px}}
.right{{position:absolute;left:530px;right:64px;top:210px}}
.kick{{font:700 20px Inter;letter-spacing:.18em;color:#2A94F8}}
.h{{font-size:66px;margin-top:20px}}
.item{{display:flex;gap:22px;margin-top:40px}}
.item b{{font:800 52px/1 'Inter Display';color:#F04A03;min-width:56px}}
.item div{{font:600 28px/1.35 Inter}} .item span{{display:block;font:400 22px/1.4 Inter;color:#A9B4F0;margin-top:6px}}
.top{{left:530px}}
.foot{{position:absolute;left:530px;bottom:64px;color:#A9B4F0}}
</style><div class="left"><img src="{F('alejandro-bn-contraste.png')}"></div>
<div class="top"><img src="{LW}"></div>
<div class="right"><div class="kick">ANTES DE INVERTIR</div><div class="h">3 reglas que <span class="o">sigo siempre</span></div>
<div class="item"><b>01</b><div>Define tu riesgo<span>Cuánto puedes perder sin que te afecte.</span></div></div>
<div class="item"><b>02</b><div>Ten un plan de salida<span>Antes de entrar, sabes dónde salir.</span></div></div>
<div class="item"><b>03</b><div>Sé consistente<span>Un método aplicado siempre, no a veces.</span></div></div></div>
<div class="foot handle">@aqfinanzas</div>"""

# 6. CARRUSEL CON FOTO
P["v6-carrusel-foto"] = f"""<style>{BASE}
body{{background:linear-gradient(155deg,#2A94F8,#1550D6 50%,#01005A);color:#fff}}
.num{{position:absolute;right:-40px;top:80px;font:900 900px/0.85 'Inter Display';color:transparent;-webkit-text-stroke:3px #ffffff30}}
.photo{{position:absolute;right:-250px;bottom:0;height:880px;filter:drop-shadow(0 30px 50px #00003a)}}
.txt{{position:absolute;left:72px;top:250px;width:620px}}
.kick{{font:700 20px Inter;letter-spacing:.18em;color:#CFE2FF}}
.h{{font-size:84px;margin-top:22px}}
.h .o{{display:inline-block;color:#fff;background:#F04A03;padding:2px 20px 10px;border-radius:18px;margin-top:10px}}
.swipe{{position:absolute;left:72px;bottom:64px;font:700 28px Inter;display:flex;align-items:center;gap:14px}}
.swipe span{{width:60px;height:60px;border-radius:50%;background:#fff;color:#01005A;display:flex;align-items:center;justify-content:center}}
.cnt{{font:700 22px Inter;background:#ffffff22;padding:12px 22px;border-radius:100px}}
</style><div class="num">7</div><img class="photo" src="{F('alejandro-espejo.png')}">
<div class="top"><img src="{LW}"><div class="cnt">1 / 8</div></div>
<div class="txt"><div class="kick">GUÁRDALO</div><div class="h">7 preguntas antes de comprar <span class="o">una acción</span></div></div>
<div class="swipe">Desliza <span>→</span></div>"""

# 7. OSCURO CON BORDE NARANJA
P["v7-oscuro-halo"] = f"""<style>{BASE}
body{{background:radial-gradient(ellipse 700px 800px at 50% 70%,#1a1d55,#05061C 70%);color:#fff}}
.photo{{position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:820px;filter:drop-shadow(0 0 2px #F04A03) drop-shadow(0 0 30px #F04A0388)}}
.title{{position:absolute;top:180px;left:60px;right:60px;text-align:center}}
.title .h{{font-size:110px}}
.title p{{font:400 30px Inter;color:#B9C1E8;margin-top:22px}}
.vs{{position:absolute;bottom:72px;left:72px;right:72px;display:flex;justify-content:space-between;z-index:3}}
.vs div{{background:#05061Ccc;border:1px solid #ffffff25;border-radius:20px;padding:18px 26px;font:700 26px Inter;backdrop-filter:blur(6px)}}
</style><img class="photo" src="{F('alejandro-traje-recortado-1500.png')}">
<div class="top"><img src="{LW}"><div class="tag" style="color:#8B93C4">PREGUNTA CLAVE</div></div>
<div class="title"><div class="h">¿Ahorras o <span class="o">inviertes?</span></div><p>Una de las dos te acerca a tus metas.</p></div>
<div class="vs"><div>Ahorrar: dinero quieto</div><div style="border-color:#F04A03">Invertir: dinero con método</div></div>"""

# 8. INVITACIÓN CLASE GRATUITA
P["v8-clase-gratuita"] = f"""<style>{BASE}
body{{background:#F5F7FC;color:#01005A}}
.card{{position:absolute;left:48px;right:48px;top:150px;height:880px;border-radius:40px;background:linear-gradient(160deg,#01005A,#1D3FD0);overflow:hidden}}
.card img{{position:absolute;right:-230px;bottom:0;height:820px}}
.card .t{{position:absolute;left:52px;top:60px;width:520px;color:#fff}}
.badge{{display:inline-block;font:800 22px Inter;letter-spacing:.14em;background:#F04A03;padding:12px 22px;border-radius:100px}}
.card .h{{font-size:74px;margin-top:30px}}
.card p{{font:400 28px/1.4 Inter;color:#C9D6FF;margin-top:22px}}
.bot{{position:absolute;left:72px;right:72px;bottom:72px;display:flex;justify-content:space-between;align-items:center}}
.cta{{font:800 34px 'Inter Display';background:#F04A03;color:#fff;padding:24px 36px;border-radius:22px;box-shadow:0 20px 40px -12px #F04A0399}}
.inc{{font:500 24px/1.5 Inter;color:#4A4E7A}} .inc b{{color:#01005A}}
.top{{top:44px}}
</style><div class="top"><img src="{LC}" style="height:70px"><div class="tag n">CLASE GRATUITA</div></div>
<div class="card"><img src="{F('alejandro-traje-recortado-1500.png')}"><div class="t"><span class="badge">100% GRATIS</span>
<div class="h">La ruta a tus primeros <span class="o">$200K</span></div><p>Cómo construir patrimonio invirtiendo en bolsa, paso a paso.</p></div></div>
<div class="bot"><div class="inc"><b>Incluye:</b> clase completa<br>+ Calculadora Financiera</div><div class="cta">Comenta CLASE</div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for n, h in P.items():
        f = D / f"{n}.html"; f.write_text("<html><head><meta charset='utf-8'></head><body>" + h + "</body></html>", encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(500)
        pg.screenshot(path=str(D / f"{n}.png")); print("ok", n)
    b.close()
