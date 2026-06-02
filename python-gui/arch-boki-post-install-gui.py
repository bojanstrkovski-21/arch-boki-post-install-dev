#!/usr/bin/env python3
# =============================================================================
# arch-boki-post-install-gui.py — Arch-Boki Post Install GUI
# Dear PyGui — Everforest theme
# Tabs: Welcome | Install Apps | Core Utils & Drivers | System Maintenance
# =============================================================================

import json
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

try:
    import dearpygui.dearpygui as dpg
except ImportError:
    print("dearpygui not installed. Run: sudo pacman -S python-dearpygui", file=sys.stderr)
    sys.exit(1)

from actions import AUR_PKGS, MAINTENANCE_ACTIONS, TERMINALS

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent

# ── Settings ──────────────────────────────────────────────────────────────────
_SETTINGS_FILE = BASE_DIR / "settings.json"


def _load_settings() -> dict:
    if _SETTINGS_FILE.exists():
        try:
            return json.loads(_SETTINGS_FILE.read_text())
        except Exception:
            pass
    return {"terminal": "alacritty", "pkg_manager": "yay"}


def _save_settings(s: dict) -> None:
    try:
        _SETTINGS_FILE.write_text(json.dumps(s, indent=2))
    except Exception:
        pass


_settings = _load_settings()


# ── Polkit policy bootstrap & root elevation ──────────────────────────────────
_POLICY_SRC = BASE_DIR / "org.archboki.postinstall.policy"
_POLICY_DST = Path("/usr/share/polkit-1/actions/org.archboki.postinstall.policy")


def _install_policy_if_needed() -> None:
    if _POLICY_DST.exists() or not _POLICY_SRC.exists():
        return
    subprocess.run(["pkexec", "cp", str(_POLICY_SRC), str(_POLICY_DST)], check=False)


def _ensure_root() -> None:
    if os.getuid() != 0:
        env_vars = []
        for var in ("DISPLAY", "XAUTHORITY", "WAYLAND_DISPLAY", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS"):
            val = os.environ.get(var)
            if val:
                env_vars.append(f"{var}={val}")
        script = os.path.abspath(__file__)
        os.execvp("pkexec", ["pkexec", "env"] + env_vars + [script] + sys.argv[1:])


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
                ("Code",               ["code"]),
                ("Meld",               ["meld"]),
                ("Notepadqq",          ["notepadqq"]),
                ("PyCharm CE",         ["pycharm-community-edition"]),
                ("VSCodium",           ["vscodium", "vscodium-marketplace"]),
                ("Visual Studio Code", ["visual-studio-code-bin"]),
                ("Zed",                ["zed"]),
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
                ("Brave",         ["brave-bin"]),
                ("Chromium",      ["chromium"]),
                ("Firefox",       ["firefox"]),
                ("Firefox ESR",   ["firefox-esr"]),
                ("Google Chrome", ["google-chrome"]),
                ("Librewolf",     ["librewolf"]),
                ("Qutebrowser",   ["qutebrowser"]),
                ("Vivaldi",       ["vivaldi", "vivaldi-ffmpeg-codecs"]),
            ],
            "Downloaders": [
                ("Deluge GTK",       ["deluge-gtk"]),
                ("KTorrent",         ["ktorrent"]),
                ("qBittorrent",      ["qbittorrent"]),
                ("Transmission GTK", ["transmission-gtk"]),
                ("Transmission Qt",  ["transmission-qt"]),
            ],
            "Recorders": [
                ("GPU Screen Recorder",  ["gpu-screen-recorder", "gpu-screen-recorder-gtk"]),
                ("Hyprshot",             ["hyprshot"]),
                ("Kazam",                ["kazam"]),
                ("OBS Studio",           ["obs-studio"]),
                ("Peek",                 ["peek"]),
                ("SimpleScreenRecorder", ["simplescreenrecorder-qt6-git"]),
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
                ("Ardour",         ["ardour"]),
                ("Audacity",       ["audacity"]),
                ("Kwave",          ["kwave"]),
                ("LMMS",           ["lmms"]),
                ("Reaper",         ["reaper", "reapack", "sws"]),
                ("SoundConverter", ["soundconverter"]),
                ("Tenacity",       ["tenacity"]),
            ],
            "Video Editors": [
                ("Flowblade",   ["flowblade"]),
                ("Handbrake",   ["handbrake"]),
                ("Kdenlive",    ["kdenlive"]),
                ("LosslessCut", ["losslesscut-bin"]),
                ("MakeMKV",     ["makemkv", "mkvtoolnix-cli", "mkvtoolnix-gui"]),
                ("Openshot",    ["openshot"]),
                ("Shotcut",     ["shotcut"]),
            ],
            "Subtitle Editors": [
                ("Aegisub",          ["aegisub"]),
                ("SubtitleEdit",     ["subtitleedit"]),
                ("SubtitleComposer", ["subtitlecomposer"]),
            ],
        },
    },
    "Graphics": {
        "_flat": False,
        "subcategories": {
            "Image Viewers": [
                ("Darktable", ["darktable"]),
                ("Ephoto",    ["ephoto"]),
                ("GPicView",  ["gpicview"]),
                ("Gwenview",  ["gwenview"]),
                ("Nomacs",    ["nomacs"]),
                ("Nsxiv",     ["nsxiv"]),
                ("Qimgv",     ["qimgv-git"]),
                ("Ristretto", ["ristretto"]),
            ],
            "Image Editors": [
                ("GIMP",        ["gimp"]),
                ("Gpick",       ["gpick"]),
                ("Inkscape",    ["inkscape"]),
                ("Krita",       ["krita"]),
                ("Pinta",       ["pinta"]),
                ("RawTherapee", ["rawtherapee"]),
                ("Upscayl",     ["upscayl-desktop-git", "upscayl-models-desktop"]),
            ],
            "Wallpaper Changers": [
                ("Azote",      ["azote"]),
                ("Feh",        ["feh"]),
                ("Hyprpaper",  ["hyprpaper"]),
                ("Nitrogen",   ["nitrogen"]),
                ("Swaybg",     ["swaybg"]),
                ("Swww",       ["swww"]),
                ("Variety",    ["variety"]),
                ("Waypaper",   ["waypaper-git"]),
                ("Xwallpaper", ["xwallpaper"]),
            ],
        },
    },
    "System Info": {
        "_flat": True,
        "items": [
            ("Bashtop",           ["bashtop"]),
            ("Btop",              ["btop"]),
            ("Countryfetch",      ["countryfetch"]),
            ("Cpufetch",          ["cpufetch"]),
            ("Fastfetch",         ["fastfetch"]),
            ("Glances",           ["glances"]),
            ("Gtop",              ["gtop"]),
            ("Htop",              ["htop"]),
            ("Hyfetch",           ["hyfetch"]),
            ("Mission Center",    ["mission-center"]),
            ("Nvtop",             ["nvtop"]),
            ("Resources",         ["resources"]),
            ("Stacer",            ["stacer-bin"]),
            ("Xfce4-Taskmanager", ["xfce4-taskmanager"]),
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
                ("Flameshot",           ["flameshot"]),
                ("Kazam",               ["kazam"]),
                ("Ksnip",               ["ksnip"]),
                ("Shutter",             ["shutter"]),
                ("Spectacle",           ["spectacle"]),
                ("Xfce4-Screenshooter", ["xfce4-screenshooter"]),
            ],
            "Screen Resolution": [
                ("Arandr",       ["arandr"]),
                ("nwg-displays", ["nwg-displays"]),
                ("Wdisplays",    ["wdisplays"]),
                ("Wlr-randr",    ["wlr-randr"]),
                ("Xorg-xrandr",  ["xorg-xrandr"]),
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
def _launch_in_terminal(bash_cmd: str) -> None:
    term = _settings.get("terminal", "alacritty")
    full = bash_cmd + '; echo; printf "\\n  Press Enter to close..."; read'
    if term == "xfce4-terminal":
        subprocess.Popen([term, "--command", f"bash -c '{full}'"])
    else:
        subprocess.Popen([term, "-e", "bash", "-c", full])


def _install_packages(pkgs: list[str]) -> None:
    if not pkgs:
        return
    manager = _settings.get("pkg_manager", "yay")
    pkg_str = " ".join(pkgs)
    if manager in ("yay", "paru"):
        cmd = (
            f'{_REAL_USER}'
            f' && sudo -u "$_ru" {manager} -S --needed --noconfirm {pkg_str}'
        )
    else:
        cmd = f"pacman -S --needed --noconfirm {pkg_str}"
    _launch_in_terminal(cmd)


def _uninstall_packages(pkgs: list[str]) -> None:
    if not pkgs:
        return
    _launch_in_terminal("pacman -Rns --noconfirm " + " ".join(pkgs))


def _install_font_packages(pkgs: list[str]) -> None:
    if not pkgs:
        return
    _launch_in_terminal(_mgr_install_cmd(pkgs, "fc-cache -fv"))


# =============================================================================
# pacman.conf helpers (pure Python — runs as root, no terminal needed)
# =============================================================================
def _get_parallel_downloads() -> str:
    try:
        text = Path("/etc/pacman.conf").read_text()
        m = re.search(r"^ParallelDownloads\s*=\s*(\d+)", text, re.MULTILINE)
        return m.group(1) if m else "not set"
    except Exception:
        return "unknown"


def _is_option_enabled(option: str) -> bool:
    try:
        text = Path("/etc/pacman.conf").read_text()
        return bool(re.search(rf"^{option}\s*$", text, re.MULTILINE))
    except Exception:
        return False


def _toggle_pacman_option(option: str, enable: bool) -> None:
    conf = Path("/etc/pacman.conf")
    try:
        text = conf.read_text()
        commented = re.search(rf"^#\s*{option}\s*$", text, re.MULTILINE)
        active    = re.search(rf"^{option}\s*$",     text, re.MULTILINE)
        if enable:
            if commented:
                text = re.sub(rf"^#\s*{option}\s*$", option, text, flags=re.MULTILINE)
            elif not active:
                text = re.sub(r"(\[options\])", f"\\1\n{option}", text)
        else:
            if active:
                text = re.sub(rf"^{option}\s*$", f"#{option}", text, flags=re.MULTILINE)
        conf.write_text(text)
    except Exception as e:
        print(f"Error toggling {option}: {e}", file=sys.stderr)


def _apply_parallel_downloads() -> None:
    raw = dpg.get_value("pd_input").strip()
    if not raw.isdigit() or not (1 <= int(raw) <= 14):
        dpg.set_value("pd_status", "  Invalid — enter a number between 1 and 14")
        dpg.set_value("pd_input", "")
        return
    num = raw
    conf = Path("/etc/pacman.conf")
    try:
        text = conf.read_text()
        if re.search(r"^#?ParallelDownloads", text, re.MULTILINE):
            text = re.sub(r"^#*ParallelDownloads.*", f"ParallelDownloads = {num}", text, flags=re.MULTILINE)
        else:
            text = re.sub(r"(\[options\])", f"\\1\nParallelDownloads = {num}", text)
        conf.write_text(text)
        dpg.set_value("pd_status", f"  Done — ParallelDownloads set to {num}")
        dpg.set_value("pd_current", f"(currently: {num})")
    except Exception as e:
        dpg.set_value("pd_status", f"  Error: {e}")
    dpg.set_value("pd_input", "")


# =============================================================================
# TAB 1 — Welcome
# =============================================================================
def _build_welcome_tab() -> None:
    with dpg.tab(label="   Welcome   "):
        dpg.add_spacer(height=20)
        _logo_data = [
            ("      █████╗ ██████╗  ██████╗██╗  ██╗      ██████╗  ██████╗ ██╗  ██╗██╗", AQUA),
            ("     ██╔══██╗██╔══██╗██╔════╝██║  ██║      ██╔══██╗██╔═══██╗██║ ██╔╝██║", AQUA),
            ("     ███████║██████╔╝██║     ███████║█████╗██████╔╝██║   ██║█████╔╝ ██║", GREEN),
            ("     ██╔══██║██╔══██╗██║     ██╔══██║╚════╝██╔══██╗██║   ██║██╔═██╗ ██║", GREEN),
            ("     ██║  ██║██║  ██║╚██████╗██║  ██║      ██████╔╝╚██████╔╝██║  ██╗██║", AQUA),
            ("     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝", AQUA),
        ]
        _line_h = 12
        _logo_size = 96
        _gap = 8
        _has_logo = dpg.does_item_exist("logo_tex")
        _max_chars = max(len(t) for t, _ in _logo_data)
        _char_w = 7
        _art_text_w = _max_chars * _char_w
        _art_h = _logo_size if _has_logo else _line_h * len(_logo_data)
        _y_off = (_art_h - _line_h * len(_logo_data)) // 2
        _total_w = ((_logo_size + _gap) if _has_logo else 0) + _art_text_w
        _indent = max(0, (1076 - _total_w) // 2)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=_indent)
            if _has_logo:
                dpg.add_image("logo_tex", width=_logo_size, height=_logo_size)
                dpg.add_spacer(width=_gap)
            with dpg.drawlist(width=_art_text_w, height=_art_h):
                for i, (txt, col) in enumerate(_logo_data):
                    dpg.draw_text((0, _y_off + i * _line_h), txt, color=col, size=12)
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
        dpg.add_text("    — First add chaotic AUR repository and install aur helper 'yay'", color=FG)
        dpg.add_text("    — Optional add arch-boki-repo or nemesis-repo", color=FG)
        dpg.add_text("    — Sudo access is required for package installation", color=FG)
        dpg.add_text("    — Authentication via pkexec is requested at startup", color=FG)

        # ── Terminal selector ─────────────────────────────────────────────────
        dpg.add_spacer(height=12)
        dpg.add_separator()
        dpg.add_spacer(height=8)
        dpg.add_text("  Terminal", color=YELLOW)
        dpg.add_spacer(height=4)
        with dpg.group(horizontal=True):
            dpg.add_text("  Terminal used to run commands:", color=FG)
            dpg.add_spacer(width=8)
            dpg.add_combo(
                TERMINALS,
                default_value=_settings.get("terminal", "alacritty"),
                tag="terminal_combo",
                width=180,
                callback=lambda s, a: (_settings.update({"terminal": a}), _save_settings(_settings)),
            )

        # ── Package manager selector ──────────────────────────────────────────
        dpg.add_spacer(height=12)
        dpg.add_separator()
        dpg.add_spacer(height=8)
        dpg.add_text("  Package Manager", color=YELLOW)
        dpg.add_spacer(height=4)
        with dpg.group(horizontal=True):
            dpg.add_text("  Package manager used to install packages:", color=FG)
            dpg.add_spacer(width=8)
            dpg.add_combo(
                ["yay", "paru", "pacman"],
                default_value=_settings.get("pkg_manager", "yay"),
                tag="pkg_manager_combo",
                width=120,
                callback=lambda s, a: (_settings.update({"pkg_manager": a}), _save_settings(_settings)),
            )
        dpg.add_spacer(height=4)
        dpg.add_text(
            "  yay / paru handle both official repos and AUR — recommended.\n"
            "  pacman handles official repos only.",
            color=DIM,
        )


# =============================================================================
# TAB 2 — Install Apps
# =============================================================================
def _get_apps_selected(cat: str, subcat: str | None) -> list[str]:
    data = INSTALL_APPS[cat]
    items = data["items"] if data["_flat"] else (data["subcategories"].get(subcat, []) if subcat else [])
    selected: list[str] = []
    for label, pkgs in items:
        tag = f"chk__{cat}__{subcat}__{label}".replace(" ", "_")
        if dpg.does_item_exist(tag) and dpg.get_value(tag):
            selected.extend(pkgs)
    return selected


def _install_selected(cat: str, subcat: str | None) -> None:
    pkgs = _get_apps_selected(cat, subcat)
    if pkgs:
        _install_packages(pkgs)


def _uninstall_selected(cat: str, subcat: str | None) -> None:
    pkgs = _get_apps_selected(cat, subcat)
    if pkgs:
        _uninstall_packages(pkgs)


def _rebuild_apps_content(cat: str, subcat: str | None, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    data = INSTALL_APPS[cat]

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
                            inst = _installed_cache.get(pkgs[0])
                            lbl  = f"  {label}" + ("  ✓" if inst else "")
                            dpg.add_checkbox(label=lbl, tag=tag, default_value=False)
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
            _ib = dpg.add_button(
                label="  Install Selected  ",
                callback=lambda s, a, u: _install_selected(u[0], u[1]),
                user_data=(cat, subcat),
            )
            dpg.bind_item_theme(_ib, INSTALL_BTN_THEME)
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="  Uninstall Selected  ",
                callback=lambda s, a, u: _uninstall_selected(u[0], u[1]),
                user_data=(cat, subcat),
            )


def _build_apps_tab() -> None:
    with dpg.tab(label="   Install Apps   "):
        dpg.add_spacer(height=8)
        content_tag = "apps_content"
        with dpg.group(horizontal=True):

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
        "_buttons": True,
        "items": [
            ("Intel Microcode", ["intel-ucode"]),
            ("AMD Microcode",   ["amd-ucode"]),
        ],
    },
    "GPU Drivers": {
        "_flat": True,
        "_buttons": True,
        "_sections": [
            {
                "title": "Nvidia",
                "items": [
                    ("NVIDIA (proprietary)", ["nvidia", "nvidia-utils", "nvidia-settings"]),
                    ("NVIDIA (open-dkms)",   ["nvidia-open-dkms", "nvidia-utils", "nvidia-settings"]),
                    ("Nouveau (OSS)",        ["xf86-video-nouveau"]),
                ],
            },
            {
                "title": "AMD",
                "items": [
                    ("AMD (mesa)",           ["mesa", "mesa-utils", "vulkan-radeon", "libva-mesa-driver", "mesa-vdpau"]),
                ],
            },
            {
                "title": "Intel",
                "items": [
                    ("Intel (mesa)",         ["mesa", "mesa-utils", "vulkan-intel", "intel-media-driver"]),
                ],
            },
        ],
        "items": [],
    },
    "Audio Drivers": {
        "_audio": True,
        "items": [],
    },
    "Bluetooth": {
        "_flat": True,
        "_buttons": True,
        "items": [
            ("BlueTooth utils", ["bluez", "bluez-utils", "bluez-libs", "blueman"]),
        ],
    },
    "Network": {
        "_flat": True,
        "_sections": [
            {
                "title": "Network Drivers & Tools",
                "items": [
                    ("NetworkManager",             ["networkmanager", "network-manager-applet", "nm-connection-editor"]),
                    ("NetworkManager VPN Plugins", ["networkmanager-openvpn", "networkmanager-openconnect"]),
                    ("Network Tools",              ["net-tools", "ethtool", "avahi", "nss-mdns", "openresolv", "netctl"]),
                    ("File Sharing (SMB/NFS)",     ["samba", "nfs-utils", "nfsidmap", "mkinitcpio-nfs-utils", "libnfs"]),
                    ("GVFS",                       ["gvfs", "gvfs-afc", "gvfs-dnssd", "gvfs-goa", "gvfs-gphoto2", "gvfs-mtp", "gvfs-nfs", "gvfs-smb"]),
                    ("iwd wireless daemon",        ["iwd"]),
                    ("Legacy wireless tools",      ["wireless_tools", "wpa_supplicant"]),
                ],
            },
            {
                "title": "Firewall Utilities",
                "items": [
                    ("nftables",   ["iptables-nft", "nftables"]),
                    ("firewalld",  ["firewalld", "firewall-config"]),
                    ("ufw + gufw", ["ufw", "gufw"]),
                ],
            },
        ],
        "items": [],
    },
    "Printer Drivers": {
        "_printers": True,
        "items": [],
    },
    "Fonts": {
        "_flat": True,
        "items": [
            ("Carlito",                ["ttf-carlito"]),
            ("Cascadia Code",          ["ttf-cascadia-code"]),
            ("Croscore",               ["ttf-croscore"]),
            ("DejaVu",                 ["ttf-dejavu"]),
            ("Fantasque Sans Mono",    ["ttf-fantasque-sans-mono"]),
            ("Fira Code",              ["ttf-fira-code"]),
            ("Fira Mono",              ["ttf-fira-mono"]),
            ("Fira Sans",              ["ttf-fira-sans"]),
            ("Font Awesome-otf",       ["otf-font-awesome"]),
            ("Font Awesome-woff2",     ["woff2-font-awesome"]),
            ("Hack",                   ["ttf-hack"]),
            ("Inter",                  ["inter-font"]),
            ("JetBrains Mono",         ["ttf-jetbrains-mono"]),
            ("Liberation",             ["ttf-liberation"]),
            ("Ms-Fonts",               ["ttf-ms-fonts"]),
            ("Noto",                   ["noto-fonts"]),
            ("Noto CJK",               ["noto-fonts-cjk"]),
            ("Noto Extra",             ["noto-fonts-extra"]),
            ("Open Sans",              ["ttf-opensans"]),
            ("Roboto",                 ["ttf-roboto"]),
            ("Roboto Mono",            ["ttf-roboto-mono"]),
            ("Terminus",               ["terminus-font"]),
            ("Ubuntu Font Family",     ["ttf-ubuntu-font-family"]),
        ],
    },
    "Core Utils": {
        "_cmdbuttons": True,
        "items": [],
    },
}


# =============================================================================
# Nerd Fonts — direct download from GitHub releases (no pacman)
# =============================================================================
NERD_FONTS_VERSION = "v3.4.0"

NERD_FONTS = [
    "0xProto", "3270", "Agave", "AnonymousPro", "Arimo",
    "AurulentSansMono", "BigBlueTerminal", "BitstreamVeraSansMono",
    "BlexMono", "CascadiaCode", "CascadiaMono", "CodeNewRoman",
    "ComicShannsMono", "CommitMono", "Cousine", "D2Coding",
    "DaddyTimeMono", "DejaVuSansMono", "DroidSansMono", "EnvyCodeR",
    "FantasqueSansMono", "FiraCode", "FiraMono", "GeistMono",
    "Go-Mono", "Gohu", "Hack", "Hasklig", "HeavyData", "Hermit",
    "IBMPlexMono", "Inconsolata", "InconsolataGo", "InconsolataLGC",
    "IntelOneMono", "Iosevka", "IosevkaTerm", "IosevkaTermSlab",
    "JetBrainsMono", "Lekton", "Lilex", "LiterationMono", "Meslo",
    "Monaspace", "Monofur", "Monoid", "Mononoki", "MPlus",
    "NerdFontsSymbolsOnly", "Noto", "OpenDyslexic", "Overpass",
    "ProFont", "ProggyClean", "RobotoMono", "ShareTechMono",
    "SourceCodePro", "SpaceMono", "Terminus", "Tinos",
    "Ubuntu", "UbuntuMono", "UbuntuSans", "VictorMono", "ZedMono",
]

_NERD_FONT_BASH_HEADER = (
    '_nf_home=$(getent passwd "${PKEXEC_UID:-0}" | cut -d: -f6 2>/dev/null || echo "$HOME")\n'
    'FONT_VERSION="' + NERD_FONTS_VERSION + '"\n'
    'FONTS_DIR="$_nf_home/.local/share/fonts"\n'
    'TEMP_DIR="/tmp/nerdfonts_$$"\n'
    'mkdir -p "$FONTS_DIR" "$TEMP_DIR"\n'
    'command -v wget  &>/dev/null || pacman -S --noconfirm --needed wget\n'
    'command -v unzip &>/dev/null || pacman -S --noconfirm --needed unzip\n'
    '\n'
    'install_nerd_font() {\n'
    '    local font="$1"\n'
    '    if [ -d "$FONTS_DIR/$font" ] && [ "$(ls -A "$FONTS_DIR/$font" 2>/dev/null)" ]; then\n'
    '        echo "  $font already installed — skipping"\n'
    '    else\n'
    '        echo "  Downloading $font..."\n'
    '        if wget --timeout=30 -q --show-progress \\\n'
    '                "https://github.com/ryanoasis/nerd-fonts/releases/download/${FONT_VERSION}/${font}.zip" \\\n'
    '                -P "$TEMP_DIR"; then\n'
    '            mkdir -p "$FONTS_DIR/$font"\n'
    '            if unzip -q "$TEMP_DIR/${font}.zip" -d "$FONTS_DIR/$font/"; then\n'
    '                echo "  ✓ $font installed"\n'
    '            else\n'
    '                echo "  ✗ Failed to extract $font"\n'
    '                rm -rf "$FONTS_DIR/$font"\n'
    '            fi\n'
    '            rm -f "$TEMP_DIR/${font}.zip"\n'
    '        else\n'
    '            echo "  ✗ Failed to download $font"\n'
    '        fi\n'
    '    fi\n'
    '}\n'
)


def _get_real_user_home() -> Path:
    try:
        import pwd
        for var in ("PKEXEC_UID", "SUDO_UID"):
            val = os.environ.get(var)
            if val and val != "0":
                return Path(pwd.getpwuid(int(val)).pw_dir)
    except Exception:
        pass
    return Path.home()


def _nerd_font_installed(font: str) -> bool:
    home = _get_real_user_home()
    for base in (
        home / ".local/share/fonts",
        home / ".fonts",
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
    ):
        d = base / font
        try:
            if d.is_dir() and any(d.iterdir()):
                return True
        except Exception:
            pass
    return False


def _install_nerd_fonts(fonts: list[str]) -> None:
    if not fonts:
        return
    calls = "\n".join(f'install_nerd_font "{f}"' for f in fonts)
    cmd = (
        _NERD_FONT_BASH_HEADER
        + calls
        + '\n\nfc-cache -fv\nrm -rf "$TEMP_DIR"\necho\necho "Done!"'
    )
    _launch_in_terminal(cmd)


def _uninstall_nerd_fonts(fonts: list[str]) -> None:
    if not fonts:
        return
    home = '_nf_home=$(getent passwd "${PKEXEC_UID:-0}" | cut -d: -f6 2>/dev/null || echo "$HOME")'
    removes = "\n".join(
        f'rm -rf "$_nf_home/.local/share/fonts/{f}" "$_nf_home/.fonts/{f}" 2>/dev/null || true'
        for f in fonts
    )
    cmd = (
        f"{home}\n"
        + removes
        + '\nfc-cache -fv\necho\necho "Done — removed selected Nerd Fonts."'
    )
    _launch_in_terminal(cmd)


_PIPEWIRE_PKGS = [
    "alsa-utils", "alsa-firmware", "alsa-plugins", "alsa-lib", "alsa-topology-conf",
    "gstreamer", "gst-libav", "gst-plugins-bad", "gst-plugins-base", "gst-plugins-good",
    "gst-plugins-ugly", "cdrdao", "faac", "faad2", "ffmpeg",
    "ffmpegthumbnailer", "flac", "frei0r-plugins", "imagemagick", "lame", "libdvdcss",
    "libopenraw", "x265", "x264", "xvidcore", "pavucontrol", "pipewire", "pipewire-audio",
    "pipewire-docs", "pipewire-pulse", "pipewire-alsa", "pipewire-jack",
    "pipewire-zeroconf", "playerctl", "volctl", "wireplumber",
]

_PULSEAUDIO_PKGS = [
    "jack2", "pulseaudio", "pulseaudio-alsa", "pulseaudio-bluetooth",
    "pulseaudio-equalizer", "pulseaudio-jack", "pulseaudio-zeroconf", "pavucontrol",
    "alsa-firmware", "alsa-lib", "alsa-plugins", "alsa-utils", "alsa-topology-conf",
    "gstreamer", "gst-plugins-good", "gst-plugins-bad", "gst-plugins-base",
    "gst-plugins-ugly", "gst-libav", "cdrdao", "faac", "faad2",
    "ffmpeg", "ffmpegthumbnailer", "flac", "frei0r-plugins", "imagemagick", "lame",
    "libdvdcss", "libopenraw", "x265", "x264", "xvidcore", "playerctl", "volctl",
]

def _pipewire_cmd() -> str:
    mgr = _settings.get("pkg_manager", "yay")
    if mgr in ("yay", "paru"):
        install = (
            f'{_REAL_USER}'
            f' && sudo -u "$_ru" {mgr} -Sy --needed --noconfirm'
            " alsa-utils alsa-firmware alsa-plugins alsa-lib alsa-topology-conf"
            " gstreamer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good"
            " gst-plugins-ugly cdrdao faac faad2 ffmpeg ffmpegthumbnailer"
            " flac frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore"
            " pavucontrol pipewire pipewire-audio pipewire-docs pipewire-pulse pipewire-alsa"
            " pipewire-jack pipewire-zeroconf playerctl volctl wireplumber"
        )
    else:
        install = (
            "pacman -Sy --needed --noconfirm"
            " alsa-utils alsa-firmware alsa-plugins alsa-lib alsa-topology-conf"
            " gstreamer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good"
            " gst-plugins-ugly cdrdao faac faad2 ffmpeg ffmpegthumbnailer"
            " flac frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore"
            " pavucontrol pipewire pipewire-audio pipewire-docs pipewire-pulse pipewire-alsa"
            " pipewire-jack pipewire-zeroconf playerctl volctl wireplumber"
        )
    return (
        "pacman -Rdd --noconfirm jack2 pulseaudio-bluetooth pulseaudio pulseaudio-alsa"
        " pulseaudio-equalizer pulseaudio-jack pulseaudio-zeroconf pavucontrol"
        " alsa-firmware alsa-lib alsa-plugins alsa-utils alsa-topology-conf"
        " gstreamer gst-plugins-good gst-plugins-bad gst-plugins-base gst-plugins-ugly"
        " gst-libav cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac"
        " frei0r-plugins imagemagick lame libdvdcss libopenraw x265 x264 xvidcore"
        f" playerctl volctl 2>/dev/null || true && {install}"
        ' && echo "" && echo "PipeWire installation complete."'
    )


def _pulseaudio_cmd() -> str:
    mgr = _settings.get("pkg_manager", "yay")
    if mgr in ("yay", "paru"):
        install = (
            f'{_REAL_USER}'
            f' && sudo -u "$_ru" {mgr} -Sy --needed --noconfirm'
            " jack2 pulseaudio pulseaudio-alsa pulseaudio-bluetooth pulseaudio-equalizer"
            " pulseaudio-jack pulseaudio-zeroconf pavucontrol alsa-firmware alsa-lib"
            " alsa-plugins alsa-utils alsa-topology-conf gstreamer gst-plugins-good"
            " gst-plugins-bad gst-plugins-base gst-plugins-ugly gst-libav"
            " cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac frei0r-plugins imagemagick"
            " lame libdvdcss libopenraw x265 x264 xvidcore playerctl volctl"
        )
    else:
        install = (
            "pacman -Sy --needed --noconfirm"
            " jack2 pulseaudio pulseaudio-alsa pulseaudio-bluetooth pulseaudio-equalizer"
            " pulseaudio-jack pulseaudio-zeroconf pavucontrol alsa-firmware alsa-lib"
            " alsa-plugins alsa-utils alsa-topology-conf gstreamer gst-plugins-good"
            " gst-plugins-bad gst-plugins-base gst-plugins-ugly gst-libav"
            " cdrdao faac faad2 ffmpeg ffmpegthumbnailer flac frei0r-plugins imagemagick"
            " lame libdvdcss libopenraw x265 x264 xvidcore playerctl volctl"
        )
    return (
        "pacman -Rdd --noconfirm alsa-utils alsa-firmware alsa-plugins alsa-lib"
        " alsa-topology-conf gstreamer gst-libav gst-plugins-bad gst-plugins-base"
        " gst-plugins-good gst-plugins-ugly cdrdao faac faad2 ffmpeg"
        " ffmpegthumbnailer flac frei0r-plugins imagemagick lame libdvdcss libopenraw"
        " x265 x264 xvidcore pavucontrol pipewire pipewire-audio pipewire-docs"
        " pipewire-pulse pipewire-alsa pipewire-jack pipewire-zeroconf playerctl"
        f" volctl wireplumber 2>/dev/null || true && {install}"
        ' && echo "" && echo "PulseAudio installation complete."'
    )


INSTALL_BTN_THEME: int = 0


def _create_install_btn_theme() -> None:
    global INSTALL_BTN_THEME
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,        (56,  65,  71,  180))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (127, 187, 179,  100))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,  (127, 187, 179,  140))
            dpg.add_theme_color(dpg.mvThemeCol_Text,          (211, 198, 170, 255))
    INSTALL_BTN_THEME = t


def _rebuild_audio_content(content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    with dpg.group(parent=content_tag):
        with dpg.child_window(height=-8, border=False):

            cache_dir  = str(_get_cache_path().parent)
            pw_active  = bool(_installed_cache.get("pipewire"))
            pa_active  = bool(_installed_cache.get("pulseaudio"))

            # PipeWire
            if pw_active:
                _pw_missing = [p for p in _PIPEWIRE_PKGS if not _installed_cache.get(p)]
                _pw_status  = "ok" if not _pw_missing else "missing"
            elif pa_active:
                _pw_missing, _pw_status = [], "inactive"
            else:
                _pw_missing, _pw_status = [], "unknown"

            if _pw_status == "ok":
                _pw_lbl = "  ✓  Install PipeWire  "
            elif _pw_status == "missing":
                _pw_lbl = "  !  Install PipeWire  "
            else:
                _pw_lbl = "  Install PipeWire  "

            dpg.add_text("  PipeWire Stack", color=AQUA)
            dpg.add_separator()
            dpg.add_spacer(height=6)
            dpg.add_text(
                "  Removes jack2 + PulseAudio packages, then installs the full\n"
                "  PipeWire stack with gstreamer and multimedia codecs.",
                color=DIM,
            )
            if _pw_status == "inactive":
                dpg.add_text("  PulseAudio is the active stack", color=DIM)
            dpg.add_spacer(height=8)
            pw_btn = dpg.add_button(label=_pw_lbl, callback=lambda: _launch_in_terminal(_pipewire_cmd()))
            dpg.bind_item_theme(pw_btn, INSTALL_BTN_THEME)
            if _pw_status == "missing":
                dpg.add_spacer(height=4)
                dpg.add_text(f"  ! {len(_pw_missing)} pkg(s) missing — see {cache_dir}/missing_pkgs.md", color=YELLOW)
            dpg.add_spacer(height=16)

            # PulseAudio
            if pa_active:
                _pa_missing = [p for p in _PULSEAUDIO_PKGS if not _installed_cache.get(p)]
                _pa_status  = "ok" if not _pa_missing else "missing"
            elif pw_active:
                _pa_missing, _pa_status = [], "inactive"
            else:
                _pa_missing, _pa_status = [], "unknown"

            if _pa_status == "ok":
                _pa_lbl = "  ✓  Install PulseAudio  "
            elif _pa_status == "missing":
                _pa_lbl = "  !  Install PulseAudio  "
            else:
                _pa_lbl = "  Install PulseAudio  "

            dpg.add_text("  PulseAudio Stack", color=AQUA)
            dpg.add_separator()
            dpg.add_spacer(height=6)
            dpg.add_text(
                "  Removes PipeWire packages, then installs the full\n"
                "  PulseAudio stack with gstreamer and multimedia codecs.",
                color=DIM,
            )
            if _pa_status == "inactive":
                dpg.add_text("  PipeWire is the active stack", color=DIM)
            dpg.add_spacer(height=8)
            pa_btn = dpg.add_button(label=_pa_lbl, callback=lambda: _launch_in_terminal(_pulseaudio_cmd()))
            dpg.bind_item_theme(pa_btn, INSTALL_BTN_THEME)
            if _pa_status == "missing":
                dpg.add_spacer(height=4)
                dpg.add_text(f"  ! {len(_pa_missing)} pkg(s) missing — see {cache_dir}/missing_pkgs.md", color=YELLOW)
            dpg.add_spacer(height=16)


EMOJI_ITEMS = [
    ("Noto Emoji",        ["noto-fonts-emoji"]),
    ("Twemoji (Twitter)", ["ttf-twemoji"]),
    ("JoyPixels",         ["ttf-joypixels"]),
    ("Blob Emoji",        ["ttf-blobmoji"]),
]

# =============================================================================
# Search index + installed cache
# =============================================================================
_installed_cache: dict[str, str] = {}


def _get_cache_path() -> Path:
    home = _get_real_user_home()
    cache_dir = home / ".cache" / "arch-boki-post-install-gui"
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        import pwd
        for var in ("PKEXEC_UID", "SUDO_UID"):
            val = os.environ.get(var)
            if val and val != "0":
                pw  = pwd.getpwuid(int(val))
                os.chown(cache_dir, pw.pw_uid, pw.pw_gid)
                break
    except Exception:
        pass
    return cache_dir / "installed.json"


def _refresh_installed_cache() -> None:
    global _installed_cache
    cache_path = _get_cache_path()

    # Load existing cache from file so checkboxes show immediately
    if cache_path.exists():
        try:
            _installed_cache = json.loads(cache_path.read_text())
        except Exception:
            pass

    # Refresh from live pacman -Q and overwrite
    try:
        out = subprocess.check_output(["pacman", "-Q"], text=True)
        fresh: dict[str, str] = {}
        for line in out.splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                fresh[parts[0]] = parts[1].strip()
        _installed_cache = fresh
        # Save to file, fix ownership
        cache_path.write_text(json.dumps(fresh, indent=2))
        try:
            import pwd
            for var in ("PKEXEC_UID", "SUDO_UID"):
                val = os.environ.get(var)
                if val and val != "0":
                    pw = pwd.getpwuid(int(val))
                    os.chown(cache_path, pw.pw_uid, pw.pw_gid)
                    break
        except Exception:
            pass
    except Exception:
        pass


def _build_search_index() -> list[dict]:
    index: list[dict] = []

    def _add(label: str, pkgs: list[str], cat: str) -> None:
        source = "AUR" if any(p in AUR_PKGS for p in pkgs) else "Official"
        index.append({"label": label, "pkgs": pkgs, "cat": cat, "source": source})

    for cat, data in INSTALL_APPS.items():
        if data["_flat"]:
            for label, pkgs in data["items"]:
                _add(label, pkgs, cat)
        else:
            for subcat, items in data["subcategories"].items():
                for label, pkgs in items:
                    _add(label, pkgs, f"{cat} › {subcat}")

    for cat, data in CORE_CATEGORIES.items():
        if "_sections" in data:
            for sec in data["_sections"]:
                for label, pkgs in sec["items"]:
                    _add(label, pkgs, cat)
        if data.get("items"):
            for label, pkgs in data["items"]:
                _add(label, pkgs, cat)

    for sec in _CORE_UTILS_SECTIONS:
        if "grid_items" in sec:
            for label, pkgs in sec["grid_items"]:
                _add(label, pkgs, "Core Utils")

    for label, pkgs in EMOJI_ITEMS:
        _add(label, pkgs, "Fonts › Emoji")

    return index


_REAL_USER = '_ru=${SUDO_USER:-$(getent passwd "$PKEXEC_UID" | cut -d: -f1 2>/dev/null)}'


def _mgr_install_cmd(pkgs: list[str], after: str = "") -> str:
    mgr     = _settings.get("pkg_manager", "yay")
    pkg_str = " ".join(pkgs)
    if mgr in ("yay", "paru"):
        install = f'{_REAL_USER} && sudo -u "$_ru" {mgr} -Sy --needed --noconfirm {pkg_str}'
    else:
        install = f"pacman -Sy --needed --noconfirm {pkg_str}"
    return install + (f" && {after}" if after else "")


_CORE_UTILS_SECTIONS = [
    {
        "title": "Core Utils",
        "desc": (
            "System tools, CLI utilities, build tools, hardware info,\n"
            "shell extras, polkit, Xorg base, flatpak and more."
        ),
        "label": "Install Core Utils",
        "pkgs": [
            "acpid", "acpi", "ananicy-cpp", "appstream", "arandr", "archiso",
            "archlinux-appstream-data", "archlinux-tools", "archlinux-wallpaper",
            "aspell", "aspell-en", "baobab", "base", "base-devel", "bash-completion",
            "bat", "btop", "cachyos-ananicy-rules-git", "catfish", "cmake",
            "cmake-extras", "cpuid", "cronie", "curl", "dconf", "dconf-editor",
            "devtools", "dialog", "dkms", "dnsutils", "dosfstools", "downgrade", "duf",
            "efitools", "expac", "expect", "extra-cmake-modules", "eza", "fastfetch",
            "fd", "feh", "fish", "flatpak", "fwupd", "fzf", "gcc", "git", "glibc",
            "hardcode-fixer-git", "hardinfo2", "hwdata", "hwdetect", "hwinfo",
            "hw-probe", "imagemagick", "inetutils", "intltool", "inxi", "irqbalance",
            "laptop-detect", "libadwaita", "libburn", "libisoburn", "libisofs",
            "linux-firmware", "linux-headers", "lm_sensors", "logrotate", "lolcat",
            "lsb-release", "maim", "make", "menulibre", "mkinitcpio-firmware", "most",
            "mugshot", "openssl", "os-prober", "pacman-contrib", "ncdu", "ntp",
            "numlockx", "pacutils", "pkgfile", "plocate", "polkit", "polkit-gnome",
            "pacmanlogviewer", "pacquery", "pciutils", "pkgconf", "playerctl",
            "power-profiles-daemon", "python", "python-pylint", "python-pyparted",
            "python-pywal", "qt5ct", "qt6ct", "ripgrep", "ripgrep-all", "rsync",
            "sdl12-compat", "sdl2", "sdl3", "starship", "the_silver_searcher", "time",
            "tldr", "tree", "tuned", "udiskie", "udisks2", "udftools", "upower",
            "webkit2gtk", "wget", "xapp", "xclip", "xdg-desktop-portal",
            "xdg-desktop-portal-gtk", "xdg-user-dirs", "xdg-user-dirs-gtk",
            "xdg-utils", "xdo", "xdotool", "xorg-server", "xorg-xinit", "mtpfs",
            "xorg-xrandr", "yad", "zenity", "zsh", "ffmpegthumbnailer", "freetype2",
            "libgsf", "libopenraw", "zram-generator", "poppler", "poppler-data",
            "poppler-glib", "poppler-qt5", "poppler-qt6",
        ],
        "cmd": lambda s: _mgr_install_cmd(s["pkgs"], 'echo "Core utils installed."'),
    },
    {
        "title": "Archiving Utils",
        "desc": "Archive managers and compression tools: 7zip, RAR, ACE, ZIP, ISO/UDF.",
        "label": "Install Archiving Utils",
        "pkgs": [
            "gzip", "bzip2", "xz", "lz4", "lrzip", "lzip", "lzop", "zstd",
            "tar", "zip", "unzip", "7zip", "lha", "unace", "unarj", "unrar",
        ],
        "cmd": lambda s: _mgr_install_cmd(s["pkgs"], 'echo "Archiving utils installed."'),
    },
    {
        "title": "GUI Archiving Software",
        "desc": "Graphical archive managers — works on Wayland and X11.",
        "grid_items": [
            ("File Roller",   ["file-roller"]),
            ("PeaZip",        ["peazip"]),
            ("Engrampa",      ["engrampa"]),
            ("Xarchiver",     ["xarchiver"]),
            ("Ark",           ["ark"]),
            ("LXQt Archiver", ["lxqt-archiver"]),
        ],
    },
]


def _check_section_status(sec: dict) -> tuple[str, list[str]]:
    pkgs = sec.get("pkgs", [])
    if not pkgs:
        return "unknown", []
    missing = [p for p in pkgs if not _installed_cache.get(p)]
    return ("ok" if not missing else "missing"), missing


def _write_missing_report(all_sections: list[dict]) -> None:
    manager   = _settings.get("pkg_manager", "yay")
    cache_dir = _get_cache_path().parent
    md_path   = cache_dir / "missing_pkgs.md"
    lines: list[str] = ["# Missing Packages Report\n\n"]
    has_missing = False

    for sec in all_sections:
        _, missing = _check_section_status(sec)
        if not missing:
            continue
        has_missing = True
        lines.append(f"## {sec['title']}\n\n")
        for p in missing:
            lines.append(f"- `{p}`\n")
        if manager in ("yay", "paru"):
            install_cmd = f"{manager} -S --needed {' '.join(missing)}"
        else:
            install_cmd = f"pacman -S --needed {' '.join(missing)}"
        lines.append(f"\n**Install missing:**\n```bash\n{install_cmd}\n```\n\n")

    if has_missing:
        md_path.write_text("".join(lines))
        try:
            import pwd
            for var in ("PKEXEC_UID", "SUDO_UID"):
                val = os.environ.get(var)
                if val and val != "0":
                    pw = pwd.getpwuid(int(val))
                    os.chown(md_path, pw.pw_uid, pw.pw_gid)
                    break
        except Exception:
            pass
    elif md_path.exists():
        md_path.unlink()


def _rebuild_cmd_sections_content(sections: list, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    with dpg.group(parent=content_tag):
        with dpg.child_window(height=-8, border=False):
            for sec in sections:
                dpg.add_text(f"  {sec['title']}", color=AQUA)
                dpg.add_separator()
                dpg.add_spacer(height=6)
                dpg.add_text(f"  {sec['desc']}", color=DIM)
                dpg.add_spacer(height=8)
                if "grid_items" in sec:
                    cols = 3
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                        for _ in range(cols):
                            dpg.add_table_column()
                        rows = [sec["grid_items"][i:i+cols] for i in range(0, len(sec["grid_items"]), cols)]
                        for row in rows:
                            with dpg.table_row():
                                for label, pkgs in row:
                                    inst    = _installed_cache.get(pkgs[0])
                                    btn_lbl = f"  ✓  {label}  " if inst else f"  {label}  "
                                    _b = dpg.add_button(
                                        label=btn_lbl,
                                        width=-1,
                                        callback=lambda *args: _install_packages(args[2]),
                                        user_data=pkgs,
                                    )
                                    dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
                                for _ in range(cols - len(row)):
                                    dpg.add_text("")
                else:
                    status, missing = _check_section_status(sec)
                    cache_dir = str(_get_cache_path().parent)
                    if status == "ok":
                        btn_lbl = f"  ✓  {sec['label']}  "
                    elif status == "missing":
                        btn_lbl = f"  !  {sec['label']}  "
                    else:
                        btn_lbl = f"  {sec['label']}  "
                    _cmd = sec["cmd"](sec) if callable(sec["cmd"]) else sec["cmd"]
                    _b = dpg.add_button(
                        label=btn_lbl,
                        callback=lambda *args: _launch_in_terminal(args[2]),
                        user_data=_cmd,
                    )
                    dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
                    if status == "missing":
                        dpg.add_spacer(height=4)
                        dpg.add_text(
                            f"  ! {len(missing)} pkg(s) missing — "
                            f"see {cache_dir}/missing_pkgs.md",
                            color=YELLOW,
                        )
                dpg.add_spacer(height=16)


_CUPS_PKGS = [
    "cups", "cups-pdf", "cups-browsed", "cups-filters", "cups-pk-helper",
    "libcups", "ghostscript", "gsfonts", "simple-scan", "system-config-printer",
    "bluez-cups", "foomatic-db", "foomatic-db-engine",
    "foomatic-db-gutenprint-ppds", "gutenprint", "splix",
]


def _cups_ensure() -> str:
    return (
        "pacman -Qi cups &>/dev/null || { "
        + _mgr_install_cmd(_CUPS_PKGS, "systemctl enable --now cups.service cups-browsed.service")
        + '; }'
    )


_PRINTER_SECTIONS = [
    {
        "title": "CUPS Core",
        "desc": (
            "Base print stack: spool, filters, PDF printing, scanner frontend,\n"
            "foomatic/gutenprint PPDs. Enables cups.service + cups-browsed.service."
        ),
        "label": "Install CUPS Core",
        "pkgs": _CUPS_PKGS,
        "cmd": lambda s: _mgr_install_cmd(
            s["pkgs"],
            'systemctl enable --now cups.service cups-browsed.service && echo "CUPS installed and services enabled."',
        ),
    },
    {
        "title": "HP",
        "desc": "HP printer/scanner drivers + proprietary plugin. Installs CUPS if not present.",
        "label": "Install HP Drivers",
        "pkgs": ["hplip", "python-pillow", "python-pip", "python-reportlab", "hplip-plugin"],
        "cmd": lambda s: (
            _cups_ensure()
            + " && " + _mgr_install_cmd(s["pkgs"], 'echo "HP drivers installed."')
        ),
    },
    {
        "title": "Brother",
        "desc": "Brother printer/scanner drivers — brscan4, brscan5, brscan-skey. Installs CUPS if not present.",
        "label": "Install Brother Drivers",
        "pkgs": ["brscan4", "brscan5", "brscan-skey"],
        "cmd": lambda s: (
            _cups_ensure()
            + " && " + _mgr_install_cmd(s["pkgs"], 'echo "Brother drivers installed."')
        ),
    },
    {
        "title": "Canon",
        "desc": "Canon CAPT + CIJFX2 drivers — capt-src, cnijfilter2. Installs CUPS if not present.",
        "label": "Install Canon Drivers",
        "pkgs": ["capt-src", "cnijfilter2"],
        "cmd": lambda s: (
            _cups_ensure()
            + " && " + _mgr_install_cmd(s["pkgs"], 'echo "Canon drivers installed."')
        ),
    },
    {
        "title": "Epson",
        "desc": "Epson ESC/P-R drivers — escpr + escpr2. Installs CUPS if not present.",
        "label": "Install Epson Drivers",
        "pkgs": ["epson-inkjet-printer-escpr", "epson-inkjet-printer-escpr2"],
        "cmd": lambda s: (
            _cups_ensure()
            + " && " + _mgr_install_cmd(s["pkgs"], 'echo "Epson drivers installed."')
        ),
    },
]


def _rebuild_printers_content(content_tag: str) -> None:
    _rebuild_cmd_sections_content(_PRINTER_SECTIONS, content_tag)


def _rebuild_sectioned_content(cat: str, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    sections = CORE_CATEGORIES[cat]["_sections"]
    all_items = [item for s in sections for item in s["items"]]

    with dpg.group(parent=content_tag):
        with dpg.child_window(height=-72, border=False):
            for sec in sections:
                dpg.add_text(f"  {sec['title']}", color=AQUA)
                dpg.add_separator()
                dpg.add_spacer(height=6)
                for label, pkgs in sec["items"]:
                    tag  = f"core_chk__{cat}__{label}".replace(" ", "_")
                    inst = _installed_cache.get(pkgs[0])
                    lbl  = f"  {label}" + ("  ✓" if inst else "")
                    dpg.add_checkbox(label=lbl, tag=tag, default_value=False)
                    dpg.add_text(f"      pkgs: {', '.join(pkgs)}", color=DIM)
                    dpg.add_spacer(height=4)
                dpg.add_spacer(height=10)

        dpg.add_spacer(height=8)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Select All",
                callback=lambda s, a, u: [
                    dpg.set_value(f"core_chk__{u[0]}__{lbl}".replace(" ", "_"), True)
                    for lbl, _ in u[1]
                ],
                user_data=(cat, all_items),
            )
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="Clear All",
                callback=lambda s, a, u: [
                    dpg.set_value(f"core_chk__{u[0]}__{lbl}".replace(" ", "_"), False)
                    for lbl, _ in u[1]
                ],
                user_data=(cat, all_items),
            )
            dpg.add_spacer(width=16)
            _b = dpg.add_button(
                label="  Install Selected  ",
                callback=lambda *args: _install_core_selected(args[2]),
                user_data=cat,
            )
            dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="  Uninstall Selected  ",
                callback=lambda *args: _uninstall_core_selected(args[2]),
                user_data=cat,
            )


def _rebuild_buttons_content(cat: str, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    data = CORE_CATEGORIES[cat]
    sections = data.get("_sections") or [{"title": None, "items": data["items"]}]

    with dpg.group(parent=content_tag):
        with dpg.child_window(height=-8, border=False):
            for sec in sections:
                if sec["title"]:
                    dpg.add_text(f"  {sec['title']}", color=AQUA)
                    dpg.add_separator()
                    dpg.add_spacer(height=6)
                for label, pkgs in sec["items"]:
                    inst     = _installed_cache.get(pkgs[0])
                    btn_lbl  = f"  ✓  {label}  " if inst else f"  Install {label}  "
                    dpg.add_text(f"  {label}", color=FG)
                    dpg.add_text(f"      pkgs: {', '.join(pkgs)}", color=DIM)
                    dpg.add_spacer(height=6)
                    _b = dpg.add_button(
                        label=btn_lbl,
                        callback=lambda *args: _install_packages(args[2]),
                        user_data=pkgs,
                    )
                    dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
                    dpg.add_spacer(height=14)


def _get_core_selected(cat: str) -> list[str]:
    data = CORE_CATEGORIES[cat]
    if "_sections" in data:
        items = [item for s in data["_sections"] for item in s["items"]]
    else:
        items = data["items"]
    selected: list[str] = []
    for label, pkgs in items:
        tag = f"core_chk__{cat}__{label}".replace(" ", "_")
        if dpg.does_item_exist(tag) and dpg.get_value(tag):
            selected.extend(pkgs)
    return selected


def _install_core_selected(cat: str) -> None:
    pkgs = _get_core_selected(cat)
    if pkgs:
        _install_packages(pkgs)


def _uninstall_core_selected(cat: str) -> None:
    pkgs = _get_core_selected(cat)
    if pkgs:
        _uninstall_packages(pkgs)


def _rebuild_core_content(cat: str, content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    items = CORE_CATEGORIES[cat]["items"]

    with dpg.group(parent=content_tag):
        dpg.add_text(f"  {cat}", color=AQUA)
        dpg.add_spacer(height=6)

        with dpg.child_window(height=-72, border=False):
            for label, pkgs in items:
                tag  = f"core_chk__{cat}__{label}".replace(" ", "_")
                inst = _installed_cache.get(pkgs[0])
                lbl  = f"  {label}" + ("  ✓" if inst else "")
                dpg.add_checkbox(label=lbl, tag=tag, default_value=False)
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
            _b = dpg.add_button(
                label="  Install Selected  ",
                callback=lambda *args: _install_core_selected(args[2]),
                user_data=cat,
            )
            dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
            dpg.add_spacer(width=8)
            dpg.add_button(
                label="  Uninstall Selected  ",
                callback=lambda *args: _uninstall_core_selected(args[2]),
                user_data=cat,
            )


def _rebuild_fonts_content(content_tag: str) -> None:
    dpg.delete_item(content_tag, children_only=True)
    sys_items = CORE_CATEGORIES["Fonts"]["items"]
    with dpg.group(parent=content_tag):
        with dpg.tab_bar():

            # ── General Fonts ─────────────────────────────────────────────────
            with dpg.tab(label="  General Fonts  "):
                dpg.add_text("  General Fonts", color=AQUA)
                dpg.add_spacer(height=6)
                cols = 3
                with dpg.child_window(height=-72, border=False):
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                        for _ in range(cols):
                            dpg.add_table_column()
                        rows = [sys_items[i:i+cols] for i in range(0, len(sys_items), cols)]
                        for row in rows:
                            with dpg.table_row():
                                for label, pkgs in row:
                                    tag  = f"core_chk__Fonts__{label}".replace(" ", "_")
                                    inst = _installed_cache.get(pkgs[0])
                                    lbl  = f"  {label}" + ("  ✓" if inst else "")
                                    dpg.add_checkbox(label=lbl, tag=tag, default_value=False)
                                for _ in range(cols - len(row)):
                                    dpg.add_text("")
                dpg.add_spacer(height=8)
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Select All",
                        callback=lambda s, a, u: [
                            dpg.set_value(f"core_chk__Fonts__{lbl}".replace(" ", "_"), True)
                            for lbl, _ in u
                        ],
                        user_data=sys_items,
                    )
                    dpg.add_spacer(width=8)
                    dpg.add_button(
                        label="Clear All",
                        callback=lambda s, a, u: [
                            dpg.set_value(f"core_chk__Fonts__{lbl}".replace(" ", "_"), False)
                            for lbl, _ in u
                        ],
                        user_data=sys_items,
                    )
                    dpg.add_spacer(width=16)
                    dpg.add_button(
                        label="  Install Selected  ",
                        callback=lambda: _install_font_packages([
                            p for lbl, pkgs in sys_items
                            if dpg.does_item_exist(f"core_chk__Fonts__{lbl}".replace(" ", "_"))
                            and dpg.get_value(f"core_chk__Fonts__{lbl}".replace(" ", "_"))
                            for p in pkgs
                        ]),
                    )
                    dpg.add_spacer(width=8)
                    dpg.add_button(
                        label="  Uninstall Selected  ",
                        callback=lambda: _uninstall_core_selected("Fonts"),
                    )

            # ── Nerd Fonts ────────────────────────────────────────────────────
            with dpg.tab(label="  Nerd Fonts  "):
                dpg.add_text("  Nerd Fonts", color=AQUA)
                dpg.add_spacer(height=4)
                dpg.add_text(
                    f"  Downloads from GitHub releases ({NERD_FONTS_VERSION})"
                    f"  →  ~/.local/share/fonts/   (✓ = already installed)",
                    color=DIM,
                )
                dpg.add_spacer(height=6)
                cols = 3
                with dpg.child_window(height=-72, border=False):
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                        for _ in range(cols):
                            dpg.add_table_column()
                        rows = [NERD_FONTS[i:i+cols] for i in range(0, len(NERD_FONTS), cols)]
                        for row in rows:
                            with dpg.table_row():
                                for font in row:
                                    installed = _nerd_font_installed(font)
                                    tag = f"nf_chk__{font}"
                                    lbl = f"  {font}" + ("  ✓" if installed else "")
                                    dpg.add_checkbox(
                                        label=lbl, tag=tag, default_value=False,
                                    )
                                for _ in range(cols - len(row)):
                                    dpg.add_text("")
                dpg.add_spacer(height=8)
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Select All",
                        callback=lambda: [dpg.set_value(f"nf_chk__{f}", True) for f in NERD_FONTS],
                    )
                    dpg.add_spacer(width=8)
                    dpg.add_button(
                        label="Clear All",
                        callback=lambda: [dpg.set_value(f"nf_chk__{f}", False) for f in NERD_FONTS],
                    )
                    dpg.add_spacer(width=16)
                    _b = dpg.add_button(
                        label="  Install Selected  ",
                        callback=lambda: _install_nerd_fonts([
                            f for f in NERD_FONTS
                            if dpg.does_item_exist(f"nf_chk__{f}") and dpg.get_value(f"nf_chk__{f}")
                        ]),
                    )
                    dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
                    dpg.add_spacer(width=8)
                    dpg.add_button(
                        label="  Uninstall Selected  ",
                        callback=lambda: _uninstall_nerd_fonts([
                            f for f in NERD_FONTS
                            if dpg.does_item_exist(f"nf_chk__{f}") and dpg.get_value(f"nf_chk__{f}")
                        ]),
                    )

            # ── Emoji Fonts ───────────────────────────────────────────────────
            with dpg.tab(label="  Emoji Fonts  "):
                _EMOJI_ITEMS = EMOJI_ITEMS
                dpg.add_text("  Emoji Fonts", color=AQUA)
                dpg.add_spacer(height=6)
                cols = 3
                with dpg.child_window(height=-72, border=False):
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                        for _ in range(cols):
                            dpg.add_table_column()
                        rows = [_EMOJI_ITEMS[i:i+cols] for i in range(0, len(_EMOJI_ITEMS), cols)]
                        for row in rows:
                            with dpg.table_row():
                                for label, pkgs in row:
                                    tag  = f"core_chk__Emoji__{label}".replace(" ", "_")
                                    inst = _installed_cache.get(pkgs[0])
                                    lbl  = f"  {label}" + ("  ✓" if inst else "")
                                    dpg.add_checkbox(label=lbl, tag=tag, default_value=False)
                                for _ in range(cols - len(row)):
                                    dpg.add_text("")
                dpg.add_spacer(height=8)
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Select All",
                        callback=lambda s, a, u: [
                            dpg.set_value(f"core_chk__Emoji__{lbl}".replace(" ", "_"), True)
                            for lbl, _ in u
                        ],
                        user_data=_EMOJI_ITEMS,
                    )
                    dpg.add_spacer(width=8)
                    dpg.add_button(
                        label="Clear All",
                        callback=lambda s, a, u: [
                            dpg.set_value(f"core_chk__Emoji__{lbl}".replace(" ", "_"), False)
                            for lbl, _ in u
                        ],
                        user_data=_EMOJI_ITEMS,
                    )
                    dpg.add_spacer(width=16)
                    _b2 = dpg.add_button(
                        label="  Install Selected  ",
                        callback=lambda *args: _install_font_packages(
                            [p for lbl, pkgs in args[2]
                             if dpg.does_item_exist(f"core_chk__Emoji__{lbl}".replace(" ", "_"))
                             and dpg.get_value(f"core_chk__Emoji__{lbl}".replace(" ", "_"))
                             for p in pkgs]
                        ),
                        user_data=_EMOJI_ITEMS,
                    )
                    dpg.bind_item_theme(_b2, INSTALL_BTN_THEME)
                    dpg.add_spacer(width=8)
                    dpg.add_button(
                        label="  Uninstall Selected  ",
                        callback=lambda *args: _uninstall_packages(
                            [p for lbl, pkgs in args[2]
                             if dpg.does_item_exist(f"core_chk__Emoji__{lbl}".replace(" ", "_"))
                             and dpg.get_value(f"core_chk__Emoji__{lbl}".replace(" ", "_"))
                             for p in pkgs]
                        ),
                        user_data=_EMOJI_ITEMS,
                    )


def _dispatch_core_content(cat: str, content_tag: str) -> None:
    data = CORE_CATEGORIES[cat]
    if cat == "Fonts":
        _rebuild_fonts_content(content_tag)
    elif cat == "Audio Drivers":
        _rebuild_audio_content(content_tag)
    elif cat == "Printer Drivers":
        _rebuild_printers_content(content_tag)
    elif cat == "Core Utils":
        _rebuild_cmd_sections_content(_CORE_UTILS_SECTIONS, content_tag)
    elif "_buttons" in data:
        _rebuild_buttons_content(cat, content_tag)
    elif "_sections" in data:
        _rebuild_sectioned_content(cat, content_tag)
    else:
        _rebuild_core_content(cat, content_tag)


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
                        callback=lambda s, a, u: _dispatch_core_content(u[0], u[1]),
                        user_data=(cat, content_tag),
                    )
                    dpg.bind_item_theme(b, btn_theme)
                    dpg.add_spacer(height=2)

            with dpg.child_window(tag=content_tag, border=True):
                pass

        _dispatch_core_content(first_cat, content_tag)


# =============================================================================
# TAB — Search
# =============================================================================
_search_index: list[dict] = []
_search_thread: threading.Thread | None = None


def _detect_aur_helper() -> str | None:
    for helper in ("yay", "paru"):
        if shutil.which(helper):
            return helper
    return None


def _get_real_user_name() -> str | None:
    try:
        import pwd
        for var in ("PKEXEC_UID", "SUDO_UID"):
            val = os.environ.get(var)
            if val and val != "0":
                return pwd.getpwuid(int(val)).pw_name
    except Exception:
        pass
    return None


def _parse_search_output(text: str) -> list[dict]:
    results: list[dict] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line and not line[0].isspace():
            installed = "[installed" in line
            clean = re.sub(r"\s*\[installed[^\]]*\]", "", line)
            clean = re.sub(r"\s*\([^)]+\)", "", clean)
            parts = clean.split(None, 2)
            if len(parts) >= 2 and "/" in parts[0]:
                repo, name = parts[0].split("/", 1)
                version = parts[1].strip()
                desc = lines[i + 1].strip() if i + 1 < len(lines) and lines[i + 1][:1] == " " else ""
                results.append({
                    "repo": repo, "name": name, "version": version,
                    "desc": desc, "installed": installed,
                })
        i += 1
    return results


_search_debounce: threading.Timer | None = None


def _do_search(query: str) -> None:
    helper  = _settings.get("pkg_manager")
    ru      = _get_real_user_name()
    results: list[dict] = []

    try:
        if helper and ru:
            cmd = ["sudo", "-u", ru, helper, "-Ss", "--", query]
        else:
            cmd = ["pacman", "-Ss", "--", query]
        out = subprocess.check_output(cmd, text=True, timeout=30,
                                      stderr=subprocess.DEVNULL)
        results = _parse_search_output(out)
    except subprocess.TimeoutExpired:
        dpg.set_value("search_count", "  Search timed out.")
        return
    except Exception as e:
        dpg.set_value("search_count", f"  Error: {e}")
        return

    src_label = f"AUR helper ({helper})" if helper else "pacman"
    dpg.set_value("search_count", f"  {len(results)} result(s)  —  via {src_label}")

    dpg.lock_mutex()
    try:
        if not dpg.does_item_exist("search_results"):
            return
        dpg.delete_item("search_results", children_only=True)
        with dpg.table(
            parent="search_results",
            header_row=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_outerV=True,
            policy=dpg.mvTable_SizingStretchProp,
        ):
            dpg.add_table_column(label="Package",     init_width_or_weight=0.18)
            dpg.add_table_column(label="Version",     init_width_or_weight=0.10)
            dpg.add_table_column(label="Repo",        init_width_or_weight=0.08)
            dpg.add_table_column(label="Installed",   init_width_or_weight=0.08)
            dpg.add_table_column(label="Description", init_width_or_weight=0.38)
            dpg.add_table_column(label="Install",     init_width_or_weight=0.09)
            dpg.add_table_column(label="Remove",      init_width_or_weight=0.09)

            for r in results[:100]:
                inst_ver = _installed_cache.get(r["name"])
                inst_txt = f"✓ {inst_ver}" if inst_ver else "—"
                inst_col = GREEN if inst_ver else DIM
                repo_col = YELLOW if r["repo"] == "aur" else AQUA
                with dpg.table_row():
                    dpg.add_text(f"  {r['name']}", color=FG)
                    dpg.add_text(f"  {r['version']}", color=DIM)
                    dpg.add_text(f"  {r['repo']}", color=repo_col)
                    dpg.add_text(f"  {inst_txt}", color=inst_col)
                    dpg.add_text(f"  {r['desc']}", color=DIM)
                    _ib = dpg.add_button(
                        label="  Install  ",
                        callback=lambda *args: _install_packages([args[2]]),
                        user_data=r["name"],
                    )
                    dpg.bind_item_theme(_ib, INSTALL_BTN_THEME)
                    dpg.add_button(
                        label="  Remove  ",
                        callback=lambda *args: _uninstall_packages([args[2]]),
                        user_data=r["name"],
                    )
    finally:
        dpg.unlock_mutex()


def _trigger_search() -> None:
    global _search_thread
    if _search_thread and _search_thread.is_alive():
        return
    query = dpg.get_value("search_input").strip()
    if not query:
        return
    dpg.set_value("search_count", "  Searching…")
    _search_thread = threading.Thread(target=_do_search, args=(query,), daemon=True)
    _search_thread.start()


def _search_on_type() -> None:
    global _search_debounce
    if _search_debounce and _search_debounce.is_alive():
        _search_debounce.cancel()
    _search_debounce = threading.Timer(0.6, _trigger_search)
    _search_debounce.start()


def _build_search_tab() -> None:
    helper = _settings.get("pkg_manager")
    hint   = f"Search via {helper}  (pacman + AUR)…" if helper else "Search via pacman…"
    with dpg.tab(label="   Search   "):
        dpg.add_spacer(height=8)
        dpg.add_text("  Package Search", color=AQUA)
        dpg.add_separator()
        dpg.add_spacer(height=6)
        if helper:
            dpg.add_text(f"  AUR helper: {helper}   (searches all pacman repos + AUR)", color=DIM)
        else:
            dpg.add_text("  No AUR helper found — searching pacman repos only", color=YELLOW)
        dpg.add_spacer(height=8)
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="search_input",
                hint=hint,
                width=-80,
                callback=_search_on_type,
            )
            dpg.add_spacer(width=4)
            _b = dpg.add_button(label="  Search  ", callback=_trigger_search)
            dpg.bind_item_theme(_b, INSTALL_BTN_THEME)
        dpg.add_spacer(height=4)
        dpg.add_text("", tag="search_count", color=DIM)
        dpg.add_spacer(height=4)
        with dpg.child_window(tag="search_results", border=False):
            pass


# =============================================================================
# TAB 4 — System Maintenance
# =============================================================================
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
                    callback=lambda s, a, u: _launch_in_terminal(u["cmd"]),
                    user_data=action,
                )
                dpg.add_spacer(width=12)
                dpg.add_text(action["desc"], color=DIM)
            dpg.add_spacer(height=6)

        # ── pacman.conf configuration ─────────────────────────────────────────
        dpg.add_spacer(height=8)
        dpg.add_separator()
        dpg.add_spacer(height=8)
        dpg.add_text("  pacman.conf configuration", color=AQUA)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        # Parallel Downloads
        with dpg.group(horizontal=True):
            dpg.add_text("  Set Parallel Downloads", color=FG)
            dpg.add_spacer(width=6)
            dpg.add_text(f"(currently: {_get_parallel_downloads()})", tag="pd_current", color=DIM)
            dpg.add_spacer(width=12)
            dpg.add_input_text(tag="pd_input", hint="1 – 14", width=90)
            dpg.add_spacer(width=8)
            dpg.add_button(label="  Apply  ", callback=_apply_parallel_downloads)
            dpg.add_spacer(width=4)
            dpg.add_button(
                label="Cancel",
                callback=lambda: (
                    dpg.set_value("pd_input", ""),
                    dpg.set_value("pd_status", ""),
                ),
            )
        dpg.add_text("", tag="pd_status", color=GREEN)
        dpg.add_spacer(height=10)

        # Boolean options
        _BOOL_OPTIONS = [
            ("Color",                  "Colored pacman output"),
            ("ILoveCandy",             "Replaces progress bar with Pac-Man"),
            ("CheckSpace",             "Check available disk space before installing"),
            ("DisableDownloadTimeout", "Disable download timeout for slow mirrors"),
            ("VerbosePkgLists",        "Show old/new package versions on upgrades"),
        ]
        for opt, desc in _BOOL_OPTIONS:
            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    label=f"  {opt}",
                    tag=f"opt_{opt}",
                    default_value=_is_option_enabled(opt),
                    callback=lambda s, a, u: _toggle_pacman_option(u, a),
                    user_data=opt,
                )
                dpg.add_spacer(width=12)
                dpg.add_text(desc, color=DIM)
            dpg.add_spacer(height=4)


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
    _install_policy_if_needed()
    _ensure_root()

    _refresh_installed_cache()
    if "pkg_manager" not in _settings:
        detected = _detect_aur_helper()
        _settings["pkg_manager"] = detected if detected else "pacman"
        _save_settings(_settings)

    pw_active = bool(_installed_cache.get("pipewire"))
    pa_active = bool(_installed_cache.get("pulseaudio"))
    audio_sections = []
    if pw_active or not pa_active:
        audio_sections.append({"title": "PipeWire", "pkgs": _PIPEWIRE_PKGS})
    if pa_active or not pw_active:
        audio_sections.append({"title": "PulseAudio", "pkgs": _PULSEAUDIO_PKGS})

    all_cmd_sections = _CORE_UTILS_SECTIONS + _PRINTER_SECTIONS + audio_sections
    _write_missing_report(all_cmd_sections)

    dpg.create_context()
    _create_install_btn_theme()
    _apply_theme()
    _try_load_font()

    with dpg.texture_registry():
        _logo_path = BASE_DIR / "logo.png"
        if _logo_path.exists():
            try:
                _lw, _lh, _, _ld = dpg.load_image(str(_logo_path))
                dpg.add_static_texture(_lw, _lh, _ld, tag="logo_tex")
            except Exception:
                pass

    with dpg.window(tag="primary", no_title_bar=True, no_move=True,
                    no_resize=False, no_scrollbar=True):
        dpg.add_text("  Arch-Boki — Post Install", color=AQUA)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        with dpg.tab_bar():
            _build_welcome_tab()
            _build_maintenance_tab()
            _build_core_tab()
            _build_apps_tab()
            _build_search_tab()

    _search_index.extend(_build_search_index())

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
