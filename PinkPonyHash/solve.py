#!/usr/bin/env python3
from base64 import b64encode
import hlextend
import requests
import re

'''
This challenge involved a SHA-1 length extension attack
Some silly maths behind this one, but thanks to this github repo we easily conduct the attack and snatch our flag

https://github.com/stephenbradshaw/hlextend
'''

sha = hlextend.new("sha1")
payload = sha.extend(b"pink_pony", b"kitty_cat", 19, "8665c860a93878c794775cafcafeea6e9f05476a")
_hash = sha.hexdigest()

token = b64encode(payload) + b"." + _hash.encode()
print("token=" + token.decode())

url = "https://uscybercombine-s4-ffctf-pink-pony-hash.chals.io/"
cookies = {'token': token.decode()}
r = requests.get(url, cookies=cookies)
print(re.search(r"FFCTF\{.*\}", r.text).group())
