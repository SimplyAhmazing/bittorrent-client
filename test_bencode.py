import unittest

from bencode import decode


class BencodeTestCase(unittest.TestCase):
    def test_decode_int(self):
        self.assertEqual(decode('i3e'), 3)
        self.assertEqual(decode('i0e'), 0)
        self.assertEqual(decode('i-4e'), -4)

    def test_decode_str(self):
        self.assertEqual(decode('4:spam'), "spam")
        self.assertEqual(decode('0:'), "")


if __name__ == '__main__':
    unittest.main()