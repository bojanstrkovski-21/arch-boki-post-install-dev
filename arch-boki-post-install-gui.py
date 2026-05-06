#!/usr/bin/env python3
# =============================================================================
# arch-boki-post-install-gui.py — Arch-Boki Post Install GUI
# Dear PyGui — Everforest theme
# Tabs: Welcome | Install Apps | Core Utils & Drivers | System Maintenance
# =============================================================================

import re
import subprocess
import sys
from pathlib import Path

try:
    import dearpygui.dearpygui as dpg
except ImportError:
    print("dearpygui not installed. Run: sudo pacman -S python-dearpygui", file=sys.stderr)
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent

# ── Everforest palette (RGBA 0-255) ───────────────────────────────────────────
BG      = (35,  42,  46,  255)
BG2     = (45,  53,  59,  255)
FG      = (168, 158, 136, 255)
GREEN   = (167, 192, 128, 255)
BLUE    = (127, 187, 179, 255)
AQUA    = (131, 192, 146, 255)
RED     = (230, 126, 128, 255)
YELLOW  = (219, 188, 127, 255)
HEADER  = (56,  65,  71,  255)
SEL     = (60,  72,  67,  255)
BORDER  = (88,  104, 117, 255)
DIM     = (120, 115, 100, 255)
SIDEBAR_W = 200

# =============================================================================
# Package data
# =============================================================================

INSTALL_APPS = {
    "File Managers": {
        "_flat": True,
        "items": [
            ("Nemo",          ["nemo", "nemo-compare", "nemo-fileroller", "nemo-image-converter", "nemo-preview", "nemo-share"]),
            ("PcmanFM GTK3",  ["pcmanfm-gtk3"]),
            ("PcmanFM Qt",    ["pcmanfm-qt"]),
            ("Thunar",        ["thunar", "thunar-archive-plugin", "thunar-shares-plugin", "thunar-volman", "tumbler", "file-roller"]),
            ("Nautilus",      ["nautilus", "nautilus-share", "sushi"]),
            ("Dolphin",       ["dolphin", "dolphin-plugins"]),
            ("Yazi",          ["yazi"]),
            ("Ranger",        ["ranger"]),
        ],
    },
    "Terminal Emulators": {
        "_flat": True,
        "items": [
            ("Alacritty",      ["alacritty", "alacritty-themes", "imagemagick", "libsixel", "lsix"]),
            ("Ghostty",        ["ghostty", "libsixel", "imagemagick", "lsix"]),
            ("Kitty",          ["kitty", "kitty-shell-integration", "libsixel", "lsix", "imagemagick"]),
            ("Tilix",          ["tilix"]),
            ("Wezterm",        ["wezterm-nightly-bin", "imagemagick"]),
            ("Xfce4-Terminal", ["xfce4-terminal"]),
        ],
    },
    "Text, PDF & Dev": {
        "_flat": False,
        "subcategories": {
            "Text Editors": [
                ("Emacs",        ["emacs"]),
                ("Geany",        ["geany", "geany-plugins"]),
                ("Leafpad",      ["leafpad"]),
                ("Mousepad",     ["mousepad"]),
                ("Sublime Text", ["sublime-text-4"]),
                ("Xed",          ["xed"]),
            ],
            "Office Suites": [
                ("LibreOffice",  ["libreoffice-fresh"]),
                ("OnlyOffice",   ["onlyoffice"]),
            ],
            "Markdown Editors": [
                ("Affine",       ["affine-bin"]),
                ("Obsidian",     ["obsidian"]),
                ("QOwnNotes",    ["qownnotes"]),
            ],
            "PDF Viewers": [
                ("Evince",   ["evince"]),
                ("Okular",   ["okular"]),
                ("Xpdf",     ["xpdf"]),
                ("Xreader",  ["xreader"]),
                ("Zathura",  ["zathura"]),
            ],
            "Dev Tools": [
                ("Code",             ["code"]),
                ("Meld",             ["meld"]),
                ("Notepadqq",        ["notepadqq"]),
                ("PyCharm CE",       ["pycharm-community-edition"]),
                ("VSCodium",         ["vscodium", "vscodium-marketplace"]),
                ("Visual Studio Code", ["visual-studio-code-bin"]),
                ("Zed",              ["zed"]),
            ],
        },
    },
    "Internet": {
        "_flat": False,
        "subcategories": {
            "Communication": [
                ("Discord",  ["discord"]),
                ("Signal",   ["signal-desktop"]),
                ("Telegram", ["telegram-desktop"]),
            ],
            "Web Browsers": [
                ("Brave",        ["brave-bin"]),
                ("Chromium",     ["chromium"]),
                ("Firefox",      ["firefox"]),
                ("Firefox ESR",  ["firefox-esr"]),
                ("Google Chrome",["google-chrome"]),
                ("Librewolf",    ["librewolf"]),
                ("Qutebrowser",  ["qutebrowser"]),
                ("Vivaldi",      ["vivaldi", "vivaldi-ffmpeg-codecs"]),
            ],
            "Downloaders": [
                ("Deluge GTK",       ["deluge-gtk"]),
                ("KTorrent",         ["ktorrent"]),
                ("qBittorrent",      ["qbittorrent"]),
                ("Transmission GTK", ["transmission-gtk"]),
                ("Transmission Qt",  ["transmission-qt"]),
            ],
            "Recorders": [
                ("GPU Screen Recorder", ["gpu-screen-recorder", "gpu-screen-recorder-gtk"]),
                ("Hyprshot",            ["hyprshot"]),
                ("Kazam",               ["kazam"]),
                ("OBS Studio",          ["obs-studio"]),
                ("Peek",                ["peek"]),
                ("SimpleScreenRecorder",["simplescreenrecorder-qt6-git"]),
            ],
        },
    },
    "Multimedia": {
        "_flat": False,
        "subcategories": {
            "Audio Players": [
                ("Amberol",         ["amberol"]),
                ("Audacious",       ["audacious", "audacious-plugins"]),
                ("Deadbeef",        ["deadbeef"]),
                ("Elisa",           ["elisa"]),
                ("G4Music",         ["g4music-git"]),
                ("Juk",             ["juk"]),
                ("Lollypop",        ["lollypop"]),
                ("Pragha",          ["pragha"]),
                ("Rhythmbox",       ["rhythmbox"]),
                ("Sayonara Player", ["sayonara-player"]),
                ("Strawberry",      ["strawberry"]),
            ],
            "Video Players": [
                ("Celluloid", ["celluloid"]),
                ("Clapper",   ["clapper", "clapper-enhancers"]),
                ("Kodi",      ["kodi"]),
                ("MPV",       ["mpv"]),
                ("SMPlayer",  ["smplayer", "smplayer-skins", "smplayer-themes"]),
                ("VLC",       ["vlc"]),
            ],
            "Audio Editors": [
                ("Ardour",          ["ardour"]),
                ("Audacity",        ["audacity"]),
                ("Kwave",           ["kwave"]),
                ("LMMS",            ["lmms"]),
                ("Reaper",          ["reaper", "reapack", "sws"]),
                ("SoundConverter",  ["soundconverter"]),
                ("Tenacity",        ["tenacity"]),
            ],
            "Video Editors": [
                ("Flowblade",  ["flowblade"]),
                ("Handbrake",  ["handbrake"]),
                ("Kdenlive",   ["kdenlive"]),
                ("LosslessCut",["losslesscut-bin"]),
                ("MakeMKV",    ["makemkv", "mkvtoolnix-cli", "mkvtoolnix-gui"]),
                ("Openshot",   ["openshot"]),
                ("Shotcut",    ["shotcut"]),
            ],
            "Subtitle Editors": [
                ("Aegisub",           ["aegisub"]),
                ("SubtitleEdit",      ["subtitleedit"]),
                ("SubtitleComposer",  ["subtitlecomposer"]),
            ],
        },
    },
    "Graphics": {
        "_flat": False,
        "subcategories": {
            "Image Viewers": [
                ("Darktable",  ["darktable"]),
                ("Ephoto",     ["ephoto"]),
                ("GPicView",   ["gpicview"]),
                ("Gwenview",   ["gwenview"]),
                ("Nomacs",     ["nomacs"]),
                ("Nsxiv",      ["nsxiv"]),
                ("Qimgv",      ["qimgv-git"]),
                ("Ristretto",  ["ristretto"]),
            ],
            "Image Editors": [
                ("GIMP",         ["gimp"]),
                ("Gpick",        ["gpick"]),
                ("Inkscape",     ["inkscape"]),
                ("Krita",        ["krita"]),
                ("Pinta",        ["pinta"]),
                ("RawTherapee",  ["rawtherapee"]),
                ("Upscayl",      ["upscayl-desktop-git", "upscayl-models-desktop"]),
            ],
            "Wallpaper Changers": [
                ("Azote",       ["azote"]),
                ("Feh",         ["feh"]),
                ("Hyprpaper",   ["hyprpaper"]),
                ("Nitrogen",    ["nitrogen"]),
                ("Swaybg",      ["swaybg"]),
                ("Swww",        ["swww"]),
                ("Variety",     ["variety"]),
                ("Waypaper",    ["waypaper-git"]),
                ("Xwallpaper",  ["xwallpaper"]),
            ],
        },
    },
    "System Info": {
        "_flat": True,
        "items": [
            ("Bashtop",          ["bashtop"]),
            ("Btop",             ["btop"]),
            ("Countryfetch",     ["countryfetch"]),
            ("Cpufetch",         ["cpufetch"]),
            ("Fastfetch",        ["fastfetch"]),
            ("Glances",          ["glances"]),
            ("Gtop",             ["gtop"]),
            ("Htop",             ["htop"]),
            ("Hyfetch",          ["hyfetch"]),
            ("Mission Center",   ["mission-center"]),
            ("Nvtop",            ["nvtop"]),
            ("Resources",        ["resources"]),
            ("Stacer",           ["stacer-bin"]),
            ("Xfce4-Taskmanager",["xfce4-taskmanager"]),
        ],
    },
    "System Tools": {
        "_flat": False,
        "subcategories": {
            "App Launchers": [
                ("Bemenu",         ["bemenu"]),
                ("Bemenu Wayland", ["bemenu-wayland"]),
                ("Dmenu",          ["dmenu"]),
                ("Fuzzel",         ["fuzzel"]),
                ("Rofi",           ["rofi"]),
                ("Rofi Wayland",   ["rofi-wayland"]),
                ("Tofi",           ["tofi"]),
                ("Walker",         ["walker-bin"]),
                ("Wofi",           ["wofi"]),
            ],
            "Calculators": [
                ("Galculator",       ["galculator"]),
                ("Gnome Calculator", ["gnome-calculator"]),
                ("Qalculate GTK",    ["qalculate-gtk"]),
                ("Qalculate Qt",     ["qalculate-qt"]),
            ],
            "Partition Tools": [
                ("KDE Partition Manager", ["partitionmanager"]),
                ("Gnome Disks",           ["gnome-disk-utility"]),
                ("GParted",               ["gparted"]),
            ],
            "Screen Shooters": [
                ("Flameshot",          ["flameshot"]),
                ("Kazam",              ["kazam"]),
                ("Ksnip",              ["ksnip"]),
                ("Shutter",            ["shutter"]),
                ("Spectacle",          ["spectacle"]),
                ("Xfce4-Screenshooter",["xfce4-screenshooter"]),
            ],
            "Screen Resolution": [
                ("Arandr",        ["arandr"]),
                ("nwg-displays",  ["nwg-displays"]),
                ("Wdisplays",     ["wdisplays"]),
                ("Wlr-randr",     ["wlr-randr"]),
                ("Xorg-xrandr",   ["xorg-xrandr"]),
            ],
        },
    },
}

# =============================================================================
# GUI state
# =============================================================================
_state: dict = {
    "apps_cat": list(INSTALL_APPS.keys())[0],
}


# =============================================================================
# Screen center helper
# =============================================================================
def _screen_center(vp_w: int, vp_h: int) -> tuple[int, int]:
    try:
        out = subprocess.check_output(["xrandr", "--current"], text=True)
        m = re.search(r"current (\d+) x (\d+)", out)
        if m:
            sw, sh = int(m.group(1)), int(m.group(2))
            return (sw - vp_w) // 2, (sh - vp_h) // 2
    except Exception:
        pass
    return 100, 100


# =============================================================================
# Terminal launcher
# =============================================================================
AUR_PKGS = {
    "affine-bin", "g4music-git", "wezterm-nightly-bin", "stacer-bin",
    "simplescreenrecorder-qt6-git", "qimgv-git", "upscayl-desktop-git",
    "upscayl-models-desktop", "waypaper-git", "walker-bin",
    "visual-studio-code-bin", "brave-bin", "google-chrome",
    "librewolf", "firefox-esr",
}


def _find_terminal() -> str:
    for t in ["alacritty", "kitty", "ghostty", "xfce4-terminal", "xterm"]:
        if subprocess.call(["which", t],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0:
            return t
    return "xterm"


def _launch_in_terminal(bash_cmd: str) -> None:
    term = _find_terminal()
    full = bash_cmd + '; echo; printf "\\n  Press Enter to close..."; read'
    if term == "gnome-terminal":
        subprocess.Popen([term, "--", "bash", "-c", full])
    elif term == "xfce4-terminal":
        subprocess.Popen([term, "--command", f"bash -c '{full}'"])
    else:
        subprocess.Popen([term, "-e", "bash", "-c", full])


def _install_packages(pkgs: list[str]) -> None:
    normal = [p for p in pkgs if p not in AUR_PKGS]
    aur    = [p for p in pkgs if p in AUR_PKGS]
    parts: list[str] = []
    if normal:
        parts.append("sudo pacman -S --needed --noconfirm " + " ".join(normal))
    if aur:
        parts.append("yay -S --needed --noconfirm " + " ".join(aur))
    if parts:
        _launch_in_terminal(" && ".join(parts))


# =============================================================================
# TAB 1 — Welcome
# =============================================================================
def _build_welcome_tab() -> None:
    with dpg.tab(label="   Welcome   "):
        dpg.add_spacer(height=16)
        dpg.add_text(
            "      █████╗ ██████╗  ██████╗██╗  ██╗      ██████╗  ██████╗ ██╗  ██╗██╗",
            color=AQUA,
        )
        dpg.add_text(
            "     ██╔══██╗██╔══██╗██╔════╝██║  ██║      ██╔══██╗██╔═══██╗██║ ██╔╝██║",
            color=AQUA,
        )
        dpg.add_text(
            "     ███████║██████╔╝██║     ███████║█████╗██████╔╝██║   ██║█████╔╝ ██║",
            color=GREEN,
        )
        dpg.add_text(
            "     ██╔══██║██╔══██╗██║     ██╔══██║╚════╝██╔══██╗██║   ██║██╔═██╗ ██║",
            color=GREEN,
        )
        dpg.add_text(
            "     ██║  ██║██║  ██║╚██████╗██║  ██║      ██████╔╝╚██████╔╝██║  ██╗██║",
            color=AQUA,
        )
        dpg.add_text(
            "     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝",
            color=AQUA,
        )
        dpg.add_spacer(height=20)
        dpg.add_separator()
        dpg.add_spacer(height=12)

        dpg.add_text("  Post-Install Setup", color=AQUA)
        dpg.add_spacer(height=8)
        dpg.add_text(
            "  Welcome to Arch-Boki Post Install GUI.\n"
            "  Use the tabs above to install applications, set up drivers,\n"
            "  and maintain your system.\n\n"
            "  Tips:\n"
            "    — Click a sidebar category to browse packages\n"
            "    — Check the boxes next to apps you want, then click Install Selected\n"
            "    — A terminal window will open and run the install\n"
            "    — Press Escape to close this window",
            color=FG,
        )
        dpg.add_spacer(height=12)
        dpg.add_separator()
        dpg.add_spacer(height=8)
        dpg.add_text("  Requirements:", color=YELLOW)
        dpg.add_text("    — sudo access is required for package installation", color=FG)
        dpg.add_text("    — yay (AUR helper) is required for AUR packages", color=FG)


# =============================================================================
# TAB 2 — Install Apps
# =============================================================================
def _install_selected(cat: str, subcat: str | None) -> None:
    data = INSTALL_APPS[cat]
    if data["_flat"]:
        items = data["items"]
    else:
        if subcat is None:
            return
        items = data["subcategories"][subcat]

    selected: list[str] = []
    for label, pkgs in items:
        tag = f"chk__{cat}__{subcat}__{label}".replace(" ", "_")
        if dpg.does_item_exist(tag) and dpg.get_value(tag):
            selected.extend(pkgs)

    if selected:
        _install_packages(selected)


def _rebuild_apps_content(cat: str, subcat: str | None, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    data = INSTALL_APPS[cat]

    # Auto-select first sub-category
    if not data["_flat"] and subcat is None:
        subcat = list(data["subcategories"].keys())[0]

    with dpg.group(parent=content_tag):
        if not data["_flat"]:
            subcats = list(data["subcategories"].keys())
            dpg.add_spacer(height=4)
            with dpg.group(horizontal=True):
                for sc in subcats:
                    active = (sc == subcat)
                    with dpg.theme() as btn_theme:
                        with dpg.theme_component(dpg.mvButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button, SEL if active else BG2)
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, HEADER)
                            dpg.add_theme_color(dpg.mvThemeCol_Text, GREEN if active else FG)
                    b = dpg.add_button(
                        label=sc,
                        callback=lambda s, a, u: _rebuild_apps_content(u[0], u[1], content_tag),
                        user_data=(cat, sc),
                    )
                    dpg.bind_item_theme(b, btn_theme)
                    dpg.add_spacer(width=4)
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=8)
            items = data["subcategories"][subcat]
        else:
            items = data["items"]

        dpg.add_text(f"  {subcat or cat}", color=AQUA)
        dpg.add_spacer(height=6)

        with dpg.child_window(height=-72, border=False):
            cols = 2
            with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                for _ in range(cols):
                    dpg.add_table_column()
                row_items = [items[i:i+cols] for i in range(0, len(items), cols)]
                for row in row_items:
                    with dpg.table_row():
                        for label, pkgs in row:
                            tag = f"chk__{cat}__{subcat}__{label}".replace(" ", "_")
                            dpg.add_checkbox(label=f"  {label}", tag=tag, default_value=False)
                        for _ in range(cols - len(row)):
                            dpg.add_text("")

        dpg.add_spacer(height=8)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Select All",
                callback=lambda s, a, u: [
                    dpg.set_value(f"chk__{u[0]}__{u[1]}__{lbl}".replace(" ", "_"), True)
                    for lbl, _ in u[2]
                ],
                user_data=(cat, subcat, items),
            )
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="Clear All",
                callback=lambda s, a, u: [
                    dpg.set_value(f"chk__{u[0]}__{u[1]}__{lbl}".replace(" ", "_"), False)
                    for lbl, _ in u[2]
                ],
                user_data=(cat, subcat, items),
            )
            dpg.add_spacer(width=16)
            dpg.add_button(
                label="  Install Selected  ",
                callback=lambda s, a, u: _install_selected(u[0], u[1]),
                user_data=(cat, subcat),
            )


def _build_apps_tab() -> None:
    with dpg.tab(label="   Install Apps   "):
        dpg.add_spacer(height=8)
        content_tag = "apps_content"
        with dpg.group(horizontal=True):

            # ── Left sidebar (plain buttons, no sticky highlight) ─────────────
            with dpg.child_window(width=SIDEBAR_W, border=True):
                dpg.add_text("  Categories", color=AQUA)
                dpg.add_separator()
                dpg.add_spacer(height=6)

                for cat in INSTALL_APPS:
                    with dpg.theme() as btn_theme:
                        with dpg.theme_component(dpg.mvButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button,        (0, 0, 0, 0))
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  HEADER)
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   SEL)
                            dpg.add_theme_color(dpg.mvThemeCol_Text,           FG)
                            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
                    b = dpg.add_button(
                        label=f"  {cat}",
                        width=-1,
                        callback=lambda s, a, u: _rebuild_apps_content(u, None, content_tag),
                        user_data=cat,
                    )
                    dpg.bind_item_theme(b, btn_theme)
                    dpg.add_spacer(height=2)

            # ── Right content panel ───────────────────────────────────────────
            with dpg.child_window(tag=content_tag, border=True):
                pass

        first_cat = list(INSTALL_APPS.keys())[0]
        _rebuild_apps_content(first_cat, None, content_tag)


# =============================================================================
# TAB 3 — Core Utils & Drivers
# =============================================================================
CORE_CATEGORIES = {
    "CPU Microcode": {
        "_flat": True,
        "items": [
            ("Intel Microcode",   ["intel-ucode"]),
            ("AMD Microcode",     ["amd-ucode"]),
        ],
    },
    "GPU Drivers": {
        "_flat": True,
        "items": [
            ("NVIDIA (proprietary)", ["nvidia", "nvidia-utils", "nvidia-settings"]),
            ("NVIDIA (open-dkms)",   ["nvidia-open-dkms", "nvidia-utils", "nvidia-settings"]),
            ("AMD (mesa)",           ["mesa", "vulkan-radeon", "libva-mesa-driver", "mesa-vdpau"]),
            ("Intel (mesa)",         ["mesa", "vulkan-intel", "intel-media-driver"]),
            ("Nouveau (OSS nvidia)", ["xf86-video-nouveau"]),
        ],
    },
    "Audio Drivers": {
        "_flat": True,
        "items": [
            ("PipeWire stack", ["pipewire", "pipewire-alsa", "pipewire-pulse", "pipewire-jack", "wireplumber"]),
            ("PulseAudio",     ["pulseaudio", "pulseaudio-alsa", "pavucontrol"]),
            ("ALSA utils",     ["alsa-utils"]),
        ],
    },
    "Bluetooth": {
        "_flat": True,
        "items": [
            ("BlueZ + tools", ["bluez", "bluez-utils", "blueman"]),
        ],
    },
    "Network": {
        "_flat": True,
        "items": [
            ("NetworkManager",    ["networkmanager", "network-manager-applet"]),
            ("iwd",               ["iwd"]),
            ("wireless_tools",    ["wireless_tools", "wpa_supplicant"]),
        ],
    },
    "Printer Drivers": {
        "_flat": True,
        "items": [
            ("CUPS stack",   ["cups", "cups-filters", "ghostscript", "system-config-printer"]),
            ("HP printers",  ["hplip"]),
            ("Epson/Canon",  ["gutenprint"]),
        ],
    },
    "Fonts": {
        "_flat": True,
        "items": [
            ("Nerd Fonts (MesloLGS)",   ["ttf-meslo-nerd"]),
            ("JetBrains Mono NF",       ["ttf-jetbrains-mono-nerd"]),
            ("Fira Code NF",            ["ttf-firacode-nerd"]),
            ("Noto fonts",              ["noto-fonts", "noto-fonts-emoji"]),
            ("Liberation fonts",        ["ttf-liberation"]),
        ],
    },
    "Core Utils": {
        "_flat": True,
        "items": [
            ("Base tools",    ["base-devel", "git", "curl", "wget", "unzip", "p7zip", "rsync"]),
            ("Shell extras",  ["zsh", "bash-completion", "starship"]),
            ("Polkit",        ["polkit", "polkit-gnome"]),
            ("Xorg base",     ["xorg-server", "xorg-xinit", "xorg-xrandr"]),
        ],
    },
}

def _install_core_selected(cat: str) -> None:
    items = CORE_CATEGORIES[cat]["items"]
    selected: list[str] = []
    for label, pkgs in items:
        tag = f"core_chk__{cat}__{label}".replace(" ", "_")
        if dpg.does_item_exist(tag) and dpg.get_value(tag):
            selected.extend(pkgs)
    if selected:
        _install_packages(selected)


def _rebuild_core_content(cat: str, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    items = CORE_CATEGORIES[cat]["items"]

    with dpg.group(parent=content_tag):
        dpg.add_text(f"  {cat}", color=AQUA)
        dpg.add_spacer(height=6)

        with dpg.child_window(height=-72, border=False):
            for label, pkgs in items:
                tag = f"core_chk__{cat}__{label}".replace(" ", "_")
                dpg.add_checkbox(label=f"  {label}", tag=tag, default_value=False)
                dpg.add_text(f"      pkgs: {', '.join(pkgs)}", color=DIM)
                dpg.add_spacer(height=4)

        dpg.add_spacer(height=8)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Select All",
                callback=lambda s, a, u: [
                    dpg.set_value(f"core_chk__{u[0]}__{lbl}".replace(" ", "_"), True)
                    for lbl, _ in u[1]
                ],
                user_data=(cat, items),
            )
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="Clear All",
                callback=lambda s, a, u: [
                    dpg.set_value(f"core_chk__{u[0]}__{lbl}".replace(" ", "_"), False)
                    for lbl, _ in u[1]
                ],
                user_data=(cat, items),
            )
            dpg.add_spacer(width=16)
            dpg.add_button(
                label="  Install Selected  ",
                callback=lambda s, a, u: _install_core_selected(u),
                user_data=cat,
            )


def _build_core_tab() -> None:
    first_cat = list(CORE_CATEGORIES.keys())[0]
    with dpg.tab(label="   Core & Drivers   "):
        dpg.add_spacer(height=8)
        content_tag = "core_content"
        with dpg.group(horizontal=True):

            with dpg.child_window(width=SIDEBAR_W, border=True):
                dpg.add_text("  Categories", color=AQUA)
                dpg.add_separator()
                dpg.add_spacer(height=6)

                for cat in CORE_CATEGORIES:
                    with dpg.theme() as btn_theme:
                        with dpg.theme_component(dpg.mvButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button,        (0, 0, 0, 0))
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  HEADER)
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   SEL)
                            dpg.add_theme_color(dpg.mvThemeCol_Text,           FG)
                            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, 0.5)
                    b = dpg.add_button(
                        label=f"  {cat}",
                        width=-1,
                        callback=lambda s, a, u: _rebuild_core_content(u, content_tag),
                        user_data=cat,
                    )
                    dpg.bind_item_theme(b, btn_theme)
                    dpg.add_spacer(height=2)

            with dpg.child_window(tag=content_tag, border=True):
                pass

        _rebuild_core_content(first_cat, content_tag)


# =============================================================================
# TAB 4 — System Maintenance
# =============================================================================
MAINTENANCE_ACTIONS = [
    {
        "label":   "Refresh Mirrors (reflector)",
        "desc":    "Update mirrorlist with fastest mirrors via reflector",
        "cmd":     ["sudo", "reflector", "--country", "AT,BE,BG,HR,CZ,DK,EE,FI,FR,DE,GR,HU,IT,MD,NL,MK,NO,PL,PT,RO,RS,SK,SI,ES,SE,CH,UA,GB", "--age", "6", "--fastest", "20", "--protocol", "https", "--sort", "rate",
                    "--save", "/etc/pacman.d/mirrorlist", "--verbose"],
    },
    {
        "label":   "Refresh Pacman DB",
        "desc":    "Force-sync all pacman databases (pacman -Syyv)",
        "cmd":     ["bash", str(BASE_DIR / "add-repos/upd_servers.sh")],
    },
    {
        "label":   "Update System",
        "desc":    "Full system update via pacman -Syyu",
        "cmd":     ["sudo", "pacman", "-Syyu", "--noconfirm"],
    },
    {
        "label":   "Add Arch-Boki Repos",
        "desc":    "Append arch-boki repository to pacman.conf",
        "cmd":     ["bash", str(BASE_DIR / "add-repos/append_archboki_repo.sh")],
    },
    {
        "label":   "Add Nemesis Repos",
        "desc":    "Add Nemesis / Erik Dubois repository",
        "cmd":     ["bash", str(BASE_DIR / "add-repos/get-the-arcolinux-keys-and-repos.sh")],
    },
    {
        "label":   "Add Chaotic-AUR Repos",
        "desc":    "Install and append Chaotic-AUR keyring and repository",
        "cmd":     ["bash", str(BASE_DIR / "add-repos/install_and_append_chaotic_repo_and_keyrings.sh")],
    },
    {
        "label":   "Fix Pacman DB & Keys",
        "desc":    "Reset pacman databases, keyrings and trust",
        "cmd":     ["bash", str(BASE_DIR / "add-repos/fix-pacman-databases-and-keys.sh")],
    },
    {
        "label":   "Install Archlinux-Tweak-Tool",
        "desc":    "Requires Erik Dubois repo — installs tweak-tool + arcolinux-app + sofirem",
        "cmd":     ["bash", str(BASE_DIR / "add-repos/install_arcolinux_apps.sh")],
    },
]


def _build_maintenance_tab() -> None:
    with dpg.tab(label="   System Maintenance   "):
        dpg.add_spacer(height=8)
        dpg.add_text("  System Maintenance", color=AQUA)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        for action in MAINTENANCE_ACTIONS:
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=f"  {action['label']}  ",
                    width=260,
                    callback=lambda s, a, u: _launch_in_terminal(" ".join(u["cmd"])),
                    user_data=action,
                )
                dpg.add_spacer(width=12)
                dpg.add_text(action["desc"], color=DIM)
            dpg.add_spacer(height=6)


# =============================================================================
# Theme
# =============================================================================
def _apply_theme() -> None:
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,          BG)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,           BG2)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg,           BG2)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,           (68, 80, 88, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,    HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,     SEL)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg,           BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,     HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,       BG)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,     BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, BLUE)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,  AQUA)
            dpg.add_theme_color(dpg.mvThemeCol_Button,            BG2)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,     HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,      SEL)
            dpg.add_theme_color(dpg.mvThemeCol_Header,            HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,     SEL)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,      SEL)
            dpg.add_theme_color(dpg.mvThemeCol_Tab,               BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered,        SEL)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive,         HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused,      BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,     HEADER)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong,  BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight,   BG2)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg,         BG)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt,      BG2)
            dpg.add_theme_color(dpg.mvThemeCol_Text,              FG)
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg,    SEL)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled,      DIM)
            dpg.add_theme_color(dpg.mvThemeCol_Border,            BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow,      BG)
            dpg.add_theme_color(dpg.mvThemeCol_Separator,         BORDER)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered,  BLUE)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,         GREEN)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding,    8)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,     6)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,     5)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding,       6)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,      8, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,       8, 5)
            dpg.add_theme_style(dpg.mvStyleVar_CellPadding,       8, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,     12, 12)
    dpg.bind_theme(global_theme)


# =============================================================================
# Font
# =============================================================================
def _try_load_font() -> None:
    candidates = [
        Path("/usr/share/fonts/TTF/MesloLGS NF Regular.ttf"),
        Path("/usr/share/fonts/TTF/MesloLGSNFRegular.ttf"),
        Path.home() / ".local/share/fonts/MesloLGS NF Regular.ttf",
        Path("/usr/share/fonts/nerd-fonts-complete/Meslo/MesloLGS NF Regular.ttf"),
    ]
    for search_dir in [Path("/usr/share/fonts"), Path.home() / ".local/share/fonts"]:
        if search_dir.exists() and not any(p.exists() for p in candidates):
            matches = list(search_dir.rglob("MesloLGS*Regular*.ttf"))
            if matches:
                candidates.insert(0, matches[0])
                break
    with dpg.font_registry():
        for p in candidates:
            if p.exists():
                try:
                    font = dpg.add_font(str(p), 15)
                    dpg.bind_font(font)
                    return
                except Exception:
                    continue


# =============================================================================
# Main
# =============================================================================
def main() -> None:
    dpg.create_context()
    _apply_theme()
    _try_load_font()

    with dpg.window(tag="primary", no_title_bar=True, no_move=True,
                    no_resize=False, no_scrollbar=True):
        dpg.add_text("  Arch-Boki — Post Install", color=AQUA)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        with dpg.tab_bar():
            _build_welcome_tab()
            _build_apps_tab()
            _build_core_tab()
            _build_maintenance_tab()

    vp_w, vp_h = 1100, 720
    cx, cy = _screen_center(vp_w, vp_h)
    dpg.create_viewport(
        title="Arch-Boki — Post Install",
        width=vp_w,
        height=vp_h,
        x_pos=cx,
        y_pos=cy,
        min_width=800,
        min_height=520,
        clear_color=list(BG[:3]) + [255],
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary", True)

    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: dpg.stop_dearpygui())

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
