# Original cinematic score for the Takween Table 01 ad (37 s), synthesized from scratch.
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
T = 37.5
N = int(SR * T)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def add(sig, t0, pan=0.0, g=1.0):
    i = int(t0 * SR)
    if i >= N: return
    s = sig[: N - i] * g
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(s)] += s * l * 1.414; R[i:i + len(s)] += s * r * 1.414

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def hz(n): return 440 * 2 ** ((n - 69) / 12)

def piano(n, vel=0.5, dur=4.0):
    f = hz(n); t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for k in range(1, 10):
        fk = f * k * np.sqrt(1 + 0.00035 * k * k)
        if fk > 15000: break
        s += (1 / k ** 1.25) * np.sin(2 * np.pi * fk * t + rng.random()) * np.exp(-t * (0.9 + 0.55 * k) * (f / 400) ** 0.3)
    s *= np.minimum(1, t / 0.004)
    ham = lp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 60) * 0.08
    return lp((s + ham) * vel, 7000 if vel > .4 else 4500) * 0.35

def pad(notes, dur, att=1.5, rel=2.0, cut=1400, g=0.06):
    t = np.arange(int((dur + rel) * SR)) / SR; s = np.zeros_like(t)
    for n in notes:
        for d in (-0.07, 0, 0.06):
            f = hz(n) * 2 ** (d / 12); ph = rng.random()
            s += 2 * (((t * f + ph) % 1) - 0.5)
    env = np.minimum(1, t / att) * np.clip((dur + rel - t) / rel, 0, 1)
    return lp(s, cut, 2) * env * g / len(notes)

def strings(notes, dur, att=2.0, rel=2.5, g=0.05):
    t = np.arange(int((dur + rel) * SR)) / SR; s = np.zeros_like(t)
    for n in notes:
        f = hz(n)
        vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)
        s += np.sin(2 * np.pi * np.cumsum(f * vib) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f * vib) / SR)
    env = np.minimum(1, t / att) ** 2 * np.clip((dur + rel - t) / rel, 0, 1)
    return s * env * g / len(notes)

def boom(g=0.9):
    t = np.arange(int(2.5 * SR)) / SR
    f = 32 + 55 * np.exp(-t * 7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    n = lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 9) * 0.35
    return np.tanh((s + n) * 1.6) * g

def riser(dur, g=0.25):
    t = np.arange(int(dur * SR)) / SR; x = rng.standard_normal(len(t)); out = np.zeros_like(t)
    seg = int(0.05 * SR)
    for i in range(0, len(t), seg):
        c = 300 * (1 + 30 * (i / len(t)) ** 2)
        out[i:i + seg] = bp(x[max(0, i - 2000):i + seg], c, min(c * 1.8, 20000))[-len(out[i:i + seg]):]
    return out * (t / dur) ** 2.2 * g

def whoosh(dur=1.0, g=0.18):
    t = np.arange(int(dur * SR)) / SR; x = rng.standard_normal(len(t))
    env = np.sin(np.pi * t / dur) ** 2
    return bp(x, 400, 5000) * env * g

def kick(g=0.35):
    t = np.arange(int(0.5 * SR)) / SR
    f = 45 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * g

def tick(g=0.05):
    t = np.arange(int(0.04 * SR)) / SR
    return hp(rng.standard_normal(len(t)), 6000) * np.exp(-t * 180) * g

def shimmer(dur, g=0.03):
    t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for n in (86, 90, 93, 98):
        s += np.sin(2 * np.pi * hz(n) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * (0.3 + rng.random() * .4) * t + rng.random() * 6))
    return s * np.minimum(1, t / 1.5) * np.clip((dur - t) / 1.5, 0, 1) * g / 4

BEAT = 60 / 84
# chords (MIDI): Dm, Bb, F, C, Gm
CH = {'Dm': [50, 57, 62, 65], 'Bb': [46, 58, 62, 65], 'F': [41, 57, 60, 65], 'C': [48, 55, 60, 64], 'Gm': [43, 58, 62, 67], 'Dm9': [38, 57, 62, 64, 65]}

# --- 0-4 : intro, drone + sparse piano
add(pad([38, 45, 50], 4.6, att=2.5, cut=700, g=0.1), 0.0)
add(shimmer(5.0), 0.2, 0.0)
for t0, n, p in [(0.6, 74, -.3), (1.9, 69, .3), (2.8, 72, -.2), (3.4, 77, .2)]:
    add(piano(n, .32, 5), t0, p)
add(riser(1.2, .18), 2.85)
add(whoosh(1.0, .12), 3.3, .2)

# --- 4.0 hero hit, progression 4 - 32
add(boom(.95), 4.0)
prog = ['Dm', 'Bb', 'F', 'C', 'Dm', 'Bb', 'Gm', 'C', 'F', 'C', 'Dm', 'Bb']
bar = BEAT * 4 * 0.7  # ~2.0 s per chord
t = 4.0
arp = [0, 2, 3, 2, 1, 3, 2, 3]
for ci, c in enumerate(prog):
    notes = CH[c]
    add(pad(notes, bar, att=.6, rel=1.2, cut=1100 + ci * 60, g=0.075), t)
    if ci >= 4: add(strings([n + 12 for n in notes[1:]], bar, att=.8, rel=1.6, g=0.035 + ci * 0.002), t, 0.0)
    step = bar / 8
    for k in range(8):
        n = notes[arp[k] % len(notes)] + 24
        add(piano(n, 0.22 + 0.06 * (k % 4 == 0), 2.5), t + k * step, (-.35 if k % 2 else .35))
    t += bar
end_prog = t  # ~ 28.0
# pulse from 8.5
tb = 8.5
while tb < 31.6:
    add(kick(.26 if tb < 27 else .32), tb)
    tb += BEAT
# precision ticks during the caliper shot 19.5-23.5
tt = 19.5
while tt < 23.4:
    add(tick(.05), tt, .4); add(tick(.03), tt + BEAT / 2, -.4); tt += BEAT
# transitions
for tc in (8.5, 12.0, 15.5, 19.5, 23.5, 27.0):
    add(whoosh(.9, .08), tc - .55, (.3 if tc % 2 else -.3))

# --- 28-32 lift
lift = ['F', 'C', 'Gm', 'Bb']
t = end_prog
for c in lift:
    d = (32.0 - end_prog) / 4
    add(pad(CH[c], d, att=.4, rel=1.0, cut=2200, g=0.085), t)
    add(strings([n + 12 for n in CH[c][1:]] + [CH[c][-1] + 24], d, att=.4, rel=1.2, g=0.05), t)
    add(piano(CH[c][-1] + 24, .4, 3), t)
    t += d
add(riser(3.4, .3), 28.6)

# --- 32 end card: big hit + resolve
add(boom(1.0), 32.0)
add(pad(CH['Dm9'], 4.2, att=.05, rel=1.4, cut=2600, g=0.11), 32.0)
add(strings([62, 69, 74, 77], 4.0, att=.3, rel=1.6, g=0.055), 32.0)
for i, n in enumerate([74, 76, 77, 81, 86]):
    add(piano(n, .38 - i * .03, 5), 32.15 + i * 0.34, (-.3 + i * .15))
add(shimmer(5.0, .04), 32.2)

# reverb
ir_len = int(3.2 * SR); ti = np.arange(ir_len) / SR
irL = rng.standard_normal(ir_len) * np.exp(-ti * 2.1); irR = rng.standard_normal(ir_len) * np.exp(-ti * 2.1)
irL = lp(irL, 6000); irR = lp(irR, 6000); irL /= np.abs(irL).sum() ** .5 * 6; irR /= np.abs(irR).sum() ** .5 * 6
wL = fftconvolve(L, irL)[:N]; wR = fftconvolve(R, irR)[:N]
L2 = L + wL * .55; R2 = R + wR * .55
# fade out tail
fo = np.clip((T - np.arange(N) / SR) / 1.2, 0, 1)
L2 *= fo; R2 *= fo
m = max(np.abs(L2).max(), np.abs(R2).max())
L2 = np.tanh(L2 / m * 1.3) * 0.89; R2 = np.tanh(R2 / m * 1.3) * 0.89
out = np.stack([L2, R2], 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('ok', T)
