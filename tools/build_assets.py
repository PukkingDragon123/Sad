#!/usr/bin/env python3
"""
Froggy Pond asset pipeline.

Turns the raw art in art/source/ into the game-ready files in assets/:

  frogs_sheet.jpeg  (6x6 painted stickers)  -> frogs_adult.png + frogs_baby.png
  foods_sheet.jpeg  (5x10 pixel foods)      -> foods_world.png + foods_ui.png
  pond_source.gif   (animated pixel pond)   -> pond.gif (copied as-is)

For each sprite it:
  1. splits the sheet into individual cells,
  2. removes the background (transparent alpha, interior whites preserved),
  3. resamples to a chunky pixel-art size and quantises the palette,
  4. drops stray fragments bled in from neighbouring cells,
  5. adds a 1px dark outline so everything reads as one cozy set,
  6. tints very slightly toward the pond's light, then packs an atlas.

It also derives the pond's walkable water mask and lily-pad spots from the GIF,
and writes both the atlas manifest and the geometry as JSON for the game.

Usage:  python3 tools/build_assets.py [--out assets] [--data tools/generated]
Needs:  pillow, numpy, scipy
"""
import argparse, base64, colorsys, json, os, shutil, sys

try:
    from PIL import Image, ImageSequence
    import numpy as np
    from scipy import ndimage
except ImportError:
    sys.exit('need: pip install pillow numpy scipy')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'art', 'source')

FROG_SHEET = os.path.join(SRC, 'frogs_sheet.jpeg')
FOOD_SHEET = os.path.join(SRC, 'foods_sheet.jpeg')
POND_GIF = os.path.join(SRC, 'pond_source.gif')

FROG_COLS, FROG_ROWS = 6, 6
FROG_CROP = (0, 0, 1292, 1192)          # trims the dark strip down the right edge
FOOD_ROWS = [(29, 182), (202, 355), (375, 528), (549, 702), (722, 875),
             (895, 1048), (1069, 1222), (1242, 1395), (1415, 1568), (1589, 1741)]
FOOD_COLS = [(15, 180), (293, 446), (564, 717), (834, 988), (1105, 1259)]

ADULT_H, BABY_H = 44, 30                # frog sprite heights, in game pixels
FOOD_WORLD_H, FOOD_UI_H = 24, 40
AMBIENT = np.array([196, 214, 150], float)   # the pond's warm green-gold light


# ---------------------------------------------------------------- helpers
def trim(rgba):
    a = rgba[..., 3] > 0
    if not a.any():
        return rgba
    ys, xs = np.where(a)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def drop_fragments(rgba, min_frac=0.02, gap=2):
    """Remove blobs bled in from a neighbouring cell."""
    a = rgba[..., 3] > 0
    lab, n = ndimage.label(a)
    if n <= 1:
        return rgba
    sizes = ndimage.sum(a, lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    far = ndimage.distance_transform_edt(~(lab == main))
    keep = {main}
    for i in range(1, n + 1):
        if i == main:
            continue
        if sizes[i - 1] >= sizes[main - 1] * min_frac and far[lab == i].min() <= gap:
            keep.add(i)
    out = rgba.copy()
    out[~np.isin(lab, list(keep))] = 0
    return out


def outline(rgba, col=(24, 32, 22), keep=0.55):
    """1px dark outline, plus a slight darkening of the sprite's own edge."""
    h, w = rgba.shape[:2]
    pad = np.zeros((h + 2, w + 2, 4), np.uint8)
    pad[1:-1, 1:-1] = rgba
    plus = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)
    a = pad[..., 3] > 0
    ring = ndimage.binary_dilation(a, plus) & ~a
    out = pad.copy()
    out[ring] = (*col, 255)
    edge = a & ~ndimage.binary_erosion(a, plus)
    px = out[edge][:, :3].astype(float) * keep + np.array(col, float) * (1 - keep)
    tmp = out[edge]
    tmp[:, :3] = np.clip(px, 0, 255).astype(np.uint8)
    out[edge] = tmp
    return out


def grade(rgba, amt=0.12):
    """Nudge colours toward the pond light so every sprite shares one key."""
    if amt <= 0:
        return rgba
    a = rgba.astype(float)
    rgb, al = a[..., :3], a[..., 3]
    lit = rgb * (1 - amt) + (rgb * AMBIENT / 255.0) * amt
    return np.dstack([np.clip(lit, 0, 255).astype(np.uint8), al.astype(np.uint8)])


def pixelate(rgba, target_h, ncolors=15, sat=1.22, val=1.05, alpha_cut=112):
    """Painted / upscaled art -> crisp pixel art of exactly target_h pixels tall."""
    img = Image.fromarray(rgba)
    a = np.asarray(img).astype(float)
    rgb, al = a[..., :3], a[..., 3]
    # premultiply, else averaging pulls transparent black into the edges
    pm = rgb * (al[..., None] / 255.0)
    tw = max(1, int(round(img.width * target_h / img.height)))
    pm2 = np.asarray(Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8))
                     .resize((tw, target_h), Image.BOX)).astype(float)
    al2 = np.asarray(Image.fromarray(al.astype(np.uint8))
                     .resize((tw, target_h), Image.BOX)).astype(float)
    with np.errstate(divide='ignore', invalid='ignore'):
        rgb2 = np.nan_to_num(np.where(al2[..., None] > 0, pm2 / (al2[..., None] / 255.0), 0))
    hard = al2 >= alpha_cut                      # hard alpha keeps pixel edges sharp
    flat = np.clip(rgb2.reshape(-1, 3), 0, 255) / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in flat])
    hsv[:, 1] = np.clip(hsv[:, 1] * sat, 0, 1)
    hsv[:, 2] = np.clip(hsv[:, 2] * val, 0, 1)
    rgb2 = (np.array([colorsys.hsv_to_rgb(*p) for p in hsv]) * 255).reshape(rgb2.shape)
    q = (Image.fromarray(np.clip(rgb2, 0, 255).astype(np.uint8))
         .quantize(colors=ncolors, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB'))
    out = np.dstack([np.asarray(q), (hard * 255).astype(np.uint8)])
    out[~hard] = 0
    return trim(drop_fragments(out))


def save_paletted(im, path, colors=255):
    """Save an RGBA image as a palette PNG with one reserved transparent index.

    The sprites use hard alpha and few colours, so this is lossless in practice
    and roughly a third the size of RGBA — which matters a lot when the game is
    served over a plain static host."""
    a = np.asarray(im.convert('RGBA'))
    opaque = a[..., 3] >= 128
    q = (Image.fromarray(a[..., :3])
         .quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE))
    idx = np.asarray(q).copy()
    pal = list(q.getpalette()[:colors * 3]) + [0, 0, 0]
    idx[~opaque] = colors                       # reserved transparent index
    out = Image.fromarray(idx, mode='P')
    out.putpalette(pal)
    out.info.pop('transparency', None)
    out.save(path, 'PNG', optimize=True, transparency=colors)


def pack(imgs, path, cols):
    """Grid atlas; every sprite is centred horizontally and bottom-aligned."""
    cw = max(i.shape[1] for i in imgs)
    ch = max(i.shape[0] for i in imgs)
    rows = (len(imgs) + cols - 1) // cols
    at = Image.new('RGBA', (cw * cols, ch * rows), (0, 0, 0, 0))
    rects = []
    for k, im in enumerate(imgs):
        r, c = divmod(k, cols)
        h, w = im.shape[:2]
        ox, oy = c * cw + (cw - w) // 2, r * ch + (ch - h)
        pi = Image.fromarray(im)
        at.paste(pi, (ox, oy), pi)
        rects.append(dict(x=ox, y=oy, w=w, h=h))
    save_paletted(at, path)
    return dict(file=os.path.basename(path), cw=cw, ch=ch, cols=cols, rects=rects)


# ---------------------------------------------------------------- frogs
def find_cuts(ink, n, span):
    """Cut positions for n cells along one axis: near each expected grid line,
    pick the row/column with the LEAST ink. The stickers overlap a uniform grid,
    so cutting at the emptiest line minimises how much of any sticker crosses."""
    step = len(ink) / n
    cuts = [0]
    for i in range(1, n):
        e = int(i * step)
        lo, hi = max(0, e - span), min(len(ink), e + span)
        cuts.append(lo + int(np.argmin(ink[lo:hi])))
    cuts.append(len(ink))
    return cuts


def cut_frogs():
    """Split the 6x6 sticker sheet with zero-margin gutter cuts.

    Neighbouring stickers touch, so any margin window inevitably drags in
    flat-cut chunks of the sprite next door. Instead we cut exactly along the
    detected ink-minimum gutters (nothing outside a cell can ever appear in it)
    and, inside each cell, keep the central blob plus only detached bits that
    sit fully interior — anything touching a cell edge is neighbour residue.
    A sticker's own overhang past a gutter is lost, but it is a few source
    pixels (<1 game pixel after downsampling) and the outline pass re-rounds
    the silhouette."""
    im = Image.open(FROG_SHEET).convert('RGB').crop(FROG_CROP)
    A = np.asarray(im).astype(int)
    mxA, mnA = A.max(axis=2), A.min(axis=2)
    ink = ~((mnA > 232) & ((mxA - mnA) < 30))
    colcut = find_cuts(ink.sum(axis=0), FROG_COLS, 22)
    rowcut = find_cuts(ink.sum(axis=1), FROG_ROWS, 22)
    out = []
    for r in range(FROG_ROWS):
        for c in range(FROG_COLS):
            cell = A[rowcut[r]:rowcut[r + 1], colcut[c]:colcut[c + 1]]
            mx, mn = cell.max(axis=2), cell.min(axis=2)
            m = ~((mn > 232) & ((mx - mn) < 30))            # not near-white
            m = ndimage.binary_opening(m, np.ones((3, 3)))  # break jpeg noise
            lab, n = ndimage.label(m)
            if n == 0:
                out.append(None); continue
            h, w = m.shape
            central = np.zeros_like(m)
            central[int(h * .18):int(h * .82), int(w * .18):int(w * .82)] = True
            sizes = ndimage.sum(m, lab, range(1, n + 1))
            main = int(np.argmax(ndimage.sum(m & central, lab, range(1, n + 1)))) + 1
            far = ndimage.distance_transform_edt(~(lab == main))
            keep = {main}
            for i in range(1, n + 1):
                if i == main or sizes[i - 1] < sizes[main - 1] * .012:
                    continue
                ys, xs = np.where(lab == i)
                # detached bits are kept only if fully interior and near the body;
                # anything at a cell edge is residue of the sprite next door
                if ys.min() < 3 or xs.min() < 3 or ys.max() > h - 4 or xs.max() > w - 4:
                    continue
                if far[lab == i].min() <= 14:
                    keep.add(i)
            m2 = np.isin(lab, list(keep))
            m2 = ndimage.binary_fill_holes(ndimage.binary_closing(m2, np.ones((3, 3))))
            if m2.sum() < 400:
                out.append(None); continue
            out.append(trim(np.dstack([cell.astype(np.uint8), (m2 * 255).astype(np.uint8)])))
    return out


# ---------------------------------------------------------------- foods
def cut_foods():
    """Split the 5x10 food sheet. Background is flood-identified from the cell
    border, so interior whites (milk, rice, egg) are preserved."""
    A = np.asarray(Image.open(FOOD_SHEET).convert('RGB')).astype(int)
    P = 16
    out = []
    for y0, y1 in FOOD_ROWS:
        for x0, x1 in FOOD_COLS:
            cy0, cy1 = max(0, y0 - P), min(A.shape[0], y1 + P)
            cx0, cx1 = max(0, x0 - P), min(A.shape[1], x1 + P)
            cell = A[cy0:cy1, cx0:cx1]
            mx, mn = cell.max(axis=2), cell.min(axis=2)
            nearbg = (mn > 230) & ((mx - mn) < 24)
            lab, _ = ndimage.label(nearbg)
            border = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
            border.discard(0)
            m = ndimage.binary_fill_holes(
                ndimage.binary_closing(~np.isin(lab, list(border)), np.ones((3, 3))))
            l2, n2 = ndimage.label(m)
            if n2 == 0:
                out.append(None); continue
            sz = ndimage.sum(m, l2, range(1, n2 + 1))
            main = int(np.argmax(sz)) + 1
            far = ndimage.distance_transform_edt(~(l2 == main))
            keep = {main}
            for i in range(1, n2 + 1):
                if i != main and sz[i - 1] >= sz[main - 1] * .02 and far[l2 == i].min() <= 8:
                    keep.add(i)
            m = np.isin(l2, list(keep))
            out.append(trim(np.dstack([cell.astype(np.uint8), (m * 255).astype(np.uint8)])))
    return out


# ---------------------------------------------------------------- pond geometry
def pond_geometry(cell=4):
    """Average the GIF frames (kills the moving light rays and sparkles), then
    classify water vs foliage and export a compact walkability bitmask."""
    frames = [np.asarray(f.convert('RGB')).astype(float)
              for f in ImageSequence.Iterator(Image.open(POND_GIF))]
    avg = np.mean(frames, axis=0)
    h, w, _ = avg.shape
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in (avg.reshape(-1, 3) / 255.0)]).reshape(h, w, 3)
    Sa, V = hsv[..., 1], hsv[..., 2]

    water = (Sa < .62) & (V > .10) & (V < .62)
    water = ndimage.binary_fill_holes(
        ndimage.binary_closing(ndimage.binary_opening(water, np.ones((3, 3))), np.ones((9, 9))))
    lab, n = ndimage.label(water)
    water = lab == int(np.argmax(ndimage.sum(water, lab, range(1, n + 1)))) + 1

    fg = ndimage.binary_dilation(                     # dark foreground fronds
        ndimage.binary_closing((V < .20) & (Sa > .45), np.ones((5, 5))), np.ones((7, 7)))
    walk = water & ~fg
    yy, xx = np.mgrid[0:h, 0:w]
    walk &= ~((yy > 330) & (xx < 210))                # bottom-left leaves
    walk &= ~((yy > 300) & (xx > 560))                # bottom-right leaves
    walk &= ~(yy > 386)
    walk = ndimage.binary_opening(ndimage.binary_erosion(walk, np.ones((5, 5))), np.ones((5, 5)))
    lab, n = ndimage.label(walk)
    walk = lab == int(np.argmax(ndimage.sum(walk, lab, range(1, n + 1)))) + 1

    pad = ndimage.binary_opening((Sa > .55) & (V > .22) & (V < .55) & water, np.ones((3, 3)))
    lab, n = ndimage.label(pad)
    sizes = ndimage.sum(pad, lab, range(1, n + 1))
    pads = []
    for i, (cyy, cxx) in enumerate(ndimage.center_of_mass(pad, lab, range(1, n + 1))):
        if not (60 <= sizes[i] <= 1400) or not walk[int(cyy), int(cxx)]:
            continue
        xs = np.where(lab == i + 1)[1]
        pads.append(dict(x=round(float(cxx), 1), y=round(float(cyy), 1),
                         r=round(float(max(6, (xs.max() - xs.min()) / 2)), 1), a=int(sizes[i])))
    pads.sort(key=lambda p: -p['a'])

    gw, gh = w // cell, h // cell
    grid = walk[:gh * cell, :gw * cell].reshape(gh, cell, gw, cell).mean(axis=(1, 3)) > .5
    return dict(cell=cell, gw=gw, gh=gh,
                b64=base64.b64encode(np.packbits(grid.flatten()).tobytes()).decode(),
                pads=pads[:22])


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'assets'))
    ap.add_argument('--data', default=os.path.join(ROOT, 'tools', 'generated'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    os.makedirs(a.data, exist_ok=True)

    manifest = {}

    frogs = cut_frogs()
    missing = [i for i, f in enumerate(frogs) if f is None]
    if missing:
        print('WARNING: could not cut frog cells', missing)
    for tag, th, cols in (('adult', ADULT_H, 6), ('baby', BABY_H, 6)):
        imgs = [grade(outline(pixelate(f, th))) for f in frogs if f is not None]
        manifest['frog_' + tag] = pack(imgs, os.path.join(a.out, f'frogs_{tag}.png'), cols)
        print(f'frogs_{tag}.png  {len(imgs)} sprites, cell '
              f'{manifest["frog_"+tag]["cw"]}x{manifest["frog_"+tag]["ch"]}')

    foods = cut_foods()
    for tag, th, amt in (('world', FOOD_WORLD_H, .08), ('ui', FOOD_UI_H, 0)):
        imgs = [grade(outline(pixelate(f, th, ncolors=13, sat=1.18, val=1.03, alpha_cut=118),
                              col=(30, 26, 20), keep=.62), amt)
                for f in foods if f is not None]
        manifest['food_' + tag] = pack(imgs, os.path.join(a.out, f'foods_{tag}.png'), 10)
        print(f'foods_{tag}.png  {len(imgs)} sprites, cell '
              f'{manifest["food_"+tag]["cw"]}x{manifest["food_"+tag]["ch"]}')

    shutil.copyfile(POND_GIF, os.path.join(a.out, 'pond.gif'))
    gif_kb = os.path.getsize(os.path.join(a.out, 'pond.gif')) // 1024
    print(f'pond.gif    copied, {gif_kb} KB (animated background, used as-is)')

    # A still first frame, ~17 KB, so the game can paint and play immediately and
    # stream the half-megabyte animation in afterwards instead of blocking on it.
    still = Image.open(POND_GIF).convert('RGB')
    still.info.pop('transparency', None)
    still.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE) \
         .save(os.path.join(a.out, 'pond_still.png'), 'PNG', optimize=True)
    print(f'pond_still.png  {os.path.getsize(os.path.join(a.out,"pond_still.png"))//1024} KB'
          ' (instant background; the gif swaps in when it arrives)')

    json.dump(manifest, open(os.path.join(a.data, 'atlas_manifest.json'), 'w'), indent=1)
    geom = pond_geometry()
    json.dump(geom, open(os.path.join(a.data, 'pond_geom.json'), 'w'), indent=1)
    print(f'geometry    {geom["gw"]}x{geom["gh"]} walk grid, {len(geom["pads"])} lily pads')
    print('\nwrote atlas_manifest.json and pond_geom.json to', a.data)
    print('these are inlined into index.html — re-inline them if you rebuild the art.')


if __name__ == '__main__':
    main()
