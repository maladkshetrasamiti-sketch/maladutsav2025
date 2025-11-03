#!/usr/bin/env python3
"""
download_sheets.py

This script downloads three specific Google Sheets as CSV files:
1. Calling List
2. Marksheet Submission
3. Malad Utsav
"""

import os
import pandas as pd
import requests
from datetime import datetime

# Sheet configurations
SHEETS = {
    'calling_list': {
        'name': 'Calling List',
        'sheet_id': '1amWR-kKdPl7xg5ZDn2TECNvCF4hqh7dY7hQoTFHpt48',
        'gid': '1001823704',
        'output': 'Call_Log.csv'
    },
    'marksheet': {
        'name': 'Marksheet Submission',
        'sheet_id': '1ZHYLwglcO_uuQeZsfEKieOyq4tJzTKqlAQA99ZcaHTw',
        'gid': '481425432',
        'output': 'Marksheet_Log.csv'
    },
    'maladutsav': {
        'name': 'Malad Utsav',
        'sheet_id': '1-iPbPrgLLAK01thEuM3iCoUqcOcKW7RAde8lvkXx130',
        'gid': '1136736033',
        'output': 'MaladUtsav2025.csv'
    }
}

def download_sheet(sheet_id: str, gid: str, output_file: str, sheet_name: str) -> bool:
    """Download a Google Sheet as CSV and save it to the specified output file."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    try:
        print(f"\nDownloading {sheet_name}...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the raw CSV
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        # Load with pandas to verify it's valid CSV and get row count
        df = pd.read_csv(output_file)
        print(f"✓ Successfully downloaded {len(df)} rows to {output_file}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download {sheet_name}")
        print(f"Error: {str(e)}")
        return False

def main():
    print(f"Starting download at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success_count = 0
    for sheet_id, sheet_info in SHEETS.items():
        if download_sheet(
            sheet_info['sheet_id'],
            sheet_info['gid'],
            sheet_info['output'],
            sheet_info['name']
        ):
            success_count += 1
    
    print(f"\nDownload complete: {success_count} of {len(SHEETS)} sheets downloaded successfully")

if __name__ == '__main__':
    main()