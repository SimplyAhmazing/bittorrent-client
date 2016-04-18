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

    def test_decode_list(self):
        self.assertListEqual(decode('l4:spam4:eggse'), ["spam", "eggs"])
        self.assertListEqual(decode('le'), [])

    def test_decode_dict(self):
        self.assertDictEqual(
            decode('d3:cow3:moo4:spam4:eggse'), {"cow": "moo", "spam": "eggs"}
        )
        self.assertDictEqual(
            decode('d4:spaml1:a1:bee'), {"spam": ["a", "b"]}
        )




if __name__ == '__main__':
    unittest.main()