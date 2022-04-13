#   ___  _   _ _         ____             __ _                    _    _              _                       
#  / _ \| |_(_) | ___   / ___|___  _ __  / _(_) __ _             / \  | | _____  __  | | __ ___   _____  _ __ 
# | | | | __| | |/ _ \ | |   / _ \| '_ \| |_| |/ _` |  _____    / _ \ | |/ _ \ \/ /  | |/ _` \ \ / / _ \| '__|
# | |_| | |_| | |  __/ | |__| (_) | | | |  _| | (_| | |_____|  / ___ \| |  __/>  < |_| | (_| |\ V / (_) | |   
#  \__\_\\__|_|_|\___|  \____\___/|_| |_|_| |_|\__, |         /_/   \_\_|\___/_/\_\___/ \__,_| \_/ \___/|_|   
#                                              |___/                                                          

# IMPORTANT: Create simbolic links for the "set_brightness_config" and "set_volume_config":
# ln -s ~/.config/qtile/set_volume_config /usr/bin/volume
# ln -s ~/.config/qtile/set_brightness_config /usr/bin/brightness

# ************** Log path *************** #
# /home/$USER/.local/share/qtile/qtile.log

# ************** default_config path *************** #
# /usr/lib/python3/dist-packages/libqtile/resources/default_config.py

# ************** Arch default libqtile path ******** #
# /usr/lib/python3.9/site-packages/libqtile/


# _______________________________________________________________________________________
#|                                                                                       |        
#|                                       IMPORTS                                         |
#|_______________________________________________________________________________________|

import os
import subprocess
import requests
import platform
import time
import socket
from urllib.request import urlopen
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger


# _______________________________________________________________________________________
#|                                                                                       |        
#|                              STARTUP HOOK (AUTOSTART)                                 |
#|_______________________________________________________________________________________|

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


# _______________________________________________________________________________________
#|                                                                                       |        
#|                                  GLOBAL VARIABLES                                     |
#|_______________________________________________________________________________________|

alt = "mod1"
mod = "mod4"

my_terminal = "terminator"
my_browser = "firefox"
my_mailclient = "thunderbird" 

headphones_macaddress = "60:AB:D2:76:99:38"

network_interface="wlp5s0"

# TODO : Change to main and then left and reigt screen. Include configuration of the size here
main_screen = 'LVDS-1'
hdmi_screen = 'HDMI-1'
displayport_screen = 'VGA-1'

ticker_refreshrate = 30 #Crypto ticker refresh rate in seconds

max_percentage_volume = '100' # Maximum Percentage: 150%

group_numbers_fr = ['ampersand', 'eacute', 'quotedbl', 'apostrophe', 'parenleft', 'minus', 'egrave', 'underscore', 'ccedilla']
group_numbers_es = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
group_numbers_kp = ['KP_End', 'KP_Down', 'KP_Next', 'KP_Left','KP_Begin', 'KP_Right', 'KP_Home', 'KP_Up', 'KP_Prior']
group_numbers_current = group_numbers_fr

colors = {
    "black_grey" : "#282A36",   # panel_bg
    "dark_grey"  : "#434758",   # current_screen_tab_bg
    "white"      : "#ffffff",   # group_names
    "light_red"  : "#ff5555",   # layout_widget_bg
    "black"      : "#000000",   # other_screen_tabs_bg
    "purple"     : "#A77AC4",   # other_screen_tabs
    "french_blue": "#0055a4",
    "french_red" : "#ef4135",
    "green"      : "#00ff00"
}

sound_card_index_PC        = 'TBD'
sound_card_index_HDMI      = 'TBD'
sound_card_index_BLUETOOTH = 'TBD'
sound_card_order_PC        = 'TBD'
sound_card_order_HDMI      = 'TBD'
sound_card_order_BLUETOOTH = 'TBD'


# _______________________________________________________________________________________
#|                                                                                       |
#|                                    SITE FUNCTIONS                                     |
#|_______________________________________________________________________________________|

# -----------------------------------------------------------
# -- VPN AND INTERNET CHECKERS 
# -----------------------------------------------------------
def internet_on(url):
    try:
        response = urlopen(url, timeout=10)
        return True
    except: 
        return False

def get_current_country():
    internet = internet_on('https://archlinux.org/')
    if(internet):
        public_ip = subprocess.getoutput("dig +short myip.opendns.com @resolver1.opendns.com")
        country = subprocess.getoutput("whois " + public_ip + " | awk ' /[Cc]ountry/{print $2}'")
        return country.upper()
    else:
        return "N/A"

def print_internet_status():
    internet = internet_on('https://archlinux.org/')
    if (internet):
        return '<span foreground="' + colors["green"] + '">直</span>'
    else:
        return '<span foreground="' + colors["french_red"] + '">睊</span>'

def check_vpn_status():
    internet = internet_on('https://archlinux.org/')
    openvpn_pid = subprocess.getoutput("ps aux | grep openvpn | grep root | awk '{print $2}'")
    #logger.warning("OpenVPN_PID: " + openvpn_pid)
    if (not internet or openvpn_pid == ""):
        return '<span foreground="' + colors["french_red"] + '">嬨</span>'
    else: 
        return '<span foreground="' + colors["green"] + '">嬨</span>'

# -----------------------------------------------------------
# -- CRYPTOCURRENCY TICKERS 
# -----------------------------------------------------------
def crypto_ticker(unit):
    internet = internet_on('https://archlinux.org/')
    if(internet):
        price = requests.get("https://eur.rate.sx/1"+unit).content.decode("utf-8").split(".")
        #price = subprocess.getoutput("curl -s eur.rate.sx/1" + unit)
        price_shown = price[0] + "." + price[1][:2] + "€"
        return price_shown
    else:
        return "N/A"

def xmr_ticker(): return crypto_ticker("xmr") 
def btc_ticker(): return crypto_ticker("btc") 
def hnt_ticker(): return crypto_ticker("hnt") 

# -----------------------------------------------------------
# -- CURRENT KEYBOARD LAYOUT 
# -----------------------------------------------------------
def get_kb_layout():
    kb_layout = subprocess.getoutput("setxkbmap -query | grep layout | awk '{print $2}'")
    return kb_layout.upper()

# -----------------------------------------------------------
# -- VOLUME AND SINK MANAGEMENT 
# -----------------------------------------------------------
def get_all_volume_sinks():
    global sound_card_index_PC
    global sound_card_index_HDMI
    global sound_card_index_BLUETOOTH
    global sound_card_order_PC 
    global sound_card_order_HDMI
    global sound_card_order_BLUETOOTH 
    
    all_sink_indexes = subprocess.getoutput("pacmd list-sinks | grep 'index' | cut -f 2 -d ':' | cut -f 2 -d ' '").split('\n')
    # all_sink_indexes output example:
    # 1
    # 2
    # 6
    
    all_sink = subprocess.getoutput("pacmd list-sinks | grep 'name: <' | cut -f 2 -d ':'").split('\n')
    # all_sink output example:
    # <alsa_output.pci-0000_00_1b.0.analog-stereo>
    # <alsa_output.pci-0000_00_03.0.hdmi-stereo>
    # <bluez_sink.60_AB_D2_76_99_38.a2dp_sink>

    if(len(all_sink) != len(all_sink_indexes)):
        logger.warning("ERROR: Check get_all_volume_sinks() - Arrays all_sink and all_sink_indexes have a different size")
        return None
    else:
        for index,sink in enumerate(all_sink):
            if "analog-stereo" in sink:
                #logger.warning("analog-stereo - index PC: " + all_sink_indexes[index] + " / order PC: " + str(index))
                sound_card_index_PC = all_sink_indexes[index]
                sound_card_order_PC = index
            elif "hdmi-stereo" in sink:
                #logger.warning("hdmi-stereo - index HDMI: " + all_sink_indexes[index] + " / order HDMI: " + str(index))
                sound_card_index_HDMI = all_sink_indexes[index]
                sound_card_order_HDMI = index
            elif "bluez_sink" in sink:
                #logger.warning("bluez_sink - index BLUETOOTH: " + all_sink_indexes[index] + " / order BLUETOOTH: " + str(index))
                sound_card_index_BLUETOOTH = all_sink_indexes[index]
                sound_card_order_BLUETOOTH = index
            else:
                logger.warning("ERROR: Check get_all_volume_sinks() - Values: \n - sink: " + sink + "\n - order_index: " + str(index) + "\n - sink_index: " + all_sink_indexes[index])

def get_current_volume(sink_order):
    if(sink_order == 'TBD'):
        return "N/A"
    else:
        volume = subprocess.getoutput("pacmd list-sinks | grep volume:\ front | awk '{i++} i==" + str(sink_order + 1) + "{print $5+0}'")
        muted  = subprocess.getoutput("pacmd list-sinks | grep muted | awk '{i++} i==" + str(sink_order + 1) + "{print $2}'")
        if(volume == ""):
            return "N/A"
        else:
            if(muted == "yes"):
                # return "M"
                return "M" # nf-mdi-volume_mute
            else:
                return volume + "%"
    
def get_current_volume_PC():
    get_all_volume_sinks()
    return get_current_volume(sound_card_order_PC)
def get_current_volume_HDMI():
    get_all_volume_sinks()
    return get_current_volume(sound_card_order_HDMI)
def get_current_volume_BLUETOOTH():
    get_all_volume_sinks()
    #return get_current_volume(sound_card_order_BLUETOOTH)
    blutooth_volume = get_current_volume(sound_card_order_BLUETOOTH)
    if(blutooth_volume == "N/A"):
        return "ﳌ" # Nerd fonts: nf-mdi-headphones_off
    else:
        return "" # Nerd fonts: nf-mdi-headphones

get_all_volume_sinks()

# _______________________________________________________________________________________
#|                                                                                       |
#|                                       KEY BINDINGS                                    |
#|_______________________________________________________________________________________|
keys = [
    # Main key bindings
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(my_terminal)),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # MonadTall recommaded key bindings
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()), 

    # Select screen focus
    Key([mod, alt], group_numbers_current[0], lazy.to_screen(0)),
    Key([mod, alt], group_numbers_current[1], lazy.to_screen(1)),
    Key([mod, alt], group_numbers_current[2], lazy.to_screen(2)),
    
    Key([mod, alt], group_numbers_kp[0], lazy.to_screen(0)),
    Key([mod, alt], group_numbers_kp[1], lazy.to_screen(1)),
    Key([mod, alt], group_numbers_kp[2], lazy.to_screen(2)),

    # Shift keyboard layout
    Key(["shift", alt], "e", lazy.spawn("setxkbmap es")),
    Key(["shift", alt], "f", lazy.spawn("setxkbmap fr")),


    # Open VPN activation / deactivation 
    # Create or add sudoers.d/custom_sudoers and add some exceptions:
    # $ sudo visudo -f /etc/sudoers.d/custom_sudoers
    # ALL ALL=NOPASSWD: /bin/systemctl start vpnd_bordeaux.service
    # ALL ALL=NOPASSWD: /bin/systemctl stop vpnd_bordeaux.service
    # ALL ALL=NOPASSWD: /usr/bin/pkill openvpn

    Key([mod], "v", lazy.spawn("sudo systemctl start vpnd_bordeaux.service")),
    Key([mod, "control"], "v", lazy.spawn("sudo pkill openvpn")),

    # Open Firefox
    Key([mod], "f", lazy.spawn(my_browser)),
    # Open Tor Browser
    Key([mod], "t", lazy.spawn("torbrowser-launcher")), 
    # Open Mail Client Thunderbird
    Key([mod, "control"], "m", lazy.spawn(my_mailclient)),
    # Open VirtualBox 
    #Key([mod], "v", lazy.spawn("virtualbox")),
    # Open Pavucontrol
    Key([mod], "p", lazy.spawn("pavucontrol")),
    # Open Session
    Key([mod], "s", lazy.spawn("./SourceCode/Session/session-desktop-linux-x86_64-1.4.4.AppImage")),
    # Open config
    Key([mod], "c", lazy.spawn("codium .config/qtile/config.py")),
    # Open Bitwarden
    Key([mod], "b", lazy.spawn("./SourceCode/Bitwarden.AppImage")),

    # Enable / Disable bluetooth headphones
    Key([mod], "h", lazy.spawn("bluetoothctl connect " + headphones_macaddress)),
    Key([mod, "control"], "h", lazy.spawn("bluetoothctl power on")),
    Key([mod, alt], "h", lazy.spawn("bluetoothctl power off")),

    # Reload Multiple Screens (2 Screens - Main + Left)
    Key([mod], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1920x1080  --left-of " + main_screen)),   
    # Reload Multiple Screens (2 Screens - Main + Right)
    Key([mod, "shift"], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1600x900  --right-of " + main_screen)),
    # Reload Multiple Screens (3 Screens)
    Key([mod, "control"], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1920x1080  --left-of " + main_screen + " --output " + displayport_screen + " --mode 1600x900 --right-of " + main_screen)),

    # Output volume control PC
    Key([], 'XF86AudioLowerVolume', lazy.spawn("pactl set-sink-volume " + sound_card_index_PC + " -5%")),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("pactl set-sink-volume " + sound_card_index_PC + " +5%")),
    Key([], 'XF86AudioMute', lazy.spawn("pactl set-sink-mute " + sound_card_index_PC + " toggle")),
    # Output volume control HDMI
    Key(["control"], 'XF86AudioLowerVolume', lazy.spawn("pactl set-sink-volume " + sound_card_index_HDMI + " -5%")),
    Key(["control"], 'XF86AudioRaiseVolume', lazy.spawn("pactl set-sink-volume " + sound_card_index_HDMI+ " +5%")),
    Key(["control"], 'XF86AudioMute', lazy.spawn("pactl set-sink-mute " + sound_card_index_HDMI + " toggle")), 

    # Brightness and state control Main Screen (PC)
    Key([], 'XF86MonBrightnessUp', lazy.spawn("brightness " + main_screen + " + 50 ")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("brightness " + main_screen + " - 50 ")),
    # Brightness and state control HDMI Screen (TV)
    Key(["control"], 'XF86MonBrightnessUp', lazy.spawn("brightness " + hdmi_screen + " + 50 ")),
    Key(["control"], 'XF86MonBrightnessDown', lazy.spawn("brightness " + hdmi_screen + " - 50 ")),
    # Brightness and state control Mini Display Port Screen (Screen2)
    Key(["shift"], 'XF86MonBrightnessUp', lazy.spawn("brightness " + displayport_screen + " + 50 ")),
    Key(["shift"], 'XF86MonBrightnessDown', lazy.spawn("brightness " + displayport_screen + " - 50 ")),

    # Move to previous group
    Key(["control", alt], "Left", lazy.screen.prev_group()),
    Key(["control", alt], "Right", lazy.screen.next_group()),
]

# _______________________________________________________________________________________
#|                                                                                       |
#|                                       WORKSPACES                                      |
#|_______________________________________________________________________________________|
group_names = [("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'max'}),
               ("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'monadtall'}),
               ("",  {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 0):
    keypad_indx = group_numbers_kp[i]
    key_indx = group_numbers_current[i]
    keys.append(Key([mod], keypad_indx, lazy.group[name].toscreen()))
    keys.append(Key([mod, 'shift'], keypad_indx, lazy.window.togroup(name)))
    keys.append(Key([mod], key_indx, lazy.group[name].toscreen()))
    keys.append(Key([mod, 'shift'], key_indx, lazy.window.togroup(name)))
        
# _______________________________________________________________________________________
#|                                                                                       |
#|                                        LAYOUTS                                        |
#|_______________________________________________________________________________________|
layout_theme = {
    "border_width": 2,
    "margin": 20,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}

layouts = [
    layout.MonadTall(**layout_theme, ratio=0.6),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme)
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# _______________________________________________________________________________________
#|                                                                                       |
#|                                  BAR CONFIGURATION                                    |
#|_______________________________________________________________________________________|

widget_defaults = dict(
    font='Fira Code Nerd Font',
    #font='Caskaydia Cove Nerd Font',
    #font='Ubuntu Bold',
    fontsize=12,
    padding=7,
    background = colors["black_grey"] 
)

def init_widgets_list():
    widgets_list = [
        # -----------------------------------------------------------
        # -- LOGO IMAGE (TROPTIMUM) 
        # -----------------------------------------------------------
        widget.Image(
            filename = "~/.config/qtile/icons/trioptimum-logo.png",
            margin = 2,
            margin_x = 5
        ),
        widget.Sep(
            linewidth = 0,
            padding = 5,
            foreground = colors["white"],
            background = colors["black_grey"]
        ),
        # -----------------------------------------------------------
        # -- WORKSPACES 
        # -----------------------------------------------------------
        widget.GroupBox(
            fontsize = 28,
            font="FontAwesome",
            margin_x = 0,
            margin_y = 3,
            center_aligned = True,
            padding_x = 12,
            padding_y = 5,
            borderwidth = 2,
            inactive = colors["white"],
            highlight_method = "block",
            rounded = False,
            active = colors["white"],
            this_current_screen_border = colors["purple"],
            this_screen_border = colors["dark_grey"],
            other_current_screen_border = colors["black_grey"],
            other_screen_border = colors["black_grey"],
            foreground = colors["white"],
            background = colors["black_grey"]
        ),

        # -----------------------------------------------------------
        # -- PROMPT AND CURRENT WINDOW NAME 
        # -----------------------------------------------------------
        widget.Prompt(
            prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname()),
            padding = 10,
            foreground = colors["light_red"],
            background = colors["dark_grey"]
        ),
        widget.WindowName(
            foreground = colors["purple"]
        ),
        
        # -----------------------------------------------------------
        # -- SYSTEM MONITORING (VPN & NETWORK, HARD DRIVE, CPU & RAM) 
        # -----------------------------------------------------------
        widget.GenPollText(
            func=print_internet_status,
            update_interval=0.5,
            fontsize=17,
            padding=10
            #foreground = "#fc6a03"
        ),
        widget.GenPollText(
            func=check_vpn_status,
            update_interval=0.5,
            fontsize=17
            #foreground = "#fc6a03"
        ),
       # widget.GenPollText(
       #     func=get_current_country,
       #     update_interval=0.5
       #     #foreground = "#fc6a03"
       # ),
        #widget.Image(
        #    filename = "~/.config/qtile/icons/rj45.png",
        #    margin = 4,
        #    margin_x = 5
        #),
        #widget.Net(
        #    interface = network_interface,
        #    format = '{down} ▼▲ {up}' # format = '{interface}: {down} ▼▲ {up}'
        #),
        widget.Sep(linewidth = 1, padding = 20, foreground = colors["white"], background = colors["black_grey"]),
        #widget.Image(
        #    filename = "~/.config/qtile/icons/processor.png",
        #    margin = 5,
        #    margin_x = 5
        #),
        #widget.CPU(
        #    format = '{load_percent}%'
        #),
        #widget.Sep(linewidth = 0, padding = 3),
        #widget.Image(
        #    filename = "~/.config/qtile/icons/ram.png",
        #    margin = 3,
        #    margin_x = 5
        #),
        #widget.Memory(
        #        foreground = colors["white"],
        #        background = colors["black_grey"],
        #        padding = 5,
        #        format = '{MemPercent}%'
        #),
        widget.Sep(linewidth = 0, padding = 3),
        widget.Image(
            filename = "~/.config/qtile/icons/floppy-disk.png",
            margin = 8,
            margin_x = 5
        ),
        widget.DF(
                foreground = colors["white"],
                background = colors["black_grey"],
                padding = 5,
                partition = '/',
                format = '{uf}Gb ({r:.0f}%)',
                visible_on_warn = False,
                warn_space = 10
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        # -----------------------------------------------------------
        # -- CRYPTO TICKERS
        # -----------------------------------------------------------
        
        # Bitcoin ticker
        # widget.Image(
        #     filename = "~/.config/qtile/icons/bitcoin.png",
        #     margin = 7,
        #     margin_x = 5
        # ),
        #widget.GenPollText(
        #    func=btc_ticker,
        #    update_interval=30,
        #    foreground = "#f7931a"
        #),
        
        # Monero ticker
        widget.Image(
            filename = "~/.config/qtile/icons/monero.png",
            margin = 7,
            margin_x = 5
        ),
        widget.GenPollText(
            func=xmr_ticker,
            update_interval=ticker_refreshrate,
            foreground = "#fc6a03"
        ),
        # Helium ticker
        widget.Image(
            filename = "~/.config/qtile/icons/helium.png",
            margin = 6,
            margin_x = 5
        ),
        widget.GenPollText(
            func=hnt_ticker,
            update_interval=ticker_refreshrate,
            foreground = "#38a2ff"
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        # -----------------------------------------------------------
        # -- BATTERY
        # -----------------------------------------------------------
        widget.Image(
            filename = "~/.config/qtile/icons/battery.png",
            margin = 6,
            margin_x = 5
        ),
        widget.Battery(
            format = '{percent:2.0%}'
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        

        # -----------------------------------------------------------
        # -- VOLUME 
        # -----------------------------------------------------------
        
        # Volume PC      
        widget.Image(
            filename = "~/.config/qtile/icons/volume.png",
            margin = 7,
            margin_x = 5
        ),
        widget.GenPollText(
            func=get_current_volume_PC,
            update_interval=0.1,
            #fontsize=13
        ), 
        widget.Sep(padding = 5, linewidth=0),
        
        # Volume HDMI
        widget.Image(
            filename = "~/.config/qtile/icons/volume.png",
            margin = 7,
            margin_x = 5
        ),
        widget.GenPollText(
            func=get_current_volume_HDMI,
            update_interval=0.1,
            #fontsize=13
        ),
        widget.Sep(padding = 5, linewidth=0),

        # Bluetooth headphones state
        widget.GenPollText(
            func=get_current_volume_BLUETOOTH,
            update_interval=0.1,
            fontsize=19
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        

        # -----------------------------------------------------------
        # -- KEYBOARD LAYOUT
        # -----------------------------------------------------------
        
        # widget.Image(
        #     filename = "~/.config/qtile/icons/keyboard.png",
        #     margin = 7,
        #     margin_x = 5
        # ), 
        widget.GenPollText(
            func=get_kb_layout,
            update_interval=0.5,
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),


        # -----------------------------------------------------------
        # -- DATE AND TIME  
        # -----------------------------------------------------------
        #widget.Clock(format=' %a, %d %b. %Y - %H:%M:%S'), # %S for adding seconds
        widget.Clock(format='%d/%m/%Y - %H:%M:%S'), # %S for adding seconds
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        # -----------------------------------------------------------
        # -- CURRENT LAYOUT 
        # -----------------------------------------------------------
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            background = colors["black_grey"],
            padding = 0,
            scale = 0.5
        ),
    ]
    return widgets_list


# _______________________________________________________________________________________
#|                                                                                       |
#|                                  SCREEN CONFIGURATIONS                                |
#|_______________________________________________________________________________________|

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list() # Slicing removes unwanted widgets on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    widgets_screen2[0] = widget.Image(
            filename = "~/.config/qtile/icons/trioptimum-logo-blue.png",
            margin = 2,
            margin_x = 5
    )
    #widgets_screen2[5] = widget.TextBox(background = colors["french_blue"], foreground = colors["white"], text = "HDMI-Left", name="default")
    return widgets_screen2

def init_widgets_screen3():
    widgets_screen3 = init_widgets_list()
    widgets_screen3[0] = widget.Image(
            filename = "~/.config/qtile/icons/trioptimum-logo-red.png",
            margin = 2,
            margin_x = 5
    )
    #widgets_screen3[5] = widget.TextBox(background = colors["french_red"], foreground = colors["white"], text = "DP-Right", name="default")
    return widgets_screen3            

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen3(), opacity=1.0, size=30))]

# _______________________________________________________________________________________
#|                                                                                       |
#|                                     OTHER OPTIONS                                     |
#|_______________________________________________________________________________________|
dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# floating_layout = layout.Floating(float_rules=[
#     {'wmclass': 'confirm'},
#     {'wmclass': 'dialog'},
#     {'wmclass': 'download'},
#     {'wmclass': 'error'},
#     {'wmclass': 'file_progress'},
#     {'wmclass': 'notification'},
#     {'wmclass': 'splash'},
#     {'wmclass': 'toolbar'},
#     {'wmclass': 'confirmreset'},  # gitk
#     {'wmclass': 'makebranch'},  # gitk
#     {'wmclass': 'maketag'},  # gitk
#     {'wname': 'branchdialog'},  # gitk
#     {'wname': 'pinentry'},  # GPG key password entry
#     {'wmclass': 'ssh-askpass'},  # ssh-askpass
#     {"wmclass": "obs"},
#     {"wmclass": "notify"},
# ])

auto_fullscreen = True
focus_on_window_activation = "smart"
extentions = []

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


# _______________________________________________________________________________________
#|                                                                                       |
#|                                          MAIN                                         |
#|_______________________________________________________________________________________|
if __name__ in ["config", "__main__"]:
    screens = init_screens()
