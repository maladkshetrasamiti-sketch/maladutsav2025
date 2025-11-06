#!/usr/bin/env python3
"""
generate_parentlist_html.py

Usage:
    python generate_parentlist_html.py --sheet-id SHEET_ID --gid GID

This script downloads a Google Sheet as CSV (works if the sheet is viewable by link),
normalizes columns (Parent Name, Student Name, Timestamp/Submitted On), sorts by
parent name, and writes:
  - includes/header.html
  - includes/footer.html
  - ParentList_Marksheet.html

Optional --serve PORT will start a simple HTTP server to view the generated files
(if your browser blocks local file fetches for the include fragments).

If the sheet is private, use the gspread/service account approach (not implemented
here). See the printed message when download fails.
"""

import argparse
import io
import os
import sys
from datetime import datetime

try:
    import pandas as pd
    import requests
except Exception as e:
    print("Missing required packages. Run: pip install pandas requests")
    raise


def fetch_sheet_csv(sheet_id: str, gid: str, timeout: int = 15) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    print(f"Downloading CSV from: {url}")
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    text = resp.content.decode("utf-8", errors="replace")
    df = pd.read_csv(io.StringIO(text))
    print(len(df))
    return df


def normalize_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c.lower().strip(): c for c in df.columns}

    def find_col(possible):
        for p in possible:
            if p.lower() in cols:
                return cols[p.lower()]
        return None

    parent_col = find_col(["parent name", "parent", "parent_name"])
    student_col = find_col(["student name", "student", "student_name"])
    time_col = find_col(["timestamp", "submitted on", "submittedon", "submitted_on"])

    if parent_col is None:
        df['Parent Name'] = ''
        parent_col = 'Parent Name'
    if student_col is None:
        df['Student Name'] = ''
        student_col = 'Student Name'
    if time_col is None:
        df['Submitted On'] = ''
        time_col = 'Submitted On'

    # Keep canonical columns
    df = df[[parent_col, student_col, time_col]].copy()
    df.columns = ['Parent Name', 'Student Name', 'Submitted On']

    # Drop fully empty rows and rows where both Parent and Student are empty strings
    df = df.dropna(how='all')
    mask = (df['Parent Name'].astype(str).str.strip() != '') | (df['Student Name'].astype(str).str.strip() != '')
    df = df[mask].reset_index(drop=True)

    # Sort case-insensitive by parent then student
    df['Parent_sort'] = df['Parent Name'].astype(str).str.lower()
    df = df.sort_values(['Parent_sort', 'Student Name'], ascending=[True, True]).reset_index(drop=True)
    df = df.drop(columns=['Parent_sort'])

    # Add sequence number
    df.insert(0, 'No', range(1, len(df) + 1))
    return df


def esc(s: object) -> str:
    s = '' if s is None else str(s)
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def write_includes(includes_dir: str, updated_str: str):
    os.makedirs(includes_dir, exist_ok=True)
    header = (
        f'<div class="page-header">\n'
        f'  <h1>Parent and Student List</h1>\n'
        f'  <div class="updated">Updated: {updated_str}</div>\n'
        f'  <div style="text-align:center; margin-bottom:12px">\n'
        f'    <input id="searchInput" type="text" placeholder="Search parent, student or timestamp..." onkeyup="searchTable()" />\n'
        f'  </div>\n'
        f'</div>\n'
    )
    footer = f'<div class="footer">Generated on {updated_str}</div>\n'
    with open(os.path.join(includes_dir, 'header.html'), 'w', encoding='utf-8') as f:
        f.write(header)
    with open(os.path.join(includes_dir, 'footer.html'), 'w', encoding='utf-8') as f:
        f.write(footer)
    print(f"Wrote include fragments to: {includes_dir}")


def build_main_html(df: pd.DataFrame, includes_dir: str, output_html: str, updated_str: str):
    rows = []
    for _, r in df.iterrows():
        rows.append(
            f"<tr>"
            f"<td class=\"sequence-number\">{int(r['No'])}</td>"
            f"<td>{esc(r['Parent Name'])}</td>"
            f"<td>{esc(r['Student Name'])}</td>"
            f"<td>{esc(r['Submitted On'])}</td>"
            f"</tr>"
        )

    css = (
        "body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f5f5f5; padding:20px; }"
        " .container{ max-width:1200px; margin:0 auto; background:#fff; padding:20px; border-radius:10px; box-shadow:0 0 20px rgba(0,0,0,0.08); }"
        " h1{ text-align:center; color:#2c3e50; margin:0 0 12px }"
        " #searchInput{ width:80%; max-width:420px; padding:10px 14px; border-radius:25px; border:2px solid #3498db; }"
        " table{ width:100%; border-collapse:collapse; margin-top:16px }"
        " th,td{ padding:12px 10px; border-bottom:1px solid #eee; text-align:left }"
        " th{ background:#3498db; color:#fff; text-transform:uppercase }"
        " tr:nth-child(even){ background:#fafafa }"
        " .sequence-number{ color:#7f8c8d; width:50px }"
        " .footer{ text-align:center; color:#7f8c8d; margin-top:14px }"
        " .updated{ text-align:center; color:#7f8c8d; margin:6px 0 12px; font-size:0.95rem }"
        " .no-results{ text-align:center; color:#7f8c8d; padding:12px; display:none }"
        " @media (max-width:600px){ table{ display:block; overflow-x:auto } }"
    )

    main_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ParentList Marksheet</title>
<style>{css}</style>
</head>
<body>
  <div class="container">
        <!-- Search header (included here so it works even when client-side includes fail for file:///) -->
        <div class="page-header">
            <h1>Parent and Student List</h1>
            <div class="updated"><b>Updated: {updated_str}</b></div>
            <div style="text-align:center; margin-bottom:12px">
                <input id="searchInput" type="text" placeholder="Search parent, student or timestamp..." onkeyup="searchTable()" />
            </div>
    </div>
    <table id="dataTable">
      <thead>
        <tr><th class="sequence-number">#</th><th>Parent Name</th><th>Student Name</th><th>Submitted On</th></tr>
      </thead>
      <tbody>
{chr(10).join(rows)}
      </tbody>
    </table>
    <div id="noResults" class="no-results">No matching results found</div>
    <div data-include="{os.path.join('includes','footer.html')}"></div>
  </div>

<script>
// Simple client-side include: loads elements with data-include attribute
async function includeFragments() {{
  const els = document.querySelectorAll('[data-include]');
  for (const el of els) {{
    const url = el.getAttribute('data-include');
    try {{
      const r = await fetch(url);
      if (r.ok) el.innerHTML = await r.text();
      else el.innerHTML = '';
    }} catch (e) {{
      el.innerHTML = '';
    }}
  }}
}}

function searchTable() {{
  const input = document.getElementById('searchInput');
  const filter = (input && input.value ? input.value.toLowerCase() : '');
  const rows = document.getElementById('dataTable').getElementsByTagName('tr');
  let found = false;
  for (let i=1; i<rows.length; i++){{
    const cols = rows[i].getElementsByTagName('td');
    if (!cols || cols.length < 4) continue;
    const p = (cols[1].textContent || cols[1].innerText).toLowerCase();
    const s = (cols[2].textContent || cols[2].innerText).toLowerCase();
    const t = (cols[3].textContent || cols[3].innerText).toLowerCase();
    if (p.indexOf(filter) > -1 || s.indexOf(filter) > -1 || t.indexOf(filter) > -1) {{
      rows[i].style.display = '';
      found = true;
    }} else {{
      rows[i].style.display = 'none';
    }}
  }}
  document.getElementById('noResults').style.display = found ? 'none' : 'block';
}}

// Run includes on load
includeFragments();
</script>
</body>
</html>
    """

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(main_html)

    print(f"Wrote {output_html}")


def serve_folder(folder: str, port: int = 8000):
    # Use Python's http.server to serve files (useful because fetching local includes via file:// may be blocked)
    import http.server
    import socketserver
    cwd = os.getcwd()
    os.chdir(folder)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving {folder} at http://localhost:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server")
        finally:
            os.chdir(cwd)


def main():
    parser = argparse.ArgumentParser(description='Generate ParentList HTML from Google Sheet CSV')
    parser.add_argument('--sheet-id', default=None, help='Google sheet id (part of the URL)')
    parser.add_argument('--gid', default=None, help='sheet gid (tab id)')
    parser.add_argument('--csv-file', default=None, help='Path to a local CSV file (3 columns) to use instead of downloading from Google Sheets')
    parser.add_argument('--output', default='ParentList_Marksheet.html', help='output HTML filename')
    parser.add_argument('--serve', type=int, nargs='?', const=8000, help='serve the folder on this port after generation (optional)')
    args = parser.parse_args()

    sheet_id = args.sheet_id if args.sheet_id else os.environ.get('SHEET_ID')
    gid = args.gid if args.gid else os.environ.get('SHEET_GID')
    csv_file = args.csv_file

    # Allow using a local CSV file instead of downloading from Google Sheets.
    # Priority: --csv-file if provided, else sheet-id+gid (or env vars).
    if csv_file:
        if not os.path.exists(csv_file):
            print(f"CSV file not found: {csv_file}")
            sys.exit(1)
        try:
            print(f"Reading local CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
        except Exception as e:
            print('Failed to read local CSV file:', e)
            sys.exit(2)
    else:
        if not sheet_id or not gid:
            print('Sheet ID and gid are required when --csv-file is not provided. Either pass --sheet-id and --gid or set SHEET_ID and SHEET_GID environment variables.')
            parser.print_help()
            sys.exit(1)

        try:
            df = fetch_sheet_csv(sheet_id, gid)
        except Exception as e:
            print('\nFailed to download the sheet as CSV. If the sheet is private, make it "Anyone with the link" can view, or use a service account.\n')
            print('Error:', e)
            sys.exit(2)
    df = normalize_and_sort(df)

    includes_dir = os.path.join(os.path.dirname(args.output) or '.', 'includes')
    updated_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_includes(includes_dir, updated_str)
    build_main_html(df, includes_dir, args.output, updated_str)

    print(f"Done — generated {args.output} with {len(df)} rows.")
    if args.serve:
        folder = os.path.dirname(os.path.abspath(args.output)) or '.'
        serve_folder(folder, args.serve)


if __name__ == '__main__':
    main()
