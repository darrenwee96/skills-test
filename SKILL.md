---
name: sizing-mooncake
description: "Get Databricks cost estimates for Azure China (Mooncake) regions using the Lakemeter Mooncake API. Covers Jobs, DBSQL, DLT, Lakebase, Model Serving, Apps, Vector Search, Clean Room, and more. Use when the user asks for cost estimation, pricing, or DBU calculations specifically for Azure Mooncake / Azure China regions."
user-invocable: true
---

# Databricks Sizing — Mooncake (Azure China)

This skill provides Databricks cost estimation for **Azure China (Mooncake)** regions via the Lakemeter Mooncake API. It mirrors the standard Lakemeter API contract but is scoped to Mooncake-specific pricing (DBU rates, instance types, and regions).

**Announce at start:** "I'm using the sizing-mooncake skill to get a Databricks cost estimate for Azure China (Mooncake)."

## When to Use This Skill

- User mentions **Azure China**, **Mooncake**, **21Vianet**, or China regions like **chinanorth3**, **chinaeast2**
- User asks for cost estimation or pricing for workloads running in China
- Use the standard `databricks-sizing` skill for all other clouds (AWS, Azure global, GCP)

## Supported Mooncake Regions

| Region ID | Display Name |
|-----------|-------------|
| chinanorth3 | China North 3 (default) |
| chinaeast2 | China East 2 |
| chinanorth2 | China North 2 |

## Supported Tiers

- **PREMIUM** — All workloads (recommended)
- **STANDARD** — Classic compute only (Jobs, All-Purpose, SQL Classic). **Retiring Oct 1, 2026.**

## Prerequisites

1. **Workspace authentication** — Run `/databricks-authentication` and authenticate with the workspace hosting the Lakemeter Mooncake app
2. **Python 3.10+** — For running the API helper script

## Authentication

The Lakemeter Mooncake app requires a token from its hosting workspace. Before calling `lakemeter_mooncake_api.py`, ensure authentication:

```bash
# Check if authenticated
databricks auth token --host https://fevm-darren-demo.cloud.databricks.com 2>/dev/null && echo "OK" || echo "NEEDS LOGIN"
```

If not authenticated:

```bash
databricks auth login --host https://fevm-darren-demo.cloud.databricks.com
```

Or use a named profile:

```bash
databricks auth token -p fevm-darren
```

## Endpoint Mapping

| Product | POST Endpoint | Discovery Endpoint |
|---------|--------------|-------------------|
| Jobs Classic | `/api/v1/calculate/jobs-classic` | `/api/v1/instances/types?cloud=AZURE&region=chinanorth3` |
| Jobs Serverless | `/api/v1/calculate/jobs-serverless` | (same) |
| All-Purpose Classic | `/api/v1/calculate/all-purpose-classic` | (same) |
| All-Purpose Serverless | `/api/v1/calculate/all-purpose-serverless` | (same) |
| DBSQL Serverless | `/api/v1/calculate/dbsql-serverless` | `/api/v1/dbsql/warehouse-sizes?cloud=AZURE` |
| DBSQL Classic/Pro | `/api/v1/calculate/dbsql-classic-pro` | (same) |
| DLT Classic | `/api/v1/calculate/dlt-classic` | `/api/v1/dlt/editions` |
| DLT Serverless | `/api/v1/calculate/dlt-serverless` | (same) |
| Lakebase | `/api/v1/calculate/lakebase` | `/api/v1/lakebase/list` |
| Databricks Apps | `/api/v1/calculate/databricks-apps` | `/api/v1/databricks-apps/sizes` |
| Model Serving | `/api/v1/calculate/model-serving` | `/api/v1/model-serving/gpu-types?cloud=AZURE` |
| Vector Search | `/api/v1/calculate/vector-search` | `/api/v1/vector-search/modes` |
| Clean Room | `/api/v1/calculate/clean-room` | `/api/v1/clean-room/info` |
| Lakeflow Connect | `/api/v1/calculate/lakeflow-connect` | `/api/v1/lakeflow-connect/info` |
| Support | `/api/v1/calculate/databricks-support` | — |
| Enhanced Security | `/api/v1/calculate/enhanced-security` | — |

## Calling the API

Use the helper script:

```bash
# Look up valid options first
python3 resources/lakemeter_mooncake_api.py GET /api/v1/lakebase/list
python3 resources/lakemeter_mooncake_api.py GET '/api/v1/instances/types?cloud=AZURE&region=chinanorth3'
python3 resources/lakemeter_mooncake_api.py GET '/api/v1/dbsql/warehouse-sizes?cloud=AZURE'
python3 resources/lakemeter_mooncake_api.py GET '/api/v1/model-serving/gpu-types?cloud=AZURE'

# Calculate cost
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/lakebase \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","cu_size":4,"num_nodes":1,"hours_per_month":730,"storage_gb":500}'
```

## Examples

### Lakebase (4 CU, Premium, 500 GB storage)
```bash
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/lakebase \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","cu_size":4,"num_nodes":1,"hours_per_month":730,"storage_gb":500}'
```

### DBSQL Serverless (Medium warehouse, 8 hours/day)
```bash
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/dbsql-serverless \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","warehouse_size":"Medium","num_clusters":1,"hours_per_month":176}'
```

### Jobs Classic (4 workers, Premium)
```bash
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/jobs-classic \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","driver_node_type":"Standard_D4s_v5","worker_node_type":"Standard_D16s_v5","num_workers":4,"photon_enabled":false,"hours_per_month":176}'
```

### Databricks Apps (Medium, 24/7)
```bash
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/databricks-apps \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","size":"medium","hours_per_month":730}'
```

### Model Serving (T4 GPU, small scale-out)
```bash
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/model-serving \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","gpu_type":"gpu_small_t4","scale_out":"small","hours_per_month":730}'
```

### DLT Classic (Advanced, Photon, 4 workers)
```bash
python3 resources/lakemeter_mooncake_api.py POST /api/v1/calculate/dlt-classic \
  '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","dlt_edition":"ADVANCED","photon_enabled":true,"driver_node_type":"Standard_D4s_v5","worker_node_type":"Standard_D16s_v5","num_workers":4,"hours_per_month":176}'
```

## Discount Support

Most endpoints accept an optional `discount_config`:

```json
{
  "discount_config": {
    "global": { "dbu_discount": 20, "vm_discount": 10, "storage_discount": 5 },
    "sku_specific": { "JOBS_COMPUTE": 25 },
    "notes": "Mooncake enterprise agreement FY26"
  }
}
```

## Mooncake DBU Rates (¥ CNY per DBU-hour, Premium tier)

| SKU | ¥ CNY/DBU-hr |
|-----|-------------|
| All-Purpose Compute | ¥3.498 |
| All-Purpose Serverless | ¥6.36 |
| Jobs Compute | ¥1.908 |
| Jobs Serverless | ¥2.989 |
| SQL Compute | ¥1.3992 |
| SQL Pro | ¥3.88 |
| Serverless SQL | ¥4.897 |
| Model Serving | ¥0.49 |
| Model Training | ¥4.547 |
| Lakebase | ¥3.625 |
| Databricks Storage | ¥0.235/DSU |
| DLT Core | ¥1.908 |
| DLT Pro | ¥2.418 |
| DLT Advanced | ¥3.432 |

**DLT is edition-based** — pass `dlt_edition` as `CORE`, `PRO`, or `ADVANCED` to `dlt-classic`/`dlt-serverless`. Core equals the Jobs Compute Premium rate; Pro and Advanced step up (≈1.27× and ≈1.80×). Discover editions + rates via `GET /api/v1/dlt/editions`.

## Key Differences from Standard Lakemeter

1. **Mooncake regions only** — chinanorth3, chinaeast2, chinanorth2
2. **Different DBU rates** — Mooncake pricing differs from Azure global
3. **No Quicksizer** — Use Lakemeter API directly (Quicksizer does not support Mooncake)
4. **Different auth** — Authenticate to the app's hosting workspace, not fe-vm-lakemeter
5. **CNY only** — All prices in Chinese Yuan (¥). No USD conversion.

## Frontend

The app includes a web UI at the app URL with:
- DBU pricing tables (USD + CNY)
- Searchable instance type catalog
- Interactive cost calculator
- API reference documentation

## Important Notes

1. **Standard tier retires Oct 1, 2026** — Use Premium for all new estimates
2. **VM prices in CNY** — Instance VM costs are in CNY (converted to USD at ~6.35 rate)
3. **Region matters** — Always specify a Mooncake region; non-Mooncake regions are rejected
4. **Serverless = Premium only** — Serverless workloads require Premium tier

## Support

- **Slack:** #sizing
- **Azure CN pricing:** https://www.azure.cn/en-us/pricing/details/databricks/
