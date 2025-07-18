from flask import Flask, request, jsonify
import swisseph as swe
import datetime

app = Flask(__name__)

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
        dob = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except Exception as e:
        return jsonify({'error': f'Invalid input: {e}'}), 400

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

@app.route('/kundli')
def kundli_page():
    return render_template('kundli.html')

if __name__ == '__main__':
    app.run(debug=True) 