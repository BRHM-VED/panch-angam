#!/usr/bin/env python3
"""
Test script for dosha detection system
"""

from dosha_rules import detect_all_doshas

# Sample kundli data for testing
sample_kundli = {
    'planets': {
        'Sun': {'house': 1, 'sign': 'Mesha (Aries)', 'deg': 15.0, 'strength': 'Neutral'},
        'Moon': {'house': 4, 'sign': 'Karka (Cancer)', 'deg': 20.0, 'strength': 'Neutral'},
        'Mars': {'house': 7, 'sign': 'Tula (Libra)', 'deg': 5.0, 'strength': 'Neutral'},
        'Mercury': {'house': 6, 'sign': 'Kanya (Virgo)', 'deg': 25.0, 'strength': 'Neutral'},
        'Jupiter': {'house': 2, 'sign': 'Vrishabha (Taurus)', 'deg': 10.0, 'strength': 'Neutral'},
        'Venus': {'house': 7, 'sign': 'Tula (Libra)', 'deg': 18.0, 'strength': 'Neutral'},
        'Saturn': {'house': 12, 'sign': 'Meena (Pisces)', 'deg': 8.0, 'strength': 'Neutral'},
        'Uranus': {'house': 3, 'sign': 'Mithuna (Gemini)', 'deg': 12.0, 'strength': 'Neutral'},
        'Neptune': {'house': 5, 'sign': 'Simha (Leo)', 'deg': 30.0, 'strength': 'Neutral'},
        'Pluto': {'house': 8, 'sign': 'Vrischika (Scorpio)', 'deg': 22.0, 'strength': 'Neutral'},
        'Rahu (Mean)': {'house': 9, 'sign': 'Dhanu (Sagittarius)', 'deg': 15.0, 'strength': 'Neutral'},
        'Ketu (Mean)': {'house': 3, 'sign': 'Mithuna (Gemini)', 'deg': 15.0, 'strength': 'Neutral'}
    },
    'lagna': {
        'sign': 'Mesha (Aries)',
        'sign_number': 1,
        'deg': 15.0
    },
    'bhavas': [
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
    ],
    'input': {
        'date': '1990-01-01',
        'time': '12:00',
        'lat': 28.6139,
        'lon': 77.2090,
        'tz': 5.5
    }
}

def test_dosha_detection():
    print("Testing Dosha Detection System...")
    print("=" * 50)
    
    # Test dosha detection
    detected_doshas = detect_all_doshas(sample_kundli)
    
    print(f"Total doshas detected: {len(detected_doshas)}")
    print()
    
    if detected_doshas:
        # Group by type
        doshas_by_type = {}
        for dosha in detected_doshas:
            if dosha['type'] not in doshas_by_type:
                doshas_by_type[dosha['type']] = []
            doshas_by_type[dosha['type']].append(dosha)
        
        for dosha_type, doshas in doshas_by_type.items():
            print(f"\n{dosha_type} ({len(doshas)} doshas):")
            print("-" * 30)
            for dosha in doshas:
                print(f"  • {dosha['name']} - {dosha['description']} ({dosha['severity']})")
                print(f"    Effects: {dosha['effects']}")
                print(f"    Remedies: {dosha['remedies']}")
                print()
    else:
        print("No doshas detected in this sample data.")
    
    print("\n" + "=" * 50)
    print("Dosha detection test completed!")

if __name__ == "__main__":
    test_dosha_detection() 