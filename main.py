import hashlib
import random
import requests
from pprint import pprint as pp
import socket
import string

# from bencode import decode
from bencoder import decode, encode

from torrent import Torrent


torrent = Torrent('data/ubuntu.torrent')

print(torrent.get_file_length())


announce_url = torrent.get_announce_url()

# info = encode(res[b'info'])
# peer_id = 'SA' + ''.join(
#     random.choice(string.ascii_lowercase + string.digits) for i in range(18)
# )
# info_hash = hashlib.sha1(info).digest()
#
# params = {
#     'info_hash': info_hash,
#     'peer_id': hashlib.sha1(peer_id.encode('utf-8')).digest(),
#     'no_peer_id': 0,
#     'compact': 1,
#     'event': 'started',
#     'port': 59696,
#     'uploaded': 0,
#     'downloaded': 0,
#     'left': get_file_length(res)
# }

# print(params)

resp = requests.get(announce_url, params=params)
resp_content = decode(resp.content)


def parse_peers(resp):
    """
    Response data can be returned in binary....
    """
    peers_data = resp_content[b'peers']

    peers = []

    # Handle binary peers_data mode
    if isinstance(peers_data, bytes):
        for i in range(0, int(len(peers_data)), 6):
            ip_addr = '.'.join(
                [str(byte) for byte in peers_data[i:i+4]]
            )
            port = (peers_data[i + 4] * 256) + peers_data[i + 5]
            peers.append((ip_addr, port))

    elif isinstance(port, dict):
        #TODO parse dict model for peers list
        pass

    else:
        raise Exception("Unable to retrieve peers from torrent response")

    return peers


peers = parse_peers(resp_content)

pp(sorted(peers))

# Do handshake
# <pstrlen><pstr><reserved><info_hash><peer_id>

encode = lambda x: x.encode() if isinstance(x, str) else x

handshake = b''.join([
    chr(19).encode(),
    b'BitTorrent protocol',
    (chr(0) * 8).encode(),
    info_hash,
    peer_id.encode()
])


def parse_handshake_response(response):
    return

def connect_handshake(peer, handshake):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.setblocking(False)

    sock.setblocking(True)

    try:
        sock.connect(peer)
        sock.send(handshake)
    except socket.error:
        pass


    ret = sock.recv(2**15)

    if ret == handshake:
        print('handshake made correctly')


    import pdb; pdb.set_trace()



    # import pdb; pdb.set_trace()
    print(ret)


[connect_handshake(peer, handshake) for peer in peers]





print(resp.url)
print()
print(resp.status_code)
