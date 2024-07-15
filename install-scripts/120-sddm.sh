#!/bin/bash


sudo pacman -S --noconfirm --needed sddm
sudo pacman -S --noconfirm --needed arch-boki-viper-grub-theme
sudo pacman -S --noconfirm --needed sddm-conf

sudo systemctl enable sddm.service --now