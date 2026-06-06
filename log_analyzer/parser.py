

import sys

# INTERFACE
print("-" * 50)
print("AETHER: Tactical Log Analyzer v2.3 (Data Lake)")
print("-" * 50)
print("[*] Initializing log extraction...\n")

log_file_path = "access.log.2017-01-01"
report_file_path = "AETHER_report.txt"

ip_counts = {}
status_counts = {}

#DATA EXTRACTION
try:
    file_obj = open(log_file_path, "r")
except FileNotFoundError:
    print(f"[-] ERROR: Could not locate target file '{log_file_path}'.")
    sys.exit(1)
else:
    with file_obj as log_file:
        for line in log_file:
            parts = line.split()
            if len(parts) < 9:
                continue

            ip_address = parts[0]
            status_code = parts[8]

            # Count IPs
            if ip_address in ip_counts:
                ip_counts[ip_address] += 1
            else:
                ip_counts[ip_address] = 1

            # Count Status Codes
            if status_code in status_counts:
                status_counts[status_code] += 1
            else:
                status_counts[status_code] = 1

#DATA SORTING ---
sorted_ips = sorted(ip_counts.items(), key=lambda item: item[1], reverse=True) #We're sorting on item in position 2 (technically [1]) and revering the order.
sorted_statuses = sorted(status_counts.items(), key=lambda item: item[1], reverse=True)

# DATA EXPORT
print(f"[*] Compiling full intelligence report to '{report_file_path}' ")

try:
    # Open a new file in "w" (write) mode. It will create it if it doesn't exist.
    with open(report_file_path, "w") as report:
        report.write("AETHER LOG ANALYSIS FULL REPORT\n")
        report.write("=" * 50 + "\n\n")

        # Write every single IP
        report.write(f"TOTAL UNIQUE IPs: {len(ip_counts)}\n")
        report.write("-" * 45 + "\n")
        report.write(f"{'IP ADDRESS':<20} | {'REQUEST COUNT':<15}\n") # As before, f{"something":<number} will give shift by number of spaces before the next character comes
        report.write("-" * 45 + "\n")
        for ip, count in sorted_ips:
            report.write(f"{ip:<20} | {count:<15}\n")

        report.write("\n" + "=" * 50 + "\n\n")

        # Write every single Status Code
        report.write(f"TOTAL UNIQUE STATUS CODES: {len(status_counts)}\n")
        report.write("-" * 45 + "\n")
        report.write(f"{'STATUS CODE':<20} | {'OCCURRENCES':<15}\n")
        report.write("-" * 45 + "\n")
        for code, count in sorted_statuses:
            report.write(f"{code:<20} | {count:<15}\n")

except Exception as e:
    print(f"[-] ERROR: Failed to write report file. System says: {e}")

# TERMINAL DASHBOARD
print("[+] Export successful.\n")
print("-" * 50)
print("TACTICAL OVERVIEW (TOP 10 THREATS)")
print("-" * 50)

print(f"{'IP ADDRESS':<20} | {'REQUEST COUNT':<15}")
print("-" * 45)
# Print only the Top 10 to the screen
for ip, count in sorted_ips[:10]:
    print(f"{ip:<20} | {count:<15}")

print("\n" + "-" * 50)
print("[*] Analysis Complete.")


