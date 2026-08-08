import argparse
import json
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Docker Storage Agent')
    parser.add_argument('--container',type=str,default='pg_prod',help='Container Name')
    arg = parser.parse_args()

    log.info(f"--------Inspection volume for container {arg.container}------------")

    try: 
        cmd = subprocess.run(['docke','inspect','-f','{{json .Mounts}}',arg.container],
                             check=True,capture_output=True,text=True,timeout=5)
        cmd_output = json.loads(cmd.stdout.strip())
        filter_mounts = next((mount for mount in cmd_output 
                              if mount.get('Type') == 'volume' and mount.get('Destination') == '/var/lib/postgresql/data')
                            ,None)
        if not filter_mounts:
            log.warning(f"ERROR: Database container {arg.container} path is not bound to a persistent volume!")
            log.info("-----------------------------------------------------------")
            sys.exit(1)

        log.info(f"SUCCESS: Database container {arg.container} path bound to host path {filter_mounts.get('Source')}")
        log.info("-----------------------------------------------------------")

    except FileNotFoundError as err:
        log.warning(f"ERROR: Check user/system Binary ERR: {err}")
        log.info("-----------------------------------------------------------")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell command failed. ERR: {err}")
        log.info("-----------------------------------------------------------")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.warning("ERROR: Shell command got timed out after 5 seconds")
        log.info("-----------------------------------------------------------")
        sys.exit(1)

if __name__ == '__main__':
    main()