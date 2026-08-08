import argparse
import logging
import subprocess
import sys

# Week 3: Structured SRE Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [DOCKERFILE_AUDIT] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging = logging.getLogger(__name__)

def main():
    # Week 3: Standardized CLI Flags
    parser = argparse.ArgumentParser(description="Production Dockerfile Security & Health Auditor")
    parser.add_argument('--container', default='pg_prod', help='Container name')
    args = parser.parse_args()

    logging.info(f"Inspecting execution user UID and HEALTHCHECK for container: {args.container}...")

    # Week 6 & 5: Inspect container User UID and status via Go Templates
    try:
        inspect_res = subprocess.run(
            ["docker", "inspect", "-f", "User: {{.Config.User}} | Status: {{.State.Status}}", args.container],
            check=True, capture_output=True, text=True, timeout=5
        )
        user_info = inspect_res.stdout.strip()
        logging.info(f"SUCCESS: Container Config -> {user_info}")
        sys.exit(0)

    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        logging.critical(f"Audit failed for container '{args.container}': {err}")
        sys.exit(1)

if __name__ == '__main__':
    main()