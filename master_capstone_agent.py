import argparse
import logging
import os
import socket
import ssl
import subprocess
import sys
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO,
                          format='%(asctime)s %(levelname)s %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S %Z')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Master Capstone Agent')
    parser.add_argument('--domain', default='google.com',help='Domain Name')
    parser.add_argument('--dbport',default=5432,type=int,help='DBPort')
    parser.add_argument('--container',default='pg_capstone_65',help='Container Name')
    args = parser.parse_args()

    log.info("========================================Master Capstone Agent====================================")

    try:
        get_ip = socket.gethostbyname(args.domain)
        log.info(f"SUCCESS: DNS resolution complete for {args.domain}->{get_ip} ")

    except socket.gaierror as err:
        log.critical(f"ERROR: DNS resolution failed for {args.domain} ERR:{err}")
        log.info("=======================================================================================================")
        sys.exit(1)

    try:
        with ssl.create_default_context().wrap_socket(socket.create_connection((get_ip,443),timeout=5),server_hostname=args.domain) as ssocket:
            get_cert = ssocket.getpeercert()['notAfter']
            cert_date = datetime.strptime(get_cert,'%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            curr_date = datetime.now(timezone.utc)
            days_remain = (cert_date - curr_date).days

            if days_remain > 30:
                log.info(f"SUCCESS: TLS certificate validation completed, expiring in {days_remain} days.")
            else:
                log.warning(f"TLS Certificate is expiring in soon.. {days_remain} days remining.")

    except Exception as err:
        log.critical(f"ERROR: TLS validation has failed.. ERR: {err}")
        log.info("=======================================================================================================")
        sys.exit(1)

    try:
        pg_password = {**os.environ,"POSTGRES_PASSWORD": "iamsre321"}
        cmd = subprocess.run(
            ['docker','exec',args.container,'psql','-U','postgres',
             '-h','127.0.0.1','-p',str(args.dbport),'-c','SELECT current_user, current_database();'],
            env=pg_password,check=True,capture_output=True,text=True,timeout=5)
        result = cmd.stdout.strip()

        log.info(f"SUCCESS: DB authentication was successfull DB Details : {result}")

    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell execution failed.. ERR: {err.stderr.strip()}")
        log.info("=======================================================================================================")
        sys.exit(1)
    except (FileNotFoundError,subprocess.TimeoutExpired) as err:
        log.warning(f"DB Validation failed.. Check ERROR: {err}")
        log.info("=======================================================================================================")
        sys.exit(1)

if __name__ == '__main__':
    main()