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
    wc -l ./subdomains/$domain/$domain-live-subdomains.txt | awk '{print $1}' | xargs -I {} echo "$domain,{}" | tee -a ./domain-csv/subdomains.csv > /dev/null 2>&1
    
done < <(ls ./subdomains/ )

echo -e "\nSubdomain discovery completed."
