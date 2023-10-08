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
from dotenv import load_dotenv

from widget.custom_groupbox             import CustomGroupBox
from widget.custom_textbox              import CustomTextBox
from widget.custom_image                import CustomImage
from qtile_extras                       import widget
from qtile_extras.widget                import modify
from qtile_extras.widget.decorations    import RectDecoration, PowerLineDecoration
from libqtile.bar 						import Bar, CALCULATED

# _______________________________________________________________________________________
#|                                                                                       |        
#|                                        DEBUG                                          |
#|_______________________________________________________________________________________|
# Log prefix, to spot more easily log generated by this config
LOG_PREFIX = "[CONFIG LOG]"
def log(msg):
	logger.warning(LOG_PREFIX + " " + msg)

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

# Environemental variables
load_dotenv()

alt = os.getenv("ALT")
mod = os.getenv("MOD")

my_terminal = os.getenv("TERMINAL")
my_browser = os.getenv("BROWSER")
my_mailclient = os.getenv("MAIL_CLIENT") 

headphones_macaddress = os.getenv("HP_MAC_ADDR")

default_network_interface = os.getenv("WIFI_NET_INT")

right_screen = os.getenv("RIGHT_SCREEN_NAME") 
right_screen_res = os.getenv("RIGHT_SCREEN_RES") 
left_screen  = os.getenv("LEFT_SCREEN_NAME")
left_screen_res  = os.getenv("LEFT_SCREEN_RES")

mobo_sound_sink_name = os.getenv("MOBO_SOUND_SINK_NAME")
bluetooth_sound_sink_name = os.getenv("BLUETOOTH_SOUND_SINK_NAME")

ticker_refreshrate = int(os.getenv("TICKER_REFRESH_RATE"))

max_percentage_volume = os.getenv("MAX_VOLUME") 

active_crypto_tickers = os.getenv("CRYPTO_TICKERS")
active_battery_percentage = os.getenv("BATTERY_PERCENTAGE")

# Constants
group_numbers_fr = ['ampersand', 'eacute', 'quotedbl', 'apostrophe', 'parenleft', 'minus', 'egrave', 'underscore', 'ccedilla']
group_numbers_es = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
group_numbers_kp = ['KP_End', 'KP_Down', 'KP_Next', 'KP_Left','KP_Begin', 'KP_Right', 'KP_Home', 'KP_Up', 'KP_Prior']
group_numbers_current = group_numbers_fr


PATH_LAYOUT_ICONS	= os.path.expanduser("~/.config/qtile/icons")
FONT = "SauceCodePro Nerd Font"
colors = {
	#"white"			: "#d3d7cf",
    "white"         : "#ffffff",   # group_names
	"light_white"	: "#e5e9f0",
	"black"			: "#242831",
	"light_black"	: "#2e3436",
	"red"			: "#ef2929",
	"light_red"		: "#bf616a",   # layout_widget_bg
	"dark_red"		: "#b11a03",   
	"blue"		 	: "#3465a4",	
	"light_blue"	: "#81a1c1",	
	"cyan" 			: "#f57900",	
	"light_cyan"	: "#fcaf3e",	
	"dark_green"	: "#037f51",	
	"green"			: "#8ae234",
	"green"			: "#8ae234",
	"light_green"	: "#a3be8c",
	"yellow"		: "#edd400",
	"light_yellow"	: "#ebcb8b",
	"magenta"		: "#75507b",
	"light_magenta" : "#b48ead",
    "black_grey"    : "#282A36",   # panel_bg
    "dark_grey"     : "#434758",   # current_screen_tab_bg
    "black"         : "#000000",   # other_screen_tabs_bg
    "purple"        : "#A77AC4",   # other_screen_tabs
    "french_blue"   : "#0055a4",
    "french_red"    : "#ef4135",
	"transparent"	: "#00000000"
}

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
        return '<span foreground="' + colors["dark_green"] + '">󰱓</span>'
    else:
        return '<span foreground="' + colors["dark_red"] + '">󰅛</span>'

def check_vpn_status():
	internet = internet_on('https://archlinux.org/')
	tun_status = subprocess.getoutput("ip addr show | grep 'tun'")
	if (not internet or tun_status == ""):
		return '<span foreground="' + colors["dark_red"] + '">󰖂</span>'
	else:
		return '<span foreground="' + colors["dark_green"] + '">󰖂</span>'

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

def is_bluetooth_hp_connected():	
    all_sinks = subprocess.getoutput('pactl list sinks | grep Name: | xargs -L 1 | cut -d " " -f 2')
    # all_sink output example:
	# alsa_output.pci-0000_03_00.1.hdmi-stereo
	# alsa_output.pci-0000_00_1f.3.analog-stereo
	# bluez_output.60_AB_D2_76_99_38.1
    if "bluez_output" in all_sinks:
        return "󰋋" # Nerd fonts: nf-mdi-headphones_off
    else:
        return "󰟎" # Nerd fonts: nf-mdi-headphones

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
    Key([mod], "x", lazy.spawn(f"xrandr --output {right_screen} --primary --mode {right_screen_res} --output {left_screen} --mode {left_screen_res} --left-of {right_screen}")),   

    # Output volume control PC
    Key([], 'XF86AudioLowerVolume', lazy.spawn(f"pactl set-sink-volume {mobo_sound_sink_name} -5%")),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(f"pactl set-sink-volume {mobo_sound_sink_name} +5%")),
    Key([], 'XF86AudioMute', lazy.spawn(f"pactl set-sink-mute {mobo_sound_sink_name} toggle")),

    # Move to previous group
    #Key(["control", alt], "Left", lazy.screen.prev_group()),
    #Key(["control", alt], "Right", lazy.screen.next_group()),
]
#log(f"pactl set-sink-volume {mobo_sound_sink_name} -5%")

# _______________________________________________________________________________________
#|                                                                                       |
#|                                       WORKSPACES                                      |
#|_______________________________________________________________________________________|
tags = ["", "", "", "󱔗", "", "󰇮", "󰊖", "󰒍", ""]

group_names = [(tags[0], {'layout': 'monadtall'}),
               (tags[1], {'layout': 'monadtall'}),
               (tags[2], {'layout': 'monadtall'}),
               (tags[3], {'layout': 'monadtall'}),
               (tags[4], {'layout': 'max'}),
               (tags[5], {'layout': 'monadtall'}),
               (tags[6], {'layout': 'monadtall'}),
               (tags[7], {'layout': 'monadtall'}),
               (tags[8], {'layout': 'monadtall'})]

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
    layout.Max(**layout_theme)
    #layout.Floating(**layout_theme)
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

#widget_defaults = dict(
#    font='Fira Code Nerd Font',
#    #font='Caskaydia Cove Nerd Font',
#    #font='Ubuntu Bold',
#    fontsize=12,
#    padding=7,
#    background = colors["black_grey"] 
#)
widget_defaults = dict(
	font		= FONT,
	fontsize	= 25,
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
		widget.Spacer(
			length = 2
		),

		modify(
			CustomImage,
			#background 	= colors["light_blue"],
			#inactive_background = colors["light_white"],
			#decorations = [ 
			#	RectDecoration(
			#		filled = True,
			#		radius = 10,
			#		use_widget_background = True
			#	)
			#],
			font = FONT,
			fontsize = 16,
			# mouse_callbacks = {
			# 	"Button1": lazy.restart()
			# },
			padding = 20,
			filename = "~/.config/qtile/icons/trioptimum-logo.png",
		),

		CustomTextBox(
			background = None,
			foreground = colors["light_white"],
			font = FONT,
			fontsize = 16,
			offset = -8,
			padding = 8,
			text = "󰇙"
		),
        #widget.GroupBox(
        #    fontsize = 30,
        #    font="FontAwesome",
        #    margin_x = 0,
        #    margin_y = 0,
        #    center_aligned = True,
        #    padding_x = 25,
        #    padding_y = 8,
        #    borderwidth = 3,
        #    inactive = colors["white"],
        #    highlight_method = "block",
        #    rounded = False,
        #    active = colors["white"],
        #    this_current_screen_border = colors["purple"],
        #    this_screen_border = colors["dark_grey"],
        #    other_current_screen_border = colors["black_grey"],
        #    other_screen_border = colors["black_grey"],
        #    foreground = colors["white"],
        #    background = colors["black_grey"]
        #),

		CustomGroupBox(
			#font=FONT,
			font = "SauceCodePro Nerd Font Mono",
			fontsize=37,
        	#background=bg,
			background = None,
   	        #background = colors["black_grey"],
        	borderwidth=1,
			center_aligned = True,
        	colors=[
				colors["red"], 
				colors["light_red"], 
				colors["yellow"], 
				colors["light_green"], 
				colors["green"], 
				colors["light_blue"], 
				colors["blue"], 
				colors["cyan"], 
				colors["light_magenta"], 
				colors["magenta"]
        	],
			this_current_screen_border = colors["purple"],
            this_screen_border = colors["dark_grey"],
            other_current_screen_border = colors["black_grey"],
            other_screen_border = colors["black_grey"],
        	#highlight_color=colors["bg"],
        	highlight_method="line",
			active=colors["light_white"],
        	inactive=colors["light_white"],
        	invert=True,
        	padding=15,
        	rainbow=True,
    	),

		CustomTextBox(
			background = None,
			foreground = colors["light_white"],
			font = FONT,
			fontsize = 16,
			offset = 10,
			padding = 4,
			text = "󰇙"
		),

		modify(
			widget.CurrentLayoutIcon,
			custom_icon_paths = [PATH_LAYOUT_ICONS],
			foreground = colors["light_black"],
			background = colors["light_magenta"],
			font = FONT,
			fontsize = 16,
			decorations = [
				RectDecoration(
					filled = True,
					radius = [10, 0, 0, 10],
					use_widget_background = True
				)
			],
			padding = 6, 
			scale = 0.5

		),

		modify(
			CustomTextBox,
			foreground = colors["light_black"],
			background = colors["light_magenta"],
			font = FONT,
			fontsize = 1,
			decorations = [
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			text = " ",
		),

		modify(
			CustomTextBox,
			foreground = colors["light_black"],
			background = colors["light_red"],
			font = FONT,
			fontsize = 13,
			offset = -1,
			text = "",
			x = -5
		),

		modify(
			widget.CheckUpdates,
			foreground = colors["light_black"],
			background = colors["light_red"],
			font = FONT,
			fontsize = 13,
			decorations = [
				RectDecoration(
					filled = True,
					radius = [0, 10, 10, 0],
					use_widget_background = True
				)
			],
			colour_have_updates = colors["light_black"],
			colour_no_updates = colors["light_black"],
			display_format = "{updates} updates  ",
			distro = "Arch",
			initial_text = "No updates  ",
			no_update_string = "No updates  ",
			padding = 0,
			update_interval = 60,
		),
		

		widget.Spacer(),

		widget.WindowName(
			foreground = colors["light_white"],
			background = None,
			font = FONT,
			fontsize = 13,
			max_chars = 60,
			format = "{name}",
			width = CALCULATED
		),

		widget.Spacer(),
		
		widget.GenPollText(
			foreground = colors["light_black"],
			background = colors["light_yellow"],
			font = FONT,
			fontsize = 25,
			decorations = [
				RectDecoration(
					filled = True,
					radius = [10, 0, 0, 10],
					use_widget_background = True
				)
			],
			padding = 12,
            func=check_vpn_status,
            update_interval=0.1,
        ),

		widget.GenPollText(
			foreground = colors["light_black"],
			background = colors["light_yellow"],
			font = FONT,
			fontsize = 25,
			decorations = [
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			padding = 15,
            func=print_internet_status,
            update_interval=0.1,
        ),
		
		modify(
			CustomTextBox,
			foreground = colors["light_black"],
			background 	= colors["light_blue"],
			decorations = [ 
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			font = FONT,
			padding = 5,
			fontsize = 20,
			text = "",
			x = 4
		),

		widget.GenPollText(
			foreground = colors["light_black"],
			background = colors["light_blue"],
			font = FONT,
			fontsize = 22,
			decorations = [
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			padding = 15,
            func=is_bluetooth_hp_connected,
            update_interval=0.1,
        ),

		
		CustomTextBox(
			foreground = colors["light_black"],
			background = colors["light_red"],
			font = FONT,
			fontsize = 20,
			offset = -2,
			padding = 7,
			text = "",
			x = -2
		),

		modify(
			widget.PulseVolume,
			foreground = colors["light_black"],
			background = colors["light_red"],
			font = FONT,
			fontsize = 16,
			decorations = [
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			update_interval = 0.01,
			device = mobo_sound_sink_name,
			#width = CALCULATED,
			padding = 0,
			fmt = " {} "
			#volume_down_command = f"pactl set-sink-volume {mobo_sound_sink_name} -5%",
			#volume_up_command = f"pactl set-sink-volume {mobo_sound_sink_name} -5%"
		),


		CustomTextBox(
			foreground = colors["light_black"],
			background = colors["light_green"],
			font = FONT,
			fontsize = 20,
			offset = -2,
			padding = 5,
			text = "󰍛",
			x = -2
		),

		widget.Memory(
			foreground = colors["light_black"],
			background = colors["light_green"],
			font = FONT,
			fontsize = 15,
			decorations = [
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			format = "{MemUsed: 2.1f} {mm}b ",
			padding = -1,
			measure_mem = "G"
		),

		CustomTextBox(
			foreground = colors["light_black"],
			background = colors["light_cyan"],
			font = FONT,
			fontsize = 20,
			padding = 10,
			offset = -1,
			text = "󰋊",
			x = -5
		),

		widget.DF(
			foreground = colors["light_black"],
			background = colors["light_cyan"],
			font = FONT,
			fontsize = 15,
			decorations = [
				PowerLineDecoration(
					path = "arrow_right",
					size = 11
				)
			],
			format = "{f: 3.0f} Gb ",
			padding = 0,
			partition = "/",
			visible_on_warn = False,
			warn_color = colors["light_cyan"]
		),
		
		CustomTextBox(
			foreground = colors["light_black"],
			background = colors["light_yellow"],
			font = FONT,
			fontsize = 20,
			offset = -1,
			text = "",
			x = -5
		),

		widget.GenPollText(
			foreground = colors["light_black"],
			background = colors["light_yellow"],
			font = FONT,
			fontsize = 15,
			decorations = [
				RectDecoration(
					filled = True,
					radius = [0, 10, 10, 0],
					use_widget_background = True
				)
			],
			padding = 10,
            func=get_kb_layout,
            update_interval=0.5,
        ),

		CustomTextBox(
			background = None,
			foreground = colors["light_white"],
			font = FONT,
			fontsize = 16,
			padding = 8,
			text = "󰇙"
		),

		modify(
			CustomTextBox,
			foreground = colors["light_black"],
			background = colors["light_magenta"],
			decorations = [
				RectDecoration(
					filled = True,
					radius = [10, 0, 0, 10],
					use_widget_background = True
				)
			],
			font = FONT,
			fontsize = 20,
			offset = 2,
			text = "󰥔",
			x = 4
		),

		modify(
			widget.Clock,
			foreground = colors["light_black"],
			background = colors["light_magenta"],
			decorations = [
				RectDecoration(
					filled = True,
					radius = [0, 10, 10, 0],
					use_widget_background = True
				)
			],
			font = FONT,
			fontsize = 16,
			format = "%d %b %Y - %H:%M",
			padding = 6
		),

		widget.Spacer(
			length = 2
		)    
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
	return widgets_screen2


#def init_screens():
#    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=30)),
#            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=30)),
#            Screen(top=bar.Bar(widgets=init_widgets_screen3(), opacity=1.0, size=30))]

def init_screens():
	return [
		Screen(top=bar.Bar(
			widgets=init_widgets_screen1(),
			size=40,
			#background=colors["light_black"],
			#border_color=colors["light_black"],
			margin=[10,10,0,10],
			border_width=4,
			opacity = 1)
		),
		Screen(top=bar.Bar(
			widgets=init_widgets_screen2(), 
			size=40,
			#background=colors["light_black"],
			#border_color=colors["light_black"],
			margin=[10,10,0,10],
			border_width=4,
			opacity = 1)
		)]



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
