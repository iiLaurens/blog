Title: Turning a Raspberry Pi 3 into a secure torrent box
Slug: RPi3-torrent-box
Date: 2016-10-05 23:16
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
cat > auth.tdxt << EOF
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
Now this is where things get tricky, and I hardly have a clue what I am doing. All I can tell is that this appears to work for me.

First, start by marking packets that originate from the `deluge` user.
```
iptables -t mangle -A OUTPUT -m owner --uid deluge -j MARK --set-mark 1
iptables -t nat -A POSTROUTING -m mark --mark 1 -j MASQUERADE
```
Next at an ip rule that tells which route table to look at for the marked packets.
```
ip rule add fwmark 0x1 table 100
```
Now we have to specify the actual routing table that we just referred to. First let's take a look at the current routing table.
```
$ ip route
0.0.0.0/1 via 10.6.0.120 dev tun0
default via 192.168.30.1 dev eth0  metric 202
10.6.0.120 dev tun0  proto kernel  scope link  src 10.6.0.119
128.0.0.0/1 via 10.6.0.120 dev tun0
176.127.251.72 via 192.168.30.1 dev eth0
192.168.30.0/24 dev eth0  proto kernel  scope link  src 192.168.30.215  metric 202
```
So these are the settings that make OpenVPN work for my VPN provider (I edited some IP addresses just to be safe). The idea behind ip routes is that the kernel chooses the most specific match. OpenVPN pulls all the traffic to the gateway `10.6.0.120` because it splits the general 0.0.0.0/0 into two slightly more specific but collectively exhaustive ranges. Namely it targets 0.0.0.0/1 and 128.0.0.0/1 (which together encompass the entire IPv4 address space). To prevent OpenVPN from pulling all traffic through the `tun0` interface, we have to delete these rules. First let's isolate the two lines.

```
$ ip route | grep -P '[0-9]+\.0\.0\.0/1'
0.0.0.0/1 via 10.6.0.120 dev tun0
128.0.0.0/1 via 10.6.0.120 dev tun0
```
**It is important that you write down these two lines as we need them later to recover the VPN connection!**
Now delete these two routes
```
sudo ip route del 0.0.0.0/1 via 10.6.0.120 dev tun0
sudo ip route del 128.0.0.0/1 via 10.6.0.120 dev tun0
```
Next we add them under our alternative route table by adding the suffix `table 100`.
```
sudo ip route add 0.0.0.0/1 via 10.6.0.120 dev tun0 table 100
sudo ip route add 128.0.0.0/1 via 10.6.0.120 dev tun0 table 100
```
Finally, we want to build a kill switch so that deluge can only use VPN and nothing else, so that it cannot go over the default `eth0` connection.
```
sudo iptables -A OUTPUT -m owner --uid-owner deluge \! -o tun0 -j REJECT
sudo iptables -A OUTPUT -m owner --uid-owner deluge -d 192.168.31.0/24 -j ACCEPT
```
