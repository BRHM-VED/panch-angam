# Kundli and Dosha Detection API

A clean, simple Flask API for astrological calculations including kundli generation and dosha detection.

## Features

- **Kundli Generation**: Calculate planetary positions and house placements
- **Dosha Detection**: Detect various astrological doshas
- **Simple API**: Clean, minimal Flask application
- **Swiss Ephemeris**: Accurate astronomical calculations

## Endpoints

### Health Check
```
GET /health
```

### Kundli Generation
```
POST /kundli
```
**Input:**
```json
{
  "date": "1990-05-15",
  "time": "14:30",
  "lat": 19.0760,
  "lon": 72.8777,
  "tz": 5.5
}
```

### Dosha Detection
```
POST /dosha-detection
```
**Input:** Same as kundli endpoint

## Doshas Detected

1. **Sade Sati**: Saturn in 12th, 1st, or 2nd house from Moon
2. **Pitra Dosha**: Rahu in 9th house
3. **Kaal Sarp Dosha**: All planets between Rahu and Ketu
4. **Wealth Dosha**: Malefic planets in 2nd or 11th house

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
python app.py
```

## Deployment

This app is designed for simple deployment on platforms like Render.com.

## Dependencies

- Flask==3.1.1
- pyswisseph==2.10.3.2
- pytz==2025.2
- gunicorn==22.0.0
