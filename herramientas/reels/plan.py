import json, subprocess
ws = json.load(open('/home/claude/reels/words_raw.json'))
fix = {28: 'lo', 29: 'financiero', 40: 'lo', 41: 'financiero', 52: '¿Ves', 55: 'tiene', 66: '5.000', 72: '7.000,', 78: '3.000,', 80: '2.000', 83: '1.000.', 89: 'aunque', 95: 'tiene'}
drop = {67, 84}
for k, v in fix.items(): ws[k]['w'] = v
ws[66]['e'] = ws[67]['e']; ws[83]['e'] = ws[84]['e']
ranges = [(23, 36), (37, 51), (52, 60), (61, 84), (85, 107), (108, 130), (148, 167), (175, 188)]
keys = {26, 33, 47, 60, 83, 100, 126, 157, 167, 186}
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
MAN = [[23,25],[26,26],[27,29],[30,31],[32,33],[34,36],[37,38],[39,41],[42,43],[44,45],[46,47],[48,49],[50,51],[52,54],[55,56],[57,58],[59,60],[61,63],[64,66],[68,68],[69,71],[72,72],[73,75],[76,78],[79,80],[81,82],[83,83],[85,85],[86,88],[89,91],[92,94],[95,96],[97,97],[98,100],[101,103],[104,105],[106,107],[108,109],[110,112],[113,115],[116,118],[119,119],[120,121],[122,124],[125,126],[127,128],[129,130],[148,150],[151,152],[153,155],[156,157],[158,158],[159,161],[162,164],[165,165],[166,167],[175,177],[178,179],[180,182],[183,185],[186,186],[187,188]]
groups = [[idxmap[a], idxmap[b]] for a, b in MAN]
json.dump({'ivs': [[round(a, 3), round(b, 3)] for a, b, _ in ivs], 'words': words, 'groups': groups, 'idxmap': idxmap, 'dur': dur}, open('/home/claude/reels/cut.json', 'w'), ensure_ascii=False, indent=0)
for g in groups: print(' '.join(words[k]['w'] for k in range(g[0], g[1] + 1)), '|', end=' ')
print(); print(len(ivs), 'intervalos')
