# Mezcla voz + efectos (sfx.json) y masteriza a -14 LUFS; exporta FINAL
import json, sys, subprocess, numpy as np, os
from scipy.io import wavfile
D, out = sys.argv[1], sys.argv[2]; os.chdir(D); E = '/home/claude/reels/Efectos/'
sr, v = wavfile.read('voz.wav'); v = v.astype(np.float32) / 32768
if v.ndim > 1: v = v.mean(1)
mix = v.copy(); vr = np.sqrt(np.mean(v[v != 0] ** 2))
for name, t0, db in json.load(open('sfx.json')):
    _, s = wavfile.read(E + name + '.wav'); s = s.astype(np.float32) / 32768
    s = s / (np.sqrt(np.mean(s ** 2)) + 1e-9) * vr * 10 ** ((db + 2) / 20)
    i = max(0, int(t0 * sr)); j = min(len(mix), i + len(s)); mix[i:j] += s[:j - i]
wavfile.write('mezcla.wav', sr, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
r = subprocess.run(['ffmpeg','-v','info','-i','mezcla.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'], capture_output=True, text=True).stderr
d = json.loads(r[r.rindex('{'):r.rindex('}')+1])
f = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true"
subprocess.run(['ffmpeg','-y','-v','error','-i','mezcla.wav','-af',f,'-ar','48000','master.wav'], check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i','video_graf.mp4','-i','master.wav','-map','0:v','-map','1:a','-c:v','libx264','-profile:v','high','-preset','slow','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart',out], check=True)
m = subprocess.run(['ffmpeg','-v','info','-i',out,'-af','ebur128=peak=true','-f','null','-'], capture_output=True, text=True).stderr
print([l.strip() for l in m.splitlines() if l.strip().startswith(('I:','Peak:'))][-2:])
