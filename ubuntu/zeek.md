## Zeek Configuration

### 1. Node Configuration
```bash
sudo nano /opt/zeek/etc/node.cfg
```

Add node details:
```ini
[zeek]
type=standalone
host=localhost
interface=enp0s8
```

### 2. Network Configuration
```bash
sudo nano /opt/zeek/etc/networks.cfg
```

Add your network:
```text
10.10.10.0/24
```

### 3. Enable JSON Logs
```bash
sudo nano /opt/zeek/share/zeek/site/local.zeek
```

Add the following line at the end. This will help Zeek to generate JSON logs instead of the default log format (CSV) so that Splunk or any SIEM can parse and normalize it easily:
```zeek
@load policy/tuning/json-logs 
```

### 4. Zeek Management Tool

If you don't add the binary to your PATH, you must specify the full path:
```bash
sudo /opt/zeek/bin/zeekctl deploy
sudo /opt/zeek/bin/zeekctl stop
```

**Environment Configuration**
To make the Zeek CLI tool globally available:
```bash
nano ~/.bashrc
```

Add this line to `.bashrc`:
```bash
export PATH=$PATH:/opt/zeek/bin
```

Then you can use the tool directly:
```bash
zeekctl deploy
zeekctl stop
zeekctl status
```

### 5. Zeek Service
```bash
sudo systemctl enable zeek
sudo systemctl start zeek
```
