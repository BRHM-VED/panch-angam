import os
import subprocess
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone
import pytz
from werkzeug.utils import secure_filename
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    # Julian day 2451545.0 is 2000-01-01 12:00:00 UTC
    dt_utc = datetime(2000, 1, 1, 12, tzinfo=timezone.utc) + timedelta(days=jd - 2451545.0)
    dt_ist = dt_utc.astimezone(pytz.timezone("Asia/Kolkata"))
    return dt_ist.strftime("%I:%M %p")

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index_fresh.html')

@app.route('/get_panchang', methods=['POST'])
def get_panchang():
    data = request.json
    date_str = data.get('date')
    lat = data.get('lat')
    lon = data.get('lon')
    location = data.get('location', 'Unknown')
    year, month, day = map(int, date_str.split('-'))
    tz = 'Asia/Kolkata'
    args = [
        'python', '-m', 'jyotisha.panchaanga.writer.write_daily_panchaanga_json',
        location, str(lat), str(lon), tz, str(year), str(month), str(day)
    ]
    import os
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    try:
        print("Received date:", date_str, "lat:", lat, "lon:", lon, "tz:", tz)
        print("Subprocess command:", args)
        # Dynamically determine the project root (one level up from this file)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(BASE_DIR)
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            check=True,
            cwd=PROJECT_ROOT
        )
        print("Raw subprocess output:", repr(result.stdout))
        stdout = result.stdout
        start = stdout.find('{')
        end = stdout.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = stdout[start:end+1]
            panchang_json = json.loads(json_str)
        else:
            print("Could not find JSON in subprocess output!")
            print("Raw output:", repr(stdout))
            return jsonify({'error': 'Could not extract JSON from output.'}), 500
        summary = extract_summary(panchang_json)
    except subprocess.CalledProcessError as e:
        print('Subprocess error (stdout):', e.stdout)
        print('Subprocess error (stderr):', e.stderr)
        return jsonify({'error': f'Failed to generate Panchangam: {e}', 'details': e.stderr}), 500
    except Exception as e:
        print('General error:', str(e))
        return jsonify({'error': f'Failed to generate Panchangam: {e}'}), 500
    return jsonify({
        'summary': summary,
        'date_str': date_str,
        'location': location,
        'lat': lat,
        'lon': lon
    })

@app.route('/api', methods=['GET'])
def api_docs():
    return jsonify({
        "endpoints": {
            "/get_panchang": {
                "method": "POST",
                "description": "Get Panchangam data for a given date and location.",
                "body": {
                    "date": "YYYY-MM-DD",
                    "lat": "float",
                    "lon": "float",
                    "location": "string"
                },
                "response": {
                    "summary": "object",
                    "date_str": "string",
                    "location": "string",
                    "lat": "float",
                    "lon": "float"
                }
            }
        }
    })

@app.route('/get_places', methods=['GET'])
def get_places():
    import os

    # Get the absolute path to the directory this file is in
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # message Build the absolute path to the TSV file
    tsv_path = os.path.join(BASE_DIR, 'jyotisha', 'panchaanga', 'spatio_temporal', 'data', 'places_lat_lon_tz_db.tsv')

    places = []
    with open(tsv_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue  # skip header
            parts = line.strip().split('\t')
            if len(parts) < 5:
                continue
            name, sa_name, lat, lon, tz = parts[:5]
            # Convert DMS to decimal if needed
            def dms_to_decimal(val):
                if ':' in val:
                    parts = [float(x) for x in val.split(':')]
                    if len(parts) == 3:
                        return parts[0] + parts[1]/60 + parts[2]/3600
                    elif len(parts) == 2:
                        return parts[0] + parts[1]/60
                return float(val)
            try:
                lat_f = dms_to_decimal(lat)
                lon_f = dms_to_decimal(lon)
            except Exception:
                continue
            places.append({
                'name': name,
                'sa_name': sa_name,
                'lat': lat_f,
                'lon': lon_f,
                'tz': tz
            })
    return jsonify({'places': places})

if __name__ == '__main__':
    app.run(debug=True) 