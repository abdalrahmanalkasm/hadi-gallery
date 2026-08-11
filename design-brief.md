# Design Brief — Artist Portfolio

Produced by `design-lead`. This file is the project's memory. Read it before
any change. Sections marked 🔒 are inputs, not outputs.

---

## Locked input                      [🔒 locked]

**Subject:** A calling-card website for a single fine-art painter and
printmaker, graduate in Fine Arts. Body of work: oil on canvas, Chinese ink on
card, silkscreen and copper/zinc etching, graphite and watercolour studies.
19 works at launch.

**Audience:** Three, in order of volume — people arriving from an Instagram
link on a phone who do not know the artist; gallerists and curators assessing
whether the work is serious; occasional collectors checking availability.

**The one job:** In ten seconds, a stranger should understand what kind of
artist this is and want to look closer.

**Stack:** Astro 4, static output, plain CSS with custom properties. No
Tailwind, no shadcn, no component library, no token pipeline. English only.

**Already locked by the client:**
- Palette: black, white, ochre. Three colours, no fourth.
- Section order: Hero → About → Paintings → Prints → Studies → Exhibitions →
  Contact.
- Background rhythm alternates; About and Studies are ochre.
- One long page, plus one separate URL per work.
- Motion: soft reveal on scroll only.

---

## Direction                         [🔒 locked]
<!-- step 1 · frontend-design -->

**Thesis:**
The single most important fact about a painting is how big it is, and the web
erases it — every portfolio flattens a 150 cm canvas and a 15 cm sketch into
the same rectangle. This site refuses that. Works are drawn at true relative
scale, so a large canvas physically occupies more of the page than a small
study, and the reader scrolls further past it. The page argues that this is a
body of work made by a hand at different speeds and sizes, not a feed of images.

**Signature element:**
**The measure.** Every work is introduced by a drawn scale bar — a short ochre
rule whose length is proportional to the real width of the piece, labelled in
centimetres. It appears before the image, at the same width the image will be.
Across the page the measures form a visible rhythm: long for the canvases,
short for the studies. It is the one thing a visitor would describe afterwards.

**Reference points:**
- **Museum object labels** (Tate, V&A) — title, medium, dimensions set quietly
  at the edge of the work, never competing with it.
- **Architectural drawing sheets** — the scale bar treated as primary
  information, not a footnote.
- **Auction catalogue dimension lines** — the convention of stating size
  immediately after the medium, because buyers read size first.

**Deliberately avoided:**
- No uniform grid of equal tiles — that is the flattening this design exists
  to refuse.
- No full-bleed dark hero with the artist's name oversized across a portrait.
  Every artist site does this.
- No all-caps condensed labels, no hairline rule grid, no registration
  crosshairs. *(The previous build drifted into the broadsheet default; see
  the self-check below.)*
- No hover zoom, no image lightbox, no parallax, no scroll-jacking.
- No "Selected Works" as a heading. The work is the site.

**Risk taken:**
True relative scale makes the Studies section physically small on the page and
gives it less presence than the paintings. A floor of 24% of column width stops
it becoming unreadable, but a 21 cm drawing will still look minor next to a
150 cm canvas. That is the honest relationship between those two objects, and
showing it is the point — but it is a real cost, and it is the first thing to
revisit if the studies turn out to be the strongest work.

**AI-default gate — self-check:**
Checked against the three defaults. The previous build hit default 3
(broadsheet: hairline rules, zero radius, all-caps labels, dense columns) and
has been revised — the label system is now sentence-case museum labelling, and
the rule grid is gone. Default 1 (cream + serif + terracotta) is adjacent,
since the palette is locked to black/white/ochre and the text face is a serif.
Mitigated: the ground is pure white and true black, not cream; the serif is a
reading face, not a high-contrast display serif; and ochre is used
structurally — it draws the measures — rather than as a warm decorative accent.

---

## Values                            [🔒 locked]
<!-- step 2 · ui-ux-pro-max, constrained by locked palette -->

**Palette** — locked by client, not derived this run:

| Token | Hex | Role |
|---|---|---|
| ink | `#101010` | Hero, Prints, Footer grounds; all body text on light |
| paper | `#FFFFFF` | Paintings and Exhibitions grounds |
| ochre | `#A9762B` | About ground; every measure bar; links |
| ochre-pale | `#E9DCC3` | Studies ground |
| ochre-deep | `#6B4512` | Ochre darkened for text on light grounds |
| stone | `#767065` | Secondary label text |
| dot-sold | `#8C2F26` | The gallery red dot, sold status only |

**Type** — two faces, chosen from the direction, not from mood:
- **Newsreader** — everything readable. A face designed for long-form reading
  at small sizes, which is what a museum label is. Used for the artist's name,
  section titles, work titles, and body copy. One face across the whole site,
  because an object label uses one face.
- **IBM Plex Mono** — measurements, catalogue numbers, plate codes, and status
  only. Data is set in a technical face; prose is not. This is the same
  distinction an architectural sheet makes.

**Type scale** (1.25 ratio, four steps only):
`0.78 / 1 / 1.563 / 3.05 rem`, plus a display step that scales with viewport.
No fifth step. If content needs one, the content is wrong.

**Spacing scale:** 4 / 8 / 16 / 24 / 40 / 64 / 104 / 168 px.

---

## Voice                             [🔒 locked]
<!-- step 3 · brand -->

**Tone:** The artist speaking plainly about process, not a gallery speaking
about the artist. Concrete over evaluative — say what was done to the surface,
not how good it is. Never "stunning", "captivating", "journey", "explores
themes of".

**Rules:**
- Work notes describe a decision or a material fact: what was painted over,
  how many acid baths, which light it was made under.
- Never claim significance. The reader decides.
- Dimensions always before status. Size is the fact people want first.

**Vocabulary:**

| Use | Not |
|---|---|
| Available | For sale / Buy |
| Sold | — |
| Not for sale | Private collection *(unless true)* |
| Enquire about this work | Contact us / Get in touch |
| Detail | Close-up / Zoom |
| Works | Gallery / Portfolio / Selected works |

**Empty and missing states:** a work with no note shows no note. Never fill the
gap with generated description.

---

## Tokens                            [skipped]
<!-- step 4 · design-system -->

Not run. The project's `CLAUDE.md` forbids a three-layer token architecture —
19 works and one stylesheet do not justify a primitive→semantic→component
pipeline or a generator script. The tokens are the `:root` custom properties in
`src/styles/global.css`, documented in place.

---

## Assets                            [skipped]
<!-- step 5 · design -->

Not run. Requires a Gemini key that is not configured, and the artist does not
need a logo — the name set in Newsreader is the wordmark. Artwork photography
is supplied by the client; the pipeline for preparing it is
`scripts/prepare-images.py`.

---

## Build                             [🔒 locked]
<!-- step 6 · stack override -->

`ui-styling` was **not** run — it is shadcn + Tailwind only, and this stack is
Astro with plain CSS. Per the Design Lead stack-override rule, the Design Lead
owns the values and the stack owns the code. Built directly in Astro.

**Scale implementation:** each work's real width in centimetres is parsed from
its `dimensions` field at build time and converted to a column percentage:

```
widthPct = clamp(cm / 150 × 100, 24, 100)
```

150 cm is the largest work; it fills the column. The 24% floor keeps the
smallest studies legible on a phone. The same number drives both the image
width and the length of its measure bar, so the two can never disagree.

---

## Decisions log

| Date | Decision | By |
|---|---|---|
| — | Palette, section order, one-page + per-work URLs, English | Client |
| — | Direction: true relative scale, the measure as signature | `frontend-design` |
| — | Newsreader + IBM Plex Mono, replacing Archivo + Libre Franklin | `design-lead` |
| — | Previous build failed the AI-default gate (broadsheet); revised | `frontend-design` |
| — | `design-system`, `design`, `ui-styling` skipped — reasons above | `design-lead` |
