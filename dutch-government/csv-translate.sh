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


# Loop trough ever directory
while true; do
    echo -ne "Domain: "
    read domain

    subdomain_file="./subdomains/$domain/$domain-combined-subdomains.txt"

    if [ "$domain" == "exit" ]; then
        echo "Exiting..."
        break
    fi

    if [ -d "./subdomains/$domain" ]; then
        mkdir -p ./domain-csv
        sed 's/$/,/' ./subdomains/$domain/$domain-live-subdomains.txt | tee ./domain-csv/$domain.csv  > /dev/null 2>&1
    else
        echo "$domain directory doesn't exist"
    fi
    

done

