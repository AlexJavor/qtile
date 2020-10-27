# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# IMPORTANT: Create simbolic links for the "set_brightness_config" and "set_volume_config":
# ln -s ~/.config/qtile/set_volume_config volume
# ln -s ~/.config/qtile/set_brightness_config brightness

# ************** Log path *************** #
# /home/$USER/.local/share/qtile/qtile.log

# ************** default_config path *************** #
# /usr/lib/python3/dist-packages/libqtile/resources/default_config.py

import os
import subprocess
import platform
import socket
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
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

sound_card_output_HDMI = '1'
sound_card_output_PC = '2'
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

def get_kb_layout():
    kb_layout = subprocess.getoutput("setxkbmap -query | grep layout | awk '{print $2}'")
    return kb_layout

def get_current_volume1():
    volume = subprocess.getoutput("pacmd list-sinks | grep volume:\ front | awk '{i++} i==1{print $5+0}'")
    muted  = subprocess.getoutput("pacmd list-sinks | grep muted | awk '{i++} i==1{print $2}'")
    if(volume == ""):
        return "N/A"
    else:
        if(muted == "yes"):
            return "M"
        else:
            return volume + "%"
    
def get_current_volume2():
    volume = subprocess.getoutput("pacmd list-sinks | grep volume:\ front | awk '{i++} i==2{print $5+0}'")
    muted  = subprocess.getoutput("pacmd list-sinks | grep muted | awk '{i++} i==2{print $2}'")
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

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(my_terminal)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # ************************ AlexJavor custom *************************** #
    # Select screen focus
    Key([mod, alt], group_numbers_current[0], lazy.to_screen(0)),
    Key([mod, alt], group_numbers_current[1], lazy.to_screen(1)),
    Key([mod, alt], group_numbers_current[2], lazy.to_screen(2)),

    # Shift keyboard layout
    Key(["shift", alt], "e", lazy.spawn("setxkbmap es")),
    Key(["shift", alt], "f", lazy.spawn("setxkbmap fr")),

    # Open Firefox
    Key([mod], "f", lazy.spawn("firefox")),
    
    # Open Pavucontrol
    Key([mod], "p", lazy.spawn("pavucontrol")),

    # Open config
    Key([mod], "c", lazy.spawn("codium .config/qtile/config.py")),

    # Reload Multiple Screens (2 Screens)
    Key([mod], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1920x1080  --left-of " + main_screen)),
    # Reload Multiple Screens (3 Screens)
    Key([mod, "control"], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1920x1080  --left-of " + main_screen + " --output " + displayport_screen + " --mode 1600x900 --right-of " + main_screen)),

    # Output volume control HDMI
    Key([], 'XF86AudioLowerVolume', lazy.spawn("pactl set-sink-volume " + sound_card_output_HDMI + " -5%")),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("pactl set-sink-volume " + sound_card_output_HDMI+ " +5%")),
    Key([], 'XF86AudioMute', lazy.spawn("pactl set-sink-mute " + sound_card_output_HDMI + " toggle")), 
    # Output volume control PC
    Key(["control"], 'XF86AudioLowerVolume', lazy.spawn("pactl set-sink-volume " + sound_card_output_PC + " -5%")),
    Key(["control"], 'XF86AudioRaiseVolume', lazy.spawn("pactl set-sink-volume " + sound_card_output_PC + " +5%")),
    Key(["control"], 'XF86AudioMute', lazy.spawn("pactl set-sink-mute " + sound_card_output_PC + " toggle")), 
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

group_names = [("DEV", {'layout': 'monadtall'}),
               ("WWW", {'layout': 'monadtall'}),
               ("SYS", {'layout': 'monadtall'}),
               ("DOC", {'layout': 'monadtall'}),
               ("VBOX", {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("VID", {'layout': 'monadtall'}),
               ("GFX", {'layout': 'floating'})]

#group_names = 'DEV WWW SYS DOC VBOX CHAT MUS VID GFX'.split()

#groups = [Group(name, layout='max') for name in group_names]
groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 0):
#for i, name in enumerate(group_names):
    # indx = str(i + 1)
    keypad_indx = group_numbers_current[i]
    keys.append(Key([mod], keypad_indx, lazy.group[name].toscreen()))
    keys.append(Key([mod, 'shift'], keypad_indx, lazy.window.togroup(name)))
        


layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='Ubuntu Bold',
    fontsize=12,
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
            fontsize = 12,
            margin_x = 0,
            margin_y = 0,
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
        
        widget.TextBox(
            background = colors["white"],
            foreground = colors["black_grey"],
            text = "AlexJavor-MAIN", 
            name="default"
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        widget.Net(
            interface = "wlp5s0",
            format = '{interface}: {down} ▼▲ {up}'
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        
        widget.CPU(
            format = 'CPU: {load_percent}%'
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        widget.Memory(
                foreground = colors["white"],
                background = colors["black_grey"],
                padding = 5,
                format = 'RAM: {MemUsed}Mb ({MemPercent}%)'
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            background = colors["black_grey"],
            padding = 0,
            scale = 0.5
        ),
        widget.CurrentLayout(**widget_defaults),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),

        widget.TextBox(text = "\U0001F50B"),
        widget.Battery(
            format = '{percent:2.0%}'
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        
        # Volume
        widget.TextBox(text = "\U0001F50A"),
        widget.GenPollText(
            func=get_current_volume1,
            update_interval=0.2,
        ),
        widget.TextBox(text = "\U0001F50A"),
        widget.GenPollText(
            func=get_current_volume2,
            update_interval=0.2,
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        
        widget.TextBox(text = "\u2328"),
        widget.GenPollText(
            func=get_kb_layout,
            update_interval=0.5,
        ),

        widget.Sep(linewidth = 1, padding = 10, foreground = colors["white"], background = colors["black_grey"]),
        
        widget.Clock(format='📅  %A, %d %b. %Y - %H:%M:%S'), # %S for adding seconds
    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list() # Slicing removes unwanted widgets on Monitors 1,3
    return widgets_screen1                       

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

def init_widgets_screen3():
    widgets_screen3 = init_widgets_list()
    return widgets_screen3            

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen3(), opacity=1.0, size=30))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


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
