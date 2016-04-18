import unittest

from bencode import decode


class BencodeTestCase(unittest.TestCase):
    def test_decode_int(self):
        self.assertEqual(decode(b'i3e'), 3)
        self.assertEqual(decode(b'i0e'), 0)
        self.assertEqual(decode(b'i-4e'), -4)

    def test_decode_str(self):
        self.assertEqual(decode(b'4:spam'), b"spam")
        self.assertEqual(decode(b'0:'), b"")

    def test_decode_list(self):
        self.assertListEqual(decode(b'l4:spam4:eggse'), [b"spam", b"eggs"])
        self.assertListEqual(decode(b'le'), [])

    def test_decode_dict(self):
        self.assertDictEqual(
            decode(
                b'd3:cow3:moo4:spam4:eggse'),
                {b"cow": b"moo", b"spam": b"eggs"}
        )
        self.assertDictEqual(
            decode(b'd4:spaml1:a1:bee'), {b"spam": [b"a", b"b"]}
        )




if __name__ == '__main__':
    unittest.main()