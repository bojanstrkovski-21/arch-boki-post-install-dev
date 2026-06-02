#!/bin/bash

echo "Clearing pacman cache..."
sudo pacman -Scc

read -rp "Run yay -Scc? [y/N]: " ans
if [[ "$ans" =~ ^[Yy]$ ]]; then
    if command -v yay &>/dev/null; then
        yay -Scc
    else
        echo "yay not found — skipping"
    fi
fi

read -rp "Run paru -Scc? [y/N]: " ans
if [[ "$ans" =~ ^[Yy]$ ]]; then
    if command -v paru &>/dev/null; then
        paru -Scc
    else
        echo "paru not found — skipping"
    fi
fi

echo "Done."
