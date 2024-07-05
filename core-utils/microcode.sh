#!/bin/bash

# Function to install microcode package
install_microcode() {
  local package_name=$1
  sudo pacman -Syu --noconfirm $package_name
}

# Detect CPU vendor
cpu_vendor=$(lscpu | grep "Vendor ID" | awk '{print $3}')

if [ "$cpu_vendor" == "GenuineIntel" ]; then
  echo "Intel CPU detected."
  install_microcode "intel-ucode"
elif [ "$cpu_vendor" == "AuthenticAMD" ]; then
  echo "AMD CPU detected."
  install_microcode "amd-ucode"
else
  echo "Unknown CPU vendor: $cpu_vendor"
  exit 1
fi

echo "Microcode installation complete."