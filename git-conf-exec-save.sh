#!/usr/bin/env bash



# git config for git hook for leaving executable scripts executable
### git config --add hooks.pre-push 'chmod +x your_script.sh'

git config --add hooks.pre-push 'chmod +x arch_boki_bash.sh'
git config --add hooks.pre-push 'chmod +x make-execute.sh'
git config --add hooks.pre-push 'chmod +x add-repos/append_archboki_repo.sh'
git config --add hooks.pre-push 'chmod +x add-repos/fix-pacman-databases-and-keys.sh'
git config --add hooks.pre-push 'chmod +x add-repos/get-the-arcolinux-keys-and-repos.sh'
git config --add hooks.pre-push 'chmod +x add-repos/install_and_append_chaotic_repo_and_keyrings.sh'
git config --add hooks.pre-push 'chmod +x add-repos/upd_servers.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/cinnamon/install_cinnamon.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/00-choices.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/01-hyprland.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/02-hyprland-pkgs.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/03-yay.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/04-paru.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/130-apps.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/kde-plasma/install-kde-plasma.sh'
git config --add hooks.pre-push 'chmod +x choose-desktop/xfce/install-xfce-and-sddm.sh'
git config --add hooks.pre-push 'chmod +x core-utils/audio-drivers.sh'
git config --add hooks.pre-push 'chmod +x core-utils/gpu-drivers.sh'
git config --add hooks.pre-push 'chmod +x core-utils/microcode.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/118-core.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/119-xorg.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/120-sddm.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/121-pipewire-sound.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/122-pulseaudio-sound.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/123-bluetooth.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/124-printers.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/125-fonts.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/126-network.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/127-package-managers.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/128-nvidia.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/129-theming.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/130.apps.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/131-install-flatpaks.sh'
git config --add hooks.pre-push 'chmod +x install-scripts/133-logout.sh'


# fit pull and check if a script is executable
### git pull && file your_script.sh | grep -q "executable" || echo "Script not executable"

git pull && file arch_boki_bash.sh | grep -q "executable" || echo "Script not executable"
git pull && file make-execute.sh | grep -q "executable" || echo "Script not executable"
git pull && file add-repos/append_archboki_repo.sh | grep -q "executable" || echo "Script not executable"
git pull && file add-repos/fix-pacman-databases-and-keys.sh | grep -q "executable" || echo "Script not executable"
git pull && file add-repos/install_and_append_chaotic_repo_and_keyrings.sh | grep -q "executable" || echo "Script not executable"
git pull && file add-repos/get-the-arcolinux-keys-and-repos.sh | grep -q "executable" || echo "Script not executable"
git pull && file add-repos/upd_servers.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/cinnamon/install_cinnamon.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/hyprland-scripts/00-choices.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/hyprland-scripts/01-hyprland.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/hyprland-scripts/02-hyprland-pkgs.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/hyprland-scripts/03-yay.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/hyprland-scripts/04-paru.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/hyprland-scripts/130-apps.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/kde-plasma/install-kde-plasma.sh | grep -q "executable" || echo "Script not executable"
git pull && file choose-desktop/xfce/install-xfce-and-sddm.sh | grep -q "executable" || echo "Script not executable"
git pull && file core-utils/audio-drivers.sh | grep -q "executable" || echo "Script not executable"
git pull && file core-utils/gpu-drivers.sh | grep -q "executable" || echo "Script not executable"
git pull && file core-utils/microcode.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/118-core.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/119-xorg.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/120-sddm.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/121-pipewire-sound.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/122-pulseaudio-sound.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/123-bluetooth.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/124-printers.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/125-fonts.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/126-network.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/127-package-managers.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/128-nvidia.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/129-theming.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/130.apps.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/131-install-flatpaks.sh | grep -q "executable" || echo "Script not executable"
git pull && file install-scripts/133-logout.sh | grep -q "executable" || echo "Script not executable"

















