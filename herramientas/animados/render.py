import sys, base64, subprocess, pathlib
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).parent.resolve()
FPS = 30

def html(scene):
    return f"""<html><body style="margin:0;background:#000"><canvas id=c width=1080 height=1920></canvas>
<script>{(D/'common.js').read_text()}</script><script>{(D/(scene+'.js')).read_text()}</script>
<script>
window.ready=(async()=>{{
 await loadImg('logoW','file://{D}/logo-aq-blanco-transparente.png'); await loadImg('logoC','file://{D}/logo-aq-color-transparente.png');
 for (const f of ["900 80px 'Inter Display'","800 80px 'Inter Display'","700 40px Inter","600 40px Inter","500 40px Inter","900 40px Inter","800 40px Inter"]) await document.fonts.load(f);
 if (window.setup) await setup();
 return true;}})();
window.frame=(t,q)=>{{const ctx=document.getElementById('c').getContext('2d');ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;draw(ctx,t);return document.getElementById('c').toDataURL('image/jpeg',q);}};
</script></body></html>"""

def run(scene, mode):
    (D/f'{scene}.html').write_text(html(scene))
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width':1080,'height':1920})
        pg.goto(f'file://{D}/{scene}.html'); pg.evaluate('window.ready')
        dur = pg.evaluate('DUR')
        if mode == 'preview':
            ts = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [dur*i/8 for i in range(8)]
            for i, t in enumerate(ts):
                u = pg.evaluate(f'frame({t},0.85)'); (D/f'prev_{scene}_{i}.jpg').write_bytes(base64.b64decode(u.split(',')[1]))
            print('preview', ts)
        else:
            out = D/f'{scene}_silent.mp4'
            ff = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
                                   '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(out)], stdin=subprocess.PIPE)
            n = int(dur*FPS)
            for i in range(n):
                u = pg.evaluate(f'frame({i/FPS},0.93)'); ff.stdin.write(base64.b64decode(u.split(',')[1]))
            ff.stdin.close(); ff.wait(); print('ok', out, n)
        b.close()

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'video')
