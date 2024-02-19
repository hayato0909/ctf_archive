from pwn import *

elf = ELF('./challenge')
libc = ELF('./ld-linux-x86-64.so.2')
io = process(elf.path)
context.binary = elf

# get hint
io.sendlineafter(b'>> ', b'1')
io.recvuntil(b'0x')
hint_addr = int(io.recv(12), 16)
io.recvuntil(b'0x')
fget_addr = int(io.recv(12), 16)

log.info(f'hint_addr: {hex(hint_addr)}')
log.info(f'fget address: {hex(fget_addr)}')

io.interactive()

