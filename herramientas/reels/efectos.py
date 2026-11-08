# Sintetiza los efectos de sonido del reel (golpe, tap, pop, whoosh, chime, riser) en ./Efectos
import numpy as np, os
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
os.makedirs('Efectos', exist_ok=True); sr = 48000
def save(n, x): x = x / np.max(np.abs(x)) * 0.9; wavfile.write(f'Efectos/{n}', sr, (x * 32767).astype(np.int16))
t = lambda d: np.arange(int(sr * d)) / sr
a = t(0.5); save('golpe.wav', np.sin(2*np.pi*(55+60*np.exp(-a*20))*a)*np.exp(-a*7)+0.3*np.random.randn(len(a))*np.exp(-a*40))
a = t(0.06); save('tap.wav', np.sin(2*np.pi*1800*a)*np.exp(-a*90))
a = t(0.15); f = 500+900*np.exp(-a*25); save('pop.wav', np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-a*28))
a = t(0.45); n = np.random.randn(len(a)); env = np.sin(np.pi*a/0.45)**2; y = np.zeros_like(n)
for i in range(0, len(n), 480):
    fc = 300+3500*(i/len(n)); sos = butter(2, [fc*0.6, fc*1.4], btype='band', fs=sr, output='sos'); y[i:i+480] = sosfilt(sos, n[i:i+480])
save('whoosh.wav', y*env)
a = t(1.2); save('chime.wav', (np.sin(2*np.pi*1318*a)+0.7*np.sin(2*np.pi*1975*a))*np.exp(-a*3.5))
a = t(1.0); f = 200+1200*a**2; save('riser.wav', (np.sin(2*np.pi*np.cumsum(f)/sr)*0.5+0.15*np.random.randn(len(a)))*(a**1.5))
