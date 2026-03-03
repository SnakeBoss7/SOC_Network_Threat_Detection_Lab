import requests

ip_address = 10.10.10.2
path= "http://" + ip_address 
uri = ["/checkin","/heartbeat","/task"]
while True:
    requests.get(uri)