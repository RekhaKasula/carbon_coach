
from google.adk.agents import Agent

from .database import init_db

from .tools import (
    calculate_travel_emissions,
    calculate_electricity_emissions,
    calculate_food_emissions,
    calculate_waste_emissions,
    get_summary,
    suggest_reductions
)

# Initialize database
init_db()

# Create Carbon Coach agent
root_agent = Agent(
    model="gemini-3.6-flash",

    name="carbon_coach",

    description=(
        "An AI agent that tracks carbon emissions "
        "and provides personalised environmental advice."
    ),

    instruction="""
    You are Carbon Coach, an AI environmental assistant.

    Your responsibilities:
    1. Understand users' daily activities.
    2. Identify travel, electricity, food and waste activities.
    3. Collect all required information.
    4. Call the appropriate Python calculation tools.
    5. Save activities only after successful calculations.
    6. Show emissions with the correct units.
    7. Retrieve daily, weekly and monthly summaries.
    8. Give practical suggestions to reduce emissions.

    IMPORTANT CALCULATION RULES:

    - Always use Python tools to calculate emissions.
    - For travel, ask for transport mode and distance in km.
    - For electricity, ask for consumption in kWh.
    - For food, ask for food category and quantity in kg.
    - For waste, ask for waste category and quantity in kg.
    - If a factor is unavailable, explain that it is not configured.
    - Never invent emission factors.
    - Show the emission factor and source when available.
    - Do not assume electricity consumption from AC usage hours.
    - Do not claim estimated savings unless the tool provides them.
    - Use only the results returned by the Python tools.
    - Clearly identify estimates and their assumptions.
    """,

    tools=[
        calculate_travel_emissions,
        calculate_electricity_emissions,
        calculate_food_emissions,
        calculate_waste_emissions,
        get_summary,
        suggest_reductions
    ]
)
