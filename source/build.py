"""Builds hazeldang.com.

Edit source/src.html, then run:  python3 source/build.py
It writes ../index.html (the live site, every image inlined so it is one file)
and source/artifact.html (the same page as a fragment, for previewing in Claude).
"""
import base64, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
A = os.path.join(HERE, 'assets')
SITE_URL = 'https://hazeldang.com/'


def uri(path):
    ext = path.rsplit('.', 1)[1].lower()
    mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'svg': 'image/svg+xml'}[ext]
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(path, 'rb').read()).decode())


def lerp(a, b, t):
    return a + (b - a) * t


def cart_svg():
    P1, P2 = '#eab1c3', '#d4789a'
    TL, TR, BR, BL = (78, 52), (302, 52), (274, 150), (104, 150)
    g = ['<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="rgba(247,219,228,.28)"/>' % (*TL, *TR, *BR, *BL)]
    n = 15
    for i in range(1, n):
        t = i / n
        g.append('<line x1="%.1f" y1="52" x2="%.1f" y2="150" stroke="%s" stroke-width="1.6"/>' % (lerp(TL[0], TR[0], t), lerp(BL[0], BR[0], t), P1))
    for y in range(64, 150, 12):
        t = (y - 52) / 98
        g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.6"/>' % (lerp(TL[0], BL[0], t), y, lerp(TR[0], BR[0], t), y, P1))
    g.append('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (*TL, *TR, *BR, *BL, P2))
    g.append('<line x1="74" y1="52" x2="306" y2="52" stroke="%s" stroke-width="5.5" stroke-linecap="round"/>' % P2)
    g.append('<path d="M80 54 L46 24" stroke="%s" stroke-width="5" stroke-linecap="round" fill="none"/>' % P2)
    g.append('<line x1="30" y1="19" x2="56" y2="29" stroke="#a63f5e" stroke-width="10" stroke-linecap="round"/>')
    g.append('<path d="M104 150 L112 196 M274 150 L264 196" stroke="%s" stroke-width="4.5" stroke-linecap="round" fill="none"/>' % P2)
    g.append('<line x1="96" y1="196" x2="280" y2="196" stroke="%s" stroke-width="5.5" stroke-linecap="round"/>' % P2)
    g.append('<line x1="114" y1="178" x2="262" y2="178" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % P1)
    for x in range(126, 262, 14):
        g.append('<line x1="%d" y1="178" x2="%d" y2="196" stroke="%s" stroke-width="1.4"/>' % (x, x, P1))

    def wheel(cx, cy, r, fill, hub):
        sp = ''.join('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>' % (cx, cy, cx + r * .8 * math.cos(a), cy + r * .8 * math.sin(a), hub) for a in (0, 2.094, 4.189))
        return '<g class="wheel"><circle cx="%d" cy="%d" r="%d" fill="%s"/>%s<circle cx="%d" cy="%d" r="%.1f" fill="%s"/></g>' % (cx, cy, r, fill, sp, cx, cy, r * .32, hub)

    g.append('<path d="M120 196 L120 210 M256 196 L256 210" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % P2)
    g.insert(0, wheel(158, 218, 11, '#e7a0b6', '#f8dde6') + wheel(236, 218, 11, '#e7a0b6', '#f8dde6'))
    g.append(wheel(120, 224, 15, '#a63f5e', '#f3c6d4') + wheel(256, 224, 15, '#a63f5e', '#f3c6d4'))
    return '<svg viewBox="0 0 320 250" role="img" aria-label="A pink shopping cart">%s</svg>' % ''.join(g)


def basket_svgs():
    P1, P2 = '#eab1c3', '#d4789a'
    FL, FR, BR_, BL_ = (52, 96), (252, 96), (232, 186), (74, 186)
    SR, SBR, BKL = (284, 70), (262, 162), (84, 70)
    back = ['<polygon points="%d,%d %d,%d %d,%d %d,%d %d,%d" fill="rgba(234,177,195,.32)"/>' % (*BKL, *SR, *SBR, *BR_, *BL_)]
    for i in range(1, 12):
        t = i / 12
        back.append('<line x1="%.1f" y1="70" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2" opacity=".55"/>' % (lerp(BKL[0], SR[0], t), lerp(BL_[0], BR_[0], t) + 18, lerp(186, 170, t), P1))
    back.append('<path d="M52 96 L84 70 L284 70" fill="none" stroke="%s" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>' % P2)
    front = ['<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="rgba(247,219,228,.58)"/>' % (*FL, *FR, *BR_, *BL_),
             '<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="rgba(234,177,195,.55)"/>' % (*FR, *SR, *SBR, *BR_)]
    for i in range(1, 13):
        t = i / 13
        front.append('<line x1="%.1f" y1="96" x2="%.1f" y2="186" stroke="%s" stroke-width="1.6"/>' % (lerp(FL[0], FR[0], t), lerp(BL_[0], BR_[0], t), P1))
    for y in range(108, 186, 12):
        t = (y - 96) / 90
        front.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.6"/>' % (lerp(FL[0], BL_[0], t), y, lerp(FR[0], BR_[0], t), y, P1))
    for i in range(1, 4):
        t = i / 4
        front.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>' % (lerp(FR[0], SR[0], t), lerp(FR[1], SR[1], t), lerp(BR_[0], SBR[0], t), lerp(BR_[1], SBR[1], t), P2))
    for k in range(1, 7):
        t = k / 7
        front.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4"/>' % (lerp(FR[0], BR_[0], t), lerp(FR[1], BR_[1], t), lerp(SR[0], SBR[0], t), lerp(SR[1], SBR[1], t), P1))
    front.append('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (*FL, *FR, *BR_, *BL_, P2))
    front.append('<path d="M252 96 L284 70 L262 162 L232 186" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % P2)
    front.append('<path d="M50 96 L254 96 L286 70" fill="none" stroke="%s" stroke-width="5.5" stroke-linejoin="round" stroke-linecap="round"/>' % P2)
    front.append('<path d="M56 100 C 22 108, 22 150, 66 152" fill="none" stroke="#c96788" stroke-width="5" stroke-linecap="round"/>')
    front.append('<path d="M280 76 C 312 86, 310 128, 268 134" fill="none" stroke="#c96788" stroke-width="5" stroke-linecap="round"/>')
    front.append('<rect x="80" y="184" width="16" height="7" rx="3" fill="%s"/><rect x="212" y="184" width="16" height="7" rx="3" fill="%s"/>' % (P2, P2))
    return ('<svg class="bback" viewBox="0 0 300 200" aria-hidden="true">%s</svg>' % ''.join(back),
            '<svg class="bfront" viewBox="0 0 300 200" aria-hidden="true">%s</svg>' % ''.join(front))


def anatomi_bars():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 10"><rect width="9" height="10" fill="#7A6FF0"/>'
           '<rect x="9" width="8" height="10" fill="#E0A23B"/><rect x="17" width="11" height="10" fill="#7FA65A"/>'
           '<rect x="28" width="7" height="10" fill="#C8DE78"/><rect x="35" width="9" height="10" fill="#2e2b2d"/></svg>')
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


def build():
    s = open(os.path.join(HERE, 'src.html')).read()
    bb, bf = basket_svgs()
    M = {'cart_svg': cart_svg(), 'basket_back': bb, 'basket_front': bf, 'logo_anatomi_bars': anatomi_bars()}
    for f in os.listdir(os.path.join(A, 'img')):
        M[f.rsplit('.', 1)[0]] = uri(os.path.join(A, 'img', f))
    for f in os.listdir(os.path.join(A, 'logos')):
        M['logo_' + f.rsplit('.', 1)[0].replace('-', '_')] = uri(os.path.join(A, 'logos', f))
    M['logo_anatomi'] = M['logo_anatomi_mark']
    for f in os.listdir(os.path.join(A, 'icons')):
        M['icon_' + f.rsplit('.', 1)[0].replace('-icon', '').replace('-', '_')] = uri(os.path.join(A, 'icons', f))
    missing = set(re.findall(r'\{\{(\w+)\}\}', s)) - set(M)
    if missing:
        sys.exit('missing assets: %s' % ', '.join(sorted(missing)))
    frag = re.sub(r'\{\{(\w+)\}\}', lambda m: M[m.group(1)], s)
    open(os.path.join(HERE, 'artifact.html'), 'w').write(frag)

    # full document for the live site: head material goes in <head>, the rest in <body>
    cut = frag.index('<svg width="0" height="0"')
    head, body = frag[:cut], frag[cut:]
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    social = (
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="canonical" href="%s">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:url" content="%s">\n'
        '<meta property="og:title" content="Hazel Dang | Marketing Portfolio">\n'
        '<meta property="og:description" content="Copywriter, editor and founder of Anatomi, acquired by Aether AI.">\n'
        '<meta property="og:image" content="%sog-image.jpg">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="theme-color" content="#f9f8f9">\n' % (SITE_URL, SITE_URL, SITE_URL))
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + social + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
    open(os.path.join(ROOT, 'index.html'), 'w').write(page)
    print('built index.html (%d KB) and source/artifact.html' % (len(page) // 1024))


if __name__ == '__main__':
    build()
