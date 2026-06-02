# =============================================================================
# actions.py — package sets, terminal list, and maintenance bash commands
# All commands run as root (pkexec at launch) — no sudo prefix needed
# =============================================================================

AUR_PKGS = {
    "affine-bin", "g4music-git", "wezterm-nightly-bin", "stacer-bin",
    "simplescreenrecorder-qt6-git", "qimgv-git", "upscayl-desktop-git",
    "upscayl-models-desktop", "waypaper-git", "walker-bin",
    "visual-studio-code-bin", "brave-bin", "google-chrome",
    "librewolf", "firefox-esr",
    "ttf-twemoji", "ttf-joypixels", "ttf-blobmoji",
    "peazip",
}

TERMINALS = ["alacritty", "ghostty", "kitty", "wezterm", "xfce4-terminal", "xterm"]

_REFLECTOR_COUNTRIES = (
    "AT,BE,BG,HR,CZ,DK,EE,FI,FR,DE,GR,HU,IT,MD,NL,MK,NO,PL,PT,RO,RS,SK,SI,ES,SE,CH,UA,GB"
)

# Real user for AUR helpers (yay/paru must not run as root)
_REAL_USER = (
    "_ru=${SUDO_USER:-$(getent passwd \"${PKEXEC_UID}\" | cut -d: -f1 2>/dev/null)}"
)

MAINTENANCE_ACTIONS = [
    {
        "label": "Refresh Mirrors (reflector)",
        "desc":  "Update mirrorlist with fastest mirrors via reflector",
        "cmd": (
            f"reflector --country {_REFLECTOR_COUNTRIES} "
            "--age 6 --fastest 20 --protocol https --sort rate "
            "--save /etc/pacman.d/mirrorlist --verbose"
        ),
    },
    {
        "label": "Refresh Pacman DB",
        "desc":  "Force-sync all pacman databases (pacman -Syyv)",
        "cmd":   "pacman -Syyv",
    },
    {
        "label": "Update System",
        "desc":  "Full system update via pacman -Syyu",
        "cmd":   "pacman -Syyu --noconfirm",
    },
    {
        "label": "Add Arch-Boki Repos",
        "desc":  "Append arch-boki repository to pacman.conf",
        "cmd": (
            "grep -q 'shtrkce-repo' /etc/pacman.conf"
            " && echo 'Arch-Boki repos already present'"
            " || { printf '\\n[shtrkce-repo]\\nSigLevel = Optional TrustAll"
            "\\nServer = https://bojanstrkovski-21.github.io/$repo/$arch"
            "\\n\\n[shtrkce_repo_xl]\\nSigLevel = Optional TrustAll"
            "\\nServer = https://gitlab.com/bojanstrkovski-21/$repo/-/raw/main/$arch\\n'"
            " >> /etc/pacman.conf && pacman -Syy; }"
        ),
    },
    {
        "label": "Add Nemesis Repos",
        "desc":  "Add Nemesis / Erik Dubois repository",
        "cmd": (
            "grep -q 'nemesis_repo' /etc/pacman.conf"
            " && echo 'Nemesis repo already present'"
            " || { printf '\\n[nemesis_repo]\\nSigLevel = Never"
            "\\nServer = https://erikdubois.github.io/$repo/$arch\\n'"
            " >> /etc/pacman.conf && pacman -Syy; }"
        ),
    },
    {
        "label": "Add Chaotic-AUR Repos",
        "desc":  "Install and append Chaotic-AUR keyring and repository",
        "cmd": (
            "pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com"
            " && pacman-key --lsign-key 3056513887B78AEB"
            " && pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'"
            " && pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'"
            " && { grep -q 'chaotic-aur' /etc/pacman.conf"
            "   || printf '\\n[chaotic-aur]\\nInclude = /etc/pacman.d/chaotic-mirrorlist\\n'"
            "   >> /etc/pacman.conf; }"
            " && pacman -Syy"
        ),
    },
    {
        "label": "Fix Pacman DB & Keys",
        "desc":  "Reset pacman databases, keyrings and trust",
        "cmd": (
            "pacman -Sy archlinux-keyring --noconfirm"
            " && rm -f /var/lib/pacman/sync/*"
            " && rm -rf /etc/pacman.d/gnupg/*"
            " && pacman-key --init"
            " && pacman-key --populate"
            " && printf '\\nkeyserver hkp://keyserver.ubuntu.com:80\\n'"
            " >> /etc/pacman.d/gnupg/gpg.conf"
            " && pacman -Sy"
        ),
    },
    {
        "label": "Remove Pacman Lock",
        "desc":  "Remove /var/lib/pacman/db.lck if present",
        "cmd": (
            "if [ -f /var/lib/pacman/db.lck ];"
            " then rm -f /var/lib/pacman/db.lck && echo 'db.lck removed — pacman is now unlocked';"
            " else echo 'db.lck not found — pacman is not locked'; fi"
        ),
    },
    {
        "label": "Clear Package Cache",
        "desc":  "Run pacman -Scc and optionally yay/paru -Scc",
        "cmd": (
            f"{_REAL_USER};"
            " pacman -Scc;"
            " read -rp 'Run yay -Scc? [y/N]: ' _a1;"
            " [[ \"$_a1\" =~ ^[Yy]$ ]] && command -v yay &>/dev/null"
            " && sudo -u \"$_ru\" yay -Scc;"
            " read -rp 'Run paru -Scc? [y/N]: ' _a2;"
            " [[ \"$_a2\" =~ ^[Yy]$ ]] && command -v paru &>/dev/null"
            " && sudo -u \"$_ru\" paru -Scc;"
            " true"
        ),
    },
    {
        "label": "Install Archlinux-Tweak-Tool",
        "desc":  "Requires Erik Dubois nemesis-repo to be added first",
        "cmd":   "pacman -Syy --needed --noconfirm archlinux-tweak-tool-git arcolinux-app-glade-git sofirem-git",
    },
]
