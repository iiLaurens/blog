Title: Installing Ubuntu on Intel Atom Devices
Slug: Ubuntu-on-Intel-Atom-Device
Date: 2017-07-10 19:46
Tags: Ubuntu, Beelink, Intel Atom, Install
Author: Laurens

A month or two ago I bought myself a new device to replace my faithfull Raspberry Pi 3. I made the change for several reasons. Among those reasons are the lack of RAM, the lack of supported video types, lack of USB 3 and the fact that the (slow) LAN port shared a controller with all USB ports. Don't get me wrong, the RPi3 is a great device, it just couldn't be the media server that I once hoped it to be. Hence, I got interested in cheap and low-powered Intel Atom devices. The [Beelink AP42](http://www.bee-link.com/Beelink-MiniPC-TV-BOX-66-1.html) caught my eye in particular due to it's fanless and therefore silent design. It would be the ultimate low-power media center.

After receiving this unit, I quickly realized that installing Linux would be quite the task. Pretty much all installation images of Linux distributions would not boot for reason that are still unclear to me. This was quite the bummer because manufacturers of these Intel Atom devices advertise Linux support. None of them actually provides the support themselves. After sinking plenty of hours in getting this little baby to work, I finally have a working Ubuntu system. In this blog post I will share the secret to the world so that everyone can enjoy these amazing devices to the fullest. This guide certainly works for installing Ubuntu to the Beelink AP42, but it will most likely work for similar Atom-based devices too (Beelink AP34, VOYO V1 Vmac).

# Preparing the installation image
One should start with downloading the official Ubuntu image. Another Ubuntu flavour should work *in theory*, however I found that in other distro's that the HDMI audio passtrough would not work. If audio over HDMI is not a concern to you and you can use the audiojack instead, then go ahead. In any other case, I recommend starting with the full Ubuntu distro and then replace the default unity desktop with the desktop of another distro (Xubuntu, Lubuntu, ...) using the package manager.

Once you have chosen a version(Ubuntu 17.04 in my case). The default boot manager in these ISO's fail to load on Intel Atom devices and one should resort to either rEFInd or syslinux as a boot manager. In addition a newer kernel version is required for proper HDMI audio support. This sounded like a daunting task to me, but [Linuxium](http://linuxiumcomau.blogspot.com/) has made an amazing script named *isorespin.sh* that does most of the work. The complete package (but without the clean ISO), including some audio, WiFi and Bluetooth drivers, can be downloaded from [here](https://ilaurens.stackstorage.com/s/E8cwo4BtIYnnJk2). Simply put all the files in the folder and run from a root shell (`sudo -i`) the following:
```
# Make scripts executable
chmod u+x isorespin.sh linuxium-install-UCM-files.sh linuxium-install-broadcom-drivers.sh wrapper-linuxium-install-UCM-files.sh wrapper-linuxium-install-broadcom-drivers.sh

# Now for the actual respinning
./isorespin.sh -i ubuntu-17.04-desktop-amd64.iso -l rtl8723bs_4.12.0_amd64.deb -f linuxium-install-UCM-files.sh -f wrapper-linuxium-install-UCM-files.sh -f linuxium-install-broadcom-drivers.sh -f wrapper-linuxium-install-broadcom-drivers.sh -c wrapper-linuxium-install-UCM-files.sh -c wrapper-linuxium-install-broadcom-drivers.sh -s 256MB -k v4.11'
```
Note however that the respinning is done on an Ubuntu distribution itself, as I found that spinning the ISO on an Lubuntu distro results in unbootable ISO's as well. I spare you from all the effort that goes into this spinning and instead offer you [this image](https://mega.nz/#!bM8hESrY). Make sure to *dd* this to an USB stick (again I recommend to use Ubuntu or a Ubuntu VM). The command should be `dd if=linuxium-persistence-v4.11-Ubuntu-17.04-desktop-amd64.iso of=\dev\sdX bs=4M`. Make sure to replace `sdX` with the correct reference to your USB device. After a succesfull copy simply boot the Live USB on your Intel Atom device (Press *F7* during for a boot menu) and start the installation.

# Making your fresh Ubuntu installation bootable
If you try to boot your freshly installed OS from your internal storage, you will be sorely dissapointed. The OS is installed with the same erroneous bootloader that was present on the official ISO file. Yikes! We now need to change the boot configuration manually. Simply launch the Live USB again. We will simply recycle the rEFInd boot manager from the USB device (with some minor adjustments). The following commands will effectively copy the boot manager. Just make sure to replace `/dev/sda1` with the proper reference to the first partition of your USB device. Similarly, replace `/dev/mmcblk1p1` with the name for your internal storage's first partition.
```
# Create mountpoints for the EFI boot partitions of the internal storage and USB
mkdir /mnt/bootusb
mkdir /mnt/bootdisk
mount /dev/sda1 /mnt/bootusb
mount /dev/mmcblk1p1 /mnt/bootdisk

# Remove the existing files from the internal hard drive's EFI partition
rm -r /mnt/bootdisk
# Now copy the rEFInd bootloader from the USB to our internal storage
cp -r /mnt/bootusb/EFI /mnt/bootdisk

# Point the EFI boot system where to look for the new bootloader and make it the first boot option
efibootmgr -c -l \\EFI\\boot\\bootx64.efi -L rEFInd -d /dev/mmcblk1 -b 1234
efibootmgr -o 1234

# Now repair some rEFInd settings so that our system immediately boots the first OS it finds (Ubuntu). No graphics for more speed.
sed -i 's/^scanfor manual$/scanfor internal/' /mnt/bootdisk/EFI/boot/refind.conf
sed -i 's/^timeout 20$/timeout -1/' /mnt/bootdisk/EFI/boot/refind.conf
sed -i 's/^#textonly$/textonly/' /mnt/bootdisk/EFI/boot/refind.conf
```

After running these commands you can remove the USB stick and restart the device. That is all there is to it. Now you can experience the joy of Linux on your Intel Atom device!
