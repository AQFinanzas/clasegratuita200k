import subprocess, numpy as np
U='/mnt/user-data/uploads/Downloads/'
def best_start(mp3, dur):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',mp3,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,np.int16).astype(float);sr=8000;e=np.convolve(x**2,np.ones(sr)/sr,'valid')[::sr];n=int(dur)
    return max(range(0,max(1,len(e)-n-2)),key=lambda s:e[s:s+n].mean())
J=[('m1_ahorrar','aq-musica-r1'),('m3_billetera','aq-musica-r2'),('m4_paraeso','aq-musica-r3'),('m5_bebe','aq-musica-r4'),('m6_dinos','aq-musica-r5'),('m7_disimular','aq-musica-r6'),('m8_hack','pista1-motivational-rise'),('m9_raro','aq-musica-r3'),('m10_fase2','pista3-cinematic')]
dur=13.5
for n,m in J:
    mp3=U+m+'.mp3';s=best_start(mp3,dur)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'{n}_silent.mp4','-ss',str(s),'-t',str(dur),'-i',mp3,'-filter_complex',f'[1:a]afade=t=in:d=0.4,afade=t=out:st={dur-1.5}:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=11[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-shortest',f'{n}.mp4'],check=True)
    print(n,m,s)
