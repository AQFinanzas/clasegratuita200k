import pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
A = (D.parent / "assets").resolve()
IA = A / "fotos" / "ia"
def F(n):
    p = IA / n
    return f"file://{p}"
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
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
"""
P = {}

# 1 · Suéter negro · blanco total
P["post-1-decision-emocion"] = ("f1-cut.png", lambda f: f"""<style>{BASE}
body{{background:#fff;color:#01005A}}
.arc{{position:absolute;right:-300px;top:280px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(#F3F5FB,#E6EAF5 70%)}}
.photo{{position:absolute;right:-170px;bottom:0;height:1000px;filter:drop-shadow(0 30px 50px #01005A30)}}
.txt{{position:absolute;left:72px;top:250px;width:480px;z-index:5}}
.h{{font-size:84px}} .h .o{{display:block}}
.line{{width:90px;height:6px;background:#F04A03;border-radius:3px;margin:40px 0 28px}}
.sub{{font:400 30px/1.45 Inter;color:#4A4E7A}}
.foot{{position:absolute;left:72px;bottom:64px;z-index:5;color:#6B7096}}
</style><div class="arc"></div><img class="photo" src="{f}">
<div class="top"><img src="{LC}"><div class="tag n">EDUCACIÓN FINANCIERA</div></div>
<div class="txt"><div class="h">Invertir es una decisión,<span class="o">no una emoción.</span></div><div class="line"></div>
<div class="sub">Cuando tienes reglas claras, el miedo y la euforia dejan de decidir por ti.</div></div>
<div class="foot handle">@aqfinanzas</div>""")

# 2 · Camisa blanca · azul con palabra gigante
P["post-2-disciplina"] = ("f2-cut.png", lambda f: f"""<style>{BASE}
body{{background:linear-gradient(170deg,#2A94F8,#0F3FC4 55%,#01005A);color:#fff}}
.big{{position:absolute;left:0;right:0;top:250px;text-align:center;font:900 190px/1 'Inter Display';letter-spacing:-.04em;color:#ffffff24}}
.photo{{position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:1000px;filter:drop-shadow(0 30px 50px #00003a88)}}
.box{{position:absolute;left:72px;right:72px;bottom:72px;background:#fff;border-radius:30px;padding:40px 44px;color:#01005A;box-shadow:0 30px 60px -20px #00003a99}}
.box .h{{font-size:58px}}
.box p{{font:500 26px/1.4 Inter;color:#4A4E7A;margin-top:14px}}
</style><div class="big">DISCIPLINA</div><img class="photo" src="{f}">
<div class="top"><img src="{LW}"><div class="tag" style="color:#DCE9FF">MÉTODO RCR</div></div>
<div class="box"><div class="h">La disciplina le gana <span class="o">al talento.</span></div><p>En la bolsa no gana el más listo. Gana el que sigue su método todos los días.</p></div>""")

# 3 · Saco azul brazos abiertos · full bleed
P["post-3-bienvenido"] = ("f3.jpg", lambda f: f"""<style>{BASE}
body{{background:#01005A;color:#fff}}
.bg{{object-position:50% 20%}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,#01005A55 0%,transparent 22%,transparent 45%,#01005Aee 72%,#01005A 100%)}}
.txt{{position:absolute;left:72px;right:72px;bottom:150px}}
.kick{{font:700 20px Inter;letter-spacing:.18em;color:#9FC4FF}}
.h{{font-size:86px;margin-top:18px}}
.sub{{font:400 30px/1.4 Inter;color:#C9D6FF;margin-top:22px;max-width:820px}}
.foot{{position:absolute;left:72px;right:72px;bottom:64px;display:flex;justify-content:space-between;color:#A9C4FF}}
</style><img class="bg" src="{f}"><div class="shade"></div>
<div class="top"><img src="{LW}"><div class="tag" style="color:#fff">AQ FINANZAS</div></div>
<div class="txt"><div class="kick">SI ERES NUEVO POR AQUÍ</div><div class="h">Te enseño a invertir <span class="o">con método.</span></div>
<div class="sub">Sin promesas mágicas. Con reglas claras de Rentabilidad, Consistencia y Riesgo.</div></div>
<div class="foot handle"><span>Sígueme para más</span><span>@aqfinanzas</span></div>""")

# 4 · Escritorio · oscuro premium
P["post-4-prisa-metodo"] = ("f4.jpg", lambda f: f"""<style>{BASE}
body{{background:#05061C;color:#fff}}
.bg{{object-position:50% 30%}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,#05061Ccc 0%,#05061C55 25%,transparent 42%,#05061Cdd 62%,#05061C 80%)}}
.txt{{position:absolute;left:72px;right:72px;bottom:190px}}
.h{{font-size:92px}} .h .o{{display:block}}
.chips{{position:absolute;left:72px;bottom:72px;display:flex;gap:14px}}
.chips div{{border:1px solid #ffffff33;background:#ffffff10;border-radius:100px;padding:14px 24px;font:600 22px Inter}}
.chips div:first-child{{border-color:#F04A03}}
.handle{{position:absolute;right:72px;bottom:82px;color:#8B93C4}}
</style><img class="bg" src="{f}"><div class="shade"></div>
<div class="top"><img src="{LW}"><div class="tag" style="color:#8B93C4">IDEA CLAVE</div></div>
<div class="txt"><div class="h">El mercado no premia la prisa.<span class="o">Premia el método.</span></div></div>
<div class="chips"><div>Rentabilidad</div><div>Consistencia</div><div>Riesgo</div></div>""")

# 5 · Saco beige ciudad · editorial cálido
P["post-5-paso-a-paso"] = ("f5.jpg", lambda f: f"""<style>{BASE}
body{{background:#FBF8F2;color:#01005A}}
.frame{{position:absolute;left:72px;right:72px;top:170px;height:720px;border-radius:28px;overflow:hidden}}
.frame img{{width:100%;height:100%;object-fit:cover;object-position:50% 25%}}
.kick{{position:absolute;top:930px;left:72px;font:700 20px Inter;letter-spacing:.18em;color:#F04A03}}
.t{{position:absolute;top:972px;left:72px;right:72px;font:600 66px/1.1 Lora;letter-spacing:-.01em}}
.t em{{color:#F04A03}}
.foot{{position:absolute;bottom:56px;left:72px;right:72px;display:flex;justify-content:space-between;font:600 20px Inter;letter-spacing:.12em;color:#6B7096}}
.top img{{height:70px}}
</style>
<div class="top"><img src="{LC}"><div class="tag n">PATRIMONIO</div></div>
<div class="frame"><img src="{f}"></div>
<div class="kick">RECUERDA ESTO</div>
<div class="t">El patrimonio se construye <em>un paso a la vez</em>, no de un salto.</div>
<div class="foot"><div>ALEJANDRO QUIÑONES</div><div>@AQFINANZAS</div></div>""")

# 6 · Cuello tortuga B/N · cita
P["post-6-cita-paciencia"] = ("f6.jpg", lambda f: f"""<style>{BASE}
body{{background:#000;color:#fff}}
.bg{{width:780px;object-position:40% 30%;filter:grayscale(1) contrast(1.05)}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,transparent 30%,#000c 52%,#000 62%)}}
.q{{position:absolute;right:64px;top:300px;width:420px}}
.qm{{font:700 200px/0.8 Lora;color:#F04A03;height:110px}}
.qt{{font:500 60px/1.15 Lora;margin-top:20px}}
.qt em{{color:#F04A03}}
.rule{{width:90px;height:5px;background:#F04A03;border-radius:3px;margin:44px 0 24px}}
.who b{{display:block;font:800 32px 'Inter Display'}} .who span{{font:400 22px/1.5 Inter;color:#aaa}}
.handle{{position:absolute;right:72px;bottom:64px;color:#888}}
</style><img class="bg" src="{f}"><div class="shade"></div>
<div class="top"><img src="{LW}"><div class="tag" style="color:#999">CRITERIO</div></div>
<div class="q"><div class="qm">“</div><div class="qt">La paciencia también es una <em>estrategia</em> de inversión.</div>
<div class="rule"></div><div class="who"><b>Alejandro Quiñones</b><span>Estratega de inversión<br>Autor de La Arquitectura del Dinero</span></div></div>
<div class="handle handle">@aqfinanzas</div>""")

# 7 · Conferencista · portada de carrusel
P["post-7-carrusel-errores"] = ("f7.jpg", lambda f: f"""<style>{BASE}
body{{background:#01005A;color:#fff}}
.bg{{object-position:50% 15%}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,#01005A88 0%,transparent 25%,transparent 40%,#01005Af0 66%,#01005A 100%)}}
.txt{{position:absolute;left:72px;right:72px;bottom:170px}}
.kick{{font:700 20px Inter;letter-spacing:.18em;color:#CFE2FF}}
.h{{font-size:96px;margin-top:20px}}
.h .o{{display:inline-block;color:#fff;background:#F04A03;padding:2px 22px 12px;border-radius:18px;margin-top:10px}}
.cnt{{font:700 22px Inter;background:#ffffff26;padding:12px 22px;border-radius:100px}}
.swipe{{position:absolute;left:72px;bottom:64px;font:700 28px Inter;display:flex;align-items:center;gap:14px}}
.swipe span{{width:60px;height:60px;border-radius:50%;background:#fff;color:#01005A;display:flex;align-items:center;justify-content:center}}
.handle{{position:absolute;right:72px;bottom:80px;color:#CFE2FF}}
</style><img class="bg" src="{f}"><div class="shade"></div>
<div class="top"><img src="{LW}"><div class="cnt">1 / 6</div></div>
<div class="txt"><div class="kick">GUÁRDALO PARA DESPUÉS</div><div class="h">5 errores que te impiden <span class="o">invertir</span></div></div>
<div class="swipe">Desliza <span>→</span></div><div class="handle">@aqfinanzas</div>""")

# 8 · Traje sin corbata · PATRIMONIO
P["post-8-patrimonio"] = ("f8-cut.png", lambda f: f"""<style>{BASE}
body{{background:radial-gradient(ellipse 900px 900px at 50% 60%,#1D3FD0,#0A1580 45%,#01005A 80%);color:#fff}}
.big{{position:absolute;left:0;right:0;top:240px;text-align:center;font:900 178px/1 'Inter Display';letter-spacing:-.04em;color:#ffffff1f}}
.photo{{position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:980px;filter:drop-shadow(0 30px 50px #00003a)}}
.box{{position:absolute;left:72px;right:72px;bottom:72px;background:#fff;border-radius:30px;padding:40px 44px;color:#01005A;box-shadow:0 30px 60px -20px #00003a99}}
.box .h{{font-size:58px}}
.box p{{font:500 26px/1.4 Inter;color:#4A4E7A;margin-top:14px}}
</style><div class="big">PATRIMONIO</div><img class="photo" src="{f}">
<div class="top"><img src="{LW}"><div class="tag" style="color:#C9D6FF">ESTRATEGIA</div></div>
<div class="box"><div class="h">El patrimonio no se improvisa. <span class="o">Se diseña.</span></div><p>Rentabilidad, Consistencia y Riesgo: las 3 preguntas antes de cada inversión.</p></div>""")

only = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for n, (img, fn) in P.items():
        if only and not any(o in n for o in only): continue
        if not (IA / img).exists(): print("skip", n, img); continue
        f = D / f"{n}.html"; f.write_text("<html><head><meta charset='utf-8'></head><body>" + fn(F(img)) + "</body></html>", encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(500)
        pg.screenshot(path=str(D / f"{n}.png")); print("ok", n)
    b.close()
