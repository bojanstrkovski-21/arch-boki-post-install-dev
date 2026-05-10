#!/usr/bin/bash

# removing conflicting pkgs
sudo pacman -Rdd iptables

# installing network pakgs
sudo pacman -S --needed --noconfirm \
iptables-nft \
avahi \
ethtool \
net-tools \
netctl \
networkmanager \
networkmanager-openvpn \
network-manager-applet \
networkmanager-openconnect \
nftables \
nm-connection-editor \
openresolv \
samba \
nfs-utils \
nfsidmap \
mkinitcpio-nfs-utils \
libnfs \
gvfs \
gvfs-afc \
gvfs-goa \
gvfs-gphoto2 \
gvfs-mtp \
gvfs-nfs \
gvfs-smb \
nss-mdns \
file-roller \
webkit2gtk 


# sudo pacman -S --needed nm-tray --noconfir
