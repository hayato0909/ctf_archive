from pwn import *

elf = ELF('./challenge/no_gadgets')
io = process(elf.path)
context.binary = elf

