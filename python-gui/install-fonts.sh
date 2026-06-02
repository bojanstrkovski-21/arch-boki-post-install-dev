#!/bin/bash
# DESC: Install regular fonts and/or Nerd Fonts with interactive selection

# Set color variables for better readability
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required dependencies
check_dependencies() {
    local deps=("wget" "unzip")
    
    for dep in "${deps[@]}"; do
        if ! command_exists "$dep"; then
            echo -e "${YELLOW}Installing required dependency: $dep${NC}"
            sudo pacman -Sy "$dep" || { 
                echo -e "${RED}Failed to install $dep. Please install it manually.${NC}"
                exit 1
            }
        fi
    done
    echo -e "${GREEN}All dependencies are satisfied.${NC}"
}

# Array of regular fonts with their package names
declare -A regular_fonts=(
    [1]="ttf-croscore"
    [2]="ttf-carlito"
    [3]="ttf-caladea"
    [4]="opendesktop-fonts"
    [5]="inter-font"
    [6]="ttf-opensans"
    [7]="terminus-font"
    [8]="freetype2"
    [9]="ttf-ms-fonts"
    [10]="ttf-mac-fonts"
    [11]="ttf-macedonian-ancient"
    [12]="ttf-macedonian-church"
    [13]="ttf-material-design-iconic-font"
    [14]="otf-font-awesome"
    [15]="ttf-font-awesome-6"
    [16]="noto-fonts"
    [17]="noto-fonts-cjk"
    [18]="noto-fonts-emoji"
    [19]="noto-fonts-extra"
    [20]="ttf-anonymous-pro"
    [21]="ttf-cascadia-code"
    [22]="ttf-dejavu"
    [23]="ttf-fantasque-sans-mono"
    [24]="ttf-fira-mono"
    [25]="ttf-fira-sans"
    [26]="ttf-fira-code"
    [27]="ttf-hack"
    [28]="ttf-hellvetica"
    [29]="ttf-jetbrains-mono"
    [30]="ttf-joypixels"
    [31]="ttf-roboto"
    [32]="ttf-roboto-mono"
    [33]="ttf-ubuntu-font-family"
)

# Array of Nerd Fonts
declare -a nerd_fonts=(
    "CascadiaCode"
    "CascadiaMono"
    "DejaVuSansMono"
    "DroidSansMono"
    "FantasqueSansMono"
    "FiraCode"
    "FiraMono"
    "GeistMono"
    "Hack"
    "Iosevka"
    "JetBrainsMono"
    "Lilex"
    "Meslo"
    "Mononoki"
    "NerFontsSymbolsOnly"
    "Noto"
    "Overpass"
    "RobotoMono"
    "SourceCodePro"
    "SpaceMono"
    "Ubuntu"
    "UbuntuMono"
    "UbuntuSans"
    "VictorMono"
)

# Font version and directories for Nerd Fonts
FONT_VERSION="v3.4.0"
FONTS_DIR="$HOME/.local/share/fonts"
TEMP_DIR="/tmp/nerdfonts_install_$$"

# Function to display regular fonts menu
display_regular_fonts_menu() {
    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}        Regular Fonts Selection${NC}"
    echo -e "${CYAN}========================================${NC}\n"
    
    # Sort and display fonts
    for key in $(echo "${!regular_fonts[@]}" | tr ' ' '\n' | sort -n); do
        printf "${GREEN}%2d${NC}) %s\n" "$key" "${regular_fonts[$key]}"
    done
    
    echo -e "\n${YELLOW}Enter your selection:${NC}"
    echo -e "  - Type numbers separated by spaces (e.g., 1 3 5 10)"
    echo -e "  - Type 'a' or 'all' to install all fonts"
    echo -e "  - Type 'b' to go back to main menu"
    echo -e "  - Type 'q' to quit\n"
}

# Function to display Nerd Fonts menu
display_nerd_fonts_menu() {
    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}         Nerd Fonts Selection${NC}"
    echo -e "${CYAN}========================================${NC}\n"
    
    for i in "${!nerd_fonts[@]}"; do
        printf "${GREEN}%2d${NC}) %s\n" "$((i+1))" "${nerd_fonts[$i]}"
    done
    
    echo -e "\n${YELLOW}Enter your selection:${NC}"
    echo -e "  - Type numbers separated by spaces (e.g., 1 3 5)"
    echo -e "  - Type 'a' or 'all' to install all Nerd Fonts"
    echo -e "  - Type 'b' to go back to main menu"
    echo -e "  - Type 'q' to quit\n"
}

# Function to install regular fonts
install_regular_fonts() {
    local selection="$1"
    local fonts_to_install=()
    
    # Parse selection
    if [[ "$selection" == "a" || "$selection" == "all" ]]; then
        echo -e "${BLUE}Installing all regular fonts...${NC}"
        for key in "${!regular_fonts[@]}"; do
            fonts_to_install+=("${regular_fonts[$key]}")
        done
    elif [[ "$selection" == "b" || "$selection" == "back" ]]; then
        return 2
    elif [[ "$selection" == "q" ]]; then
        echo -e "${YELLOW}Exiting...${NC}"
        exit 0
    else
        # Parse space-separated numbers
        for num in $selection; do
            if [[ "$num" =~ ^[0-9]+$ ]] && [ -n "${regular_fonts[$num]}" ]; then
                fonts_to_install+=("${regular_fonts[$num]}")
            else
                echo -e "${RED}Invalid selection: $num${NC}"
            fi
        done
    fi
    
    if [ ${#fonts_to_install[@]} -eq 0 ]; then
        echo -e "${RED}No valid fonts selected.${NC}"
        return 1
    fi
    
    echo -e "\n${BLUE}Installing ${#fonts_to_install[@]} font package(s)...${NC}\n"
    
    # Install fonts
    sudo pacman -S --needed --noconfirm "${fonts_to_install[@]}"
    
    echo -e "\n${BLUE}Updating font cache...${NC}"
    sudo fc-cache -f -v
    
    echo -e "${GREEN}Regular fonts installation completed!${NC}"
    
    echo -e "\n${YELLOW}Press Enter to return to main menu or type 'q' to quit:${NC} "
    read -r continue_choice
    if [[ "$continue_choice" == "q" || "$continue_choice" == "Q" ]]; then
        exit 0
    fi
    return 0
}

# Function to install Nerd Fonts
install_nerd_fonts() {
    local selection="$1"
    local fonts_to_install=()
    
    # Parse selection
    if [[ "$selection" == "a" || "$selection" == "all" ]]; then
        echo -e "${BLUE}Installing all Nerd Fonts...${NC}"
        fonts_to_install=("${nerd_fonts[@]}")
    elif [[ "$selection" == "b" || "$selection" == "back" ]]; then
        return 2
    elif [[ "$selection" == "q" ]]; then
        echo -e "${YELLOW}Exiting...${NC}"
        exit 0
    else
        # Parse space-separated numbers
        for num in $selection; do
            if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le "${#nerd_fonts[@]}" ]; then
                fonts_to_install+=("${nerd_fonts[$((num-1))]}")
            else
                echo -e "${RED}Invalid selection: $num${NC}"
            fi
        done
    fi
    
    if [ ${#fonts_to_install[@]} -eq 0 ]; then
        echo -e "${RED}No valid Nerd Fonts selected.${NC}"
        return 1
    fi
    
    # Create necessary directories
    mkdir -p "$FONTS_DIR"
    mkdir -p "$TEMP_DIR"
    
    # Check dependencies
    check_dependencies
    
    local installed=0
    local skipped=0
    local failed=0
    
    echo -e "\n${BLUE}===== Nerd Fonts Installer =====${NC}"
    echo -e "${BLUE}Installing fonts to:${NC} $FONTS_DIR"
    
    # Start timer
    local start_time=$(date +%s)
    
    # Process each selected font
    for font in "${fonts_to_install[@]}"; do
        echo -e "\n${BLUE}Processing:${NC} $font"
        
        # Check if font is already installed
        if [ -d "$FONTS_DIR/$font" ] && [ "$(ls -A "$FONTS_DIR/$font" 2>/dev/null)" ]; then
            echo -e "  ${YELLOW}➤ $font is already installed. Skipping.${NC}"
            ((skipped++))
        else
            echo -e "  ${BLUE}⚙ Downloading $font...${NC}"
            
            # Download the font zip file with a timeout
            if wget --timeout=30 -q --show-progress "https://github.com/ryanoasis/nerd-fonts/releases/download/${FONT_VERSION}/${font}.zip" -P "$TEMP_DIR"; then
                echo -e "  ${BLUE}⚙ Extracting $font...${NC}"
                
                # Create font directory
                mkdir -p "$FONTS_DIR/$font"
                
                # Extract the font with error handling
                if unzip -q "$TEMP_DIR/${font}.zip" -d "$FONTS_DIR/$font/" 2>/dev/null; then
                    echo -e "  ${GREEN}✓ Successfully installed $font${NC}"
                    ((installed++))
                else
                    echo -e "  ${RED}✗ Failed to extract $font${NC}"
                    rm -rf "$FONTS_DIR/$font"
                    ((failed++))
                fi
                
                # Clean up the zip file
                rm -f "$TEMP_DIR/${font}.zip"
            else
                echo -e "  ${RED}✗ Failed to download $font${NC}"
                ((failed++))
            fi
        fi
    done
    
    # Update font cache
    echo -e "\n${BLUE}Updating font cache...${NC}"
    fc-cache -f
    
    # End timer and calculate duration
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # Print summary
    echo -e "\n${BLUE}====== Installation Summary ======${NC}"
    echo -e "  ${GREEN}✓ Successfully installed:${NC} $installed fonts"
    echo -e "  ${YELLOW}➤ Already installed (skipped):${NC} $skipped fonts"
    echo -e "  ${RED}✗ Failed to install:${NC} $failed fonts"
    echo -e "  ${BLUE}⏱ Total time:${NC} $duration seconds"
    echo -e "${BLUE}==============================${NC}"
    echo -e "Fonts installed in: $FONTS_DIR"
    
    # Clean up the temporary directory
    rm -rf "$TEMP_DIR"
    
    echo -e "\n${YELLOW}Press Enter to return to main menu or type 'q' to quit:${NC} "
    read -r continue_choice
    if [[ "$continue_choice" == "q" || "$continue_choice" == "Q" ]]; then
        exit 0
    fi
    return 0
}

# Handle script interruption
cleanup() {
    echo -e "\n${YELLOW}Script interrupted. Cleaning up...${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
}

# Set the trap for SIGINT (Ctrl+C)
trap cleanup SIGINT

# Main menu
main_menu() {
    while true; do
        clear
        echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║     Font Installation Manager         ║${NC}"
        echo -e "${CYAN}╔════════════════════════════════════════╗${NC}\n"
        
        echo -e "${GREEN}1)${NC} Install Regular Fonts"
        echo -e "${GREEN}2)${NC} Install Nerd Fonts"
        echo -e "${GREEN}3)${NC} Install Both (Regular Fonts + Nerd Fonts)"
        echo -e "${GREEN}q)${NC} Quit\n"
        
        echo -ne "${YELLOW}Enter your choice:${NC} "
        read -r choice
        
        case "$choice" in
            1)
                display_regular_fonts_menu
                echo -ne "${YELLOW}Your selection:${NC} "
                read -r font_selection
                install_regular_fonts "$font_selection"
                local result=$?
                if [ $result -eq 2 ]; then
                    continue
                fi
                ;;
            2)
                display_nerd_fonts_menu
                echo -ne "${YELLOW}Your selection:${NC} "
                read -r nerd_selection
                install_nerd_fonts "$nerd_selection"
                local result=$?
                if [ $result -eq 2 ]; then
                    continue
                fi
                ;;
            3)
                # Install regular fonts first
                display_regular_fonts_menu
                echo -ne "${YELLOW}Your selection:${NC} "
                read -r font_selection
                
                install_regular_fonts "$font_selection"
                local regular_result=$?
                
                if [ $regular_result -eq 2 ]; then
                    continue
                elif [ $regular_result -eq 0 ]; then
                    echo -e "\n${GREEN}Regular fonts installation completed!${NC}"
                    echo -e "${BLUE}Press Enter to continue to Nerd Fonts installation...${NC}"
                    read -r
                    
                    # Then install Nerd Fonts
                    display_nerd_fonts_menu
                    echo -ne "${YELLOW}Your selection:${NC} "
                    read -r nerd_selection
                    install_nerd_fonts "$nerd_selection"
                    local nerd_result=$?
                    if [ $nerd_result -eq 2 ]; then
                        continue
                    fi
                else
                    echo -e "${RED}Regular fonts installation failed.${NC}"
                    sleep 2
                fi
                ;;
            q|Q)
                echo -e "${YELLOW}Exiting...${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                sleep 2
                ;;
        esac
    done
}

# Run the main menu
main_menu
