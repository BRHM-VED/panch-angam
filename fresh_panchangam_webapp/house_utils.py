# House Calculation Utilities for Vedic Astrology
# This module provides functions to calculate houses relative to the Lagna sign

def get_sign_from_deg(deg):
    """
    Return sign number (1-12) from 0-360°.
    
    Args:
        deg (float): Degree (0-360)
    
    Returns:
        int: Sign number (1=Aries, 2=Taurus, ..., 12=Pisces)
    """
    return int(deg / 30) + 1

def get_relative_house(lagna_deg, planet_deg):
    """
    Calculate house number (1-12) of a planet relative to Lagna.
    
    Args:
        lagna_deg (float): Lagna degree (0-360)
        planet_deg (float): Planet degree (0-360)
    
    Returns:
        int: House number relative to Lagna (1-12)
    
    Example:
        If Lagna is in Cancer (90-120°) and Jupiter is in Leo (120-150°):
        Lagna sign = 4, Jupiter sign = 5
        Relative house = (5 - 4 + 12) % 12 + 1 = 2nd house from Lagna
    """
    lagna_sign = get_sign_from_deg(lagna_deg)
    planet_sign = get_sign_from_deg(planet_deg)
    return ((planet_sign - lagna_sign + 12) % 12) + 1

def calculate_all_relative_houses(lagna_deg, planets_dict):
    """
    Calculate relative houses for all planets based on Lagna.
    
    Args:
        lagna_deg (float): Lagna degree (0-360)
        planets_dict (dict): Dictionary with planet positions in degrees
    
    Returns:
        dict: Updated planets_dict with relative house numbers
    """
    updated_planets = planets_dict.copy()
    
    for planet, data in updated_planets.items():
        if isinstance(data, dict) and 'longitude' in data:
            # If planet data has longitude
            relative_house = get_relative_house(lagna_deg, data['longitude'])
            updated_planets[planet]['house'] = relative_house
        elif isinstance(data, (int, float)):
            # If planet data is just the degree
            relative_house = get_relative_house(lagna_deg, data)
            updated_planets[planet] = {
                'longitude': data,
                'house': relative_house
            }
    
    return updated_planets

def is_kendra_house(house_number):
    """
    Check if house is a Kendra (angular house).
    
    Args:
        house_number (int): House number (1-12)
    
    Returns:
        bool: True if house is Kendra (1, 4, 7, 10)
    """
    return house_number in [1, 4, 7, 10]

def is_trikona_house(house_number):
    """
    Check if house is a Trikona (trine house).
    
    Args:
        house_number (int): House number (1-12)
    
    Returns:
        bool: True if house is Trikona (1, 5, 9)
    """
    return house_number in [1, 5, 9]

def is_dusthana_house(house_number):
    """
    Check if house is a Dusthana (difficult house).
    
    Args:
        house_number (int): House number (1-12)
    
    Returns:
        bool: True if house is Dusthana (6, 8, 12)
    """
    return house_number in [6, 8, 12]

def get_house_nature(house_number):
    """
    Get the nature of a house.
    
    Args:
        house_number (int): House number (1-12)
    
    Returns:
        str: House nature ('Kendra', 'Trikona', 'Dusthana', or 'Neutral')
    """
    if is_kendra_house(house_number):
        return 'Kendra'
    elif is_trikona_house(house_number):
        return 'Trikona'
    elif is_dusthana_house(house_number):
        return 'Dusthana'
    else:
        return 'Neutral'

def check_parivartana_yoga(planet1, planet2, planets_dict):
    """
    Check for Parivartana Yoga (exchange of houses) between two planets.
    
    Args:
        planet1 (str): Name of first planet
        planet2 (str): Name of second planet
        planets_dict (dict): Dictionary with planet positions and houses
    
    Returns:
        bool: True if Parivartana Yoga exists
    """
    if planet1 not in planets_dict or planet2 not in planets_dict:
        return False
    
    house1 = planets_dict[planet1]['house']
    house2 = planets_dict[planet2]['house']
    
    # Check if planets are in each other's houses
    return house1 == house2

def validate_house_calculation(lagna_deg, planet_deg, expected_house):
    """
    Validate house calculation for testing purposes.
    
    Args:
        lagna_deg (float): Lagna longitude
        planet_deg (float): Planet longitude
        expected_house (int): Expected house number
    
    Returns:
        bool: True if calculation matches expected result
    """
    calculated_house = get_relative_house(lagna_deg, planet_deg)
    return calculated_house == expected_house 