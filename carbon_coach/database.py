
import sqlite3
from datetime import date, timedelta

DB_NAME = "carbon_activities.db"


# Create the database and table
def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            activity TEXT,
            quantity REAL,
            unit TEXT,
            emission_factor REAL,
            emissions REAL,
            source TEXT,
            activity_date TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save an activity
def save_activity(category, activity, quantity, unit,
                  factor, emissions, source):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO activities
        (category, activity, quantity, unit,
         emission_factor, emissions, source, activity_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        category, activity, quantity, unit,
        factor, emissions, source, date.today().isoformat()
    ))

    conn.commit()
    conn.close()


# Get activities for a particular period
def get_activities(period="week"):

    today = date.today()

    if period == "today":
        start = today
    elif period == "week":
        start = today - timedelta(days=6)
    elif period == "month":
        start = today - timedelta(days=29)
    else:
        return {"error": "Use today, week or month"}

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT category, activity, quantity, unit,
               emissions, activity_date
        FROM activities
        WHERE activity_date BETWEEN ? AND ?
        ORDER BY activity_date
    """, (start.isoformat(), today.isoformat())).fetchall()

    conn.close()

    records = [dict(row) for row in rows]

    total = sum(row["emissions"] for row in records)

    return {
        "period": period,
        "total_emissions_kg": round(total, 3),
        "activity_count": len(records),
        "records": records
    }
