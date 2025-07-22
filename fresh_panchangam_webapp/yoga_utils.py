# Yoga detection utilities for Vedic astrology

# Sign lords (rashi lords)
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
    "Ketu": 9      # Sagittarius
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
    "Ketu": 3      # Gemini
}

# Friendly and enemy planets
FRIENDLY_PLANETS = {
    "Sun": ["Mars", "Jupiter"],
    "Moon": ["Mercury", "Venus"],
    "Mars": ["Sun", "Jupiter"],
    "Mercury": ["Venus", "Saturn"],
    "Jupiter": ["Sun", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu (Mean)": ["Venus", "Saturn"],
    "Ketu": ["Mars", "Jupiter"]
}

ENEMY_PLANETS = {
    "Sun": ["Venus", "Saturn"],
    "Moon": ["Mars", "Saturn"],
    "Mars": ["Mercury", "Venus"],
    "Mercury": ["Sun", "Mars"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Mars"],
    "Saturn": ["Sun", "Moon"],
    "Rahu (Mean)": ["Sun", "Moon"],
    "Ketu": ["Mercury", "Venus"]
}

def get_sign_lord(sign_number):
    """Get the lord of a zodiac sign"""
    return SIGN_LORDS.get(sign_number, "Unknown")

def is_exalted(planet, sign_number):
    """Check if a planet is exalted in a sign"""
    return EXALTATION_SIGNS.get(planet) == sign_number

def is_debilitated(planet, sign_number):
    """Check if a planet is debilitated in a sign"""
    return DEBILITATION_SIGNS.get(planet) == sign_number

def is_friendly(planet1, planet2):
    """Check if two planets are friendly"""
    return planet2 in FRIENDLY_PLANETS.get(planet1, [])

def is_enemy(planet1, planet2):
    """Check if two planets are enemies"""
    return planet2 in ENEMY_PLANETS.get(planet1, [])

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

def get_aspects(planet1_house, planet2_house):
    """Get aspects between houses (simplified)"""
    # 7th aspect (opposite)
    if abs(planet1_house - planet2_house) == 6:
        return ["7th"]
    # 4th and 8th aspects
    elif abs(planet1_house - planet2_house) == 3:
        return ["4th", "8th"]
    # 5th and 9th aspects
    elif abs(planet1_house - planet2_house) == 4:
        return ["5th", "9th"]
    # 3rd and 10th aspects
    elif abs(planet1_house - planet2_house) == 2:
        return ["3rd", "10th"]
    else:
        return []

def get_planet_aspects(planet1_house, planet2_house):
    """Get detailed aspects between planets based on Vedic astrology rules"""
    aspects = []
    
    # Calculate house difference
    diff = abs(planet1_house - planet2_house)
    
    # Special aspects for different planets
    if diff == 6:  # 7th aspect (opposite)
        aspects.append("7th")
    elif diff == 3:  # 4th aspect
        aspects.append("4th")
    elif diff == 9:  # 10th aspect
        aspects.append("10th")
    elif diff == 4:  # 5th aspect
        aspects.append("5th")
    elif diff == 8:  # 9th aspect
        aspects.append("9th")
    elif diff == 2:  # 3rd aspect
        aspects.append("3rd")
    elif diff == 10:  # 11th aspect
        aspects.append("11th")
    
    return aspects

def has_aspect(planet1_house, planet2_house, aspect_type="7th"):
    """Check if two planets have a specific aspect"""
    aspects = get_planet_aspects(planet1_house, planet2_house)
    return aspect_type in aspects

def get_full_aspect(planet1_house, planet2_house):
    """Get full aspect relationship between planets"""
    aspects = get_planet_aspects(planet1_house, planet2_house)
    if aspects:
        return aspects[0]  # Return the strongest aspect
    return None

def is_conjunct(planet1_house, planet2_house):
    """Check if planets are in the same house"""
    return planet1_house == planet2_house

def is_opposite(planet1_house, planet2_house):
    """Check if planets are in opposite houses (7th aspect)"""
    return abs(planet1_house - planet2_house) == 6

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