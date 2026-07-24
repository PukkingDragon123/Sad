# 🐸 Froggy Pond — a cozy frog breeder simulator

A tiny pixel-art pond where you feed, breed, collect and sell round little frogs.
Everything lives in one file — no build, no dependencies.

## Play

Open `index.html` in any browser. That's it.
(Or serve the folder: `npx http-server` / `python3 -m http.server` and visit it.)

Your progress saves automatically in the browser (localStorage).

## How it works

- **Throw snacks** — click a snack in the tray, then click the pond.
  Frogs swarm to it; the closest one gets the bite. Every snack is its own
  little pixel sprite with its own description (the fly is free!).
- **Breed** — click a frog → `breed` to send it to the pink **love-pad**.
  Pick two frogs. If **both parents last snacked on the right food**, the egg
  hatches into a brand-new species — otherwise you get a copy of a parent
  (still great for selling).
- **The phone** (bottom right) has four apps:
  - 🛒 **ShopHop** — buy starter frogs and unlock fancier snacks.
  - 📖 **FrogDex** — your collection index. Undiscovered frogs are silhouettes;
    once you've met both parents of a recipe, the Dex reveals the snack hint.
  - 💬 **RibbitChat** — collectors message you wanting specific frogs and pay
    well over market price. This is how you fund the fancy snacks.
  - ⚙ **Settings** — sound toggle & pond reset.
- **Goal:** discover all **30 species**. 10 can be bought — the other 20 are
  **breed-only**, up to the legendary King Frog. Catch them all to become
  Pond Master.

Frogs are bouncy (squash & stretch on every hop), waddle for short strolls,
blink, croak, and get the zoomies from dragonflies. Petting is free and
encouraged.

## Tech notes

- Single `index.html` (~100 KB), vanilla JS + canvas at a 480×270 internal
  resolution, integer-ish scaled with crisp pixels.
- **All sprites are generated at runtime** from tiny pixel grids — each of the
  30 frog species and 12 snacks is composed (base body → per-species palette →
  pattern → accessory) into its own transparent-background sprite, i.e. a
  sprite sheet that's already split. Frame variants (blink, walk A/B) are
  generated per species; hops are tweened transforms.
- Sounds are synthesized with WebAudio — no audio assets.
- Font: [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P)
  (SIL Open Font License), embedded as base64 so the game works offline.
- `?fast` query param speeds up all timers ×10 (handy for testing).

## Spoilers — full recipe book

<details>
<summary>Click if you're truly stuck 🐸</summary>

| Baby | Parents | Both must snack on |
|---|---|---|
| Mint-Chip | Pond + Snow | Ice Pop |
| Bubblegum | Cherry + Snow | Berry |
| Honey | Lemon + Toffee | Honey Drop |
| Lilac | Blueberry + Snow | Berry |
| Tangerine | Lemon + Cherry | Berry |
| Cocoa | Inky + Toffee | Donut |
| Tabby | Toffee + Snow | Sushi |
| Shiba | Toffee + Peach | Donut |
| Sushi | Snow + Inky | Sushi |
| Pizza | Cherry + Lemon | Pizza Slice |
| Chili | Cherry + Inky | Hot Pepper |
| Earth | Moss + Sky | Berry |
| Glacier | Mint-Chip + Blueberry | Ice Pop |
| Galaxy | Inky + Blueberry | Star Candy |
| Lava | Chili + Inky | Hot Pepper |
| Cake | Bubblegum + Snow | Donut |
| Boba | Cocoa + Snow | Honey Drop |
| Moonlight | Snow + Galaxy | Moon Dew |
| Golden | Honey + Moonlight | Gold Apple |
| King | Golden + Moonlight | Gold Apple |

</details>
