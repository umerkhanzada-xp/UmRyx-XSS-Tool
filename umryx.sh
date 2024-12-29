#!/bin/bash

# Author: Umer Khanzada
# Tool: UmRyx - Fast Recon Bug Bounty Tool

# Check if required tools are installed
required_tools=("figlet" "gau" "gf" "uro" "Gxss" "kxss" "python3")
for tool in "${required_tools[@]}"; do
    if ! command -v $tool &> /dev/null; then
        echo "[!] $tool is not installed. Please install it to use this tool."
        exit 1
    fi
done

# Display a banner with Muhammad Umer's name in a centered large ASCII art
clear
figlet -c "Um-Ryx"
echo "============================================="
echo "           Developed by Umer Khanzada        "
echo "============================================="

echo "[+] Welcome to UmRyx, your automated reconnaissance tool!"
echo "[+] Starting automated reconnaissance..."

# Ask for the target domain
echo -n "Enter target domain: "
read target_domain

# Show loading animation
echo -n "[+] Initializing"
for i in {1..5}; do
    echo -n "."; sleep 0.5
done
echo " Done!"

# Methodology: Chain commands for reconnaissance
echo "[+] Running reconnaissance methodology..."
echo $target_domain | gau | gf xss | uro | Gxss | kxss | tee xss_output.txt

# Show a loading animation for processing results
echo -n "[+] Processing results"
for i in {1..3}; do
    echo -n "."; sleep 0.5
done
echo " Done!"

# Post-processing: Extract unique URLs
cat xss_output.txt | grep -oP '^URL: \K\S+' | sed 's/=.*/=/' | sort -u > final.txt

# Check if final.txt is created successfully
if [[ -f "final.txt" ]]; then
    echo "[+] final.txt saved in the current directory."
else
    echo "[!] Error: Failed to generate final.txt"
    exit 1
fi

# Stop after generating final.txt
echo "[+] Recon complete. Stopping after generating final.txt."

# Automatically start the XSS scanner with the generated final.txt
echo "[+] Starting XSS scanner..."
python3 xss_scanner.py

