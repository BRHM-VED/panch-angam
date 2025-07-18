from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime, timedelta
import pytz
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'

# Panchanga name mappings
TITHI_NAMES = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada (Krishna)", "Dvitiya (Krishna)", "Tritiya (Krishna)", "Chaturthi (Krishna)", "Panchami (Krishna)",
    "Shashthi (Krishna)", "Saptami (Krishna)", "Ashtami (Krishna)", "Navami (Krishna)", "Dashami (Krishna)",
    "Ekadashi (Krishna)", "Dwadashi (Krishna)", "Trayodashi (Krishna)", "Chaturdashi (Krishna)", "Amavasya"
]
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
] + [None] * 49
YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]
NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]
RASHI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)",
    "Tula (Libra)", "Vrischika (Scorpio)", "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

def jd_to_time(jd):
    dt = datetime(2000, 1, 1, 12) + timedelta(days=jd - 2451545.0)
    return dt.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%I:%M %p")

def extract_summary(data):
    sunrise = jd_to_time(data["jd_sunrise"])
    sunset = jd_to_time(data["jd_sunset"])
    moonrise = jd_to_time(data["graha_rise_jd"]["moon"])
    moonset = jd_to_time(data["graha_set_jd"]["moon"])
    tithi_strs = []
    for idx, t in enumerate(data["sunrise_day_angas"]["tithis_with_ends"]):
        name = TITHI_NAMES[t["anga"]["index"] - 1]
        end_time = jd_to_time(t["jd_end"]) if "jd_end" in t else "end of day"
        tithi_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))
    nakshatra_strs = []
    for idx, n in enumerate(data["sunrise_day_angas"]["nakshatras_with_ends"]):
        name = NAKSHATRA_NAMES[n["anga"]["index"] - 1]
        end_time = jd_to_time(n["jd_end"]) if "jd_end" in n else "end of day"
        nakshatra_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))
    yoga_strs = []
    for idx, y in enumerate(data["sunrise_day_angas"]["yogas_with_ends"]):
        name = YOGA_NAMES[y["anga"]["index"] - 1]
        end_time = jd_to_time(y["jd_end"]) if "jd_end" in y else "end of day"
        yoga_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))
    karana_strs = []
    for idx, k in enumerate(data["sunrise_day_angas"]["karanas_with_ends"]):
        name = KARANA_NAMES[k["anga"]["index"] - 1] if KARANA_NAMES[k["anga"]["index"] - 1] else f"Karana #{k['anga']['index']}"
        end_time = jd_to_time(k["jd_end"]) if "jd_end" in k else "end of day"
        karana_strs.append(f"{name}" + (f" upto {end_time}" if "jd_end" in k else ""))
    weekday = datetime(data["date"]["year"], data["date"]["month"], data["date"]["day"]).strftime("%A")
    paksha = "Shukla Paksha" if data["lunar_date"]["index"] <= 15 else "Krishna Paksha"
    moonsign = RASHI_NAMES[data["sunrise_day_angas"]["raashis_with_ends"][0]["anga"]["index"] - 1]
    sunsign = RASHI_NAMES[data["sunrise_day_angas"]["graha_raashis_with_ends"]["sun"][0]["anga"]["index"] - 1]
    summary = {
        "Sunrise": sunrise,
        "Sunset": sunset,
        "Moonrise": moonrise,
        "Moonset": moonset,
        "Tithi": tithi_strs,
        "Nakshatra": nakshatra_strs,
        "Yoga": yoga_strs,
        "Karana": karana_strs,
        "Weekday": weekday,
        "Paksha": paksha,
        "Moonsign": moonsign,
        "Sunsign": sunsign
    }
    return summary

@app.route('/panchang_upload', methods=['GET', 'POST'])
def panchang_upload():
    if request.method == 'POST':
        if 'jsonfile' not in request.files:
            return 'No file part', 400
        file = request.files['jsonfile']
        if file.filename == '':
            return 'No selected file', 400
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        summary = extract_summary(data)
        date_obj = datetime(data["date"]["year"], data["date"]["month"], data["date"]["day"])
        date_str = date_obj.strftime('%B %d, %Y')
        return render_template('panchang_table.html', summary=summary, date_str=date_str)
    return '''
    <!doctype html>
    <title>Upload Panchangam JSON</title>
    <h1>Upload Panchangam JSON File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=jsonfile>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True) 