import re

log_line = 'STATUS: connection Failed on port 8080.'
pattern = re.search(r'Failed on port (\d{1,5})', log_line, re.IGNORECASE)

if pattern:
    failed_port = pattern.group(1)
    print(f'Connection failed on port: {failed_port}')
else:
    print('No failed port found in the log line.')