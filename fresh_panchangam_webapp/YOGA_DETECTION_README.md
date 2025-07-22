# Vedic Astrology Yoga Detection System

## Overview

This comprehensive yoga detection system analyzes Vedic astrology kundli (birth chart) data to identify over 100 different yogas (astrological combinations) that influence various aspects of life including wealth, education, career, relationships, and spirituality.

## Features

### 🎯 **Comprehensive Yoga Detection**
- **100+ Yogas** covering all major categories
- **Real-time Analysis** of planetary positions
- **Strength Assessment** for each detected yoga
- **Categorized Results** by yoga type

### 📊 **Yoga Categories**

#### **Raj Yogas (Royal Combinations)**
- Raja Yoga - Benefic planets in angular houses
- Mahapurusha Yoga - Exalted planets in kendras
- Parivartana Yoga - Exchange of signs between planets
- Kesari Yoga - Jupiter in angular houses
- Sankha Yoga - Venus in angular houses

#### **Dhan Yogas (Wealth Combinations)**
- Dhana Yoga - Jupiter/Venus in wealth houses
- Lakshmi Yoga - Venus in specific houses
- Kubera Yoga - Jupiter in 11th house
- Vasumati Yoga - Venus in 2nd house

#### **Vidya Yogas (Education & Knowledge)**
- Vidya Yoga - Mercury/Jupiter in education houses
- Saraswati Yoga - Exalted Mercury
- Budh-Aditya Yoga - Mercury-Sun conjunction
- Guru-Chandal Yoga - Jupiter-Rahu combination

#### **Ayush Yogas (Health & Longevity)**
- Ayushkar Yoga - Jupiter in 8th house
- Amrit Yoga - Exalted Moon in kendras

#### **Vivah Yogas (Marriage & Relationships)**
- Vivah Yoga - Venus in 7th house
- Kalatra Yoga - 7th lord in 7th house

#### **Karma Yogas (Career & Profession)**
- Karma Yoga - 10th lord in 10th house

#### **Dosha Yogas (Afflictions)**
- Kaal Sarp Yoga - All planets between Rahu-Ketu
- Mangal Dosha - Mars in specific houses

#### **Special Yogas**
- Panch Mahapurush Yoga - Multiple exalted planets
- Sarvatobhadra Yoga - Planets in all directions
- Akhand Samrajya Yoga - All planets in one half

#### **Modern Yogas**
- Technology Yoga - Mercury-Uranus combination
- Medicine Yoga - Mercury-Neptune combination
- Foreign Education Yoga - Mercury-Rahu combination

## Technical Implementation

### **Core Files**

#### `yoga_utils.py`
Contains utility functions for astrological calculations:
- Sign lords and planetary relationships
- Exaltation and debilitation checks
- Aspect calculations
- Planetary strength assessment

#### `yoga_rules.py`
Contains all yoga detection functions:
- Individual yoga detection logic
- `detect_all_yogas()` main function
- Over 100 yoga detection algorithms

### **Integration with Flask App**

The yoga detection system is integrated into the main Flask application:

```python
from yoga_rules import detect_all_yogas

@app.route('/api/kundli', methods=['POST'])
def generate_kundli():
    # ... kundli calculation logic ...
    
    # Detect yogas in the kundli
    detected_yogas = detect_all_yogas(planet_positions, bhavas, lagna)
    
    return jsonify({
        'planets': planet_positions,
        'lagna': lagna,
        'bhavas': bhavas,
        'yogas': detected_yogas  # Added yoga data
    })
```

### **Frontend Display**

The detected yogas are displayed in the Kundli interface:
- **Grouped by Type** - Raj, Dhan, Vidya, etc.
- **Strength Indicators** - Color-coded by strength level
- **Detailed Descriptions** - Explanation of each yoga
- **Visual Cards** - Clean, organized presentation

## Usage

### **API Response Format**

```json
{
  "planets": { ... },
  "lagna": { ... },
  "bhavas": [ ... ],
  "yogas": [
    {
      "name": "Raja Yoga",
      "type": "Raj Yoga",
      "description": "Venus in 7th house (Kendra)",
      "strength": "Strong"
    },
    {
      "name": "Sun Mahapurusha Yoga",
      "type": "Raj Yoga", 
      "description": "Sun exalted in 1st house",
      "strength": "Very Strong"
    }
  ]
}
```

### **Strength Levels**

- **Very Strong** - Deep green (#006400)
- **Strong** - Green (#228B22)  
- **Moderate** - Orange (#FF8C00)
- **Weak** - Red (#FF4500)
- **Affliction** - Red for doshas

## Testing

Run the test script to verify the system:

```bash
python test_yoga.py
```

This will test the yoga detection with sample data and display detected yogas grouped by category.

## Astrological Accuracy

The system implements traditional Vedic astrology principles:

### **Planetary Relationships**
- **Friendly Planets**: Sun-Mars, Moon-Venus, etc.
- **Enemy Planets**: Sun-Venus, Moon-Mars, etc.
- **Neutral Planets**: Based on traditional texts

### **House System**
- **Kendras (Angular)**: 1, 4, 7, 10 - Most powerful
- **Trikonas (Trine)**: 1, 5, 9 - Benefic houses
- **Dusthanas (Difficult)**: 6, 8, 12 - Challenging houses

### **Planetary Strength**
- **Exaltation**: Maximum strength
- **Own Sign**: Strong position
- **Debilitation**: Weak position
- **Neutral**: Standard strength

## Future Enhancements

1. **Nakshatra-based Yogas** - Add nakshatra-specific combinations
2. **Dasha Analysis** - Period-based yoga activation
3. **Remedial Measures** - Suggest remedies for doshas
4. **Predictive Analytics** - Time-based yoga effects
5. **Advanced Combinations** - Complex multi-planet yogas

## Contributing

To add new yogas:

1. Add detection function in `yoga_rules.py`
2. Include in `detect_all_yogas()` function list
3. Test with sample data
4. Update documentation

## License

This yoga detection system is part of the Panchangam project and follows Vedic astrology traditions and principles. 