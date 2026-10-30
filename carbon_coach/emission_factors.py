EMISSION_FACTORS = {

    # 1. Electricity
    "electricity": {
        "grid": {
            "value": 0.675,
            "unit": "kg CO2/kWh",
            "source": "Central Electricity Authority (CEA)",
            "reference_year": "2025-26"
        }
    },
    "travel": {
    "bike": {
        "value": 0.1609,
        "unit": "kg CO2e/passenger-km",
        "source": "IIT Madras and TNPCB, Reducing Emissions by Mass Transport",
        "reference_year": "2023"
    },
    "car": {
        "value": 0.3591,
        "unit": "kg CO2e/passenger-km",
        "source": "IIT Madras and TNPCB, Reducing Emissions by Mass Transport",
        "reference_year": "2023"
    },
    "bus": {
        "value": 0.0315,
        "unit": "kg CO2e/passenger-km",
        "source": "IIT Madras and TNPCB, Reducing Emissions by Mass Transport",
        "reference_year": "2023"
    }
},

    # 3. Food
    "food": {
        "vegetarian": {
            "value": None,
            "unit": "kg CO2e/kg",
            "source": None,
            "reference_year": None
        },
        "chicken": {
            "value": None,
            "unit": "kg CO2e/kg",
            "source": None,
            "reference_year": None
        }
    },

    # 4. Waste
    "waste": {
        "mixed": {
            "value": None,
            "unit": "kg CO2e/kg",
            "source": None,
            "reference_year": None
        },
        "paper": {
            "value": None,
            "unit": "kg CO2e/kg",
            "source": None,
            "reference_year": None
        }
    }
}