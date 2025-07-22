# Vedic Astrology Dosha Detection System

## Overview

A comprehensive Vedic astrology dosha detection system that analyzes kundli (birth chart) data to identify various astrological afflictions (doshas) and provides detailed information about their causes, effects, and remedies.

## Features

### 🔍 **25+ Dosha Types Detected**

#### **Major Doshas**
- **Mangal Dosha (Kuja Dosha)** - Mars in specific houses
- **Kaal Sarp Dosha** - All planets between Rahu and Ketu
- **Guru Chandal Dosha** - Jupiter and Rahu conjunction
- **Sade Sati** - Saturn's 7.5-year period over Moon
- **Pitra Dosha** - Ancestral/father-related issues
- **Shrapit Dosha** - Curses and black magic effects

#### **Compatibility Doshas**
- **Nadi Dosha** - Nakshatra compatibility issues
- **Gana Dosha** - Temperament compatibility problems
- **Bhakoot Dosha** - Moon sign compatibility issues

#### **Family & Ancestral Doshas**
- **Matri Dosha** - Mother-related issues
- **Enhanced Pitra Dosha** - Multiple ancestral factors
- **Pret Dosha** - Ghost/spirit related issues
- **Tara Dosha** - Star-related problems
- **Mrityu Dosha** - Death-related issues
- **Kalatra Dosha** - Spouse-related problems

#### **Planetary Doshas**
- **Saturn Dosha** - Saturn-related afflictions
- **Rahu Dosha** - Rahu-related issues
- **Ketu Dosha** - Ketu-related problems
- **Sun Dosha** - Sun-related afflictions
- **Mars Dosha** - Mars-related issues
- **Mercury Dosha** - Mercury-related problems

#### **House-based Doshas**
- **8th House Dosha** - Death and obstacles
- **12th House Dosha** - Losses and expenses
- **6th House Dosha** - Enemies and diseases

#### **Special Doshas**
- **Sarpa Dosha** - Snake-related issues
- **Grahan Dosha** - Eclipse-related problems
- **Kemadruma Dosha** - Moon without adjacent planets

#### **Modern Doshas**
- **Career Dosha** - Professional problems
- **Health Dosha** - Health-related issues
- **Wealth Dosha** - Financial problems
- **Education Dosha** - Learning difficulties
- **Travel Dosha** - Travel-related issues
- **Legal Dosha** - Legal problems

### 📊 **Severity Levels**
- **Mild** - Yellow indicator, minimal impact
- **Moderate** - Orange indicator, moderate impact
- **Severe** - Red indicator, significant impact

### 🎯 **Detailed Information**
Each detected dosha includes:
- **Name** - Traditional Sanskrit name
- **Type** - Category classification
- **Description** - Astrological cause
- **Effects** - Life impact areas
- **Remedies** - Traditional solutions
- **Severity** - Impact level

## Technical Implementation

### Core Files

#### **`dosha_utils.py`**
Utility functions for dosha calculations:
- Planet strength analysis (exalted, debilitated, own sign)
- Aspect calculations (drishti)
- House relationship analysis
- Nakshatra calculations
- Severity assessment functions

#### **`dosha_rules.py`**
Main dosha detection logic:
- `detect_all_doshas(kundli)` - Main detection function
- Individual dosha detection functions
- Comprehensive rule-based analysis
- Error handling and fallbacks

#### **`dosha_list.json`**
Reference database containing:
- Dosha definitions and causes
- Traditional effects and impacts
- Recommended remedies and solutions
- Severity level guidelines
- Gemstone recommendations

### Flask Integration

#### **`app.py`**
- Integrated dosha detection into `/api/kundli` endpoint
- Added dosha data to JSON response
- Error handling for deployment environments

#### **`templates/kundli.html`**
- Added dosha display section
- Grouped by type with color-coded severity
- Professional UI with effects and remedies
- Responsive design for all devices

## Usage

### API Response Format
```json
{
  "planets": {...},
  "lagna": {...},
  "bhavas": [...],
  "yogas": [...],
  "doshas": [
    {
      "name": "Mangal Dosha (Kuja Dosha)",
      "type": "Major Dosha",
      "description": "Mars in 7th house",
      "severity": "Severe",
      "effects": "Marriage delays, relationship issues, anger problems",
      "remedies": "Wear red coral, perform Mangal puja, fast on Tuesdays"
    }
  ]
}
```

### Testing
```bash
python test_dosha.py
```

## Astrological Accuracy

### **Classical Rules Implemented**
- **Mangal Dosha**: Mars in houses 1, 2, 4, 7, 8, 12
- **Kaal Sarp**: All planets between Rahu-Ketu axis
- **Sade Sati**: Saturn over Moon sign ±1 house
- **Pitra Dosha**: Malefics in 9th house (father's house)
- **Guru Chandal**: Jupiter-Rahu conjunction
- **House Doshas**: Malefics in specific houses

### **Strength Considerations**
- **Exalted planets** - Reduced dosha severity
- **Debilitated planets** - Increased dosha severity
- **Own sign planets** - Moderate severity
- **House positions** - Location-based severity

### **Aspect Analysis**
- **7th aspect** - Opposition effects
- **4th/8th aspects** - Square relationships
- **5th/9th aspects** - Trine relationships
- **3rd/10th aspects** - Sextile relationships

## Frontend Display

### **Visual Features**
- **Color-coded severity** (Red/Orange/Yellow)
- **Grouped by type** for easy navigation
- **Detailed information** with effects and remedies
- **Responsive design** for mobile and desktop
- **Professional styling** with cards and shadows

### **User Experience**
- **Clear categorization** of dosha types
- **Immediate severity indication** through colors
- **Comprehensive information** for each dosha
- **Actionable remedies** for users
- **Easy navigation** through different dosha categories

## Deployment

### **Render Compatibility**
- Error handling for import failures
- Fallback functions for deployment environments
- Graceful degradation if modules unavailable
- Production-ready error management

### **Performance**
- Efficient detection algorithms
- Minimal computational overhead
- Fast response times
- Scalable architecture

## Future Enhancements

### **Planned Features**
- **Dosha strength scoring** (0-100 scale)
- **Remedial period calculations** (when doshas end)
- **Compatibility analysis** for marriage matching
- **Transit dosha detection** (current planetary positions)
- **Personalized remedy recommendations**

### **Advanced Analysis**
- **Dasha-specific dosha effects**
- **Combined dosha interactions**
- **Temporal dosha variations**
- **Regional astrological variations**

## Contributing

### **Adding New Doshas**
1. Add detection logic to `dosha_rules.py`
2. Update `dosha_list.json` with reference data
3. Test with `test_dosha.py`
4. Update documentation

### **Improving Accuracy**
- Review classical texts for rule validation
- Add regional astrological variations
- Implement advanced strength calculations
- Enhance aspect analysis

## License

This dosha detection system is part of the Panchangam web application and follows the same licensing terms.

---

**Note**: This system provides astrological analysis based on classical Vedic astrology principles. Users should consult qualified astrologers for personalized guidance and interpretation. 