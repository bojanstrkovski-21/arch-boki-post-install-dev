#!/usr/bin/bash

# sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
# sudo pacman-key --lsign-key 3056513887B78AEB
# sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
# sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'

# [garuda]
# Include = /etc/pacman.d/chaotic-mirrorlist

# [chaotic-aur]
# Include = /etc/pacman.d/chaotic-mirrorlist

# echo -e "\n[garuda]\nSigLevel = Required DatabaseOptional\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf
# echo -e "\n[chaotic-aur]\nSigLevel = Required DatabaseOptional\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf
# sudo pacman -Syy

# Setup
# We start by retrieving the primary key to enable the installation of our keyring and mirror 

sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
sudo pacman-key --lsign-key 3056513887B78AEB


# This allows us to install our chaotic-keyring and chaotic-mirrorlist packages.

sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'

echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf

sudo pacman -Syy