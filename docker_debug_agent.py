import argparse
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Docker Debug Agent')
    parser.add_argument('--container',type=str,default='pg_cgroup_lab',help='Container Name')
    arg = parser.parse_args()

    log.info(f"----------Docker debug agent started for {arg.container}------------")

    try:
        state_cmd = subprocess.run(
            ['docker','inspect','-f','Status: {{.State.Status}} Exit_cd: {{.State.ExitCode}} Pid: {{.State.Pid}}',arg.container],
            check=True,capture_output=True,text=True,timeout=5)
        state_cmd_output = state_cmd.stdout.strip()
        log.info(f"SUCCESS: Container {arg.container} Running State: {state_cmd_output}")

        log_cmd = subprocess.run(['docker','logs','--tail','5','--timestamps',arg.container],
                                 check=True,capture_output=True,text=True,timeout=5)
        log_cmd_output = (log_cmd.stdout + log_cmd.stderr).splitlines()

        log.info("Container Log Lines: ")

        for log_line in log_cmd_output:
            log.info(f" --> {log_line}")
    
    except FileNotFoundError as err:
        log.warning(f"ERROR: Check system binary.. ERR:{err}")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell Command failed.. ERR: {err.stderr.strip()}")
        sys.exit(1)
    except subprocess.TimeoutExpired as err:
        log.warning(f"ERROR: Shell Command got timed out.. ERR: {err}")
        sys.exit(1)

    log.info("-------------------------------------------------------------------------")

if __name__ == '__main__':
    main()

