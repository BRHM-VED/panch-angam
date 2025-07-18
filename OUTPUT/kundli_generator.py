import swisseph as swe
import datetime

# 🔧 Location & Timezone (Chennai, IST)
LAT = 27.6
LON = 78.05
TZ = 5.5  # Indian Standard Time

# 📅 Date and 🕒 Time of Birth
dob = datetime.datetime(1997, 11, 27, 19, 30)
jd_ut = swe.julday(dob.year, dob.month, dob.day, dob.hour - TZ)

# 🗂 Set ephemeris path and sidereal mode
swe.set_ephe_path('.')  # Optional: directory for ephemeris files
swe.set_sid_mode(swe.SIDM_LAHIRI)  # ✅ Lahiri Ayanamsa (used by AstroSage)

# 🪐 Define Planets
planets = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN,
    'Rahu (Mean)': swe.MEAN_NODE
}

# ♈ Zodiac Signs
rashi_names = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrischika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

# 🧮 Navamsha Sign Calculation
def get_navamsha_sign(sign, deg):
    segment = int(deg / 3.3333)
    return ((sign - 1) * 9 + segment) % 12 + 1

# 🌟 Planetary Positions with Navamsha
print("🌟 Planetary Positions with Navamsha:")
planet_positions = {}
for planet, code in planets.items():
    pos = swe.calc_ut(jd_ut, code, flags=swe.FLG_SIDEREAL)[0][0]
    sign = int(pos / 30)
    deg = pos % 30
    nav_sign = get_navamsha_sign(sign + 1, deg)
    planet_positions[planet] = {
        'deg': deg,
        'sign': sign,
        'navamsha_sign': nav_sign
    }
    print(f"{planet:12s}: {deg:.2f}° {rashi_names[sign]}  (Navamsha: {rashi_names[nav_sign - 1]})")
# Ketu calculation (always 180 deg from Rahu)
rahu_pos = swe.calc_ut(jd_ut, swe.MEAN_NODE, flags=swe.FLG_SIDEREAL)[0][0]
ketu_pos = (rahu_pos + 180) % 360
ketu_sign = int(ketu_pos / 30)
ketu_deg = ketu_pos % 30
ketu_nav = get_navamsha_sign(ketu_sign + 1, ketu_deg)
print(f"Ketu (Mean): {ketu_deg:.2f}° {rashi_names[ketu_sign]}  (Navamsha: {rashi_names[ketu_nav - 1]})")

# 📍 Ascendant (Lagna) and House Cusps
cusps, ascmc = swe.houses_ex(jd_ut, LAT, LON, b'A', flags=swe.FLG_SIDEREAL)
lagna_deg = ascmc[0] % 30
lagna_sign = int(ascmc[0] / 30)

print(f"\n📍 Lagna (Ascendant): {lagna_deg:.2f}° {rashi_names[lagna_sign]}")

# 🏠 Parashara-style Bhava Starts (Cusp - 15°)
print("\n🏠 Bhava Start Points (Parashara Paddhati):")
print("Number of cusps:", len(cusps))
for i in range(1, len(cusps)):
    cusp = cusps[i]
    bhava_start = (cusp - 15) % 360
    bhava_sign = int(bhava_start / 30)
    bhava_deg = bhava_start % 30
    print(f"House {i:2d}: {bhava_deg:.2f}° {rashi_names[bhava_sign]}")
