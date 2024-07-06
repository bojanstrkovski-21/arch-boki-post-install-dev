#!/usr/bin/env bash



#git config --add hooks.pre-push 'chmod +x your_script.sh'

git config --add hooks.pre-push 'chmod +x arch_boki_bash.sh'
git config --add hooks.pre-push 'chmod +x make-execute.sh'
git config --add hooks.pre-push 'chmod +x add-repos/*'
git config --add hooks.pre-push 'chmod +x choose-desktop/cinnamon/*'
git config --add hooks.pre-push 'chmod +x choose-desktop/hyprland-scripts/*'
git config --add hooks.pre-push 'chmod +x choose-desktop/kde-plasma/*'
git config --add hooks.pre-push 'chmod +x choose-desktop/xfce/*'
git config --add hooks.pre-push 'chmod +x core-utils/*'
git config --add hooks.pre-push 'chmod +x install-scripts/*'
