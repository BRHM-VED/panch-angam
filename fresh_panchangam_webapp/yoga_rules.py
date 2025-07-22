# Comprehensive Vedic Astrology Yoga Detection System
from yoga_utils import *

def detect_all_yogas(planets, bhavas, lagna, time_info=None):
    """Detect all yogas in the kundli"""
    detected_yogas = []
    
    # Get all yoga detection functions
    yoga_functions = [
        # Raj Yogas (Royal Combinations)
        detect_raja_yoga, detect_mahapurusha_yoga, detect_parivartana_yoga,
        detect_vasumati_yoga, detect_kesari_yoga, detect_sankha_yoga,
        detect_brahma_yoga, detect_indra_yoga, detect_mahendra_yoga,
        
        # Dhan Yogas (Wealth Combinations)
        detect_dhana_yoga, detect_lakshmi_yoga, detect_kubera_yoga,
        detect_rajalakshmi_yoga, detect_vasumati_yoga, detect_akhand_samrajya_yoga,
        
        # Education and Knowledge Yogas
        detect_vidya_yoga, detect_saraswati_yoga, detect_budh_aditya_yoga,
        detect_guru_chandal_yoga, detect_brahma_yoga, detect_sankha_yoga,
        
        # Health and Longevity Yogas
        detect_ayushkar_yoga, detect_amrit_yoga, detect_sarala_yoga,
        detect_vyaghata_yoga, detect_paridhi_yoga, detect_sankata_yoga,
        
        # Marriage and Relationships
        detect_vivah_yoga, detect_kalatra_yoga, detect_mangal_yoga,
        detect_saubhagya_yoga, detect_putra_yoga, detect_santan_yoga,
        
        # Career and Profession
        detect_karma_yoga, detect_dharma_yoga,
        detect_artha_yoga, detect_kama_yoga, detect_moksha_yoga,
        
        # Travel and Foreign
        detect_paradesh_yoga, detect_videsh_yoga, detect_yatra_yoga,
        detect_foreign_yoga, detect_immigration_yoga,
        
        # Spiritual and Religious
        detect_sanyas_yoga, detect_tapasvi_yoga, detect_moksha_yoga,
        detect_dharma_yoga, detect_bhakti_yoga, detect_gyan_yoga,
        
        # Special Combinations
        detect_panch_mahapurush_yoga, detect_nabhas_yoga, detect_nala_yoga,
        detect_nala_raj_yoga, detect_nala_mahendra_yoga, detect_nala_brahma_yoga,
        detect_nala_indra_yoga, detect_nala_mahendra_yoga, detect_nala_kesari_yoga,
        detect_nala_sankha_yoga, detect_nala_vasumati_yoga, detect_nala_kubera_yoga,
        
        # Dosha Yogas (Afflictions)
        detect_kaal_sarp_yoga, detect_mangal_dosha, detect_rahu_dosha,
        detect_ketu_dosha, detect_saturn_dosha, detect_sun_dosha,
        
        # Nakshatra Yogas
        detect_gand_mool_yoga, detect_nakshatra_yoga, detect_janma_nakshatra_yoga,
        
        # Tithi Yogas
        detect_amavasya_yoga, detect_purnima_yoga, detect_ekadashi_yoga,
        detect_sankranti_yoga, detect_solar_eclipse_yoga, detect_lunar_eclipse_yoga,
        
        # House Specific Yogas
        detect_first_house_yoga, detect_second_house_yoga, detect_third_house_yoga,
        detect_fourth_house_yoga, detect_fifth_house_yoga, detect_sixth_house_yoga,
        detect_seventh_house_yoga, detect_eighth_house_yoga, detect_ninth_house_yoga,
        detect_tenth_house_yoga, detect_eleventh_house_yoga, detect_twelfth_house_yoga,
        
        # Planetary Combinations
        detect_sun_moon_yoga, detect_sun_mars_yoga, detect_sun_jupiter_yoga,
        detect_moon_venus_yoga, detect_moon_mercury_yoga, detect_mars_jupiter_yoga,
        detect_venus_jupiter_yoga, detect_mercury_venus_yoga, detect_saturn_venus_yoga,
        detect_rahu_ketu_yoga, detect_rahu_saturn_yoga, detect_ketu_mars_yoga,
        
        # Special Yogas
        detect_akhand_samrajya_yoga, detect_sarvatobhadra_yoga, detect_sarvartha_siddhi_yoga,
        detect_rajyoga_bhanga, detect_dhanayoga_bhanga, detect_vidyayoga_bhanga,
        detect_ayushyoga_bhanga, detect_putrayoga_bhanga, detect_kalatra_yoga_bhanga,
        
        # Modern Yogas
        detect_foreign_education_yoga, detect_foreign_marriage_yoga, detect_foreign_career_yoga,
        detect_technology_yoga, detect_media_yoga, detect_sports_yoga,
        detect_arts_yoga, detect_music_yoga, detect_writing_yoga,
        detect_research_yoga, detect_medicine_yoga, detect_law_yoga,
        detect_business_yoga, detect_politics_yoga, detect_administration_yoga,
        
        # Timing Yogas
        detect_dasha_yoga, detect_antardasha_yoga, detect_pratyantar_yoga,
        detect_sookshma_yoga, detect_prana_yoga, detect_deha_yoga,
        
        # Remedial Yogas
        detect_gem_yoga, detect_mantra_yoga, detect_yantra_yoga,
        detect_tantra_yoga, detect_puja_yoga, detect_donation_yoga,
        detect_fasting_yoga, detect_meditation_yoga, detect_yoga_yoga,
        
        # Combination Yogas
        detect_benefic_combination_yoga, detect_malefic_combination_yoga,
        detect_neutral_combination_yoga, detect_mixed_combination_yoga,
        
        # Strength Yogas
        detect_exalted_combination_yoga, detect_debilitated_combination_yoga,
        detect_own_sign_combination_yoga, detect_friendly_sign_combination_yoga,
        detect_enemy_sign_combination_yoga, detect_neutral_sign_combination_yoga,
        
        # Enhanced Yogas with Aspect and Strength
        detect_shankh_yoga, detect_parvat_yoga, detect_grahan_yoga,
        detect_chandal_yoga, detect_kemadruma_yoga, detect_gajakesari_yoga,
        detect_budh_aditya_enhanced_yoga, detect_amrit_siddhi_yoga,
        detect_parijat_yoga, detect_vasumati_enhanced_yoga,
        detect_rajalakshmi_enhanced_yoga, detect_akhand_samrajya_enhanced_yoga
    ]
    
    # Call each yoga detection function
    for yoga_func in yoga_functions:
        try:
            result = yoga_func(planets, bhavas, lagna, time_info)
            if result:
                detected_yogas.append(result)
        except Exception as e:
            print(f"Error in {yoga_func.__name__}: {e}")
            continue
    
    return detected_yogas

# Raj Yogas (Royal Combinations)
def detect_raja_yoga(planets, bhavas, lagna):
    """Detect Raja Yoga - combination of benefic planets in kendras"""
    kendras = [1, 4, 7, 10]  # Angular houses
    benefics = ["Jupiter", "Venus", "Mercury"]
    
    for kendra in kendras:
        for planet in benefics:
            if planet in planets and planets[planet]['house'] == kendra:
                return {
                    'name': 'Raja Yoga',
                    'type': 'Raj Yoga',
                    'description': f'{planet} in {kendra}th house (Kendra)',
                    'strength': 'Strong'
                }
    return None

def detect_mahapurusha_yoga(planets, bhavas, lagna):
    """Detect Mahapurusha Yoga - exalted planets in kendras"""
    kendras = [1, 4, 7, 10]
    
    for planet, data in planets.items():
        if data['house'] in kendras and is_exalted(planet, data['house']):
            return {
                'name': f'{planet} Mahapurusha Yoga',
                'type': 'Raj Yoga',
                'description': f'{planet} exalted in {data["house"]}th house',
                'strength': 'Very Strong'
            }
    return None

def detect_parivartana_yoga(planets, bhavas, lagna):
    """Detect Parivartana Yoga - exchange of signs between planets"""
    for planet1, data1 in planets.items():
        for planet2, data2 in planets.items():
            if planet1 != planet2:
                lord1 = get_sign_lord(data1['house'])
                lord2 = get_sign_lord(data2['house'])
                if lord1 == planet2 and lord2 == planet1:
                    return {
                        'name': f'{planet1}-{planet2} Parivartana Yoga',
                        'type': 'Raj Yoga',
                        'description': f'Exchange between {planet1} and {planet2}',
                        'strength': 'Strong'
                    }
    return None

# Dhan Yogas (Wealth Combinations)
def detect_dhana_yoga(planets, bhavas, lagna):
    """Detect Dhana Yoga - wealth combinations"""
    # Jupiter or Venus in 2nd, 5th, 9th, or 11th house
    wealth_houses = [2, 5, 9, 11]
    wealth_planets = ["Jupiter", "Venus"]
    
    for planet in wealth_planets:
        if planet in planets and planets[planet]['house'] in wealth_houses:
            return {
                'name': f'{planet} Dhana Yoga',
                'type': 'Dhan Yoga',
                'description': f'{planet} in {planets[planet]["house"]}th house',
                'strength': 'Strong'
            }
    return None

def detect_lakshmi_yoga(planets, bhavas, lagna):
    """Detect Lakshmi Yoga - Venus in specific houses"""
    if "Venus" in planets:
        venus_house = planets["Venus"]['house']
        if venus_house in [2, 4, 7, 9, 11]:
            return {
                'name': 'Lakshmi Yoga',
                'type': 'Dhan Yoga',
                'description': f'Venus in {venus_house}th house',
                'strength': 'Strong'
            }
    return None

# Education and Knowledge Yogas
def detect_vidya_yoga(planets, bhavas, lagna):
    """Detect Vidya Yoga - education combinations"""
    # Mercury or Jupiter in 4th, 5th, or 9th house
    education_houses = [4, 5, 9]
    education_planets = ["Mercury", "Jupiter"]
    
    for planet in education_planets:
        if planet in planets and planets[planet]['house'] in education_houses:
            return {
                'name': f'{planet} Vidya Yoga',
                'type': 'Vidya Yoga',
                'description': f'{planet} in {planets[planet]["house"]}th house',
                'strength': 'Strong'
            }
    return None

def detect_saraswati_yoga(planets, bhavas, lagna):
    """Detect Saraswati Yoga - Mercury in specific houses"""
    if "Mercury" in planets:
        mercury_house = planets["Mercury"]['house']
        if mercury_house in [4, 5, 9] and is_exalted("Mercury", mercury_house):
            return {
                'name': 'Saraswati Yoga',
                'type': 'Vidya Yoga',
                'description': f'Exalted Mercury in {mercury_house}th house',
                'strength': 'Very Strong'
            }
    return None

# Health and Longevity Yogas
def detect_ayushkar_yoga(planets, bhavas, lagna):
    """Detect Ayushkar Yoga - longevity combinations"""
    # Jupiter in 8th house or strong 8th lord
    if "Jupiter" in planets and planets["Jupiter"]['house'] == 8:
        return {
            'name': 'Jupiter Ayushkar Yoga',
            'type': 'Ayush Yoga',
            'description': 'Jupiter in 8th house',
            'strength': 'Strong'
        }
    return None

def detect_amrit_yoga(planets, bhavas, lagna):
    """Detect Amrit Yoga - Moon in specific houses"""
    if "Moon" in planets:
        moon_house = planets["Moon"]['house']
        if moon_house in [1, 4, 7, 10] and is_exalted("Moon", moon_house):
            return {
                'name': 'Amrit Yoga',
                'type': 'Ayush Yoga',
                'description': f'Exalted Moon in {moon_house}th house',
                'strength': 'Very Strong'
            }
    return None

# Marriage and Relationships
def detect_vivah_yoga(planets, bhavas, lagna):
    """Detect Vivah Yoga - marriage combinations"""
    # Venus in 7th house or 7th lord strong
    if "Venus" in planets and planets["Venus"]['house'] == 7:
        return {
            'name': 'Vivah Yoga',
            'type': 'Vivah Yoga',
            'description': 'Venus in 7th house',
            'strength': 'Strong'
        }
    return None

def detect_kalatra_yoga(planets, bhavas, lagna):
    """Detect Kalatra Yoga - spouse combinations"""
    # 7th lord in 7th house or Venus in 7th
    seventh_lord = get_sign_lord(bhavas[6]['house'])  # 7th house (index 6)
    if seventh_lord in planets and planets[seventh_lord]['house'] == 7:
        return {
            'name': 'Kalatra Yoga',
            'type': 'Vivah Yoga',
            'description': f'{seventh_lord} (7th lord) in 7th house',
            'strength': 'Strong'
        }
    return None

# Career and Profession
def detect_karma_yoga(planets, bhavas, lagna):
    """Detect Karma Yoga - career combinations"""
    # 10th lord in 10th house or strong 10th house
    tenth_lord = get_sign_lord(bhavas[9]['house'])  # 10th house (index 9)
    if tenth_lord in planets and planets[tenth_lord]['house'] == 10:
        return {
            'name': 'Karma Yoga',
            'type': 'Karma Yoga',
            'description': f'{tenth_lord} (10th lord) in 10th house',
            'strength': 'Strong'
        }
    return None

# Travel and Foreign
def detect_paradesh_yoga(planets, bhavas, lagna):
    """Detect Paradesh Yoga - foreign travel"""
    # 12th lord in 12th house or Rahu in 12th
    if "Rahu (Mean)" in planets and planets["Rahu (Mean)"]['house'] == 12:
        return {
            'name': 'Paradesh Yoga',
            'type': 'Foreign Yoga',
            'description': 'Rahu in 12th house',
            'strength': 'Strong'
        }
    return None

# Spiritual and Religious
def detect_sanyas_yoga(planets, bhavas, lagna):
    """Detect Sanyas Yoga - spiritual life"""
    # Saturn in 12th house or Ketu in 12th
    if "Saturn" in planets and planets["Saturn"]['house'] == 12:
        return {
            'name': 'Sanyas Yoga',
            'type': 'Spiritual Yoga',
            'description': 'Saturn in 12th house',
            'strength': 'Strong'
        }
    return None

# Special Combinations
def detect_panch_mahapurush_yoga(planets, bhavas, lagna):
    """Detect Panch Mahapurush Yoga - five great men"""
    exalted_planets = []
    for planet, data in planets.items():
        if is_exalted(planet, data['house']):
            exalted_planets.append(planet)
    
    if len(exalted_planets) >= 3:
        return {
            'name': 'Panch Mahapurush Yoga',
            'type': 'Special Yoga',
            'description': f'Multiple exalted planets: {", ".join(exalted_planets)}',
            'strength': 'Very Strong'
        }
    return None

# Dosha Yogas (Afflictions)
def detect_kaal_sarp_yoga(planets, bhavas, lagna):
    """Detect Kaal Sarp Yoga - Rahu and Ketu covering all planets"""
    if "Rahu (Mean)" in planets and "Ketu" in planets:
        rahu_house = planets["Rahu (Mean)"]['house']
        ketu_house = planets["Ketu"]['house']
        
        # Check if all planets are between Rahu and Ketu
        all_planets_between = True
        for planet, data in planets.items():
            if planet not in ["Rahu (Mean)", "Ketu"]:
                planet_house = data['house']
                if not (min(rahu_house, ketu_house) <= planet_house <= max(rahu_house, ketu_house)):
                    all_planets_between = False
                    break
        
        if all_planets_between:
            return {
                'name': 'Kaal Sarp Yoga',
                'type': 'Dosha Yoga',
                'description': 'All planets between Rahu and Ketu',
                'strength': 'Strong Affliction'
            }
    return None

def detect_mangal_dosha(planets, bhavas, lagna):
    """Detect Mangal Dosha - Mars in specific houses"""
    if "Mars" in planets:
        mars_house = planets["Mars"]['house']
        if mars_house in [1, 2, 4, 7, 8, 12]:
            return {
                'name': 'Mangal Dosha',
                'type': 'Dosha Yoga',
                'description': f'Mars in {mars_house}th house',
                'strength': 'Affliction'
            }
    return None

# Nakshatra Yogas
def detect_gand_mool_yoga(planets, bhavas, lagna):
    """Detect Gand Mool Yoga - Moon in specific nakshatras"""
    # This would require nakshatra information
    return None

# Tithi Yogas
def detect_amavasya_yoga(planets, bhavas, lagna):
    """Detect Amavasya Yoga - Sun and Moon conjunction"""
    if "Sun" in planets and "Moon" in planets:
        if is_conjunct(planets["Sun"]['house'], planets["Moon"]['house']):
            return {
                'name': 'Amavasya Yoga',
                'type': 'Tithi Yoga',
                'description': 'Sun and Moon in same house',
                'strength': 'Strong'
            }
    return None

def detect_purnima_yoga(planets, bhavas, lagna):
    """Detect Purnima Yoga - Sun and Moon opposition"""
    if "Sun" in planets and "Moon" in planets:
        if is_opposite(planets["Sun"]['house'], planets["Moon"]['house']):
            return {
                'name': 'Purnima Yoga',
                'type': 'Tithi Yoga',
                'description': 'Sun and Moon in opposite houses',
                'strength': 'Strong'
            }
    return None

# House Specific Yogas
def detect_first_house_yoga(planets, bhavas, lagna):
    """Detect 1st house specific yogas"""
    first_house_planets = []
    for planet, data in planets.items():
        if data['house'] == 1:
            first_house_planets.append(planet)
    
    if first_house_planets:
        return {
            'name': 'First House Yoga',
            'type': 'House Yoga',
            'description': f'Planets in 1st house: {", ".join(first_house_planets)}',
            'strength': 'Moderate'
        }
    return None

def detect_second_house_yoga(planets, bhavas, lagna):
    """Detect 2nd house specific yogas"""
    if "Jupiter" in planets and planets["Jupiter"]['house'] == 2:
        return {
            'name': 'Second House Yoga',
            'type': 'House Yoga',
            'description': 'Jupiter in 2nd house (wealth)',
            'strength': 'Strong'
        }
    return None

def detect_fourth_house_yoga(planets, bhavas, lagna):
    """Detect 4th house specific yogas"""
    if "Moon" in planets and planets["Moon"]['house'] == 4:
        return {
            'name': 'Fourth House Yoga',
            'type': 'House Yoga',
            'description': 'Moon in 4th house (happiness)',
            'strength': 'Strong'
        }
    return None

def detect_fifth_house_yoga(planets, bhavas, lagna):
    """Detect 5th house specific yogas"""
    if "Jupiter" in planets and planets["Jupiter"]['house'] == 5:
        return {
            'name': 'Fifth House Yoga',
            'type': 'House Yoga',
            'description': 'Jupiter in 5th house (children)',
            'strength': 'Strong'
        }
    return None

def detect_seventh_house_yoga(planets, bhavas, lagna):
    """Detect 7th house specific yogas"""
    if "Venus" in planets and planets["Venus"]['house'] == 7:
        return {
            'name': 'Seventh House Yoga',
            'type': 'House Yoga',
            'description': 'Venus in 7th house (marriage)',
            'strength': 'Strong'
        }
    return None

def detect_ninth_house_yoga(planets, bhavas, lagna):
    """Detect 9th house specific yogas"""
    if "Jupiter" in planets and planets["Jupiter"]['house'] == 9:
        return {
            'name': 'Ninth House Yoga',
            'type': 'House Yoga',
            'description': 'Jupiter in 9th house (fortune)',
            'strength': 'Strong'
        }
    return None

def detect_tenth_house_yoga(planets, bhavas, lagna):
    """Detect 10th house specific yogas"""
    if "Saturn" in planets and planets["Saturn"]['house'] == 10:
        return {
            'name': 'Tenth House Yoga',
            'type': 'House Yoga',
            'description': 'Saturn in 10th house (career)',
            'strength': 'Strong'
        }
    return None

# Planetary Combinations
def detect_sun_moon_yoga(planets, bhavas, lagna):
    """Detect Sun-Moon combination yoga"""
    if "Sun" in planets and "Moon" in planets:
        sun_house = planets["Sun"]['house']
        moon_house = planets["Moon"]['house']
        
        if is_conjunct(sun_house, moon_house):
            return {
                'name': 'Sun-Moon Conjunction Yoga',
                'type': 'Planetary Yoga',
                'description': 'Sun and Moon in same house',
                'strength': 'Strong'
            }
        elif is_opposite(sun_house, moon_house):
            return {
                'name': 'Sun-Moon Opposition Yoga',
                'type': 'Planetary Yoga',
                'description': 'Sun and Moon in opposite houses',
                'strength': 'Strong'
            }
    return None

def detect_sun_jupiter_yoga(planets, bhavas, lagna):
    """Detect Sun-Jupiter combination yoga"""
    if "Sun" in planets and "Jupiter" in planets:
        if is_friendly("Sun", "Jupiter") and is_conjunct(planets["Sun"]['house'], planets["Jupiter"]['house']):
            return {
                'name': 'Sun-Jupiter Yoga',
                'type': 'Planetary Yoga',
                'description': 'Friendly Sun and Jupiter in same house',
                'strength': 'Strong'
            }
    return None

def detect_venus_jupiter_yoga(planets, bhavas, lagna):
    """Detect Venus-Jupiter combination yoga"""
    if "Venus" in planets and "Jupiter" in planets:
        if is_conjunct(planets["Venus"]['house'], planets["Jupiter"]['house']):
            return {
                'name': 'Venus-Jupiter Yoga',
                'type': 'Planetary Yoga',
                'description': 'Venus and Jupiter in same house',
                'strength': 'Strong'
            }
    return None

def detect_rahu_ketu_yoga(planets, bhavas, lagna):
    """Detect Rahu-Ketu combination yoga"""
    if "Rahu (Mean)" in planets and "Ketu" in planets:
        if is_opposite(planets["Rahu (Mean)"]['house'], planets["Ketu"]['house']):
            return {
                'name': 'Rahu-Ketu Opposition Yoga',
                'type': 'Planetary Yoga',
                'description': 'Rahu and Ketu in opposite houses',
                'strength': 'Strong'
            }
    return None

# Special Yogas
def detect_akhand_samrajya_yoga(planets, bhavas, lagna):
    """Detect Akhand Samrajya Yoga - continuous empire"""
    # All planets in one half of the chart
    houses = [data['house'] for data in planets.values()]
    if all(house <= 6 for house in houses) or all(house >= 7 for house in houses):
        return {
            'name': 'Akhand Samrajya Yoga',
            'type': 'Special Yoga',
            'description': 'All planets in one half of the chart',
            'strength': 'Very Strong'
        }
    return None

def detect_sarvatobhadra_yoga(planets, bhavas, lagna):
    """Detect Sarvatobhadra Yoga - auspicious in all directions"""
    # Planets in all four directions (1,4,7,10)
    kendra_planets = []
    for planet, data in planets.items():
        if data['house'] in [1, 4, 7, 10]:
            kendra_planets.append(planet)
    
    if len(kendra_planets) >= 3:
        return {
            'name': 'Sarvatobhadra Yoga',
            'type': 'Special Yoga',
            'description': f'Planets in kendras: {", ".join(kendra_planets)}',
            'strength': 'Strong'
        }
    return None

# Modern Yogas
def detect_foreign_education_yoga(planets, bhavas, lagna):
    """Detect foreign education yoga"""
    if "Mercury" in planets and "Rahu (Mean)" in planets:
        if planets["Mercury"]['house'] == 4 and planets["Rahu (Mean)"]['house'] == 9:
            return {
                'name': 'Foreign Education Yoga',
                'type': 'Modern Yoga',
                'description': 'Mercury in 4th and Rahu in 9th house',
                'strength': 'Strong'
            }
    return None

def detect_technology_yoga(planets, bhavas, lagna):
    """Detect technology yoga"""
    if "Mercury" in planets and "Uranus" in planets:
        if is_conjunct(planets["Mercury"]['house'], planets["Uranus"]['house']):
            return {
                'name': 'Technology Yoga',
                'type': 'Modern Yoga',
                'description': 'Mercury and Uranus in same house',
                'strength': 'Strong'
            }
    return None

def detect_medicine_yoga(planets, bhavas, lagna):
    """Detect medicine yoga"""
    if "Mercury" in planets and "Neptune" in planets:
        if is_conjunct(planets["Mercury"]['house'], planets["Neptune"]['house']):
            return {
                'name': 'Medicine Yoga',
                'type': 'Modern Yoga',
                'description': 'Mercury and Neptune in same house',
                'strength': 'Strong'
            }
    return None

# Strength Yogas
def detect_exalted_combination_yoga(planets, bhavas, lagna):
    """Detect exalted combination yoga"""
    exalted_count = 0
    for planet, data in planets.items():
        if is_exalted(planet, data['house']):
            exalted_count += 1
    
    if exalted_count >= 2:
        return {
            'name': 'Multiple Exalted Yoga',
            'type': 'Strength Yoga',
            'description': f'{exalted_count} planets exalted',
            'strength': 'Very Strong'
        }
    return None

def detect_own_sign_combination_yoga(planets, bhavas, lagna):
    """Detect own sign combination yoga"""
    own_sign_count = 0
    for planet, data in planets.items():
        if get_sign_lord(data['house']) == planet:
            own_sign_count += 1
    
    if own_sign_count >= 2:
        return {
            'name': 'Multiple Own Sign Yoga',
            'type': 'Strength Yoga',
            'description': f'{own_sign_count} planets in own signs',
            'strength': 'Strong'
        }
    return None

# Additional yoga functions (simplified versions for brevity)
def detect_kesari_yoga(planets, bhavas, lagna):
    """Detect Kesari Yoga - Jupiter in kendra"""
    if "Jupiter" in planets and planets["Jupiter"]['house'] in [1, 4, 7, 10]:
        return {
            'name': 'Kesari Yoga',
            'type': 'Raj Yoga',
            'description': f'Jupiter in {planets["Jupiter"]["house"]}th house (kendra)',
            'strength': 'Strong'
        }
    return None

def detect_sankha_yoga(planets, bhavas, lagna):
    """Detect Sankha Yoga - Venus in kendra"""
    if "Venus" in planets and planets["Venus"]['house'] in [1, 4, 7, 10]:
        return {
            'name': 'Sankha Yoga',
            'type': 'Raj Yoga',
            'description': f'Venus in {planets["Venus"]["house"]}th house (kendra)',
            'strength': 'Strong'
        }
    return None

def detect_vasumati_yoga(planets, bhavas, lagna):
    """Detect Vasumati Yoga - Venus in 2nd house"""
    if "Venus" in planets and planets["Venus"]['house'] == 2:
        return {
            'name': 'Vasumati Yoga',
            'type': 'Dhan Yoga',
            'description': 'Venus in 2nd house',
            'strength': 'Strong'
        }
    return None

def detect_kubera_yoga(planets, bhavas, lagna):
    """Detect Kubera Yoga - Jupiter in 11th house"""
    if "Jupiter" in planets and planets["Jupiter"]['house'] == 11:
        return {
            'name': 'Kubera Yoga',
            'type': 'Dhan Yoga',
            'description': 'Jupiter in 11th house',
            'strength': 'Strong'
        }
    return None

def detect_budh_aditya_yoga(planets, bhavas, lagna):
    """Detect Budh-Aditya Yoga - Mercury and Sun conjunction"""
    if "Mercury" in planets and "Sun" in planets:
        if is_conjunct(planets["Mercury"]['house'], planets["Sun"]['house']):
            return {
                'name': 'Budh-Aditya Yoga',
                'type': 'Vidya Yoga',
                'description': 'Mercury and Sun in same house',
                'strength': 'Strong'
            }
    return None

def detect_guru_chandal_yoga(planets, bhavas, lagna):
    """Detect Guru-Chandal Yoga - Jupiter and Rahu conjunction"""
    if "Jupiter" in planets and "Rahu (Mean)" in planets:
        if is_conjunct(planets["Jupiter"]['house'], planets["Rahu (Mean)"]['house']):
            return {
                'name': 'Guru-Chandal Yoga',
                'type': 'Special Yoga',
                'description': 'Jupiter and Rahu in same house',
                'strength': 'Mixed'
            }
    return None

# Add more yoga detection functions as needed...
# For brevity, I'm including the most important ones above.
# The complete system would have over 100 yoga detection functions.

# Placeholder functions for remaining yogas (to be implemented as needed)
def detect_brahma_yoga(planets, bhavas, lagna): return None
def detect_indra_yoga(planets, bhavas, lagna): return None
def detect_mahendra_yoga(planets, bhavas, lagna): return None
def detect_rajalakshmi_yoga(planets, bhavas, lagna): return None
def detect_saraswati_yoga(planets, bhavas, lagna): return None
def detect_sarala_yoga(planets, bhavas, lagna): return None
def detect_vyaghata_yoga(planets, bhavas, lagna): return None
def detect_paridhi_yoga(planets, bhavas, lagna): return None
def detect_sankata_yoga(planets, bhavas, lagna): return None
def detect_mangal_yoga(planets, bhavas, lagna): return None
def detect_saubhagya_yoga(planets, bhavas, lagna): return None
def detect_putra_yoga(planets, bhavas, lagna): return None
def detect_santan_yoga(planets, bhavas, lagna): return None
def detect_dharma_yoga(planets, bhavas, lagna): return None
def detect_artha_yoga(planets, bhavas, lagna): return None
def detect_kama_yoga(planets, bhavas, lagna): return None
def detect_moksha_yoga(planets, bhavas, lagna): return None
def detect_videsh_yoga(planets, bhavas, lagna): return None
def detect_yatra_yoga(planets, bhavas, lagna): return None
def detect_foreign_yoga(planets, bhavas, lagna): return None
def detect_immigration_yoga(planets, bhavas, lagna): return None
def detect_tapasvi_yoga(planets, bhavas, lagna): return None
def detect_bhakti_yoga(planets, bhavas, lagna): return None
def detect_gyan_yoga(planets, bhavas, lagna): return None
def detect_nabhas_yoga(planets, bhavas, lagna): return None
def detect_nala_yoga(planets, bhavas, lagna): return None
def detect_nala_raj_yoga(planets, bhavas, lagna): return None
def detect_nala_mahendra_yoga(planets, bhavas, lagna): return None
def detect_nala_brahma_yoga(planets, bhavas, lagna): return None
def detect_nala_indra_yoga(planets, bhavas, lagna): return None
def detect_nala_kesari_yoga(planets, bhavas, lagna): return None
def detect_nala_sankha_yoga(planets, bhavas, lagna): return None
def detect_nala_vasumati_yoga(planets, bhavas, lagna): return None
def detect_nala_kubera_yoga(planets, bhavas, lagna): return None
def detect_rahu_dosha(planets, bhavas, lagna): return None
def detect_ketu_dosha(planets, bhavas, lagna): return None
def detect_saturn_dosha(planets, bhavas, lagna): return None
def detect_sun_dosha(planets, bhavas, lagna): return None
def detect_nakshatra_yoga(planets, bhavas, lagna): return None
def detect_janma_nakshatra_yoga(planets, bhavas, lagna): return None
def detect_purnima_yoga(planets, bhavas, lagna): return None
def detect_ekadashi_yoga(planets, bhavas, lagna): return None
def detect_sankranti_yoga(planets, bhavas, lagna): return None
def detect_solar_eclipse_yoga(planets, bhavas, lagna): return None
def detect_lunar_eclipse_yoga(planets, bhavas, lagna): return None
def detect_third_house_yoga(planets, bhavas, lagna): return None
def detect_sixth_house_yoga(planets, bhavas, lagna): return None
def detect_eighth_house_yoga(planets, bhavas, lagna): return None
def detect_eleventh_house_yoga(planets, bhavas, lagna): return None
def detect_twelfth_house_yoga(planets, bhavas, lagna): return None
def detect_sun_mars_yoga(planets, bhavas, lagna): return None
def detect_moon_venus_yoga(planets, bhavas, lagna): return None
def detect_moon_mercury_yoga(planets, bhavas, lagna): return None
def detect_mars_jupiter_yoga(planets, bhavas, lagna): return None
def detect_mercury_venus_yoga(planets, bhavas, lagna): return None
def detect_saturn_venus_yoga(planets, bhavas, lagna): return None
def detect_rahu_saturn_yoga(planets, bhavas, lagna): return None
def detect_ketu_mars_yoga(planets, bhavas, lagna): return None
def detect_sarvartha_siddhi_yoga(planets, bhavas, lagna): return None
def detect_rajyoga_bhanga(planets, bhavas, lagna): return None
def detect_dhanayoga_bhanga(planets, bhavas, lagna): return None
def detect_vidyayoga_bhanga(planets, bhavas, lagna): return None
def detect_ayushyoga_bhanga(planets, bhavas, lagna): return None
def detect_putrayoga_bhanga(planets, bhavas, lagna): return None
def detect_kalatra_yoga_bhanga(planets, bhavas, lagna): return None
def detect_foreign_marriage_yoga(planets, bhavas, lagna): return None
def detect_foreign_career_yoga(planets, bhavas, lagna): return None
def detect_media_yoga(planets, bhavas, lagna): return None
def detect_sports_yoga(planets, bhavas, lagna): return None
def detect_arts_yoga(planets, bhavas, lagna): return None
def detect_music_yoga(planets, bhavas, lagna): return None
def detect_writing_yoga(planets, bhavas, lagna): return None
def detect_research_yoga(planets, bhavas, lagna): return None
def detect_law_yoga(planets, bhavas, lagna): return None
def detect_business_yoga(planets, bhavas, lagna): return None
def detect_politics_yoga(planets, bhavas, lagna): return None
def detect_administration_yoga(planets, bhavas, lagna): return None
def detect_dasha_yoga(planets, bhavas, lagna): return None
def detect_antardasha_yoga(planets, bhavas, lagna): return None
def detect_pratyantar_yoga(planets, bhavas, lagna): return None
def detect_sookshma_yoga(planets, bhavas, lagna): return None
def detect_prana_yoga(planets, bhavas, lagna): return None
def detect_deha_yoga(planets, bhavas, lagna): return None
def detect_gem_yoga(planets, bhavas, lagna): return None
def detect_mantra_yoga(planets, bhavas, lagna): return None
def detect_yantra_yoga(planets, bhavas, lagna): return None
def detect_tantra_yoga(planets, bhavas, lagna): return None
def detect_puja_yoga(planets, bhavas, lagna): return None
def detect_donation_yoga(planets, bhavas, lagna): return None
def detect_fasting_yoga(planets, bhavas, lagna): return None
def detect_meditation_yoga(planets, bhavas, lagna): return None
def detect_yoga_yoga(planets, bhavas, lagna): return None
def detect_benefic_combination_yoga(planets, bhavas, lagna): return None
def detect_malefic_combination_yoga(planets, bhavas, lagna): return None
def detect_neutral_combination_yoga(planets, bhavas, lagna): return None
def detect_mixed_combination_yoga(planets, bhavas, lagna): return None
def detect_debilitated_combination_yoga(planets, bhavas, lagna): return None
def detect_friendly_sign_combination_yoga(planets, bhavas, lagna): return None
def detect_enemy_sign_combination_yoga(planets, bhavas, lagna): return None
def detect_neutral_sign_combination_yoga(planets, bhavas, lagna): return None 

# Enhanced Yoga Detection Functions with Aspect and Strength Data

def detect_shankh_yoga(planets, bhavas, lagna):
    """Detect Shankh Yoga - Venus in 2nd house with aspect from Jupiter"""
    if "Venus" in planets and "Jupiter" in planets:
        venus_house = planets["Venus"]['house']
        jupiter_house = planets["Jupiter"]['house']
        
        if venus_house == 2 and has_aspect(jupiter_house, venus_house, "5th"):
            return {
                'name': 'Shankh Yoga',
                'type': 'Dhan Yoga',
                'description': 'Venus in 2nd house with Jupiter\'s 5th aspect',
                'strength': 'Strong'
            }
    return None

def detect_parvat_yoga(planets, bhavas, lagna):
    """Detect Parvat Yoga - Moon in 4th house with aspect from Mars"""
    if "Moon" in planets and "Mars" in planets:
        moon_house = planets["Moon"]['house']
        mars_house = planets["Mars"]['house']
        
        if moon_house == 4 and has_aspect(mars_house, moon_house, "4th"):
            return {
                'name': 'Parvat Yoga',
                'type': 'Special Yoga',
                'description': 'Moon in 4th house with Mars\' 4th aspect',
                'strength': 'Strong'
            }
    return None

def detect_grahan_yoga(planets, bhavas, lagna):
    """Detect Grahan Yoga - Sun and Moon conjunction with Rahu/Ketu"""
    if "Sun" in planets and "Moon" in planets and "Rahu (Mean)" in planets:
        sun_house = planets["Sun"]['house']
        moon_house = planets["Moon"]['house']
        rahu_house = planets["Rahu (Mean)"]['house']
        
        if is_conjunct(sun_house, moon_house) and (is_conjunct(sun_house, rahu_house) or has_aspect(sun_house, rahu_house, "7th")):
            return {
                'name': 'Grahan Yoga',
                'type': 'Special Yoga',
                'description': 'Sun-Moon conjunction with Rahu',
                'strength': 'Strong'
            }
    return None

def detect_chandal_yoga(planets, bhavas, lagna):
    """Detect Chandal Yoga - Jupiter and Rahu conjunction"""
    if "Jupiter" in planets and "Rahu (Mean)" in planets:
        jupiter_house = planets["Jupiter"]['house']
        rahu_house = planets["Rahu (Mean)"]['house']
        
        if is_conjunct(jupiter_house, rahu_house):
            return {
                'name': 'Chandal Yoga',
                'type': 'Special Yoga',
                'description': 'Jupiter and Rahu in same house',
                'strength': 'Mixed'
            }
    return None

def detect_kemadruma_yoga(planets, bhavas, lagna):
    """Detect Kemadruma Yoga - Moon without any planets in adjacent houses"""
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
                'name': 'Kemadruma Yoga',
                'type': 'Dosha Yoga',
                'description': 'Moon without planets in adjacent houses',
                'strength': 'Affliction'
            }
    return None

def detect_gajakesari_yoga(planets, bhavas, lagna):
    """Detect Gajakesari Yoga - Jupiter and Moon in kendras with aspect"""
    if "Jupiter" in planets and "Moon" in planets:
        jupiter_house = planets["Jupiter"]['house']
        moon_house = planets["Moon"]['house']
        
        kendras = [1, 4, 7, 10]
        if jupiter_house in kendras and moon_house in kendras and has_aspect(jupiter_house, moon_house, "7th"):
            return {
                'name': 'Gajakesari Yoga',
                'type': 'Raj Yoga',
                'description': 'Jupiter and Moon in kendras with 7th aspect',
                'strength': 'Very Strong'
            }
    return None

def detect_budh_aditya_enhanced_yoga(planets, bhavas, lagna):
    """Enhanced Budh-Aditya Yoga with strength consideration"""
    if "Mercury" in planets and "Sun" in planets:
        mercury_house = planets["Mercury"]['house']
        sun_house = planets["Sun"]['house']
        
        if is_conjunct(mercury_house, sun_house):
            mercury_strength = planets["Mercury"].get('strength', 'Neutral')
            sun_strength = planets["Sun"].get('strength', 'Neutral')
            
            strength = 'Strong'
            if mercury_strength == 'Exalted' or sun_strength == 'Exalted':
                strength = 'Very Strong'
            
            return {
                'name': 'Enhanced Budh-Aditya Yoga',
                'type': 'Vidya Yoga',
                'description': f'Mercury-Sun conjunction (Mercury: {mercury_strength}, Sun: {sun_strength})',
                'strength': strength
            }
    return None

def detect_amrit_siddhi_yoga(planets, bhavas, lagna, time_info=None):
    """Detect Amrit Siddhi Yoga - based on Tithi and planetary positions"""
    if time_info and "Moon" in planets:
        tithi = time_info.get('tithi', 0)
        moon_house = planets["Moon"]['house']
        
        # Amrit Siddhi Yoga: Moon in 4th house on specific tithis
        if moon_house == 4 and tithi in [1, 6, 11, 16, 21, 26]:
            return {
                'name': 'Amrit Siddhi Yoga',
                'type': 'Special Yoga',
                'description': f'Moon in 4th house on Tithi {tithi}',
                'strength': 'Strong'
            }
    return None

def detect_parijat_yoga(planets, bhavas, lagna):
    """Detect Parijat Yoga - Venus in 6th house with navamsha consideration"""
    if "Venus" in planets:
        venus_data = planets["Venus"]
        venus_house = venus_data['house']
        navamsha_sign = venus_data.get('navamsha_sign', '')
        
        if venus_house == 6 and 'Cancer' in navamsha_sign:
            return {
                'name': 'Parijat Yoga',
                'type': 'Special Yoga',
                'description': 'Venus in 6th house with Cancer navamsha',
                'strength': 'Strong'
            }
    return None

def detect_vasumati_enhanced_yoga(planets, bhavas, lagna):
    """Enhanced Vasumati Yoga with strength consideration"""
    if "Venus" in planets:
        venus_data = planets["Venus"]
        venus_house = venus_data['house']
        venus_strength = venus_data.get('strength', 'Neutral')
        
        if venus_house == 2:
            strength = 'Strong'
            if venus_strength == 'Exalted':
                strength = 'Very Strong'
            elif venus_strength == 'Debilitated':
                strength = 'Weak'
            
            return {
                'name': 'Enhanced Vasumati Yoga',
                'type': 'Dhan Yoga',
                'description': f'Venus in 2nd house ({venus_strength})',
                'strength': strength
            }
    return None

def detect_rajalakshmi_enhanced_yoga(planets, bhavas, lagna):
    """Enhanced Rajalakshmi Yoga with multiple benefic combinations"""
    benefic_planets = ["Jupiter", "Venus", "Mercury"]
    benefic_count = 0
    strong_benefics = []
    
    for planet in benefic_planets:
        if planet in planets:
            planet_data = planets[planet]
            planet_house = planet_data['house']
            planet_strength = planet_data.get('strength', 'Neutral')
            
            if planet_house in [2, 5, 9, 11]:  # Wealth houses
                benefic_count += 1
                if planet_strength in ['Exalted', 'Own Sign']:
                    strong_benefics.append(planet)
    
    if benefic_count >= 2:
        strength = 'Strong'
        if len(strong_benefics) >= 2:
            strength = 'Very Strong'
        
        return {
            'name': 'Enhanced Rajalakshmi Yoga',
            'type': 'Dhan Yoga',
            'description': f'Multiple benefics in wealth houses: {", ".join(strong_benefics)}',
            'strength': strength
        }
    return None

def detect_akhand_samrajya_enhanced_yoga(planets, bhavas, lagna):
    """Enhanced Akhand Samrajya Yoga with strength consideration"""
    houses = [data['house'] for data in planets.values()]
    
    # Check if all planets are in one half
    if all(house <= 6 for house in houses) or all(house >= 7 for house in houses):
        # Count strong planets
        strong_planets = []
        for planet, data in planets.items():
            strength = data.get('strength', 'Neutral')
            if strength in ['Exalted', 'Own Sign']:
                strong_planets.append(planet)
        
        strength = 'Strong'
        if len(strong_planets) >= 3:
            strength = 'Very Strong'
        
        return {
            'name': 'Enhanced Akhand Samrajya Yoga',
            'type': 'Special Yoga',
            'description': f'All planets in one half with {len(strong_planets)} strong planets',
            'strength': strength
        }
    return None 