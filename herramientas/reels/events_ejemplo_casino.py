import json
c = json.load(open('/home/claude/r3/cut.json'))
W = c['words']; im = c['idxmap']
def t(i): return W[im[str(i)]]['s']
def te(i): return W[im[str(i)]]['e']
L, R = (138, 560), (837, 380)
N = 1241; END = N / 30
ev = []; sfx = []
def icon(i, name, label, pos, d=1.7, **kw):
    s = t(i); ev.append(dict({'type': 'icon', 'icon': name, 'label': label, 'pos': pos, 's': s, 'e': s + d}, **kw)); sfx.append(('pop', s, -22))
def big(a, b, txt, y=250, **kw):
    ev.append(dict({'type': 'bigword', 'text': txt, 's': t(a), 'e': te(b) + 0.25, 'y': y}, **kw)); sfx.append(('whoosh', t(a) - 0.05, -24))
def chip(i, text, ok, y, until):
    ev.append({'type': 'chip', 'text': text, 'ok': ok, 'pos': [540, y], 's': t(i), 'e': until}); sfx.append(('tap', t(i), -20))
def card(a, b, lines, sub=None, theme=None):
    ev.append({'type': 'card', 'lines': lines, 'sub': sub, 'theme': theme, 's': t(a) - 0.05, 'e': te(b) + 0.12}); sfx.append(('whoosh', t(a) - 0.12, -22))

# gancho
NAR = [240, 74, 3]; BLc = [255, 255, 255]; MARc = [1, 0, 90]; NG = [10, 10, 10]
ev.append({'type': 'flash', 's': 0.0}); sfx.append(('golpe', 0.0, -18))
ev.append({'type': 'blurbg', 's': 0.0, 'e': te(281) + 0.35})
ev.append({'type': 'img', 'img': '/home/claude/r3/img/dados.png', 'w': 520, 'pos': [540, 420], 's': 0.08, 'e': te(281) + 0.4}); sfx.append(('pop', 0.1, -22))
icon(21, 'x', 'FÓRMULA MÁGICA', R, bg=NAR, fg=BLc, edge=BLc)
big(34, 39, '¿DE LA NOCHE\nA LA MAÑANA?', colors=[BLc, NAR])
icon(67, 'clover', 'SUERTE', L, bg=BLc, fg=MARc, edge=NAR)
icon(85, 'clock', 'AÑOS', R, bg=NG, fg=BLc, edge=NAR)
ev.append({'type': 'band', 'text': 'NO CREO EN LA RIQUEZA RÁPIDA', 'bg': MARc, 'fg': BLc, 'y': 1440, 's': t(96), 'e': te(106) + 0.3}); sfx.append(('whoosh', t(96) - 0.05, -24))
chip(131, 'HOY: 1 DÓLAR', False, 225, te(141) + 0.2)
chip(134, 'MAÑANA: 1.000', False, 325, te(141) + 0.2)
icon(226, 'heart', 'CORAZÓN ABIERTO', L, bg=BLc, fg=MARc, edge=NAR)
ev.append({'type': 'blurbg', 's': t(240), 'e': te(257)})
icon(246, 'person', 'CIRUJANO', R, bg=[42, 148, 248], fg=BLc, edge=BLc)
sfx.append(('riser', t(258) - 1.0, -26))
icon(268, 'steps', 'PASO A PASO', L, bg=NAR, fg=BLc, edge=BLc)
card(288, 292, [['NO ES SUERTE', 'w'], ['ES UN', 'w'], ['MÉTODO', 'blk']], theme='orange')
ev.append({'type': 'end', 's': te(292) + 0.15, 'e': END + 1, 'cta': 'GUÁRDALO Y COMPÁRTELO'}); sfx.append(('chime', te(292) + 0.15, -20))

# punch-ins por tramo (alterna)
starts = []; acc = 0
for n, m in c['frames']: starts.append(acc / 1.15); acc += n / 30
zooms = []
for k, s in enumerate(starts):
    e = starts[k + 1] if k + 1 < len(starts) else END
    zooms.append([s, e, [1.06, 1.0, 1.04, 1.0][k % 4]])

cfg = {'words': W, 'groups': c['groups'], 'events': ev, 'nframes': N, 'zooms': zooms,
       'base': '/home/claude/r3/base.mp4', 'matte': '/home/claude/r3/mate/mate.mkv', 'out': '/home/claude/r3/video_graf.mp4'}
json.dump(cfg, open('/home/claude/r3/cfg.json', 'w'), ensure_ascii=False)
json.dump(sfx, open('/home/claude/r3/sfx.json', 'w'))
for e in ev: print(e['type'], round(e.get('s', 0), 2), round(e.get('e', 0), 2), e.get('label', e.get('text', '')))
