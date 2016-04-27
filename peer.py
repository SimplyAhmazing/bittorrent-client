import socket
import struct

from bitstring import BitArray

from messages import MessageParser
from torrent import Torrent


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

        self.recieved_data_buffer = b''


    def is_handshake_valid(self, handshake : bytes, resp : bytes):
        """
        <pstrlen><pstr><reserved><info_hash><peer_id>
        """
        return handshake[28:48] == resp[28:48]


    def connect(self):
        handshake = self.torrent.get_handshake()

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(True)

        try:
            print('peer info is ', self.peer_info)
            self.sock.connect(self.peer_info)
            self.sock.send(handshake)
        except OSError:
            raise Exception("Failed to connect")

        resp = self.sock.recv(2**15)

        print(resp)

        if not self.is_handshake_valid(handshake, resp):
            print("Failed to connect to {} -- invalid handshake".format(self.peer_info))
        else:
            print("{} connected successfully".format(self.peer_info))
            self.is_connected = True

        self.recieved_data_buffer = resp[68:]
        self.process_read_buffer()


    def fileno(self):
        if not self.sock:
            raise Exception("TCP connection with peer has not been established")
        return self.sock.fileno()


    def read(self):
        self.recieved_data_buffer += self.sock.recv(2**15)
        self.process_read_buffer()

    def process_read_buffer(self):
        while self.recieved_data_buffer:
            message = MessageParser.parse(self.recieved_data_buffer)
            self.recieved_data_buffer = self.recieved_data_buffer[4 + message.length:]

            print(message)

            # print('..............................')
            # print('{} Buffer has: {}'.format(self.peer_info, self.recieved_data_buffer))
            # msg_len = struct.unpack('>I', self.recieved_data_buffer[:4])[0]
            # print('Msg recieved of len: ', msg_len)
            # print('Msg recieved of type: ', self.recieved_data_buffer[4])
            #
            # print('Msg recieved of type: ', msg_len)
            # self.recieved_data_buffer = self.recieved_data_buffer[msg_len:]

    def write(self):
        pass
