import hashlib
import random
import string

from bencoder import decode, encode


class Torrent(object):
    """Represents a .torrent file
    """

    torrent_file_dict = None

    def __init__(self, torrent_file_path):
        self.torrent_file_path = torrent_file_path

        self.parse_file()


    def get_file_length(self):
        info = self.torrent_file_dict[b'info']

        if b'length' in info:
            return int(info[b'length'])
        else:
            return sum([int(file[b'length']) for file in info[b'files']])

    def get_announce_url(self):
        announce_url = self.torrent_file_dict[b'announce'].decode('utf-8')

    def get_peer_id(self):
        info = encode(res[b'info'])
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
            'left': self.get_file_length()
        }

        return params

    def parse_file(self):
        data = open(self.torrent_file_path, 'rb').read()
        self.torrent_file_dict = decode(data)
