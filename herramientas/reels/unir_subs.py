# Une subtítulos que duran menos de 0,4 s (máx. 4 palabras, sin cruzar fin de frase)
import json, sys
f = sys.argv[1]; c = json.load(open(f)); w = c['words']; gs = c['groups']
def dur(k): return (w[gs[k+1][0]]['s'] if k+1 < len(gs) else 99) - w[gs[k][0]]['s']
n = lambda g: g[1]-g[0]+1
endp = lambda g: w[g[1]]['raw'][-1:] in '.?'
ch = True
while ch:
    ch = False
    for k in range(len(gs)):
        if dur(k) >= 0.4: continue
        if k+1 < len(gs) and n(gs[k])+n(gs[k+1]) <= 4 and not endp(gs[k]): gs[k] = [gs[k][0], gs[k+1][1]]; del gs[k+1]; ch = True; break
        if k > 0 and n(gs[k])+n(gs[k-1]) <= 4 and not endp(gs[k-1]): gs[k-1] = [gs[k-1][0], gs[k][1]]; del gs[k]; ch = True; break
json.dump(c, open(f, 'w'), ensure_ascii=False)
print('cortos restantes', [round(dur(k),2) for k in range(len(gs)) if dur(k) < 0.4])
