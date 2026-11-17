import subprocess, numpy as np, sys
def best_start(mp3, dur):
    raw = subprocess.run(['ffmpeg','-loglevel','error','-i',mp3,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout
    x = np.frombuffer(raw,np.int16).astype(float); sr=8000
    e = np.convolve(x**2, np.ones(sr)/sr, 'valid')[::sr]  # energía por segundo
    n=int(dur); tot=len(e)
    best=max(range(0,max(1,tot-n-2)), key=lambda s: e[s:s+n].mean() + (0 if s>5 else -1e12*0))
    return best
for name,dur in [('r2_baterias',15.5),('r3_quincena',17.5),('r4_caja',17.5),('r5_tuberia',17.5),('r6_jean',18)]:
    mp3=f'/mnt/user-data/uploads/Downloads/aq-musica-{name[:2]}.mp3'
    s=best_start(mp3,dur)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'{name}_silent.mp4','-ss',str(s),'-t',str(dur),'-i',mp3,
      '-filter_complex',f'[1:a]afade=t=in:d=0.4,afade=t=out:st={dur-1.5}:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
      '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-shortest',f'{name}.mp4'],check=True)
    print(name,'start',s)
