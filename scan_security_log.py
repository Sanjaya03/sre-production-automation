import os
import sys
import re

LOG_FILE = "/home/sanjaya/sre/logs/security.log"

def scan_log_file(file_path):
    if not os.path.isfile(file_path):
        print(f"ERROR: Log file {file_path} not found!", file=sys.stderr)
        return 1
    pattern = r'failed login for (\w+)'
    with open(file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                username = match.group(1).strip()
                print(f"ALERT: Failed login attempt detected for user: {username}")
    return 0

if scan_log_file(LOG_FILE) != 0:
    print("Security scan failed.", file=sys.stderr)
    sys.exit(1) 
else:
    print("Security scan completed successfully.")
    sys.exit(0)