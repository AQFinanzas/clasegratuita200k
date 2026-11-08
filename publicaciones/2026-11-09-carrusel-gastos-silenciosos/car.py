from playwright.sync_api import sync_playwright
CSS='''@font-face{font-family:Cav;src:url(cav.woff2)}@font-face{font-family:PM;src:url(pm.woff2)}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden}
body{background:#E9E4DA;font-family:Inter;color:#01005A;position:relative}
body:before{content:"";position:absolute;inset:0;background:radial-gradient(#00000010 1px,transparent 1.3px) 0 0/6px 6px,linear-gradient(160deg,#F2EEE6,#DDD6C9)}
.top{position:absolute;top:56px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.top img{height:66px}.pg{font:600 22px Inter;color:#6A6C8C;letter-spacing:.1em}
.note{position:absolute;background:linear-gradient(180deg,#FFE97A,#FFDF4F);box-shadow:0 30px 40px -18px #0005,0 2px 4px #0002;padding:70px 64px}
.note:after{content:"";position:absolute;right:0;bottom:0;width:70px;height:70px;background:linear-gradient(315deg,#E9E4DA 50%,#E8C93A 50%);box-shadow:-4px -4px 8px #0001}
.note.dk:after{background:linear-gradient(315deg,#01005A 50%,#E8C93A 50%)}
.tape{position:absolute;top:-26px;left:50%;width:180px;height:52px;margin-left:-90px;background:#ffffff99;transform:rotate(-3deg);box-shadow:0 1px 3px #0002}
.hand{font-family:Cav;color:#1B1B3A;line-height:1.02}
.mk{font-family:PM;color:#F04A03}
.card{position:absolute;left:72px;right:72px;background:#fff;border-radius:18px;padding:40px 46px;box-shadow:0 14px 30px -16px #0003}
.card .k{font:700 20px Inter;letter-spacing:.14em;color:#F04A03}
.card .t{font:500 31px/1.4 Inter;color:#22244A;margin-top:12px}
.card b{color:#01005A}
.math{font:800 40px 'Inter Display';color:#01005A;margin-top:18px;letter-spacing:-.01em}
.math span{color:#F04A03}
.foot{position:absolute;bottom:48px;left:72px;right:72px;display:flex;justify-content:space-between;font:600 22px Inter;color:#6A6C8C}
.sw{font:700 24px Inter;color:#01005A}
'''
def head(n,tot=7):
    return f'<div class="top"><img src="lc.png"><div class="pg">{n:02d} / {tot:02d}</div></div>'
slides=[]
slides.append(head(1)+'''
<div class="note" style="left:110px;top:230px;width:860px;height:760px;transform:rotate(-2.2deg)"><div class="tape"></div>
<div class="hand" style="font-size:132px">5 gastos<br>silenciosos</div>
<div class="hand" style="font-size:78px;margin-top:26px">que se comen tu</div>
<div class="mk" style="font-size:104px;margin-top:6px">excedente</div></div>
<div style="position:absolute;left:72px;right:72px;top:1080px;font:500 32px/1.4 Inter;color:#22244A">No es que ganes poco.<br>Es que se te va por <b style="color:#F04A03">huecos que no ves.</b></div>
<div class="foot"><span>@aqfinanzas</span><span class="sw">Desliza →</span></div>''')
items=[
 ('Suscripciones<br>que ya no usas','Streaming, apps, la prueba "gratis" que nunca cancelaste. Se cobran solas, todos los meses.','3 apps de $15 al mes =','$540 al año'),
 ('Cuota de manejo<br>y comisiones','La cuenta, la tarjeta, el retiro en otro cajero. Pequeño cada vez, constante siempre.','$12 al mes en cobros =','$144 al año'),
 ('Pagar solo<br>el mínimo','La tarjeta te deja "al día", pero los intereses siguen corriendo sobre todo lo demás.','Pagas el mínimo y la deuda','casi no baja'),
 ('El antojo<br>de todos los días','El café, el snack, el "solo es un momento". No se siente porque es poquito.','$4 x 22 días x 12 meses =','$1.056 al año'),
 ('Domicilios<br>por costumbre','Envío, propina, tarifa de servicio y el pedido mínimo que te hace comprar de más.','$6 extra x 2 pedidos x 52 semanas =','$624'),
]
rots=[2,-1.6,1.8,-2.2,1.4]
for i,(t,d,m1,m2) in enumerate(items):
    slides.append(head(i+2)+f'''
<div class="note" style="left:150px;top:210px;width:780px;height:560px;transform:rotate({rots[i]}deg)"><div class="tape"></div>
<div class="mk" style="font-size:120px;line-height:1">{i+1}</div>
<div class="hand" style="font-size:96px;margin-top:20px">{t}</div></div>
<div class="card" style="top:850px"><div class="k">POR QUÉ DUELE</div><div class="t">{d}</div>
<div class="math">{m1} <span>{m2}</span></div></div>
<div class="foot"><span>@aqfinanzas</span><span class="sw">→</span></div>''')
slides.append(head(7)+'''
<div style="position:absolute;inset:0;background:#01005A"></div>
<div class="top" style="z-index:6"><img src="lb.png"><div class="pg" style="color:#9FC4FF">07 / 07</div></div>
<div style="position:absolute;left:72px;right:72px;top:250px;color:#fff;font:900 84px/1 'Inter Display';letter-spacing:-.03em">Ese dinero no<br>desaparece.<br><span style="color:#F04A03">Es tu excedente<br>perdido.</span></div>
<div style="position:absolute;left:72px;right:110px;top:720px;color:#C9CDEB;font:500 32px/1.45 Inter">Recupéralo, ponle un destino y deja que trabaje para ti, con método y sin promesas mágicas.</div>
<div class="note dk" style="left:500px;top:930px;width:480px;height:270px;padding:44px 46px;transform:rotate(-3deg)"><div class="tape"></div>
<div class="hand" style="font-size:58px">Hoy: abre tu extracto y tacha 1 gasto.</div></div>
<div class="foot" style="color:#9FC4FF"><span>Guárdalo · @aqfinanzas</span><span></span></div>''')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(slides,1):
        open('s.html','w').write(f'<html><head><style>{CSS}</style></head><body>{s}</body></html>')
        pg.goto('file:///home/claude/posts3/s.html'); pg.wait_for_timeout(500); pg.screenshot(path=f'c{i}.png')
    b.close()
