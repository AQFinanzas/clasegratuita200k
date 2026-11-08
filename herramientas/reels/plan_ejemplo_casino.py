import json, subprocess
ws = json.load(open('/home/claude/r3/words_raw.json'))
fix = {277: 'Esto', 25: 'vengo', 26: 'a', 235: 'mis', 56: 'aquellas', 57: 'historias', 128: 'vale', 231: 'de que', 236: 'manos', 246: 'cirujano', 248: 'oye,', 250: 'opérame', 263: 'sí', 267: 'sí', 150: 'metodología,'}
drop = {110, 111, 119, 129, 130, 249}
for k, v in fix.items(): ws[k]['w'] = v
ranges = [(277, 281), (19, 39), (55, 69), (70, 92), (93, 106), (107, 141), (217, 239), (240, 257), (258, 270), (282, 292)]
keys = {281, 22, 33, 69, 85, 100, 138, 228, 257, 270, 287, 292}
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
MAN = [[277, 279], [280, 281], [19, 22], [23, 27], [28, 31], [32, 33], [34, 36], [37, 39], [55, 57], [58, 61], [62, 65], [66, 69], [70, 72], [73, 75], [76, 77], [78, 81], [82, 85], [86, 89], [90, 92], [93, 95], [96, 97], [98, 100], [101, 103], [104, 106], [107, 109], [112, 114], [115, 118], [120, 122], [123, 125], [126, 128], [131, 132], [133, 135], [136, 138], [139, 141], [217, 220], [221, 221], [222, 225], [226, 228], [229, 230], [231, 233], [234, 236], [237, 239], [240, 243], [244, 247], [248, 250], [251, 253], [254, 255], [256, 257], [258, 259], [260, 262], [263, 265], [266, 270], [282, 284], [285, 287], [288, 290], [291, 292]]
groups = [[idxmap[a], idxmap[b]] for a, b in MAN]
json.dump({'ivs': [[round(a, 3), round(b, 3)] for a, b, _ in ivs], 'words': words, 'groups': groups, 'idxmap': idxmap, 'dur': dur}, open('/home/claude/r3/cut.json', 'w'), ensure_ascii=False, indent=0)
for g in groups: print(' '.join(words[k]['w'] for k in range(g[0], g[1] + 1)), '|', end=' ')
print(); print(len(ivs), 'intervalos')
