#!/usr/bin/bash	


# # Check if pacutils is installed

# if ! command -v pacutils &> /dev/null; then
#     echo "pacutils is not installed, installing..."
#     # Use sudo to install pacutils with pacman
#     sudo pacman -S pacutils
# else
#     echo "pacutils is already installed."
# fi

sudo pacman -S --noconfirm --needed pacutils

# Install pipewire pkgs 



sudo pacinstall --resolve-conflicts=all  --no-confirm  --notimeout \
alsa-utils \
alsa-firmware \
alsa-plugins \
alsa-lib \
gstreamer \
gst-libav \
gst-plugins-bad \
gst-plugins-base \
gst-plugins-good \
gst-plugins-ugly \
gstreamer-vaapi \
cdrdao \
faac \
faad2 \
ffmpeg \
ffmpegthumbnailer \
flac \
frei0r-plugins \
imagemagick \
lame \
libdvdcss \
libopenraw \
x265 \
x264 \
xvidcore \
pavucontrol \
pipewire \
pipewire-pulse \
pipewire-alsa \
pipewire-jack \
pipewire-zeroconf \
playerctl \
volumeicon