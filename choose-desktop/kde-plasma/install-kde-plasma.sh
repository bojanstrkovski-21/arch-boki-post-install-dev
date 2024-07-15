#!/usr/bin/env bash

## Core-utils-apps
sudo pacman  -S --needed --noconfirm \
neovim \
sublime-text-4 \
xed

## Plasma group

sudo pacman  -S --needed --noconfirm \
plasma \
sddm \
sddm-conf \

### Kf6 group
    
sudo pacman  -S --needed --noconfirm \
attica   \
baloo   \
bluez-qt   \
breeze-icons   \
extra-cmake-modules   \
frameworkintegration   \
kapidox   \
karchive   \
kauth   \
kbookmarks   \
kcalendarcore   \
kcmutils   \
kcodecs \
kcolorscheme   \
kcompletion   \
kconfig   \
kconfigwidgets   \
kcontacts   \
kcoreaddons   \
kcrash   \
kdav    \
kdeclarative   \
kded   \
kdesu   \
kdnssd   \
kdoctools \
kfilemetadata   \
kglobalaccel   \
kguiaddons   \
kholidays   \
ki18n   \
kiconthemes   \
kidletime   \
kimageformats   \
kio   \
kirigami   \
knewstuff    \
kpackage    \
kpty   \
kquickcharts   \
krunner     \
kstatusnotifieritem   \
ksvg \
ktexteditor   \
ktexttemplate   \
ktextwidgets   \
kunitconversion    \
kwidgetsaddons 

### Qt6 gropoup (all)
sudo pacman  -S --needed --noconfirm \
qt6 \
kvantum

### Kde-network group

sudo pacman  -S --needed --noconfirm \
kdeconnect \
kdenetwork-filesharing  \
kget   \
kio-extras  \
kio-gdrive  \
kio-zeroconf  \
krdc  \
krfb


### Kde-system

sudo pacman  -S --needed --noconfirm \
dolphin  \
kcron  \
kio-admin


### Kde-graphics

sudo pacman  -S --needed --noconfirm \
gwenview \
kcolorchooser   \
kruler   \
okular    \
spectacle


### kde-multimedia

#sudo pacman  -S --needed --noconfirm \
#kdenlive  


### kde-utilities

sudo pacman  -S --needed --noconfirm \
ark  \
kalk  \
kate  \
kbackup  \
kcalc  \
kcharselect   \
kdebugsettings  \
kfind  \
kgpg   \
konsole  \
kweather  \
markdownpart  


### kde-sdk


sudo pacman  -S --needed --noconfirm \
dolphin-plugins \
kdesdk-kio \
kdesdk-thumbnailers \
kapptemplate \
kcachegrind \
kde-dev-scripts \
kde-dev-utils \
kde-cli-tools


sleep 5

sudo systemctl enable --now sddm
sudo systemctl start --now sddm
