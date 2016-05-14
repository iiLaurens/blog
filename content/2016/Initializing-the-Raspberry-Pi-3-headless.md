Title: Initializing the Raspberry Pi 3 (headless)
Slug: Initializing-the-raspberry-pi-3
Date: 2016-05-03 20:15
Tags: Raspberry Pi 3, Settings
Author: Laurens

Recently I received my first Raspberry Pi 3 in an attempt to satisfy the curiousity.
I occasionally play with projects that require jobs to be run at regular interval and
having a low powered Raspberry Pi 3 to do this is ideal. Since I will likely mess up
my RPi3 numerous times I would like to quickly document how I set up my RPi3 so I can
reset my pi if need be. In this guide I will briefly explain the essential steps that are needed to get a usable RPi. In this guide I will do that completely headless, that is without any keyboard, screen or other peripherals connected to the Raspberry Pi.


First a interesting little fact that I would like to share. [A recent review](http://tweakers.net/reviews/4443/5/raspberry-pi-3-net-iets-sneller-dan-de-oude-opgenomen-vermogen-en-warmte.html) shows that the RPi3 consumes 2.21 Watt in idle state and
and maximum peaks of 3.62 Watt under stress. If we assume a generous 2.5 Watt average power consumption and 0.23€ Kwh energy price, the RPi3 costs only
`2.5 / 1000 * 24 * 365 * 0.23 = 5.037€` to operate full-time per year. It thus costs virtually
nothing to run my own little RPi3 server and it is an excellent opportunity for me to
experience and learn the ways of Linux.

# Installing the OS
The official supported operating system for the RPi is [Raspbian](https://www.raspberrypi.org/downloads/raspbian), and comes pre-installed with plenty of software for education, programming and general use. It has Python, Scratch, Sonic Pi, Java, Mathematica and more. Since I will be running the RPi headless, I will be obtaining
the Raspbian Jessie Lite image. This lite version of Raspbian does not include the
components for displaying a desktop environment. Everything will be running from a
simple terminal, which hopefully frees some much needed resources.

For Windows, the image can simply be installed to a MicroSD card (min. 2GB) using `Win32DiskImager` ([Sourceforge page](http://sourceforge.net/projects/win32diskimager/)). These directions are pretty straightforward, altough be aware that this wipes the complete SD card, so back up what you still need on the card.

# Setting up to the Raspberry Pi 3 for the first time
After writing the image the SD card, it needs to be inserted into the RPi. Power the RPi with
standard microUSB charger. It is wise to have a charger that provides a stable voltage and plenty of amperes. The recommended voltage is 5V (or within 10% margin) and at least 2A. Having too little power can result in an unstable pi. Now that the pi is running, we would like to contol it. To control it we have to use a SSH connection. SSH, or secure shell, is the mainstay of remote access and administration in the Linux world. Windows lacks a native SSH client for connecting to Linux machines. So if you are a Windows user like me, please grab a SSH client first, *e.g.* [Putty](http://www.putty.org/).

## Connecting to the RPi3
The RPi3 has onboard WiFi, but unfortunately has no ears. This makes it hard for us to tell it the correct WiFi settings. Fortunately, most people will have some LAN cable to connect the RPi for the first time and edit the relevant WiFi settings. Simply connect the RPi to a router or computer and try to discover the local IP adress of the RPi. Enter this IP adress in your SSH client, and assume the default port for SSH (port 22). The SSH terminal will ask for a user and password. The default password is `pi` and the password is `raspberry`.

If you have no LAN cable available or you are just lazy like me, there is a workaround which I will explain in the next section that allows us to set up WiFi without the need of a LAN cable.

## Setting up WiFi
We now must set up the RPi with the correct WiFi configuration. For this we need to edit the file `\etc\wpa_supplicant\wpa_supplicant.conf`. If already connected to the Pi through a LAN cable, we can simply edit that file over SSH using the command
```
sudo nano \etc\wpa_supplicant\wpa_supplicant.conf
```
If not connected yet, it is possible to edit the SD card using another Linux-operated computer or by mounting the *Ext* filesystem on the SD card on Windows with [Pargon ExtFS for Windows](http://www.paragon-software.com/home/extfs-windows/). With the latter option, please use a proper file editor that supports LF line endings.

For each wireless network that we would like to use, add the following lines:
```
network{
  ssid="Wifi name here"
  psk="Wifi password here"
}
```
Now simply save the file (CRTL+X if you used the `sudo nano` command) and restart the RPi. If set up correctly, the Raspberry Pi now connects to your wireless network! Just find the new local IP in the administrative console of your router and you can connect using a SSH client.


# Expanding the filesystem
The usual distribution images are 2 GB. When you copy the image to a larger SD card you have a portion of that card unused. This will quickly lead to issues where you run out of space. To fix this, the default raspbian image comes with a config tool. Start this config tool with the command
```
sudo raspi-config
```
There will simply be a option `Expand Filesystem `. Select this and reboot the Pi. Now pretty much most steps are completed that are needed to get started with the pi. Enjoy!
