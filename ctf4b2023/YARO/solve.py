from pwn import *

host = 'yaro.beginners.seccon.games'
port = 5003
io = remote(host, port)

flag = "ctf4"
c = 'b'
yara_rule = f"""rule flag {{
    strings:
        $flag = "{flag}{c}"
    condition:
        $flag
}}"""

io.sendlineafter('rule:', yara_rule)
io.sendline('')

s = io.recvall().decode()
if 'Found' in s:
    print(flag)
