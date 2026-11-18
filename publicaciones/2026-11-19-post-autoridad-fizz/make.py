from d import *
from PIL import Image,ImageDraw,ImageFont
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
NAVY='#01005A';OR='#F04A03';LB='#2A94F8';BG='#0B0A3A';GR='#22C55E';RD='#EF4444'
F='/usr/share/fonts/opentype/inter/'; f=lambda n,s: ImageFont.truetype(F+n,s)
BLK='InterDisplay-Black.otf'
W,H=1080,1350; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
def ct(y,t,fo,fill):
    w=d.textlength(t,font=fo); d.text(((W-w)/2,y),t,font=fo,fill=fill)
ct(55,'Esto le di a mis alumnos',f(BLK,62),'white')
t='el martes 13 de octubre';fo=f(BLK,62);w=d.textlength(t,font=fo)
d.rounded_rectangle(((W-w)/2-26,138,(W+w)/2+26,226),18,fill=OR);ct(145,t,fo,'white')
ct(258,'FIZZ · National Beverage (LaCroix)',f('Inter-SemiBold.otf',34),'#B9C3FF')
# chart
s=T.index('09-01'); i0=T.index('10-13')
x=list(range(len(T)-s))
fig=plt.figure(figsize=(9.6,6.2),dpi=100); ax=fig.add_axes([0.02,0.08,0.86,0.9]); fig.patch.set_alpha(0); ax.set_facecolor((0,0,0,0))
for k,j in enumerate(range(s,len(T))):
    up=C[j]>=O[j]; col=GR if up else RD
    ax.vlines(k,L[j],Hh[j],color=col,lw=1.6); ax.add_patch(plt.Rectangle((k-0.32,min(O[j],C[j])),0.64,max(abs(C[j]-O[j]),0.04),color=col))
ki=i0-s; ax.axvline(ki,color=OR,lw=2,ls='--'); ax.axhline(C[i0],color=OR,lw=1.2,ls=':',alpha=.7)
ax.annotate('',xy=(len(x)-1,C[-1]+0.15),xytext=(ki+0.5,C[i0]+0.3),arrowprops=dict(arrowstyle='->',color='white',lw=2.5,connectionstyle='arc3,rad=-0.15'))
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(colors='#8891C9',labelsize=13); ax.yaxis.tick_right(); ax.set_xticks([0,T.index('10-01')-s,ki,T.index('11-02')-s,len(x)-1]); ax.set_xticklabels(['1 sep','1 oct','13 oct','2 nov','17 nov'])
ax.set_ylim(28.2,39.3); ax.grid(axis='y',color='#2A2A66',lw=.8)
fig.savefig('ch.png',transparent=True); plt.close(fig)
ch=Image.open('ch.png'); im.paste(ch,(40,320),ch)
d.rounded_rectangle((70,420,330,530),16,fill='#1B1A5A'); d.text((90,430),'Señal',font=f('Inter-SemiBold.otf',28),fill='#B9C3FF'); d.text((90,465),'$32,99',font=f(BLK,48),fill='white')
d.rounded_rectangle((600,730,880,840),16,fill='#1B1A5A'); d.text((620,740),'Al 17 de nov.',font=f('Inter-SemiBold.otf',28),fill='#B9C3FF'); d.text((620,775),'$37,23',font=f(BLK,48),fill='white')
t='Así va: +12,9 %';fo=f(BLK,84);w=d.textlength(t,font=fo)
d.rounded_rectangle(((W-w)/2-34,985,(W+w)/2+34,1095),24,fill=GR);ct(990,t,fo,'white')
ct(1120,'No es adivinar: es leer el gráfico con método.',f('Inter-ExtraBold.otf',34),'white')
lg=Image.open('/home/claude/repo/logos/logo-aq-blanco-transparente.png').convert('RGBA');lg.thumbnail((100,100))
d.text((60,1210),'@aqfinanzas',font=f('Inter-ExtraBold.otf',30),fill='white');im.paste(lg,(W-60-lg.width,1180),lg)
ct(1282,'Cierres diarios de FIZZ, del 13-oct al 17-nov-2026. Resultados pasados no garantizan',f('Inter-Medium.otf',17),'#8891C9')
ct(1304,'resultados futuros. Educativo, no es recomendación de inversión.',f('Inter-Medium.otf',17),'#8891C9')
im.save('post.png')
