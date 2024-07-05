#!/bin/bash

# Function to install PipeWire
install_pipewire() {
  sudo pacman -Rns --noconfirm pulseaudio pulseaudio-alsa pulseaudio-bluetooth pulseaudio-equalizer pulseaudio-jack pulseaudio-zeroconf pavucontrol alsa-firmware alsa-lib alsa-plugins alsa-utils alsa-topology-conf gstreamer gst-plugins-good gst-plugins-bad gst-plugins-base gst-plugins-ugly gst-libav gstreamer-vaapi cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore playerctl volumeicon 
  sudo pacman -Syu --noconfirm alsa-utils alsa-firmware alsa-plugins alsa-lib alsa-topology-conf gstreamer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly gstreamer-vaapi cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore pavucontrol pipewire pipewire-audio pipewire-docs pipewire-pulse pipewire-alsa pipewire-jack pipewire-zeroconf playerctl volumeicon wireplumber
}

# Function to install PulseAudio
install_pulseaudio() {
  sudo pacman -Rns --noconfirm alsa-utils alsa-firmware alsa-plugins alsa-lib alsa-topology-conf gstreamer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly gstreamer-vaapi cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore pavucontrol pipewire pipewire-audio pipewire-docs pipewire-pulse pipewire-alsa pipewire-jack pipewire-zeroconf playerctl volumeicon wireplumber  
  sudo pacman -Syu --noconfirm pulseaudio pulseaudio-alsa pulseaudio-bluetooth pulseaudio-equalizer pulseaudio-jack pulseaudio-zeroconf pavucontrol alsa-firmware alsa-lib alsa-plugins alsa-utils alsa-topology-conf gstreamer gst-plugins-good gst-plugins-bad gst-plugins-base gst-plugins-ugly gst-libav gstreamer-vaapi cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore playerctl volumeicon 
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