#!/usr/bin/env python3
"""
download_sheets.py

This script downloads:
1. Three specific Google Sheets as CSV files:
   - Calling List
   - Marksheet Submission
   - Malad Utsav
2. Images from two Google Drive folders:
   - Student Images
   - Marksheet Photos
"""

import os
import pandas as pd
import requests
import re
from datetime import datetime
import gdown
import shutil

# Configurations
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

FOLDERS = {
    'student_images': {
        'name': 'Student Images',
        'folder_id': '1PevxbqcqZsrZdW7NOfd_h95V3rZULt8-Y0cPAaFfr3mwyCp1t7caGrEpJT-32SoVZqXufkSl',
        'output_dir': 'student_images'
    },
    'marksheet_photos': {
        'name': 'Marksheet Photos',
        'folder_id': '1913u0ZcciIXSRGDxrn03FaCdhAkcCCCPUu-ik2f7GypMtV0SMFA7cl9HQXU8J-NQOtFwPcZp',
        'output_dir': 'marksheet_photos'
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

def download_subfolder(folder_url: str, output_dir: str, subfolder_name: str = "") -> int:
    """Download files from a subfolder and return number of files downloaded."""
    try:
        print(f"\nDownloading {subfolder_name if subfolder_name else 'files'}...")
        
        # Create subdirectory if name provided
        if subfolder_name:
            output_dir = os.path.join(output_dir, subfolder_name)
            os.makedirs(output_dir, exist_ok=True)
        
        # Try to download the folder
        files = gdown.download_folder(
            url=folder_url,
            output=output_dir,
            quiet=False,
            use_cookies=False
        )
        
        if not files:
            print(f"✗ No files downloaded from {subfolder_name if subfolder_name else folder_url}")
            return 0
            
        return len(files)
        
    except Exception as e:
        print(f"✗ Failed to download {subfolder_name if subfolder_name else folder_url}")
        print(f"Error: {str(e)}")
        return 0

def download_folder(folder_id: str, output_dir: str, folder_name: str) -> bool:
    """Download all files from a Google Drive folder by accessing sub-folders."""
    try:
        print(f"\nProcessing {folder_name}...")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct subfolder URLs (splitting into batches of 40 to be safe)
        subfolders = {
            'batch1': f"https://drive.google.com/drive/folders/{folder_id}/1-40",
            'batch2': f"https://drive.google.com/drive/folders/{folder_id}/41-80",
            'batch3': f"https://drive.google.com/drive/folders/{folder_id}/81-120",
            'batch4': f"https://drive.google.com/drive/folders/{folder_id}/121-160",
            'batch5': f"https://drive.google.com/drive/folders/{folder_id}/161-200"
        }
        
        total_files = 0
        for batch_name, subfolder_url in subfolders.items():
            files_downloaded = download_subfolder(subfolder_url, output_dir, "")
            total_files += files_downloaded
            if files_downloaded > 0:
                print(f"✓ Downloaded {files_downloaded} files from {batch_name}")
        
        # Try the main folder for any remaining files
        main_url = f"https://drive.google.com/drive/folders/{folder_id}"
        files_downloaded = download_subfolder(main_url, output_dir, "")
        total_files += files_downloaded
        
        if total_files > 0:
            print(f"\n✓ Successfully downloaded total {total_files} files to {output_dir}/")
            return True
        else:
            print(f"\n✗ No files were downloaded to {output_dir}/")
            return False
            
    except Exception as e:
        print(f"✗ Failed to download {folder_name}")
        print(f"Error: {str(e)}")
        return False

def main():
    print(f"Starting download at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Download sheets
    sheets_success = 0
    print("\n=== Downloading Sheets ===")
    for sheet_id, sheet_info in SHEETS.items():
        if download_sheet(
            sheet_info['sheet_id'],
            sheet_info['gid'],
            sheet_info['output'],
            sheet_info['name']
        ):
            sheets_success += 1
    
    # Download folders
    folders_success = 0
    print("\n=== Downloading Image Folders ===")
    for folder_id, folder_info in FOLDERS.items():
        if download_folder(
            folder_info['folder_id'],
            folder_info['output_dir'],
            folder_info['name']
        ):
            folders_success += 1
    
    print(f"\nDownload Summary:")
    print(f"- Sheets: {sheets_success} of {len(SHEETS)} downloaded successfully")
    print(f"- Folders: {folders_success} of {len(FOLDERS)} downloaded successfully")

if __name__ == '__main__':
    main()