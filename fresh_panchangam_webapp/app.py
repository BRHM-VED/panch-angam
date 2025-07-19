import os
import subprocess
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone
import pytz
from werkzeug.utils import secure_filename
import sys
from flask_cors import CORS
import swisseph as swe

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

@app.route('/kundli', methods=['GET'])
def kundli_page():
    return render_template('kundli.html')

@app.route('/api/kundli', methods=['POST'])
def generate_kundli():
    data = request.json
    # Required: date (YYYY-MM-DD), time (HH:MM), lat, lon, tz
    try:
        date_str = data['date']
        time_str = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])
        tz = float(data['tz'])
        dob = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except Exception as e:
        return jsonify({'error': f'Invalid input: {e}'}), 400

    rashi_names = [
        "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
        "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrischika (Scorpio)",
        "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
    ]
    planets = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN,
        'Rahu (Mean)': swe.MEAN_NODE
    }
    def get_navamsha_sign(sign, deg):
        segment = int(deg / 3.3333)
        return ((sign - 1) * 9 + segment) % 12 + 1

    jd_ut = swe.julday(dob.year, dob.month, dob.day, dob.hour + dob.minute/60 - tz)
    swe.set_ephe_path('.')
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    planet_positions = {}
    for planet, code in planets.items():
        pos = swe.calc_ut(jd_ut, code, flags=swe.FLG_SIDEREAL)[0][0]
        sign = int(pos / 30)
        deg = pos % 30
        nav_sign = get_navamsha_sign(sign + 1, deg)
        planet_positions[planet] = {
            'deg': deg,
            'sign': rashi_names[sign],
            'navamsha_sign': rashi_names[nav_sign - 1]
        }
    # Ketu
    rahu_pos = swe.calc_ut(jd_ut, swe.MEAN_NODE, flags=swe.FLG_SIDEREAL)[0][0]
    ketu_pos = (rahu_pos + 180) % 360
    ketu_sign = int(ketu_pos / 30)
    ketu_deg = ketu_pos % 30
    ketu_nav = get_navamsha_sign(ketu_sign + 1, ketu_deg)
    planet_positions['Ketu (Mean)'] = {
        'deg': ketu_deg,
        'sign': rashi_names[ketu_sign],
        'navamsha_sign': rashi_names[ketu_nav - 1]
    }
    # Lagna and Bhavas
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'A', flags=swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0] % 30
    lagna_sign = int(ascmc[0] / 30)
    lagna = {
        'deg': lagna_deg,
        'sign': rashi_names[lagna_sign]
    }
    bhavas = []
    for i in range(1, len(cusps)):
        cusp = cusps[i]
        bhava_start = (cusp - 15) % 360
        bhava_sign = int(bhava_start / 30)
        bhava_deg = bhava_start % 30
        bhavas.append({
            'house': i,
            'deg': bhava_deg,
            'sign': rashi_names[bhava_sign]
        })
    return jsonify({
        'input': {
            'date': date_str,
            'time': time_str,
            'lat': lat,
            'lon': lon,
            'tz': tz
        },
        'planets': planet_positions,
        'lagna': lagna,
        'bhavas': bhavas
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
            if not line or line.strip() == '':
                continue  # skip empty lines
            if i == 0:
                continue  # skip header
            parts = line.strip().split('\t')
            if not isinstance(parts, list) or len(parts) < 5:
                print(f"Skipping line {i}: parts={parts}")
                continue
            try:
                name, sa_name, lat, lon, tz = parts[:5]
            except Exception as e:
                print(f"Error unpacking line {i}: {parts}, error: {e}")
                continue
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