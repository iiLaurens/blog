Title: Initializing the Raspberry Pi 3 Part II
Slug: Initializing-the-raspberry-pi-3-part-II
Date: 2016-10-05 20:15
Tags: Raspberry Pi 3, Settings
Author: Laurens

Here I will be updating some of my adventures with my RPi3. I will be pushing SSH keys for secure connecting and I will set up how to boot from USB. I also assume that we are working on *bash on ubuntu for windows*.

# Programming USB boot mode
Next up is programming the Pi to boot from the USB. This is now supported in the newest releases of raspbian, but only for the Raspberry Pi 3. This special mode completely removes the need for having a SD card inserted.

First, prepare the `/boot` directory with experimental boot files:

```
# If on raspbian lite you need to install rpi-update before you can use it:
$ sudo apt-get update; sudo apt-get install rpi-update
$ sudo BRANCH=next rpi-update
```
Then enable USB boot mode with this code:
```
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```
Reboot the Pi with sudo reboot, then check that the OTP has been programmed with:
```
$ vcgencmd otp_dump | grep 17:
17:3020000a
```
Ensure the output `0x3020000a` is correct.

If you wish, you can remove the `program_usb_boot_mode` line from config.txt (make sure there is no blank line at the end) so that if you put the SD card in another Pi, it won't program USB boot mode. You can do this with `sudo nano /boot/config.txt`, for example.

# Preparing the USB storage device
We will start by using Parted to create a 100MB FAT32 partition, followed by a Linux ext4 partition that will contain the Raspbian distribution. Additionally I wanted two NTFS drives myself that serve as datawarehouses and network drives for my desktop computer.

First, make sure that NTFS support is installed.
```
sudo apt-get install ntfs-3g
```
Then format the USB drive to our needs.
```
sudo parted /dev/sda

(parted) mktable msdos
Warning: The existing disk label on /dev/sda will be destroyed and all data on this disk will be lost. Do you want to
continue?
Yes/No? Yes
(parted) mkpart primary fat32 0% 100M
(parted) mkpart primary ext4 100M 10G
(parted) mkpart primary ntfs 10G 610G
(parted) mkpart primary ntfs 610G 100%
(parted) print
Model: SAMSUNG HD154UI (scsi)
Disk /dev/sda: 1500GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  99.6MB  98.6MB  primary  fat32        lba
 2      99.6MB  10.0GB  9901MB  primary  ext4         lba
 3      10.0GB  610GB   600GB   primary  ntfs         lba
 4      610GB   1500GB  890GB   primary  ntfs         lba
```
Your parted print output should look similar to the one above.

Create the boot and root file systems:
```
sudo mkfs.vfat -n BOOT -F 32 /dev/sda1
sudo mkfs.ext4 /dev/sda2
sudo mkfs.ntfs /dev/sda3 -f
sudo mkfs.ntfs /dev/sda4 -f
```
Mount the target file system and copy the running raspbian system to it:
```
sudo mkdir /mnt/target
sudo mount /dev/sda2 /mnt/target/
sudo mkdir /mnt/target/boot
sudo mount /dev/sda1 /mnt/target/boot/
sudo apt-get update; sudo apt-get install rsync
sudo rsync -ax --progress / /boot /mnt/target
```
Regenerate ssh host keys:
```
cd /mnt/target
sudo mount --bind /dev dev
sudo mount --bind /sys sys
sudo mount --bind /proc proc
sudo chroot /mnt/target
rm /etc/ssh/ssh_host*
dpkg-reconfigure openssh-server
exit
sudo umount dev
sudo umount sys
sudo umount proc
```
Edit /boot/cmdline.txt so that it uses the USB storage device as the root file system instead of the SD card.
```
sudo sed -i "s,root=/dev/mmcblk0p2,root=/dev/sda2," /mnt/target/boot/cmdline.txt
```
The same needs to be done for fstab:
```
sudo sed -i "s,/dev/mmcblk0p,/dev/sda," /mnt/target/etc/fstab
```
Finally, unmount the target file systems, and power the Pi off.
```
cd ~
sudo umount /mnt/target/boot
sudo umount /mnt/target
sudo poweroff
```
Disconnect the power supply from the Pi, remove the SD card, and reconnect the power supply. If all has gone well, the Pi should begin to boot after a few seconds.

# Passwordless access using SSH keys
If your Pi does not have an .ssh directory you will need to set one up so that you can copy the key from your computer.
```
cd ~
install -d -m 700 ~/.ssh
```
To copy your public key to your Raspberry Pi, use the following command to append the public key to your authorized_keys file on the Pi, sending it over SSH. First exit the pi using `logout`. Then from your linux (or ubuntu for windows) distribution transfer the keys:
```
cat ~/.ssh/id_rsa.pub | ssh <username>@<address of RPi> "cat >> .ssh/authorized_keys"
```
Now if you have the correct `id_rsa` in your (non-RPi) OS in the `.ssh` folder, then logging into the RPi should not ask for a password again!

Disallowing password login. To disallow password login we need to edit the ssh config found in /etc/ssh/sshd_config. Do do this we can ssh into the Pi. Once at the prompt we can enter the following:
```
sudo nano /etc/ssh/sshd_config
```
scroll down to the section that says `#PasswordAuthentication yes` and uncomment it to no. Save it using `CTRL+X`.

From now on it is only possible to login on the RPi using the correct SSH keys!
