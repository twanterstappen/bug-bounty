#!/bin/bash

# Specify the directory where your domains directories are located
base_dir="/home/kali/bugbounty/dutch-government/subdomains"

# Iterate through each directory
for dir in "$base_dir"/*/; do
    if [ -d "$dir" ]; then  # Check if it's a directory
        # Extract the directory name
        domain=$(basename "$dir")
        
        # Check if $domain-live.txt exists in the directory
        if [ -f "$dir/$domain-live-subdomains.txt" ]; then
            # Run wc -l on $domain-live.txt
            line_count=$(wc -l < "$dir/$domain-live-subdomains.txt")
            echo "Line count for $domain-live.txt in directory $dir: $line_count"
        else
            echo "Error: $domain-live.txt not found in directory $dir"
        fi
    fi
done
