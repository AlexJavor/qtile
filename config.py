#   ___  _   _ _         ____             __ _                    _    _              _                       
#  / _ \| |_(_) | ___   / ___|___  _ __  / _(_) __ _             / \  | | _____  __  | | __ ___   _____  _ __ 
# | | | | __| | |/ _ \ | |   / _ \| '_ \| |_| |/ _` |  _____    / _ \ | |/ _ \ \/ /  | |/ _` \ \ / / _ \| '__|
# | |_| | |_| | |  __/ | |__| (_) | | | |  _| | (_| | |_____|  / ___ \| |  __/>  < |_| | (_| |\ V / (_) | |   
#  \__\_\\__|_|_|\___|  \____\___/|_| |_|_| |_|\__, |         /_/   \_\_|\___/_/\_\___/ \__,_| \_/ \___/|_|   
#                                              |___/                                                          

# IMPORTANT: Create simbolic links for the "set_brightness_config" and "set_volume_config":
# ln -s ~/.config/qtile/set_volume_config volume
# ln -s ~/.config/qtile/set_brightness_config brightness

# ************** Log path *************** #
# /home/$USER/.local/share/qtile/qtile.log

# ************** default_config path *************** #
# /usr/lib/python3/dist-packages/libqtile/resources/default_config.py

# ************** Arch default libqtile path ******** #
# /usr/lib/python3.9/site-packages/libqtile/

import os
import subprocess
import platform
import socket
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger
import os
import subprocess

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

my_terminal= "terminator"
alt = "mod1"
mod = "mod4"

colors = {
    "black_grey" : "#282A36",   # panel_bg
    "dark_grey"  : "#434758",   # current_screen_tab_bg
    "white"      : "#ffffff",   # group_names
    "light_red"  : "#ff5555",   # layout_widget_bg
    "black"      : "#000000",   # other_screen_tabs_bg
    "purple"     : "#A77AC4",   # other_screen_tabs
    "french_blue": "#0055a4",
    "french_red" : "#ef4135"
}

sound_card_index_HDMI = 'TBD'
sound_card_index_PC   = 'TBD'
sound_card_order_HDMI = 'TBD'
sound_card_order_PC   = 'TBD'

main_screen = 'eDP-1'
hdmi_screen = 'HDMI-1'
displayport_screen = 'DP-1'

max_percentage_volume = '100' # Maximum Percentage: 150%

selected_screen = {
    "MainPC": "eDP-1",
    "TV": "HDMI-1",
    "DisplayPortScreen": "DP-1"
}

group_numbers_fr = ['ampersand', 'eacute', 'quotedbl', 'apostrophe', 'parenleft', 'minus', 'egrave', 'underscore', 'ccedilla']
group_numbers_es = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
group_numbers_kp = ['KP_End', 'KP_Down', 'KP_Next', 'KP_Left','KP_Begin', 'KP_Right', 'KP_Home', 'KP_Up', 'KP_Prior']
group_numbers_current = group_numbers_kp

def xmr_ticker():
    xmr_price = subprocess.getoutput("curl -s eur.rate.sx/1xmr")
    xmr_price_split = xmr_price.split(".")
    xmr_price_shown = xmr_price_split[0] + "." + xmr_price_split[1][:2]
    return "XMR: " + xmr_price_shown + "€"

def get_current_country():
    public_ip = subprocess.getoutput("dig +short myip.opendns.com @resolver1.opendns.com")
    country = subprocess.getoutput("whois " + public_ip + " | awk ' /[Cc]ountry/{print $2}'")
    return country
 
def get_kb_layout():
    kb_layout = subprocess.getoutput("setxkbmap -query | grep layout | awk '{print $2}'")
    return kb_layout

def get_index_volume():
    sink1_name  = subprocess.getoutput("pacmd list-sinks | grep alsa.name | awk '{i++} i==1{print}' | cut -f 2 -d '=' | cut -f 2 -d '\"'")
    sink1_index = subprocess.getoutput("pacmd list-sinks | grep index | awk '{i++} i==1{print}' | cut -f 2 -d ':' | cut -f 2 -d ' '")
    sink2_name  = subprocess.getoutput("pacmd list-sinks | grep alsa.name | awk '{i++} i==2{print}' | cut -f 2 -d '=' | cut -f 2 -d '\"'")
    sink2_index = subprocess.getoutput("pacmd list-sinks | grep index | awk '{i++} i==2{print}' | cut -f 2 -d ':' | cut -f 2 -d ' '")
    global sound_card_index_PC
    global sound_card_index_HDMI
    global sound_card_order_PC 
    global sound_card_order_HDMI
    
    if(sink1_name == 'ALC892 Analog' and sink2_name == 'HDMI 0'):
        sound_card_index_PC   = sink1_index
        sound_card_index_HDMI = sink2_index
        sound_card_order_PC   = "1"
        sound_card_order_HDMI = "2"
    elif(sink1_name == 'HDMI 0' and sink2_name == 'ALC892 Analog'):
        sound_card_index_PC   = sink2_index
        sound_card_index_HDMI = sink1_index
        sound_card_order_PC   = "2"
        sound_card_order_HDMI = "1"
    else:
        logger.warning("ERROR: There is a sound card NOT DEFINED! - Check get_index_volume()")

def get_current_volume_ALC892Analog():
    get_index_volume()
    volume = subprocess.getoutput("pacmd list-sinks | grep volume:\ front | awk '{i++} i==" + sound_card_order_PC + "{print $5+0}'")
    muted  = subprocess.getoutput("pacmd list-sinks | grep muted | awk '{i++} i==" + sound_card_order_PC + "{print $2}'")
    if(volume == ""):
        return "N/A"
    else:
        if(muted == "yes"):
            return "M"
        else:
            return volume + "%"
    
def get_current_volume_HDMI0():        
    get_index_volume()
    volume = subprocess.getoutput("pacmd list-sinks | grep volume:\ front | awk '{i++} i==" + sound_card_order_HDMI + "{print $5+0}'")
    muted  = subprocess.getoutput("pacmd list-sinks | grep muted | awk '{i++} i==" + sound_card_order_HDMI + "{print $2}'")
    if(volume == ""):
        return "N/A"
    else:
        if(muted == "yes"):
            return "M"
        else:
            return volume + "%"
    
# Not used
#def get_keycode():
#    keycode = subprocess.getoutput("xmodmap -pke | grep KP_1 | awk '{print $2}'")
#    return keycode
get_index_volume()
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

    # Shift keyboard layout
    Key(["shift", alt], "e", lazy.spawn("setxkbmap es")),
    Key(["shift", alt], "f", lazy.spawn("setxkbmap fr")),

    # Open Firefox
    Key([mod], "f", lazy.spawn("firefox")),
    # Open Tor Browser
    Key([mod], "t", lazy.spawn("torbrowser-launcher")),
    # Open Pavucontrol
    Key([mod], "p", lazy.spawn("pavucontrol")),
    # Open Session
    Key([mod], "s", lazy.spawn("./SourceCode/Session/session-desktop-linux-x86_64-1.4.4.AppImage")),
    # Open config
    Key([mod], "c", lazy.spawn("codium .config/qtile/config.py")),

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

group_names = [("DEV",  {'layout': 'monadtall'}),
               ("WWW",  {'layout': 'monadtall'}),
               ("SYS",  {'layout': 'monadtall'}),
               ("DOC",  {'layout': 'monadtall'}),
               ("VM",   {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("OBS",  {'layout': 'monadtall'}),
               ("VPS",  {'layout': 'monadtall'}),
               ("GFX",  {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 0):
    keypad_indx = group_numbers_current[i]
    keys.append(Key([mod], keypad_indx, lazy.group[name].toscreen()))
    keys.append(Key([mod, 'shift'], keypad_indx, lazy.window.togroup(name)))
        

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

widget_defaults = dict(
    font='Ubuntu Bold',
    fontsize=11,
    padding=3,
    background = colors["black_grey"] 
)

def init_widgets_list():
    widgets_list = [

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
        widget.GroupBox(font="Ubuntu Bold",
            #fontsize = 12,
            margin_x = 0,
            margin_y = 2,
            padding_x = 8,
            padding_y = 8,
            borderwidth = 1,
            active = colors["white"],
            inactive = colors["white"],
            highlight_method = "block",
            rounded = False,
            this_current_screen_border = colors["purple"],
            this_screen_border = colors["dark_grey"],
            other_current_screen_border = colors["black_grey"],
            other_screen_border = colors["black_grey"],
            foreground = colors["white"],
            background = colors["black_grey"]
        ),

        widget.Prompt(
            prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname()),
            font = "Ubuntu Mono",
            padding = 10,
            foreground = colors["light_red"],
            background = colors["dark_grey"]
        ),

        widget.WindowName(
            foreground = colors["purple"]
        ),
        
        widget.Image(
            filename = "~/.config/qtile/icons/rj45.png",
            margin = 2,
            margin_x = 5
        ),
        widget.Net(
            interface = "wlp5s0",
            format = '{down} ▼▲ {up}' # format = '{interface}: {down} ▼▲ {up}'
        ),
        
        widget.Sep(linewidth = 0, padding = 3),
        widget.Image(
            filename = "~/.config/qtile/icons/processor.png",
            margin = 4,
            margin_x = 5
        ),
        widget.CPU(
            format = '{load_percent}%'
        ),

        widget.Sep(linewidth = 0, padding = 3),
        widget.Image(
            filename = "~/.config/qtile/icons/ram.png",
            margin = 2,
            margin_x = 5
        ),
        widget.Memory(
                foreground = colors["white"],
                background = colors["black_grey"],
                padding = 5,
                format = '{MemUsed}Mb ({MemPercent}%)'
        ),

        widget.Sep(linewidth = 0, padding = 3),
        widget.Image(
            filename = "~/.config/qtile/icons/floppy-disk.png",
            margin = 5,
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

        # Bitcoin ticker
        widget.BitcoinTicker(
            foreground = "#f7931a",
            currency="EUR",
        ),

        # Monero ticker
        widget.GenPollText(
            func=xmr_ticker,
            update_interval=30,
            foreground = "#fc6a03"
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            background = colors["black_grey"],
            padding = 0,
            scale = 0.5
        ),
        #widget.CurrentLayout(**widget_defaults),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        widget.BatteryIcon(
            battery=0
        ),
        widget.Battery(
            format = '{percent:2.0%}'
        ),
        
        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        
        # Volume
        widget.Image(
            filename = "~/.config/qtile/icons/volume.png",
            margin = 5,
            margin_x = 5
        ),
        widget.GenPollText(
            func=get_current_volume_ALC892Analog,
            update_interval=0.1
        ), 
        widget.Image(
            filename = "~/.config/qtile/icons/volume.png",
            margin = 5,
            margin_x = 5
        ),
        widget.GenPollText(
            func=get_current_volume_HDMI0,
            update_interval=0.1
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        
        widget.Image(
            filename = "~/.config/qtile/icons/keyboard.png",
            margin = 6,
            margin_x = 5
        ),
        
        widget.GenPollText(
            func=get_kb_layout,
            update_interval=0.5,
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        widget.Clock(format=' %a, %d %b. %Y - %H:%M:%S'), # %S for adding seconds
    ]
    return widgets_list


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
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen3(), opacity=1.0, size=25))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {"wmclass": "obs"},
    {"wmclass": "notify"},
])
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
