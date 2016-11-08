Title: Initializing the Raspberry Pi 3 Part II
Slug: Initializing-the-raspberry-pi-3-part-II
Date: 2016-10-05 20:15
Tags: Raspberry Pi 3, Settings
Author: Laurens

Here I will be updating some of my adventures with my RPi3. In this episode, I will be pushing SSH keys for secure connecting and I will set up how to boot from USB. I also assume that we are working on *bash on ubuntu for windows*.

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
