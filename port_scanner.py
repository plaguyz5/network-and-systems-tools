import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor


def scan_port(host: str, port: int, timeout: float = 1.0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return port if sock.connect_ex((host, port)) == 0 else None


def scan_ports(host: str, start_port: int, end_port: int, workers: int = 50):
    open_ports = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        tasks = [
            executor.submit(scan_port, host, port)
            for port in range(start_port, end_port + 1)
        ]

        for task in tasks:
            result = task.result()
            if result:
                open_ports.append(result)

    return open_ports


def main():
    parser = argparse.ArgumentParser(description="Threaded TCP port scanner")
    parser.add_argument("host", help="Target host (IP or domain)")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=50)

    args = parser.parse_args()

    start_time = time.time()
    open_ports = scan_ports(args.host, args.start, args.end, args.threads)
    elapsed = time.time() - start_time

    print("\nScan finished")
    print(f"Open ports: {sorted(open_ports)}")
    print(f"Time elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
