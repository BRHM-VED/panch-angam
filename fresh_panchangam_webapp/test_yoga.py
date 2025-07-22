#!/usr/bin/env python3
"""
Test script for yoga detection system
"""

from yoga_rules import detect_all_yogas

# Sample kundli data for testing
sample_planets = {
    'Sun': {'house': 1, 'sign': 'Mesha (Aries)', 'deg': 15.0},
    'Moon': {'house': 4, 'sign': 'Karka (Cancer)', 'deg': 20.0},
    'Mars': {'house': 10, 'sign': 'Makara (Capricorn)', 'deg': 5.0},
    'Mercury': {'house': 6, 'sign': 'Kanya (Virgo)', 'deg': 25.0},
    'Jupiter': {'house': 2, 'sign': 'Vrishabha (Taurus)', 'deg': 10.0},
    'Venus': {'house': 7, 'sign': 'Tula (Libra)', 'deg': 18.0},
    'Saturn': {'house': 12, 'sign': 'Meena (Pisces)', 'deg': 8.0},
    'Uranus': {'house': 3, 'sign': 'Mithuna (Gemini)', 'deg': 12.0},
    'Neptune': {'house': 5, 'sign': 'Simha (Leo)', 'deg': 30.0},
    'Pluto': {'house': 8, 'sign': 'Vrischika (Scorpio)', 'deg': 22.0},
    'Rahu (Mean)': {'house': 9, 'sign': 'Dhanu (Sagittarius)', 'deg': 15.0},
    'Ketu (Mean)': {'house': 3, 'sign': 'Mithuna (Gemini)', 'deg': 15.0}
}

sample_bhavas = [
    {'house': 1, 'sign': 'Mesha (Aries)'},
    {'house': 2, 'sign': 'Vrishabha (Taurus)'},
    {'house': 3, 'sign': 'Mithuna (Gemini)'},
    {'house': 4, 'sign': 'Karka (Cancer)'},
    {'house': 5, 'sign': 'Simha (Leo)'},
    {'house': 6, 'sign': 'Kanya (Virgo)'},
    {'house': 7, 'sign': 'Tula (Libra)'},
    {'house': 8, 'sign': 'Vrischika (Scorpio)'},
    {'house': 9, 'sign': 'Dhanu (Sagittarius)'},
    {'house': 10, 'sign': 'Makara (Capricorn)'},
    {'house': 11, 'sign': 'Kumbha (Aquarius)'},
    {'house': 12, 'sign': 'Meena (Pisces)'}
]

sample_lagna = {
    'sign': 'Mesha (Aries)',
    'sign_number': 1,
    'deg': 15.0
}

def test_yoga_detection():
    print("Testing Yoga Detection System...")
    print("=" * 50)
    
    # Add strength information to sample planets
    for planet, data in sample_planets.items():
        data['strength'] = 'Neutral'
        data['is_exalted'] = False
        data['is_debilitated'] = False
        data['is_own_sign'] = False
    
    # Sample time info
    sample_time_info = {
        'tithi': 15,  # Purnima
        'nakshatra': 10,  # Magha
        'lunar_phase': 180,
        'sun_position': 0,
        'moon_position': 180
    }
    
    # Test yoga detection
    detected_yogas = detect_all_yogas(sample_planets, sample_bhavas, sample_lagna, sample_time_info)
    
    print(f"Total yogas detected: {len(detected_yogas)}")
    print()
    
    if detected_yogas:
        # Group by type
        yogas_by_type = {}
        for yoga in detected_yogas:
            if yoga['type'] not in yogas_by_type:
                yogas_by_type[yoga['type']] = []
            yogas_by_type[yoga['type']].append(yoga)
        
        for yoga_type, yogas in yogas_by_type.items():
            print(f"\n{yoga_type} ({len(yogas)} yogas):")
            print("-" * 30)
            for yoga in yogas:
                print(f"  • {yoga['name']} - {yoga['description']} ({yoga['strength']})")
    else:
        print("No yogas detected in this sample data.")
    
    print("\n" + "=" * 50)
    print("Yoga detection test completed!")

if __name__ == "__main__":
    test_yoga_detection() 