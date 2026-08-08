import os
import sys
from pathlib import Path

db_port = os.environ.get('DB_PORT','5432')
check_dir = Path('/tmp/sre_dev')

print(f"Active python executables: {sys.executable}")
print(f"Database Port configuration: {db_port}")
print(f"Directory {check_dir} Exists: {check_dir.exists()}")

sys.exit(0)