import json
import csv
import sys
from datetime import datetime, timedelta
import pytz
import os

tithi_names = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada (Krishna)", "Dvitiya (Krishna)", "Tritiya (Krishna)", "Chaturthi (Krishna)", "Panchami (Krishna)",
    "Shashthi (Krishna)", "Saptami (Krishna)", "Ashtami (Krishna)", "Navami (Krishna)", "Dashami (Krishna)",
    "Ekadashi (Krishna)", "Dwadashi (Krishna)", "Trayodashi (Krishna)", "Chaturdashi (Krishna)", "Amavasya"
]

karana_names = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
] + [None] * 49  # Padding to index 60

yoga_names = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]

nakshatra_names = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

rashi_names = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)",
    "Tula (Libra)", "Vrischika (Scorpio)", "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

def jd_to_time(jd):
    dt = datetime(2000, 1, 1, 12) + timedelta(days=jd - 2451545.0)
    return dt.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%I:%M %p")

def json_to_panchang_csv(json_path, csv_path=None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sunrise = jd_to_time(data["jd_sunrise"])
    sunset = jd_to_time(data["jd_sunset"])
    moonrise = jd_to_time(data["graha_rise_jd"]["moon"])
    moonset = jd_to_time(data["graha_set_jd"]["moon"])

    tithi_strs = []
    for idx, t in enumerate(data["sunrise_day_angas"]["tithis_with_ends"]):
        name = tithi_names[t["anga"]["index"] - 1]
        end_time = jd_to_time(t["jd_end"]) if "jd_end" in t else "end of day"
        tithi_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))

    nakshatra_strs = []
    for idx, n in enumerate(data["sunrise_day_angas"]["nakshatras_with_ends"]):
        name = nakshatra_names[n["anga"]["index"] - 1]
        end_time = jd_to_time(n["jd_end"]) if "jd_end" in n else "end of day"
        nakshatra_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))

    yoga_strs = []
    for idx, y in enumerate(data["sunrise_day_angas"]["yogas_with_ends"]):
        name = yoga_names[y["anga"]["index"] - 1]
        end_time = jd_to_time(y["jd_end"]) if "jd_end" in y else "end of day"
        yoga_strs.append(f"{name}" + (f" upto {end_time}" if idx == 0 else ""))

    karana_strs = []
    for idx, k in enumerate(data["sunrise_day_angas"]["karanas_with_ends"]):
        name = karana_names[k["anga"]["index"] - 1] if karana_names[k["anga"]["index"] - 1] else f"Karana #{k['anga']['index']}"
        end_time = jd_to_time(k["jd_end"]) if "jd_end" in k else "end of day"
        karana_strs.append(f"{name}" + (f" upto {end_time}" if "jd_end" in k else ""))

    weekday = datetime(data["date"]["year"], data["date"]["month"], data["date"]["day"]).strftime("%A")
    paksha = "Shukla Paksha" if data["lunar_date"]["index"] <= 15 else "Krishna Paksha"
    moonsign = rashi_names[data["sunrise_day_angas"]["raashis_with_ends"][0]["anga"]["index"] - 1]
    sunsign = rashi_names[data["sunrise_day_angas"]["graha_raashis_with_ends"]["sun"][0]["anga"]["index"] - 1]

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

    if not csv_path:
        city = data["city"]["name"].replace(" ", "_")
        dt = datetime(data["date"]["year"], data["date"]["month"], data["date"]["day"])
        csv_path = f"OUTPUT/{city}_Panchang_-_{dt.strftime('%B_%d__%Y')}.csv"

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["", "Value"])
        for k, v in summary.items():
            if isinstance(v, list):
                writer.writerow([k, str(v)])
            else:
                writer.writerow([k, v])
    print(f"CSV written to {csv_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_to_panchang_csv.py <input_json> [output_csv]")
        sys.exit(1)
    json_path = sys.argv[1]
    csv_path = sys.argv[2] if len(sys.argv) > 2 else None
    json_to_panchang_csv(json_path, csv_path) 