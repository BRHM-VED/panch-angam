# Comprehensive Vedic Astrology Dosha Detection System
from dosha_utils import *
from house_utils import is_dusthana_house, is_kendra_house

def detect_all_doshas(kundli):
    """Detect all doshas in the kundli"""
    detected_doshas = []
    
    # Get kundli components
    planets = kundli.get('planets', {})
    lagna = kundli.get('lagna', {})
    bhavas = kundli.get('bhavas', [])
    input_data = kundli.get('input', {})
    
    # Get all dosha detection functions
    dosha_functions = [
        # Major Doshas
        detect_mangal_dosha, detect_kaal_sarp_dosha, detect_guru_chandal_dosha,
        detect_sade_sati, detect_pitra_dosha, detect_shrapit_dosha,
        
        # Nadi and Compatibility Doshas
        detect_nadi_dosha, detect_gana_dosha, detect_bhakoot_dosha,
        
        # Family and Ancestral Doshas
        detect_matri_dosha, detect_pitra_dosha_enhanced, detect_pret_dosha,
        detect_tara_dosha, detect_mrityu_dosha, detect_kalatra_dosha,
        
        # Planetary Doshas
        detect_saturn_dosha, detect_rahu_dosha, detect_ketu_dosha,
        detect_sun_dosha, detect_mars_dosha, detect_mercury_dosha,
        
        # House-based Doshas
        detect_8th_house_dosha, detect_12th_house_dosha, detect_6th_house_dosha,
        detect_2nd_house_dosha, detect_7th_house_dosha, detect_4th_house_dosha,
        
        # Special Doshas
        detect_sarpa_dosha, detect_grahan_dosha, detect_kemadruma_dosha,
        detect_angarak_dosha, detect_shani_dosha, detect_budh_dosha,
        
        # Modern Doshas
        detect_career_dosha, detect_health_dosha, detect_wealth_dosha,
        detect_education_dosha, detect_travel_dosha, detect_legal_dosha
    ]
    
    # Call each dosha detection function
    for dosha_func in dosha_functions:
        try:
            result = dosha_func(kundli)
            if result:
                detected_doshas.append(result)
        except Exception as e:
            print(f"Error in {dosha_func.__name__}: {e}")
            continue
    
    return detected_doshas

# Major Doshas

def detect_mangal_dosha(kundli):
    """Detect Mangal Dosha (Kuja Dosha) - Mars in specific houses relative to Lagna"""
    planets = kundli.get('planets', {})
    
    if "Mars" in planets:
        mars_house = planets["Mars"]['house']
        # Mangal Dosha houses: 1, 4, 7, 8, 12 (relative to Lagna)
        mangal_dosha_houses = [1, 4, 7, 8, 12]
        if mars_house in mangal_dosha_houses:
            severity = get_dosha_severity("Mars", planets, "Mangal")
            return {
                'name': 'Mangal Dosha (Kuja Dosha)',
                'type': 'Major Dosha',
                'description': f'Mars in {mars_house}th house from Lagna',
                'severity': severity,
                'effects': 'Marriage delays, relationship issues, anger problems',
                'remedies': 'Wear red coral, perform Mangal puja, fast on Tuesdays'
            }
    return None

def detect_kaal_sarp_dosha(kundli):
    """Detect Kaal Sarp Dosha - all planets between Rahu and Ketu"""
    planets = kundli.get('planets', {})
    
    if is_kaal_sarp_yoga(planets):
        return {
            'name': 'Kaal Sarp Dosha',
            'type': 'Major Dosha',
            'description': 'All planets between Rahu and Ketu',
            'severity': 'Severe',
            'effects': 'Obstacles in life, delays, health issues, financial problems',
            'remedies': 'Wear snake ring, perform Kaal Sarp puja, donate to temples'
        }
    return None

def detect_guru_chandal_dosha(kundli):
    """Detect Guru Chandal Dosha - Jupiter and Rahu conjunction"""
    planets = kundli.get('planets', {})
    
    if "Jupiter" in planets and "Rahu (Mean)" in planets:
        jupiter_house = planets["Jupiter"]['house']
        rahu_house = planets["Rahu (Mean)"]['house']
        
        if is_conjunct(jupiter_house, rahu_house):
            return {
                'name': 'Guru Chandal Dosha',
                'type': 'Major Dosha',
                'description': 'Jupiter and Rahu in same house',
                'severity': 'Moderate',
                'effects': 'Confusion in decisions, religious conflicts, education issues',
                'remedies': 'Wear yellow sapphire, perform Jupiter puja, study religious texts'
            }
    return None

def detect_sade_sati(kundli):
    """Detect Sade Sati - Saturn's 7.5 year period over Moon"""
    planets = kundli.get('planets', {})
    
    if "Saturn" in planets and "Moon" in planets:
        saturn_house = planets["Saturn"]['house']
        moon_house = planets["Moon"]['house']
        
        phase = calculate_sade_sati_phase(saturn_house, moon_house)
        if phase != "No Sade Sati":
            return {
                'name': 'Sade Sati',
                'type': 'Major Dosha',
                'description': f'Saturn in {phase} over Moon sign',
                'severity': 'Moderate',
                'effects': '7.5 years of challenges, health issues, career obstacles',
                'remedies': 'Wear blue sapphire, perform Saturn puja, donate black items'
            }
    return None

def detect_pitra_dosha(kundli):
    """Detect Pitra Dosha - issues related to ancestors/father"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 9th house (father's house)
    malefic_planets = ["Saturn", "Mars", "Rahu (Mean)", "Ketu (Mean)"]
    pitra_afflicted = False
    
    for planet in malefic_planets:
        if is_planet_in_house(planet, 9, planets):
            pitra_afflicted = True
            break
    
    if pitra_afflicted:
        return {
            'name': 'Pitra Dosha',
            'type': 'Ancestral Dosha',
            'description': 'Malefic planets in 9th house (father\'s house)',
            'severity': 'Moderate',
            'effects': 'Ancestral curses, father-related issues, property disputes',
            'remedies': 'Perform Pitra puja, donate to Brahmins, visit holy places'
        }
    return None

def detect_shrapit_dosha(kundli):
    """Detect Shrapit Dosha - cursed by someone"""
    planets = kundli.get('planets', {})
    
    # Check for Rahu in 6th, 8th, or 12th houses
    if "Rahu (Mean)" in planets:
        rahu_house = planets["Rahu (Mean)"]['house']
        if rahu_house in [6, 8, 12]:
            return {
                'name': 'Shrapit Dosha',
                'type': 'Curse Dosha',
                'description': f'Rahu in {rahu_house}th house (house of enemies/death)',
                'severity': 'Severe',
                'effects': 'Curses, black magic effects, enemies, legal issues',
                'remedies': 'Perform Rahu puja, wear hessonite garnet, visit temples'
            }
    return None

# Nadi and Compatibility Doshas

def detect_nadi_dosha(kundli):
    """Detect Nadi Dosha - nakshatra compatibility issue"""
    planets = kundli.get('planets', {})
    
    if "Moon" in planets:
        moon_data = planets["Moon"]
        moon_house = moon_data['house']
        
        # Calculate nakshatra from moon position (simplified)
        # In real implementation, you'd need actual nakshatra data
        nakshatra_lord = get_nakshatra_lord(1)  # Simplified
        
        if nakshatra_lord in ["Rahu", "Ketu"]:
            return {
                'name': 'Nadi Dosha',
                'type': 'Compatibility Dosha',
                'description': 'Moon in problematic nakshatra',
                'severity': 'Moderate',
                'effects': 'Marriage compatibility issues, health problems',
                'remedies': 'Perform nakshatra puja, wear appropriate gemstones'
            }
    return None

def detect_gana_dosha(kundli):
    """Detect Gana Dosha - temperament compatibility issue"""
    planets = kundli.get('planets', {})
    
    # Simplified gana calculation based on moon sign
    if "Moon" in planets:
        moon_house = planets["Moon"]['house']
        
        # Dev gana: 1, 5, 9 (Aries, Leo, Sagittarius)
        # Manushya gana: 2, 6, 10 (Taurus, Virgo, Capricorn)
        # Rakshasa gana: 3, 7, 11 (Gemini, Libra, Aquarius)
        # Pisces is special
        
        if moon_house in [3, 7, 11]:  # Rakshasa gana
            return {
                'name': 'Gana Dosha',
                'type': 'Compatibility Dosha',
                'description': 'Moon in Rakshasa gana (aggressive temperament)',
                'severity': 'Mild',
                'effects': 'Temperament conflicts, relationship issues',
                'remedies': 'Practice meditation, perform moon puja'
            }
    return None

def detect_bhakoot_dosha(kundli):
    """Detect Bhakoot Dosha - moon sign compatibility issue"""
    planets = kundli.get('planets', {})
    
    if "Moon" in planets:
        moon_house = planets["Moon"]['house']
        
        # Bhakoot dosha: incompatible moon signs
        # 1-7, 2-8, 3-9, 4-10, 5-11, 6-12 are incompatible
        incompatible_signs = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        
        if moon_house in [1, 2, 3, 4, 5, 6]:
            incompatible = incompatible_signs[moon_house - 1]
            return {
                'name': 'Bhakoot Dosha',
                'type': 'Compatibility Dosha',
                'description': f'Moon in {moon_house} incompatible with {incompatible}',
                'severity': 'Moderate',
                'effects': 'Marriage compatibility issues, relationship problems',
                'remedies': 'Perform compatibility puja, wear moon stone'
            }
    return None

# Family and Ancestral Doshas

def detect_matri_dosha(kundli):
    """Detect Matri Dosha - mother-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 4th house (mother's house)
    malefic_planets = ["Saturn", "Mars", "Rahu (Mean)", "Ketu (Mean)"]
    matri_afflicted = False
    
    for planet in malefic_planets:
        if is_planet_in_house(planet, 4, planets):
            matri_afflicted = True
            break
    
    if matri_afflicted:
        return {
            'name': 'Matri Dosha',
            'type': 'Family Dosha',
            'description': 'Malefic planets in 4th house (mother\'s house)',
            'severity': 'Moderate',
            'effects': 'Mother-related issues, property problems, emotional instability',
            'remedies': 'Perform mother puja, donate to women, visit mother\'s temple'
        }
    return None

def detect_pitra_dosha_enhanced(kundli):
    """Enhanced Pitra Dosha detection with multiple factors"""
    planets = kundli.get('planets', {})
    
    # Check multiple factors for Pitra dosha
    factors = []
    
    # 1. Malefic in 9th house
    if get_planets_in_houses([9], planets):
        factors.append("Malefic in 9th house")
    
    # 2. Sun debilitated or weak
    if "Sun" in planets and is_planet_weak("Sun", planets):
        factors.append("Weak Sun")
    
    # 3. Saturn aspecting 9th house
    if "Saturn" in planets:
        saturn_house = planets["Saturn"]['house']
        if has_aspect(saturn_house, 9, "7th"):
            factors.append("Saturn aspects 9th house")
    
    if factors:
        return {
            'name': 'Enhanced Pitra Dosha',
            'type': 'Ancestral Dosha',
            'description': f'Multiple factors: {", ".join(factors)}',
            'severity': 'Severe' if len(factors) > 2 else 'Moderate',
            'effects': 'Ancestral curses, father issues, property disputes, legal problems',
            'remedies': 'Perform Pitra puja, donate to Brahmins, visit holy places, wear ruby'
        }
    return None

def detect_pret_dosha(kundli):
    """Detect Pret Dosha - ghost/spirit related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 8th and 12th houses
    malefic_planets = ["Saturn", "Mars", "Rahu (Mean)", "Ketu (Mean)"]
    pret_afflicted = False
    
    for planet in malefic_planets:
        if is_planet_in_house(planet, 8, planets) or is_planet_in_house(planet, 12, planets):
            pret_afflicted = True
            break
    
    if pret_afflicted:
        return {
            'name': 'Pret Dosha',
            'type': 'Spiritual Dosha',
            'description': 'Malefic planets in 8th/12th houses (death/ghost houses)',
            'severity': 'Severe',
            'effects': 'Spirit possession, nightmares, fear, mental health issues',
            'remedies': 'Perform Pret puja, visit temples, wear protective gemstones'
        }
    return None

def detect_tara_dosha(kundli):
    """Detect Tara Dosha - star-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 6th, 8th, 12th houses
    if get_planets_in_houses([6, 8, 12], planets):
        return {
            'name': 'Tara Dosha',
            'type': 'Star Dosha',
            'description': 'Malefic planets in 6th, 8th, or 12th houses',
            'severity': 'Moderate',
            'effects': 'Health issues, enemies, obstacles, delays',
            'remedies': 'Perform Tara puja, wear appropriate gemstones, visit temples'
        }
    return None

def detect_mrityu_dosha(kundli):
    """Detect Mrityu Dosha - death-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 8th house (house of death)
    if get_planets_in_houses([8], planets):
        return {
            'name': 'Mrityu Dosha',
            'type': 'Death Dosha',
            'description': 'Malefic planets in 8th house (house of death)',
            'severity': 'Severe',
            'effects': 'Health issues, accidents, life-threatening situations',
            'remedies': 'Perform Mrityu puja, wear protective gemstones, visit temples'
        }
    return None

def detect_kalatra_dosha(kundli):
    """Detect Kalatra Dosha - spouse-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 7th house (spouse's house)
    malefic_planets = ["Saturn", "Mars", "Rahu (Mean)", "Ketu (Mean)"]
    kalatra_afflicted = False
    
    for planet in malefic_planets:
        if is_planet_in_house(planet, 7, planets):
            kalatra_afflicted = True
            break
    
    if kalatra_afflicted:
        return {
            'name': 'Kalatra Dosha',
            'type': 'Marriage Dosha',
            'description': 'Malefic planets in 7th house (spouse\'s house)',
            'severity': 'Moderate',
            'effects': 'Marriage problems, spouse issues, relationship conflicts',
            'remedies': 'Perform marriage puja, wear diamond, visit Venus temple'
        }
    return None

# Planetary Doshas

def detect_saturn_dosha(kundli):
    """Detect Saturn Dosha - Saturn-related issues"""
    planets = kundli.get('planets', {})
    
    if "Saturn" in planets:
        saturn_data = planets["Saturn"]
        saturn_house = saturn_data['house']
        saturn_strength = saturn_data.get('strength', 'Neutral')
        
        # Saturn in difficult houses or weak
        if saturn_house in [1, 2, 4, 7, 8, 12] or saturn_strength == 'Debilitated':
            severity = 'Severe' if saturn_house in [1, 7, 8] else 'Moderate'
            return {
                'name': 'Saturn Dosha',
                'type': 'Planetary Dosha',
                'description': f'Saturn in {saturn_house}th house ({saturn_strength})',
                'severity': severity,
                'effects': 'Delays, obstacles, health issues, career problems',
                'remedies': 'Wear blue sapphire, perform Saturn puja, donate black items'
            }
    return None

def detect_rahu_dosha(kundli):
    """Detect Rahu Dosha - Rahu-related issues"""
    planets = kundli.get('planets', {})
    
    if "Rahu (Mean)" in planets:
        rahu_house = planets["Rahu (Mean)"]['house']
        
        # Rahu in difficult houses
        if rahu_house in [1, 2, 4, 7, 8, 9, 12]:
            return {
                'name': 'Rahu Dosha',
                'type': 'Planetary Dosha',
                'description': f'Rahu in {rahu_house}th house',
                'severity': 'Severe' if rahu_house in [1, 7, 8] else 'Moderate',
                'effects': 'Confusion, illusions, foreign issues, mental problems',
                'remedies': 'Wear hessonite garnet, perform Rahu puja, visit temples'
            }
    return None

def detect_ketu_dosha(kundli):
    """Detect Ketu Dosha - Ketu-related issues"""
    planets = kundli.get('planets', {})
    
    if "Ketu (Mean)" in planets:
        ketu_house = planets["Ketu (Mean)"]['house']
        
        # Ketu in difficult houses
        if ketu_house in [1, 2, 4, 7, 8, 9, 12]:
            return {
                'name': 'Ketu Dosha',
                'type': 'Planetary Dosha',
                'description': f'Ketu in {ketu_house}th house',
                'severity': 'Severe' if ketu_house in [1, 7, 8] else 'Moderate',
                'effects': 'Detachment, confusion, spiritual issues, health problems',
                'remedies': 'Wear cat\'s eye, perform Ketu puja, practice meditation'
            }
    return None

def detect_sun_dosha(kundli):
    """Detect Sun Dosha - Sun-related issues"""
    planets = kundli.get('planets', {})
    
    if "Sun" in planets:
        sun_data = planets["Sun"]
        sun_house = sun_data['house']
        sun_strength = sun_data.get('strength', 'Neutral')
        
        # Sun in difficult houses or weak
        if sun_house in [6, 8, 12] or sun_strength == 'Debilitated':
            return {
                'name': 'Sun Dosha',
                'type': 'Planetary Dosha',
                'description': f'Sun in {sun_house}th house ({sun_strength})',
                'severity': 'Moderate',
                'effects': 'Father issues, authority problems, eye problems',
                'remedies': 'Wear ruby, perform Sun puja, donate red items'
            }
    return None

def detect_mars_dosha(kundli):
    """Detect Mars Dosha - Mars-related issues"""
    planets = kundli.get('planets', {})
    
    if "Mars" in planets:
        mars_data = planets["Mars"]
        mars_house = mars_data['house']
        mars_strength = mars_data.get('strength', 'Neutral')
        
        # Mars in difficult houses or weak
        if mars_house in [4, 6, 8, 12] or mars_strength == 'Debilitated':
            return {
                'name': 'Mars Dosha',
                'type': 'Planetary Dosha',
                'description': f'Mars in {mars_house}th house ({mars_strength})',
                'severity': 'Moderate',
                'effects': 'Anger issues, blood problems, accidents, conflicts',
                'remedies': 'Wear red coral, perform Mars puja, donate red items'
            }
    return None

def detect_mercury_dosha(kundli):
    """Detect Mercury Dosha - Mercury-related issues"""
    planets = kundli.get('planets', {})
    
    if "Mercury" in planets:
        mercury_data = planets["Mercury"]
        mercury_house = mercury_data['house']
        mercury_strength = mercury_data.get('strength', 'Neutral')
        
        # Mercury in difficult houses or weak
        if mercury_house in [6, 8, 12] or mercury_strength == 'Debilitated':
            return {
                'name': 'Mercury Dosha',
                'type': 'Planetary Dosha',
                'description': f'Mercury in {mercury_house}th house ({mercury_strength})',
                'severity': 'Moderate',
                'effects': 'Communication issues, nervous problems, skin issues',
                'remedies': 'Wear emerald, perform Mercury puja, donate green items'
            }
    return None

# House-based Doshas

def detect_8th_house_dosha(kundli):
    """Detect 8th House Dosha - death and obstacles"""
    planets = kundli.get('planets', {})
    
    if get_planets_in_houses([8], planets):
        return {
            'name': '8th House Dosha',
            'type': 'House Dosha',
            'description': 'Planets in 8th house (house of death and obstacles)',
            'severity': 'Severe',
            'effects': 'Health issues, accidents, obstacles, delays',
            'remedies': 'Perform 8th house puja, wear protective gemstones'
        }
    return None

def detect_12th_house_dosha(kundli):
    """Detect 12th House Dosha - losses and expenses"""
    planets = kundli.get('planets', {})
    
    if get_planets_in_houses([12], planets):
        return {
            'name': '12th House Dosha',
            'type': 'House Dosha',
            'description': 'Planets in 12th house (house of losses)',
            'severity': 'Moderate',
            'effects': 'Financial losses, expenses, foreign issues',
            'remedies': 'Perform 12th house puja, donate to charity'
        }
    return None

def detect_6th_house_dosha(kundli):
    """Detect 6th House Dosha - enemies and diseases"""
    planets = kundli.get('planets', {})
    
    if get_planets_in_houses([6], planets):
        return {
            'name': '6th House Dosha',
            'type': 'House Dosha',
            'description': 'Planets in 6th house (house of enemies)',
            'severity': 'Moderate',
            'effects': 'Enemies, health issues, legal problems',
            'remedies': 'Perform 6th house puja, wear protective gemstones'
        }
    return None

# Special Doshas

def detect_sarpa_dosha(kundli):
    """Detect Sarpa Dosha - snake-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for Rahu and Ketu in difficult positions
    if "Rahu (Mean)" in planets and "Ketu (Mean)" in planets:
        rahu_house = planets["Rahu (Mean)"]['house']
        ketu_house = planets["Ketu (Mean)"]['house']
        
        if rahu_house in [1, 4, 7, 8, 12] or ketu_house in [1, 4, 7, 8, 12]:
            return {
                'name': 'Sarpa Dosha',
                'type': 'Special Dosha',
                'description': 'Rahu/Ketu in difficult houses',
                'severity': 'Moderate',
                'effects': 'Snake-related fears, illusions, confusion',
                'remedies': 'Perform Sarpa puja, wear snake ring, visit temples'
            }
    return None

def detect_grahan_dosha(kundli):
    """Detect Grahan Dosha - eclipse-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for Sun-Moon conjunction with Rahu/Ketu
    if "Sun" in planets and "Moon" in planets and "Rahu (Mean)" in planets:
        sun_house = planets["Sun"]['house']
        moon_house = planets["Moon"]['house']
        rahu_house = planets["Rahu (Mean)"]['house']
        
        if is_conjunct(sun_house, moon_house) and (is_conjunct(sun_house, rahu_house) or has_aspect(sun_house, rahu_house, "7th")):
            return {
                'name': 'Grahan Dosha',
                'type': 'Special Dosha',
                'description': 'Sun-Moon conjunction with Rahu (eclipse)',
                'severity': 'Severe',
                'effects': 'Eclipse effects, confusion, health issues',
                'remedies': 'Perform Grahan puja, wear protective gemstones'
            }
    return None

def detect_kemadruma_dosha(kundli):
    """Detect Kemadruma Dosha - Moon without adjacent planets"""
    planets = kundli.get('planets', {})
    
    if "Moon" in planets:
        moon_house = planets["Moon"]['house']
        adjacent_houses = [moon_house - 1, moon_house + 1]
        adjacent_houses = [h if h > 0 else 12 for h in adjacent_houses]
        adjacent_houses = [h if h <= 12 else h - 12 for h in adjacent_houses]
        
        has_adjacent_planets = False
        for planet, data in planets.items():
            if planet != "Moon" and data['house'] in adjacent_houses:
                has_adjacent_planets = True
                break
        
        if not has_adjacent_planets:
            return {
                'name': 'Kemadruma Dosha',
                'type': 'Special Dosha',
                'description': 'Moon without planets in adjacent houses',
                'severity': 'Moderate',
                'effects': 'Mental instability, emotional issues, loneliness',
                'remedies': 'Perform Moon puja, wear pearl, practice meditation'
            }
    return None

# Modern Doshas

def detect_career_dosha(kundli):
    """Detect Career Dosha - career-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 10th house (career house)
    malefic_planets = ["Saturn", "Mars", "Rahu (Mean)", "Ketu (Mean)"]
    
    for planet in malefic_planets:
        if is_planet_in_house(planet, 10, planets):
            return {
                'name': 'Career Dosha',
                'type': 'Modern Dosha',
                'description': f'{planet} in 10th house (career house)',
                'severity': 'Moderate',
                'effects': 'Career obstacles, job issues, professional problems',
                'remedies': 'Perform career puja, wear appropriate gemstones'
            }
    return None

def detect_health_dosha(kundli):
    """Detect Health Dosha - health-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 6th and 8th houses (health houses)
    if get_planets_in_houses([6, 8], planets):
        return {
            'name': 'Health Dosha',
            'type': 'Modern Dosha',
            'description': 'Malefic planets in health houses (6th/8th)',
            'severity': 'Moderate',
            'effects': 'Health issues, diseases, medical problems',
            'remedies': 'Perform health puja, wear protective gemstones, exercise'
        }
    return None

def detect_wealth_dosha(kundli):
    """Detect Wealth Dosha - wealth-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 2nd and 11th houses (wealth houses)
    if get_planets_in_houses([2, 11], planets):
        return {
            'name': 'Wealth Dosha',
            'type': 'Modern Dosha',
            'description': 'Malefic planets in wealth houses (2nd/11th)',
            'severity': 'Moderate',
            'effects': 'Financial problems, wealth issues, money problems',
            'remedies': 'Perform wealth puja, wear yellow sapphire, donate to charity'
        }
    return None

def detect_education_dosha(kundli):
    """Detect Education Dosha - education-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 4th and 5th houses (education houses)
    if get_planets_in_houses([4, 5], planets):
        return {
            'name': 'Education Dosha',
            'type': 'Modern Dosha',
            'description': 'Malefic planets in education houses (4th/5th)',
            'severity': 'Moderate',
            'effects': 'Education problems, learning difficulties, academic issues',
            'remedies': 'Perform education puja, wear emerald, study regularly'
        }
    return None

def detect_travel_dosha(kundli):
    """Detect Travel Dosha - travel-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 12th house (foreign travel house)
    if get_planets_in_houses([12], planets):
        return {
            'name': 'Travel Dosha',
            'type': 'Modern Dosha',
            'description': 'Malefic planets in 12th house (travel house)',
            'severity': 'Mild',
            'effects': 'Travel problems, foreign issues, immigration problems',
            'remedies': 'Perform travel puja, wear appropriate gemstones'
        }
    return None

def detect_legal_dosha(kundli):
    """Detect Legal Dosha - legal-related issues"""
    planets = kundli.get('planets', {})
    
    # Check for malefic planets in 6th house (legal house)
    if get_planets_in_houses([6], planets):
        return {
            'name': 'Legal Dosha',
            'type': 'Modern Dosha',
            'description': 'Malefic planets in 6th house (legal house)',
            'severity': 'Moderate',
            'effects': 'Legal problems, court cases, disputes',
            'remedies': 'Perform legal puja, wear protective gemstones, consult lawyers'
        }
    return None

# Placeholder functions for additional doshas
def detect_angarak_dosha(kundli): return None
def detect_shani_dosha(kundli): return None
def detect_budh_dosha(kundli): return None
def detect_2nd_house_dosha(kundli): return None
def detect_7th_house_dosha(kundli): return None
def detect_4th_house_dosha(kundli): return None 