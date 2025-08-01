# Kundli API Documentation

## Overview

The Kundli API provides comprehensive Vedic astrology calculations including planet positions, Lagna (Ascendant), house calculations, yoga detection, dosha analysis, and detailed astrological insights.

**Base URL**: `https://panch-angam-xmmn.onrender.com`

## Endpoints

### 1. Basic Kundli Generation

**Endpoint**: `POST /api/kundli/basic`

**Description**: Generate basic Kundli with planet positions and Lagna

**Request Body**:
```json
{
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "lat": float,
    "lon": float,
    "tz": float,
    "name": "string (optional)",
    "gender": "string (optional)"
}
```

**Example Request**:
```json
{
    "date": "1990-05-15",
    "time": "14:30",
    "lat": 19.0760,
    "lon": 72.8777,
    "tz": 5.5,
    "name": "John Doe",
    "gender": "Male"
}
```

**Response**:
```json
{
    "status": "success",
    "input": {
        "date": "1990-05-15",
        "time": "14:30",
        "lat": 19.0760,
        "lon": 72.8777,
        "tz": 5.5,
        "name": "John Doe",
        "gender": "Male"
    },
    "planets": {
        "Sun": {
            "longitude": 123.45,
            "degree": 3.45,
            "sign": "Simha (Leo)",
            "sign_number": 5,
            "navamsha_sign": "Mesha (Aries)",
            "navamsha_sign_number": 1,
            "house": 3
        },
        "Moon": {
            "longitude": 234.56,
            "degree": 24.56,
            "sign": "Kanya (Virgo)",
            "sign_number": 6,
            "navamsha_sign": "Vrishabha (Taurus)",
            "navamsha_sign_number": 2,
            "house": 4
        }
        // ... other planets
    },
    "lagna": {
        "longitude": 156.78,
        "degree": 6.78,
        "sign": "Kanya (Virgo)",
        "sign_number": 6
    },
    "houses": [
        {
            "house_number": 1,
            "longitude": 156.78,
            "degree": 6.78,
            "sign": "Kanya (Virgo)",
            "sign_number": 6
        }
        // ... other houses
    ],
    "julian_day": 2448034.1041666665
}
```

### 2. Comprehensive Kundli Generation

**Endpoint**: `POST /api/kundli/comprehensive`

**Description**: Generate comprehensive Kundli with all astrological details including yogas, doshas, and detailed analysis

**Request Body**: Same as basic kundli

**Response**:
```json
{
    "status": "success",
    "input": { /* same as basic */ },
    "planets": { /* same as basic */ },
    "lagna": { /* same as basic */ },
    "houses": [ /* same as basic */ ],
    "tithi": 15,
    "nakshatra": 8,
    "yogas": [
        {
            "name": "Gajakesari Yoga",
            "description": "Jupiter in Kendra from Moon",
            "strength": "Strong"
        }
    ],
    "doshas": [
        {
            "name": "Mangal Dosha",
            "description": "Mars in 1st, 4th, 7th, 8th, or 12th house",
            "severity": "Medium"
        }
    ],
    "comprehensive_details": {
        "basic_details": {
            "name": "John Doe",
            "gender": "Male",
            "date_of_birth": "15 May 1990",
            "time_of_birth": "02:30 PM",
            "timezone": "+5.5",
            "moon_sign": "Kanya (Virgo)",
            "ascendant": "Kanya (Virgo)",
            "sun_sign_western": "Simha (Leo)",
            "place_of_birth": "Mumbai",
            "country": "India",
            "longitude_latitude": "72.8777, 19.0760",
            "ayanamsa": "Chitra Paksha = 23Deg. 28Min. 15Sec."
        },
        "astrological_details": {
            "sign_lord": "Mercury",
            "nakshatra_lord": "Sun",
            "charan": 2,
            "name_alphabet": "Ma, Ta | म, ट",
            "nakshatra_charan_alphabet": "मू (Moo)",
            "paya": "Iron",
            "ascendant_lord": "Mercury",
            "atma_karaka": "Mercury",
            "amatya_karaka": "Sun",
            "dasha_system": "Vimshottari, Years = 365.25 Days"
        },
        "panchang_details": {
            "sunrise": "06:00",
            "sunset": "18:00",
            "local_mean_time": "14:30",
            "weekday": "Tuesday",
            "birth_star_nakshatra": "Pushya",
            "tithi_lunar_day": "Purnima",
            "karan": "Bava",
            "nithya_yoga": "Vishkambha"
        },
        "lucky_points": {
            "favourable_days": "Sunday",
            "favourable_color": "Red",
            "lucky_number": "1",
            "inspiring_deity": "Shri Surya Dev",
            "lucky_direction": "East",
            "lucky_letter": "A, L, E",
            "favourable_metal": "Gold"
        }
    },
    "julian_day": 2448034.1041666665
}
```

### 3. Planets Only

**Endpoint**: `POST /api/kundli/planets`

**Description**: Get only planet positions for a given date/time/location

**Request Body**: Same as basic kundli (without name/gender)

**Response**:
```json
{
    "status": "success",
    "planets": {
        "Sun": {
            "longitude": 123.45,
            "degree": 3.45,
            "sign": "Simha (Leo)",
            "sign_number": 5,
            "navamsha_sign": "Mesha (Aries)",
            "navamsha_sign_number": 1
        }
        // ... other planets
    },
    "julian_day": 2448034.1041666665
}
```

### 4. Lagna Only

**Endpoint**: `POST /api/kundli/lagna`

**Description**: Get Lagna (Ascendant) and house positions

**Request Body**: Same as basic kundli (without name/gender)

**Response**:
```json
{
    "status": "success",
    "lagna": {
        "longitude": 156.78,
        "degree": 6.78,
        "sign": "Kanya (Virgo)",
        "sign_number": 6
    },
    "houses": [
        {
            "house_number": 1,
            "longitude": 156.78,
            "degree": 6.78,
            "sign": "Kanya (Virgo)",
            "sign_number": 6
        }
        // ... other houses
    ],
    "julian_day": 2448034.1041666665
}
```

### 5. API Documentation

**Endpoint**: `GET /api/kundli/docs`

**Description**: Get API documentation

**Response**:
```json
{
    "api_name": "Kundli API",
    "version": "1.0.0",
    "description": "Comprehensive Vedic Astrology API for Kundli generation and analysis",
    "endpoints": {
        "/api/kundli/basic": {
            "method": "POST",
            "description": "Generate basic Kundli with planet positions and Lagna",
            "required_fields": ["date", "time", "lat", "lon", "tz"],
            "optional_fields": ["name", "gender"]
        }
        // ... other endpoints
    },
    "date_format": "YYYY-MM-DD",
    "time_format": "HH:MM (24-hour)",
    "coordinates": "Decimal degrees",
    "timezone": "Hours offset from UTC (e.g., 5.5 for IST)"
}
```

## Data Formats

### Date Format
- **Format**: `YYYY-MM-DD`
- **Example**: `1990-05-15`

### Time Format
- **Format**: `HH:MM` (24-hour)
- **Example**: `14:30` (2:30 PM)

### Coordinates
- **Latitude**: Decimal degrees (-90 to 90)
- **Longitude**: Decimal degrees (-180 to 180)
- **Example**: `19.0760, 72.8777` (Mumbai)

### Timezone
- **Format**: Hours offset from UTC
- **Example**: `5.5` for Indian Standard Time (IST)

## Planet Information

The API calculates positions for the following celestial bodies:

1. **Sun** (Surya)
2. **Moon** (Chandra)
3. **Mars** (Mangal)
4. **Mercury** (Budh)
5. **Jupiter** (Guru/Brihaspati)
6. **Venus** (Shukra)
7. **Saturn** (Shani)
8. **Rahu** (Mean Node)
9. **Ketu** (Descending Node)

## Rashi (Zodiac Signs)

1. **Mesha** (Aries)
2. **Vrishabha** (Taurus)
3. **Mithuna** (Gemini)
4. **Karka** (Cancer)
5. **Simha** (Leo)
6. **Kanya** (Virgo)
7. **Tula** (Libra)
8. **Vrischika** (Scorpio)
9. **Dhanu** (Sagittarius)
10. **Makara** (Capricorn)
11. **Kumbha** (Aquarius)
12. **Meena** (Pisces)

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid input)
- **500**: Internal Server Error

Error response format:
```json
{
    "error": "Error description"
}
```

## Usage Examples

### Python
```python
import requests

url = "https://panch-angam-xmmn.onrender.com/api/kundli/basic"
data = {
    "date": "1990-05-15",
    "time": "14:30",
    "lat": 19.0760,
    "lon": 72.8777,
    "tz": 5.5,
    "name": "John Doe",
    "gender": "Male"
}

response = requests.post(url, json=data)
result = response.json()
print(f"Lagna: {result['lagna']['sign']}")
```

### JavaScript
```javascript
const url = "https://panch-angam-xmmn.onrender.com/api/kundli/basic";
const data = {
    date: "1990-05-15",
    time: "14:30",
    lat: 19.0760,
    lon: 72.8777,
    tz: 5.5,
    name: "John Doe",
    gender: "Male"
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    console.log(`Lagna: ${result.lagna.sign}`);
});
```

### cURL
```bash
curl -X POST https://panch-angam-xmmn.onrender.com/api/kundli/basic \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1990-05-15",
    "time": "14:30",
    "lat": 19.0760,
    "lon": 72.8777,
    "tz": 5.5,
    "name": "John Doe",
    "gender": "Male"
  }'
```

## Rate Limiting

Currently, there are no rate limits on the API. However, please use the API responsibly and avoid making excessive requests.

## Support

For issues or questions about the API, please contact the development team or create an issue in the project repository. 