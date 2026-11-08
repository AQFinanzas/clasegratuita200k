import json
D='/home/claude/reels/r10/'
c = json.load(open(D+'cut.json'))
W = c['words']; im = c['idxmap']
def t(i): return W[im[str(i)]]['s']
def te(i): return W[im[str(i)]]['e']
L, R = (138, 560), (837, 380)
import subprocess
N = int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',D+'base.mp4'],capture_output=True,text=True).stdout); END = N / 30
ev = []; sfx = []
def icon(i, name, label, pos, d=1.7, **kw):
    s = t(i); ev.append(dict({'type': 'icon', 'icon': name, 'label': label, 'pos': pos, 's': s, 'e': s + d}, **kw)); sfx.append(('pop', s, -22))
def big(a, b, txt, y=250, **kw):
    ev.append(dict({'type': 'bigword', 'text': txt, 's': t(a), 'e': te(b) + 0.25, 'y': y}, **kw)); sfx.append(('whoosh', t(a) - 0.05, -24))
def chip(i, text, ok, y, until):
    ev.append({'type': 'chip', 'text': text, 'ok': ok, 'pos': [540, y], 's': t(i), 'e': until}); sfx.append(('tap', t(i), -20))
def card(a, b, lines, sub=None, theme=None):
    ev.append({'type': 'card', 'lines': lines, 'sub': sub, 'theme': theme, 's': t(a) - 0.05, 'e': te(b) + 0.12}); sfx.append(('whoosh', t(a) - 0.12, -22))
NAR = [240, 74, 3]; BLc = [255, 255, 255]; MARc = [1, 0, 90]; NG = [10, 10, 10]; AZ = [42, 148, 248]; VE = [46, 170, 100]; RO = [214, 48, 49]
ev.append({'type': 'flash', 's': 0.0}); sfx.append(('golpe', 0.0, -18))
# gancho: pregunta grande detrás de la cabeza, pared difuminada
ev.append({'type': 'blurbg', 's': 0.0, 'e': te(37) + 0.3})
big(29, 37, '¿Y SI MAÑANA\nLO QUIERES\nDE VUELTA?', colors=[BLc, BLc, NAR])
icon(28, 'house', 'INMUEBLE', (930, 820), bg=BLc, fg=MARc, edge=NAR)
icon(49, 'clock', 'MESES', R, bg=BLc, fg=RO, edge=RO)
# comparación con chips que se acumulan
chip(98, 'INMUEBLE: MESES', False, 225, te(205) + 0.4)
icon(131, 'store', 'NEGOCIO', R, bg=NG, fg=BLc, edge=NAR)
chip(143, 'NEGOCIO: 1 A 2 AÑOS', False, 325, te(205) + 0.4)
icon(192, 'chart', 'ACCIONES', L, bg=AZ, fg=BLc, edge=BLc)
ev.append({'type': 'band', 'text': 'COMPRO 10:00  ·  VENDO 10:02', 'bg': NAR, 'fg': BLc, 'y': 1440, 's': t(193), 'e': te(201) + 0.35}); sfx.append(('whoosh', t(193) - 0.05, -24))
chip(204, 'ACCIONES: MINUTOS', True, 425, te(205) + 0.4)
sfx.append(('riser', t(209) - 1.0, -26))
card(213, 223, [['TU DINERO', 'w'], ['CUANDO LO', 'w'], ['NECESITES', 'blk']], sub='ESO ES LIQUIDEZ', theme='white')
ev.append({'type': 'end', 's': te(223) + 0.15, 'e': END + 1, 'cta': 'GUÁRDALO Y COMPÁRTELO'}); sfx.append(('chime', te(223) + 0.15, -20))
starts = []; acc = 0
for n, m in c['frames']: starts.append(acc / 1.15); acc += n / 30
zooms = []
for k, s in enumerate(starts):
    e = starts[k + 1] if k + 1 < len(starts) else END
    zooms.append([s, e, [1.06, 1.0, 1.04, 1.0][k % 4]])
cfg = {'words': W, 'groups': c['groups'], 'events': ev, 'nframes': N, 'zooms': zooms,
       'base': D+'base.mp4', 'matte': D+'mate/mate.mkv', 'out': D+'video_graf.mp4'}
json.dump(cfg, open(D+'cfg.json', 'w'), ensure_ascii=False)
json.dump(sfx, open(D+'sfx.json', 'w'))
for e in ev: print(e['type'], round(e.get('s', 0), 2), round(e.get('e', 0), 2), e.get('label', e.get('text', '')))
