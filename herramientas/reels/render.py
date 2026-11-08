# Motor de render del reel AQ (Pillow fotograma a fotograma)
import json, subprocess, sys, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
NAR = (240, 74, 3); AZ = (42, 148, 248); MAR = (1, 0, 90); BL = (255, 255, 255); NG = (10, 10, 10)
FD = '/home/claude/reels/inter/extras/ttf/'
def font(name, size): return ImageFont.truetype(FD + name, size)
F_BLACK = lambda s: font('InterDisplay-Black.ttf', s)
F_XB = lambda s: font('InterDisplay-ExtraBold.ttf', s)
F_B = lambda s: font('Inter-Bold.ttf', s)

cfg = json.load(open(sys.argv[1]))
words = cfg['words']            # [{w,s,e,key}]
groups = cfg['groups']          # [[i0,i1], ...] índices de palabras por subtítulo
events = cfg['events']          # gráficos
N = cfg['nframes']
base = cfg['base']; matte = cfg['matte']; out = cfg['out']

def easeOutBack(x, s=1.70158):
    x = min(max(x, 0), 1); x -= 1; return x * x * ((s + 1) * x + s) + 1
def easeOut(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def rr(d, box, r, fill): d.rounded_rectangle(box, r, fill=fill)

# ---------- íconos de línea ----------
def icon(name, size=120, fg=None, acc=None):
    S = 4; im = Image.new('RGBA', (size * S, size * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = 7 * S; c = tuple(fg) if fg else BL; a = tuple(acc) if acc else (NAR if c != NAR else MAR); z = size * S
    def L(*p, col=c): d.line([q * S for q in p], fill=col, width=w, joint='curve')
    if name == 'phone':
        d.rounded_rectangle([z*.3, z*.08, z*.7, z*.92], 14*S, outline=c, width=w); d.line([z*.44, z*.8, z*.56, z*.8], fill=a, width=w)
    elif name == 'calendar':
        d.rounded_rectangle([z*.12, z*.2, z*.88, z*.88], 10*S, outline=c, width=w); d.line([z*.12, z*.4, z*.88, z*.4], fill=c, width=w)
        for x in (.32, .68): d.line([z*x, z*.1, z*x, z*.28], fill=c, width=w)
        d.ellipse([z*.55, z*.55, z*.75, z*.75], fill=a)
    elif name == 'chart':
        d.line([z*.12, z*.12, z*.12, z*.88, z*.9, z*.88], fill=c, width=w, joint='curve')
        d.line([z*.22, z*.7, z*.42, z*.5, z*.58, z*.6, z*.85, z*.25], fill=a, width=w, joint='curve')
    elif name == 'target':
        for r in (.4, .26, .12): d.ellipse([z*(.5-r), z*(.5-r), z*(.5+r), z*(.5+r)], outline=c if r != .12 else a, width=w)
    elif name == 'money':
        d.rounded_rectangle([z*.08, z*.25, z*.92, z*.75], 10*S, outline=c, width=w)
        d.ellipse([z*.38, z*.37, z*.62, z*.63], outline=a, width=w)
    elif name == 'brain':
        d.ellipse([z*.12, z*.18, z*.58, z*.78], outline=c, width=w); d.ellipse([z*.42, z*.18, z*.88, z*.78], outline=c, width=w)
        d.line([z*.5, z*.3, z*.5, z*.7], fill=a, width=w)
    elif name == 'map':
        d.line([z*.1, z*.25, z*.37, z*.12, z*.63, z*.25, z*.9, z*.12, z*.9, z*.75, z*.63, z*.88, z*.37, z*.75, z*.1, z*.88, z*.1, z*.25], fill=c, width=w, joint='curve')
        d.ellipse([z*.55, z*.38, z*.75, z*.58], fill=a)
    elif name == 'person':
        d.ellipse([z*.33, z*.1, z*.67, z*.44], outline=c, width=w); d.arc([z*.15, z*.5, z*.85, z*1.2], 180, 360, fill=c, width=w)
        d.ellipse([z*.7, z*.08, z*.86, z*.24], fill=a)
    elif name == 'check':
        d.ellipse([z*.1, z*.1, z*.9, z*.9], outline=c, width=w); d.line([z*.3, z*.52, z*.45, z*.67, z*.72, z*.36], fill=a, width=w+2*S, joint='curve')
    elif name == 'x':
        d.ellipse([z*.1, z*.1, z*.9, z*.9], outline=c, width=w); d.line([z*.33, z*.33, z*.67, z*.67], fill=a, width=w); d.line([z*.67, z*.33, z*.33, z*.67], fill=a, width=w)
    elif name == 'clock':
        d.ellipse([z*.1, z*.1, z*.9, z*.9], outline=c, width=w); d.line([z*.5, z*.25, z*.5, z*.5, z*.68, z*.62], fill=a, width=w, joint='curve')
    elif name == 'question':
        d.ellipse([z*.1, z*.1, z*.9, z*.9], outline=c, width=w)
        d.text((z*.5, z*.5), '?', font=F_BLACK(int(z*.55)), fill=a, anchor='mm')
    elif name == 'rocket':
        d.line([z*.2, z*.8, z*.75, z*.25], fill=c, width=w); d.line([z*.75, z*.25, z*.88, z*.12], fill=a, width=w)
        d.line([z*.55, z*.25, z*.75, z*.25, z*.75, z*.45], fill=c, width=w, joint='curve')
    elif name == 'dice':
        d.rounded_rectangle([z*.12, z*.12, z*.88, z*.88], 16*S, outline=c, width=w)
        for (x, y) in [(.3,.3),(.7,.7),(.5,.5),(.3,.7),(.7,.3)]: d.ellipse([z*(x-.07), z*(y-.07), z*(x+.07), z*(y+.07)], fill=a if (x, y) == (.5, .5) else c)
    elif name == 'heart':
        d.polygon([(z*.5, z*.88), (z*.1, z*.45), (z*.9, z*.45)], fill=None, outline=c)
        d.pieslice([z*.08, z*.15, z*.52, z*.6], 140, 360, fill=None, outline=c, width=w); d.pieslice([z*.48, z*.15, z*.92, z*.6], 180, 40, fill=None, outline=c, width=w)
        d.line([z*.12, z*.47, z*.5, z*.88, z*.88, z*.47], fill=c, width=w, joint='curve'); d.line([z*.3, z*.5, z*.42, z*.5, z*.48, z*.38, z*.56, z*.62, z*.62, z*.5, z*.72, z*.5], fill=a, width=int(w*.8), joint='curve')
    elif name == 'clover':
        for (x, y) in [(.35,.32),(.65,.32),(.35,.62),(.65,.62)]: d.ellipse([z*(x-.16), z*(y-.16), z*(x+.16), z*(y+.16)], outline=c, width=w)
        d.line([z*.5, z*.6, z*.62, z*.92], fill=a, width=w)
    elif name == 'steps':
        d.line([z*.1, z*.85, z*.35, z*.85, z*.35, z*.62, z*.6, z*.62, z*.6, z*.38, z*.85, z*.38, z*.85, z*.15], fill=c, width=w, joint='curve'); d.ellipse([z*.78, z*.08, z*.92, z*.22], fill=a)
    return im.resize((size, size), Image.LANCZOS)

def icon_card(name, label, bg=None, fg=None, edge=None):
    bg = tuple(bg) if bg else MAR; fg = tuple(fg) if fg else BL; edge = tuple(edge) if edge else AZ
    cw, ch = 196, 250
    im = Image.new('RGBA', (cw + 30, ch + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([15, 21, 15 + cw, 21 + ch], 28, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([15, 15, 15 + cw, 15 + ch], 28, fill=bg + (245,))
    d.rounded_rectangle([15, 15, 15 + cw, 15 + ch], 28, outline=edge + (255,), width=3)
    ic = icon(name, 120, fg, MAR if bg == NAR else None); im.alpha_composite(ic, (15 + (cw - 120) // 2, 15 + 32))
    fs = 30
    while F_XB(fs).getlength(label) > cw - 24 and fs > 16: fs -= 1
    d.text((15 + cw / 2, 15 + 205), label, font=F_XB(fs), fill=fg, anchor='mm')
    return im

# ---------- subtítulos ----------
def subtitle_img(txt, keyword, scale):
    fsn, fsk = 84, 132
    parts = txt.split(' ')
    fonts = [F_BLACK(fsk) if (keyword and p == keyword) else F_XB(fsn) for p in parts]
    gap = 22
    widths = [f.getlength(p) for p, f in zip(parts, fonts)]
    tw = sum(widths) + gap * (len(parts) - 1)
    if tw > 940:  # reducir si no cabe
        k = 940 / tw; fonts = [F_BLACK(int(fsk * k)) if (keyword and p == keyword) else F_XB(int(fsn * k)) for p in parts]
        widths = [f.getlength(p) for p, f in zip(parts, fonts)]; tw = sum(widths) + gap * (len(parts) - 1)
    im = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = (W - tw) / 2; cy = 130
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    for p, f, wd in zip(parts, fonts, widths):
        sd.text((x + 4, cy + 6), p, font=f, fill=(0, 0, 0, 150), anchor='lm'); x += wd + gap
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
    x = (W - tw) / 2
    for p, f, wd in zip(parts, fonts, widths):
        iskey = keyword and p == keyword
        d.text((x, cy), p, font=f, fill=NAR if iskey else BL, anchor='lm', stroke_width=6, stroke_fill=NG)
        x += wd + gap
    if scale != 1:
        nw, nh = int(W * scale), int(260 * scale); im2 = im.resize((nw, nh), Image.BICUBIC)
        c = Image.new('RGBA', im.size, (0, 0, 0, 0)); c.alpha_composite(im2, ((W - nw) // 2, (260 - nh) // 2)); im = c
    return im

# ---------- tarjeta a pantalla completa ----------
def full_card(lines, sub=None, theme=None):
    BG = NAR if theme == 'orange' else (BL if theme == 'white' else MAR); TX = MAR if theme == 'white' else BL; BLK = MAR if theme == 'orange' else NAR; ACC = BL if theme == 'orange' else NAR
    im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    # trama sutil
    for y in range(0, H, 6): d.line([0, y, W, y], fill=(255, 255, 255, 6))
    total = len(lines) * 150; y = H / 2 - total / 2 + 60
    for i, (t, col) in enumerate(lines):
        f = F_BLACK(128)
        while f.getlength(t) > 940: f = F_BLACK(f.size - 4)
        if col == 'blk':
            tw = f.getlength(t); rr(d, [W/2 - tw/2 - 30, y - 82, W/2 + tw/2 + 30, y + 72], 24, BLK); d.text((W/2, y), t, font=f, fill=BL, anchor='mm')
        else: d.text((W/2, y), t, font=f, fill=ACC if col == 'nar' else TX, anchor='mm')
        y += 165
    d.rectangle([W/2 - 60, 560, W/2 + 60, 572], fill=ACC)
    if sub: d.text((W/2, y + 40), sub, font=F_B(44), fill=(200, 205, 230), anchor='mm')
    return im

# ---------- cierre ----------
LOGO = Image.open('/home/claude/reels/kit/logos/logo-aq-blanco-transparente.png').convert('RGBA')
lw = 360; LOGO = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
def end_card(cta):
    im = Image.new('RGBA', (W, H), (1, 0, 90, 235)); d = ImageDraw.Draw(im)
    im.alpha_composite(LOGO, ((W - lw) // 2, 640)); d = ImageDraw.Draw(im)
    y = 640 + LOGO.height + 70
    d.text((W/2, y), '@aqfinanzas', font=F_XB(64), fill=BL, anchor='mm')
    f = F_XB(46); tw = f.getlength(cta)
    rr(d, [W/2 - tw/2 - 36, y + 90, W/2 + tw/2 + 36, y + 180], 28, NAR)
    d.text((W/2, y + 135), cta, font=f, fill=BL, anchor='mm')
    return im

def chip(text, ok):
    f = F_XB(54); tw = f.getlength(text) + 130
    im = Image.new('RGBA', (int(tw) + 40, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, [20, 20, 20 + tw, 110], 28, MAR + (245,)); d.rounded_rectangle([20, 20, 20 + tw, 110], 28, outline=(AZ if ok else NAR) + (255,), width=4)
    d.text((48, 65), text, font=f, fill=BL, anchor='lm')
    d.text((20 + tw - 52, 65), '✓' if ok else '✗', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 54), fill=(46, 204, 113) if ok else (231, 76, 60), anchor='mm')
    return im

def recuerdo_chip():
    im = Image.new('RGBA', (300, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, [0, 0, 290, 64], 32, (10, 10, 10, 200)); d.ellipse([22, 22, 42, 42], fill=NAR); d.text((56, 32), 'RECUERDO', font=F_XB(32), fill=BL, anchor='lm')
    return im

# ---------- preparar eventos ----------
cache = {}
for i, ev in enumerate(events):
    t = ev['type']
    if t == 'icon': cache[i] = icon_card(ev['icon'], ev['label'], ev.get('bg'), ev.get('fg'), ev.get('edge'))
    elif t == 'img':
        im0 = Image.open(ev['img']).convert('RGBA'); w0 = ev.get('w', 360); cache[i] = im0.resize((w0, int(im0.height * w0 / im0.width)), Image.LANCZOS)
    elif t == 'band':
        bh = 110; f = F_XB(54); tw = f.getlength(ev['text'])
        im = Image.new('RGBA', (int(tw) + 100, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.rounded_rectangle([0, 0, im.width - 1, bh - 1], 48, fill=tuple(ev.get('bg', NAR)) + (250,)); dd.text((im.width / 2, bh / 2), ev['text'], font=f, fill=tuple(ev.get('fg', BL)), anchor='mm'); cache[i] = im
    elif t == 'card': cache[i] = full_card(ev['lines'], ev.get('sub'), ev.get('theme'))
    elif t == 'end': cache[i] = end_card(ev['cta'])
    elif t == 'chip': cache[i] = chip(ev['text'], ev['ok'])
    elif t == 'bigword':
        lines = ev['text'].split('\n'); f = F_BLACK(ev.get('size', 190))
        while max(f.getlength(l) for l in lines) > 1000: f = F_BLACK(f.size - 6)
        lh = int(f.size * 1.02); im = Image.new('RGBA', (W, lh * len(lines) + 40), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        cols = [tuple(c) for c in ev.get('colors', [BL, NAR])]
        for li, l in enumerate(lines): dd.text((W/2, 20 + lh * li + lh / 2), l, font=f, fill=(cols[1] if li == len(lines) - 1 else cols[0]) + (255,), anchor='mm')
        cache[i] = im
REC = recuerdo_chip()
_f = np.ones((380, 340), np.float32); _f[:, -60:] *= np.linspace(1, 0, 60)[None]; _f[:40, :] *= np.linspace(0, 1, 40)[:, None]
FEATH = Image.fromarray((_f * 255).astype(np.uint8), 'L')
_g = np.zeros((H, W, 4), np.uint8); _g[..., 0:3] = MAR
ys = np.arange(H); a = np.clip((ys - 1540) / 380, 0, 1) ** 1.4 * 215
_g[..., 3] = a[:, None].astype(np.uint8); GRAD = Image.fromarray(_g, 'RGBA')

# subtítulos: frames por grupo
subs = []
for g in groups:
    ws = words[g[0]:g[1] + 1]
    s = ws[0]['s']; e = max(ws[-1]['e'], s + 0.45)
    subs.append((s, e, g))
for k in range(len(subs) - 1):
    s, e, g = subs[k]; subs[k] = (s, min(max(e, s + 0.45), subs[k + 1][0]), g)

def fr(t): return int(round(t * FPS))

rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', base, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
rm = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', matte, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)

subimg_cache = {}
for n in range(N):
    t = n / FPS
    raw = rd.stdout.read(W * H * 3)
    if len(raw) < W * H * 3: break
    mraw = rm.stdout.read(W * H)
    frame = Image.frombuffer('RGB', (W, H), raw).convert('RGBA')
    m = Image.frombuffer('L', (W, H), mraw)
    z = next((zz[2] for zz in cfg.get('zooms', []) if zz[0] <= t < zz[1]), 1.0)
    if z != 1.0:
        cw, ch = W / z, H / z; cx, cy = W / 2, 760; box = (cx - cw / 2, max(0, cy - ch * 760 / H), 0, 0)
        box = (box[0], box[1], box[0] + cw, box[1] + ch)
        frame = frame.resize((W, H), Image.BICUBIC, box=box); m = m.resize((W, H), Image.BILINEAR, box=box)
    reg = frame.crop((0, 1460, 340, 1840)).filter(ImageFilter.GaussianBlur(45)); reg = Image.blend(reg, Image.new('RGBA', reg.size, (10, 10, 20, 255)), 0.35); frame.paste(reg, (0, 1460), FEATH)
    if any(ev['type'] == 'blurbg' and ev['s'] <= t < ev['e'] for ev in events):
        ev0 = next(ev for ev in events if ev['type'] == 'blurbg' and ev['s'] <= t < ev['e'])
        k = min(1, (t - ev0['s']) / 0.3, (ev0['e'] - t) / 0.3); bl = frame.filter(ImageFilter.GaussianBlur(28 * k))
        frame = Image.composite(frame, bl, m)
    frame = Image.alpha_composite(frame, GRAD)
    # recuerdo (B/N)
    rec = [ev for ev in events if ev['type'] == 'recuerdo' and ev['s'] <= t < ev['e']]
    if rec:
        g = frame.convert('L').convert('RGBA'); frame = Image.blend(frame, g, 0.85)
    back = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # capa detrás de él
    front = Image.new('RGBA', (W, H), (0, 0, 0, 0))  # capa delante
    for i, ev in enumerate(events):
        s = ev.get('s', 0); e = ev.get('e', 0)
        if not (s <= t < e): continue
        typ = ev['type']; p = (t - s)
        if typ == 'icon':
            im = cache[i]; k = easeOutBack(p / 0.3); out_k = 1 - easeOut((t - (e - 0.2)) / 0.2) if t > e - 0.2 else 1
            sc = max(0.01, k * out_k); iw, ih = int(im.width * sc), int(im.height * sc)
            if iw < 4: continue
            im2 = im.resize((iw, ih), Image.BICUBIC)
            cx, cy = ev['pos']; back.alpha_composite(im2, (int(cx - iw / 2), int(cy - ih / 2)))
        elif typ == 'bigword':
            im = cache[i]; a = min(1, p / 0.25) * (1 if t < e - 0.25 else (e - t) / 0.25)
            y0 = ev.get('y', 330); dy = int((1 - easeOut(p / 0.35)) * 60)
            im2 = im.copy(); im2.putalpha(im2.getchannel('A').point(lambda v: int(v * a)))
            back.alpha_composite(im2, (0, y0 + dy))
        elif typ == 'img':
            im = cache[i]; k = easeOutBack(p / 0.35); out_k = 1 - easeOut((t - (e - 0.25)) / 0.25) if t > e - 0.25 else 1
            sc = max(0.01, k * out_k); iw, ih = int(im.width * sc), int(im.height * sc)
            if iw < 4: continue
            im2 = im.resize((iw, ih), Image.BICUBIC); cx, cy = ev['pos']
            (front if ev.get('front') else back).alpha_composite(im2, (int(cx - iw / 2), int(cy - ih / 2)))
        elif typ == 'chip':
            im = cache[i]; k = easeOutBack(p / 0.3); dx = int((1 - k) * (-200 if ev['pos'][0] < W / 2 else 200))
            a = 1 if t < e - 0.2 else (e - t) / 0.2
            im2 = im.copy(); im2.putalpha(im2.getchannel('A').point(lambda v: int(v * a)))
            back.alpha_composite(im2, (int(ev['pos'][0] - im.width / 2 + dx), int(ev['pos'][1])))
    # componer: fondo + capa trasera recortada por mate
    if back.getbbox():
        inv = Image.eval(m, lambda v: 255 - v)
        ba = back.getchannel('A'); back.putalpha(Image.fromarray((np.asarray(ba, dtype=np.uint16) * np.asarray(inv, dtype=np.uint16) // 255).astype(np.uint8)))
        frame = Image.alpha_composite(frame, back)
    if rec and not any(ev['type'] == 'bigword' and ev['s'] <= t < ev['e'] for ev in events):
        frame.alpha_composite(REC, (60, 240))
    # tarjetas a pantalla completa / cierre
    covering = False
    for i, ev in enumerate(events):
        if ev['type'] in ('card', 'end') and ev['s'] <= t < ev['e']:
            p = t - ev['s']; a = min(1, p / 0.18) * (1 if t < ev['e'] - 0.15 or ev['type'] == 'end' else (ev['e'] - t) / 0.15)
            im = cache[i]
            if ev['type'] == 'card':
                sc = 0.92 + 0.08 * easeOut(p / 0.3); iw, ih = int(W * sc), int(H * sc)
                im2 = Image.new('RGBA', (W, H), im.getpixel((5, 5))); im2.alpha_composite(im.resize((iw, ih)), ((W - iw) // 2, (H - ih) // 2)); im = im2
            im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
            frame = Image.alpha_composite(frame, im); covering = a > 0.5
    for i, ev in enumerate(events):
        if ev['type'] == 'band' and ev['s'] <= t < ev['e']:
            im = cache[i]; p = t - ev['s']; dy = int((1 - easeOut(p / 0.3)) * 160); a = 1 if t < ev['e'] - 0.2 else (ev['e'] - t) / 0.2
            im2 = im.copy(); im2.putalpha(im2.getchannel('A').point(lambda v: int(v * a))); frame.alpha_composite(im2, (int((W - im.width) / 2), ev.get('y', 1450) + dy))
    if front.getbbox(): frame = Image.alpha_composite(frame, front)
    # subtítulos
    if not covering:
        for s, e, g in subs:
            if s <= t < e:
                ws = words[g[0]:g[1] + 1]
                shown = [w for w in ws if w['s'] <= t + 0.03]
                if not shown: shown = ws[:1]
                txt = ' '.join(w['w'] for w in shown)
                key = next((w['w'] for w in shown if w.get('key')), None)
                pp = (t - s); sc = 0.85 + 0.15 * easeOut(pp / 0.12)
                ck = (txt, key, round(sc, 2))
                if ck not in subimg_cache:
                    if len(subimg_cache) > 400: subimg_cache.clear()
                    subimg_cache[ck] = subtitle_img(txt, key, sc)
                frame.alpha_composite(subimg_cache[ck], (0, 1250 - 130))
                break
    # flashes
    for ev in events:
        if ev['type'] == 'flash' and ev['s'] <= t < ev['s'] + 0.13:
            a = 1 - (t - ev['s']) / 0.13; fl = Image.new('RGBA', (W, H), (255, 255, 255, int(200 * a))); frame = Image.alpha_composite(frame, fl)
    wr.stdin.write(frame.convert('RGB').tobytes())
    if n % 150 == 0: print('frame', n, '/', N, flush=True)
wr.stdin.close(); wr.wait()
print('listo')
