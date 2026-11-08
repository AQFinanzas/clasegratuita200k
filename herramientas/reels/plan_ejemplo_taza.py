import json, subprocess
ws = json.load(open('/home/claude/r2/words_raw.json'))
fix = {17: 'Alejandro,', 169: 'compra', 277: 'le', 46: '¿pero', 47: 'cómo', 49: 'eso?', 50: '¿llenar', 52: 'taza?', 53: 'Sí.'}
drop = {33, 34, 120, 121, 190}
ranges = [(17, 24), (35, 42), (43, 53), (54, 67), (85, 93), (94, 106), (110, 116), (117, 128), (130, 144), (145, 155), (161, 171), (172, 178), (191, 201), (262, 274), (275, 281)]
for k, v in fix.items(): ws[k]['w'] = v
keys = {42, 59, 87, 103, 116, 128, 144, 155, 171, 201, 274, 281}
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
    if ivs[k][0] < ivs[k - 1][1]: m = (ivs[k][0] + ivs[k - 1][1]) / 2; ivs[k - 1][1] = m; ivs[k][0] = m
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
MAN = [[17, 20], [21, 24], [35, 36], [37, 38], [39, 42], [43, 45], [46, 49], [50, 53], [54, 55], [56, 58], [59, 59], [60, 63], [64, 67], [85, 87], [88, 90], [91, 93], [94, 96], [97, 99], [100, 103], [104, 106], [110, 111], [112, 114], [115, 116], [117, 119], [122, 124], [125, 128], [130, 132], [133, 134], [135, 137], [138, 141], [142, 144], [145, 148], [149, 151], [152, 155], [161, 164], [165, 168], [169, 171], [172, 174], [175, 178], [191, 193], [194, 196], [197, 199], [200, 201], [262, 263], [264, 265], [266, 268], [269, 270], [271, 274], [275, 278], [279, 281]]
groups = [[idxmap[a], idxmap[b]] for a, b in MAN]
json.dump({'ivs': [[round(a, 3), round(b, 3)] for a, b, _ in ivs], 'words': words, 'groups': groups, 'idxmap': idxmap, 'dur': dur}, open('/home/claude/r2/cut.json', 'w'), ensure_ascii=False, indent=0)
for g in groups: print(' '.join(words[k]['w'] for k in range(g[0], g[1] + 1)), '|', end=' ')
print(); print(len(ivs), 'intervalos')
