# Network Configuration for this lab
## Ubuntu Router Setup Guide

This guide configures an Ubuntu server to act as a router, providing internet access to a client machine (e.g., Windows 11) on an internal LAN.

## Step 1: Network Interface Configuration

Ensure the Ubuntu server has two Network Interfaces (NICs):

1.  **WAN Interface (Internet):** Connected to the host via NAT (e.g., `libvirt` NAT).
2.  **LAN Interface (Internal):** Connected to the internal network (LAN) to serve the "victim" or client machine.

*Tip: Check your interface names using `ip a` (e.g., `enp0s3`, `enp0s8`).*

## Step 2: Configure Netplan 

Configure the network interfaces with static IP for the LAN and DHCP for the WAN.

**1. Edit the Netplan configuration:**
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

**2. Configure the network:**
Use the structure below. Ensure indentation is correct (YAML is sensitive to spaces).
*   `enp0s3`: WAN/Internet interface (DHCP).
*   `enp0s8`: LAN/Internal interface (Static IP).

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses:
        - 192.168.50.1/24
```

**3. Apply changes:**
```bash
sudo netplan apply
```

**4. Verify configuration:**
```bash
ip a
```
*You should see `enp0s8` is UP with IP `192.168.50.1/24`.*

## Step 3: Enable IP Forwarding

This allows the Ubuntu kernel to forward packets between the two interfaces.

**1. Enable temporarily:**
```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

**2. Verify status:**
```bash
cat /proc/sys/net/ipv4/ip_forward
```
*Output should be `1`.*

**3. Make it permanent:**
Edit the sysctl configuration:
```bash
sudo nano /etc/sysctl.conf
```
Add or uncomment the following line:
```ini
net.ipv4.ip_forward=1
```
Save and apply changes:
```bash
sudo sysctl -p
```

## Step 4: Configure NAT (Masquerading)

Enable Network Address Translation (NAT) to allow the LAN client to access the internet through the Ubuntu server.

*Replace `enp1s0` with your **WAN/Internet** interface.*
*Replace `enp7s0` with your **LAN/Internal** interface.*

```bash
# Mask outgoing traffic as coming from the WAN interface
sudo iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE

# Allow forwarding from LAN to WAN
sudo iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT

# Allow return traffic for established connections
sudo iptables -A FORWARD -i enp0s3 -o enp0s8 -m state --state RELATED,ESTABLISHED -j ACCEPT
```


## Kali linux
```
#temporary
ip addr add 10.10.10.20 dev eth0
sudo ip link set eth0 up
ip route default via 10.10.10.1 dev eth0

#persistant
nmcli con mod eth0 ipv4.addresses 10.10.10.20/24
nmcli con mod eth0 ipv4.gateway 10.10.10.1
nmcli con mod eth0 ipv4.method manual
nmcli con up eth0
```

Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.7.5-1.msi -OutFile
${env.tmp}\wazuh-agent; msiexec.exe /i ${env.tmp}\wazuh-agent /q WAZUH_MANAGER='10.10.10.1'
WAZUH_AGENT_NAME='Win10' WAZUH_REGISTRATION_SERVER='10.10.10.1'