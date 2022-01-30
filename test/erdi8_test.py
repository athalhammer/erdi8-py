import unittest
from erdi8 import Erdi8

class E8Test(unittest.TestCase):

    def test_inc_enc_dec(self):
        e8 = Erdi8()
        a = "a"
        for i in range(0, 9999):
            enc = e8.encode_int(i)
            dec = e8.decode_int(a)
            self.assertEqual(a, enc)
            self.assertEqual(i, dec)
            a = e8.increment(a)
        self.assertEqual(a, "ifa")

    def test_inc_fancy(self):
        e8 = Erdi8()
        current = "erd"
        target_len = 25 * 33 * 33
        col_set = set()
        for i in range(0, target_len):
            col_set.add(current)
            current = e8.increment_fancy(current, 12345)
        self.assertEqual(len(col_set), target_len)

    def test_string_check(self):
        e8 = Erdi8()
        self.assertFalse(e8.check("23"))
        self.assertFalse(e8.check("2ab"))
        self.assertFalse(e8.check("a23l"))
        self.assertFalse(e8.check("ab1"))

    def test_safe(self):
        e8 = Erdi8(safe = True)
        self.assertFalse(e8.check("b23a"))
        self.assertFalse(e8.check("b2e3"))
        self.assertFalse(e8.check("bi23"))
        self.assertFalse(e8.check("b23o"))
        self.assertFalse(e8.check("b2u3"))
