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

mod = "mod4"
colors = {
    "panel_bg" : "#282A36",
    "current_screen_tab_bg" : "#434758",
    "group_names" : "#ffffff",
    "layout_widget_bg" : "#ff5555",
    "other_screen_tabs_bg" : "#000000",
    "other_screen_tabs" : "#A77AC4"
}

sound_card_output_HDMI = '1'
sound_card_output_PC = '2'
main_screen = 'eDP-1-1'
hdmi_screen = 'HDMI-1-1'
displayport_screen = 'DP-1-1'

max_percentage_volume = '100' # Maximum Percentage: 150%

selected_screen = {
    "MainPC": "eDP-1-1",
    "TV": "HDMI-1-1",
    "DisplayPortScreen": "DP-1-1"
}

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
    Key([mod], "Return", lazy.spawn("terminator")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # ************************ AlexJavor custom *************************** #
    #Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 1 sset Master,0 5%-')),
    #Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 1 sset Master,0 5%+')),
    #Key([], 'XF86AudioMute', lazy.spawn('amixer sset Master,0 toggle')),
    Key([mod, "mod1"], "1",      lazy.to_screen(0)),
    Key([mod, "mod1"], "2",      lazy.to_screen(1)),
    Key([mod, "mod1"], "3",      lazy.to_screen(2)),

    # Open Firefox
    Key([mod], "f", lazy.spawn("firefox")),

    # Reload Multiple Screens (2 Screens)
    Key([mod], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1920x1080  --left-of " + main_screen)),
    # Reload Multiple Screens (3 Screens)
    Key([mod, "control"], "x", lazy.spawn("xrandr --output " + main_screen + " --primary --mode 1920x1080 --output " + hdmi_screen + " --mode 1920x1080  --left-of " + main_screen + " --output " + displayport_screen + " --mode 1600x900 --right-of " + main_screen)),

    # Output volume control HDMI
    Key([], 'XF86AudioLowerVolume', lazy.spawn("volume " + sound_card_output_PC + " - 5 " + max_percentage_volume)),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("volume " + sound_card_output_PC + " + 5 " + max_percentage_volume)),
    Key([], 'XF86AudioMute', lazy.spawn("volume " + sound_card_output_PC + " m 0 " + max_percentage_volume)),
    # Output volume control PC
    Key(["control"], 'XF86AudioLowerVolume', lazy.spawn("volume " + sound_card_output_HDMI + " - 5 " + max_percentage_volume)),
    Key(["control"], 'XF86AudioRaiseVolume', lazy.spawn("volume " + sound_card_output_HDMI + " + 5 " + max_percentage_volume)),
    Key(["control"], 'XF86AudioMute', lazy.spawn("volume " + sound_card_output_HDMI + " m 0 " + max_percentage_volume)),

    # Brightness and state control Main Screen (PC)
    Key([], 'XF86MonBrightnessUp', lazy.spawn("brightness " + main_screen + " + 50 ")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("brightness " + main_screen + " - 50 ")),
    # Brightness and state control HDMI Screen (TV)
    Key(["control"], 'XF86MonBrightnessUp', lazy.spawn("brightness " + hdmi_screen + " + 50 ")),
    Key(["control"], 'XF86MonBrightnessDown', lazy.spawn("brightness " + hdmi_screen + " - 50 ")),
    # Brightness and state control Mini Display Port Screen (Screen2)
    Key(["shift"], 'XF86MonBrightnessUp', lazy.spawn("brightness " + displayport_screen + " + 50 ")),
    Key(["shift"], 'XF86MonBrightnessDown', lazy.spawn("brightness " + displayport_screen + " - 50 ")),
]


group_names = 'DEV WWW SYS DOC VBOX CHAT MUS VID GFX'.split()
groups = [Group(name, layout='max') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Floating()
]

widget_defaults = dict(
    font='Ubuntu Bold',
    fontsize=12,
    padding=3,
    background = colors["panel_bg"] 
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    foreground = colors["group_names"],
                    background = colors["panel_bg"]
                ),
                widget.GroupBox(font="Ubuntu Bold",
                    fontsize = 12,
                    margin_x = 0,
                    margin_y = 0,
                    padding_x = 8,
                    padding_y = 8,
                    borderwidth = 1,
                    active = colors["group_names"],
                    inactive = colors["group_names"],
                    highlight_method = "block",
                    rounded = False,
                    this_current_screen_border = colors["other_screen_tabs"],
                    this_screen_border = colors["current_screen_tab_bg"],
                    other_current_screen_border = colors["panel_bg"],
                    other_screen_border = colors["panel_bg"],
                    foreground = colors["group_names"],
                    background = colors["panel_bg"]
                ),
                widget.Prompt(
                    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname()),
                    font = "Ubuntu Mono",
                    padding = 10,
                    foreground = colors["layout_widget_bg"],
                    background = colors["current_screen_tab_bg"]
                ),
                widget.WindowName(
                    foreground = colors["other_screen_tabs"]
                ),
                
                widget.TextBox(
                    background = colors["other_screen_tabs"],
                    text = "AlexJavor-MAIN", 
                    name="default"
                ),
                widget.CurrentLayout(**widget_defaults),
                #widget.Battery(**widget_defaults),
                widget.ThermalSensor(**widget_defaults),
                widget.CheckUpdates(
                    distro = 'Ubuntu'
                ),
                widget.Systray(),
                widget.Net(interface="wlp5s0"),
                widget.Volume(**widget_defaults),
                widget.Clock(format='%A, %d/%m/%Y - %H:%M'),
            ],
            30,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors["group_names"],
                    background = colors["panel_bg"]
                ),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("AlexJavor-SECONDARY-1", name="default"),
                widget.Systray(),
                widget.Net(interface="wlp5s0"),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors["group_names"],
                    background = colors["panel_bg"]
                ),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("AlexJavor-SECONDARY-2", name="default"),
                widget.Systray(),
                widget.Net(interface="wlp5s0"),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
        ),
    )
]

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
floating_layout = layout.Floating()
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
