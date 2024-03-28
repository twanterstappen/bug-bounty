#!/bin/bash
# Made by: Twan Terstappen
## httprobe
# Date: 09-02-2024

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "This script needs to be run with sudo."
    exit 1
else
    echo "Script is running with sudo privileges."
fi

# Check if httprobe is installed
if ! command -v httprobe &> /dev/null; then
    echo "httprobe is not installed. Please install httprobe to use this script."
    exit 1
fi


# Function to handle Ctrl+C
function cleanup() {
    echo -e "\nReceived Ctrl+C. Exiting..."
    exit 1
}

# Set up trap to call cleanup function on Ctrl+C
trap cleanup SIGINT

# Count total number of lines/domains in the input file

total_domains=$(ls -1 ./subdomains | wc -l)
processed_domains=0

# Loop trough ever directory
while read -r domain; do
    processed_domains=$((processed_domains + 1))
    progress=$((processed_domains * 100 / total_domains))

    subdomain_file="./subdomains/$domain/$domain-combined-subdomains.txt"

    cat $subdomain_file | httprobe --prefer-https -t 4000 -c 50 | tee "./subdomains/$domain/$domain-live-subdomains.txt" > /dev/null 2>&1

    # Display progress bar on a single line
    echo -ne "Progress: $progress% (Processed $processed_domains/$total_domains domains)\r"


done < <(ls ./subdomains/ )

echo -e "\nSubdomain discovery completed."
