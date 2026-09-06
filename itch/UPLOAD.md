# Putting Froggy Pond on itch.io

Everything here is ready to upload — no build step, no export.

## The files

| file | what it is | where it goes |
|---|---|---|
| `../dist/froggy-pond-html5.zip` | `index.html` + `assets/pond.gif` | **Uploads → Upload files**, tick *This file will be played in the browser* |
| `../dist/froggy-pond-offline.zip` | the single self-contained `index.html` | optional second upload, *downloadable* |
| `cover-630x500.png` | the cover image itch asks for | **Cover image** |
| `thumbnail-315x250.png` | half-size cover, for anywhere a smaller one is wanted | — |
| `wide-1280x720.png` | wide version of the same art | social / OG image |
| `screenshot-1-menu.png` … `screenshot-4-mobile.png` | the menu, the pond, the phone, and a phone screen | **Screenshots** |

## Page settings that match the game

- **Kind of project:** HTML
- **Embed options:** *Click to launch in fullscreen* — or a manual viewport of **1280 × 720**
- **Mobile friendly:** on (*orientation: default*) — the menu and the pond both lay
  themselves out for a phone, and every control is a pointer event, so touch works
- **Frame the game with a border:** off, the pond fills its own frame

## Blurb you can paste

> A cozy pixel-art pond where you feed, breed, collect and sell round frogs.
> 36 species, 22 snacks, 8 tools and a little in-game phone with 14 apps.
> Every frog has a diet and will not breed on an empty stomach — find the pair,
> find the snack, meet somebody new. Plays with a mouse or a finger.

Art & code by Pukking Dragon. Pond backdrop by @anasabdin. Type is Pixelify Sans (OFL).
