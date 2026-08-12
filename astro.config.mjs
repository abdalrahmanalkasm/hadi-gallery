import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // Netlify's default subdomain. Replace with the custom domain once one is
  // pointed at the site — this value is baked into the sitemap, the canonical
  // links and the absolute og:image URL, so a wrong value silently breaks
  // share cards and search indexing rather than erroring.
  site: 'https://hadi-gallery.netlify.app',
  build: { format: 'directory' },
  integrations: [sitemap()],
});
