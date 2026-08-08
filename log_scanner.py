import re

pattern = r'from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

with open('/home/sanjaya/sre/logs/some.log', 'r') as log_lines:
    for line in log_lines:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            ip_address = match.group(1)
            print(f'IP address found: {ip_address}')
        else:
            print('No IP address found in the log line.')