# Tanish Urbania: SEO setup and launch checklist

## 1. Domain
The site is configured for `https://tanishurbania.com` (no www) in canonical tags, Open Graph tags,
JSON-LD, robots.txt and sitemap.xml. Redirect `www.tanishurbania.com` to `https://tanishurbania.com`
(and http to https) so only one version is indexed. To change the domain later:
`python3 set-domain.py https://new-domain.com`.

## 2. What is already in place
- Unique title (<= 60 chars) and meta description (<= 160 chars) on every page
- Canonical URL, hreflang (en-IN), robots directives with max-image-preview:large
- Open Graph and Twitter Card tags with a 1200x630 preview image (images/og-image.jpg)
- JSON-LD: Organization, WebSite, ApartmentComplex, WebPage, FAQPage (home);
  BlogPosting + BreadcrumbList (articles); CollectionPage (blog index)
- One H1 per page, logical H2/H3 order, descriptive alt text, image width/height (no layout shift)
- Hero image is a real <img> with fetchpriority=high and a preload (better Largest Contentful Paint)
- robots.txt (allows all, blocks thankyou.html and 404.html), sitemap.xml with image entries
- thankyou.html and 404.html are noindex
- Favicons, apple-touch-icon, web manifest

## 3. Google Search Console steps
1. Add the property (Domain property via DNS is best) at search.google.com/search-console.
2. Verify ownership (DNS TXT record, or the HTML tag method: paste the tag in <head> of index.html).
3. Sitemaps > submit `https://your-domain/sitemap.xml`.
4. URL Inspection > enter the home page > Request indexing. Repeat for each blog article.
5. After 3-7 days check Pages (indexing) and Enhancements (FAQ, breadcrumbs).
6. Check Core Web Vitals after a few weeks of traffic.
7. Also add the site to Bing Webmaster Tools (import from Search Console).

## 4. Hosting requirements for ranking
- HTTPS everywhere; redirect http -> https and non-www -> www (or the reverse), one version only
- Serve files with gzip/brotli and long cache headers for /images, /css and JS
- Serve 404.html for missing pages (status code must be 404)

## 5. Content and off-page work that moves rankings
- Add the RERA number, real price range, amenities and location distances on the page (and update the
  FAQ + JSON-LD to match). Real, specific facts rank and convert better than generic copy.
- Publish new articles regularly; target searches such as "2 BHK in Charholi", "flats near Ajinkya
  D.Y. Patil University", "new projects in Charholi PCMC".
- Create and verify a Google Business Profile for the sales office; keep the name, address and phone
  (+91 72640 11256) identical everywhere (NAP consistency).
- Get listings and backlinks from property portals, local news and the developer's own site.
- Keep the Google Maps link accurate; add geo coordinates to the JSON-LD when you have them.
- Do not use the meta keywords tag (Google ignores it).

## 6. Audit follow-up (added)
- Hosting file: `.htaccess` (Apache / LiteSpeed shared hosting) handles HTTPS, one canonical host (non-www), clean URLs
  without .html, caching, compression, security headers and the 404 page. Upload it next to index.html.
- Images are served as WebP with JPEG fallback; keep both files when adding images (`python3 build_blog.py` regenerates WebP).
- Every article shows its author, published and updated date. Update the "Updated" date when you change an article.
- Category pages have their own intro text and quick answers. Add more articles to each category over time so
  they grow beyond one article each; thin category pages rank poorly.
- Still needed from the client: RERA number, real price range, amenity list, floor plans, site address and geo coordinates.

## 7. Clean URL structure
    /                                         home
    /blog/                                    blog index
    /blog/<category>/                         category hub, e.g. /blog/nearby-schools/
    /blog/<category>/<article>/               article,      e.g. /blog/nearby-schools/schools-and-colleges/
    /thank-you/                               form confirmation (noindex)
Every page lives in its own folder with an index.html, so the links work on any host without rewrite rules.
Do not upload build_blog.py, blog_data/, set-domain.py, README.txt or this guide to the public site.
