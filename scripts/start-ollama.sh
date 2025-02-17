#!/bin/bash

# Create a larger swap file (4GB)
dd if=/dev/zero of=/swapfile bs=1M count=4096
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Show memory info for debugging
free -h
swapon --show

# Start Ollama
/usr/bin/ollama serve 