# FreeTools4U

FreeTools4U is a static HTML/CSS/JavaScript website containing browser-based productivity tools, plus a separate FastAPI service for PDF-to-Word conversion.

## Site structure

- `index.html` — tool directory and homepage
- `tools/` — individual tool pages
- `assets/tool-page.css` and `assets/tool-page.js` — shared styles and behavior for the first ten browser tools
- `about.html`, `privacy.html`, `terms.html` — site information and policy pages
- `contact.html` — contact information placeholder; currently marked noindex until verified public contact details are added
- `sitemap.xml` and `robots.txt` — search crawling configuration
- `server/main.py` — PDF-to-Word API service

## Browser tools

The first ten tools process their inputs in the browser: Word Counter, Case Converter, Duplicate Line Remover, Text Line Sorter, Percentage Calculator, Discount Calculator, Age Calculator, Date Difference Calculator, JSON Formatter, and Password Generator.

The Volume Optimizer uses browser tab capture and the Web Audio API. It does not change the operating system's master volume.

## PDF to Word processing

The PDF-to-Word page uploads a PDF to the separate Render-hosted FastAPI service. The API accepts PDF files up to 20 MB and uses temporary files during conversion. The application attempts to remove the temporary PDF and DOCX files in a cleanup block after processing. Review `privacy.html` before changing this behavior or the disclosure on the website.

## Local checks before deployment

1. Open every tool page directly, not only through the homepage.
2. Test each tool with empty input, normal input, invalid input, and boundary values.
3. Test the pages at desktop and mobile widths and with keyboard navigation.
4. Test PDF conversion with a simple text PDF, a multi-page PDF, and a scanned/image-only PDF; confirm the API is awake and configured for the production domain.
5. Check every internal link, canonical URL, sitemap URL, and favicon after deployment.
6. Confirm the custom domain is configured in GitHub Pages and DNS before changing `CNAME`.
7. Add an `ads.txt` record and AdSense script only after the real publisher account ID and seller details are available. Do not use placeholder IDs.

## AdSense preparation

The site should be complete, useful, easy to navigate, and compliant with Google's publisher policies before applying. The policy pages are informational groundwork, not a guarantee of approval. Google does not publish a universal word-count threshold that guarantees approval.

Useful official references:
- https://support.google.com/adsense/answer/7299563
- https://support.google.com/adsense/answer/81904
- https://support.google.com/adsense/answer/48182
- https://support.google.com/adsense/answer/10502938

## Important deployment notes

- The canonical host used in page metadata and the sitemap is `https://freetools4u.xyz` (non-www).
- The repository's `CNAME` file is currently empty. Verify the GitHub Pages custom-domain setting and DNS before writing a domain value into it.
- `ads.txt` is currently empty because no verified AdSense publisher ID was supplied. Populate it only with the exact seller record provided by the publisher account.
- The Contact page is intentionally excluded from the sitemap and search indexing until verified contact details are provided.
