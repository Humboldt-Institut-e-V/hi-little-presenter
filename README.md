# hi-little-presenter

Runs presentations in PDF/ODP format in an endless loop on a Raspberry Pi or other Linux Desktop. Is operated via web interface.

## Installation

Download and Install "[Raspberry Pi OS  with desktop](https://www.raspberrypi.org/downloads/raspberry-pi-os/)" on a SD card

Boot your Raspberry Pi from your SD card and follow the initial setup routine. Our settings are:
 - Language: Deutsch, Country: Deutschland, Timezone: Berlin
 - A solid password
 - No WiFi

Run a software update and reboot the system.

### Adjust the system configuration 

- Open "Raspberry-Pi-Configuration" via start menu.
- In the "System" tab choose a better "host name"
- In the "Interfaces" tab activate "SSH"
- In the "Performance" tab set "GPU memory" to 128 MB.
- Accept all changes with "OK" and reboot the system.
    

### Install software dependencies

```bash
sudo apt install python3-tornado python3-psutil libreoffice impressive
```

### Install "hi-little-presenter"

Copy the directory "LittlePresenter" to the home directory of the user "pi" (/home/pi).

Create the directory "~/.config/autostart":

```bash
mkdir ~/.config/autostart
```

Copy the file "\~/LittlePresenter/LittlePresenter.desktop" to the directory "\~/.config/autostart".

```bash
cp ~/LittlePresenter/LittlePresenter.desktop ~/.config/autostart/
```

### Ajust the appearance of the desktop

Open "Desktop settings" via right click on the desktop.

Choose "~/LittlePresenter/wallpaper.png" as your desktop wallpaper.

Turn off displaying of "Wastebasket" and "Mounted Disks" on desktop.

### Testing

Reboot the Raspberry Pi and open the web interface in a browser from any computer in the same network.

http://\<IP-ADDRESS\>:8080

### Final configuration steps

Set either a static IP address for your Raspberry Pi out side the range of your DHCP server or make sure it always gets the same IP address via DHCP. 

To set a static IP address perform a right click on the network icon (top, right ). Click "Wireless & Wired Network Settings", choose the interface "eth0" and enter your configuration.
