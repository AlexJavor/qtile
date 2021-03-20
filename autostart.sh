#!/bin/sh
# Set up Wallpaper
feh --bg-scale ~/Pictures/trioptimum.jpeg &
sleep 0.5

# Activate and configure the 2 screens at the same time (Main+TV) (tested in Ubuntu 20.04.1 LTS x86_64):
#xrandr --output eDP-1 --primary --mode 1920x1080 --output HDMI-1 --mode 1920x1080  --left-of eDP-1

# Activate and configure the 2 screens at the same time (Main+HP) (tested in Ubuntu 20.04.1 LTS x86_64):
#xrandr --output eDP-1 --primary --mode 1920x1080 --output DP-1 --mode 1600x900 --right-of eDP-1

# Activate and configure the 3 screens at the same time (tested in Ubuntu 20.04.1 LTS x86_64):
# Set eDP-1 (Laptop screen) as primary monitor + HDMI-1 (TV) as secondary(1) monitor left of the laptop + DP-1 (HP screen) as secondary(2) monitor right of the laptop
#xrandr --output eDP-1 --primary --mode 1920x1080 --output HDMI-1 --mode 1920x1080  --left-of eDP-1 --output DP-1 --mode 1600x900 --right-of eDP-1
#sleep 0.5

# Default to french keyboard
#setxkbmap fr
