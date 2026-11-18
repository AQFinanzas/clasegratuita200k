from data import M,D
from PIL import Image,ImageDraw,ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
NAVY='#01005A';OR='#F04A03';LB='#2A94F8';BG='#FFFFFF'
F='/usr/share/fonts/opentype/inter/'
def f(n,s): return ImageFont.truetype(F+n,s)
BLK='InterDisplay-Black.otf'
import os
if not os.path.exists(F+BLK): BLK='Inter-Black.otf' if os.path.exists(F+'Inter-Black.otf') else 'InterDisplay-ExtraBold.otf'
W,H=1080,1350
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
def ctext(y,t,font,fill):
    w=d.textlength(t,font=font);d.text(((W-w)/2,y),t,font=font,fill=fill)
ctext(55,'¿SE ESTÁ CAYENDO',f(BLK,82),NAVY)
t='LA BOLSA?';fo=f(BLK,96);w=d.textlength(t,font=fo)
d.rounded_rectangle(((W-w)/2-30,152,(W+w)/2+30,268),18,fill=OR);ctext(158,t,fo,'white')
ctext(292,'El S&P 500 (SPY) en los últimos…',f('Inter-SemiBold.otf',36),'#555577')
panels=[(D[227:],'1 mes',OR,'−4,0 %'),(D,'1 año',LB,'+10,5 %'),(M[-121:],'10 años',NAVY,'+232 %'),(M[-362:],'30 años',NAVY,'+864 %')]
pw,ph=470,365;x0,y0,g=60,355,20
for k,(s,lab,col,pct) in enumerate(panels):
    fig=plt.figure(figsize=(pw/100,(ph-110)/100),dpi=100);ax=fig.add_axes([0.04,0.06,0.92,0.9])
    ax.plot(range(len(s)),s,color=col,lw=4.5,solid_capstyle='round');ax.axis('off')
    if k==3: ax.plot([len(s)-1],[s[-1]],'o',color=OR,ms=13)
    fig.savefig('p.png',transparent=True);plt.close(fig)
    px=x0+(k%2)*(pw+g);py=y0+(k//2)*(ph+g)
    d.rounded_rectangle((px,py,px+pw,py+ph),22,fill='#F4F6FB')
    pc=Image.open('p.png');im.paste(pc,(px,py+95),pc)
    d.text((px+28,py+22),pct,font=f(BLK,58),fill=col if col!=LB else '#1877D6')
    lw=d.textlength(lab,font=f('Inter-Bold.otf',30));d.text((px+pw-28-lw,py+40),lab,font=f('Inter-Bold.otf',30),fill='#555577')
    if k==3:
        d.text((px+150,py+108),'Tú estás aquí →',font=f('Inter-Bold.otf',26),fill=OR)
ctext(1118,'Lo que asusta en un mes, se ve pequeño en 30 años.',f('Inter-ExtraBold.otf',33),NAVY)
ctext(1162,'Por eso invierto en EE. UU. con método.',f('Inter-ExtraBold.otf',38),OR)
lg=Image.open('/home/claude/repo/logos/logo-aq-color-transparente.png').convert('RGBA');lg.thumbnail((110,110));
d.text((60,1238),'@aqfinanzas',font=f('Inter-ExtraBold.otf',30),fill=NAVY);im.paste(lg,(W-60-lg.width,1212),lg)
n='Precio de cierre del ETF SPY al 17-nov-2026, sin dividendos. Resultados pasados no garantizan'
n2='resultados futuros. Educativo, no es recomendación de inversión.'
ctext(1296,n,f('Inter-Regular.otf' if os.path.exists(F+'Inter-Regular.otf') else 'Inter-Medium.otf',17),'#888899');ctext(1318,n2,f('Inter-Medium.otf',17),'#888899')
im.save('post.png')
