# VELUMBRA — The City of the Second Dawn

[![make.fun bounty](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Aldo1q/the-poster-for-a-place/rank.svg)](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Aldo1q/the-poster-for-a-place/reward.svg)](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539)

A travel poster for a place that does not exist, drawn entirely in code.

**VELUMBRA, the City of the Second Dawn** — a harbour city terraced into a
white salt cliff on a tidal strait where the sun rises twice: once over the
sea, then again as a pale second sun reflected off the salt face. Its
landmark is the Lantern Stair, a coral-striped lighthouse reached by 214
steps cut into the rock, with the Port Serein ferry crossing below.

> Arrive for the first sunrise. Stay for the second.

Close-look details in the poster's bottom band: the Festival of the Second
Dawn, 14–21 June; Port Serein ferries at 06:10 · 09:40 · 15:20; and the
warning every visitor learns — *last ferry leaves before the tide forgets
the way home*. Velumbra Salt Line · Est. 1911.

Bounty: https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539

## How it works

- `render.py` draws the poster with PIL — gradient sky, two suns,
  mask-clipped salt-cliff strata, terraced houses, the lighthouse with its
  beams and stair zigzag, the Port Serein ferry, gulls and fine print
  grain — and writes `entry.png` (768 × 1024, under 1 MiB).
- `main.py` is the entrypoint (Python 3.13, standard library only): it
  validates `entry.png` against the gate (PNG header, dimensions, size),
  copies it to `$MAKEFUN_OUTPUT_DIR` (or `/output`), and SHA-256-verifies
  the copy.

## Run it

```sh
python3 render.py   # regenerate entry.png (needs Pillow)
python3 main.py     # validate and write /output/entry.png
```

## License

MIT — see `LICENSE`.
