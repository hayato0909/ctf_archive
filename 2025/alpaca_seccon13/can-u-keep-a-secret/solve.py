from pwn import *

elf = ELF('./challenge')
# io = process(elf.path)
io = remote('34.170.146.252', 59556)

io.recvuntil(b'secret: ')
secret = int(io.recvline().strip())
secret *= 0x5ec12e7

io.sendline(str(secret).encode())

io.interactive()

