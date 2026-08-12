# CLAUDE.md

Context for Claude Code. Read this before making any change.

## Precedence

If a user-level `~/.claude/CLAUDE.md` is installed (for example the Design Pack
router), this file wins for anything inside this repository. Where they
disagree, follow this file and say out loud which instruction you are setting
aside.

The Design Pack's `design-lead` router may run. Its specialists must respect the
constraints below.

### Already decided — treat as locked from the first message

These were settled with the client before any code was written. In Design Pack
terms they enter every session **locked**, and a request to change something
else is never permission to reopen them:

- **Direction** — works are shown at true relative scale. That is the signature
  element. Full reasoning in `design-brief.md`. (The drawn measure bar that
  originally annotated it was removed at the client's request — see below.)
- **Palette** — black, white, ochre. Three colours. No fourth.
- **Type** — Newsreader (everything readable), IBM Plex Mono (measurements,
  catalogue numbers, plate codes, status). Two faces, no third.
- **Section rhythm** — the ink / ochre / paper alternation below.

If a change genuinely requires one of these to move, stop and ask first.

### Hard technical constraints

The build stack is fixed and is **not** a default that can be modernised:

- **No Tailwind.** No utility classes. Plain CSS with custom properties.
- **No shadcn/ui**, no component library, no React, Vue, or Svelte.
- **No token pipeline.** The design tokens are the `:root` custom properties in
  `src/styles/global.css`. Do not introduce a three-layer token architecture, a
  `tokens.json`, or a generator script — this project is too small for it.
- **No CSS-in-JS, no preprocessor.** One stylesheet.

If a specialist skill assumes Tailwind or shadcn, that assumption does not apply
here. Say so and build in plain CSS instead.

## What this is

A static portfolio website for a single fine-art painter and printmaker.
Its job is to be a credible calling card: someone lands here from Instagram or
a gallery email, understands who the artist is within ten seconds, and can look
closely at the work.

It is **not** a shop. There is no cart, no checkout, no payment. Enquiries go to
email.

Prices are the one exception, added later at the client's request against the
original brief. An asking price is shown for a work that has one, and only
while its `status` is `available` — a price beside a sold work reads as an
offer that no longer stands. Nothing else about the commerce rule moves: there
is still no cart, no checkout, and no payment, and the only call to action is
the email enquiry.

## Stack

- **Astro 4**, static output only. No SSR, no adapter.
- **No CSS framework.** Plain CSS with custom properties in `src/styles/global.css`.
- **No UI component library.** No React, Vue, or Svelte islands.
- **No client-side router.** Every page is a real HTML file.
- Client JavaScript is limited to four things, all in `src/layouts/Base.astro`:
  mobile menu toggle, `IntersectionObserver` scroll reveal, exhibition accordion,
  and the work-page lightbox. If a new feature needs more JS than that, raise it
  before writing it.

## Content model

All content lives in exactly two JSON files. Nothing else should hold copy.

- `src/data/works.json` — every artwork.
- `src/data/site.json` — artist bio, exhibitions, contact links.

Adding a work means: add one object to `works.json`, drop the image in
`public/images/`. Nothing else. The home page section and the
`/works/<slug>/` page are both generated from that object.

Fields on a work:

| field | notes |
|---|---|
| `slug` | URL segment, lowercase, hyphenated, never change after launch |
| `cat` | catalogue number, two digits, sequential |
| `section` | `paintings` \| `prints` \| `studies` \| `portraits` — decides where it appears |
| `code` | plate code, e.g. `OIL/CNV`, `INK/CARD`, `SCR/PRT`, `ETCH/CU` |
| `status` | `available` \| `sold` \| `nfs` |
| `edition` | prints only |
| `details` | array of close-up filenames; may be empty, and usually is |
| `note` | one or two sentences in the artist's voice; may be empty |
| `_ramp`, `_ar`, `_seed` | placeholder-generation only — delete once real photos exist |

## Design system — do not drift from this

`design-brief.md` is the source of truth for *why*. This section is the *what*.

Palette is three colours and nothing else. Do not introduce a fourth.

```
--ink        #101010
--paper      #FFFFFF
--ochre      #A9762B
--ochre-pale #E9DCC3
--ochre-deep #6B4512   (ochre darkened for text on light grounds)
--stone      #767065   (secondary label text)
--dot-sold   #8C2F26   (the gallery red dot, sold status only)
```

Section background rhythm, top to bottom. This alternation is the structure of
the page — keep it if you add sections:

```
Hero         ink
About        ochre
Paintings    paper
Prints       ink
Studies      ochre-pale
Portraits    ochre
Exhibitions  paper
Footer       ink
```

`Portraits` was added after launch planning, at the client's request. It sits
last of the work sections so that no existing section's ground had to move, and
takes `ochre` because that is the only ground that neither of its neighbours
(`ochre-pale` above, `paper` below) already uses.

Grounds are applied with `.g-ink`, `.g-paper`, `.g-ochre`, `.g-pale`. Each also
sets `.quiet` and `.accent` colours so contrast stays correct automatically. Use
those classes rather than writing new background rules.

Type, two faces only:

- **Newsreader** — everything a person reads. Name, section titles, work
  titles, body copy. A museum object label uses one text face; so does this.
- **IBM Plex Mono** (`.data`) — measurements, catalogue numbers, plate codes,
  status, nav. Data is set in a technical face; prose is not.

Four type steps (`--t-xs` … `--t-xl`) plus one viewport-scaled display step. Do
not add a fifth. If content seems to need one, the content is wrong.

### True relative scale — the signature element

A work's width on the page is its real width, mapped through `scalePct()` in
`src/lib/scale.js`, which parses the `dimensions` string. A 220 cm canvas fills
the column; a 10 cm panel takes a quarter of it. This is not decoration; it is
the design's whole argument, made visible. **Never** set a work's width by
hand, and never compute a second scale formula inline — one function owns it.

`.work-scaled` must keep `display: block`. It is an `<a>`, and `width` has no
effect on an inline box, so without it every work silently draws at full column
width and the argument disappears while the CSS still looks correct.

**The drawn measure was removed at the client's request.** It was an ochre rule
as wide as the image, ticked at both ends and labelled in centimetres, sitting
above every work. The scale it annotated stays; the sizes are now stated in each
label instead of drawn. Do not reintroduce the bar without asking.

The mapping is a square root, not a straight proportion. The reasoning is in
the file's comment; read it before changing `MAX_CM` or `MIN_PCT`.

Motion: scroll reveal only — 14px rise, once per element. It is progressive
enhancement: the `.js` class is added in `<head>` and only then does CSS hide
anything, so content stays visible if scripts fail. Keep it that way. No
parallax, no counters, no carousels, no hover zoom.

**Lightbox — added later at the client's request**, against the original brief.
It exists only on a work page, only on the lead image and the details, and only
on click; there is still no hover zoom anywhere, and the home page is untouched.
It is a native `<dialog>`, so Esc, the focus trap, and returning focus to the
button that opened it are the element's own behaviour rather than script.
Zoom runs from the fitted size up to one screen pixel per image pixel and no
further — past that the photograph has no more detail, only blur. The wheel
zooms anchored on the pointer, click toggles fitted against full, and `+`/`-`
/`0` do the same from the keyboard. Dragging pans, mouse only — a touch screen
already pans and pinches by itself and hijacking that makes it worse. A press
that travels more than a few pixels counts as a drag, anything shorter stays a
click, which is what lets one button both pan and toggle. Panning sets the
scroll box's own scroll position, so there is no gesture library, and with
scripts off the page is unchanged.

## Rules

- Never hardcode artwork copy into `.astro` files. It belongs in JSON.
- Never add a colour, typeface, or animation type not listed above.
- Never compute a work's display width outside `src/lib/scale.js`.
- Keep `prefers-reduced-motion` respected and keyboard focus visible.
- Images: always set `loading="lazy"` except the hero portrait and the lead
  image on a work page, which use `fetchpriority="high"`.
- Alt text describes the work — title and year — not "image of painting".
- Mobile is the primary case. Most visitors arrive from Instagram on a phone.
- Slugs are permanent once the site is live. Renaming one breaks links.

## Photography

Originals go in `photos-raw/` (never published, never modified). Run
`python3 scripts/prepare-images.py` to generate the web images and the JSON
stubs. Do not resize, rename, or compress by hand.

## Commands

```bash
npm install      # once
npm run dev      # local server at localhost:4321
npm run build    # static output to dist/
npm run preview  # serve dist/ locally to check the real build
```

## Before launch

- [ ] Replace every `[bracketed placeholder]` in `site.json`
- [ ] Replace all placeholder imagery in `public/images/` with real photography
- [ ] Delete the `_ramp` / `_ar` / `_seed` keys from `works.json`
- [ ] Add the real `public/cv.pdf`
- [ ] Set the real domain in `astro.config.mjs` (`site:`)
- [ ] Add `public/favicon.svg` and an Open Graph share image
