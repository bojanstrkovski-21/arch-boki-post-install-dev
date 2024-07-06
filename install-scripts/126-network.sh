#!/usr/bin/bash

# removing conflicting pkgs
sudo pacman -Rdd iptables-nft

# installing network pakgs
sudo pacman -S --needed --noconfirm \
avahi \
ethtool \
gnome-nettool \
iptables-nft \
net-tools \
netctl \
networkmanager \
networkmanager-openvpn \
network-manager-applet \
networkmanager-vpnc \
networkmanager-pptp \
networkmanager-openconnect \
nftables \
nm-connection-editor \
openresolv \
samba \
smb4k \
nfs-utils \
nfsidmap \
qemu-block-nfs \
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