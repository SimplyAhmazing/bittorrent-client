from pprint import pprint as pp

from torrent import Torrent
from peer import Peer
from peers_getter import PeersGetter


def main():

    torrent = Torrent('data/ubuntu.torrent')

    print(torrent.num_pieces)
    print(torrent.get_download_length())

    peers_info = PeersGetter(torrent).parse_peers()

    writers = []
    readers = []

    # Build connected peers
    for peer_info in peers_info:
        peer = Peer(torrent, peers_info)
        peer.connect()

        if peer.is_connected:
            writers.append(peer)
            readers.append(peer)

    pp(sorted(peers_info))



if __name__ == '__main__':
    main()

# print(resp.url)
# print()
# print(resp.status_code)
