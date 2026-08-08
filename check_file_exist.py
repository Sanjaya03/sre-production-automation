import os
import sys

FILE_NAME = '/home/sanjaya/sre/logs/some.logs'

if not os.path.isfile(FILE_NAME):
    print(f"Error: The file {FILE_NAME} does not exist", file=sys.stderr)
    sys.exit(1)
else:
    print(f"The file {FILE_NAME} exists. Proceeding with further operations.")