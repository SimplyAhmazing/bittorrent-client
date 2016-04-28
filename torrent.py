import hashlib
import math
import random
import string

from bencoder import decode, encode
from bitstring import BitArray


class Torrent(object):
    """Represents a .torrent file
    """

    torrent_file_dict = None

    def __init__(self, torrent_file_path):
        self.torrent_file_path = torrent_file_path
        self.torrent_file_dict = self.parse_file()


        self.piece_length = int(
            self.torrent_file_dict.get(b'info', {}).get(b'piece length', 0)
        )
        print(self.piece_length)
        self.num_pieces = int(self.get_download_length() / self.piece_length)
        self.last_piece_length = int(self.piece_length % self.num_pieces)

        self.block_length = 2**16
        self.last_block_length = int(self.piece_length % self.block_length)
        self.blocks_per_piece = int(math.ceil(self.piece_length / self.block_length))
        self.last_block_length = int(self.piece_length % self.block_length)

        self.have_pieces = BitArray(bin='0' * self.num_pieces)
        self.requested_pieces = BitArray(bin='0' * self.num_pieces)

        self.have_blocks = [
            BitArray(bin='0' * self.blocks_per_piece)
            for _ in range(self.num_pieces)
        ]
        self.requested_blocks = [
            BitArray(bin='0' * self.blocks_per_piece)
            for _ in range(self.num_pieces)
        ]

    def is_download_finished(self):
        return False

    def get_announce_url(self):
        return self.torrent_file_dict[b'announce'].decode('utf-8')

    def get_download_length(self):
        info = self.torrent_file_dict[b'info']

        if b'length' in info:
            return int(info[b'length'])
        else:
            return sum([int(file[b'length']) for file in info[b'files']])

    def get_next_request(self, have_pieces):
        # total_number_of_blocks = self.torrent.

        obtainable_pieces = have_pieces & ~self.requested_pieces

        try:
            piece_idx = next(
                idx
                for idx in range(len(obtainable_pieces))
                if obtainable_pieces[idx] == True
            )
        except StopIteration:
            return None

        offset = next(
            idx * self.block_length
            for idx in range(self.blocks_per_piece)
            if self.requested_blocks[piece_idx][idx] == False
        )

        piece_length = (
            self.last_piece_length
            if piece_idx == self.num_pieces - 1
            else self.piece_length
        )

        request_length = min(self.block_length, piece_length - offset)

        if request_length < 0:
            print('request length is below 0....')
            return None

        return piece_idx, offset, request_length



    def get_handshake(self):
        return b''.join([
            chr(19).encode(),
            b'BitTorrent protocol',
            (chr(0) * 8).encode(),
            self.get_info_hash(),
            self.get_peer_id().encode()
        ])

    def get_peer_id(self):
        info = encode(self.torrent_file_dict[b'info'])
        peer_id = 'SA' + ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for i in range(18)
        )
        return peer_id

    def get_info_hash(self):
        info = encode(self.torrent_file_dict[b'info'])
        return hashlib.sha1(info).digest()

    def get_tracker_request_params(self):
        params = {
            'info_hash': self.get_info_hash(),
            'peer_id': hashlib.sha1(self.get_peer_id().encode('utf-8')).digest(),
            'no_peer_id': 0,
            'compact': 1,
            'event': 'started',
            'port': 59696,
            'uploaded': 0,
            'downloaded': 0,
            'left': self.get_download_length()
        }

        return params

    def parse_file(self):
        data = None
        with open(self.torrent_file_path, 'rb') as f:
            data = f.read()
        return decode(data)
