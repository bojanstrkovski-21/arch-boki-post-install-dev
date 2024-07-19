#!/bin/bash

# ASCII Art
ASCII_ART="


      █████╗ ██████╗  ██████╗██╗  ██╗      ██████╗  ██████╗ ██╗  ██╗██╗
     ██╔══██╗██╔══██╗██╔════╝██║  ██║      ██╔══██╗██╔═══██╗██║ ██╔╝██║
     ███████║██████╔╝██║     ███████║█████╗██████╔╝██║   ██║█████╔╝ ██║
     ██╔══██║██╔══██╗██║     ██╔══██║╚════╝██╔══██╗██║   ██║██╔═██╗ ██║
     ██║  ██║██║  ██║╚██████╗██║  ██║      ██████╔╝╚██████╔╝██║  ██╗██║
     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝
     
                                                
"

# Function to display the main menu
main_menu() {
    clear
    echo "$ASCII_ART"
    echo "                                Main Menu
    "
    echo "                          1. Update and Refresh
    "
    echo "                          2. Choose Desktop
    "
    echo "                          3. Install Core Utils and Drivers
    "
    echo "                          4. Install Apps
    "
    echo "                          5. Quit Arch-Boki post install
    "
    echo -n "                           Please choose an option: "
    read main_choice

    case $main_choice in
        1) update_and_refresh ;;
        2) choose_desktop ;;
        3) install_core_utils ;;
        4) install_apps ;;
        5) exit 0 ;;
        *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
    esac
}

# Function for "Update and Refresh" submenu
update_and_refresh() {
    while true; do
        clear
        echo "$ASCII_ART"
        echo "                              Update and Refresh
        "
        echo "                        1. Refresh Mirrors
        "
        echo "                        2. Update System
        "
        echo "                        3. Add arch-boki Repos
        "
        echo "                        4. Add ArcoLinux_repos
        "
        echo "                        5. Add Chaotic_repos
        "
        echo "                        6. Fix pacman_db_and_keys
        "
        echo "                        7. Install ArcoLinux Apps (add repos first!)
        "
        echo "                        8. Back to Main Menu
        "
        echo "                        9. Quit Arch-Boki post install
        "
        echo -n "                         Please choose an option: "
        read update_choice

        case $update_choice in
            1) refresh_mirrors_db ;;
            2) update_system ;;
            3) add_arch_boki_repos ;;
            4) add_arco_linux_repos ;;
            5) add_chaotic_linux_repos ;;
            6) fix-pacman-db-and-keys ;;
            7) install_arcolinux_apps.sh ;;
            8) return ;;
            9) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for "Choose Desktop"
choose_desktop() {
while true; do
    clear
    echo "$ASCII_ART"
    echo "                                  Choose Desktop
    "
    echo "                        1. Kde - Plasma
    "
    echo "                        2. Xfce
    "
    echo "                        3. Cinnamon
    "
    echo "                        4. Hyprland
    "
    echo "                        5. Back to Main Menu
    "
    echo "                        6. Quit Arch-Boki post install
    "
    echo -n "                         Please choose an option: "

    read update_choice

    case $update_choice in
        1) kde_plasma ;;
        2) xfce ;;
        3) cinnamon ;;
        4) hyprland ;;
        5) return ;;
        6) exit ;;
        *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
    esac
done

}

# Function for "Install Core Utils and Drivers"

install_core_utils() {
while true; do
    clear
    echo "$ASCII_ART"
    echo "                     Install Core Utils and Drivers
    "
    echo "                        1. Cpu Check and Install Microcode
    "
    echo "                        2. Install GPU Drivers
    "
    echo "                        3. Install Audio Drivers
    "
    echo "                        4. Install Bluetooth Drivers
    "
    echo "                        5. Install Network Drivers
    "
    echo "                        6. Install Printer Drivers
    "
    echo "                        7. Install Fonts
    "
    echo "                        8. Install Core Utils
    "
    echo "                        9. Back to Main Menu
    "
    echo "                       10. Quit Arch-Boki post install
    "
    echo -n "                        Please choose an option: "

    read update_choice

    case $update_choice in
        1) cpu-microde-install ;;
        2) gpu-drivers ;;
        3) audio-drivers ;;
        4) bluetooth-drivers ;;
        5) network-drivers ;;
        6) printer-drivers ;;
        7) fonts ;;
        8) core-utils ;;
        9) return ;;
       10) exit ;;
        *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
    esac
done
}

# Function for "Install Apps"
install_apps() {
    clear
    echo "$ASCII_ART"
    echo "Installing Apps..."
    ./install-scripts/130.apps.sh
    read -p "Press Enter to continue..."
}

# Function for "Refresh Mirrors"
refresh_mirrors_db() {
    clear
    echo "$ASCII_ART"
    echo "Refreshing Mirrors..."
    #sudo pacman -Syy
    ./add-repos/upd_servers.sh
    read -p "Press Enter to continue..."
}

# Function for "Add arch-boki Repos"
add_arch_boki_repos() {
    clear
    echo "$ASCII_ART"
    echo "Adding arch-boki Repos..."
    ./add-repos/append_archboki_repo.sh
    # Add your code to add repos here
    read -p "Press Enter to continue..."
}

# Functions for adding Arco and garuda and chaotic repos
add_arco_linux_repos() {
    clear
    echo "$ASCII_ART"
    echo "Adding add_arco_linux_repos..."
    ./add-repos/get-the-arcolinux-keys-and-repos.sh
    # Add your code to add repos here
    read -p "Press Enter to continue..."
}

add_chaotic_linux_repos() {
    clear
    echo "$ASCII_ART"
    echo "Adding chaotic_garuda_repos..."
    ./add-repos/install_and_append_chaotic_repo_and_keyrings.sh
    # Add your code to add repos here
    read -p "Press Enter to continue..."
}

# Function for fix archlinux-keyrings
fix-pacman-db-and-keys() {
    clear
    echo "$ASCII_ART"
    echo "Fixing pacman-db_and_keys..."
    ./add-repos/fix-pacman-databases-and-keys.sh
    # Add your code to add repos here
    read -p "Press Enter to continue..."
}

install_arcolinux_apps.sh() {
    clear
    echo "$ASCII_ART"
    echo "Installing ArchLinux TweakTool..."
    ./add-repos/install_arcolinux_apps.sh
    # Add your code to add repos here
    read -p "Press Enter to continue..."
}

# Function for "Update System"

update_system() {
    clear
    echo "$ASCII_ART"
    echo "Updating System..."
    sudo pacman -Syyu
    read -p "Press Enter to continue..."
}

# Choose Desktop Environment

kde_plasma() {
    clear
    echo "$ASCII_ART"
    echo "Installing Kde_Plasma..."
    ./choose-desktop/kde-plasma/install-kde-plasma.sh
    read -p "Press Enter to continue..."
}

xfce() {
    clear
    echo "$ASCII_ART"
    echo "Installing Kde_Plasma..."
    ./choose-desktop/xfce/install-xfce-and-sddm.sh
    read -p "Press Enter to continue..."
}

cinnamon() {
    clear
    echo "$ASCII_ART"
    echo "Installing Kde_Plasma..."
    ./choose-desktop/cinnamon/install_cinnamon.sh
    read -p "Press Enter to continue..."
}

hyprland() {
    clear
    echo "$ASCII_ART"
    echo "Installing Hyprland..."
    ./choose-desktop/hyprland-scripts/00-choices.sh
    read -p "Press Enter to continue..."
}


# Functions for Install Core Utils and Drivers

# Function for cpu-microde-install
cpu-microde-install() {
    clear
    echo "$ASCII_ART"
    echo "Installing Microcode..."
    ./core-utils/microcode.sh
    read -p "Press Enter to continue..."
}

# Function for gpu-drivers
gpu-drivers() {
    clear
    echo "$ASCII_ART"
    echo "Installing gpu-drivers..."
    ./core-utils/gpu-drivers.sh
    read -p "Press Enter to continue..."
}

# Function for audio-drivers
audio-drivers() {
    clear
    echo "$ASCII_ART"
    echo "Installing audio-drivers..."
    ./core-utils/audio-drivers.sh
    read -p "Press Enter to continue..."
}


# Function for bluetooth-drivers
bluetooth-drivers() {
    clear
    echo "$ASCII_ART"
    echo "Installing bluetooth-drivers..."
    ./install-scripts/123-bluetooth.sh
    read -p "Press Enter to continue..."
}


# Function for network-drivers
network-drivers() {
    clear
    echo "$ASCII_ART"
    echo "Installing network-drivers..."
    ./install-scripts/126-network.sh
    read -p "Press Enter to continue..."
}


# Function for installing fonts
fonts() {
    clear
    echo "$ASCII_ART"
    echo "Installing fonts..."
    ./install-scripts/125-fonts.sh
    read -p "Press Enter to continue..."
}

core-utils() {
    clear
    echo "$ASCII_ART"
    echo "Installing fonts..."
    ./install-scripts/118-core.sh
    read -p "Press Enter to continue..."
}

printer-drivers() {
    clear
    echo "$ASCII_ART"
    echo "Installing fonts..."
    ./install-scripts/124-printers.sh
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    main_menu
done
