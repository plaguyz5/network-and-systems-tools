import socket
import argparse


def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0


def scan_ports(host: str, start_port: int, end_port: int):
    print(f"Scanning {host} from port {start_port} to {end_port}\n")

    open_ports = []

    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            print(f"[OPEN] Port {port}")
            open_ports.append(port)

    return open_ports


def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("host", help="Target host (IP or domain)")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)

    args = parser.parse_args()
    open_ports = scan_ports(args.host, args.start, args.end)

    print("\nScan finished.")
    print(f"Open ports: {open_ports}")


if __name__ == "__main__":
    main()
