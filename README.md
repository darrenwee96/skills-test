# Databricks Sizing — Mooncake (Azure China)

Azure China (Mooncake) Databricks cost estimation using the Lakemeter Mooncake API. Calculates monthly costs for customer workloads across Jobs, DBSQL, DLT, Lakebase, Model Serving, Apps, Vector Search, and more — all with Mooncake-specific DBU rates and instance types.

## How to Invoke

### Slash Command

```
/sizing-mooncake
```

### Example Prompts

```
"Size a Lakebase instance in China North 3: 4 CU, 500GB storage, Premium"
"Get Mooncake pricing for DBSQL Serverless: Medium warehouse, 8 hours/day"
"Cost estimate for Azure China: Jobs Classic with 4 workers on Standard_D16s_v5"
```

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Workspace Auth | Run `/databricks-authentication` and authenticate with the `fevm-darren` profile |
| Python 3.10+ | Required for the API helper script |

## What This Skill Does

1. Authenticates with the Lakemeter Mooncake app workspace
2. Calls the Lakemeter Mooncake API with Mooncake-specific pricing
3. Returns a cost breakdown with DBU estimates, VM costs (for classic), and totals in USD + CNY

## Key Resources

| File | Description |
|------|-------------|
| `resources/lakemeter_mooncake_api.py` | Python helper script for API calls |

## Related Skills

- `/databricks-sizing` — Standard Lakemeter for AWS, Azure (global), GCP
- `/databricks-authentication` — Required for workspace authentication before sizing
