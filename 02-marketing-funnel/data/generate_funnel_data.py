"""
Generates synthetic marketing funnel and revenue pipeline data.
Outputs: funnel_leads.csv, funnel_monthly.csv
"""

import csv
import random
from datetime import date, timedelta

random.seed(7)

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)

SOURCES = ["Organic Search", "Paid Search", "Social Media", "Referral", "Email Campaign"]
STAGES = ["Lead", "MQL", "SQL", "Proposal", "Closed Won", "Closed Lost"]
INDUSTRIES = ["SaaS", "Healthcare", "E-commerce", "Finance", "Agency"]

STAGE_CONVERSION = {
    "Lead":       0.40,
    "MQL":        0.50,
    "SQL":        0.55,
    "Proposal":   0.45,
    "Closed Won": None,
}

STAGE_DAYS = {
    "Lead":     (3, 10),
    "MQL":      (5, 15),
    "SQL":      (7, 21),
    "Proposal": (5, 14),
}

CAC_BY_SOURCE = {
    "Organic Search":  random.uniform(180, 240),
    "Paid Search":     random.uniform(320, 420),
    "Social Media":    random.uniform(250, 350),
    "Referral":        random.uniform(100, 160),
    "Email Campaign":  random.uniform(140, 200),
}

MRR_BY_INDUSTRY = {
    "SaaS":       random.uniform(800, 2400),
    "Healthcare":  random.uniform(1200, 3200),
    "E-commerce":  random.uniform(600, 1600),
    "Finance":     random.uniform(1400, 3600),
    "Agency":      random.uniform(700, 1800),
}

leads = []
lead_id = 1
current = START_DATE

while current <= END_DATE:
    month_multiplier = 1 + (current.month - 1) * 0.03
    daily_leads = int(random.gauss(6, 1.5) * month_multiplier)
    daily_leads = max(1, daily_leads)

    for _ in range(daily_leads):
        source = random.choice(SOURCES)
        industry = random.choice(INDUSTRIES)
        entry_date = current
        stage = "Lead"
        final_stage = "Lead"
        close_date = None
        mrr = 0
        days_in_funnel = 0

        for s in STAGES[:-2]:
            rate = STAGE_CONVERSION[s]
            if random.random() < rate:
                days_in_funnel += random.randint(*STAGE_DAYS[s])
                next_idx = STAGES.index(s) + 1
                final_stage = STAGES[next_idx]
            else:
                final_stage = "Closed Lost"
                days_in_funnel += random.randint(*STAGE_DAYS[s])
                break

        if final_stage == "Closed Won":
            close_date = entry_date + timedelta(days=days_in_funnel)
            if close_date > END_DATE:
                close_date = END_DATE
            mrr = round(MRR_BY_INDUSTRY[industry] * random.uniform(0.85, 1.15), 2)

        cac = round(CAC_BY_SOURCE[source] * random.uniform(0.9, 1.1), 2)

        leads.append({
            "lead_id": lead_id,
            "entry_date": entry_date.isoformat(),
            "month": entry_date.strftime("%B"),
            "month_num": entry_date.month,
            "source": source,
            "industry": industry,
            "final_stage": final_stage,
            "days_in_funnel": days_in_funnel,
            "close_date": close_date.isoformat() if close_date else "",
            "mrr": mrr,
            "cac": cac,
            "is_won": 1 if final_stage == "Closed Won" else 0,
            "is_lost": 1 if final_stage == "Closed Lost" else 0,
        })
        lead_id += 1

    current += timedelta(days=1)

# Monthly summary
monthly = {}
for row in leads:
    key = (row["month_num"], row["month"])
    if key not in monthly:
        monthly[key] = {"month_num": key[0], "month": key[1],
                        "new_leads": 0, "won": 0, "lost": 0, "mrr": 0}
    monthly[key]["new_leads"] += 1
    if row["is_won"]:
        monthly[key]["won"] += 1
        monthly[key]["mrr"] += row["mrr"]
    elif row["is_lost"]:
        monthly[key]["lost"] += 1

monthly_rows = []
cumulative_mrr = 0
for key in sorted(monthly):
    m = monthly[key]
    cumulative_mrr += m["mrr"]
    monthly_rows.append({
        "month_num": m["month_num"],
        "month": m["month"],
        "new_leads": m["new_leads"],
        "won": m["won"],
        "lost": m["lost"],
        "new_mrr": round(m["mrr"], 2),
        "cumulative_mrr": round(cumulative_mrr, 2),
        "win_rate": round(m["won"] / m["new_leads"], 4) if m["new_leads"] else 0,
    })

base = r"c:\Users\Administrator\Documents\Marcus\Portfolio\powerbi-dashboards\02-marketing-funnel\data"

with open(f"{base}\\funnel_leads.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=leads[0].keys())
    writer.writeheader()
    writer.writerows(leads)

with open(f"{base}\\funnel_monthly.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=monthly_rows[0].keys())
    writer.writeheader()
    writer.writerows(monthly_rows)

print(f"Generated {len(leads)} leads and {len(monthly_rows)} monthly rows")
