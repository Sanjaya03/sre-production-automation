import argparse
import logging
import socket
import ssl
import subprocess
import sys
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s [WEEK4_CAPSTONE] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Network & Security Diagnostic Agent')
    parser.add_argument('--domain',type=str,default='google.com',help='Target domain name')
    parser.add_argument('--tlsport',type=int,default=443,help='Target TLS Port')
    parser.add_argument('--dbhost',type=str,default='localhost',help='Local DB Host')
    parser.add_argument('--dbport',type=int,default=5432,help='Local DB TCP Port')
    args = parser.parse_args()

    log.info("----------------------Network & Security Diagnostic Agent Report-------------------------")
    log.info(f"[CHECK 1] Resolving DNS for domain: {args.domain}----------------")

    try:
        ip_resolve = socket.gethostbyname(args.domain)
        log.info(f"SUCCESS: DNS resolved {args.domain} --> IP: {ip_resolve}")
        
    except socket.gaierror as err:
        log.critical(f"FAILED: DNS resolution check failed for {args.domain} with Error: {err}")
        sys.exit(1)

    log.info(f"[CHECK 2] Inspecting TLS Certificate Expiration for Socket:{args.domain}:{args.tlsport}")

    try:
        with ssl.create_default_context().wrap_socket(socket.create_connection((args.domain,args.tlsport),timeout=5),server_hostname=args.domain) as ssock:
            cert_date_ext = ssock.getpeercert()['notAfter']
            expiry_dt = datetime.strptime(cert_date_ext,'%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            curr_date = datetime.now(timezone.utc)
            days_left = (expiry_dt - curr_date).days

            log.info(f"SUCCESS: TLS Certificate for {args.domain} expires on {cert_date_ext}")
            if days_left < 30:
                log.critical(f"Certificate for {args.domain} is expiring in {days_left} days")

    except Exception as err:
        log.critical(f"FAILED: TLS Security Layer Check for Socket:{args.domain}:{args.tlsport} failed. Error: {err}")
        sys.exit(1)

    log.info(f"[CHECK 3] Probing local database TCP port for Socket:{args.dbhost}:{args.dbport}")    

    try:
        cmd= subprocess.run(['nc','-z','-v','-w','2',args.dbhost,str(args.dbport)],
                            check=True,capture_output=True,text=True,timeout=5)
        cmd_output = cmd.stderr.strip()
        log.info(cmd_output)
        log.info(f"SUCCESS: Local DB TCP socket probe for Socket:{args.dbhost}:{args.dbport} Complted")

    except FileNotFoundError:
        log.warning("ERROR: Check System Binary....")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell command failed.. Error: {err.stderr.strip()}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.warning("ERROR: Shell command got timedout after 5 seconds")
        sys.exit(1)

    log.info("-----------------------------------------------------------------------------------------")

if __name__ == '__main__':
    main()


