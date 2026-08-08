import subprocess
import sys

try:
   command_output = subprocess.run(
      ["pg_isready","-h","localhost"],
      check=True,
      capture_output=True,
      text=True,
      timeout=5)
   result = command_output.stdout.strip()
   print(f"{result}")
   sys.exit(0)
except subprocess.CalledProcessError as err:
   print(f"command failed: {err.stderr.strip()}")
   sys.exit(1)
except FileNotFoundError as err:
   print(f"Check command binary: {err}")
   sys.exit(1)
except subprocess.TimeoutExpired:
   print("command timed out after 5 seconds")
   sys.exit(1)