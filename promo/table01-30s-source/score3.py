# Original cinematic score for the Takween Table 01 ad (37 s), synthesized from scratch.
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
T = 30.0
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


BEAT = 0.6   # 100 bpm, cuts every 4 beats (2.4 s)
CH = {'Dm':[50,57,62,65],'Bb':[46,58,62,65],'F':[41,57,60,65],'C':[48,55,60,64],'Gm':[43,58,62,67],'Am':[45,57,60,64],'Dm9':[38,57,62,64,65]}
def snap(g=0.16):
    t=np.arange(int(0.25*SR))/SR
    n=bp(rng.standard_normal(len(t)),1200,6000)*np.exp(-t*28)
    b=np.sin(2*np.pi*190*t)*np.exp(-t*40)*0.4
    return (n+b)*g
def bass(n,dur,g=0.22):
    t=np.arange(int(dur*SR))/SR; f=hz(n)
    s=np.sin(2*np.pi*f*t)+0.35*np.sin(4*np.pi*f*t)
    return lp(s,500)*np.minimum(1,t/0.01)*np.exp(-t*1.2)*g
def mech(g=0.18):
    t=np.arange(int(0.5*SR))/SR
    c=hp(rng.standard_normal(len(t)),2500)*np.exp(-t*90)*0.6
    th=np.sin(2*np.pi*np.cumsum(70+80*np.exp(-t*25))/SR)*np.exp(-t*14)
    return (c+th)*g
def slide(dur=0.45,g=0.1):
    t=np.arange(int(dur*SR))/SR; x=rng.standard_normal(len(t))
    return bp(x,800,3500)*np.sin(np.pi*t/dur)**2*g

# 0-3 hook
add(pad([38,45,50],3.4,att=.6,cut=700,g=0.11),0)
add(boom(.8),0.0)
for k in range(5): add(tick(.06),0.2+k*0.6,.3)
add(piano(74,.35,3),0.2,-.3); add(piano(77,.33,3),1.5,.3)
add(snap(.12),1.5); add(riser(1.4,.25),1.6)
# 3-7.2 sensory groove
for i,c in enumerate(['Dm','Bb']):
    t0=3.0+i*2.4 if i==0 else 5.4
for b in range(7):
    tb=3.0+b*0.6; add(kick(.34),tb); add(tick(.045),tb+0.3,.3)
    add(bass(38 if b<4 else 34,0.55,.2),tb)
add(pad(CH['Dm'],2.4,att=.1,rel=.8,cut=1500,g=.07),3.0); add(pad(CH['Bb'],1.8,att=.1,rel=.8,cut=1700,g=.07),5.4)
for tc in (4.0,5.0): add(whoosh(.5,.1),tc-.3); add(snap(.14),tc)
# reverse assembly 5.0-6.4 : reversed riser + slam
add(riser(1.3,.3),5.05); add(boom(.9),6.4); add(mech(.25),6.4); add(snap(.18),6.4)
add(shimmer(1.2,.04),6.4)
# 7.2-14.4 carousel drop
add(boom(.7),7.2)
prog=['Dm','Bb','F','C']
for i in range(3):
    c=prog[i%4]; t0=7.2+i*2.4
    add(pad(CH[c],2.4,att=.1,rel=.8,cut=1800+i*150,g=.075),t0)
    add(strings([n+12 for n in CH[c][1:]],2.4,att=.3,rel=1,g=.035),t0)
    for b in range(4):
        tb=t0+b*0.6; add(kick(.36),tb); add(tick(.045),tb+0.3,.3)
        if b in (1,3): add(snap(.14),tb)
        add(bass(CH[c][0]-12 if CH[c][0]>40 else CH[c][0],0.55,.21),tb)
    for k in range(8): add(piano(CH[c][[1,2,3,2,3,2,1,2][k]]+24,.17,1.4),t0+k*0.3,(-.3 if k%2 else .3))
for k in range(1,6): add(whoosh(.55,.12),7.2+0.55+k*1.0,(.4 if k%2 else -.4)); add(tick(.07),7.2+0.9+k*1.0)
# 14.4-19.2 price: half-time, merge hit
add(pad(CH['Gm'],2.0,att=.2,rel=.8,cut=1400,g=.08),14.4)
for k in range(3): add(chime_ := None) if False else None
for k,tt in enumerate([14.6,14.8,15.0]): add(piano([79,83,86][k],.3,2.5),tt)
add(riser(1.0,.28),15.25); add(boom(.9),16.25); add(shimmer(3.0,.05),16.25)
add(pad(CH['F'],3.0,att=.1,rel=1.0,cut=2200,g=.085),16.25); add(strings([69,72,77,81],3.0,att=.2,rel=1.2,g=.05),16.25)
for b in range(5):
    tb=16.25+b*0.6; add(kick(.33),tb); add(tick(.045),tb+0.3,.3)
    if b%2: add(snap(.13),tb)
    add(bass(29,0.55,.21),tb)
for i,n in enumerate([81,84,86,89]): add(piano(n,.25,2),16.5+i*0.3)
# 19.2-22.8 teardown
add(whoosh(.6,.14),18.9); add(boom(.6),19.2)
add(pad([38,45,50,52],3.6,att=.3,cut=700,g=.1),19.2)
for k,tt in enumerate([19.6,20.0,20.4,20.8,21.2,21.6,22.0]):
    add(slide(.4,.1),tt-.15,(.4 if k%2 else -.4)); add(mech(.17),tt+.15)
for b in range(6): add(kick(.25),19.2+b*0.6)
add(riser(1.2,.32),21.6)
# 22.8 packshot
add(boom(1.0),22.8); add(snap(.2),22.8)
add(pad(CH['Dm9'],7.0,att=.05,rel=1.4,cut=2400,g=.1),22.8)
add(strings([62,69,74,77],6.8,att=.4,rel=1.6,g=.05),22.8)
add(whoosh(2.4,.12),23.1,-.3)
for k in range(10): add(tick(.05),23.8+k*0.07,(.5 if k%2 else -.5))
add(snap(.16),24.6)
for i,n in enumerate([74,77,81,86]): add(piano(n,.3,3),24.7+i*0.3,(-.3+i*.2))
for b in range(8): add(kick(.25),24.8+b*0.6)
add(boom(.75),27.7); add(shimmer(2.4,.05),27.7)
for i,n in enumerate([86,89,93,98]): add(piano(n,.28,2.5),27.75+i*0.18)
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
