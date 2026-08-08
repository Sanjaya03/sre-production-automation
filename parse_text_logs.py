import re
import sys
from pathlib import Path

LOG_PATH = Path('/home/sanjaya/sre/logs/db.log')

print("-------------------LOG SCAN STARTED-------------------------")

if not LOG_PATH.is_file():
    print(f"ERROR: log file {LOG_PATH.name} is not available in path {LOG_PATH.parent}")
    sys.exit(1)

pattern = re.compile(r'fatal: .* authentication failed .* (\b(?:\d{1,3}\.){3}\d{1,3}\b)', re.IGNORECASE)
failing_ip = []

with open(LOG_PATH,'r') as log_stream:
     for line in log_stream:
          match = pattern.search(line)
          if match:
                failing_ip.append(match.group(1))

print(f"Failing IP: {failing_ip}")

print("-------------------LOG SCAN ENDED-------------------------")