import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

openPorts = []


def scanPort(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:

            # try to figure out what service is running
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"

            print(f"[OPEN] Port {port} -> {service.upper()}")

            openPorts.append({
                "port": port,
                "service": service
            })

        sock.close()

    except:
        pass


def main():

    parser = argparse.ArgumentParser(
        description="Simple Port Scanner with Service Detection"
    )

    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("start_port", type=int, help="Starting port number")
    parser.add_argument("end_port", type=int, help="Ending port number")

    args = parser.parse_args()

    try:
        targetIP = socket.gethostbyname(args.target)

    except:
        print("Could not resolve hostname.")
        return

    print("\n" + "=" * 55)
    print(f"Scanning Target: {args.target} ({targetIP})")
    print(f"Scanning Ports: {args.start_port} - {args.end_port}")
    print("=" * 55)

    startTime = time.time()

    # using threads to speed up scanning
    with ThreadPoolExecutor(max_workers=100) as executor:

        for port in range(args.start_port, args.end_port + 1):
            executor.submit(scanPort, targetIP, port)

    endTime = time.time()

    print("\n" + "=======================================================" )
    print("Scan Finished")
    print(f"Open Ports Found: {len(openPorts)}")
    print(f"Time Taken: {round(endTime-startTime, 2)} seconds")
    print("=======================================================" + "\n")


if __name__ == "__main__":
    main()