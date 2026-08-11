import { defineConfig } from 'astro/config';

export default defineConfig({
  // Change this to the real domain before launch. It is used for sitemap
  // and canonical URLs.
  site: 'https://example.com',
  build: { format: 'directory' }
});
