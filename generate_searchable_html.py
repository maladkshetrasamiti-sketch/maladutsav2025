#!/usr/bin/env python3
"""
generate_searchable_html_nowrap.py

Creates a mobile-friendly searchable HTML with:
- Case-insensitive, partial-match search
- Yellow highlight for matched text
- Columns auto-fit content width (no wrapping)
- Horizontal scrolling when table is wider than screen
"""

import pandas as pd
from datetime import datetime
import argparse

def generate_html(csv_path, output_html="searchable_list_nowrap.html"):
    # Read and prep CSV
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    df.insert(0, "No", range(1, len(df) + 1))

    # Build table rows
    rows = []
    for _, r in df.iterrows():
        row_html = "".join(f"<td>{r[c]}</td>" for c in df.columns)
        rows.append(f"<tr>{row_html}</tr>")

    # ✅ CSS: no wrapping, full-width, horizontal scroll if overflow
    css = """
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #f8f9fa;
        margin: 0;
        padding: 0;
    }
    .container {
        width: 100%;
        background: #fff;
        padding: 14px;
        box-sizing: border-box;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    h1 {
        text-align: center;
        font-size: 1.4em;
        color: #2c3e50;
        margin: 10px 0 16px;
    }
    #searchInput {
        width: 90%;
        max-width: 500px;
        font-size: 1em;
        padding: 10px 14px;
        border-radius: 25px;
        border: 2px solid #007bff;
        margin-bottom: 16px;
    }
    .table-wrapper {
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.08);
    }
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95em;
        table-layout: auto; /* auto expands by content */
        white-space: nowrap; /* no wrapping inside cells */
    }
    th, td {
        padding: 10px 12px;
        border-bottom: 1px solid #eee;
        text-align: left;
        vertical-align: top;
    }
    th {
        background: #007bff;
        color: white;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    tr:nth-child(even) { background: #f8f8f8; }
    mark {
        background: yellow;
        color: black;
        font-weight: bold;
    }
    .no-results {
        display: none;
        text-align: center;
        color: #777;
        margin-top: 12px;
    }
    @media (max-width: 600px) {
        table { font-size: 0.9em; }
        th, td { padding: 8px 10px; }
    }
    """

    # ✅ JS: efficient highlight + search
    script = """
    function escapeHtml(text) {
      return text.replace(/[&<>"']/g, function(m) {
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m];
      });
    }

    function highlightText(text, term) {
      if (!term) return escapeHtml(text);
      const regex = new RegExp('(' + term + ')', 'gi');
      return escapeHtml(text).replace(regex, '<mark>$1</mark>');
    }

    function searchTable() {
      const input = document.getElementById('searchInput');
      const filter = input.value.trim().toLowerCase();
      const rows = document.querySelectorAll('#dataTable tbody tr');
      let found = false;

      rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let matchFound = false;
        cells.forEach(td => {
          const original = td.textContent || "";
          if (filter && original.toLowerCase().includes(filter)) {
            td.innerHTML = highlightText(original, filter);
            matchFound = true;
          } else {
            td.innerHTML = escapeHtml(original);
          }
        });
        row.style.display = matchFound || !filter ? "" : "none";
        if (matchFound) found = true;
      });

      document.getElementById('noResults').style.display = found || !filter ? "none" : "block";
    }
    """

    updated_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Build HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Malad Utsav 2025 - Searchable List</title>
      <style>{css}</style>
    </head>
    <body>
      <div class="container">
        <h1>Malad Utsav 2025 - Pre-Registered List</h1>
        <input id="searchInput" type="text" placeholder="🔍 Search by Name, Number, Registration, etc..." oninput="searchTable()" />
        <div class="table-wrapper">
          <table id="dataTable">
            <thead><tr>{''.join(f'<th>{c}</th>' for c in df.columns)}</tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>
        <div id="noResults" class="no-results">No matching results found</div>
        <div style="text-align:center; color:#777; margin-top:10px;">Updated on {updated_str}</div>
      </div>
      <script>{script}</script>
    </body>
    </html>
    """

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML generated successfully: {output_html}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate searchable HTML with full-width, no-wrap columns and highlights")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    parser.add_argument("--output", default="searchable_list_nowrap.html", help="Output HTML filename")
    args = parser.parse_args()

    generate_html(args.csv, args.output)
