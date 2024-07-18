import ipaddress
import os
import time
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to display loading messages with a delay
def loading_screen():
    messages = [
        "- Created by Proxynich -",
        "- Copyright? nah it's free -",
        "- Please wait until the process is done -",
        "- IDCloudHost 2k24 -",
        "- Problem with script? please contact to @ekcelsebastianus -",
        "- Bye Bye -"
    ]
    
    for message in messages:
        print(message)
        time.sleep(5)  # 5-second delay
        os.system('clear' if os.name == 'posix' else 'cls')

# Function to display a simple loading animation
def loading_animation(duration=5):
    animation = [
        "   ▄       ▄  ",
        "  ▌▒█   ▄▀▒▌  ",
        "  ▌▒▒█▄▀▒▒▌   ",
        " ▐▄█▒▒▀▀▀▒▒▐  ",
        " ▐▒▒▀▄▀▄▀▒▒▌  ",
        "  ▀▄▒▒▀▒▒▄▀   ",
        "    ▀▄▀▄▀     "
    ]
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in animation:
            sys.stdout.write(f'\r{frame}')
            sys.stdout.flush()
            time.sleep(0.2)
        os.system('clear' if os.name == 'posix' else 'cls')

# Function to read IP addresses from a file
def read_ips(file_name):
    with open(file_name, 'r') as f:
        return set(line.strip() for line in f)

# Function to extract IPs from /24 prefixes in a file
def extract_ips(file_name):
    with open(file_name, 'r') as f:
        prefixes = [line.strip() for line in f]

    extracted_ips = set()
    for prefix in prefixes:
        network = ipaddress.ip_network(prefix)
        extracted_ips.update(str(ip) for ip in network.hosts())

    return extracted_ips

# Function to ping an IP address
def ping_ip(ip):
    try:
        print(f"Pinging {ip}...")
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        if result.returncode == 0:
            return ip
    except subprocess.TimeoutExpired:
        pass
    return None

# Function to ping IP addresses in parallel and count successful pings
def ping_ips(ips):
    print("Ping is running, please wait")
    loading_animation(5)
    
    successful_pings = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            if future.result():
                successful_pings.append(ip)
    return successful_pings

# Function to find matching IPs and write results to the output file
def match_and_write_results(prefix_file, isp_ips, name, as_number, output_file, ping_option):
    extracted_ips = extract_ips(prefix_file)
    matched_ips = extracted_ips & isp_ips
    
    with open(output_file, 'a') as f:
        f.write(f"Name : {name}\n")
        f.write(f"AS : {as_number}\n")
        if matched_ips:
            for ip in matched_ips:
                f.write(f"{ip}\n")
            f.write(f"\nTotal matched IPs: {len(matched_ips)}\n")
        else:
            f.write("No matched IPs found.\n")
        f.write("\n=====================\n\n")

    if ping_option.lower() == 'y' and matched_ips:
        successful_pings = ping_ips(matched_ips)
        with open(f"Ping_Results_{name}.txt", 'w') as ping_file:
            for ip in successful_pings:
                ping_file.write(f"{ip}\n")
        print(f"Total IPs replied to ping for {name}: {len(successful_pings)}")
        print(f"Ping results have been saved to Ping_Results_{name}.txt")

# Ensure the script is running with Python 3
if sys.version_info[0] < 3:
    raise Exception("This script requires Python 3 or later")

# Read the IPs from ipaddress_isp.txt
isp_ips = read_ips('ipaddress_isp.txt')

# Define the prefix files and corresponding metadata
prefix_files_metadata = [
    ('IDCH-AS136052.txt', 'PT.CloudHosting', '136052'),
    ('AWANKILAT-AS138062.txt', 'PT.Awan Kilat Semesta', '138062'),
    ('CLOUDHOST-AS138608.txt', 'PT.Cloudhost Asia', '138608')
]

# Output file name
output_file = 'Blocked_TrustPositif.txt'

# Remove the output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

# Display the loading screen
loading_screen()

# Display the loading animation
loading_animation(5)

# Ask user if they want to ping the matched IPs
ping_option = input("Do you want to ping the matched IPs and save the results? (y/n): ")

# Process each prefix file and write the results
for prefix_file, name, as_number in prefix_files_metadata:
    match_and_write_results(prefix_file, isp_ips, name, as_number, output_file, ping_option)

print("\nDone")

print("\nMatched IP addresses have been written to Blocked_TrustPositif.txt")
