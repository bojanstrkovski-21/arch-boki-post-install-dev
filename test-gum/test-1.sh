#!/usr/bin/env bash

sudo pacman -S --needed --noconfirm gum figlet

figlet -f big "ArchBoki"

main_menu=$( gum choose "Update & Refresh" "Choose Desktop" "Install Core utils_drivers" "Install Apps" )

if [ "${main_menu}" = "Update & Refresh" ]; then
	update_refresh=$( gum choose "Refresh Mirrors" "Update System" "Add arch-boki Repos" "Add ArcoLinux_repos" "Add Chaotic_repos" "Install ArcoLinux Apps (add repos first!)" "Fix pacman-db-keys" )
fi

if [ "${update_refresh}" = "Refresh Mirrors" ]; then
	sudo pacman -Syy

elif [ "${update_refresh}" = "Update System" ]; then

	sudo pacman -Syyu

elif [ "${update_refresh}" = "Add arch-boki-repos" ]; then
	echo -e "\n[shtrkce-repo]\nSigLevel = Optional TrustAll\nServer = https://bojanstrkovski-21.github.io/\$repo/\$arch\n" | sudo tee -a /etc/pacman.conf
	echo -e "\n[shtrkce_repo_xl]\nSigLevel = Optional TrustAll\nServer = https://gitlab.com/bojanstrkovski-21/\$repo/-/raw/main/\$arch\n" | sudo tee -a /etc/pacman.conf
	sudo pacman -Syy

elif [ "${update_refresh}" = "Add arch-boki Repos" ]; then

	sudo pacman -Sy
	sudo pacman -S wget --noconfirm --needed
	sudo pacman -S jq --noconfirm --needed
	arco_repo_db=$(wget -qO- https://api.github.com/repos/arcolinux/arcolinux_repo/contents/x86_64)
	echo "Getting the ArcoLinux keys from the ArcoLinux repo"

	sudo wget "$(echo "$arco_repo_db" | jq -r '[.[] | select(.name | contains("arcolinux-keyring")) | .name] | .[0] | sub("arcolinux-keyring-"; "https://github.com/arcolinux/arcolinux_repo/raw/main/x86_64/arcolinux-keyring-")')" -O /tmp/arcolinux-keyring-git-any.pkg.tar.zst
	sudo pacman -U --noconfirm --needed /tmp/arcolinux-keyring-git-any.pkg.tar.zst

	echo "Getting the latest arcolinux mirrors file"

	sudo wget "$(echo "$arco_repo_db" | jq -r '[.[] | select(.name | contains("arcolinux-mirrorlist-git-")) | .name] | .[0] | sub("arcolinux-mirrorlist-git-"; "https://github.com/arcolinux/arcolinux_repo/raw/main/x86_64/arcolinux-mirrorlist-git-")')" -O /tmp/arcolinux-mirrorlist-git-any.pkg.tar.zst
	sudo pacman -U --noconfirm --needed /tmp/arcolinux-mirrorlist-git-any.pkg.tar.zst

	if grep -q arcolinux_repo /etc/pacman.conf; then

	  echo
	  tput setaf 2
	  echo "################################################################"
	  echo "################ ArcoLinux repos are already in /etc/pacman.conf "
	  echo "################################################################"
	  tput sgr0
	  echo

	else

	echo '

	#[arcolinux_repo_testing]
	#SigLevel = PackageRequired DatabaseNever
	#Include = /etc/pacman.d/arcolinux-mirrorlist

	[arcolinux_repo]
	SigLevel = PackageRequired DatabaseNever
	Include = /etc/pacman.d/arcolinux-mirrorlist

	[arcolinux_repo_3party]
	SigLevel = PackageRequired DatabaseNever
	Include = /etc/pacman.d/arcolinux-mirrorlist

	[arcolinux_repo_xlarge]
	SigLevel = PackageRequired DatabaseNever
	Include = /etc/pacman.d/arcolinux-mirrorlist' | sudo tee --append /etc/pacman.conf

	fi

elif [ "${update_refresh}" = "Add Chaotic_repos" ]; then 
	sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
	sudo p	acman-key --lsign-key 3056513887B78AEB
	sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
	sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
	echo -e "\n[garuda]\nSigLevel = Required DatabaseOptional\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf
	echo -e "\n[chaotic-aur]\nSigLevel = Required DatabaseOptional\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf
	sudo pacman -Syy

elif [ "${update_refresh}" = "Install ArcoLinux Apps (add repos first!)" ]; then 
	sudo pacman -Syy --needed --noconfirm archlinux-tweak-tool-git arcolinux-app-glade-git sofirem-git

elif [ "${update_refresh}" = "Fix pacman-db-keys" ]; then
	Online=0

	function check_connectivity() {
	
	    local test_ip
	    local test_count
	
	    test_ip="8.8.8.8"
	    test_count=1
	
	    if ping -c ${test_count} ${test_ip} > /dev/null; then
	       	tput setaf 2
	       	echo 
	       	echo "You are online"
	       	echo
	       	tput sgr0
	       	Online=1
	    else
	    	tput setaf 1
	    	echo
	       	echo "You are not connected to the internet"
	       	echo "We can not download the latest archlinux-keyring package"
	       	echo
	       	echo "Make sure you are online to retrieve packages"
	       	echo
	       	tput sgr0
	       	Online=0
	    fi
	 }
	
	check_connectivity
	
	if [ $Online -eq 1 ] ; then
		tput setaf 2
		echo
		echo "Installing the latest archlinux-keyring package from the internet"
		echo
		tput sgr0
		sudo pacman -Sy archlinux-keyring --noconfirm
		echo
	fi
	
	sudo rm /var/lib/pacman/sync/*
	sudo rm -rf /etc/pacman.d/gnupg/*
	sudo pacman-key --init
	sudo pacman-key --populate
	keyserver hkp://keyserver.ubuntu.com:80" | sudo tee --append /etc/pacman.d/gnupg/gpg.conf
	sudo pacman -Sy

else
	"echo "Unknown option: ${update_refresh}"
fi