#!/bin/bash
# Made by: Twan Terstappen
## SUBDOMAIN FINDER
# Date: 09-02-2024

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "This script needs to be run with sudo."
    exit 1
else
    echo "Script is running with sudo privileges."
fi

# Check if sublist3r is installed
if ! command -v sublist3r &> /dev/null; then
    echo "sublist3r is not installed. Please install sublist3r to use this script."
    exit 1
fi

# Check if subfinder is installed
if ! command -v subfinder &> /dev/null; then
    echo "subfinder is not installed. Please install subfinder to use this script."
    exit 1
fi


# Check if a parameter (filename) is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <domain(s)_filename>"
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
total_domains=$(wc -l < "$1")
processed_domains=0

# Find subdomains of a domain using sublist3r and subfinder
while read -r domain; do
  processed_domains=$((processed_domains + 1))
  progress=$((processed_domains * 100 / total_domains))

  subdomain_dir="./subdomains/$domain"

  # check if directory exists
  if [ ! -d "$subdomain_dir" ]; then
    mkdir -p "$subdomain_dir"

    # run sublist3r and subfinder
    sublist3r -d $domain -n -o "$subdomain_dir/$domain-sublist3r.txt" > /dev/null 2>&1
    subfinder -nc -silent -d $domain -o "$subdomain_dir/$domain-subfinder.txt" > /dev/null 2>&1

    # Check if both files are created. If not take one of the files and output it to the combined file
    if [ ! -f "$subdomain_dir/$domain-sublist3r.txt" ]; then
        cp "$subdomain_dir/$domain-subfinder.txt" "$subdomain_dir/$domain-combined-subdomains.txt"
    elif [ ! -f "$subdomain_dir/$domain-subfinder.txt" ]; then
        cp "$subdomain_dir/$domain-sublist3r.txt" "$subdomain_dir/$domain-combined-subdomains.txt"
    else
      # combine the files, remove duplicates, and reverse the order
      cat "$subdomain_dir/$domain-sublist3r.txt" "$subdomain_dir/$domain-subfinder.txt" | sort -u | tac > "$subdomain_dir/$domain-combined-subdomains.txt"
    fi

  else
      echo "Directory $subdomain_dir exists. Skipping domain..."
  fi
  # Display progress bar on a single line
  echo -ne "Progress: $progress% (Processed $processed_domains/$total_domains domains)\r"


done < "$1"

echo -e "\nSubdomain discovery completed."
