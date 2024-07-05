#!/usr/bin/bash	


# Check if pacutils is installed
# if ! command -v pacutils &> /dev/null; then
#     echo "pacutils is not installed, installing..."
#     # Use sudo to install pacutils with pacman
#     sudo pacman -S pacutils
# else
#     echo "pacutils is already installed."
# fi

sudo pacman -S --noconfirm --needed pacutils

# Install pulseaudio pkgs

sudo pacinstall --resolve-conflicts=all --no-confirm \
pulseaudio \
pulseaudio-alsa \
pulseaudio-bluetooth \
pulseaudio-equalizer \
pulseaudio-jack \
pulseaudio-zeroconf \
pavucontrol \
alsa-utils \
alsa-plugins \
alsa-firmware \
alsa-lib \
alsa-topology-conf \
gstreamer \
gst-libav \
gst-plugins-good \
gst-plugins-bad \
gst-plugins-base \
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
playerctl \
volumeicon \