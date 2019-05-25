import socket
import struct
import subprocess as sp
from threading import Thread


hosts = {}  # {ip: hostname}
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


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def send_message(msg):
    _multicast_group = ('224.3.29.71', 10000)
    try:
        if msg == '.../...':
            # Send data to the multicast group
            # print('sending "%s"' % message())
            sock.sendto(str.encode('.../...' + message()), _multicast_group)
            print('\nHello message sent')
        else:
            sock.sendto(str.encode(msg), _multicast_group)

    except Exception as e:
        print(e)


def message():
    global hostname
    cmd = ['cat /etc/hostname']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    return hostname


def receive_message():
    while True:
        data, address = sock.recvfrom(1024)

        if data.decode()[:7] == '.../...':
            # print('received %s bytes from %s' % (len(data), address))
            hosts[address[0]] = data.decode()[7:]
            if len(hosts) == mec:
                print('MEC Details: ', hosts)
        else:
            if address[0] != ip_address():
                print('{}: {}'.format(hosts[address[0]], data.decode()))


def messaging_nodes():
    try:

        while True:
            msg = input('{}: '.format(hostname))
            if (msg == '') or (msg == ' '):
                print('\n')
            else:
                print('{}: {}'.format(hostname, msg))
                send_message(msg)

    except KeyboardInterrupt:
        print('Programme Terminated')


def main():
    global mec
    try:
        mec = int(input('Number of Nodes: ').strip())
        print('\nCompiling All Neighbours Details')
        h1 = Thread(target=receive_message)
        h1.start()
        if input('Send Hello Message (Y/N): ').strip().lower() == 'y':
            send_message('.../...')
        messaging_nodes()

    except KeyboardInterrupt:
        print('\nProgramme Terminated')
        exit(0)


main()




