import json
import sys

try:
    with open("/home/sanjaya/sre/config/config.json", "r") as config_line:
        config = json.load(config_line)
        print(config["port"])
except FileNotFoundError:
    print("Configuration file not found.", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print("Error decoding JSON from the configuration file.", file=sys.stderr)
    sys.exit(1)