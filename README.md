# **Qtile Skrivroot configuration**
## **Installation**

Official documentation: https://docs.qtile.org/en/latest/manual/install/

1. Install qtile and other dependencies using a package manager. Example:
```
pacman -S qtile 
pacman -S xorg xorg-xinit picom lightdm lightdm-slick-greeter dmenu feh arc-gtk-theme arc-icon-theme
yay -S nerd-fonts-fira-code
yay -S ttf-nerd-fonts-symbols
yay -S ttf-nerd-fonts-symbols-common
yay -S ttf-nerd-fonts-symbols-mono
yay -S ttf-sourcecodepro-nerd
```
2. Create the directory `~/.config/qtile` and clone the GitHub repository
```
mkdir ~/.config/qtile/
cd ~/.config/qtile/
git clone git@github.com:AlexJavor/qtile.git
```
3. Change to the appropriate branch depending on the system
```
git checkout <branch>
```
4. Change the name of the file containing the env variables to `.env` (while conserving the original). Example: 
```
cp .env.fractal .env
```
5. Move the `qtile.desktop` file to `/usr/share/xsessions`
```
cp display_system_conf/qtile.desktop /usr/share/xsessions
```
6. Append the contents of `.xprofile` to the user's file
```
cat display_system_conf/.xprofile >>  ~/.xprofile
```
7. Move the `20_keyboard.conf` file to `/etc/X11/xorg.conf.d`
```
cat display_system_conf/20_keyboard.conf >> /etc/X11/xorg.conf.d
```
8. If lightdm is used as a display manager, modify the following lines in the config file:
```
vim /etc/lightdm/lightdm.conf

[Seat:*]
[...]
greeter-session=lightdm-slick-greeter
[...]
user-session=qtile
[...]
```

9. Reboot. Check the qtile logs for any errors:
```
tail /home/$USER/.local/share/qtile/qtile.log
```



