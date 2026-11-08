# Corta tramos de vert.mp4 / mate / audio de la toma según cut.json, sincroniza palabras y une (1.15x, color, cola)
import json, subprocess, sys, os
D = sys.argv[1]; toma = sys.argv[2]; os.chdir(D); os.makedirs('parts', exist_ok=True)
c = json.load(open('cut.json')); ivs = c['ivs']; SP = 1.15; TAIL = 2.6
fr = []
for k, (s, e) in enumerate(ivs):
    d = e - s
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(s),'-i','vert.mp4','-t',f'{d:.3f}','-c:v','libx264','-preset','fast','-crf','12','-an',f'parts/v{k}.mp4'],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(s),'-i','mate/mate_full.mkv','-t',f'{d:.3f}','-c:v','ffv1',f'parts/m{k}.mkv'],check=True)
    n = int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',f'parts/v{k}.mp4'],capture_output=True,text=True).stdout)
    fr.append((n, n))
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(s),'-i',toma,'-t',f'{d:.3f}','-vn','-af',f'afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012,apad,atrim=0:{n/30:.5f}','-ar','48000','-ac','1','-c:a','pcm_s16le',f'parts/b{k}.wav'],check=True)
for x, ext in (('v','mp4'),('m','mkv'),('b','wav')):
    open(f'parts/{x}.txt','w').write(''.join(f"file '{x}{k}.{ext}'\n" for k in range(len(ivs))))
ws = json.load(open('words_raw.json')); words = c['words']
starts = []; acc = 0
for n, m in fr: starts.append(acc); acc += n / 30
for w in words:
    i = w['src']
    k = next(k for k, (s, e) in enumerate(ivs) if s - 0.01 <= ws[i]['s'] <= e)
    w['s'] = round((starts[k] + ws[i]['s'] - ivs[k][0]) / SP, 3); w['e'] = round((starts[k] + w.get('e_raw', ws[i]['e']) - ivs[k][0]) / SP, 3)
c['dur'] = acc / SP; c['frames'] = fr
json.dump(c, open('cut.json','w'), ensure_ascii=False)
G = "eq=contrast=1.06:saturation=1.05:gamma=0.98,colorbalance=rs=0.03:gs=0.01:bs=-0.03:rm=0.02:bm=-0.02,hqdn3d=1.5:1.5:3:3,vignette=PI/5"
subprocess.run(f'ffmpeg -y -v error -f concat -safe 0 -i parts/v.txt -vf "setpts=PTS/{SP},fps=30,{G},tpad=stop_mode=clone:stop_duration={TAIL}" -c:v libx264 -preset fast -crf 12 base.mp4', shell=True, check=True)
subprocess.run(f'ffmpeg -y -v error -f concat -safe 0 -i parts/m.txt -vf "setpts=PTS/{SP},fps=30,tpad=stop_mode=clone:stop_duration={TAIL},format=gray" -c:v ffv1 mate/mate.mkv', shell=True, check=True)
subprocess.run(f'ffmpeg -y -v error -f concat -safe 0 -i parts/b.txt -af "atempo={SP},highpass=f=80,afftdn=nf=-25,deesser=i=0.3,apad=pad_dur={TAIL}" -ar 48000 -c:a pcm_s16le voz.wav', shell=True, check=True)
N = int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0','base.mp4'],capture_output=True,text=True).stdout)
print('dur', round(acc / SP, 2), 'frames base', N)
