import requests

# from bencode import decode
from bencoder import decode, encode


class PeersGetter(object):
    def __init__(self, torrent):
        self.torrent = torrent

    def request_peers(self):
        resp = requests.get(
            self.torrent.get_announce_url(),
            params=self.torrent.get_tracker_request_params()
        )
        print(decode(resp.content))
        return decode(resp.content)


    def parse_peers(self):
        """
        Response data can be returned in binary....
        """
        peers_resp = self.request_peers()
        peers_data = peers_resp[b'peers']


        peers = []

        # Handle binary peers_data mode
        if isinstance(peers_data, bytes):
            for i in range(0, int(len(peers_data)), 6):
                ip_addr = '.'.join(
                    [str(byte) for byte in peers_data[i:i+4]]
                )
                port = (peers_data[i + 4] * 256) + peers_data[i + 5]
                peers.append((ip_addr, port))

        elif isinstance(peers_data, dict):
            #TODO parse dict model for peers list
            pass

        else:
            raise Exception("Unable to retrieve peers from torrent response")

        return peers