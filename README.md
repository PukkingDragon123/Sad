# 🐸 Froggy Pond — a cozy frog breeder simulator

A little pixel-art pond where you feed, breed, collect and sell round frogs.
36 species, 22 snacks, 8 tools, four pond tracks, one very sleepy pond.

![the pond](docs/pond.png)

![the title screen](docs/title.png)

## Play

**Just open `index.html`.** Double-click it, or drag it into a browser — the
sprite art is inlined, so there is no loading screen, nothing to install and no
server needed. Serving the folder over http (`npx http-server`) only adds the
pond's animated background, which is optional.

**Works with a finger.** Everything is one pointer path, so a tap, a press and a
drag all mean the same thing whether you are on a mouse or a phone: press a frog
to pick it up, drag to carry it, let go to set it down, tap to pet it. On a
narrow screen the tool strip and snack tray stack, the pond sits up at the top
and the frog card tucks in above the bar.

![on a phone](docs/mobile.png)

Progress saves automatically in your browser.

## How it works

- **Throw snacks** — pick a snack from the tray, then tap the open water.
  It arcs in, splashes, and the frogs swarm it; the closest one gets the bite.
  Every frog remembers its **last snack**.
  You can also **tap a frog** with a snack selected to hand-feed it directly —
  the reliable way to get one particular snack into one particular frog.
- **Breed with a breeding tool.** Take the **Love Wand**, tap one frog, tap
  another, and they walk to the pink **love-pad** by themselves. (The Gentle Hand
  works too — just drop a frog on the pad. `breed` on a frog's card hands you the
  wand with that frog already chosen.) If the pair matches a recipe and **either**
  parent last ate that recipe's snack, the egg hatches a brand-new species. Any
  other pairing gives you a copy of a parent — still worth selling. Parents aren't
  consumed and keep their snack, so a working pair keeps giving. The love-pad tells
  you on screen what the current pair will make, or which snack it still wants.
- **Froglets** hatch small and grow up before they can breed or be sold.
- **Tools** — eight of them, in the strip beside the snacks.

  *Breeding:*
  - **Gentle Hand** (free) — lift a frog and set it down anywhere. Drop it on the
    love-pad to breed, or onto a snack to choose exactly who eats what. It's what
    you start holding, and a press without a drag just pets the frog.
  - **Love Wand** (free) — the quick way to breed: tap one frog, then its
    partner. No walking them over, no menus.
  - **Breed Tonic** (10c) — for two minutes that frog makes the best baby it
    can: it works with no snack at all, crosses the pond for the next snack,
    rests and hatches quicker, and never wastes a pairing. Dosed frogs shimmer.
  - **Matchmaker Bell** (12c) — ring it at a frog and it marks the best partner
    in your pond with a gold heart, and says which snack the pair still needs.
    If nothing in the pond matches, it tells you so and costs nothing.

  *Speed-up:*
  - **Sun Lamp** (8c) — tap the egg on the love-pad and it hatches in well under
    half the time. Tap a resting frog and its rest ends; tap a froglet and it
    grows up much sooner.

  *Toys:*
  - **Bouncy Ball** (free) — tap the water to bounce it. Frogs hop after it and
    headbutt it around, which gives them zoomies, trims their rest and helps
    froglets grow. Tap again anywhere to kick it that way.
  - **Bubble Wand** (free) — tap or drag across the water to blow bubbles. No
    frog can leave one alone; popping one is worth zoomies and a little growing.
  - **Music Box** (free) — set it down in the pond and it plays whatever RibbitFM
    is on, and every frog nearby gathers round and bops on the beat. Tap the box
    again to pick it up.
- **The phone** (bottom right) — a frog-themed handset with twelve apps:
  - 🛒 **ShopHop** — buy the 8 starter frogs, unlock deeper snacks.
  - 📖 **FrogDex** — the collection. Unmet frogs are silhouettes; once you've met
    both parents of a recipe, the Dex reveals which snack it needs. It remembers
    every frog you've met even after you sell it, so selling never costs you progress.
  - 💬 **RibbitChat** — collectors message you wanting a specific frog and pay
    1.4–1.9× the shelf price. This is the main way to fund the fancy snacks.
  - ⚙️ **Settings** — sound, music and a pond reset.
  - 🌄 **Pondscape** — buy and apply 10 pond looks (dawn mist, blossom spring,
    autumn, rain, golden hour, moonlit, thunderhead, first snow, aurora) plus six
    little ornaments. Each look is a colour treatment of the same pond art with
    its own weather: snow, petals, rain, leaves, fireflies, stars, lightning.
  - 📷 **PondCam** — a live viewfinder of your actual pond, with a shutter that
    keeps real photos, and 🖼 **Album** to look back at them.
  - 📼 **RibbitFM** — four real pond tracks, synthesised note by note in the
    browser: *lilypad lullaby*, *puddle skip*, *moss and honey* and *rain on the
    rock*. Play, stop, skip, or pick one from the list; the sleeve doubles as a
    level meter. Whatever is on here is what the Music Box plays in the pond.
  - ⛅ **Cloudpad**, 👟 **Hopcount**, 🌙 **Frogscope** and 📓 **PondDiary** —
    a sky and weather readout, how far your frogs hopped today, a daily reading
    for one of them, and a diary the pond keeps of hatchings, sales and
    redecorating.
- **Goal** — meet all **36 species**. 8 are buyable; the other 28 are breed-only,
  four tiers deep, ending in two legendaries.

The pond holds 12 frogs at a time, which is the real pacing constraint: to go
deeper you sell frogs you've already recorded to make room.

Frogs squash and stretch on every hop, waddle between nearby spots, doze off
with a little `z`, croak, cast reflections in the water, and get the zoomies off
a matcha latte. Petting is free, and keeping at it builds a combo: more hearts,
a bigger squish, and by the fourth pet they bounce off in delight.

## The main menu

The menu is a **wooden sign hung over the pond** — nailed at both corners, lit
by a slow lantern glow, with fireflies drifting through the shade behind it while
frogs potter about in the live pond. A mascot sits on the sign and introduces
itself; pet it, or tap any of the nine friends below to meet one of them instead.

Under the big **hop in** are three panes, and only one is ever open — the button
for the open one lights up:

- **how to play** — the six things worth knowing, in order.
- **settings** — sound on/off, music on/off, and a track picker with the blurb
  for whatever is cued up. All of it works from the menu, before you start.
- **credits** — art & code by **Pukking Dragon**, plus the pond backdrop artist,
  the music and the typeface.

![the credits pane](docs/credits.png)

It remembers your pond, too: returning players get **continue** with a summary of
their frogs, dex and coins, and a **start fresh** button that asks twice.

## Tech notes

- A single self-contained `index.html` (~390 KB). Vanilla JS, no build step, no
  dependencies. Canvas renders at 640×400 and scales in crisp quarter-steps.
- **Input is pointer events only** — one code path for mouse and touch, so there
  is no duplicated mouse/touch logic to drift apart. The canvas takes
  `touch-action:none` so pinch-zoom and pull-to-scroll can't fight a drag, and
  pointer capture means a release outside the window still sets the frog down.
- **No loading screen, and nothing that can hang.** Every sprite atlas and the
  still pond are inlined as data URIs, so playing needs exactly one HTTP request
  (the page) and works from `file://` with the network unplugged. The title
  screen is up in ~150 ms. The only external file is the pond's animated gif,
  which is a pure upgrade over the still frame already on screen and is never
  awaited. If a decode somehow failed, the game falls back to procedural
  placeholder sprites rather than blocking.
- Atlases are palette PNGs with one reserved transparent index — lossless for
  this art (each sprite has ~15 colours) and about a third the size of RGBA.
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
  quiet pond hiss. **No audio files, and that includes the music**: the four
  tracks are a little step sequencer. Each is four bars of a 16-step grid where a
  digit picks a degree of the track's pentatonic scale and `-` holds the note,
  played by a soft triangle lead, a sine bass, a music-box pluck on the chord and
  a brushed shaker, scheduled ~0.3 s ahead off the audio clock. Muting or
  backgrounding the tab stops synthesis instead of queueing it up.
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

- **Art & code — Pukking Dragon.** Every frog, snack and icon, and the game
  itself. Also shown in-game under *credits* on the menu and in Settings.
- **Music** — the four pond tracks were written for this game and are synthesised
  in the browser; there are no audio files.
- **Animated pond backdrop** — pixel art by **@anasabdin**, whose watermark is
  left intact in the artwork.
- **Typeface** — [Pixelify Sans](https://fonts.google.com/specimen/Pixelify+Sans),
  under the Open Font License.

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

**Either** parent needs to have eaten the listed snack — not both.

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
