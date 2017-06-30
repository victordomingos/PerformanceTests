#!/usr/bin/env python3.6
# encoding: utf-8
"""
Test some different ways to determine external IP and see how much time it takes.
 
© 2017 Victor Domingos
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import platform    
import sys
from timeit import default_timer as timer

print(platform.python_implementation())
print(sys.version)


# Get current IP (method 1)
# Needs this: https://github.com/phoemur/ipgetter
start = timer()
import ipgetter
current_ip = ipgetter.myip()
print(current_ip)
end = timer()
delta1 = end - start


# Get current IP (method 2)
start = timer()
import requests
current_ip = requests.get('https://api.ipify.org').text
print(current_ip)
end = timer()
delta2 = end - start


# Get current IP and approximate location (method 3)
# Thanks to Jishnu Mohan & Kuba Jeziorny for the tip
start = timer()
import requests, datetime
myinfo = requests.get("http://freegeoip.net/json").json()
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"{now} - {myinfo['ip']} - {myinfo['city']} ({myinfo['country_code']})")
end = timer()
delta3 = end - start


print('---')
print('ipgetter:', delta1)
print('ipify.org:', delta2)
print('freegeoip:', delta3)
