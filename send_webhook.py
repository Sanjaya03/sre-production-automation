import json
import os
import sys
import urllib.error
import urllib.request

webhook_url = os.environ.get('WEBHOOK_URL','https://httpbin.org/post')
alert_payload = {
    "event": "POSTGRES_DATABASE_DOWN",
    "severity": "P1_CRITICAL",
    "host": os.environ.get('HOSTNAME','localhost')
}
json_data = json.dumps(alert_payload).encode('utf-8')
request = urllib.request.Request(
    webhook_url,
    data=json_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=5) as response:
        print(f"[PYTHON AGENT]Webhook Alert Delivered! STATUS: {response.status}")
        sys.exit(0)

except urllib.error.HTTPError as err:
    print(f"[PYTHON AGENT]CRITICAL: Webhook HTTP Error {err.code}: {err.reason}")
    sys.exit(1)
except urllib.error.URLError as err:
    print(f"[PYTHON AGENT]CRITICAL: Network Failure: {err.reason}")
    sys.exit(1)