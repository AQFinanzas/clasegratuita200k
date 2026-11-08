import json, subprocess
ws = json.load(open('/home/claude/reels/r10/words_raw.json'))
fix = {33: 'quiero', 192: 'Apple', 99: 'inmediatamente.', 205: 'liquidez.', 173: 'líquido.', 24: 'Si', 174: 'En', 113: 'Entonces,'}
drop = {31, 32, 179, 186, 187}
for k, v in fix.items(): ws[k]['w'] = v
ranges = [(24, 37), (45, 49), (71, 74), (95, 99), (113, 119), (127, 131), (138, 146), (170, 173), (174, 201), (202, 205), (209, 223)]
keys = {28, 49, 74, 98, 119, 131, 143, 173, 192, 205, 218}
SP = 1.15
# intervalos a conservar (tiempo de la toma)
keep = []; kw = []
for a, b in ranges:
    idx = [i for i in range(a, b + 1) if i not in drop]
    cur = [idx[0]]
    for i in idx[1:]:
        if ws[i]['s'] - ws[cur[-1]]['e'] > 0.4: keep.append(cur); cur = [i]
        else: cur.append(i)
    keep.append(cur)
ivs = []
for g in keep:
    s = ws[g[0]]['s'] - 0.10; e = ws[g[-1]]['e'] + 0.14
    ivs.append([max(0, s), e, g])
# evitar solapes
for k in range(1, len(ivs)):
    if ivs[k - 1][0] <= ivs[k][0] < ivs[k - 1][1]: m = (ivs[k][0] + ivs[k - 1][1]) / 2; ivs[k - 1][1] = m; ivs[k][0] = m
# mapear palabras al tiempo final
words = []; idxmap = {}; off = 0
for s, e, g in ivs:
    for i in g:
        w = ws[i]; ns = (off + w['s'] - s) / SP; ne = (off + w['e'] - s) / SP
        idxmap[i] = len(words)
        words.append({'w': w['w'].upper().strip(',.¿?'), 'raw': w['w'], 's': round(ns, 3), 'e': round(ne, 3), 'key': i in keys, 'src': i})
    off += e - s
dur = off / SP
print('duración cortada', round(off, 2), '-> final', round(dur, 2))
# palabras con signos
for w in words:
    r = w['raw']; t = w['w']
    if r.startswith('¿'): t = '¿' + t
    if r.endswith('?'): t = t + '?'
    w['w'] = t
# grupos de subtítulos (1-3 palabras, corte en puntuación)
MAN = [[24,26],[27,28],[29,30],[33,35],[36,37],[45,47],[48,49],[71,72],[73,74],[95,97],[98,99],[113,115],[116,119],[127,129],[130,131],[138,140],[141,143],[144,146],[170,173],[174,175],[176,178],[180,182],[183,185],[188,190],[191,192],[193,195],[196,197],[198,201],[202,203],[204,205],[209,212],[213,216],[217,220],[221,223]]
groups = [[idxmap[a], idxmap[b]] for a, b in MAN]
json.dump({'ivs': [[round(a, 3), round(b, 3)] for a, b, _ in ivs], 'words': words, 'groups': groups, 'idxmap': idxmap, 'dur': dur}, open('/home/claude/reels/r10/cut.json', 'w'), ensure_ascii=False, indent=0)
for g in groups: print(' '.join(words[k]['w'] for k in range(g[0], g[1] + 1)), '|', end=' ')
print(); print(len(ivs), 'intervalos')
