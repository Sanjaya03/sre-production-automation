import os
import sys
import re

LOG_FILE = "/home/sanjaya/sre/logs/access.log"

def analyze_log_file(file_path):
    if not os.path.isfile(file_path):
        print(f"ERROR: Log file {file_path} not found!", file=sys.stderr)
        return 1
    pattern = r'\" (5\d{2})'
    with open(file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(pattern, line)
            if match:
                status_code = match.group(1).strip()
                print(f"CRITICAL OUTAGE: Checkout failed with status code: {status_code}")
    return 0

if analyze_log_file(LOG_FILE) != 0:
    print("Outage analysis failed.", file=sys.stderr)
    sys.exit(1)
else:
    print("Outage analysis completed successfully.")
    sys.exit(0)