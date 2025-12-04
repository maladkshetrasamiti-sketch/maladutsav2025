#!/usr/bin/env python3
"""
generate_certificates.py

Generate A4-sized certificates for students using:
- Student data from student_ppt_csv.csv
- Photos from Final_Processed_photos folder
- Signature images (Gautam_sign.png and Gopal_sign.png)
- Certificate layout template
"""

import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

# Configuration
INPUT_CSV = "student_ppt_csv.csv"
PHOTOS_FOLDER = "Final_Processed_photos"
OUTPUT_FOLDER = "Generated_Certificates"
SIGNATURES = {
    'gautam': 'Gautam_sign.png',
    'gopal': 'Gopal_sign.png'
}

def register_fonts():
    """Register custom fonts for the certificates."""
    try:
        # Register fonts (adjust paths as needed)
        pdfmetrics.registerFont(TTFont('Marathi', 'Marathi.ttf'))
        pdfmetrics.registerFont(TTFont('Hindi', 'Hindi.ttf'))
    except:
        print("⚠️ Could not load custom fonts. Using built-in fonts.")

def get_photo_path(student_name):
    """Get the photo file path for a student."""
    for ext in ['.jpg', '.jpeg', '.png']:
        photo_path = os.path.join(PHOTOS_FOLDER, f"{student_name}{ext}")
        if os.path.exists(photo_path):
            return photo_path
    return None

def create_certificate(student_data, output_path):
    """Create a single certificate PDF for a student."""
    # Create PDF with A4 size
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4  # A4 is 210x297mm
    
    # Draw certificate border
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    margin = 0.5 * inch
    c.rect(margin, margin, width - 2*margin, height - 2*margin)
    
    # Add header
    c.setFont("Times-Bold", 24)
    c.drawCentredString(width/2, height - 1.5*inch, "CERTIFICATE OF PARTICIPATION")
    
    # Add Marathi/Hindi text (using fallback font if custom fonts not available)
    try:
        c.setFont("Marathi", 18)
    except:
        c.setFont("Times-Roman", 18)
    c.drawCentredString(width/2, height - 2.2*inch, "माहेश्वरी प्रगति मंडल मालाड")
    
    # Add student name
    c.setFont("Times-Bold", 22)
    c.drawCentredString(width/2, height - 3*inch, student_data['Name'].upper())
    
    # Add student photo if available
    photo_path = get_photo_path(student_data['Name'])
    if photo_path:
        try:
            img = Image.open(photo_path)
            # Scale photo to 2x2 inches while maintaining aspect ratio
            img_width = 2 * inch
            img_height = 2 * inch
            c.drawImage(photo_path, (width - img_width)/2, height - 5.5*inch, 
                       width=img_width, height=img_height, preserveAspectRatio=True)
        except Exception as e:
            print(f"⚠️ Could not add photo for {student_data['Name']}: {e}")
    
    # Add signature images
    sig_width = 1.5 * inch
    sig_height = 0.75 * inch
    sig_y = 2.5 * inch
    
    # Left signature
    if os.path.exists(SIGNATURES['gautam']):
        c.drawImage(SIGNATURES['gautam'], width/3 - sig_width/2, sig_y,
                   width=sig_width, height=sig_height, preserveAspectRatio=True)
        c.setFont("Times-Roman", 12)
        c.drawCentredString(width/3, sig_y - 20, "Gautam Sign")
    
    # Right signature
    if os.path.exists(SIGNATURES['gopal']):
        c.drawImage(SIGNATURES['gopal'], 2*width/3 - sig_width/2, sig_y,
                   width=sig_width, height=sig_height, preserveAspectRatio=True)
        c.setFont("Times-Roman", 12)
        c.drawCentredString(2*width/3, sig_y - 20, "Gopal Sign")
    
    # Add date
    c.setFont("Times-Roman", 12)
    c.drawString(margin + 0.5*inch, margin + 0.5*inch, "Date: November 9, 2025")
    
    # Save the PDF
    c.save()

def main():
    """Main function to generate certificates for all students."""
    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Register custom fonts
    register_fonts()
    
    try:
        # Read student data
        df = pd.read_csv(INPUT_CSV)
        
        # Generate certificates for each student
        for idx, student in df.iterrows():
            output_path = os.path.join(OUTPUT_FOLDER, f"Certificate_{student['Name']}.pdf")
            try:
                create_certificate(student, output_path)
                print(f"✓ Created certificate for: {student['Name']}")
            except Exception as e:
                print(f"⚠️ Error creating certificate for {student['Name']}: {e}")
        
        print(f"\n✅ Certificate generation complete. Check the '{OUTPUT_FOLDER}' folder.")
    
    except Exception as e:
        print(f"⚠️ Error processing student data: {e}")

if __name__ == '__main__':
    main()