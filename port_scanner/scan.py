import socket
from concurrent.futures import ThreadPoolExecutor


# ENGINE FUNCTION
# We isolate the core scanning logic into a single function that an individual thread can run.
def probe_port(ip, port):
    try:
        my_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Since threads run in parallel, we can slightly increase the timeout
        # to 1.0 second to ensure higher accuracy without sacrificing total speed.
        my_soc.settimeout(1.0)

        result = my_soc.connect_ex((ip, port))

        if result == 0:
            print(f"[+] SUCCESS: Port {port} is OPEN!")

        my_soc.close()
    except Exception:
        # Ignore any operational or thread-level socket errors
        pass


# MAIN EXECUTION
def main():
    print("-" * 50)
    print("AETHER: Tactical Port Scout - Multi-Threaded")
    print("-" * 50)

    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    # Define how many simultaneous scouts (threads) we want to deploy
    max_threads = 100

    print(f"\n[*] Deploying {max_threads} threads against {target_ip}...")
    print("-" * 50)

    # The ThreadPoolExecutor acts as the command center, managing the worker pool
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Loop through the port range and assign each port probe task to a thread
        for port in range(start_port, end_port + 1):
            executor.submit(probe_port, target_ip, port)

    print("-" * 50)
    print("[*] Multi-Threaded Sweep Complete.")


if __name__ == "__main__":
    main()