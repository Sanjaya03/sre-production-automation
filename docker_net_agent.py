import argparse
import logging
import subprocess
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NET_AGENT] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Production Container Network Inspector")
    parser.add_argument('--container', default='pg_prod', help='Container name')
    parser.add_argument('--host-port', type=int, default=5433, help='Host bound port')
    parser.add_argument('--hostip',default='127.0.0.1',help='Host bound IP Address')
    args = parser.parse_args()

    logging.info(f"Inspecting network bindings for container: {args.container}...")

    # Go template accessing per-network bridge IP
    try:
        inspect_res = subprocess.run(
            ["docker", "inspect", "-f", "IP: {{.NetworkSettings.Networks.bridge.IPAddress}}", args.container],
            check=True, capture_output=True, text=True, timeout=5
        )
        ip_info = inspect_res.stdout.strip()
        logging.info(f"SUCCESS: Container '{args.container}' Private Bridge {ip_info}")

    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        logging.critical(f"Failed to inspect network settings for '{args.container}': {err}")
        sys.exit(1)

    # Netcat raw socket probe on host port 5433
    logging.info(f"Probing host DNAT port forwarding on {args.hostip}:{args.host_port}...")
    try:
        nc_res = subprocess.run(
            ["nc", "-z", "-v", "-w", "2", args.hostip, str(args.host_port)],
            check=True, capture_output=True, text=True, timeout=5
        )
        nc_output = (nc_res.stdout + nc_res.stderr).strip()
        logging.info(f"SUCCESS: Port Forwarding Active! {nc_output}")
        sys.exit(0)

    except subprocess.CalledProcessError as err:
        logging.critical(f"Port Forwarding Failed on {args.hostip}:{args.host_port}: {err.stderr.strip()}")
        sys.exit(1)

if __name__ == '__main__':
    main()