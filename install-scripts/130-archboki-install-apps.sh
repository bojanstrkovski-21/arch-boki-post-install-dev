#!/bin/bash

sudo pacman -S gum --needed --noconfirm

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

# Function to display the install_apps menu
install_apps_menu() {
    echo ""
    gum style --align center --margin="0 0 0 5" "Install Apps Menu"
    echo ""
    gum style --align center --margin="0 0 0 5" "1. File Managers"
    gum style --align center --margin="0 0 0 5" "2. Terminal Emulators"
    gum style --align center --margin="0 0 0 5" "3. Text editors,pdf, office, dev_tools"
    gum style --align center --margin="0 0 0 5" "4. Internet"
    gum style --align center --margin="0 0 0 5" "5. Multimedia"
    gum style --align center --margin="0 0 0 5" "6. Graphics"
    gum style --align center --margin="0 0 0 5" "7. System Info/Monitoring"
    gum style --align center --margin="0 0 0 5" "8. System Tools"
    gum style --align center --margin="0 0 0 5" "9. Main Menu"
    gum style --align center --margin="0 0 0 5" "10. Quit Arch-Boki post install"
    echo ""
    read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" main_choice

    case $main_choice in
        1) file_managers ;;
        2) terminal_emulators ;;
        3) text_devt_office_pdf ;;
        4) internet ;;
        5) multimedia ;;
        6) graphics ;;
        7) system_info ;;
        8) system_tools ;;
        9) main_menu ;;
        10) exit 0 ;;
        *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
    esac
}

# Function for "File Managers" submenu
file_managers() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "File Managers"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Nemo file manager"
        gum style --align center --margin="0 0 0 5" "2. PcmanFM-gtk3"
        gum style --align center --margin="0 0 0 5" "3. PcmanFM-qt"
        gum style --align center --margin="0 0 0 5" "4. Thunar file manager"
        gum style --align center --margin="0 0 0 5" "5. Nautilus - gnome files"
        gum style --align center --margin="0 0 0 5" "6. Dolphin - Kde Plasma"
        gum style --align center --margin="0 0 0 5" "7. Yazi-Terminal"
        gum style --align center --margin="0 0 0 5" "8. Ranger-Terminal"
        gum style --align center --margin="0 0 0 5" "9. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "10. Main Menu"
        gum style --align center --margin="0 0 0 5" "11. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) nemo_file_manager ;;
            2) pcmanfm_gtk3 ;;
            3) pcmanfm_qt ;;
            4) thunar_file_manager ;;
            5) nautilus_gnome ;;
            6) dolphin ;;
            7) yazi_terminal ;;
            8) ranger_terminal ;;
            9) return ;;
            10) ./03.arch-boki-post-install-gum.sh ;;
            11) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for "Install nemo file manager"
nemo_file_manager() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Nemo File Manager..."
    sudo pacman -S --needed --noconfirm nemo nemo-compare nemo-fileroller nemo-image-converter nemo-preview nemo-share
    read -p "Press Enter to continue..."
}

# Function for "Install pcmanfm-gtk3 file manager"
pcmanfm_gtk3() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing PcmanFM-gtk3 File Manager..."
    sudo pacman -S --needed --noconfirm pcmanfm-gtk3
    read -p "Press Enter to continue..."
}

# Function for "Install pcmanfm-qt file manager"
pcmanfm_qt() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing PcmanFM-qt File Manager..."
    sudo pacman -S --needed --noconfirm pcmanfm-qt
    read -p "Press Enter to continue..."
}

# Function for "Install thunar file manager"
thunar_file_manager() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing thunar File Manager..."
    sudo pacman -S --needed --noconfirm thunar thunar-archive-plugin thunar-shares-plugin thunar-volman tumbler file-roller
    read -p "Press Enter to continue..."
}

# Function for "Install nautilus_gnome file manager"
nautilus_gnome() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Nautilus_Gnome File Manager..."
    sudo pacman -S --needed --noconfirm nautilus nautilus-share sushi nautilus-code-git nautilus-open-any-terminal
    read -p "Press Enter to continue..."
}

# Function for "Install dolphin file manager"
dolphin() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Dolphin File Manager..."
    sudo pacman -S --needed --noconfirm dolphin dolphin-plugins 
    read -p "Press Enter to continue..."
}

# Function for "Install yazi_terminal file manager"
yazi_terminal() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Yazi_Terminal File Manager..."
    sudo pacman -S --needed --noconfirm yazy 
    read -p "Press Enter to continue..."
}

# Function for "Install ranger_terminal file manager"
ranger_terminal() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Ranger_Terminal File Manager..."
    sudo pacman -S --needed --noconfirm ranger 
    read -p "Press Enter to continue..."
}

# Function for "Terminal emulators" submenu
terminal_emulators() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Terminal Emulators"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Alacritty"
        gum style --align center --margin="0 0 0 5" "2. Ghostty"
        gum style --align center --margin="0 0 0 5" "3. Kitty"
        gum style --align center --margin="0 0 0 5" "4. tilix"
        gum style --align center --margin="0 0 0 5" "5. Wezterm"
        gum style --align center --margin="0 0 0 5" "6. Xfce4-Terminal"
        gum style --align center --margin="0 0 0 5" "7. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "8. Main Menu"
        gum style --align center --margin="0 0 0 5" "9. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) alacritty ;;
            2) ghostty ;;
            3) kitty ;;
            4) tilix ;;
            5) wezterm ;;
            6) xfce4_terminal ;;
            7) return ;;
            8) ./03.arch-boki-post-install-gum.sh ;;
            9) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for "Install alacritty"
alacritty() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Alacritty Terminal..."
    sudo pacman -S --needed --noconfirm alacritty alacritty-themes imagemagick libsixel lsix 
    read -p "Press Enter to continue..."
}

# Function for "Install ghostty"
ghostty() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Ghostty Terminal..."
    sudo pacman -S --needed --noconfirm ghostty libsixel imagemagick lsix
    read -p "Press Enter to continue..."
}

# Function for "Install kitty"
kitty() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Kitty Terminal..."
    sudo pacman -S --needed --noconfirm kitty kitty-shell-integration libsixel lsix imagemagick
    read -p "Press Enter to continue..."
}

# Function for "Install tilix"
tilix() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Tilix Terminal..."
    sudo pacman -S --needed --noconfirm tilix
    read -p "Press Enter to continue..."
}

# Function for "Install wezterm"
wezterm() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Wezterm Terminal..."
    sudo pacman -S --needed --noconfirm wezterm-nightly-bin imagemagick
    read -p "Press Enter to continue..."
}

# Function for "Install xfce4-terminal"
xfce4_terminal() {
    clear
    gum style --align center --margin="0 0 0 0" "$ASCII_ART"
    gum style --align center --margin="0 0 0 5" "Installing Xfce4-Terminal Terminal..."
    sudo pacman -S --needed --noconfirm xfce4-terminal
    read -p "Press Enter to continue..."
}

# Function for "Text, Pdf, Dev_tools" submenu
text_devt_office_pdf() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Text, Pdf, Dev_tools"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Text editors"
        gum style --align center --margin="0 0 0 5" "2. Office suits"
        gum style --align center --margin="0 0 0 5" "3. Markdown editors"
        gum style --align center --margin="0 0 0 5" "4. Pdf viewers"
        gum style --align center --margin="0 0 0 5" "5. Dev Tools"
        gum style --align center --margin="0 0 0 5" "6. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "7. Main Menu"
        gum style --align center --margin="0 0 0 5" "8. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) text_edtors ;;
            2) office_suits ;;
            3) markdown_editors ;;
            4) pdf_viewers ;;
            5) devtools ;;
            6) return ;;
            7) ./03.arch-boki-post-install-gum.sh ;;
            8) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for "Text Editors" submenu
text_edtors() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Text Editors"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Emacs"
        gum style --align center --margin="0 0 0 5" "2. Geany"
        gum style --align center --margin="0 0 0 5" "3. Leafpad (Lxde)"
        gum style --align center --margin="0 0 0 5" "4. Mousepad (Xfce)"
        gum style --align center --margin="0 0 0 5" "5. Sublime-text-4"
        gum style --align center --margin="0 0 0 5" "6. Xed (Linux Mint)"
        gum style --align center --margin="0 0 0 5" "7. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "8. Main Menu"
        gum style --align center --margin="0 0 0 5" "9. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm emacs ;;
            2) sudo pacman -S --needed --noconfirm geany geany-plugins ;;
            3) sudo pacman -S --needed --noconfirm leafpad ;;
            4) sudo pacman -S --needed --noconfirm mousepad ;;
            5) sudo pacman -S --needed --noconfirm sublime-text-4 ;;
            6) sudo pacman -S --needed --noconfirm xed ;;
            7) return ;;
            8) ./03.arch-boki-post-install-gum.sh ;;
            9) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for "Office suits" submenu
office_suits() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Office suits"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. LibreOffice"
        gum style --align center --margin="0 0 0 5" "2. OnlyOffice"
        gum style --align center --margin="0 0 0 5" "3. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "4. Main Menu"
        gum style --align center --margin="0 0 0 5" "5. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm libreoffice-fresh ;;
            2) sudo pacman -S --needed --noconfirm onlyoffice ;;
            3) return ;;
            4) ./03.arch-boki-post-install-gum.sh ;;
            5) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for markdown editors submenu
markdown_editors() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Markdown Editors"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Affine"
        gum style --align center --margin="0 0 0 5" "2. Obsidian"
        gum style --align center --margin="0 0 0 5" "3. Qownnotes"
        gum style --align center --margin="0 0 0 5" "4. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "5. Main Menu"
        gum style --align center --margin="0 0 0 5" "6. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) yay -S affine-bin ;;
            2) sudo pacman -S --needed --noconfirm obsidian ;;
            3) sudo pacman -S --needed --noconfirm qownnotes ;;
            4) return ;;
            5) ./03.arch-boki-post-install-gum.sh ;;
            6) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for pdf viewers submenu
pdf_viewers() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Pdf Viewers"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Evince"
        gum style --align center --margin="0 0 0 5" "2. Okular"
        gum style --align center --margin="0 0 0 5" "3. Xpdf"
        gum style --align center --margin="0 0 0 5" "4. Xreader"
        gum style --align center --margin="0 0 0 5" "5. Zathura"
        gum style --align center --margin="0 0 0 5" "6. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "7. Main Menu"
        gum style --align center --margin="0 0 0 5" "8. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm evince ;;
            2) sudo pacman -S --needed --noconfirm okular ;;
            3) sudo pacman -S --needed --noconfirm xpdf ;;
            4) sudo pacman -S --needed --noconfirm xreader ;;
            5) sudo pacman -S --needed --noconfirm zathura ;;
            6) return ;;
            7) ./03.arch-boki-post-install-gum.sh ;;
            8) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for dev tools submenu
devtools() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Dev Tools"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Code"
        gum style --align center --margin="0 0 0 5" "2. Meld"
        gum style --align center --margin="0 0 0 5" "3. Notepadqq"
        gum style --align center --margin="0 0 0 5" "4. Pycharm-community-edition"
        gum style --align center --margin="0 0 0 5" "5. Vscodium"
        gum style --align center --margin="0 0 0 5" "6. Visual Studio Code"
        gum style --align center --margin="0 0 0 5" "7. Zed"
        gum style --align center --margin="0 0 0 5" "8. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "9. Main Menu"
        gum style --align center --margin="0 0 0 5" "10. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm code ;;
            2) sudo pacman -S --needed --noconfirm meld ;;
            3) sudo pacman -S --needed --noconfirm notepadqq ;;
            4) sudo pacman -S --needed --noconfirm pycharm-community-edition ;;
            5) sudo pacman -S --needed --noconfirm vscodium vscodium-marketplace ;;
            6) sudo pacman -S --needed --noconfirm visual-studio-code-bin ;;
            7) sudo pacman -S --needed --noconfirm zed ;;
            8) return ;;
            9) ./03.arch-boki-post-install-gum.sh ;;
            10) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for Internet submenu
internet() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Internet"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Communication/Social"
        gum style --align center --margin="0 0 0 5" "2. Web browsers"
        gum style --align center --margin="0 0 0 5" "3. Downloaders"
        gum style --align center --margin="0 0 0 5" "4. Recorders"
        gum style --align center --margin="0 0 0 5" "5. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "6. Main Menu"
        gum style --align center --margin="0 0 0 5" "7. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) comunication ;;
            2) web_browsers ;;
            3) downloaders ;;
            4) Recorders ;;
            5) return ;;
            6) ./03.arch-boki-post-install-gum.sh ;;
            7) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for comunication submenu
comunication() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Comunication/Social"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Discord"
        gum style --align center --margin="0 0 0 5" "2. Signal"
        gum style --align center --margin="0 0 0 5" "3. Telegram"
        gum style --align center --margin="0 0 0 5" "4. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "5. Main Menu"
        gum style --align center --margin="0 0 0 5" "6. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm discord ;;
            2) sudo pacman -S --needed --noconfirm signal-desktop ;;
            3) sudo pacman -S --needed --noconfirm telegram-desktop ;;
            4) return ;;
            5) ./03.arch-boki-post-install-gum.sh ;;
            6) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for web_browsers submenu
web_browsers() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Web Browsers"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Brave"
        gum style --align center --margin="0 0 0 5" "2. Chromium"
        gum style --align center --margin="0 0 0 5" "3. Firefox"
        gum style --align center --margin="0 0 0 5" "4. Firefox-esr"
        gum style --align center --margin="0 0 0 5" "5. Google Chrome"
        gum style --align center --margin="0 0 0 5" "6. Librewolf"
        gum style --align center --margin="0 0 0 5" "7. Qutebrowser"
        gum style --align center --margin="0 0 0 5" "8. Vivaldi"
        gum style --align center --margin="0 0 0 5" "9. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "10. Main Menu"
        gum style --align center --margin="0 0 0 5" "11. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm brave-bin ;;
            2) sudo pacman -S --needed --noconfirm chromium ;;
            3) sudo pacman -S --needed --noconfirm firefox ;;
            4) sudo pacman -S --needed --noconfirm firefox-esr ;;
            5) sudo pacman -S --needed --noconfirm google-chrome ;;
            6) sudo pacman -S --needed --noconfirm librewolf ;;
            7) sudo pacman -S --needed --noconfirm qutebrowser ;;
            8) sudo pacman -S --needed --noconfirm vivaldi vivaldi-ffmpeg-codecs ;;
            9) return ;;
            10) ./03.arch-boki-post-install-gum.sh ;;
            11) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for downloaders submenu
downloaders() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Downloaders"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Deluge-Gtk"
        gum style --align center --margin="0 0 0 5" "2. Ktorrent"
        gum style --align center --margin="0 0 0 5" "3. Qbittorrent"
        gum style --align center --margin="0 0 0 5" "4. Transmission-Gtk"
        gum style --align center --margin="0 0 0 5" "5. Transmission-Qt"
        gum style --align center --margin="0 0 0 5" "6. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "7. Main Menu"
        gum style --align center --margin="0 0 0 5" "8. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm deluge-gtk ;;
            2) sudo pacman -S --needed --noconfirm qbittorrent ;;
            3) sudo pacman -S --needed --noconfirm ktorrent ;;
            4) sudo pacman -S --needed --noconfirm transmission-gtk ;;
            5) sudo pacman -S --needed --noconfirm transmission-qt ;;
            6) return ;;
            7) ./03.arch-boki-post-install-gum.sh ;;
            8) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for recorders submenu
recorders() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Recorders"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Gpu-screen-recorder-gtk"
        gum style --align center --margin="0 0 0 5" "2. Hyprshot (hyprland-onmly)"
        gum style --align center --margin="0 0 0 5" "3. Kazam"
        gum style --align center --margin="0 0 0 5" "4. Obs-studio"
        gum style --align center --margin="0 0 0 5" "5. Peek"
        gum style --align center --margin="0 0 0 5" "6. Simplescreenrecorder"
        gum style --align center --margin="0 0 0 5" "7. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "8. Main Menu"
        gum style --align center --margin="0 0 0 5" "9. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm gpu-screen-recorder gpu-screen-recorder-gtk ;;
            2) sudo pacman -S --needed --noconfirm hyprshot ;;
            3) sudo pacman -S --needed --noconfirm kazam ;;
            4) sudo pacman -S --needed --noconfirm obs-studio ;;
            5) sudo pacman -S --needed --noconfirm peek ;;
            6) sudo pacman -S --needed --noconfirm simplescreenrecorder-qt6-git ;;
            7) return ;;
            8) ./03.arch-boki-post-install-gum.sh ;;
            9) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for Multimedia submenu
multimedia() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Multimedia"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Audio Players"
        gum style --align center --margin="0 0 0 5" "2. Video Players"
        gum style --align center --margin="0 0 0 5" "3. Audio Editors"
        gum style --align center --margin="0 0 0 5" "4. Video Editors"
        gum style --align center --margin="0 0 0 5" "4. Subtitle Editors"
        gum style --align center --margin="0 0 0 5" "5. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "6. Main Menu"
        gum style --align center --margin="0 0 0 5" "7. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) audio_players ;;
            2) video_players ;;
            3) audio_editors ;;
            4) video_editors ;;
            4) sutitle_editors ;;
            5) return ;;
            6) ./03.arch-boki-post-install-gum.sh ;;
            7) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for audio_plaeyers submenu
audio_plaeyers() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Audio Players"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Amberol"
        gum style --align center --margin="0 0 0 5" "2. Audacious"
        gum style --align center --margin="0 0 0 5" "3. Deadbeef"
        gum style --align center --margin="0 0 0 5" "4. Elisa"
        gum style --align center --margin="0 0 0 5" "5. G4music"
        gum style --align center --margin="0 0 0 5" "6. juk"
        gum style --align center --margin="0 0 0 5" "7. lollypop"
        gum style --align center --margin="0 0 0 5" "8. Pragha"
        gum style --align center --margin="0 0 0 5" "9. Rhythmbox"
        gum style --align center --margin="0 0 0 5" "10. Sayonara Player"
        gum style --align center --margin="0 0 0 5" "11. Strawberry"
        gum style --align center --margin="0 0 0 5" "12. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "13. Main Menu"
        gum style --align center --margin="0 0 0 5" "14. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm amberol ;;
            2) sudo pacman -S --needed --noconfirm audacious audacious-plugins ;;
            3) sudo pacman -S --needed --noconfirm deadbeef ;;
            4) sudo pacman -S --needed --noconfirm elisa ;;
            5) sudo pacman -S --needed --noconfirm g4music-git ;;
            6) sudo pacman -S --needed --noconfirm juk ;;
            7) sudo pacman -S --needed --noconfirm lollypop ;;
            8) sudo pacman -S --needed --noconfirm pragha ;;
            9) sudo pacman -S --needed --noconfirm rhythmbox ;;
            10) sudo pacman -S --needed --noconfirm sayonara-player ;;
            11) sudo pacman -S --needed --noconfirm strawberry ;;
            12) return ;;
            13) ./03.arch-boki-post-install-gum.sh ;;
            14) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for video_players submenu
video_players() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Video Players"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Celluloid"
        gum style --align center --margin="0 0 0 5" "2. Clapper"
        gum style --align center --margin="0 0 0 5" "3. Kodi"
        gum style --align center --margin="0 0 0 5" "4. Mpv"
        gum style --align center --margin="0 0 0 5" "5. Smplayer"
        gum style --align center --margin="0 0 0 5" "6. Vlc media player"
        gum style --align center --margin="0 0 0 5" "7. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "8. Main Menu"
        gum style --align center --margin="0 0 0 5" "9. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm celluloid ;;
            2) sudo pacman -S --needed --noconfirm clapper clapper-enhancers ;;
            3) sudo pacman -S --needed --noconfirm kodi ;;
            4) sudo pacman -S --needed --noconfirm mpv ;;
            5) sudo pacman -S --needed --noconfirm smplayer smplayer-skins smplayer-themes ;;
            6) sudo pacman -S --needed --noconfirm vlc vlc-plugin-a52dec vlc-plugin-aalib vlc-plugin-alsa vlc-plugin-aom vlc-plugin-archive vlc-plugin-aribb24 vlc-plugin-aribb25 vlc-plugin-ass vlc-plugin-avahi vlc-plugin-bluray vlc-plugin-caca vlc-plugin-cddb vlc-plugin-chromecast vlc-plugin-dav1d vlc-plugin-dbus vlc-plugin-dbus-screensave vlc-plugin-dca vlc-plugin-dvb vlc-plugin-dvd vlc-plugin-faad2 vlc-plugin-ffmpeg vlc-plugin-firewire vlc-plugin-flac vlc-plugin-fluidsynth vlc-plugin-freetype vlc-plugin-gme vlc-plugin-gnutls vlc-plugin-gstreamer vlc-plugin-inflate vlc-plugin-jack vlc-plugin-journal vlc-plugin-jpeg vlc-plugin-kate vlc-plugin-kwallet vlc-plugin-libsecret vlc-plugin-lirc vlc-plugin-live555 vlc-plugin-lua vlc-plugin-mad vlc-plugin-matroska vlc-plugin-mdns vlc-plugin-modplug vlc-plugin-mpeg2 vlc-plugin-mpg123 vlc-plugin-mtp vlc-plugin-musepack vlc-plugin-nfs vlc-plugin-notify vlc-plugin-ogg vlc-plugin-opus vlc-plugin-png vlc-plugin-pulse vlc-plugin-quicksync vlc-plugin-samplerate vlc-plugin-sdl vlc-plugin-sftp vlc-plugin-shout vlc-plugin-smb vlc-plugin-soxr vlc-plugin-speex vlc-plugin-srt vlc-plugin-svg vlc-plugin-tag vlc-plugin-theora vlc-plugin-twolame vlc-plugin-udev vlc-plugin-upnp vlc-plugin-vorbis vlc-plugin-vpx vlc-plugin-x264 vlc-plugin-x265 vlc-plugin-xml vlc-plugin-zvb ;;
            7) return ;;
            8) ./03.arch-boki-post-install-gum.sh ;;
            9) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for audio_editors submenu
audio_editors() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Audio Editors"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Ardour"
        gum style --align center --margin="0 0 0 5" "2. Audacity"
        gum style --align center --margin="0 0 0 5" "3. Kwave"
        gum style --align center --margin="0 0 0 5" "4. Lmms"
        gum style --align center --margin="0 0 0 5" "5. Openshot"
        gum style --align center --margin="0 0 0 5" "6. soundconverter"
        gum style --align center --margin="0 0 0 5" "7. reaper"
        gum style --align center --margin="0 0 0 5" "8. tenacity"
        gum style --align center --margin="0 0 0 5" "9. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "10. Main Menu"
        gum style --align center --margin="0 0 0 5" "11. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm ardour ;;
            2) sudo pacman -S --needed --noconfirm audacity ;;
            3) sudo pacman -S --needed --noconfirm kwave ;;
            4) sudo pacman -S --needed --noconfirm lmms ;;
            5) sudo pacman -S --needed --noconfirm openshot ;;
            6) sudo pacman -S --needed --noconfirm soundconverter ;;
            7) sudo pacman -S --needed --noconfirm reaper reapack sws ;;
            8) sudo pacman -S --needed --noconfirm tenacity ;;
            9) return ;;
            10) ./03.arch-boki-post-install-gum.sh ;;
            11) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for video_editors submenu
video_editors() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Video Editors"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. flowblade"
        gum style --align center --margin="0 0 0 5" "2. handbrake"
        gum style --align center --margin="0 0 0 5" "3. kdenlive"
        gum style --align center --margin="0 0 0 5" "4. losslesscut"
        gum style --align center --margin="0 0 0 5" "5. makemkv"
        gum style --align center --margin="0 0 0 5" "6. Openshot"
        gum style --align center --margin="0 0 0 5" "7. Shotcut"
        gum style --align center --margin="0 0 0 5" "8. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "9. Main Menu"
        gum style --align center --margin="0 0 0 5" "10. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm flowblade ;;
            2) sudo pacman -S --needed --noconfirm handbrake ;;
            3) sudo pacman -S --needed --noconfirm kdenlive ;;
            4) sudo pacman -S --needed --noconfirm losslesscut-bin ;;
            5) sudo pacman -S --needed --noconfirm makemkv mkvtoolnix-cli mkvtoolnix-gui ;;
            6) sudo pacman -S --needed --noconfirm Openshot ;;
            7) sudo pacman -S --needed --noconfirm shotcut;;
            8) return ;;
            9) ./03.arch-boki-post-install-gum.sh ;;
            10) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for subtitle_editors submenu
subtitle_editors() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Subtitle Editors"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Aegisub"
        gum style --align center --margin="0 0 0 5" "2. Subtitleedit"
        gum style --align center --margin="0 0 0 5" "3. Subtitlecomposer"
        gum style --align center --margin="0 0 0 5" "4. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "5. Main Menu"
        gum style --align center --margin="0 0 0 5" "6. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm aegisub ;;
            2) sudo pacman -S --needed --noconfirm subtitleedit ;;
            3) sudo pacman -S --needed --noconfirm subtitlecomposer ;;
            4) return ;;
            5) ./03.arch-boki-post-install-gum.sh ;;
            6) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for graphics submenu
graphics() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Graphics"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Photo/Image Viewers"
        gum style --align center --margin="0 0 0 5" "2. Photo/Image Editors"
        gum style --align center --margin="0 0 0 5" "3. Wallpaper/Backround Changer "
        gum style --align center --margin="0 0 0 5" "4. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "5. Main Menu"
        gum style --align center --margin="0 0 0 5" "6. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) photo_viewers ;;
            2) photo_editors ;;
            3) wallpaper_changer ;;
            4) return ;;
            5) ./03.arch-boki-post-install-gum.sh ;;
            6) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for photo_viewers submenu
photo_viewers() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Photo/Image Viewers"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Darktable"
        gum style --align center --margin="0 0 0 5" "2. Ephoto"
        gum style --align center --margin="0 0 0 5" "3. GPicView"
        gum style --align center --margin="0 0 0 5" "4. Gwenview"
        gum style --align center --margin="0 0 0 5" "5. Nomacs"
        gum style --align center --margin="0 0 0 5" "6. Nsxiv"
        gum style --align center --margin="0 0 0 5" "7. Qimgv"
        gum style --align center --margin="0 0 0 5" "8. Ristretto"
        gum style --align center --margin="0 0 0 5" "9. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "10. Main Menu"
        gum style --align center --margin="0 0 0 5" "11. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm darktable ;;
            2) sudo pacman -S --needed --noconfirm ephoto ;;
            3) sudo pacman -S --needed --noconfirm gpicview ;;
            4) sudo pacman -S --needed --noconfirm gwenview ;;
            5) sudo pacman -S --needed --noconfirm nomacs ;;
            6) sudo pacman -S --needed --noconfirm nsxiv ;;
            7) sudo pacman -S --needed --noconfirm qimgv-git;;
            8) sudo pacman -S --needed --noconfirm ristretto;;
            9) return ;;
            10) ./03.arch-boki-post-install-gum.sh ;;
            11) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for photo_editors submenu
photo_editors() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Photo/Image editors"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Gimp"
        gum style --align center --margin="0 0 0 5" "2. Gpick"
        gum style --align center --margin="0 0 0 5" "3. Inkscape"
        gum style --align center --margin="0 0 0 5" "4. Krita"
        gum style --align center --margin="0 0 0 5" "5. Pinta"
        gum style --align center --margin="0 0 0 5" "6. RawTherapee"
        gum style --align center --margin="0 0 0 5" "7. Upscayl"
        gum style --align center --margin="0 0 0 5" "8. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "9. Main Menu"
        gum style --align center --margin="0 0 0 5" "10. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm gimp ;;
            2) sudo pacman -S --needed --noconfirm gpick ;;
            3) sudo pacman -S --needed --noconfirm inkscape ;;
            4) sudo pacman -S --needed --noconfirm krita ;;
            5) sudo pacman -S --needed --noconfirm pinta ;;
            6) sudo pacman -S --needed --noconfirm rawtherapee ;;
            7) sudo pacman -S --needed --noconfirm upscayl-desktop-git upscayl-models-desktop ;;
            8) return ;;
            9) ./03.arch-boki-post-install-gum.sh ;;
            10) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for wallpaper_changer submenu
wallpaper_changer() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Wallpaper/Backround Changer"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Azote(nwg creators)"
        gum style --align center --margin="0 0 0 5" "2. Feh(terminal)"
        gum style --align center --margin="0 0 0 5" "3. Hyprpaper(hyprland)"
        gum style --align center --margin="0 0 0 5" "4. Nitrogen"
        gum style --align center --margin="0 0 0 5" "5. Swaybg(terminal-wayland"
        gum style --align center --margin="0 0 0 5" "6. Swww(terminal)"
        gum style --align center --margin="0 0 0 5" "7. Variety"
        gum style --align center --margin="0 0 0 5" "8. Waypaper(wayland-x11-gui)"
        gum style --align center --margin="0 0 0 5" "9. Xwallpaper(terminal)"
        gum style --align center --margin="0 0 0 5" "10. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "11. Main Menu"
        gum style --align center --margin="0 0 0 5" "12. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm azote ;;
            2) sudo pacman -S --needed --noconfirm feh ;;
            3) sudo pacman -S --needed --noconfirm hyprpaper ;;
            4) sudo pacman -S --needed --noconfirm nitrogen ;;
            5) sudo pacman -S --needed --noconfirm swaybg ;;
            6) sudo pacman -S --needed --noconfirm swww ;;
            7) sudo pacman -S --needed --noconfirm variety ;;
            8) sudo pacman -S --needed --noconfirm waypaper-git ;;
            9) sudo pacman -S --needed --noconfirm xwallpaper ;;
            10) return ;;
            11) ./03.arch-boki-post-install-gum.sh ;;
            12) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for system_info submenu
system_info() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "System Info/Monitoring"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Bashtop"
        gum style --align center --margin="0 0 0 5" "2. Btop"
        gum style --align center --margin="0 0 0 5" "3. Countryfetch"
        gum style --align center --margin="0 0 0 5" "4. Cpufetch"
        gum style --align center --margin="0 0 0 5" "5. Fastfetch"
        gum style --align center --margin="0 0 0 5" "6. Glances"
        gum style --align center --margin="0 0 0 5" "7. Gtop"
        gum style --align center --margin="0 0 0 5" "8. Htop"
        gum style --align center --margin="0 0 0 5" "9. Hyfetch"
        gum style --align center --margin="0 0 0 5" "10. Mission Center"
        gum style --align center --margin="0 0 0 5" "11. Nvtop"
        gum style --align center --margin="0 0 0 5" "12. Resources"
        gum style --align center --margin="0 0 0 5" "13. Stacer"
        gum style --align center --margin="0 0 0 5" "14. Xfce4-Taskmanager"
        gum style --align center --margin="0 0 0 5" "15. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "16. Main Menu"
        gum style --align center --margin="0 0 0 5" "17. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm bashtop ;;
            2) sudo pacman -S --needed --noconfirm btop ;;
            3) sudo pacman -S --needed --noconfirm countryfetch ;;
            4) sudo pacman -S --needed --noconfirm cpufetch ;;
            5) sudo pacman -S --needed --noconfirm fastfetch ;;
            6) sudo pacman -S --needed --noconfirm glances ;;
            7) sudo pacman -S --needed --noconfirm gtop ;;
            8) sudo pacman -S --needed --noconfirm htop ;;
            9) sudo pacman -S --needed --noconfirm hyfetch ;;
            10) sudo pacman -S --needed --noconfirm mission-center ;;
            11) sudo pacman -S --needed --noconfirm nvtop ;;
            12) sudo pacman -S --needed --noconfirm resources ;;
            13) yay -S --needed --noconfirm stacer-bin ;;
            14) sudo pacman -S --needed --noconfirm xfce4-taskmanager ;;
            15) return ;;
            16) ./03.arch-boki-post-install-gum.sh ;;
            17) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for System Tools submenu
system_tools() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "System Tools"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. App Launchers"
        gum style --align center --margin="0 0 0 5" "2. Calculators"
        gum style --align center --margin="0 0 0 5" "3. Partition tools"
        gum style --align center --margin="0 0 0 5" "4. Screen Shooters"
        gum style --align center --margin="0 0 0 5" "5. Screen Resolution Setters"
        gum style --align center --margin="0 0 0 5" "6. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "7. Main Menu"
        gum style --align center --margin="0 0 0 5" "8. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) app_launchers ;;
            2) calaculators ;;
            3) partition_tools ;;
            4) screen_shooters ;;
            5) screen_resolution ;;
            6) return ;;
            7) ./03.arch-boki-post-install-gum.sh ;;
            8) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for app_launchers submenu
app_launchers() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "App Launchers"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Bemenu"
        gum style --align center --margin="0 0 0 5" "2. Bemenu-Wayland"
        gum style --align center --margin="0 0 0 5" "3. Dmenu(it is better to clone and build)"
        gum style --align center --margin="0 0 0 5" "4. Fuzzel"
        gum style --align center --margin="0 0 0 5" "5. Rofi"
        gum style --align center --margin="0 0 0 5" "6. Rofi-Wayland"
        gum style --align center --margin="0 0 0 5" "7. Tofi"
        gum style --align center --margin="0 0 0 5" "8. Walker"
        gum style --align center --margin="0 0 0 5" "9. Wofi"
        gum style --align center --margin="0 0 0 5" "10. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "11. Main Menu"
        gum style --align center --margin="0 0 0 5" "12. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm bemenu ;;
            2) sudo pacman -S --needed --noconfirm bemenu-wayland ;;
            3) sudo pacman -S --needed --noconfirm dmenu ;;
            4) sudo pacman -S --needed --noconfirm fuzzel ;;
            5) sudo pacman -S --needed --noconfirm rofi ;;
            6) sudo pacman -S --needed --noconfirm rofi-wayland ;;
            7) sudo pacman -S --needed --noconfirm tofi ;;
            8) sudo pacman -S --needed --noconfirm walker-bin ;;
            9) sudo pacman -S --needed --noconfirm wofi ;;
            10) return ;;
            11) ./03.arch-boki-post-install-gum.sh ;;
            12) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for calculators submenu
calculators() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Calculators"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Galculator"
        gum style --align center --margin="0 0 0 5" "2. Gnome Calculator"
        gum style --align center --margin="0 0 0 5" "3. Qalculate-Gtk"
        gum style --align center --margin="0 0 0 5" "4. Qalculate-Qt"
        gum style --align center --margin="0 0 0 5" "5. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "6. Main Menu"
        gum style --align center --margin="0 0 0 5" "7. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm gnome-calculator ;;
            2) sudo pacman -S --needed --noconfirm galculator ;;
            3) sudo pacman -S --needed --noconfirm qalculate-gtk ;;
            4) sudo pacman -S --needed --noconfirm qalculate-qt ;;
            5) return ;;
            6) ./03.arch-boki-post-install-gum.sh ;;
            7) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for partition_tools submenu
partition_tools() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Partition Tools"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Kde Partition Manager"
        gum style --align center --margin="0 0 0 5" "2. Gnome Disks Utility"
        gum style --align center --margin="0 0 0 5" "3. Gparted"
        gum style --align center --margin="0 0 0 5" "4. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "5. Main Menu"
        gum style --align center --margin="0 0 0 5" "6. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm partitionmanager ;;
            2) sudo pacman -S --needed --noconfirm gnome-disk-utility ;;
            3) sudo pacman -S --needed --noconfirm gparted ;;
            4) return ;;
            5) ./03.arch-boki-post-install-gum.sh ;;
            6) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for screen_shooters submenu
screen_shooters() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Screen Shooters"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Flameshot"
        gum style --align center --margin="0 0 0 5" "2. Kazam"
        gum style --align center --margin="0 0 0 5" "3. Ksnip"
        gum style --align center --margin="0 0 0 5" "4. Shutter"
        gum style --align center --margin="0 0 0 5" "5. Spectacle"
        gum style --align center --margin="0 0 0 5" "6. Xfce4-screenshooter"
        gum style --align center --margin="0 0 0 5" "7. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "8. Main Menu"
        gum style --align center --margin="0 0 0 5" "9. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm flameshot ;;
            2) sudo pacman -S --needed --noconfirm kazam ;;
            3) sudo pacman -S --needed --noconfirm ksnip ;;
            4) sudo pacman -S --needed --noconfirm shutter ;;
            5) sudo pacman -S --needed --noconfirm spectacle ;;
            6) sudo pacman -S --needed --noconfirm xfce4-screenshooter ;;
            7) return ;;
            8) ./03.arch-boki-post-install-gum.sh ;;
            9) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Function for screen_resolution submenu
screen_resolution() {
    while true; do
        clear
        gum style --align center --margin="0 0 0 0" "$ASCII_ART"
        echo ""
        gum style --align center --margin="0 0 0 5" "Screen Resolution"
        echo ""
        gum style --align center --margin="0 0 0 5" "1. Arandr(gui x11)"
        gum style --align center --margin="0 0 0 5" "2. nwg-displays(hyprland-sway-nwg-shell only)"
        gum style --align center --margin="0 0 0 5" "3. wdisplays(gui wayland)"
        gum style --align center --margin="0 0 0 5" "3. wlr-randr(cli wayland)"
        gum style --align center --margin="0 0 0 5" "4. xorg-xrandr(cli x11)"
        gum style --align center --margin="0 0 0 5" "5. Back to install_apps"
        gum style --align center --margin="0 0 0 5" "6. Main Menu"
        gum style --align center --margin="0 0 0 5" "7. Quit Arch-Boki install_apps"
        echo ""
        read -p "$(gum style --align center --margin="1 0 0 5" --foreground 212 "Please choose an option: ")" update_choice

        case $update_choice in
            1) sudo pacman -S --needed --noconfirm arandr ;;
            2) sudo pacman -S --needed --noconfirm nwg-displays ;;
            3) sudo pacman -S --needed --noconfirm wdisplays ;;
            4) sudo pacman -S --needed --noconfirm wlr-randr ;;
            4) sudo pacman -S --needed --noconfirm xorg-xrandr ;;
            5) return ;;
            6) ./03.arch-boki-post-install-gum.sh ;;
            7) exit ;;
            *) echo "Invalid option!"; read -p "Press Enter to continue..." ;;
        esac
    done
}

# Main loop
while true; do
    install_apps_menu
done