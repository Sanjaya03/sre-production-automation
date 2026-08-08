import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

arg_help_desc = argparse.ArgumentParser(description="Database Monitoring Script")
arg_help_desc.add_argument('--webhook', 
                           default='https://httpbin.org/post', 
                           help='Alerting Webhook URL')
arg_help_desc.add_argument('--db', 
                           default='sre_dev', 
                           help='DB Name')
arg = arg_help_desc.parse_args()

try:
    pg_check_cmd = subprocess.run(
        ["pg_isready","-d",f"{arg.db}"], 
        check=True, 
        capture_output=True, 
        text=True, 
        timeout=5)
    pg_check_output = pg_check_cmd.stdout.strip()
    print(f"SUCCESS: Database {arg.db} is healthy and up..")
    print(f"{pg_check_output}")
    sys.exit(0)

except FileNotFoundError as err:
    print(f"WARNING: Check command binary: {err}")
except subprocess.CalledProcessError as err:
    print(f"ERROR: Check command: {err.stderr.strip()}")
except subprocess.TimeoutExpired:
    print("WARNING: Command got timed out after 5 seconds")

alert_page = {
    "Event": "Postgres DB is down",
    "Severity": "P1",
    "Host": os.environ.get('HOSTNAME','localhost')
}

json_data = json.dumps(alert_page).encode('utf-8')
request = urllib.request.Request(arg.webhook,
                                 data=json_data,
                                 headers={"Content-type": "application/json"},
                                 method="POST")

try:
    with urllib.request.urlopen(request, timeout=5) as response:
        print(f"SUCCESS: Webhook alert has been sent, response: {response.status}")
        sys.exit(1)
except urllib.error.HTTPError as err:
    print(f"FAILED: Webhook alert has failed to sent, HTTP Error: {err.code}: {err.reason}")
    sys.exit(1)
except urllib.error.URLError as err:
    print(f"ERROR: Webhook URL issue, Error: {err.reason}")