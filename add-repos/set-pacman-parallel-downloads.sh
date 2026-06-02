#!/bin/bash
read -rp "Parallel downloads (default 5): " num
num=${num:-5}

if ! [[ "$num" =~ ^[1-9][0-9]*$ ]]; then
    echo "Invalid number" >&2
    exit 1
fi

# Uncomment and set, or add under [options] if missing
if grep -q "^#\?ParallelDownloads" /etc/pacman.conf; then
    sudo sed -i "s/^#*ParallelDownloads.*/ParallelDownloads = $num/" /etc/pacman.conf
else
    sudo sed -i "/^\[options\]/a ParallelDownloads = $num" /etc/pacman.conf
fi

echo "ParallelDownloads set to $num"