#!/bin/bash

# Function to install PipeWire
install_pipewire() {
  sudo pacman -Rns --noconfirm pulseaudio pulseaudio-alsa pulseaudio-bluetooth
  sudo pacman -Syu --noconfirm pipewire pipewire-alsa pipewire-pulse pipewire-jack
}

# Function to install PulseAudio
install_pulseaudio() {
  sudo pacman -Rns --noconfirm pipewire pipewire-alsa pipewire-pulse pipewire-jack
  sudo pacman -Syu --noconfirm pulseaudio pulseaudio-alsa pulseaudio-bluetooth
}

# Prompt the user to choose between PipeWire and PulseAudio
echo "Which audio system would you like to install?"
echo "1) PipeWire"
echo "2) PulseAudio"
read -p "Enter your choice (1 or 2): " choice

case $choice in
  1)
    echo "Installing PipeWire..."
    install_pipewire
    ;;
  2)
    echo "Installing PulseAudio..."
    install_pulseaudio
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac

echo "Installation complete."