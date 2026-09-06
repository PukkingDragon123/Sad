#!/usr/bin/env python3
"""
Froggy Pixel — the game's own typeface, drawn pixel by pixel.

Every glyph is a little grid of '#' below: seven rows above the baseline, two
below it for descenders. The script turns each grid into the smallest set of
rectangles that covers it, emits those as TrueType contours at 100 units per
pixel, and writes a regular and a bold face (bold is the same grid smeared one
pixel to the right, which is how a pixel font gets heavier without blurring).

    python3 tools/make_font.py            # writes tools/generated/froggy-pixel*.woff2
    python3 tools/make_font.py --inline   # ...and pastes them into index.html

Design metrics, in pixels:
    cap height 7 · x-height 5 · ascender 7 · descender 2 · em 12
"""
import argparse, base64, io, os, re, sys

PX      = 100          # font units per pixel
EM      = 12           # pixels per em
TOP     = 7            # rows above the baseline
ASC     = 10 * PX
DESC    = -2 * PX
SPACING = 1            # blank pixels between glyphs

# --------------------------------------------------------------------------
# the alphabet. '#' is ink, '.' is air; the first row sits at the cap line.
# --------------------------------------------------------------------------
G = {}

def g(ch, *rows): G[ch] = list(rows)

# ---- uppercase: 5 wide, 7 tall, square shoulders and round bowls ----
g('A', '.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#')
g('B', '####.', '#...#', '#...#', '####.', '#...#', '#...#', '####.')
g('C', '.###.', '#...#', '#....', '#....', '#....', '#...#', '.###.')
g('D', '####.', '#...#', '#...#', '#...#', '#...#', '#...#', '####.')
g('E', '#####', '#....', '#....', '####.', '#....', '#....', '#####')
g('F', '#####', '#....', '#....', '####.', '#....', '#....', '#....')
g('G', '.###.', '#...#', '#....', '#.###', '#...#', '#...#', '.###.')
g('H', '#...#', '#...#', '#...#', '#####', '#...#', '#...#', '#...#')
g('I', '###', '.#.', '.#.', '.#.', '.#.', '.#.', '###')
g('J', '..###', '....#', '....#', '....#', '#...#', '#...#', '.###.')
g('K', '#...#', '#..#.', '#.#..', '##...', '#.#..', '#..#.', '#...#')
g('L', '#....', '#....', '#....', '#....', '#....', '#....', '#####')
g('M', '#...#', '##.##', '#.#.#', '#...#', '#...#', '#...#', '#...#')
g('N', '#...#', '##..#', '#.#.#', '#..##', '#...#', '#...#', '#...#')
g('O', '.###.', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.')
g('P', '####.', '#...#', '#...#', '####.', '#....', '#....', '#....')
g('Q', '.###.', '#...#', '#...#', '#...#', '#.#.#', '#..#.', '.##.#')
g('R', '####.', '#...#', '#...#', '####.', '#.#..', '#..#.', '#...#')
g('S', '.####', '#....', '#....', '.###.', '....#', '....#', '####.')
g('T', '#####', '..#..', '..#..', '..#..', '..#..', '..#..', '..#..')
g('U', '#...#', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.')
g('V', '#...#', '#...#', '#...#', '#...#', '#...#', '.#.#.', '..#..')
g('W', '#...#', '#...#', '#...#', '#.#.#', '#.#.#', '##.##', '#...#')
g('X', '#...#', '#...#', '.#.#.', '..#..', '.#.#.', '#...#', '#...#')
g('Y', '#...#', '#...#', '.#.#.', '..#..', '..#..', '..#..', '..#..')
g('Z', '#####', '....#', '...#.', '..#..', '.#...', '#....', '#####')

# ---- digits: 5 wide and all the same width, so counters do not jitter ----
g('0', '.###.', '#...#', '#..##', '#.#.#', '##..#', '#...#', '.###.')
g('1', '..#..', '.##..', '..#..', '..#..', '..#..', '..#..', '.###.')
g('2', '.###.', '#...#', '....#', '...#.', '..#..', '.#...', '#####')
g('3', '####.', '....#', '....#', '.###.', '....#', '....#', '####.')
g('4', '...#.', '..##.', '.#.#.', '#..#.', '#####', '...#.', '...#.')
g('5', '#####', '#....', '#....', '####.', '....#', '#...#', '.###.')
g('6', '..##.', '.#...', '#....', '####.', '#...#', '#...#', '.###.')
g('7', '#####', '....#', '...#.', '..#..', '..#..', '.#...', '.#...')
g('8', '.###.', '#...#', '#...#', '.###.', '#...#', '#...#', '.###.')
g('9', '.###.', '#...#', '#...#', '.####', '....#', '...#.', '.##..')

# ---- lowercase: x-height 5, shouldered like the caps ----
g('a', '.....', '.....', '.###.', '....#', '.####', '#...#', '.####')
g('b', '#....', '#....', '####.', '#...#', '#...#', '#...#', '####.')
g('c', '.....', '.....', '.###.', '#....', '#....', '#....', '.###.')
g('d', '....#', '....#', '.####', '#...#', '#...#', '#...#', '.####')
g('e', '.....', '.....', '.###.', '#...#', '#####', '#....', '.###.')
g('f', '..##', '.#..', '####', '.#..', '.#..', '.#..', '.#..')
g('g', '.....', '.....', '.####', '#...#', '#...#', '#...#', '.####',
        '....#', '.###.')
g('h', '#....', '#....', '#.##.', '##..#', '#...#', '#...#', '#...#')
g('i', '.#.', '...', '##.', '.#.', '.#.', '.#.', '###')
g('j', '..#.', '....', '.##.', '..#.', '..#.', '..#.', '..#.', '#.#.', '.##.')
g('k', '#....', '#....', '#..#.', '#.#..', '##...', '#.#..', '#..#.')
g('l', '##.', '.#.', '.#.', '.#.', '.#.', '.#.', '.##')
g('m', '.....', '.....', '##.##', '#.#.#', '#.#.#', '#.#.#', '#.#.#')
g('n', '.....', '.....', '#.##.', '##..#', '#...#', '#...#', '#...#')
g('o', '.....', '.....', '.###.', '#...#', '#...#', '#...#', '.###.')
g('p', '.....', '.....', '####.', '#...#', '#...#', '#...#', '####.',
        '#....', '#....')
g('q', '.....', '.....', '.####', '#...#', '#...#', '#...#', '.####',
        '....#', '....#')
g('r', '....', '....', '#.##', '##..', '#...', '#...', '#...')
g('s', '.....', '.....', '.####', '#....', '.###.', '....#', '####.')
g('t', '.#..', '.#..', '####', '.#..', '.#..', '.#..', '..##')
g('u', '.....', '.....', '#...#', '#...#', '#...#', '#...#', '.####')
g('v', '.....', '.....', '#...#', '#...#', '#...#', '.#.#.', '..#..')
g('w', '.....', '.....', '#...#', '#...#', '#.#.#', '#.#.#', '.#.#.')
g('x', '.....', '.....', '#...#', '.#.#.', '..#..', '.#.#.', '#...#')
g('y', '.....', '.....', '#...#', '#...#', '#...#', '#...#', '.####',
        '....#', '####.')
g('z', '.....', '.....', '#####', '...#.', '..#..', '.#...', '#####')

# ---- punctuation and the handful of symbols the UI actually shows ----
g(' ', '..', '..', '..', '..', '..', '..', '..')
g('.', '.', '.', '.', '.', '.', '.', '#')
g(',', '..', '..', '..', '..', '..', '..', '.#', '#.')
g(':', '.', '.', '.', '#', '.', '.', '#')
g(';', '..', '..', '..', '.#', '..', '..', '.#', '#.')
g('!', '#', '#', '#', '#', '#', '.', '#')
g('?', '.###.', '#...#', '....#', '..##.', '..#..', '.....', '..#..')
g("'", '#', '#')
g('"', '#.#', '#.#')
g('-', '...', '...', '...', '...', '###')
g('_', '.....', '.....', '.....', '.....', '.....', '.....', '.....', '#####')
g('+', '.....', '.....', '..#..', '..#..', '#####', '..#..', '..#..')
g('=', '.....', '.....', '.....', '#####', '.....', '#####')
g('*', '.....', '#.#.#', '.###.', '#####', '.###.', '#.#.#')
g('/', '....#', '....#', '...#.', '..#..', '.#...', '#....', '#....')
g('\\', '#....', '#....', '.#...', '..#..', '...#.', '....#', '....#')
g('(', '..#', '.#.', '#..', '#..', '#..', '.#.', '..#')
g(')', '#..', '.#.', '..#', '..#', '..#', '.#.', '#..')
g('[', '.##', '.#.', '.#.', '.#.', '.#.', '.#.', '.##')
g(']', '##.', '.#.', '.#.', '.#.', '.#.', '.#.', '##.')
g('{', '..##', '.#..', '.#..', '##..', '.#..', '.#..', '..##')
g('}', '##..', '..#.', '..#.', '..##', '..#.', '..#.', '##..')
g('<', '...#', '..#.', '.#..', '#...', '.#..', '..#.', '...#')
g('>', '#...', '.#..', '..#.', '...#', '..#.', '.#..', '#...')
g('|', '#', '#', '#', '#', '#', '#', '#')
g('#', '.#.#.', '#####', '.#.#.', '.#.#.', '#####', '.#.#.')
g('$', '..#..', '.####', '#.#..', '.###.', '..#.#', '####.', '..#..')
g('%', '##..#', '##.#.', '...#.', '..#..', '.#.##', '#..##')
g('&', '.##..', '#..#.', '#.#..', '.#...', '#.#.#', '#..#.', '.##.#')
g('@', '.###.', '#...#', '#.###', '#.#.#', '#.###', '#....', '.###.')
g('^', '..#..', '.#.#.', '#...#')
g('~', '.....', '.....', '.##..', '#..##')
g('`', '#.', '.#')
g('=', '.....', '.....', '.....', '#####', '.....', '#####')

# ---- the non-ASCII the game types ----
g('·', '.', '.', '.', '.', '#')                          # middot
g('—', '.....', '.....', '.....', '.....', '#####')       # em dash
g('…', '.....', '.....', '.....', '.....', '.....', '.....', '#.#.#')
g('→', '.....', '.....', '..#..', '...#.', '#####', '...#.', '..#..')
g('◀', '...#.', '..##.', '.###.', '####.', '.###.', '..##.', '...#.')
g('▶', '.#...', '.##..', '.###.', '.####', '.###.', '.##..', '.#...')
g('✕', '.....', '#...#', '.#.#.', '..#..', '.#.#.', '#...#')            # ✕
g('♪', '...##', '..###', '...#.', '...#.', '...#.', '.###.', '.##..')   # ♪
g('❙', '##', '##', '##', '##', '##', '##', '##')                        # ❙
g('❀', '..#..', '#.#.#', '.###.', '#####', '.###.', '#.#.#', '..#..')   # ❀
g('◉', '.###.', '#...#', '#.#.#', '##.##', '#.#.#', '#...#', '.###.')   # ◉
g('♡', '.....', '.#.#.', '#.#.#', '#...#', '.#.#.', '..#..')            # ♡
g('♥', '.....', '.#.#.', '#####', '#####', '.###.', '..#..')            # ♥
g('✓', '.....', '....#', '...#.', '#..#.', '.##..', '..#..')            # ✓

# ---- bold ----
# Bold is the regular grid smeared one pixel to the right, which is how a pixel
# font gets heavier without going blurry. Four letters carry two 1px gaps that a
# smear would close, so they are drawn heavy by hand; the symbols keep their
# regular shape, since a heavier ♪ or ❀ is nobody's idea of emphasis.
BOLD = {}
def gb(ch, *rows): BOLD[ch] = list(rows)

gb('M', '##...##', '###.###', '##.#.##', '##...##', '##...##', '##...##', '##...##')
gb('W', '##...##', '##...##', '##...##', '##.#.##', '##.#.##', '##.#.##', '.##.##.')
gb('m', '.......', '.......', '#######', '##.#.##', '##.#.##', '##.#.##', '##.#.##')
gb('w', '........', '........', '##....##', '##....##', '##.##.##', '##.##.##', '.######.')

NO_SMEAR = set(" .,:;'\"!?()[]{}<>|/\\-_=+*#$%&@^~`\u00b7\u2014\u2026\u2192\u25c0\u25b6"
               "\u2715\u266a\u2759\u2740\u25c9\u2661\u2665\u2713")

# --------------------------------------------------------------------------
# grids -> rectangles -> TrueType contours
# --------------------------------------------------------------------------
def norm(rows):
    """pad every glyph out to the full 9-row box and a rectangular width"""
    w = max((len(r) for r in rows), default=1)
    out = [r.ljust(w, '.') for r in rows]
    while len(out) < TOP + 2: out.append('.' * w)
    return out, w

def rects(rows, w):
    """greedy maximal rectangles — fewer contours than one square per pixel"""
    px = {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == '#'}
    out = []
    while px:
        x0, y0 = min(px, key=lambda p: (p[1], p[0]))
        rw = 1
        while (x0 + rw, y0) in px: rw += 1
        rh = 1
        while all((x0 + i, y0 + rh) in px for i in range(rw)): rh += 1
        for j in range(rh):
            for i in range(rw): px.discard((x0 + i, y0 + j))
        out.append((x0, y0, rw, rh))
    return out

def embolden(rows, w):
    """one pixel of smear to the right: a pixel font's idea of bold"""
    out = []
    for r in rows:
        r = r + '.'
        out.append(''.join('#' if (r[i] == '#' or (i and r[i-1] == '#')) else '.'
                           for i in range(w + 1)))
    return out, w + 1

def build(bold=False):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    order, cmap, glyphs, metrics = ['.notdef'], {}, {}, {}

    pen = TTGlyphPen(None)                      # .notdef: a hollow box
    for (x0, y0, x1, y1) in [(50, 0, 450, 100), (50, 600, 450, 700),
                             (50, 0, 150, 700), (350, 0, 450, 700)]:
        pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1))
        pen.lineTo((x1, y0)); pen.closePath()
    glyphs['.notdef'] = pen.glyph(); metrics['.notdef'] = (600, 50)

    for ch, raw in G.items():
        rows, w = norm(raw)
        if bold and ch in BOLD:      rows, w = norm(BOLD[ch])
        elif bold and ch not in NO_SMEAR: rows, w = embolden(rows, w)
        name = 'uni%04X' % ord(ch)
        pen = TTGlyphPen(None)
        for (x, y, rw, rh) in rects(rows, w):
            x0, x1 = x * PX, (x + rw) * PX
            y1, y0 = (TOP - y) * PX, (TOP - y - rh) * PX
            pen.moveTo((x0, y0)); pen.lineTo((x0, y1))
            pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()
        order.append(name); cmap[ord(ch)] = name
        glyphs[name] = pen.glyph()
        metrics[name] = ((w + SPACING) * PX, 0)

    style = 'Bold' if bold else 'Regular'
    fb = FontBuilder(EM * PX, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASC, descent=DESC, lineGap=0)
    fb.setupNameTable({
        'familyName': 'Froggy Pixel', 'styleName': style,
        'psName': 'FroggyPixel-' + style, 'fullName': 'Froggy Pixel ' + style,
        'version': 'Version 1.000', 'uniqueFontIdentifier': 'FroggyPixel-' + style + '-1.000',
        'copyright': 'Froggy Pixel — drawn for Froggy Pond by Pukking Dragon.',
        'designer': 'Pukking Dragon',
        'licenseDescription': 'Free to use with the game it was drawn for.',
    })
    fb.setupOS2(sTypoAscender=ASC, sTypoDescender=DESC, sTypoLineGap=0,
                usWinAscent=ASC, usWinDescent=-DESC,
                sxHeight=5 * PX, sCapHeight=TOP * PX,
                usWeightClass=700 if bold else 400,
                fsSelection=(1 << 5) if bold else (1 << 6))
    fb.setupPost(isFixedPitch=0, underlinePosition=-2 * PX, underlineThickness=PX)
    if bold: fb.font['head'].macStyle |= 1
    return fb.font

def woff2(font, path):
    font.flavor = 'woff2'
    font.save(path)
    return open(path, 'rb').read()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inline', action='store_true', help='paste into index.html')
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, 'generated'); os.makedirs(out, exist_ok=True)
    blobs = {}
    for bold in (False, True):
        name = 'froggy-pixel-%s.woff2' % ('bold' if bold else 'regular')
        blobs[bold] = woff2(build(bold), os.path.join(out, name))
        print('%-28s %6d bytes  %d glyphs' % (name, len(blobs[bold]), len(G) + 1))
    if not a.inline: return
    page = os.path.join(os.path.dirname(here), 'index.html')
    src = io.open(page, encoding='utf-8').read()
    face = ''.join(
        "@font-face{font-family:'Pix';font-style:normal;font-weight:%d;"
        "src:url(data:font/woff2;base64,%s) format('woff2');font-display:block;}"
        % (700 if bold else 400, base64.b64encode(blobs[bold]).decode())
        for bold in (False, True))
    new, n = re.subn(r"@font-face\{font-family:'Pix';.*?\}", face, src, count=1, flags=re.S)
    if n != 1: sys.exit('could not find the @font-face block to replace')
    io.open(page, 'w', encoding='utf-8').write(new)
    print('inlined into %s (%d KB)' % (page, len(new) // 1024))

if __name__ == '__main__':
    main()
