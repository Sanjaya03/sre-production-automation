import json
import sys

try:
    with open("/home/sanjaya/sre/config/alerts.json", "r") as json_line:
        alerts_file = json.load(json_line)
except FileNotFoundError:
    print("Error: alerts.json not found", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: alerts.json is corrupt", file=sys.stderr)
    sys.exit(1)
alerts = alerts_file.get("channel", "general")
print("Alerts will be sent to channel: " + alerts)