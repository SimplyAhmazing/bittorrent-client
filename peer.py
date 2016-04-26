import socket
from torrent import Torrent
import struct

from bitstring import BitArray


class Peer(object):
    def __init__(self, torrent : Torrent, peer_info : (str, int)):
        self.torrent = torrent
        self.peer_info = peer_info

        self.sock = None
        self.handshake = ''
        self.is_connected = False

        self.state = None
        self.is_interested = False
        self.am_interested = False
        self.am_chocking = True
        self.is_interested = False

        self.msg_queue = []

        self.pieces = BitArray(bin='0' * self.torrent.num_pieces)


    def is_handshake_valid(self, handshake : bytes, resp : bytes):
        """
        <pstrlen><pstr><reserved><info_hash><peer_id>
        """
        return handshake[28:48] == resp[28:48]


    def connect(self):
        handshake = self.torrent.get_handshake()

        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)

        try:
            print('peer info is ', self.peer_info)
            sock.connect(self.peer_info)
            sock.send(handshake)
        except OSError:
            raise Exception("Failed to connect")

        resp = sock.recv(2**15)

        print(resp)

        if not self.is_handshake_valid(handshake, resp):
            print("Failed to connect to {} -- invalid handshake".format(self.peer_info))
        else:
            print("{} connected successfully".format(self.peer_info))
            self.is_connected = True


    def fileno(self):
        if not self.sock:
            raise Exception("TCP connection with peer has not been established")
        return self.sock.fileno()
