# Suricata Guide

## Installation

```bash
sudo apt update
sudo apt install suricata
```

## Configuration

```bash
sudo suricata -c /etc/suricata/suricata.yaml -i <interface>
sudo suricata -c /etc/suricata/suricata.yaml -i enp0s8
```

## Update Rules

```bash
sudo suricata-update
```
## custom rules 
```bash
sudo nano /var/lib/suricata/rules/suircata.rules
```
## Test Suricata Rules
```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
```
##  Suricata Service

```bash
sudo systemctl start suricata
sudo systemctl enable suricata
```

## logs 

| File                       | Purpose         |
|----------------------------|-----------------|
| /var/log/suricata/eve.json | Main SOC log    |
| /var/log/suricata/fast.log | Quick alerts    |
| /var/log/suricata/stats.log| Performance     |
