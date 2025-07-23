#!/usr/bin/env python3
"""
Test script for comprehensive Kundli details
"""

from kundli_details import calculate_comprehensive_kundli_details

def test_comprehensive_kundli():
    print("Testing Comprehensive Kundli Details System...")
    print("=" * 60)
    
    # Test data
    date_str = "1990-01-01"
    time_str = "12:00"
    lat = 28.6139
    lon = 77.2090
    tz = 5.5
    name = "Test User"
    gender = "Male"
    
    try:
        # Calculate comprehensive details
        result = calculate_comprehensive_kundli_details(
            date_str, time_str, lat, lon, tz, name, gender
        )
        
        print(f"✅ Successfully calculated comprehensive Kundli details!")
        print()
        
        # Display results
        print("📋 Basic Details:")
        print("-" * 30)
        for key, value in result['basic_details'].items():
            print(f"  {key}: {value}")
        
        print("\n🔮 Astrological Details:")
        print("-" * 30)
        for key, value in result['astrological_details'].items():
            print(f"  {key}: {value}")
        
        print("\n📅 Panchang Details:")
        print("-" * 30)
        for key, value in result['panchang_details'].items():
            print(f"  {key}: {value}")
        
        print("\n🍀 Lucky Points:")
        print("-" * 30)
        for key, value in result['lucky_points'].items():
            print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)
        print("✅ All sections calculated successfully!")
        print(f"📊 Total sections: 4")
        print(f"📊 Total fields: {len(result['basic_details']) + len(result['astrological_details']) + len(result['panchang_details']) + len(result['lucky_points'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_comprehensive_kundli() 