import subprocess

raw_percentage = int(subprocess.run(['df', '--output=pcent', '/'], capture_output=True, text=True, check=True).stdout.strip().split('\n')[1].strip('%'))

if raw_percentage >= 90:
    print(f"CRITICAL: Disk space is at {raw_percentage}%!")
    exit(1)
else:
    print(f"Disk healthy: {raw_percentage}%.")