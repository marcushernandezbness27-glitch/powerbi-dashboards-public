# Dashboard 3 — Stellapura Payroll Analytics

Operational analytics dashboard for a real-money weekly commission payroll system. Data sourced live from BigQuery via the Stellapura edge payroll engine.

## Pages

| Page | Purpose |
|---|---|
| Payroll Overview | Headline KPIs + disbursed trend + payroll run history table |
| Commission Detail | Payment success rate + net pay vs holdback + earnings by agent + status breakdown |
| Payroll Timeline | Monthly disbursed + agents per run + engine version history + holdback trend |

## Key metrics

| Metric | Definition |
|---|---|
| **Total Payroll Runs** | Distinct submitted payroll cycles |
| **Total Disbursed** | Sum of paid agent commissions (USD) |
| **Total Holdback** | Sum of withheld amounts across all runs (USD) |
| **Avg Payout Per Run** | Total disbursed / total payroll runs |
| **Payment Success Rate** | Paid commissions / total commission records |

## DAX measures

```dax
Total Payroll Runs    = CALCULATE(DISTINCTCOUNT(payroll_runs[payroll_id]), payroll_runs[status] = "submitted")
Total Disbursed       = DIVIDE(CALCULATE(SUM(agent_commissions[amount_cents]), agent_commissions[status] = "paid"), 100)
Total Holdback        = DIVIDE(SUM(agent_commissions[holdback_new_cents]), 100)
Active Agents         = DISTINCTCOUNT(agent_commissions[external_agent_id])
Payment Success Rate  = DIVIDE(CALCULATE(COUNT(agent_commissions[status]), agent_commissions[status] = "paid"), COUNT(agent_commissions[status]))
Avg Payout Per Run    = DIVIDE([Total Disbursed], [Total Payroll Runs])
```

## Data source

Live BigQuery connection to `stellapura_analytics` dataset (GCP project `rare-scout-457011-m7`):

- `payroll_runs` — one row per status transition per payroll cycle (calculated → submitted)
- `agent_commissions` — one row per agent per payroll run with amount, holdback, and payment status

The `agent_commissions` table records both the net pay (`amount_cents`) and the withheld portion (`holdback_new_cents`) — a mechanism used to hold back a portion of new-agent commissions until service confirmation.

## Files

```
03-stellapura-ops/
  Stellapura_Payroll.pbix     Power BI report (BigQuery connection)
  screenshots/
    payroll-overview.png
    commission-detail.png
    payroll-timeline.png
```
