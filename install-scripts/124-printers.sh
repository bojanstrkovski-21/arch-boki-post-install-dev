#!/bin/bash

sudo pacman -S --noconfirm --needed pacutils

sudo pacinstall --resolve-conflicts=all --no-confirm \
cups \
cups-pdf \
cups-browsed \
cups-filters \
bluez-cups \
ghostscript \
gsfonts \
gutenprint \
foomatic-db-gutenprint-ppds \
libcups \
system-config-printer




sudo systemctl enable --now cups.service