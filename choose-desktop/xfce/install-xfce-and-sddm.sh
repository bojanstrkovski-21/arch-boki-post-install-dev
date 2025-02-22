#!/bin/bash

sudo pacman -S --noconfirm --needed \
xfce4 \
xfce4-goodies \
xfce4-artwork \
xfce4-screensaver \
mugshot \
accountsservice \
sddm \
sddm-conf \
neovim \
sublime-text-4 \
xed \
arcolinux-wallpapers-git \
archlinux-logout-git \
a-candy-beauty-icon-theme-git \
shtrkce-simplicity-sddm-theme \
arch-boki-viper-grub-theme-main \
arc-gtk-theme \
arc-icon-theme \
papirus-icon-theme \
bibata-cursor-theme-bin \
archboki-xfce-git \
xfce4-panel-profiles \
xfce4-docklike-plugin


sudo systemctl enable sddm.service --now