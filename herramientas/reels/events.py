import json
c = json.load(open('/home/claude/reels/cut.json'))
W = c['words']; im = c['idxmap']
def t(i): return W[im[str(i)]]['s']
def te(i): return W[im[str(i)]]['e']
L, R = (138, 560), (837, 380)
N = 1091; END = N / 30
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
icon(23, 'question', 'LA PREGUNTA', L)
big(32, 36, '¿CUÁNTO\nGANAS?')
sfx.append(('riser', t(45) - 1.0, -26))
big(45, 51, '¿CUÁNTO\nTE QUEDA?')
icon(52, 'money', 'NO ES DINERO', R)
icon(61, 'person', 'ALUMNOS', L)
chip(64, 'GANA 5.000 · GASTA 7.000', False, 250, te(97))
chip(82, 'GANA 3.000 · GUARDA 1.000', True, 385, te(97))
icon(99, 'chart', 'RIQUEZA', R)
icon(102, 'clock', 'TIEMPO', L)
sfx.append(('riser', t(110) - 1.0, -26))
ev.append({'type': 'flash', 's': t(111)}); sfx.append(('golpe', t(111), -22))
card(119, 126, [['LO QUE HACES', 'w'], ['CON LO QUE', 'w'], ['TE QUEDA', 'blk']])
# anécdota
ev.append({'type': 'recuerdo', 's': t(148) - 0.08, 'e': te(161) + 0.1})
ev.append({'type': 'flash', 's': t(148) - 0.08}); sfx.append(('whoosh', t(148) - 0.15, -22)); sfx.append(('whoosh', te(161) + 0.02, -24))
icon(157, 'money', 'INGRESOS', R)
big(162, 167, '¿CUÁNTO\nTE QUEDA?')
icon(176, 'target', 'AVANZAR', L)
card(183, 188, [['ESO SE LLAMA', 'w'], ['EXCEDENTE', 'blk']])
ev.append({'type': 'end', 's': te(188) + 0.15, 'e': END + 1, 'cta': 'GUÁRDALO Y COMPÁRTELO'}); sfx.append(('chime', te(188) + 0.15, -20))

# punch-ins por tramo (alterna)
starts = []; acc = 0
for n, m in c['frames']: starts.append(acc / 1.15); acc += n / 30
zooms = []
for k, s in enumerate(starts):
    e = starts[k + 1] if k + 1 < len(starts) else END
    zooms.append([s, e, [1.06, 1.0, 1.04, 1.0][k % 4]])

cfg = {'words': W, 'groups': c['groups'], 'events': ev, 'nframes': N, 'zooms': zooms,
       'base': '/home/claude/reels/base.mp4', 'matte': '/home/claude/reels/mate/mate.mkv', 'out': '/home/claude/reels/video_graf.mp4'}
json.dump(cfg, open('/home/claude/reels/cfg.json', 'w'), ensure_ascii=False)
json.dump(sfx, open('/home/claude/reels/sfx.json', 'w'))
for e in ev: print(e['type'], round(e.get('s', 0), 2), round(e.get('e', 0), 2), e.get('label', e.get('text', '')))
