# Hero packshot (7.2 s @30fps): push-in, drifting smoke, swaying beams, dust, orbiting copper light ring, glitch title, CTA.
import numpy as np, os, math
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS, DUR = 1080, 1920, 30, 7.2
NF = int(DUR * FPS)
os.makedirs('pk', exist_ok=True)
rng = np.random.default_rng(3)
base = np.asarray(Image.open('s0.png').convert('RGB').resize((W, 1910)).resize((W, H)), np.float32) / 255
T = {k: np.asarray(Image.open(f't_{k}.png').convert('RGBA'), np.float32) / 255 for k in ['tag', 'en', 'ar', 'sub', 'wm', 'cta']}
cl = lambda v: max(0.0, min(1.0, v))
ease = lambda v: 1 - (1 - cl(v)) ** 3
def back(v):
    v = cl(v); c = 1.7; return 1 + (c + 1) * (v - 1) ** 3 + c * (v - 1) ** 2

# --- smoke: fbm value noise
def vnoise(shape, seed):
    r = np.random.default_rng(seed); return r.random(shape).astype(np.float32)
G = [vnoise((14, 26), 1), vnoise((28, 50), 2), vnoise((56, 100), 3)]
def sample(g, xs, ys):
    h, w = g.shape
    x = xs % (w - 1); y = np.clip(ys, 0, h - 1.001)
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int); fx = x - x0; fy = y - y0
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    a = g[y0, x0]; b = g[y0, x0 + 1]; c = g[y0 + 1, x0]; d = g[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy
sw, shh = 270, 480
yy, xx = np.mgrid[0:shh, 0:sw].astype(np.float32)
smask = np.clip((yy / shh - 0.38) / 0.25, 0, 1) * np.clip((0.97 - yy / shh) / 0.1, 0, 1)
def smoke(t):
    n = 0
    for i, (g, amp) in enumerate(zip(G, (0.55, 0.3, 0.15))):
        h, w = g.shape
        n = n + amp * sample(g, xx / sw * (w - 1) * 0.9 + t * (0.35 + i * 0.25), yy / shh * (h - 1) - t * 0.05 * (i + 1))
    v = np.clip((n - 0.42) * 2.2, 0, 1) * smask
    return np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255

# --- beams
by, bx = np.mgrid[0:shh, 0:sw].astype(np.float32)
def beam(t, ox, oy, a0, sway, width, freq):
    ang = np.arctan2(by - oy, bx - ox)
    a = a0 + sway * math.sin(t * freq)
    d = np.hypot(bx - ox, by - oy) / shh
    return np.exp(-((ang - a) / width) ** 2) * np.exp(-d * 1.4)
def beams(t):
    b = beam(t, 10, -20, 1.05, 0.05, 0.07, 0.9) + beam(t, 260, -20, 2.05, 0.05, 0.06, 1.1) + 0.6 * beam(t, 135, -40, 1.57, 0.08, 0.05, 0.7)
    fl = 0.85 + 0.15 * math.sin(t * 13) * math.sin(t * 7.3)
    return np.asarray(Image.fromarray(np.clip(b * 255, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255 * fl

# --- dust
P = rng.random((140, 4)).astype(np.float32)
def dust(t):
    im = Image.new('L', (W, H)); d = ImageDraw.Draw(im)
    for px, py, ps, ph in P:
        x = px * W + 20 * math.sin(t * 0.8 + ph * 6); y = ((py * H * 0.9) - t * (20 + 50 * ps)) % (H * 0.9) + 100
        r = 1.5 + 3 * ps; a = int(120 + 135 * (0.5 + 0.5 * math.sin(t * 3 + ph * 9)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=a)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(2)), np.float32) / 255

# --- ring
CX, CY, RX, RY, TILT = 530, 1175, 505, 150, -0.04
TB = (84, 985, 978, 1340)  # table bbox (occludes back arc)
def ring(t):
    lay = Image.new('L', (W, H)); d = ImageDraw.Draw(lay)
    on = cl((t - 0.3) / 0.2)
    if on <= 0: return None
    prog = ease((t - 0.3) / 2.4)
    head = -math.pi / 2 + prog * 4 * math.pi
    full = cl((t - 2.6) / 0.4) * (1 - 0.75 * cl((t - 3.4) / 1.0))
    N = 160
    for k in range(N):
        th0 = head - k * 0.02; th1 = th0 - 0.02
        a = ((1 - k / N) ** 1.6) * on
        a = max(a, full * 0.8)
        if a < 0.02: continue
        pts = []
        for th in (th0, th1):
            x = CX + RX * math.cos(th); y = CY + RY * math.sin(th) + TILT * RX * math.cos(th)
            pts.append((x, y))
        midy = (pts[0][1] + pts[1][1]) / 2; midx = (pts[0][0] + pts[1][0]) / 2
        behind = math.sin(th0) < 0
        if behind and TB[0] < midx < TB[2] and TB[1] - 40 < midy < TB[3]: continue
        d.line(pts, fill=int(255 * a), width=7 if not behind else 5)
    core = np.asarray(lay, np.float32) / 255
    glow = np.asarray(lay.filter(ImageFilter.GaussianBlur(16)), np.float32) / 255
    glow2 = np.asarray(lay.filter(ImageFilter.GaussianBlur(50)), np.float32) / 255
    # head sparkle
    hx = CX + RX * math.cos(head); hy = CY + RY * math.sin(head) + TILT * RX * math.cos(head)
    sp = Image.new('L', (W, H)); ds = ImageDraw.Draw(sp)
    if on > 0 and t < 2.9 and not (math.sin(head) < 0 and TB[0] < hx < TB[2]):
        ds.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=255)
    spg = np.asarray(sp.filter(ImageFilter.GaussianBlur(12)), np.float32) / 255
    return core, glow, glow2, spg

def place(dst, layer, alpha, dx=0, dy=0, scale=1.0):
    if alpha <= 0: return dst
    L = layer
    if scale != 1.0:
        im = Image.fromarray((L * 255).astype(np.uint8), 'RGBA'); sw_ = int(W * scale); sh_ = int(H * scale)
        im = im.resize((sw_, sh_), Image.BILINEAR); c = Image.new('RGBA', (W, H)); c.paste(im, ((W - sw_) // 2 + dx, (H - sh_) // 2 + dy)); L = np.asarray(c, np.float32) / 255
    elif dx or dy:
        L = np.roll(np.roll(L, dy, 0), dx, 1)
    a = L[..., 3:4] * alpha
    return dst * (1 - a) + L[..., :3] * a

def glitch(L, amt, seed):
    r = np.random.default_rng(seed); out = L.copy()
    dx = int(r.integers(4, 16) * amt)
    out[..., 0] = np.roll(L[..., 0], dx, 1); out[..., 2] = np.roll(L[..., 2], -dx, 1)
    out[..., 3] = np.maximum(np.roll(L[..., 3], dx, 1), np.roll(L[..., 3], -dx, 1))
    for _ in range(int(3 * amt) + 1):
        y0 = int(r.integers(250, 560)); h = int(r.integers(6, 30)); s = int(r.integers(-40, 40) * amt)
        out[y0:y0 + h] = np.roll(out[y0:y0 + h], s, 1)
    return out

def wipe(L, frac, rtl=False, x0=0, x1=W):
    m = np.zeros((1, W, 1), np.float32); edge = x0 + (x1 - x0) * frac
    xs = np.arange(W)[None, :, None]
    m = np.clip((edge - xs) / 30 + 1, 0, 1) if not rtl else np.clip((xs - (x1 - (x1 - x0) * frac)) / 30 + 1, 0, 1)
    o = L.copy(); o[..., 3:4] *= m; return o

warm = np.array([1.0, 0.62, 0.36], np.float32)
for f in range(NF):
    t = f / FPS
    z = 1.0 + 0.075 * ease(t / DUR) + 0.04 * (1 - ease(t / 0.35))
    im = Image.fromarray((base * 255).astype(np.uint8)); sw_ = int(W * z); sh_ = int(H * z)
    im = im.resize((sw_, sh_), Image.BICUBIC).crop(((sw_ - W) // 2, int((sh_ - H) * 0.55), (sw_ - W) // 2 + W, int((sh_ - H) * 0.55) + H))
    fr = np.asarray(im, np.float32) / 255
    fr = fr + beams(t)[..., None] * warm * 0.22
    s = smoke(t)[..., None]
    fr = 1 - (1 - fr) * (1 - s * np.array([0.55, 0.38, 0.28], np.float32) * 0.9)
    fr = fr + dust(t)[..., None] * np.array([1.0, 0.8, 0.55], np.float32) * 0.55
    rg = ring(t)
    if rg:
        core, glow, glow2, spg = rg
        fr = fr + core[..., None] * np.array([1.0, 0.9, 0.75]) * 0.9 + glow[..., None] * np.array([1.0, 0.55, 0.22]) * 0.9 \
             + glow2[..., None] * np.array([1.0, 0.45, 0.15]) * 0.45 + spg[..., None] * np.array([1, 0.95, 0.85]) * 1.4
        # ring light spilling on the table when it passes in front
        fr = fr * (1 + 0.08 * (cl((t - 0.3) / .3) * (1 - cl((t - 3.6) / .8))))
    # texts
    fr = place(fr, T['tag'], cl((t - 0.8) / 0.4))
    if t >= 1.0:
        L = wipe(T['en'], ease((t - 1.0) / 0.7), x0=150, x1=930)
        g = 1 - cl((t - 1.75) / 0.25)
        if g > 0 and f % 3 != 2: L = glitch(L, g, f)
        fr = place(fr, L, 1.0)
    if t >= 1.9: fr = place(fr, wipe(T['ar'], ease((t - 1.9) / 0.6), rtl=True, x0=250, x1=830), 1.0)
    fr = place(fr, T['sub'], cl((t - 2.5) / 0.5), dy=int(20 * (1 - ease((t - 2.5) / 0.6))))
    fr = place(fr, T['wm'], cl((t - 4.4) / 0.5), dy=int(24 * (1 - ease((t - 4.4) / 0.6))))
    if t >= 4.9:
        sc = 0.75 + 0.25 * back((t - 4.9) / 0.5)
        fr = place(fr, T['cta'], cl((t - 4.9) / 0.2), scale=sc, dy=int(1700 * (1 - sc) * 0.5) if sc < 1 else 0)
    # flash in
    fr = fr + (1 - cl(t / 0.18)) * 0.8
    # vignette
    if f == 0:
        vy, vx = np.mgrid[0:H, 0:W].astype(np.float32); VG = np.clip(1 - 0.55 * (((vx - W / 2) / W) ** 2 + ((vy - H * 0.55) / H) ** 2) * 2.2, 0.45, 1)[..., None]
    fr = np.clip(fr * VG, 0, 1)
    Image.fromarray((fr * 255).astype(np.uint8)).save(f'pk/p{f:04d}.jpg', quality=94)
print('frames', NF)
