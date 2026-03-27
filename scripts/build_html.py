#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, date, timezone
from zoneinfo import ZoneInfo

CET = ZoneInfo("Europe/Berlin")


def map_signal(value):
    if value == -1:
        return "Red", "Grid congestion", "red"
    if value == 0:
        return "Red", "Low renewable share", "red"
    if value == 1:
        return "Yellow", "Average renewable share", "yellow"
    if value == 2:
        return "Green", "High renewable share", "green"
    return "Unknown", "No mapping available", ""


def format_time_cet(dt):
    return dt.strftime("%H:%M")


def build_rows(payload, day_cet):
    times = payload.get("timestamps") or payload.get("time") or payload.get("unix_seconds") or []
    shares = payload.get("share_renewables") or payload.get("renewable_share") or payload.get("share") or []
    signals = payload.get("signal") or payload.get("signals") or []

    if not times or not signals or not shares:
        raise ValueError("Missing expected fields in API response.")

    rows = []
    for i, t in enumerate(times):
        if len(str(t)) == 10:
            t = int(t) * 1000
        dt = datetime.fromtimestamp(int(t) / 1000, tz=timezone.utc).astimezone(CET)

        if dt.date() != day_cet:
            continue
        if dt.hour < 8 or dt.hour > 23:
            continue

        share_val = shares[i] if i < len(shares) else None
        signal_val = signals[i] if i < len(signals) else None
        if share_val is None or signal_val is None:
            continue

        label, desc, css = map_signal(signal_val)
        rows.append({
            "time": format_time_cet(dt),
            "share": f"{float(share_val):.1f}",
            "label": label,
            "desc": desc,
            "css": css
        })
    return rows


def render_html(rows, postal_code, day_cet):
    date_str = day_cet.strftime("%Y-%m-%d")
    title = f"Germany Renewable share of electricity - München (80339) ({date_str})"
    status = "No rows for today 08:00-23:00 CET." if not rows else "Showing today's values between 08:00 and 23:00 CET."

    row_html = []
    for row in rows:
        cls = f" class=\"{row['css']}\"" if row["css"] else ""
        row_html.append(
            "<tr{cls}><td>{time}</td><td>{share}</td><td>{label}</td><td>{desc}</td></tr>".format(
                cls=cls,
                time=row["time"],
                share=row["share"],
                label=row["label"],
                desc=row["desc"]
            )
        )

    rows_block = "\n      ".join(row_html) if row_html else ""

    return """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif; margin: 20px; }}
    h1 {{ font-size: 1.4rem; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
    th, td {{ border: 1px solid #ccc; padding: 6px 8px; text-align: center; }}
    th {{ background: #f2f2f2; }}
    .red {{ background-color: #fdd; }}
    .yellow {{ background-color: #fffae0; }}
    .green {{ background-color: #e4f8e4; }}
    #status {{ margin-top: 10px; font-size: 0.9rem; color: #555; }}
  </style>
</head>
<body>
  <h1>Germany Renewable Share Signal - {postal_code} ({date_str}, CET)</h1>
  <div id=\"status\">{status}</div>
  <table>
    <thead>
      <tr>
        <th>Time (CET)</th>
        <th>Renewable Share (%)</th>
        <th>Signal</th>
        <th>Signal Description</th>
      </tr>
    </thead>
    <tbody>
      {rows_block}
    </tbody>
  </table>
</body>
</html>
""".format(title=title, postal_code=postal_code, status=status, rows_block=rows_block, date_str=date_str)


def main():
    parser = argparse.ArgumentParser(description="Build static HTML from API data.")
    parser.add_argument("--input", required=True, help="Path to API JSON response")
    parser.add_argument("--output", required=True, help="Path to HTML output")
    parser.add_argument("--postal-code", default="80339", help="Postal code label")
    parser.add_argument("--date", default="", help="CET date YYYY-MM-DD for deterministic builds")
    args = parser.parse_args()

    day_cet = date.fromisoformat(args.date) if args.date else datetime.now(CET).date()

    with open(args.input, "r", encoding="utf-8") as fh:
        payload = json.load(fh)

    rows = build_rows(payload, day_cet)
    html = render_html(rows, args.postal_code, day_cet)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(html)


if __name__ == "__main__":
    main()
