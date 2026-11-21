[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Aldo1q/the-poster-for-a-place/rank.svg)](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Aldo1q/the-poster-for-a-place/reward.svg)](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539)

# VELUMBRA — The City of the Second Dawn

An entry for make.fun's [The Poster for a Place That Isn't There](https://make.fun/c/the-poster-for-a-place-that-i-2-20261121-0539) bounty: a travel poster for a place that does not exist.

**Velumbra** is a harbour city terraced into a white salt cliff on a tidal
strait, famous for its Second Dawn: the sun rises over the sea, slips behind
the cliff for twenty minutes, then rises a second time off the salt face —
the pale second sun drawn low on the cliff in the poster. Its landmark is
the **Lantern Stair**, a striped lighthouse reached by 214 steps cut into
the rock. The poster's small print rewards a close look: the Festival of
the Second Dawn (14–21 June), the ferry times from Port Serein (06:10 ·
09:40 · 15:20), and the warning that the last ferry leaves before the tide
forgets the way home. Tagline: *Arrive for the first sunrise. Stay for the
second.*

## The program

`main.py` (Python 3, standard library only) copies the shipped `entry.png`
— the artwork rendered when this entry was built — into
`$MAKEFUN_OUTPUT_DIR` (or `/output`), after checking it is a whole PNG
inside the gate limits (≤ 1,048,576 bytes, ≤ 1024×1024), and verifies the
copy is byte-identical. It needs no network and no third-party packages.

`render.py` is the drawing program that produced `entry.png` with Pillow:
gradient sky, two suns, the layered salt cliff clipped to its silhouette,
terraced houses, the Lantern Stair lighthouse, the Port Serein ferry, and
the poster's typography are all drawn in code.

## License

MIT — see [LICENSE](LICENSE).
