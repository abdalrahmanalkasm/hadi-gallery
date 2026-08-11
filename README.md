# Artist Portfolio

Static site built with Astro. Black, white and ochre. English.

## Run it

```bash
npm install
npm run dev
```

Open http://localhost:4321

## Structure

```
src/
  data/
    works.json        every artwork — the file you edit most
    site.json         bio, exhibitions, contact
  styles/global.css   the whole design system, one file
  components/         Nav, RegMark, SectionHead, Status
  layouts/Base.astro  head, fonts, nav, the three client scripts
  pages/
    index.astro       the single long home page
    works/[slug].astro  generates one page per artwork
public/images/        artwork photography
CLAUDE.md             read this first if you are Claude Code
```

## Add a new artwork

1. Put the photograph in `public/images/`, e.g. `new-painting.jpg`
2. Add an object to the `works` array in `src/data/works.json`:

```json
{
  "slug": "new-painting",
  "cat": "20",
  "title": "New Painting",
  "year": 2026,
  "section": "paintings",
  "medium": "Oil on canvas",
  "code": "OIL/CNV",
  "dimensions": "100 × 80 cm",
  "status": "available",
  "image": "new-painting.jpg",
  "details": [],
  "note": ""
}
```

That's it. The home page and `/works/new-painting/` both appear on next build.

## Photography

The images currently in `public/images/` are generated placeholders, not
artwork. Replace them. When shooting:

- Camera square to the canvas, work lit evenly from both sides at ~45°
- No flash — oil paint reflects and the glare cannot be fixed later
- Include a colour reference card in one frame per session
- Shoot RAW, keep the originals, export long-edge 2400px JPEG for the site
- For the few works that deserve them, shoot 2–3 close-ups of surface and edge

## Deploy

Any static host works. Netlify or Cloudflare Pages:

- Build command: `npm run build`
- Publish directory: `dist`
