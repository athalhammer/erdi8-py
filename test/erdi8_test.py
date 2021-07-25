import unittest
import erdi8

class E8Test(unittest.TestCase):

    def test_inc_enc_dec(self):
        e8 = erdi8.Erdi8()
        a = "a"
        for i in range(0, 9999):
            enc = e8.encode_int(i)
            dec = e8.decode_int(a)
            self.assertEqual(a, enc)
            self.assertEqual(i, dec)
            a = e8.increment(a)
        self.assertEqual(a, "ifa")

    def test_string_check(self):
        e8 = erdi8.Erdi8()
        self.assertFalse(e8.check("23"))
        self.assertFalse(e8.check("2ab"))
        self.assertFalse(e8.check("a23l"))
        self.assertFalse(e8.check("ab1"))

    def test_safe(self):
        e8 = erdi8.Erdi8(safe = True)
        self.assertFalse(e8.check("b23a"))
        self.assertFalse(e8.check("b2e3"))
        self.assertFalse(e8.check("bi23"))
        self.assertFalse(e8.check("b23o"))
        self.assertFalse(e8.check("b2u3"))
