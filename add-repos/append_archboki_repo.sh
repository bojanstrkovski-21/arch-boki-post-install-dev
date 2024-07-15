#!/usr/bin/bash

echo -e "\n[shtrkce-repo]\nSigLevel = Optional TrustAll\nServer = https://bojanstrkovski-21.github.io/\$repo/\$arch\n" | sudo tee -a /etc/pacman.conf
echo -e "\n[shtrkce_repo_xl]\nSigLevel = Optional TrustAll\nServer = https://gitlab.com/bojanstrkovski-21/\$repo/-/raw/main/\$arch\n" | sudo tee -a /etc/pacman.conf
sudo pacman -Syy