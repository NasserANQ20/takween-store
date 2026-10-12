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

B=0.5
def k808(n,dur,g=.5,glide=0):
    t=np.arange(int(dur*SR))/SR; f=hz(n)*(1+glide*np.exp(-t*10))
    s=np.sin(2*np.pi*np.cumsum(f)/SR)
    return np.tanh(s*np.exp(-t*1.3)*2.2)*np.minimum(1,t/0.003)*g
def kk(g=.55):
    t=np.arange(int(.35*SR))/SR; f=50+140*np.exp(-t*40)
    return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*3)*g
def clap(g=.22):
    t=np.arange(int(.3*SR))/SR; x=rng.standard_normal(len(t)); e=np.zeros_like(t)
    for o in (0,.011,.022): e+=np.exp(-np.clip(t-o,0,None)*120)*(t>=o)
    e+=np.exp(-t*18)*.5
    return bp(x,900,5000)*e*g
def hh(g=.06,dec=70):
    t=np.arange(int(.08*SR))/SR; return hp(rng.standard_normal(len(t)),8000)*np.exp(-t*dec)*g
def stab(notes,g=.09,dur=.35):
    t=np.arange(int(dur*SR))/SR; s=np.zeros_like(t)
    for n in notes:
        for d in (-.08,.08): s+=2*(((t*hz(n)*2**(d/12))%1)-.5)
    cut=lp(s,3200)*np.exp(-t*9)
    return cut*g/len(notes)
def pen(dur,g=.05):
    t=np.arange(int(dur*SR))/SR; x=rng.standard_normal(len(t))
    m=0.6+0.4*np.sin(2*np.pi*7*t)*np.sin(2*np.pi*2.3*t)
    return bp(x,2500,7000)*m*g
CHS={'Dm':[62,65,69,72],'Bb':[58,62,65,69],'F':[60,65,69,72],'C':[60,64,67,72]}
# 0-6 tension: drone + word hits
add(pad([38,45],6.2,att=.8,cut=500,g=.12),0)
for a in (0.35,1.6,3.1,4.6):
    add(kk(.5),a); add(stab(CHS['Dm'],.12,.5),a); add(whoosh(.35,.08),a-.3)
add(boom(.5),0.35)
for k in range(6): add(hh(.05),3.0+k*B)
for k in range(12): add(hh(.04+.002*k),4.6+k*B/4,(.3 if k%2 else -.3))
add(riser(1.4,.3),4.6)
# 6-26 groove
prog=['Dm','Bb','F','C']
bassn={'Dm':38,'Bb':34,'F':41,'C':36}
t=6.0
while t<26.0-1e-6:
    bar=int((t-6.0)/2.0); c=prog[bar%4]
    low = 23.5<=t<26.0
    for b in range(4):
        tb=t+b*B
        if not low or b==0: add(kk(.55 if b==0 else .45),tb)
        if b in (1,3) and not low: add(clap(.22),tb)
        for s in range(4):
            g=.055 if s%2==0 else .03
            if low: g*=.5
            add(hh(g),tb+s*B/4,(.35 if s%2 else -.35))
    add(k808(bassn[c],1.0,.42,glide=.6 if bar%2==0 else 0),t)
    add(k808(bassn[c]+(7 if bar%2 else 0),0.6,.32),t+1.25)
    for st in (0,0.75,1.5):
        add(stab(CHS[c],.07 if not low else .04,.3),t+st,(.25 if st else -.25))
    t+=2.0
add(boom(.9),6.0); add(snap(.2),6.0)
for a in range(12,18): add(stab([74,77,81],.08,.25),a); add(whoosh(.3,.07),a-.25)
add(boom(.6),12.0)
for a in (9.0,18.0,21.0,23.5): add(whoosh(.5,.12),a-.4); add(kk(.5),a)
add(riser(1.6,.3),24.4)
# 26-30 end
add(boom(1.0),26.0)
add(pad([38,50,57,62,65],4.2,att=.05,rel=1.2,cut=2200,g=.1),26.0)
for i,n in enumerate([74,77,81,86]): add(stab([n],.1,.6),26.2+i*.06,(-.3+i*.2))
add(pen(1.1,.06),27.1)
add(stab(CHS['F'],.1,.6),28.4); add(snap(.14),28.4)
# reverb
ir_len = int(3.2 * SR); ti = np.arange(ir_len) / SR
irL = rng.standard_normal(ir_len) * np.exp(-ti * 2.1); irR = rng.standard_normal(ir_len) * np.exp(-ti * 2.1)
irL = lp(irL, 6000); irR = lp(irR, 6000); irL /= np.abs(irL).sum() ** .5 * 6; irR /= np.abs(irR).sum() ** .5 * 6
wL = fftconvolve(L, irL)[:N]; wR = fftconvolve(R, irR)[:N]
L2 = L + wL * .18; R2 = R + wR * .18
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
