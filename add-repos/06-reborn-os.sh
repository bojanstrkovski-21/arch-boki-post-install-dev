#!/usr/bin/env bash


cd reborn-os

sudo pacman -U --needed --noconfirm \
rebornos-keyring-20240525-1-any.pkg.tar.zst \
rebornos-mirrorlist-20240513-1-any.pkg.tar.zst


echo -e "\n[Reborn-OS]\nServer = /etc/pacman.d/reborn-mirrorlist" | sudo tee -a /etc/pacman.conf
sudo pacman -Syy

# [Reborn-OS]
# SigLevel = Optional TrustAll
# Include = /etc/pacman.d/reborn-mirrorlist