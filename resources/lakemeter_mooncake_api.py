#!/usr/bin/env python3
"""
Lakemeter Mooncake API helper script for Azure China Databricks cost estimation.

Usage:
    python3 lakemeter_mooncake_api.py GET /api/v1/lakebase/list
    python3 lakemeter_mooncake_api.py POST /api/v1/calculate/lakebase '{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","cu_size":4,"num_nodes":1,"hours_per_month":730,"storage_gb":500}'
    python3 lakemeter_mooncake_api.py GET '/api/v1/instances/types?cloud=AZURE&region=chinanorth3'

Authentication:
    The Lakemeter Mooncake app requires a token scoped to its hosting workspace
    (e2-demo-field-eng.cloud.databricks.com). Tokens from other workspaces
    will be rejected with HTTP 401.

    The script tries in order:
    1. Named profile: Darren
    2. Host-based token: databricks auth token --host <APP_HOST>
    3. If nothing works: prompts the user to run databricks auth login
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error

# ============================================================
# UPDATE THESE AFTER DEPLOYMENT
# ============================================================
BASE_URL = "https://lakemeter-mooncake-7474649521824087.aws.databricksapps.com"
APP_HOST = "https://fevm-darren-demo.cloud.databricks.com"
PROFILE = "fevm-darren"


def get_token():
    """Get a Databricks OAuth token scoped to the app's hosting workspace."""
    # Try named profile first
    token = _try_get_token(["databricks", "auth", "token", "-p", PROFILE])
    if token:
        return token

    # Try host-based
    token = _try_get_token(["databricks", "auth", "token", "--host", APP_HOST])
    if token:
        return token

    print("ERROR: Not authenticated to the Lakemeter Mooncake workspace.", file=sys.stderr)
    print(f"Run:  databricks auth login --host {APP_HOST}", file=sys.stderr)
    print(f"  or: databricks auth login -p {PROFILE}", file=sys.stderr)
    sys.exit(1)


def _try_get_token(cmd):
    """Run a databricks auth command and extract the access_token from JSON output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return None
        try:
            data = json.loads(result.stdout)
            return data.get("access_token")
        except json.JSONDecodeError:
            raw = result.stdout.strip()
            return raw if raw else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def call_api(method, path, body=None):
    """Call the Lakemeter Mooncake API."""
    token = get_token()
    url = f"{BASE_URL}{path}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = None
    if body:
        if isinstance(body, str):
            data = body.encode("utf-8")
        else:
            data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            try:
                result = json.loads(raw)
                print(json.dumps(result, indent=2))
                return result
            except json.JSONDecodeError:
                print(raw)
                return raw
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            print(json.dumps(error_json, indent=2), file=sys.stderr)
        except json.JSONDecodeError:
            print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 lakemeter_mooncake_api.py <METHOD> <PATH> [JSON_BODY]")
        print()
        print("Lakemeter Mooncake — Azure China Databricks cost estimation")
        print(f"Base URL: {BASE_URL}")
        print()
        print("Examples:")
        print("  python3 lakemeter_mooncake_api.py GET /api/v1/lakebase/list")
        print("  python3 lakemeter_mooncake_api.py GET '/api/v1/instances/types?cloud=AZURE&region=chinanorth3'")
        print("  python3 lakemeter_mooncake_api.py GET '/api/v1/dbsql/warehouse-sizes?cloud=AZURE'")
        print("  python3 lakemeter_mooncake_api.py GET '/api/v1/model-serving/gpu-types?cloud=AZURE'")
        print()
        print("  python3 lakemeter_mooncake_api.py POST /api/v1/calculate/lakebase \\")
        print('    \'{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","cu_size":4,"num_nodes":1,"hours_per_month":730,"storage_gb":500}\'')
        print()
        print("  python3 lakemeter_mooncake_api.py POST /api/v1/calculate/dbsql-serverless \\")
        print('    \'{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","warehouse_size":"Medium","num_clusters":1,"hours_per_month":176}\'')
        print()
        print("  python3 lakemeter_mooncake_api.py POST /api/v1/calculate/jobs-classic \\")
        print('    \'{"cloud":"AZURE","region":"chinanorth3","tier":"PREMIUM","driver_node_type":"Standard_D4s_v5","worker_node_type":"Standard_D16s_v5","num_workers":4,"hours_per_month":176}\'')
        sys.exit(1)

    method = sys.argv[1].upper()
    path = sys.argv[2]
    body = sys.argv[3] if len(sys.argv) > 3 else None

    if body:
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON body: {body}", file=sys.stderr)
            sys.exit(1)

    call_api(method, path, body)


if __name__ == "__main__":
    main()
