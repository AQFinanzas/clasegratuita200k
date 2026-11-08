import onnxruntime as ort, numpy as np, subprocess, sys
src, dst = sys.argv[1], sys.argv[2]
w, h = 540, 960
sess = ort.InferenceSession('/home/claude/reels/rvm.onnx', providers=['CPUExecutionProvider'])
rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{w}x{h}', '-r', '30', '-i', '-',
                       '-vf', 'scale=1080:1920:flags=bicubic', '-c:v', 'ffv1', '-pix_fmt', 'gray', dst], stdin=subprocess.PIPE)
rec = [np.zeros([1, 1, 1, 1], dtype=np.float32)] * 4
dr = np.array([0.4], dtype=np.float32)
prev = None; n = 0
while True:
    b = rd.stdout.read(w * h * 3)
    if len(b) < w * h * 3: break
    x = np.frombuffer(b, np.uint8).reshape(h, w, 3).transpose(2, 0, 1)[None].astype(np.float32) / 255
    fgr, pha, *rec = sess.run(None, {'src': x, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3], 'downsample_ratio': dr})
    a = pha[0, 0]
    if prev is not None: a = 0.6 * a + 0.4 * prev  # suavizado temporal
    prev = a
    wr.stdin.write((np.clip(a, 0, 1) * 255).astype(np.uint8).tobytes()); n += 1
    if n % 300 == 0: print(n, flush=True)
wr.stdin.close(); wr.wait(); print('fin', n)
