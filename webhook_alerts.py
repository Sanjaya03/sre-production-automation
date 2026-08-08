import json
import re
import sys
import requests

LOG_FILE = "/home/sanjaya/sre/logs/payment_app.log"
CONFIG_FILE = "/home/sanjaya/sre/config/config.json"
pattern = r'Error: '
error_count = 0

try:
    with open(CONFIG_FILE,'r') as config_line:
        config = json.load(config_line)
except FileNotFoundError:
    print(f"Warning: Config file{CONFIG_FILE} is missing!", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Warning: File {CONFIG_FILE} bad json format", file=sys.stderr)
    sys.exit(1)
    
webhook_url = config.get("webhook_url")    
if not webhook_url:
    print(f'Warning: {CONFIG_FILE} is missing key "webhook_url"', file=sys.stderr)
    sys.exit(1)
   
try:
    with open(LOG_FILE,'r') as log_line:
        for line in log_line:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                error_count+=1
except FileNotFoundError:
    print(f"Warning: Log file {LOG_FILE} is missing", file=sys.stderr)
    sys.exit(1)
    
if error_count == 0:
    print(f"Success: No Error capture in {LOG_FILE}")
    sys.exit(0)
    
alert = {
    "text": "Alert: Error has been captured in /home/sanjaya/sre/logs/payment_app.log"
}
    
try:
    response = requests.post(webhook_url, json=alert, timeout=5)
    response.raise_for_status()
except requests.exceptions.RequestException as error:
    print(f"Failed to send Slack alert, Error: {error}", file=sys.stderr)
    sys.exit(1)
    
print("Success: Outage alert sent to Slack!")