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
        # THEM
        self.is_chocking = True
        self.is_interested = False

        # ME
        self.am_interested = False
        self.am_chocking = True

        self.outbound_messages = []

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



        pass


    def read(self):
        self.recieved_data_buffer += self.sock.recv(2**15)
        self.process_read_buffer()

    def process_read_buffer(self):
        while self.recieved_data_buffer:

            msg_length = struct.unpack('>I', self.recieved_data_buffer[0:4])[0]
            packet_length = msg_length + 4

            # If the buffer doesn't contain the entirety of the packet then
            # break and wait until more data is read from socket
            if len(self.recieved_data_buffer) < packet_length:
                break

            message = MessageParser.parse(
                self.recieved_data_buffer[:packet_length],
                msg_length
            )

            self.recieved_data_buffer = self.recieved_data_buffer[packet_length:]
            print('buffer is: ', self.recieved_data_buffer)

            # Msg ID 0
            if message.name == 'choke':
                self.is_chocking = True

            # Msg ID 1
            if message.name == 'unchoke':
                self.is_chocking = False

            # Msg ID 2
            if message.name == 'interested':
                # TODO: send unchoke message
                pass

            # Msg ID 3
            if message.name == 'not_interested':
                self.is_interested = False

            # Msg ID 4
            if message.name == 'have':
                have_piece = struct.unpack('>I', message.payload)[0]
                self.pieces[have_piece] = True
                if self.am_interested and not self.am_chocking:
                    req = self.torrent.get_next_request(self.pieces)
                    if not req:
                        return

                    index, begin, length = req
                    payload = struct.pack('>III', index, begin, length)
                    req_msg = MessageParser.encode_msg('request', payload)
                    self.outbound_messages.append(req_msg)

            # Msg ID 5
            if message.name == 'bitfield':
                self.pieces = BitArray(bytes=message.payload)
                self.outbound_messages.append(
                    MessageParser.encode_msg('interested')
                )

            # Msg ID 6
            if message.name == 'request':
                if not self.am_chocking:
                    # Find piece from our downloaded torrent and send it back
                    pass

            # Msg ID 7
            if message.name == 'piece':
                index, begin = struct.unpack('>I I', message.payload[:8])
                print('Got piece, need to write it to file...')

    def write(self):
        pass
