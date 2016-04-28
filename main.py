from pprint import pprint as pp
from copy import deepcopy
import select

from torrent import Torrent
from peer import Peer
from peers_getter import PeersGetter


def main():

    torrent = Torrent('data/ubuntu.torrent')

    td = deepcopy(torrent.torrent_file_dict)

    td[b'info'][b'pieces'] = '20 byte pieces hashes go here...'

    pp(td)
    print('Number of pieces in the file:', torrent.num_pieces)
    print('Size of download in bytes: ', torrent.get_download_length())

    input()

    peers_info = PeersGetter(torrent).parse_peers()

    writers = []
    readers = []

    peers_connected_to_count = 0

    # Build connected peers
    for peer_info in peers_info:
        if peers_connected_to_count > 3:
            break
        peers_connected_to_count += 1

        peer = Peer(torrent, peer_info=peer_info)
        peer.connect()

        if peer.is_connected:
            writers.append(peer)
            readers.append(peer)


    while not torrent.is_download_finished():
        # print(
        #     'Downloading... Writers: {} Readers: {}'.format(
        #         len(readers), len(writers)
        #     )
        # )

        to_read, to_write, errors = select.select(readers, writers, readers)

        for peer in to_read:
            peer.read()

        for peer in to_write:
            peer.write()

        for peer in errors:
            readers.remove(peer)
            writers.remove(peer)

if __name__ == '__main__':
    main()
