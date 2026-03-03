# Incident Report: Suspected C2 HTTP Beaconing

## Summary
- Incident ID: IR-001
- Date: 03/03/2026
- Severity: Critical (P1)
- Status: Confirmed Malicious
- Analyst: Rahul dharwal

## 1. Alert Trigger
What alert fired and from which tool?

- Splunk alert triggered on Zeek HTTP logs
- SPL query detected low coefficient of variance (< 0.3) 
  between a source and destination IP pair
- Beaconing interval: ~10 seconds
- Request count: 114 requests in 10 hours

## 2. Investigation / Triage
Step 1: Verified the source IP (10.10.10.5 — Windows victim) 

Step 2: Verified the destination IP (10.10.10.2 — Kali/attacker)

Step 3: Checked the URIs being hit → /checkin, /heartbeat, /task
        (These are not normal browsing patterns)

Step 4: Checked User-Agent → "python-requests/2.28"
        (Not a browser — automated script)

Step 5: Checked Suricata logs for any signature-based alerts
        on the same IP pair, `found a SYN port scan and a ssh brute force attempt right after that`
        
Step 6: Checked if destination IP is a known/internal server → 
        Destination ip is internal thus its a `insider threat` or someone in out internal network

## 3. Findings / Indicators of Compromise (IOCs)
| IOC Type | Value |
|----------|-------|
| Source IP | 10.10.10.5 |
| Destination IP | 10.10.10.2 |
| Destination Port | 8080 |
| URIs | /checkin, /heartbeat, /task |
| User-Agent | python-requests/2.28 |
| Beacon Interval | ~10 seconds |
| Protocol | HTTP (unencrypted) |

## 4. Impact Assessment
- Compromised host: Windows 10 victim machine
- The malware is actively calling back to a C2 server
- Threat is `insider threat` or someone is our internal network
- Potential for data exfiltration, remote command execution
- No lateral movement detected (yet)

## 5. Recommended Response / Containment
- Immediately isolate the victim machine from the network
- Block destination IP 10.10.10.2 at the firewall
- Identify and kill the malicious process on the victim
- Check for persistence mechanisms (startup scripts, 
  scheduled tasks)
- Scan the victim with endpoint detection tools
- Monitor for the same IOCs across other machines

## 6. Lessons Learned
- Signature-based detection (Suricata) alone would have 
  missed this — no malicious payload signature to match
- Behavioral detection via Zeek + Splunk caught it through 
  statistical analysis of request intervals
- Unencrypted HTTP C2 is easy to detect; real attackers 
  would use HTTPS, DNS tunneling, or domain fronting
