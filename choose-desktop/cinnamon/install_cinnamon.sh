#!/bin/bash

sudo pacman -S --noconfirm --needed \
cinnamon \
cinnamon-translations \
gnome-screenshot \
gnome-system-monitor \
gnome-terminal \
xfce4-terminal \
iso-flag-png \
mintlocale \
nemo-fileroller \
xed \
mugshot \
accountsservice \
sddm \
sddm-conf \
arcolinux-wallpapers-git \
archlinux-logout-git \
a-candy-beauty-icon-theme-git \
shtrkce-simplicity-sddm-theme \
arch-boki-viper-grub-theme-main \
arc-gtk-theme \
arc-icon-theme \
papirus-icon-theme \
bibata-cursor-theme-bin


sudo systemctl enable sddm.service --now