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
        echo "                        7. Back to Main Menu
        "
        echo "                        8. Quit Arch-Boki post install
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
            7) return ;;
            8) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for "Choose Desktop"
choose_desktop() {
while true; do
    clear
    echo "$ASCII_ART"
    echo "Choose Desktop
    "
    echo "                        1. Kde - Plasma
    "
    echo "                        2. Xfce
    "
    echo "                        3. Cinnamon
    "
    echo "                        4. Hyprland
    "
    echo -n "                         Please choose an option: "
    read update_choice

    case $update_chice in
        1) kde_plasma ;;
        2) xfce ;;
        3) cinnamon ;;
        4) hyprland ;;
    esac
done

}

# Function for "Install Core Utils and Drivers"
install_core_utils() {
    clear
    echo "$ASCII_ART"
    echo "Install Core Utils and Drivers"
    echo "Functionality to install core utils and drivers will go here."
    read -p "Press Enter to continue..."
}

# Function for "Install Apps"
install_apps() {
    clear
    echo "$ASCII_ART"
    echo "Install Apps"
    echo "Functionality to install applications will go here."
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

fix-pacman-db-and-keys() {
    clear
    echo "$ASCII_ART"
    echo "Fixing pacman-db_and_keys..."
    ./add-repos/install_and_append_chaotic_repo_and_keyrings.sh
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

# Choose Desktop Envornment

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

# Main loop
while true; do
    main_menu
done
