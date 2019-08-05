import socket
import struct
import subprocess as sp
from threading import Thread


hosts = {}  # {ip: hostname}


def first_group():
    global sock1

    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    # Create the socket
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to the server address
    sock1.bind(server_address)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def second_group():
    global sock2

    multicast_group = '224.5.5.55'
    server_address = ('', 10000)

    # Create the socket
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to the server address
    sock2.bind(server_address)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock2.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


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
            sock1.sendto(str.encode('.../...' + message()), _multicast_group)
            print('\nHello message sent')
        else:
            sock1.sendto(str.encode(msg), _multicast_group)

    except Exception as e:
        print(e)


def send_message2(msg):
    _multicast_group = ('224.5.5.55', 10000)
    try:
        sock2.sendto(str.encode(msg), _multicast_group)

    except Exception as e:
        print(e)


def message():
    global hostname
    cmd = ['cat /etc/hostname']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    return hostname


def receive_message2():
    while True:
        data, address = sock2.recvfrom(1024)

        if data.decode()[:7] == '.../...':
            # print('received %s bytes from %s' % (len(data), address))
            hosts[address[0]] = data.decode()[7:]

        else:
            if address[0] != ip_address():
                print('group 2: ', data.decode())


def receive_message():
    while True:
        data, address = sock1.recvfrom(1024)

        if data.decode()[:7] == '.../...':
            # print('received %s bytes from %s' % (len(data), address))
            hosts[address[0]] = data.decode()[7:]
            if len(hosts) == mec:
                print('MEC Details: ', hosts)
        else:
            if address[0] != ip_address():
                print('group 1: ', data.decode())


def messaging_nodes():
    try:

        while True:
            msg = input()
            if (msg == '') or (msg == ' '):
                print('\n')
            elif msg[0] == '1':
                send_message(msg[2:])
            elif msg[0] == '2':
                send_message2(msg[2:])

    except KeyboardInterrupt:
        print('Programme Terminated')


def main():
    global mec
    first_group()
    second_group()
    try:
        mec = int(input('Number of Nodes: ').strip())
        print('\nCompiling All Neighbours Details')
        h1 = Thread(target=receive_message)
        h2 = Thread(target=receive_message2)
        h1.daemon = True
        h2.daemon = True
        h1.start()
        h2.start()
        if input('Send Hello Message (Y/N): ').strip().lower() == 'y':
            send_message('.../...')
        messaging_nodes()

    except KeyboardInterrupt:
        print('\nProgramme Terminated')
        exit(0)


main()




