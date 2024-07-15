#!/bin/bash

# Function to install NVIDIA packages
install_nvidia() {
  sudo pacman -Syu --noconfirm nvidia-dkms nvidia-utils nvidia-settings
}

# Function to install AMD packages
install_amd() {
  sudo pacman -Syu --noconfirm xf86-video-amdgpu
}

# Detect GPU vendor
gpu_vendor=$(lspci | grep -E "VGA|3D" | grep -i "nvidia\|amd" | awk '{print $5}')

if [[ "$gpu_vendor" =~ "NVIDIA" ]]; then
  echo "NVIDIA GPU detected."
  install_nvidia
elif [[ "$gpu_vendor" =~ "AMD" ]]; then
  echo "AMD GPU detected."
  install_amd
else
  echo "Unknown or no supported GPU vendor detected."
  exit 1
fi

echo "Driver installation complete."