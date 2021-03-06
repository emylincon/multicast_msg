import socket
import struct
import subprocess as sp
from threading import Thread


hosts = {}  # {hostname: ip}
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind to the server address
sock.bind(server_address)
# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def send_message():
    _multicast_group = ('224.3.29.71', 10000)
    try:

        # Send data to the multicast group
        # print('sending "%s"' % message())
        sent = sock.sendto(str.encode(message()), _multicast_group)
        print('\nmessage sent')

    except Exception as e:
        print(e)


def message():
    cmd = ['cat /etc/hostname']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    return hostname


def receive_message():
    while True:
        data, address = sock.recvfrom(1024)

        # print('received %s bytes from %s' % (len(data), address))
        hosts[data.decode()] = address[0]
        if len(hosts) == mec:
            print('MEC Details: ', hosts)


def main():
    global mec
    try:
        mec = int(input('Number of Nodes: ').strip())
        print('\nCompiling MEC Details')
        h1 = Thread(target=receive_message)
        h1.start()
        if input('Type "Y" to Start: ').strip().lower() == 'y':
            send_message()
    except KeyboardInterrupt:
        print('\nProgramme Terminated')
        exit(0)


main()




