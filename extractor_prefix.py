import sys
import ipaddress

# Function to extract IPs from the selected file
def extract_ips(file_name):
    with open(file_name, 'r') as f:
        prefixes = [line.strip() for line in f]

    extracted_ips = []
    for prefix in prefixes:
        network = ipaddress.ip_network(prefix)
        extracted_ips.extend([str(ip) for ip in network.hosts()])

    output_file = f'extracted_ips_{file_name}'
    with open(output_file, 'w') as f:
        for ip in extracted_ips:
            f.write(ip + '\n')

    print(f"IP addresses have been extracted to {output_file}")

# Ensure the script is running with Python 3
if sys.version_info[0] < 3:
    raise Exception("This script requires Python 3 or later")

# Menu for selecting the file
print("Select the IP list to process:")
print("1. IDCH-AS136052")
print("2. AWANKILAT-AS138062")
print("3. CLOUDHOST-AS138608")

choice = input("Enter the number of your choice: ")

file_map = {
    '1': 'IDCH-AS136052.txt',
    '2': 'AWANKILAT-AS138062.txt',
    '3': 'CLOUDHOST-AS138608.txt'
}

if choice in file_map:
    selected_file = file_map[choice]
    extract_ips(selected_file)
else:
    print("Invalid choice. Please run the script again and select a valid option.")
