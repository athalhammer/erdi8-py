import unittest
import erdi8

class E8Test(unittest.TestCase):

    def test_inc_enc_dec(self):
        a = "a"
        for i in range(0, 9999):
            enc = erdi8.encode_int(i)
            dec = erdi8.decode_int(a)
            self.assertEqual(a, enc)
            self.assertEqual(i, dec)
            a = erdi8.increment(a)
        self.assertEqual(a, "ifa")

    def test_string_check(self):
        self.assertFalse(erdi8.check("23"))
        self.assertFalse(erdi8.check("2ab"))
        self.assertFalse(erdi8.check("a23l"))
        self.assertFalse(erdi8.check("ab1"))

    def test_safe(self):
        erdi8.safe()
        self.assertFalse(erdi8.check("b23a"))
        self.assertFalse(erdi8.check("b2e3"))
        self.assertFalse(erdi8.check("bi23"))
        self.assertFalse(erdi8.check("b23o"))
        self.assertFalse(erdi8.check("b2u3"))
        erdi8.un_safe()
        self.assertTrue(erdi8.check("b23a"))
        self.assertTrue(erdi8.check("b2e3"))
        self.assertTrue(erdi8.check("bi23"))
        self.assertTrue(erdi8.check("b23o"))
        self.assertTrue(erdi8.check("b2u3"))
