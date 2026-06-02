#!/bin/bash

LOCK_FILE="/var/lib/pacman/db.lck"

if [ -f "$LOCK_FILE" ]; then
    sudo rm -f "$LOCK_FILE"
    echo "db.lck removed — pacman is now unlocked"
else
    echo "db.lck not found — pacman is not locked"
fi
