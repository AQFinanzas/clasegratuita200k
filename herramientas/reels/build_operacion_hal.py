import json, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V = '/mnt/user-data/uploads/Downloads/sesion-111-15oct.mp4'
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
FX = '/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'
OR, NAVY = (240, 74, 3), (1, 0, 90)
def run(c): subprocess.run(c, check=True)

# Segmentos (inicio, fin, franja superior)
SEG = [
  (869.3, 875.6, ['+6,3 %', 'SOBRE MI CAPITAL']),
  (1018.4, 1028.9, ['NO ES ADRENALINA', 'ES ARMAR LA OPERACIÓN']),
  (1068.2, 1091.0, ['MI STOP LOSS:', '2.ª O 3.ª CAPA DE PROTECCIÓN']),
  (2068.6, 2075.6, ['CONFÍA EN EL MÉTODO', 'Y APLÍCALO']),
  (2131.6, 2139.7, ['CON APALANCAMIENTO', 'ACELERO LA GANANCIA']),
]
STILL = 1022  # el primer tramo muestra Quantfury con saldo: usamos el gráfico congelado

def band(lines, path, big_first=False):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = 250
    for i, l in enumerate(lines):
        size = 120 if (big_first and i == 0) else 64
        f = ImageFont.truetype(FB, size); w = d.textlength(l, font=f)
        if i == len(lines) - 1 and not (big_first and i == 0):
            d.rounded_rectangle((540 - w / 2 - 22, y - 6, 540 + w / 2 + 22, y + size + 14), 16, fill=OR + (255,))
        d.text((540 - w / 2, y), l, font=f, fill=(255, 255, 255, 255), stroke_width=0 if i == len(lines) - 1 else 3, stroke_fill=(0, 0, 0, 160))
        y += size + 26
    # franja "sesión en vivo"
    f2 = ImageFont.truetype(FX, 30); s = 'SESIÓN EN VIVO CON MIS ALUMNOS · DINERO REAL'
    w = d.textlength(s, font=f2); d.rounded_rectangle((540 - w / 2 - 20, 1500, 540 + w / 2 + 20, 1550), 25, fill=NAVY + (235,))
    d.text((540 - w / 2, 1508), s, font=f2, fill=(255, 255, 255, 255))
    im.save(path)

def seg_video(i, a, b, lines):
    band(lines, f'band{i}.png', big_first=(i == 0))
    src = ['-loop', '1', '-i', 'still.png'] if i == 0 else ['-ss', str(a), '-t', str(b - a), '-i', V]
    loop = []
    # recorte del gráfico y desenfoques (encabezado/leyendas con precios, ejes de precio y de horas)
    fc = (
      "[0:v]split=3[s0][s1][s2];"
      "[s0]crop=1130:765:40:235,gblur=sigma=30,scale=-2:1920,crop=1080:1920,eq=brightness=-0.35[bg];"
      "[s1]crop=1130:765:40:235[c];"
      "[c]split=4[c0][c1][c2][c3];"
      "[c1]crop=1130:195:0:0,gblur=sigma=14[b1];"
      "[c2]crop=75:765:1055:0,gblur=sigma=14[b2];"
      "[c3]crop=1130:55:0:710,gblur=sigma=14[b3];"
      "[c0][b1]overlay=0:0[c4];[c4][b2]overlay=1055:0[c5];[c5][b3]overlay=0:710,scale=1080:-2[ch];"
      "[s2]crop=240:130:1680:0,scale=480:260[cam];"
      "[bg][ch]overlay=0:760[v1];[v1]drawbox=x=296:y=476:w=488:h=268:color=white:t=fill[v2];[v2][cam]overlay=300:480[v3];"
      "[v3][1:v]overlay=0:0,fps=30,format=yuv420p[v]"
    )
    dur = b - a
    cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + loop + src + ['-loop', '1', '-i', f'band{i}.png']
    if i == 0:
        cmd += ['-ss', str(a), '-t', str(dur), '-i', V]
        cmd += ['-filter_complex', fc, '-map', '[v]', '-map', '2:a', '-t', str(dur)]
    else:
        cmd += ['-filter_complex', fc, '-map', '[v]', '-map', '0:a', '-t', str(dur)]
    cmd += ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-ar', '48000', '-ac', '2', f'seg{i}.mp4']
    run(cmd)

def subs():
    r = json.load(open('t111.json'))
    W = [(w['start'] + 840, w['end'] + 840, w['word'].strip()) for s in r['segments'] for w in s['words']]
    fix = {'aliburton': 'Halliburton', 'aliburto': 'Halliburton', 'jali': 'Halli', 'burton': 'burton', 'plos': 'loss', 'esto': 'esto', 'confí': 'confía', 'estoplos': 'stop loss'}
    ev = []; off = 0.0
    for (a, b, _) in SEG:
        ws = [w for w in W if a <= w[0] < b]
        # palabras: arreglos de transcripción
        out = []
        for k, (s, e, t) in enumerate(ws):
            tl = t.lower().strip('.,')
            if tl == 'esto' and k + 1 < len(ws) and ws[k + 1][2].lower().startswith('plos'): t = 'stop'
            elif tl == 'plos': t = 'loss'
            elif tl in fix: t = fix[tl]
            out.append((s - a + off, min(e, b) - a + off, t))
        for j in range(0, len(out), 3):
            ch = out[j:j + 3]; ev.append((ch[0][0], ch[-1][1] + 0.05, ' '.join(c[2] for c in ch)))
        off += b - a
    def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
    hdr = """[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Inter Display Black,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,2,2,60,60,230,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f'Dialogue: 0,{ts(s)},{ts(e)},S,,0,0,0,,{t}' for s, e, t in ev]
    open('subs.ass', 'w').write(hdr + '\n'.join(lines))
    return off

def cards():
    q = Image.open('qf.png').convert('RGB').crop((160, 365, 1520, 700))
    for box in [(20, 165, 270, 200), (20, 210, 560, 270), (20, 285, 430, 330)]:
        r = q.crop(box).filter(ImageFilter.GaussianBlur(14)); q.paste(r, box[:2])
    q = q.resize((1000, int(335 * 1000 / 1360)))
    def card(main, sub, extra, path, show_q):
        im = Image.new('RGB', (1080, 1920), (5, 6, 28)); d = ImageDraw.Draw(im)
        if show_q: im.paste(q, (40, 560)); d.rounded_rectangle((40, 560, 1040, 560 + q.height), 18, outline=(255, 255, 255), width=4)
        y = 900 if show_q else 640
        f = ImageFont.truetype(FB, 150); w = d.textlength(main, font=f); d.text((540 - w / 2, y), main, font=f, fill=OR)
        f2 = ImageFont.truetype(FB, 54)
        for k, s in enumerate(sub):
            w = d.textlength(s, font=f2); d.text((540 - w / 2, y + 190 + k * 70), s, font=f2, fill=(255, 255, 255))
        f3 = ImageFont.truetype(FX, 26)
        for k, s in enumerate(extra):
            w = d.textlength(s, font=f3); d.text((540 - w / 2, 1560 + k * 40), s, font=f3, fill=(170, 176, 214))
        im.save(path)
    card('+0,56 %', ['SOBRE LA POSICIÓN', 'OPERACIÓN EN CORTO · HAL'], [], 'card1.png', True)
    card('≈ 11×', ['MI POSICIÓN ≈ 11 VECES MI CAPITAL', 'CON APALANCAMIENTO'], ['EL APALANCAMIENTO TAMBIÉN MULTIPLICA LAS PÉRDIDAS'], 'card2.png', False)
    card('+6,3 %', ['SOBRE MI CAPITAL', 'EN 24 MINUTOS'], ['RESULTADO PASADO, NO GARANTIZA RESULTADOS FUTUROS', 'EL APALANCAMIENTO TAMBIÉN MULTIPLICA LAS PÉRDIDAS'], 'card3.png', False)
    for i, (p, d) in enumerate([('card1.png', 2.6), ('card2.png', 2.6), ('card3.png', 3.2)]):
        run(['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-t', str(d), '-i', p, '-f', 'lavfi', '-t', str(d), '-i', 'anullsrc=r=48000:cl=stereo',
             '-vf', 'fps=30,format=yuv420p,fade=in:st=0:d=0.25', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-shortest', f'cardv{i}.mp4'])

if __name__ == '__main__':
    for i, (a, b, l) in enumerate(SEG): seg_video(i, a, b, l)
    total = subs()
    open('segs.txt', 'w').write(''.join(f'file seg{i}.mp4\n' for i in range(len(SEG))))
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-i', 'segs.txt', '-vf', 'subtitles=subs.ass:fontsdir=/usr/share/fonts/opentype/inter', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-ar', '48000', 'talk.mp4'])
    cards()
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/home/claude/anim/r1_outro.mp4', '-f', 'lavfi', '-t', '1.8', '-i', 'anullsrc=r=48000:cl=stereo', '-c:v', 'copy', '-c:a', 'aac', '-shortest', 'outro.mp4'])
    open('all.txt', 'w').write('file talk.mp4\nfile cardv0.mp4\nfile cardv1.mp4\nfile cardv2.mp4\nfile outro.mp4\n')
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-i', 'all.txt', '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-ar', '48000', 'hal_novoz_mix.mp4'])
    print('total talk', total)
