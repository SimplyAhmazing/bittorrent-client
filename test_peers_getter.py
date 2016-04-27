import unittest
from unittest import mock

from torrent import Torrent
from peers_getter import PeersGetter


class PeersGetterTestCase(unittest.TestCase):
    def setUp(self):
        self.torrent = Torrent('data/ubuntu.torrent')
        self.pg = PeersGetter(self.torrent)
        self.pg.request_peers = mock.Mock(
            return_value={
                b'complete': 389,
                b'peers':
                    b'.\xa6\xbc\xe2\xa7\xabI\xe1\xc8\x1c\x1a\xe1^\x17\xd3K\xc8\x89\xd43\x9f\x81~\xafQ\xa9\x96:\xc8\xd5\x94e\x94\xbd\xf0PY_&\xb8\xc8\xd5G\xaf1\x11\xe3\x88[\xca(s\xc78\xc6\x1bJ\xd0y\xb8\x1f\xd0)\x9e\x1a\xe1X\xc6\\/\x1a\xe1G\xf1\xff\xbc\xd1.\xc1Gp\x83\x1b:\x05\x87\xb7\xe2\x82e%\xbbp\x9a\xc8\xd5XP((\xc8\xd5T\xec"#\xcb\x1fm\xcd\xc8\xa1\xd6\xd8>\xd2\xc34\xc8\xd5\xb0\x1fx.\xdd\x1eU\x11\x1ds\xee\x80\xd9\x0b\xb6\x04\xc8\xd5%\xbb\x05\xba\xaf\xc8\xc3\x9ai\x85\xc8\xd5l\x13kV\xe1\n_\xd3\xcd\x97\xc8\xd5\xc3\x9a\r\xa7\xc8\nd#\xec\xfe\xc3P\xbc\x1b\xbd-\xc8\xd5\x05\xc4Xj\xaf\xc8K\x98x\xb5\xc00\xbck\xa4\xc2\x1a\xe1[\xd2W\xcd\xc8\xd5Q\x02S~\xc8\xd5\xb9\x15\xd8\x9djmO\x8d\xad\xad\x9c\xddO\x8d\xabQ,\xefO\x8d\xae\'\xb0\xd3O\x8d\xad\x8et&_\x8d\x1c\xb5\x8f\x06O\x8d\xabI\xe5\x01O\x8d\xa0I\xbb\x06O\x8d\xad\xa3A\x95_\x8d\x1c\xb1\xb7\x18O\x8d\xabDz\x10_\x8d\x1c\xb4\xe6y_\x8d\x1c\xb3 \x90O\x8d\xabE\xee@O\x8d\xa0KA@',
                b'incomplete': 60,
                b'interval': 1800
            }
        )



    def test_parse_peers(self):
        expected = [
            ('46.166.188.226', 42923),
            ('73.225.200.28', 6881),
            ('94.23.211.75', 51337),
            ('212.51.159.129', 32431),
            ('81.169.150.58', 51413),
            ('148.101.148.189', 61520),
            ('89.95.38.184', 51413),
            ('71.175.49.17', 58248),
            ('91.202.40.115', 51000),
            ('198.27.74.208', 31160),
            ('31.208.41.158', 6881),
            ('88.198.92.47', 6881), ('71.241.255.188', 53550), ('193.71.112.131', 6970), ('5.135.183.226', 33381), ('37.187.112.154', 51413), ('88.80.40.40', 51413), ('84.236.34.35', 51999), ('109.205.200.161', 55000), ('62.210.195.52', 51413), ('176.31.120.46', 56606), ('85.17.29.115', 61056), ('217.11.182.4', 51413), ('37.187.5.186', 45000), ('195.154.105.133', 51413), ('108.19.107.86', 57610), ('95.211.205.151', 51413), ('195.154.13.167', 51210), ('100.35.236.254', 50000), ('188.27.189.45', 51413), ('5.196.88.106', 45000), ('75.152.120.181', 49200), ('188.107.164.194', 6881), ('91.210.87.205', 51413), ('81.2.83.126', 51413), ('185.21.216.157', 27245), ('79.141.173.173', 40157), ('79.141.171.81', 11503), ('79.141.174.39', 45267), ('79.141.173.142', 29734), ('95.141.28.181', 36614), ('79.141.171.73', 58625), ('79.141.160.73', 47878), ('79.141.173.163', 16789), ('95.141.28.177', 46872), ('79.141.171.68', 31248), ('95.141.28.180', 59001), ('95.141.28.179', 8336), ('79.141.171.69', 60992), ('79.141.160.75', 16704)]

        peers = self.pg.parse_peers()

        self.assertListEqual(peers, expected)


if __name__ == '__main__':
    unittest.main()