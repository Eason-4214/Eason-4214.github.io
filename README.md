# Yiteng Sun — Academic Homepage

Public website: https://eason-4214.github.io/

Static, responsive academic homepage with biography, news, selected publications, education, and contact information. The HTML contains all content directly, with no JavaScript needed for reading or navigation.

## Update content

1. Edit `profile.json` to update the biography, news, papers, or education.
2. Add replacement images under `assets/` and update the corresponding paths in `profile.json`.
3. Run `python3 scripts/build.py` from this directory.
4. Commit and push the changed source and generated files to `main`.

GitHub Pages publishes from the root of `main`. `.nojekyll` enables plain static file hosting. Styles are in `style.css`. No packages or build service are required.

## Search engines

The site provides a canonical URL, descriptive title and description, an indexable static HTML body, `robots.txt`, `sitemap.xml`, and JSON-LD ProfilePage/Person metadata. These help discovery and interpretation but cannot guarantee indexing or ranking.

Google Search Console setup (requires the owner's Google account):

1. Open https://search.google.com/search-console/ and add the URL-prefix property `https://eason-4214.github.io/`.
2. Choose HTML-tag verification. Add the provided token as `googleSiteVerification` in `profile.json`, rebuild, and push. Alternatively, place Google's supplied verification HTML file in this repository root and push it.
3. Once the change is published, verify ownership in Search Console.
4. Submit `sitemap.xml` under Sitemaps, then inspect the homepage URL and request indexing if available.

Add the public homepage URL to your Google Scholar profile, ORCID website links, GitHub profile website field, and university profile where you manage them.

## Images

See `ASSET_SOURCES.md`. Image rights remain with their respective owners. The CV linked in the top navigation is the owner-provided PDF in `assets/CV_Yiteng_Sun.pdf`. Publication source PDFs are not included.
