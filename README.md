# DE Renewable Signal (80339)

This project provides a simple static HTML page that shows the renewable share of electricity and the corresponding traffic-light signal for Germany (postal code **80339**) using the public API from [energy-charts.info](https://energy-charts.info).

## How to use

Note: Opening the HTML file directly with `file://` will not load data due to CORS.

### GitHub Actions pipeline

A workflow at `.github/workflows/build-html.yml` fetches the API in Job 1, then builds a static HTML file in Job 2 and uploads it as an artifact.

- Artifact from Job 1: `api-data` (raw API JSON)
- Artifact from Job 2: `html-page` (`dist/de_renewable_signal.html`)

### Local build (static HTML)

```bash
python3 scripts/build_html.py --input tests/fixtures/api_sample.json --output dist/de_renewable_signal.html --postal-code 80339 --date 2026-03-01
```

### Tests

```bash
python3 -m unittest tests/test_build_html.py
```
