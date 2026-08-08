import argparse
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s [SEC_AGENT] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Docker Security Agent')
    parser.add_argument('--container',type=str,default='pg_secure_lab',help='Docker Container Name')
    arg = parser.parse_args()

    log.info("-------------------------Docker Securiry Agent Started--------------------------------")
    log.info(f"Inspecting Docker Container({arg.container}) Kernal Capability Masking")

    try:
        process_stat_cmd = subprocess.Popen(['docker','exec',arg.container,'cat','/proc/1/status'],
                                           stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        filter_kernel_cap = subprocess.run(['grep','-i','CapEff'],
                                            stdin=process_stat_cmd.stdout,check=True,capture_output=True,text=True,timeout=5)
        cap_eff_value = str(filter_kernel_cap.stdout.strip())

        if '0000000000000000' in cap_eff_value:
              log.info(f"SUCCESS: Container {arg.container} Active Kernel Capability Mask: {cap_eff_value}")
        else:
             log.warning(f"Container {arg.container} might have adminstrative kernel capability: {cap_eff_value}")

        write_attmpt = subprocess.run(['docker','exec',arg.container,'touch','/usr/bin/xyz'],
                                      capture_output=True,text=True,timeout=5)
        if write_attmpt.returncode != 0:
             log.info(f"SUCCESS: Kernel Rejected write attempt: {write_attmpt.stderr.strip()}")             
        else:
             log.warning("Container Root FS is writable!")
        log.info("----------------------------------------------------------------------------------------")

    except (FileNotFoundError,subprocess.CalledProcessError) as err:
         log.critical(f"ERROR: Docker Securiry Agent Failed.. ERR: {err}")
         log.info("----------------------------------------------------------------------------------------")
         sys.exit(1)
    except subprocess.TimeoutExpired:
         log.warning("ERROR: Docker Securiry Agent Failed, command got timeout..")
         log.info("----------------------------------------------------------------------------------------")
         sys.exit(1)

if __name__ == '__main__':
     main()