import argparse
import json
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s [WEEK5 CAPSTONE AGENT] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Week 5 Pre flight Infrastrcture Auditor')
    parser.add_argument('--container',type=str,default='pg_prod',help='Container name')
    parser.add_argument('--hostip',type=str,default='127.0.0.1',help='Host IP Address')
    parser.add_argument('--hport',type=int,default=5433,help='Host Port')
    parser.add_argument('--dbport',type=int,default=5432,help='Container DB Port')
    args = parser.parse_args()

    log.info("================ WEEK 5 CAPSTONE AUDIT STARTED ================")
    log.info(f"[CHECK-1] Container {args.container} Health Check")

    try:
        state_res = subprocess.run(
            ['docker','inspect','-f','Status: {{.State.Status}} Pid: {{.State.Pid}}',args.container],
            check=True,capture_output=True,text=True,timeout=5)
        con_state = state_res.stdout.strip()

        if "running" in con_state:
            log.info(f"SUCCESS: Container {args.container} is healthy with {con_state}")
        else:
            log.critical(f"ERROR: Container {args.container} is not in running state")
            log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
            sys.exit(1)

    except FileNotFoundError as err:
        log.warning(f"ERROR: Check Executable Binary. ERR: {err}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell Command execution failed. ERR: {err.stderr.strip()}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.critical("ERROR: Shell command got timeout at execution.")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)

    log.info(f"[CHECK-2] Inspection for Container {args.container} Kernel Cgroup Memory Limit")

    try: 
        memory_res = subprocess.run(
            ['docker','exec',args.container,'cat','/sys/fs/cgroup/memory.max'],
            check=True,capture_output=True,text=True,timeout=5)
        mem_state = memory_res.stdout.strip()

        if mem_state.isdigit:
            mem_in_mb = int(int(mem_state) / (1024 * 1024))
            log.info(f"SUCCESS: Container {args.container} Maximum memory set as {mem_in_mb} Mb")
        else:
            log.warning(f"Container {args.container} running at {mem_state}")
        
    except FileNotFoundError as err:
        log.warning(f"ERROR: Check Executable Binary. ERR: {err}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell Command execution failed. ERR: {err.stderr.strip()}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.critical("ERROR: Shell command got timeout at execution.")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)

    log.info(f"[CHECK-3]Inspecting DB Container{args.container} Storage Persistence")

    try:
        vol_state = subprocess.run(['docker','inspect','-f','{{json .Mounts}}',args.container],
                               check=True,capture_output=True,text=True,timeout=5)
        vol_data = json.loads(vol_state.stdout.strip())

        vol_data_ext = next(
            (vol for vol in vol_data if vol.get('Type') == 'volume' and vol.get('Destination') == '/var/lib/postgresql/data'),
            None)

        if vol_data_ext:
            log.info(f"SUCCESS: Container {args.container} bounded to host volume {vol_data_ext.get('Source')}")
        else:
            log.warning(f"Container {args.container} not bounded with host storage")

    except FileNotFoundError as err:
        log.warning(f"ERROR: Check Executable Binary. ERR: {err}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell Command execution failed. ERR: {err.stderr.strip()}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.critical("ERROR: Shell command got timeout at execution.")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)

    log.info(f"[CHECK-4] Inspecting container {args.container} IP and host:port -> {args.hostip}:{args.hport} binding")

    try:
        con_ip = subprocess.run(
            ['docker','inspect','-f','{{.NetworkSettings.Networks.bridge.IPAddress}}',args.container],
            check=True,capture_output=True,text=True,timeout=5)
        con_ip_ext = con_ip.stdout.strip()

        log.info(f"SUCCESS: Container {args.container} assigned to IP {con_ip_ext}")

        con_port = subprocess.run(
            ['nc','-z','-v','-w','2',args.hostip,str(args.hport)],
            check=True,capture_output=True,text=True,timeout=5)

        con_port_probe = con_port.stderr.strip()

        if 'succeeded!' in con_port_probe:
            log.info(f"SUCCESS: Socket {args.hostip}:{args.hport} Port Forwarding working fine!")
            log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        else:
            log.critical(f"ERROR: Container DB {args.container} Port Forwarding at host {args.hostip} failed!")
            log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
            sys.exit(1)

    except FileNotFoundError as err:
        log.warning(f"ERROR: Check Executable Binary. ERR: {err}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.CalledProcessError as err:
        log.critical(f"ERROR: Shell Command execution failed. ERR: {err.stderr.strip()}")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.critical("ERROR: Shell command got timeout at execution.")
        log.info("================ WEEK 5 CAPSTONE AUDIT ENDED ================")
        sys.exit(1)

if __name__ == '__main__':
    main()