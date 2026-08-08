import os
import subprocess
import sys
from pathlib import Path

LOG_PATH = Path('/var/log/bootstrap.log')

if LOG_PATH.is_file():
    print(f"file {LOG_PATH.name} exists in directory {LOG_PATH.parent}")
else:
    print(f"file {LOG_PATH.name} does not exists in directory {LOG_PATH.parent}")

secure_pg_password = {**os.environ, "PGPASSWORD": "iamsre321"}

try:

    cmd = subprocess.run(["psql", "-h", "127.0.0.1", "-U", "sre_app_user", "-d", "prod_app_db", "-t", "-P", "format=unaligned", "-c", "SELECT user;"],
                    env=secure_pg_password,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=5)
    result = cmd.stdout.strip()
    print(f"DB Logged in User: {result}")

except subprocess.CalledProcessError as err:
    print(f"Failed: Check command {err.stderr.strip()}")
    sys.exit(1)