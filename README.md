# 🐸 Froggy Pond — a cozy frog breeder simulator

A little pixel-art pond where you feed, breed, collect and sell round frogs.
36 species, 22 snacks, one very sleepy pond.

![the pond](docs/pond.png)

## Play

The game loads its art from `assets/`, so open it over http rather than as a
bare file:

```bash
npx http-server        # then visit the printed URL
# or: python3 -m http.server
```

Progress saves automatically in your browser.

## How it works

- **Throw snacks** — pick a snack from the tray, then click the open water.
  It arcs in, splashes, and the frogs swarm it; the closest one gets the bite.
  Every frog remembers its **last snack**.
- **Breed** — click a frog → `breed` to send it to the pink **love-pad** in the
  middle of the pond. Send two. If the pair matches a recipe **and both parents
  last ate that recipe's snack**, the egg hatches a brand-new species. Any other
  pairing gives you a copy of a parent — still worth selling.
  Parents aren't consumed; they just rest a moment, so a good pair keeps giving.
- **Froglets** hatch small and grow up before they can breed or be sold.
- **The phone** (bottom right):
  - 🛒 **ShopHop** — buy the 8 starter frogs, unlock deeper snacks.
  - 📖 **FrogDex** — the collection. Unmet frogs are silhouettes; once you've met
    both parents of a recipe, the Dex reveals which snack it needs. It remembers
    every frog you've met even after you sell it, so selling never costs you progress.
  - 💬 **RibbitChat** — collectors message you wanting a specific frog and pay
    1.4–1.9× the shelf price. This is the main way to fund the fancy snacks.
  - ⚙️ **Settings** — sound and a pond reset.
- **Goal** — meet all **36 species**. 8 are buyable; the other 28 are breed-only,
  four tiers deep, ending in two legendaries.

The pond holds 12 frogs at a time, which is the real pacing constraint: to go
deeper you sell frogs you've already recorded to make room.

Frogs squash and stretch on every hop, waddle between nearby spots, doze off
with a little `z`, croak, cast reflections in the water, and get the zoomies off
a matcha latte. Petting is free.

## Tech notes

- One `index.html` (~99 KB) plus `assets/` (~740 KB). Vanilla JS, no build step,
  no dependencies. Canvas renders at 640×400 and scales in crisp quarter-steps.
- The **animated pond is the GIF itself**, layered under a transparent canvas —
  20 frames of drifting light for ~0 CPU. The game derives its **walkable water
  mask** from that same art (a 160×100 bitmask, base64-inlined) so frogs and food
  only ever land on real water, following the pond's irregular banks.
- All sprites are **split out of the source sheets at build time** into
  transparent-background atlases: 36 frogs × 2 sizes, 50 snacks × 2 sizes. Since
  the frog sheet was painted rather than pixelled, the pipeline resamples each
  sticker onto a pixel grid, quantises its palette, adds a 1px dark outline and
  grades it slightly toward the pond's light so the whole cast reads as one set.
- Sound is synthesised at runtime (WebAudio) — bloops, ribbits, crickets and a
  quiet pond hiss. No audio files.
- Font: [Pixelify Sans](https://fonts.google.com/specimen/Pixelify+Sans) (OFL),
  embedded so it works offline. UI panels are 9-slice pixel frames drawn at boot.
- `?fast` in the URL runs all timers 10× faster, which is how the tests drive it.

### Rebuilding the art

```bash
pip install pillow numpy scipy
python3 tools/build_assets.py
```

That regenerates everything in `assets/` from `art/source/`, plus
`tools/generated/{atlas_manifest,pond_geom}.json` — the sprite rects and pond
geometry that are inlined into `index.html`. Re-inline those two if you change
the art.

## Credits

- **Pond background** — animated pixel art by **@anasabdin** (watermark left
  intact in the artwork; also credited in-game under Settings).
- **Frog and snack sprite sheets** — supplied by the repo owner; original artists
  unknown to me. If you know who made them, please add proper credit here.
  Everything in `assets/` is derived from those sheets, so the same terms apply.
- Code and the asset pipeline in this repo: written for this project.

## Spoilers — the full recipe book

<details>
<summary>the 8 starters</summary>

| Frog | Buy | |
|---|---|---|
| Bunny Tongue Frog | 110 | tongue out always. this is simply how it is. |
| Mosscap Frog | 50 | never takes the little hat off, not even to nap. |
| Silkie Frog | 140 | clucks at dawn, then denies everything. |
| Green Apple Frog | 85 | crisp, tart, and a little embarrassed. |
| Speckled Drool Frog | 55 | spotted, dewy, and unbothered by both. |
| Fresh Loaf Frog | 70 | warm crust, smells like the morning shelf. |
| Doorway Frog | 95 | knock twice; the little bell answers for it. |
| Cocoa Nap Frog | 65 | sleeps rooted, sprouts greens, dreams of rain. |

</details>

<details>
<summary>all 28 breed-only recipes (click if you're truly stuck)</summary>

Both parents must have eaten the listed snack.

| Baby | Parents | Snack | Sells for |
|---|---|---|---|
| Piggyback Frog | Speckled Drool Frog + Cocoa Nap Frog | Twin Pop | 95 |
| Sardine Tin Frog | Speckled Drool Frog + Doorway Frog | Maki Rolls | 100 |
| Bunny Pile Frog | Mosscap Frog + Cocoa Nap Frog | Pea Bowl | 110 |
| Ramshorn Frog | Silkie Frog + Cocoa Nap Frog | Pea Bowl | 115 |
| Tabby Mouser Frog | Bunny Tongue Frog + Fresh Loaf Frog | Milk Carton | 120 |
| Blossom Puff Frog | Silkie Frog + Bunny Tongue Frog | Butter Toast | 125 |
| Redswirl Frog | Speckled Drool Frog + Silkie Frog | Loopy Cereal | 135 |
| Ember Egg Frog | Mosscap Frog + Fresh Loaf Frog | Hearty Stew | 140 |
| Kiosk Frog | Doorway Frog + Fresh Loaf Frog | Popcorn Tub | 145 |
| Nigiri Frog | Silkie Frog + Green Apple Frog | Onigiri | 150 |
| Handheld Frog | Doorway Frog + Mosscap Frog | Toaster Tart | 160 |
| Omurice Love Frog | Silkie Frog + Fresh Loaf Frog | Fried Egg | 165 |
| Kaeru Shiba Frog | Handheld Frog + Fresh Loaf Frog | Kebab Skewer | 215 |
| Stone Guardian Frog | Mosscap Frog + Kiosk Frog | Dirt Pot | 230 |
| Bouquet Frog | Blossom Puff Frog + Bunny Pile Frog | Heart Cupcake | 250 |
| Hazard Flask Frog | Ember Egg Frog + Kiosk Frog | Matcha Latte | 270 |
| Peony Bloom Frog | Blossom Puff Frog + Doorway Frog | Heart Cupcake | 285 |
| Crimson Coil Frog | Sardine Tin Frog + Redswirl Frog | Candy Apple | 300 |
| Monocle Frog | Tabby Mouser Frog + Sardine Tin Frog | Maki Rolls | 320 |
| Porcelain Koi Frog | Nigiri Frog + Redswirl Frog | Creme Brulee | 340 |
| Lantern Frog | Ember Egg Frog + Ramshorn Frog | Hearty Stew | 355 |
| Blue Ring Frog | Hazard Flask Frog + Porcelain Koi Frog | Creme Brulee | 440 |
| Shrimp Charm Frog | Crimson Coil Frog + Kaeru Shiba Frog | Candy Apple | 535 |
| Ringed Saucer Frog | Hazard Flask Frog + Handheld Frog | Sprinkle Donut | 630 |
| Lion Dance Frog | Crimson Coil Frog + Lantern Frog | Kebab Skewer | 725 |
| Daruma Frog | Porcelain Koi Frog + Stone Guardian Frog | Matcha Latte | 820 |
| Little Planet Frog | Ringed Saucer Frog + Ember Egg Frog | Pie a la Mode | 1500 |
| Gemfist Frog | Daruma Frog + Blue Ring Frog | Candy Brownie | 2600 |

</details>
