Title: Turning a Raspberry Pi 3 into a secure torrent box
Slug: RPi3-torrent-box
Date: 2016-11-15 23:10
Tags: Raspberry Pi 3, Settings
Author: Laurens

I will be discussing some of the applications I have been using on my raspberry pi to turn it into a low power torrent that can always stay powered on. It serves as a torrent box with *Deluge*, which I can control remotely from one of my desktop computers using deluge's *thin client*. I will also show how to connect deluge through a secure VPN tunnel such that all torrenting traffic is safely encrypted whilst the rest of the Raspberry Pi's traffic can travel through regular channels.

# Confuguring OpenVPN
Start with installing openVPN
```
sudo apt-get install openvpn
```
To get the client up and running, I expect that you already are subscribed to some VPN service provider. Most providers have configuratoin files available that are ready to be used with OpenVPN. Obtain the download URL of these settings from your provider and put it in `/etc/openvpn`:
```
cd /etc/openvpn
sudo wget <url here>
```
My service provider happened to have multiple configuration available for several VPN servers. These files are all contained in a zip, hence I unzip them. Notice that I also rename the files to a `.conf` extension as mine originally came in a `.ovpn` format. The rename command is thus optional.
```
sudo unzip <filename>
sudo rename "s/.ovpn/.conf/" *.ovpn
```
Acces to VPN servers is often password protect. The configuration files generally do not include your personal password and username so we have to add them ourselves. Drop your username and password into a file named `auth.txt`:
```
sudo cat << EOF | sudo tee auth.txt
username
password
EOF
```
Now we have edit our VPN's configuration files to include a reference to our authorization file.
```
sudo sed -i 's/auth-user-pass/auth-user-pass auth.txt/' *.conf
```
The above command replaces every occurance of `auth-user-pass` with `auth-user-pass auth.txt`. If your configuration file did not include a `auth-user-pass` line then you have to append it yourself. Finally see if is working correctly using a
```
curl https://jsonip.com
sudo openvpn --daemon --config /etc/openvpn/<file>.conf
curl https://jsonip.com
```
Note that the curl commands should return ip addresses. It should show two different IP addresses before and after starting OpenVPN. If this works, we are all set!

# Installing Deluge
To install deluge, start with installing the `deluged` package, which is the daemon package of deluge (so without the front-end as we are running it from a terminal).
```
sudo apt-get install deluged
sudo apt-get install deluge-console
```
First of all, we want deluge to operate from a seperate user so that later we can redirect it's traffic by user ID. We start by creating a new user named `deluge`:
```
sudo adduser deluge
```
Next, we have to start deluge once under the deluge username to create all the configuration files. The -u after the sudo command tells our Pi to run this operations as the `deluge` user.
```
sudo -u deluge deluged
sudo pkill deluged
```
Now we can create a custom username and password so we control the deluge app remotely.
```
sudo nano /home/deluge/.config/deluge/auth
```
Once inside nano, you’ll need to add a line to the configuration file in the following format:
```
user:password:10
```
The final number 10 defines the rights of the user (in which case 10 implies the full-access/administrative level). When you’re done editing, hit CTRL+X and save your changes. Once you’ve saved them, start up the daemon again and enter the deluge-console:
```
sudo -u deluge deluged
sudo -u deluge deluge-console
```
Once you’re inside the console, we need to make a quick configuration change to enable remote access. Enter the following:
```
config -s allow_remote True
exit
```
Now it’s time to kill the daemon and restart it one more time so that the config changes take effect:
```
sudo pkill deluged
sudo -u deluge deluged
```
Now deluge should be ready to accept connections from the *Thin Client*! To connect, simply enter the ip address of you Raspberry pi and the credentials you created earlier.

# Restrict torrenting traffic to use only the VPN connection
What OpenVPN does by default is pull all traffic over the tunnel it creates. I only wanted my torrent traffic to use the VPN. Now this is where things took me a long time to figure out. Networking is just pretty confusing stuff for someone that never really bothered with it. However, I was able to solve it in the following way:

First, we move to the openvpn directory again and make sure openvpn and deluged are not running.
```
cd /etc/openvpn
sudo pkill deluged
sudo pkill openvpn
```
Now we need to change the confuguration file a bit so we stop openvpn from pulling all traffic to the tunnel.
```
sudo sed -i 's/client/client\nroute-noexec\nroute-up route-up.sh/' *.conf
```
But this also means we have to add the correct routes for our internet packages as well. For this, we can create the `route-up.sh` file. Create the file using
```
sudo nano route-up.sh
```
Paste the following contents and save with `ctrl+x`. Please note that I assume that the default internet uses the `eth0` interface. If it is not, then you should replace each occurence with your specific interface (for example `wlan0`).
```
#!/bin/bash

echo "Delete any pre-existing rules"
# It's okay if we get errors if the rules were not found.
# The end goal is to not have these rules so it's fine.
ip route flush table 111
iptables -t mangle -D OUTPUT -m owner --uid deluge -j MARK --set-mark 1
iptables -t nat -D POSTROUTING -m mark --mark 1 -j MASQUERADE
ip rule del fwmark 0x1 table 111

echo "Applying routes"
iptables -t mangle -A OUTPUT -m owner --uid deluge -j MARK --set-mark 1
iptables -t nat -A POSTROUTING -m mark --mark 1 -j MASQUERADE
ip rule add fwmark 0x1 table 111

ip route add 0.0.0.0/1 via $route_vpn_gateway dev $dev table 111
ip route add 128.0.0.0/1 via $route_vpn_gateway dev $dev table 111
ip route add $(echo $route_net_gateway | sed 's/\.[0-9]*$/.0/')/24 dev eth0  proto kernel  scope link \
  src $(ifconfig eth0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)  metric 202  table 111
ip route add blackhole default table 111
ip route flush cache
```
The script does a couple of things. First, it deletes any pre-existing rules that might be created if you restart OpenVPN in the future. After that, I add multiple filters and routes. First I mark all packets that originate from the `deluge` user, which is who will be running the torrent daemon. Then, we tell the kernel to use a different routing table if a outward destined packet is marked. I finish by generating the routes for table 111. The first two `ip route add` commands just define the tunnel to our VPN server. The third makes sure that everything that is destined for the local network does not go through the tunnel but over the local network. Finally, a black hole is added. If the connection with the VPN server drops for whatever reason, then the tunnel routes will dissapear. In that case, packets will end up in the blackhole and can not secretly exit through our local network. This is *killswitch* to make sure no torrent traffic leaves the Raspberry Pi unsecured.

Finally we have to make the file executable by everyone.
```
sudo chown root route-up.sh
sudo chmod +x route-up.sh
```
Now we can test whether everything works fine. First start OpenVPN.
```
sudo openvpn --daemon --config /etc/openvpn/<file>.conf
```
And test that it works.
```
curl http://jsonip.com
sudo -u deluge curl http://jsonip.com
```
Both commands should return a different IP, as one is run by you as an user, and the other is run by the `deluge` user. If you pass this test, then we can start deluge
```
sudo -u deluge deluged
```
If everything is allright, you should be able to connect to deluge using your client over the local network, but the actual torrent traffic is tunneled over the VPN. That's it!
