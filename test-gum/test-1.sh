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

# Clear screen and display ASCII art centered
clear
gum style --align center --margin="0 0 0 0" "$ASCII_ART"

# Function to display the main menu
main_menu() {
    echo ""
    gum style --align center --margin="0 50 0 5" "Main Menu"
    echo ""
    gum style --align center --margin="0 50 0 5" "1. Update and Refresh"
    gum style --align center --margin="0 50 0 5" "2. Choose Desktop"
    gum style --align center --margin="0 50 0 5" "3. Install Core Utils and Drivers"
    gum style --align center --margin="0 50 0 5" "4. Install Apps"
    gum style --align center --margin="0 50 0 5" "5. Quit Arch-Boki post install"
    echo ""
    gum style --align center --margin="0 50 0 5" --foreground 212 "Please choose an option: "
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
        gum style --align center "$ASCII_ART"
        echo ""
        gum style --align center "Update and Refresh"
        echo ""
        gum style --align center "1. Refresh Mirrors"
        gum style --align center "2. Update System"
        gum style --align center "3. Add arch-boki Repos"
        gum style --align center "4. Add ArcoLinux_repos"
        gum style --align center "5. Add Chaotic_repos"
        gum style --align center "6. Fix pacman_db_and_keys"
        gum style --align center "7. Install ArcoLinux Apps (add repos first!)"
        gum style --align center "8. Back to Main Menu"
        gum style --align center "9. Quit Arch-Boki post install"
        echo ""
        gum style --align center --foreground 212 "Please choose an option: "
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
        gum style --align center "$ASCII_ART"
        echo ""
        gum style --align center "Choose Desktop"
        echo ""
        gum style --align center "1. Kde - Plasma"
        gum style --align center "2. Xfce"
        gum style --align center "3. Cinnamon"
        gum style --align center "4. Hyprland"
        gum style --align center "5. Back to Main Menu"
        gum style --align center "6. Quit Arch-Boki post install"
        echo ""
        gum style --align center --foreground 212 "Please choose an option: "

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
        gum style --align center "$ASCII_ART"
        echo ""
        gum style --align center "Install Core Utils and Drivers"
        echo ""
        gum style --align center "1. Cpu Check and Install Microcode"
        gum style --align center "2. Install GPU Drivers"
        gum style --align center "3. Install Audio Drivers"
        gum style --align center "4. Install Bluetooth Drivers"
        gum style --align center "5. Install Network Drivers"
        gum style --align center "6. Install Printer Drivers"
        gum style --align center "7. Install Fonts"
        gum style --align center "8. Install Core Utils"
        gum style --align center "9. Back to Main Menu"
        gum style --align center "10. Quit Arch-Boki post install"
        echo ""
        gum style --align center --foreground 212 "Please choose an option: "

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
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Apps..."
    ./install-scripts/130.apps.sh
    read -p "Press Enter to continue..."
}

# Function for "Refresh Mirrors"
refresh_mirrors_db() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Refreshing Mirrors..."
    ./add-repos/upd_servers.sh
    read -p "Press Enter to continue..."
}

# Function for "Add arch-boki Repos"
add_arch_boki_repos() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Adding arch-boki Repos..."
    ./add-repos/append_archboki_repo.sh
    read -p "Press Enter to continue..."
}

# Functions for adding Arco and garuda and chaotic repos
add_arco_linux_repos() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Adding add_arco_linux_repos..."
    ./add-repos/get-the-arcolinux-keys-and-repos.sh
    read -p "Press Enter to continue..."
}

add_chaotic_linux_repos() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Adding chaotic_garuda_repos..."
    ./add-repos/install_and_append_chaotic_repo_and_keyrings.sh
    read -p "Press Enter to continue..."
}

# Function for fix archlinux-keyrings
fix-pacman-db-and-keys() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Fixing pacman-db_and_keys..."
    ./add-repos/fix-pacman-databases-and-keys.sh
    read -p "Press Enter to continue..."
}

install_arcolinux_apps.sh() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing ArchLinux TweakTool..."
    ./add-repos/install_arcolinux_apps.sh
    read -p "Press Enter to continue..."
}

# Function for "Update System"
update_system() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Updating System..."
    sudo pacman -Syyu
    read -p "Press Enter to continue..."
}

# Choose Desktop Environment
kde_plasma() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Kde_Plasma..."
    ./choose-desktop/kde-plasma/install-kde-plasma.sh
    read -p "Press Enter to continue..."
}

xfce() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Xfce..."
    ./choose-desktop/xfce/install-xfce-and-sddm.sh
    read -p "Press Enter to continue..."
}

cinnamon() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Cinnamon..."
    ./choose-desktop/cinnamon/install_cinnamon.sh
    read -p "Press Enter to continue..."
}

hyprland() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Hyprland..."
    ./choose-desktop/hyprland-scripts/00-choices.sh
    read -p "Press Enter to continue..."
}

# Functions for Install Core Utils and Drivers

cpu-microde-install() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Microcode..."
    ./core-utils/microcode.sh
    read -p "Press Enter to continue..."
}

gpu-drivers() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing GPU drivers..."
    ./core-utils/gpu-drivers.sh
    read -p "Press Enter to continue..."
}

audio-drivers() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Audio drivers..."
    ./core-utils/audio-drivers.sh
    read -p "Press Enter to continue..."
}

bluetooth-drivers() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Bluetooth drivers..."
    ./install-scripts/123-bluetooth.sh
    read -p "Press Enter to continue..."
}

network-drivers() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Network drivers..."
    ./install-scripts/126-network.sh
    read -p "Press Enter to continue..."
}

fonts() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Fonts..."
    ./install-scripts/125-fonts.sh
    read -p "Press Enter to continue..."
}

core-utils() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Core Utils..."
    ./install-scripts/118-core.sh
    read -p "Press Enter to continue..."
}

printer-drivers() {
    clear
    gum style --align center "$ASCII_ART"
    gum style --align center "Installing Printer drivers..."
    ./install-scripts/124-printers.sh
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    main_menu
done
