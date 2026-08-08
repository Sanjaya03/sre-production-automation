import subprocess

active_user = subprocess.run(["whoami"], capture_output=True, text=True, check=True).stdout.strip()

if active_user == "root":
    print("CRITICAL: Script is running with root privileges!")
else:
    print("Normal User detected.")