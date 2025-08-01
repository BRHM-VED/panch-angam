#!/usr/bin/env python3
"""
Test script for Kundli API
Demonstrates how to use the Kundli API endpoints
"""

import requests
import json

# API base URL (update this to your deployed URL)
BASE_URL = "https://panch-angam-xmmn.onrender.com"

def test_basic_kundli():
    """Test the basic kundli endpoint"""
    url = f"{BASE_URL}/api/kundli/basic"
    
    data = {
        "date": "1990-05-15",
        "time": "14:30",
        "lat": 19.0760,
        "lon": 72.8777,
        "tz": 5.5,
        "name": "Test User",
        "gender": "Male"
    }
    
    print("Testing Basic Kundli API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Basic Kundli API Test Successful!")
            print(f"Planets found: {len(result.get('planets', {}))}")
            print(f"Lagna: {result.get('lagna', {}).get('sign', 'N/A')}")
        else:
            print(f"❌ Basic Kundli API Test Failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Basic Kundli API: {e}")

def test_comprehensive_kundli():
    """Test the comprehensive kundli endpoint"""
    url = f"{BASE_URL}/api/kundli/comprehensive"
    
    data = {
        "date": "1990-05-15",
        "time": "14:30",
        "lat": 19.0760,
        "lon": 72.8777,
        "tz": 5.5,
        "name": "Test User",
        "gender": "Male"
    }
    
    print("\nTesting Comprehensive Kundli API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Comprehensive Kundli API Test Successful!")
            print(f"Planets found: {len(result.get('planets', {}))}")
            print(f"Yogas found: {len(result.get('yogas', []))}")
            print(f"Doshas found: {len(result.get('doshas', []))}")
            print(f"Comprehensive details: {bool(result.get('comprehensive_details'))}")
        else:
            print(f"❌ Comprehensive Kundli API Test Failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Comprehensive Kundli API: {e}")

def test_planets_only():
    """Test the planets-only endpoint"""
    url = f"{BASE_URL}/api/kundli/planets"
    
    data = {
        "date": "1990-05-15",
        "time": "14:30",
        "lat": 19.0760,
        "lon": 72.8777,
        "tz": 5.5
    }
    
    print("\nTesting Planets Only API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Planets Only API Test Successful!")
            print(f"Planets found: {len(result.get('planets', {}))}")
            
            # Show some planet details
            planets = result.get('planets', {})
            for planet, details in list(planets.items())[:3]:  # Show first 3 planets
                if 'sign' in details:
                    print(f"  {planet}: {details['sign']} at {details.get('degree', 0):.1f}°")
        else:
            print(f"❌ Planets Only API Test Failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Planets Only API: {e}")

def test_lagna_only():
    """Test the lagna-only endpoint"""
    url = f"{BASE_URL}/api/kundli/lagna"
    
    data = {
        "date": "1990-05-15",
        "time": "14:30",
        "lat": 19.0760,
        "lon": 72.8777,
        "tz": 5.5
    }
    
    print("\nTesting Lagna Only API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Lagna Only API Test Successful!")
            print(f"Lagna: {result.get('lagna', {}).get('sign', 'N/A')}")
            print(f"Houses found: {len(result.get('houses', []))}")
        else:
            print(f"❌ Lagna Only API Test Failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Lagna Only API: {e}")

def test_api_docs():
    """Test the API documentation endpoint"""
    url = f"{BASE_URL}/api/kundli/docs"
    
    print("\nTesting API Documentation...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Documentation Test Successful!")
            print(f"API Name: {result.get('api_name', 'N/A')}")
            print(f"Version: {result.get('version', 'N/A')}")
            print(f"Endpoints: {len(result.get('endpoints', {}))}")
        else:
            print(f"❌ API Documentation Test Failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API Documentation: {e}")

def main():
    """Run all API tests"""
    print("🚀 Starting Kundli API Tests...")
    print("=" * 50)
    
    test_api_docs()
    test_planets_only()
    test_lagna_only()
    test_basic_kundli()
    test_comprehensive_kundli()
    
    print("\n" + "=" * 50)
    print("🏁 All tests completed!")

if __name__ == "__main__":
    main() 