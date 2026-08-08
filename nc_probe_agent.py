import argparse
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Production TCP Socket Probe Agent')
    parser.add_argument('--host', default='localhost', help='TCP Host')
    parser.add_argument('--port', default=5432, type=int, help='TCP Port')
    parser.add_argument('--timeout', default=5, type=int, help='Timeout')
    args = parser.parse_args()

    log.info("................Production TCP Socket Probe Agent Started................")
    log.info(f"Validation for port probe on host:{args.host} port:{args.port} has started")

    try:
        linux_cmd = subprocess.run(
            ["nc", "-z", "-v", "-w", str(args.timeout), args.host, str(args.port)],
            check=True,
            capture_output=True,
            text=True,
            timeout=args.timeout + 2)
        cmd_output = (linux_cmd.stdout + linux_cmd.stderr).strip()
        log.info(f"{cmd_output }")
        log.info(f"Validation for port:{args.port} on host:{args.host} has ended")
        log.info("................Production TCP Socket Probe Process Ended................")
        sys.exit(0)
    except FileNotFoundError as err:
        log.warning(f"Validation for port:{args.port} on host:{args.host} ended with error: {err}")
        log.info("................Production TCP Socket Probe Agent Ended................")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"Linux shell command failed, Validate Error: {err.stderr.strip()}")
        log.info("................Production TCP Socket Probe Agent Ended................")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.warning(f"Linux shell command got timeout after {args.timeout + 2} seconds")
        log.info("................Production TCP Socket Probe Agent Ended................")
        sys.exit(1)

if __name__ == '__main__':
    main()