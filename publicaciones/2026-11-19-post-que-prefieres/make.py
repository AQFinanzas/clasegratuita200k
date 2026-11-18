from PIL import Image,ImageDraw,ImageFont
NAVY='#01005A';OR='#F04A03';LB='#2A94F8';BG='#F6F0E6'
F='/usr/share/fonts/opentype/inter/';f=lambda n,s:ImageFont.truetype(F+n,s);BLK='InterDisplay-Black.otf'
W,H=1080,1350;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
def ct(y,t,fo,fill,cx=W/2):
    w=d.textlength(t,font=fo);d.text((cx-w/2,y),t,font=fo,fill=fill)
ct(60,'¿QUÉ PREFIERES?',f(BLK,96),NAVY)
ct(178,'Mismo sueldo. Distinta decisión.',f('Inter-SemiBold.otf',38),'#5A587A')
def donut(cx,cy,r,inv):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=OR)
    d.pieslice((cx-r,cy-r,cx+r,cy+r),-90,-90+360*inv,fill=LB)
    d.ellipse((cx-r*0.55,cy-r*0.55,cx+r*0.55,cy+r*0.55),fill=BG)
    t=f'{int(inv*100)} %';ct(cy-40,t,f(BLK,64),LB,cx);ct(cy+28,'inviertes',f('Inter-Bold.otf',26),'#5A587A',cx)
for cx,sp,inv,yrs,lab in ((285,95,0.05,53,'A'),(795,70,0.30,25,'B')):
    d.rounded_rectangle((cx-245,270,cx+245,1060),30,fill='white')
    ct(295,'Opción '+lab,f('Inter-ExtraBold.otf',34),'#5A587A',cx)
    ct(345,f'Gastas el {sp} %',f(BLK,44),OR,cx); ct(400,f'e inviertes el {int(inv*100)} %',f(BLK,44),LB,cx)
    donut(cx,640,170,inv)
    ct(850,'y trabajas',f('Inter-Bold.otf',34),NAVY,cx)
    t=f'{yrs} años';fo=f(BLK,82);w=d.textlength(t,font=fo)
    col=OR if lab=='A' else NAVY
    d.rounded_rectangle((cx-w/2-24,905,cx+w/2+24,1015),22,fill=col);ct(912,t,fo,'white',cx)
ct(1095,'Esta decisión la tomas hoy.',f(BLK,52),NAVY)
ct(1160,'El tiempo que ganas es tuyo.',f('Inter-ExtraBold.otf',40),OR)
lg=Image.open('/home/claude/repo/logos/logo-aq-color-transparente.png').convert('RGBA');lg.thumbnail((100,100))
d.text((60,1235),'@aqfinanzas',font=f('Inter-ExtraBold.otf',30),fill=NAVY);im.paste(lg,(W-60-lg.width,1205),lg)
ct(1290,'Supuesto educativo: inversión al 7 % anual real y retiro del 4 % al año. Resultados',f('Inter-Medium.otf',17),'#8A8799')
ct(1312,'pasados no garantizan resultados futuros. No es recomendación de inversión.',f('Inter-Medium.otf',17),'#8A8799')
im.save('post.png')
