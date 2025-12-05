# === CONFIG ===
key = "maladyuva"
Program_Name = "Sidhivinayak"
Team_Name = "Malad MPM Yuva Samiti"

programFolder = "program"
mainFolder = f"program\\{key}\\"

karykarta_list = f"program\\{key}\\karykarta.csv"      # CSV must have 'Samiti Member Phone Number'
dashboard_for_adhyakya_csv = f"dashboard_{key}.html"

call_log_data_csv = f"program\\{key}\\call_log_data.csv"  # CSV must have 'Samiti Member Phone Number', 'Contact Name', 'Contact Phone Number', 'Call Status', 'Remarks'

karykarta_assignment_list = f"{mainFolder}karykarta_member_assignment.csv"      # CSV must have 'Samiti Member Phone Number'
karykarta_assignment_list_output_folder = f"{mainFolder}output\\"

github_base_url = "https://maladkshetrasamiti-sketch.github.io/maladutsav2025"  # Replace with your actual GitHub Pages URL
image_path = f"{github_base_url}/{programFolder}/MPM_logo.png"

form_url_base = "https://docs.google.com/forms/d/e/1FAIpQLSddgJb-7qSWjw4vIjB-6rAddcIrCSTreRmbnNNAst2I_bd8dA/viewform?usp=pp_url"

event_message_in_person = (
    "Dear {} Ji,\n\n"
    "Maheshwari Pragati Mandal \n\n"
    "Malad Kshetriya Yuva Samiti Organises\n\n"
    "*🛕 Siddhivinayak Padyatra - A Spiritual walk to Siddhivinayak🚶🏽‍♂🚶🏼‍♀*\n\n"
    "Enjoy a spiritual walk to Siddhivinayak temple under the cool night sky as we go in a group singing and chanting along the way.\n\n"
    "Date - 20th December (Saturday)\n\n"
    "Time 🕙 - Departure at night 10.30 pm\n\n"
    "Location - From Chincholi Hanuman Mandir, S.V. Road\n\n"
    "Do register on below link and secure your spot now\n\n"
    "https://forms.gle/Q4Y92RSTE7DwPVzn9\n\n"
    "*Last date for registration 10th December 2025*\n\n"
    "Note -\n"
    "- Approx 21 kms Walking to Siddhivnayak via S.V. road\n"
    "- Return journey via bus till Hanuman Mandir, Malad SV road"
)
        
message_to_karykartas = (f"🌸 जय महेश! 🙏\r\n"
    "प्रिय {} जी,\r\n\r\n"
    f"{Program_Name} के अंतर्गत आपकी calling list नीचे share की जा रही है —\r\n"
    "{}\r\n\r\n"
    "कृपया अपने निर्धारित संपर्कों से सप्रेम बात करें , WhatsApp karen और उन्हें Program main shamil होने के लिए motivate करें 💫\r\n"
    "आपका सहयोग इस आयोजन को सफल बनाने में महत्वपूर्ण है 🙏\r\n\r\n"
    f"– {Team_Name} 🌸"
    )
