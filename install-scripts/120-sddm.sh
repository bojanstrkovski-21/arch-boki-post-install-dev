#!/bin/bash


sudo pacman -S --noconfirm --needed sddm
sudo pacman -S --noconfirm --needed arch-boki-viper-grub-theme

enable sddm.service -f