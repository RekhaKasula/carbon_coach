
from .emission_factors import EMISSION_FACTORS
from .database import save_activity, get_activities


def calculate_travel_emissions(mode: str, km: float) -> dict:
    mode = mode.lower()

    if mode not in EMISSION_FACTORS["travel"]:
        return {"error": "Choose bus, car or bike."}

    factor_data = EMISSION_FACTORS["travel"][mode]
    factor = factor_data["value"]

    if factor is None:
        return {"error": f"No verified emission factor available for {mode}."}

    emissions = km * factor

    save_activity(
        "travel", mode, km, "passenger-km",
        factor, emissions, factor_data["source"]
    )

    return {
        "category": "travel",
        "activity": mode,
        "distance_passenger_km": km,
        "emissions_kg_co2e": round(emissions, 3),
        "factor": factor,
        "unit": factor_data["unit"],
        "source": factor_data["source"]
    }


def calculate_electricity_emissions(kwh: float) -> dict:
    factor_data = EMISSION_FACTORS["electricity"]["grid"]
    factor = factor_data["value"]

    if factor is None:
        return {"error": "Electricity emission factor is unavailable."}

    emissions = kwh * factor

    save_activity(
        "electricity", "grid", kwh, "kWh",
        factor, emissions, factor_data["source"]
    )

    return {
        "category": "electricity",
        "consumption_kwh": kwh,
        "emissions_kg_co2": round(emissions, 3),
        "factor": factor,
        "unit": factor_data["unit"],
        "source": factor_data["source"],
        "reference_year": factor_data["reference_year"]
    }


def calculate_food_emissions(
    meal_type: str, quantity_kg: float
) -> dict:
    meal_type = meal_type.lower()

    if meal_type not in EMISSION_FACTORS["food"]:
        return {"error": "Choose a supported food category."}

    factor_data = EMISSION_FACTORS["food"][meal_type]
    factor = factor_data["value"]

    if factor is None:
        return {
            "error": f"No verified emission factor available for {meal_type}."
        }

    emissions = quantity_kg * factor

    save_activity(
        "food", meal_type, quantity_kg, "kg",
        factor, emissions, factor_data["source"]
    )

    return {
        "category": "food",
        "food_type": meal_type,
        "quantity_kg": quantity_kg,
        "emissions_kg_co2e": round(emissions, 3),
        "factor": factor,
        "source": factor_data["source"]
    }


def calculate_waste_emissions(
    waste_type: str, kg: float
) -> dict:
    waste_type = waste_type.lower()

    if waste_type not in EMISSION_FACTORS["waste"]:
        return {"error": "Choose a supported waste category."}

    factor_data = EMISSION_FACTORS["waste"][waste_type]
    factor = factor_data["value"]

    if factor is None:
        return {
            "error": f"No verified emission factor available for {waste_type}."
        }

    emissions = kg * factor

    save_activity(
        "waste", waste_type, kg, "kg",
        factor, emissions, factor_data["source"]
    )

    return {
        "category": "waste",
        "waste_type": waste_type,
        "quantity_kg": kg,
        "emissions_kg_co2e": round(emissions, 3),
        "factor": factor,
        "source": factor_data["source"]
    }


def get_summary(period: str = "week") -> dict:
    return get_activities(period)


def suggest_reductions() -> dict:
    summary = get_activities("week")

    if "error" in summary:
        return summary

    tips = []

    car_factor = EMISSION_FACTORS["travel"]["car"]["value"]
    bus_factor = EMISSION_FACTORS["travel"]["bus"]["value"]

    if car_factor is not None and bus_factor is not None:
        for record in summary["records"]:
            if (
                record["category"] == "travel"
                and record["activity"] == "car"
            ):
                saving = (
                    car_factor - bus_factor
                ) * record["quantity"]

                if saving > 0:
                    tips.append({
                        "suggestion": (
                            "Consider taking a bus instead of a car "
                            "for this distance, if practical."
                        ),
                        "estimated_saving_kg_co2e": round(saving, 3),
                        "basis": (
                            "Estimated comparison using the same "
                            "passenger-kilometres and the configured factors."
                        )
                    })

    return {
        "period": "week",
        "suggestions": tips
    }
