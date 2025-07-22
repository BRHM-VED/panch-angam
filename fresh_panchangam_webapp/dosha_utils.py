# Dosha detection utilities for Vedic astrology

# Sign lords (rashi lords) - same as yoga_utils but needed for dosha calculations
SIGN_LORDS = {
    1: "Mars",    # Aries
    2: "Venus",   # Taurus
    3: "Mercury", # Gemini
    4: "Moon",    # Cancer
    5: "Sun",     # Leo
    6: "Mercury", # Virgo
    7: "Venus",   # Libra
    8: "Mars",    # Scorpio
    9: "Jupiter", # Sagittarius
    10: "Saturn", # Capricorn
    11: "Saturn", # Aquarius
    12: "Jupiter" # Pisces
}

# Exaltation and debilitation signs
EXALTATION_SIGNS = {
    "Sun": 1,      # Aries
    "Moon": 2,     # Taurus
    "Mars": 10,    # Capricorn
    "Mercury": 6,  # Virgo
    "Jupiter": 4,  # Cancer
    "Venus": 12,   # Pisces
    "Saturn": 7,   # Libra
    "Rahu (Mean)": 3,  # Gemini
    "Ketu (Mean)": 9   # Sagittarius
}

DEBILITATION_SIGNS = {
    "Sun": 7,      # Libra
    "Moon": 8,     # Scorpio
    "Mars": 4,     # Cancer
    "Mercury": 12, # Pisces
    "Jupiter": 10, # Capricorn
    "Venus": 6,    # Virgo
    "Saturn": 1,   # Aries
    "Rahu (Mean)": 9,  # Sagittarius
    "Ketu (Mean)": 3   # Gemini
}

# Nakshatra lords for Nadi dosha
NAKSHATRA_LORDS = {
    1: "Ketu", 2: "Venus", 3: "Sun", 4: "Moon", 5: "Mars", 6: "Rahu", 7: "Jupiter",
    8: "Saturn", 9: "Mercury", 10: "Ketu", 11: "Venus", 12: "Sun", 13: "Moon",
    14: "Mars", 15: "Rahu", 16: "Jupiter", 17: "Saturn", 18: "Mercury", 19: "Ketu",
    20: "Venus", 21: "Sun", 22: "Moon", 23: "Mars", 24: "Rahu", 25: "Jupiter",
    26: "Saturn", 27: "Mercury"
}

# Dosha-specific house combinations
MANGAL_DOSHA_HOUSES = [1, 2, 4, 7, 8, 12]  # Houses where Mars causes Mangal Dosha
PITRA_DOSHA_HOUSES = [9, 10, 11]  # Houses related to father
MATRI_DOSHA_HOUSES = [4, 10]  # Houses related to mother
PRET_DOSHA_HOUSES = [8, 12]  # Houses related to death/ghosts
TARA_DOSHA_HOUSES = [6, 8, 12]  # Houses related to Tara dosha
MRITYU_DOSHA_HOUSES = [8, 12]  # Houses related to death

def get_sign_lord(sign_number):
    """Get the lord of a zodiac sign"""
    return SIGN_LORDS.get(sign_number, "Unknown")

def is_exalted(planet, sign_number):
    """Check if a planet is exalted in a sign"""
    return EXALTATION_SIGNS.get(planet) == sign_number

def is_debilitated(planet, sign_number):
    """Check if a planet is debilitated in a sign"""
    return DEBILITATION_SIGNS.get(planet) == sign_number

def get_planet_strength(planet, sign_number):
    """Get the strength of a planet based on its position"""
    if is_exalted(planet, sign_number):
        return "Exalted"
    elif is_debilitated(planet, sign_number):
        return "Debilitated"
    elif get_sign_lord(sign_number) == planet:
        return "Own Sign"
    else:
        return "Neutral"

def is_conjunct(planet1_house, planet2_house):
    """Check if planets are in the same house"""
    return planet1_house == planet2_house

def is_opposite(planet1_house, planet2_house):
    """Check if planets are in opposite houses (7th aspect)"""
    return abs(planet1_house - planet2_house) == 6

def get_aspect(planet1_house, planet2_house):
    """Get aspect between two houses"""
    diff = abs(planet1_house - planet2_house)
    if diff == 0:
        return "Conjunction"
    elif diff == 6:
        return "7th"
    elif diff == 3:
        return "4th"
    elif diff == 9:
        return "10th"
    elif diff == 4:
        return "5th"
    elif diff == 8:
        return "9th"
    elif diff == 2:
        return "3rd"
    elif diff == 10:
        return "11th"
    else:
        return "No Aspect"

def has_aspect(planet1_house, planet2_house, aspect_type="7th"):
    """Check if two planets have a specific aspect"""
    aspect = get_aspect(planet1_house, planet2_house)
    return aspect == aspect_type

def get_house_relationship(house1, house2):
    """Get the relationship between two houses"""
    diff = abs(house1 - house2)
    if diff == 0:
        return "Same House"
    elif diff == 6:
        return "Opposite"
    elif diff in [1, 5, 7, 11]:
        return "Adjacent"
    elif diff in [2, 4, 8, 10]:
        return "Trine"
    elif diff in [3, 9]:
        return "Square"
    else:
        return "Other"

def is_benefic_planet(planet):
    """Check if a planet is generally benefic"""
    benefic_planets = ["Jupiter", "Venus", "Mercury"]
    return planet in benefic_planets

def is_malefic_planet(planet):
    """Check if a planet is generally malefic"""
    malefic_planets = ["Saturn", "Mars", "Sun"]
    return planet in malefic_planets

def get_planet_nature(planet):
    """Get the nature of a planet"""
    if is_benefic_planet(planet):
        return "Benefic"
    elif is_malefic_planet(planet):
        return "Malefic"
    else:
        return "Neutral"

def calculate_nakshatra(moon_position):
    """Calculate nakshatra from moon position (0-360 degrees)"""
    nakshatra_number = int(moon_position / 13.3333) + 1
    return nakshatra_number if nakshatra_number <= 27 else nakshatra_number - 27

def get_nakshatra_lord(nakshatra_number):
    """Get the lord of a nakshatra"""
    return NAKSHATRA_LORDS.get(nakshatra_number, "Unknown")

def is_planet_in_house(planet_name, house_number, planets):
    """Check if a planet is in a specific house"""
    if planet_name in planets:
        return planets[planet_name]['house'] == house_number
    return False

def get_planets_in_house(house_number, planets):
    """Get all planets in a specific house"""
    planets_in_house = []
    for planet, data in planets.items():
        if data['house'] == house_number:
            planets_in_house.append(planet)
    return planets_in_house

def get_planets_in_houses(house_numbers, planets):
    """Get all planets in specific houses"""
    planets_in_houses = []
    for planet, data in planets.items():
        if data['house'] in house_numbers:
            planets_in_houses.append(planet)
    return planets_in_houses

def is_planet_aspecting_house(planet_house, target_house, aspect_type="7th"):
    """Check if a planet aspects a specific house"""
    return has_aspect(planet_house, target_house, aspect_type)

def get_planets_aspecting_house(target_house, planets, aspect_type="7th"):
    """Get all planets that aspect a specific house"""
    aspecting_planets = []
    for planet, data in planets.items():
        if has_aspect(data['house'], target_house, aspect_type):
            aspecting_planets.append(planet)
    return aspecting_planets

def is_planet_strong(planet, planets):
    """Check if a planet is strong (exalted or in own sign)"""
    if planet in planets:
        strength = planets[planet].get('strength', 'Neutral')
        return strength in ['Exalted', 'Own Sign']
    return False

def is_planet_weak(planet, planets):
    """Check if a planet is weak (debilitated)"""
    if planet in planets:
        strength = planets[planet].get('strength', 'Neutral')
        return strength == 'Debilitated'
    return False

def get_planet_house(planet, planets):
    """Get the house number of a planet"""
    if planet in planets:
        return planets[planet]['house']
    return None

def get_planet_sign(planet, planets):
    """Get the sign of a planet"""
    if planet in planets:
        return planets[planet]['sign']
    return None

def calculate_sade_sati_phase(saturn_house, moon_house):
    """Calculate Sade Sati phase based on Saturn and Moon positions"""
    # Sade Sati: Saturn transiting over Moon sign or its 12th/2nd
    if saturn_house == moon_house:
        return "First Phase"  # Saturn in Moon sign
    elif saturn_house == (moon_house - 1) or saturn_house == (moon_house + 1):
        return "Second Phase"  # Saturn in 12th or 2nd from Moon
    else:
        return "No Sade Sati"

def is_kaal_sarp_yoga(planets):
    """Check if Kaal Sarp Yoga exists (all planets between Rahu and Ketu)"""
    if "Rahu (Mean)" in planets and "Ketu (Mean)" in planets:
        rahu_house = planets["Rahu (Mean)"]['house']
        ketu_house = planets["Ketu (Mean)"]['house']
        
        # Check if all planets are between Rahu and Ketu
        all_planets_between = True
        for planet, data in planets.items():
            if planet not in ["Rahu (Mean)", "Ketu (Mean)"]:
                planet_house = data['house']
                if not (min(rahu_house, ketu_house) <= planet_house <= max(rahu_house, ketu_house)):
                    all_planets_between = False
                    break
        
        return all_planets_between
    return False

def get_dosha_severity(planet, planets, dosha_type):
    """Get the severity of a dosha based on planet strength and position"""
    if planet not in planets:
        return "Mild"
    
    strength = planets[planet].get('strength', 'Neutral')
    house = planets[planet]['house']
    
    # Base severity on planet strength
    if strength == 'Exalted':
        base_severity = "Mild"
    elif strength == 'Own Sign':
        base_severity = "Moderate"
    elif strength == 'Debilitated':
        base_severity = "Severe"
    else:
        base_severity = "Moderate"
    
    # Adjust based on house position
    if dosha_type == "Mangal":
        if house in [1, 7]:  # Lagna and 7th house are most severe
            return "Severe"
        elif house in [2, 8, 12]:  # 2nd, 8th, 12th are moderate
            return "Moderate"
        else:  # 4th house is mild
            return "Mild"
    
    return base_severity 