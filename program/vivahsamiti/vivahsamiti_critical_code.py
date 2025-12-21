# === CONFIG ===
key = "vivahsamiti"
keyDescription = "Vivah Samiti"
Program_Name = "Meet n Greet - 2"
Team_Name = "Vivah Sahyog Samiti"
programFolder = "program"
mainFolder = f"program\\{key}\\"

karykarta_list = f"program\\{key}\\karykarta.csv"      # CSV must have 'Samiti Member Phone Number'
dashboard_for_adhyakya_csv = f"dashboard_{key}.html"

call_log_data_csv = f"program\\{key}\\call_log_data.csv"  # CSV must have 'Samiti Member Phone Number', 'Contact Name', 'Contact Phone Number', 'Call Status', 'Remarks'

karykarta_assignment_list = f"{mainFolder}karykarta_member_assignment.csv"      # CSV must have 'Samiti Member Phone Number'
karykarta_assignment_list_output_folder = f"{mainFolder}output\\"

github_base_url = "https://maladkshetrasamiti-sketch.github.io/maladutsav2025"  # Replace with your actual GitHub Pages URL
image_path = f"{github_base_url}/{mainFolder}/MPM_logo.png"

form_url_base = "https://docs.google.com/forms/d/e/1FAIpQLSddgJb-7qSWjw4vIjB-6rAddcIrCSTreRmbnNNAst2I_bd8dA/viewform?usp=pp_url"

event_message_in_person = (
    "🙏 Jai Shree Krishna\n\n"
    "Dear {} ji,\n\n"
    "Maheshwari Pragati Mandal, Mumbai\n\n"
    "Vivah Sahyog Samiti Presents\n\n"
    "✨ Meet & Greet - 2 ✨\n"
    "Camp Max, Kalote\n\n"
    "A unique extension of our \"Together Forever\" initiative — bringing eligible Maheshwari boys and girls together in a beautiful natural setting to connect, converse, and build meaningful bonds 🌲\n\n"
    "📅 Date: 17-18 January 2026\n"
    "📍 Venue: Camp Max, Kalote\n"
    "🌐 www.thecampmax.com\n\n"
    "🎁 Package Includes:\n"
    "✅ Pickup & Drop from Mumbai\n"
    "✅ All Meals\n"
    "✅ Overnight Stay & Glamping\n\n"
    "🎯 Activities:\n"
    "🔥 Campfire\n"
    "🎸 Music & Karaoke\n"
    "🚣 Kayaking\n"
    "⛺ Adventure & more!\n\n"
    "Register Now 👇\n"
    "https://forms.gle/iSME7QisCrrWydu9A\n\n"
    "📞 Contact:\n"
    "Kalpana Lohiyaa: +91 93230 08960\n\n"
    "Kanta Malpani: +91 93227 33821\n\n"
    "Jyoti Rathi: +91 87793 80780\n\n"
    "Note: Limited Seats, Only 40 boys and 40 Girls\n"
    "Registration on First come first serve basis."
)
        
message_to_karykartas = (f"🌸 जय महेश! 🙏\r\n"
    "प्रिय {} जी,\r\n\r\n"
    f"{Program_Name} के अंतर्गत आपकी calling list नीचे share की जा रही है —\r\n"
    "{}\r\n\r\n"
    "कृपया अपने निर्धारित संपर्कों से सप्रेम बात करें , WhatsApp karen और उन्हें Program main shamil होने के लिए motivate करें 💫\r\n"
    "आपका सहयोग इस आयोजन को सफल बनाने में महत्वपूर्ण है 🙏\r\n\r\n"
    f"– {Team_Name} 🌸"
    )

