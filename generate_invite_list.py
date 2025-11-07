#!/usr/bin/env python3
"""
generate_invite_list.py

Generate HTML file with registration list and WhatsApp/SMS message links.
Reads from CSV and creates a formatted HTML table with direct messaging links.
"""

import pandas as pd
import urllib.parse
import os

def main():
    # === CONFIG ===
    input_csv = "inviteList.csv"  # Input CSV file
    output_html = "MaladUtsav_Registration_List.html"  # Single output HTML file
    output_folder = "."  # Folder where the file will be saved

    # === READ CSV ===
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()

    # === SORT BY REGISTRATION ID ===
    df = df.sort_values(by="Registration ID")

    # === CREATE OUTPUT FOLDER ===
    os.makedirs(output_folder, exist_ok=True)

    # === START HTML CONTENT ===
    html = """
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Malad Utsav 2025 - Registration List</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #fafafa; color: #333; }
        h2 { text-align: center; color: #b22222; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 14px; }
        th { background-color: #f2f2f2; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
    </head>
    <body>
    <h2>🌸 Malad Utsav 2025 - Registration List 🌸</h2>
    <p style="text-align:center; font-size: 15px;">
    Click on <strong>WhatsApp</strong> or <strong>SMS</strong> link to send message directly.
    </p>
    <table>
    <tr>
        <th>#</th>
        <th>Member Name</th>
        <th>Registration ID</th>
        <th># of People</th>
        <th>WhatsApp</th>
        <th>SMS</th>
    </tr>
    """

    # === LOOP THROUGH DATA ===
    for i, row in enumerate(df.itertuples(index=False), start=1):
        name = str(row._0).strip()  # Member Name
        phone = str(row._1).strip()  # Member Whatsapp Phone Number
        num_people = str(row._2).strip()  # # of People
        reg_id = str(row._3).strip()  # Registration ID

        message = (
            f"🌸 *Jai Mahesh!* नमस्कार {name} जी,\n\n"
            "आपका *माहेश्वरी प्रगति मंडल*, मालाड क्षेत्रीय समितियों द्वारा आयोजित "
            "*मालाड उत्सव 2025* में हार्दिक स्वागत है! 🎉\n\n"
            f"आपकी पंजीकरण जानकारी इस प्रकार है:\n"
            f"📱 *Registered Mobile:* {phone}\n"
            f"🆔 *Registration ID:* {reg_id}\n"
            f"👨‍👩‍👧‍👦 *Registered for:* {num_people} सदस्य\n\n"
            "📅 *रविवार, 9 नवम्बर 2025*\n"
            "🕠 *कार्यक्रम प्रारंभ:* शाम 5:30 बजे से\n"
            "📍 *स्थल:* माहेश्वरी प्लॉट, बोरिवली (पश्चिम)\n"
            "📍 *Google Map Pin:* https://maps.app.goo.gl/81cSEuYJy9XTTzSD8\n\n"
            "☕ *Light Chai–Nashta:* शाम 5:00 बजे से उपलब्ध रहेगा\n"
            "🍛 *कार्यक्रम के बाद महाप्रसाद अवश्य लें*\n"
            "🅿️ *Valet Parking सुविधा उपलब्ध*\n"
            "🚇 *Nearest Metro Station:* Borivali West / Eksar\n\n"
            "कृपया समय पर पधारें और इस अद्भुत कार्यक्रम का पूर्ण आनंद उठाएँ! 🌼\n"
            "*Please show this message at the venue.*🙏"
        )

        encoded_message = urllib.parse.quote_plus(message)

        whatsapp_link = f'<a href="https://wa.me/91{phone}?text={encoded_message}" target="_blank">WhatsApp</a>'
        sms_link = f'<a href="sms:+91{phone}?body={encoded_message}" target="_blank">SMS</a>'

        html += f"""
        <tr>
            <td>{i}</td>
            <td>{name}</td>
            <td>{reg_id}</td>
            <td>{num_people}</td>
            <td>{whatsapp_link}</td>
            <td>{sms_link}</td>
        </tr>
        """

    # === CLOSE HTML ===
    html += """
    </table>
    <p style="text-align:center; margin-top:20px; font-size:13px; color:#555;">
    Generated automatically for internal communication - Malad Utsav 2025.
    </p>
    </body>
    </html>
    """

    # === SAVE HTML ===
    output_path = os.path.join(output_folder, output_html)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML file successfully created: {output_path}")

if __name__ == '__main__':
    main()