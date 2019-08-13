import socket
import struct


def getOutgoingInterface(self):
    i = self.socket.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF)
    return socket.inet_ntoa(struct.pack("@i", i))


def _setInterface(self, addr):
    i = socket.inet_aton(addr)
    self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, i)
    return 1


def create_multicast_sock(own_ip, remote_addr, bind_to_multicast_addr):
        """Create UDP multicast socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)

        sock.setsockopt(
            socket.SOL_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(own_ip))
        sock.setsockopt(
            socket.SOL_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(remote_addr[0]) +
            socket.inet_aton(own_ip))
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_TTL, 2)
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(own_ip))

        # I have no idea why we have to use different bind calls here
        # - bind() with multicast addr does not work with gateway search requests
        #   on some machines. It only works if called with own ip.
        # - bind() with own_ip does not work with ROUTING_INDICATIONS on Gira
        #   knx router - for an unknown reason.
        if bind_to_multicast_addr:
            sock.bind((remote_addr[0], remote_addr[1]))
        else:
            sock.bind((own_ip, 0))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        return sock


def subscribe_multicast(interface):
    """subscribe to the mcast addr"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface.ipv4_address))
    mreq = socket.inet_aton(interface.mcastaddr) + socket.inet_aton(interface.ipv4_address)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.bind(('', 52122))

    return sock


def set_ipv4_multicast_source_address(sock, source_address):
    """Sets the given socket up to send multicast from the specified source.

    Ensures the multicast TTL is set to 1, so that packets are not forwarded
    beyond the local link.

    :param sock: An opened IP socket.
    :param source_address: A string representing an IPv4 source address.
    """
    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
        socket.inet_aton(source_address))