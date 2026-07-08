# DE Renewable Signal (80339)

This project provides a simple static HTML page that shows the renewable share of electricity and the corresponding traffic-light signal for Germany (postal code **80339**) using the public API from [energy-charts.info](https://energy-charts.info).

The generated HTML page filters and displays energy signal rows for daytime and evening hours (**08:00 to 23:00 CET**).

## How to use

Because the Python build script pre-renders all data directly into the HTML table, the output file is entirely static. You can open the generated HTML file directly in any web browser (`file://` protocol) without needing a local web server or encountering CORS issues.

### GitHub Actions pipeline

A workflow at `.github/workflows/build-html.yml` fetches the API in Job 1, then builds a static HTML file in Job 2 and uploads it as an artifact. It also publishes the output to GitHub Pages.

- Artifact from Job 1: `api-data` (raw API JSON)
- Artifact from Job 2: `html-page` (`dist/de_renewable_signal.html`)
- Pages output: `dist/index.html` (copy of `dist/de_renewable_signal.html`)

To enable Pages, set the repository Pages source to **GitHub Actions**.

Once enabled, the site will be available at:

- `https://ruuubens.github.io/deenergy/`

### Local build (static HTML)

You can build the HTML locally using the Python script:

```bash
python3 scripts/build_html.py --input tests/fixtures/api_sample.json --output dist/de_renewable_signal.html --postal-code 80339 --date 2026-03-01
