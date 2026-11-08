import json
c = json.load(open('/home/claude/r2/cut.json'))
W = c['words']; im = c['idxmap']
def t(i): return W[im[str(i)]]['s']
def te(i): return W[im[str(i)]]['e']
L, R = (138, 560), (837, 380)
N = 1339; END = N / 30
ev = []; sfx = []
def icon(i, name, label, pos, d=1.7):
    s = t(i); ev.append({'type': 'icon', 'icon': name, 'label': label, 'pos': pos, 's': s, 'e': s + d}); sfx.append(('pop', s, -22))
def big(a, b, txt, y=250):
    ev.append({'type': 'bigword', 'text': txt, 's': t(a), 'e': te(b) + 0.25, 'y': y}); sfx.append(('whoosh', t(a) - 0.05, -24))
def chip(i, text, ok, y, until):
    ev.append({'type': 'chip', 'text': text, 'ok': ok, 'pos': [540, y], 's': t(i), 'e': until}); sfx.append(('tap', t(i), -20))
def card(a, b, lines, sub=None):
    ev.append({'type': 'card', 'lines': lines, 'sub': sub, 's': t(a) - 0.05, 'e': te(b) + 0.12}); sfx.append(('whoosh', t(a) - 0.12, -22))

# gancho
ev.append({'type': 'flash', 's': 0.0}); sfx.append(('golpe', 0.0, -18))
ev.append({'type': 'recuerdo', 's': 0.0, 'e': te(53) + 0.1}); sfx.append(('whoosh', te(53) + 0.02, -24))
big(39, 42, 'LLENAR\nLA TAZA')
icon(59, 'money', 'EXCEDENTE', L)
icon(87, 'chart', 'INVERTIR', R)
card(97, 106, [['PRIMERO LLENAS', 'w'], ['LA TAZA', 'nar'], ['LUEGO VIVES DE', 'w'], ['LO QUE REBOSA', 'blk']])
icon(112, 'map', 'AMÉRICA LATINA', L)
chip(141, 'APARTAMENTO EN LA PLAYA', False, 225, te(178))
chip(153, 'OTRO CARRO', False, 325, te(178))
chip(170, 'UNA MOTO', False, 425, te(178))
big(191, 201, 'EL ÚNICO ACTIVO\nSON ELLOS')
sfx.append(('riser', t(262) - 1.0, -26))
ev.append({'type': 'flash', 's': t(262)}); sfx.append(('golpe', t(262), -22))
icon(271, 'question', '¿QUÉ TAZA?', R)
card(279, 281, [['LA TAZA', 'w'], ['FINANCIERA', 'blk']])
ev.append({'type': 'end', 's': te(281) + 0.15, 'e': END + 1, 'cta': 'GUÁRDALO Y COMPÁRTELO'}); sfx.append(('chime', te(281) + 0.15, -20))

# punch-ins por tramo (alterna)
starts = []; acc = 0
for n, m in c['frames']: starts.append(acc / 1.15); acc += n / 30
zooms = []
for k, s in enumerate(starts):
    e = starts[k + 1] if k + 1 < len(starts) else END
    zooms.append([s, e, [1.06, 1.0, 1.04, 1.0][k % 4]])

cfg = {'words': W, 'groups': c['groups'], 'events': ev, 'nframes': N, 'zooms': zooms,
       'base': '/home/claude/r2/base.mp4', 'matte': '/home/claude/r2/mate/mate.mkv', 'out': '/home/claude/r2/video_graf.mp4'}
json.dump(cfg, open('/home/claude/r2/cfg.json', 'w'), ensure_ascii=False)
json.dump(sfx, open('/home/claude/r2/sfx.json', 'w'))
for e in ev: print(e['type'], round(e.get('s', 0), 2), round(e.get('e', 0), 2), e.get('label', e.get('text', '')))
