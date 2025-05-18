#!/bin/bash

# ######################################################################################################################
# sudo pacman -Sy
# sudo pacman -S wget --noconfirm --needed
# sudo pacman -S jq --noconfirm --needed
# arco_repo_db=$(wget -qO- https://api.github.com/repos/arcolinux/arcolinux_repo/contents/x86_64)
# echo "Getting the ArcoLinux keys from the ArcoLinux repo"

# sudo wget "$(echo "$arco_repo_db" | jq -r '[.[] | select(.name | contains("arcolinux-keyring")) | .name] | .[0] | sub("arcolinux-keyring-"; "https://github.com/arcolinux/arcolinux_repo/raw/main/x86_64/arcolinux-keyring-")')" -O /tmp/arcolinux-keyring-git-any.pkg.tar.zst
# sudo pacman -U --noconfirm --needed /tmp/arcolinux-keyring-git-any.pkg.tar.zst

# ######################################################################################################################

# echo "Getting the latest arcolinux mirrors file"

# sudo wget "$(echo "$arco_repo_db" | jq -r '[.[] | select(.name | contains("arcolinux-mirrorlist-git-")) | .name] | .[0] | sub("arcolinux-mirrorlist-git-"; "https://github.com/arcolinux/arcolinux_repo/raw/main/x86_64/arcolinux-mirrorlist-git-")')" -O /tmp/arcolinux-mirrorlist-git-any.pkg.tar.zst
# sudo pacman -U --noconfirm --needed /tmp/arcolinux-mirrorlist-git-any.pkg.tar.zst

# if grep -q arcolinux_repo /etc/pacman.conf; then

#   echo
#   tput setaf 2
#   echo "################################################################"
#   echo "################ ArcoLinux repos are already in /etc/pacman.conf "
#   echo "################################################################"
#   tput sgr0
#   echo

# else

# echo '

# #[arcolinux_repo_testing]
# #SigLevel = PackageRequired DatabaseNever
# #Include = /etc/pacman.d/arcolinux-mirrorlist

# [arcolinux_repo]
# SigLevel = PackageRequired DatabaseNever
# Include = /etc/pacman.d/arcolinux-mirrorlist

# [arcolinux_repo_3party]
# SigLevel = PackageRequired DatabaseNever
# Include = /etc/pacman.d/arcolinux-mirrorlist

# [arcolinux_repo_xlarge]
# SigLevel = PackageRequired DatabaseNever
# Include = /etc/pacman.d/arcolinux-mirrorlist' | sudo tee --append /etc/pacman.conf

# fi

#!/bin/bash
#set -e
##################################################################################################################
# Author  : Erik Dubois
# Website   : https://www.erikdubois.be
# Website   : https://www.alci.online
# Website : https://www.arcolinux.info
# Website : https://www.arcolinux.com
# Website : https://www.arcolinuxd.com
# Website : https://www.arcolinuxb.com
# Website : https://www.arcolinuxiso.com
# Website : https://www.arcolinuxforum.com
##################################################################################################################
#
#   DO NOT JUST RUN THIS. EXAMINE AND JUDGE. RUN AT YOUR OWN RISK.
#
##################################################################################################################
#tput setaf 0 = black 
#tput setaf 1 = red 
#tput setaf 2 = green
#tput setaf 3 = yellow 
#tput setaf 4 = dark blue 
#tput setaf 5 = purple
#tput setaf 6 = cyan 
#tput setaf 7 = gray 
#tput setaf 8 = light blue
##################################################################################################################

#iso=arcolinux

#!/usr/bin/bash

echo -e "\n[nemesis_repo]\nSigLevel = Never\nServer = https://erikdubois.github.io/$repo/$arch" | sudo tee -a /etc/pacman.conf
echo -e "\n[arcolinux_repo]\nSigLevel = Never\nServer = https://arcolinux.github.io/$repo/$arch" | sudo tee -a /etc/pacman.conf
echo -e "\n[arcolinux_repo_3party]\nSigLevel = Never\nServer = https://arcolinux.github.io/$repo/$arch" | sudo tee -a /etc/pacman.conf
sudo pacman -Syy
