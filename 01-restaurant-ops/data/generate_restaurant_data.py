"""
Generates synthetic restaurant operations data for the Power BI portfolio dashboard.
Outputs: restaurant_ops.csv
"""

import csv
import random
from datetime import date, timedelta

random.seed(42)

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)
SEATS = 60

# Weekday multipliers (Mon=0 ... Sun=6)
DAY_MULTIPLIERS = {0: 0.65, 1: 0.70, 2: 0.75, 3: 0.80, 4: 0.95, 5: 1.30, 6: 1.20}

# Sort order: Sun=1 ... Sat=7 (US convention)
DAY_SORT = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}

# Monthly seasonality
MONTH_MULTIPLIERS = {1: 0.80, 2: 0.82, 3: 0.90, 4: 0.95, 5: 1.00,
                     6: 1.05, 7: 1.10, 8: 1.08, 9: 1.00, 10: 0.98,
                     11: 1.05, 12: 1.20}

rows = []
current = START_DATE
while current <= END_DATE:
    dow = current.weekday()
    month = current.month
    multiplier = DAY_MULTIPLIERS[dow] * MONTH_MULTIPLIERS[month]

    base_covers = 90
    covers = max(10, int(base_covers * multiplier + random.gauss(0, 6)))

    avg_check = round(random.uniform(48, 62), 2)
    revenue = round(covers * avg_check, 2)

    food_revenue = round(revenue * random.uniform(0.66, 0.72), 2)
    bev_revenue = round(revenue - food_revenue, 2)

    food_cost_pct = round(random.uniform(0.27, 0.33), 4)
    bev_cost_pct = round(random.uniform(0.19, 0.25), 4)
    food_cost = round(food_revenue * food_cost_pct, 2)
    bev_cost = round(bev_revenue * bev_cost_pct, 2)
    total_cogs = round(food_cost + bev_cost, 2)
    cogs_pct = round(total_cogs / revenue, 4)

    labor_hours = round(covers * random.uniform(0.30, 0.38), 1)
    labor_cost = round(labor_hours * random.uniform(16, 19), 2)
    labor_pct = round(labor_cost / revenue, 4)

    table_turns = round(covers / SEATS, 2)
    rev_per_cover = round(revenue / covers, 2)

    rows.append({
        "date": current.isoformat(),
        "day_of_week": current.strftime("%A"),
        "day_sort": DAY_SORT[dow],
        "month": current.strftime("%B"),
        "week": current.isocalendar()[1],
        "covers": covers,
        "revenue": revenue,
        "food_revenue": food_revenue,
        "beverage_revenue": bev_revenue,
        "food_cost": food_cost,
        "beverage_cost": bev_cost,
        "total_cogs": total_cogs,
        "cogs_pct": cogs_pct,
        "labor_hours": labor_hours,
        "labor_cost": labor_cost,
        "labor_pct": labor_pct,
        "table_turns": table_turns,
        "revenue_per_cover": rev_per_cover,
        "seats": SEATS,
    })
    current += timedelta(days=1)

output_path = r"c:\Users\Administrator\Documents\Marcus\Portfolio\dashboards\data\restaurant_ops.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> {output_path}")
