Title: Automatic port forwarding in deluge with VPN
Slug: automatic-port-forwarding-deluge-pia
Date: 2017-08-20 21:10
Tags: VPN, Private Internet Access, Deluge, Port forwarding
Author: Laurens

To improve the performance of torrents, it is recommended to open ports so that swarm can connect with you. Unfortunately not many VPN providers allow port forwarding. PIA (Private Internet Access) is one of the few that does, and I recently switched to them. In this guide I will explain how to enable port forwarding in Deluge using openVPN and PIA.

# Setting up the script
Start by going to your openVPN folder `\etc\openvpn\`. I assume that you have set up your openVPN and deluge according to [this post of mine]({filename}/2016/Turning a RPi3 into a data center.md). Hence, you should already have the applications `deluge-console` and know your deluge credentials.

Start by creating a file `portforward.sh`:
```
#!/usr/bin/env bash
# Adapted from https://github.com/blindpet/piavpn-portforward/
# Based on https://github.com/crapos/piavpn-portforward

# Set path for root Cron Job
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

USERNAME=piauser
PASSWORD=piapass
VPNINTERFACE=tun0
VPNLOCALIP=$(ifconfig $VPNINTERFACE | awk '/inet / {print $2}' | awk 'BEGIN { FS = ":" } {print $(NF)}')
CURL_TIMEOUT=5
CLIENT_ID=$(uname -v | sha1sum | awk '{ print $1 }')

DELUGEUSER=delugeuser
DELUGEPASS=delugepass
DELUGEHOST=localhost

#get VPNIP
VPNIP=$(curl -m $CURL_TIMEOUT --interface $VPNINTERFACE "http://ipinfo.io/ip" --silent --stderr -)
echo $VPNIP

#request new port
PORTFORWARDJSON=$(curl -m $CURL_TIMEOUT --silent --interface $VPNINTERFACE  'https://www.privateinternetaccess.com/vpninfo/port_forward_assignment' -d "user=$USERNAME&pass=$PASSWORD&client_id=$CLIENT_ID&local_ip=$VPNLOCALIP" | head -1)
#trim VPN forwarded port from JSON
PORT=$(echo $PORTFORWARDJSON | awk 'BEGIN{r=1;FS="{|:|}"} /port/{r=0; print $3} END{exit r}')
echo $PORT  

#change deluge port on the fly
deluge-console "connect $DELUGEHOST:58846 $DELUGEUSER $DELUGEPASS; config --set listen_ports ($PORT,$PORT)"
```
You should replace the `USERNAME`, `PASSWORD`, `DELUGEUSER` and `DELUGEPASS` fields in accordance with your setup and PIA account. Also do not forgot to make this file executable.
```
sudo chmod +x portforward.sh
```

# Testing the setup
Now we will test the script. First ensure that Deluge does not user random ports in the settings by accessing the Network tab in the settings of your Deluge client. After that you can test the script:
```
sudo bash portforward.sh
```
If successful it will print your VPN IP and port and shows no error. You can test if your port is correctly forwarding with the *test active port* button in the network settings of your Deluge thin client. The picture below illustrates what you should be looking at during testing.

![deluge]({filename}/images/delugeportsettings.PNG)

# Automating using Cron
If everything worked out, the last step is to regularly call the script we just created. For this we will use a Cron Job.
```
sudo crontab -e
```
and insert the following lines:
```
@reboot sleep 60 && /etc/openvpn/portforward.sh | while IFS= read -r line; do echo "$(date) $line"; done #PIA Port Forward
0 */2 * * * /etc/openvpn/portforward.sh | while IFS= read -r line; do echo "$(date) $line"; done  #PIA Port Forward
```
And now it should run after each reboot and every two hours afterwards.

Credits to [htpcguides](https://www.htpcguides.com/configure-auto-port-forward-pia-vpn-for-deluge/) for this setup!
