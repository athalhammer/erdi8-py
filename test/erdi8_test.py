import unittest
import random
import math
from erdi8 import Erdi8


class E8Test(unittest.TestCase):

    KNOWN_VALUES = "test/test.csv"

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

    def test_known_values(self):
        e8 = Erdi8()
        k = []
        with open(self.KNOWN_VALUES, "r") as f:
            m = f.readline()
            while m:
                k.append(tuple([x.strip() for x in m.split(",")]))
                m = f.readline()
        for i in k:
            print(f"checking {i}...")
            self.assertEqual(e8.encode_int(int(i[0])), i[1])
            self.assertEqual(e8.decode_int(i[1]), int(i[0]))

    def test_inc_fancy_safe(self):
        e8 = Erdi8(safe=True)
        current = "rd8"
        target_len = 20 * 28 * 28
        col_set = set()
        stride = random.randint(0, 100000000000000000000000)
        # do the full tour
        for i in range(0, target_len):
            col_set.add(current)
            current = e8.increment_fancy(current, stride)
        self.assertEqual(len(col_set), target_len)
        self.assertEqual(current, "rd8")

    def test_inc_fancy(self):
        e8 = Erdi8()
        current = "erd"
        target_len = 25 * 33 * 33
        col_set = set()
        stride = random.randint(0, 100000000000000000000000)

        # do the full tour
        for i in range(0, target_len):
            col_set.add(current)
            current = e8.increment_fancy(current, stride)
        self.assertEqual(len(col_set), target_len)
        self.assertEqual(current, "erd")

    def test_string_check(self):
        e8 = Erdi8()
        self.assertRaises(Exception, e8.check, "23")
        self.assertRaises(Exception, e8.check, "2ab")
        self.assertRaises(Exception, e8.check, "a23l")
        self.assertRaises(Exception, e8.check, "ab1")

    def test_safe(self):
        e8 = Erdi8(safe=True)
        self.assertRaises(Exception, e8.check, "b23a")
        self.assertRaises(Exception, e8.check, "b2e3")
        self.assertRaises(Exception, e8.check, "bi23")
        self.assertRaises(Exception, e8.check, "b23o")
        self.assertRaises(Exception, e8.check, "b2u3")

    def safe_stride(self, erdi8, current, stride):
        mini, maxi, space = erdi8._mod_space(current)
        stride = stride % space
        while math.gcd(mini + stride, space) != 1:
            stride = stride + 1
        return stride

    def test_stride_compute(self):
        for i in range(0, 10000):
            e8 = Erdi8(safe=True)
            n = e8.encode_int(random.randint(0, 100000000000000000000000))
            stride = self.safe_stride(e8, n, random.randint(0, 100000000000000000000000))
            n_plus_1 = e8.increment_fancy(n, stride)
            computed_stride = e8.compute_stride(n, n_plus_1)
            print(n, n_plus_1, stride) 
            self.assertEqual(stride, computed_stride["stride_effective"])

    def test_stride_compute_safe_false(self):
        for i in range(0, 10000):
            e8 = Erdi8(safe=False)
            n = e8.encode_int(random.randint(0, 100000000000000000000000))
            stride = self.safe_stride(e8, n, random.randint(0, 100000000000000000000000))
            n_plus_1 = e8.increment_fancy(n, stride)
            print(n, n_plus_1, stride)
            computed_stride = e8.compute_stride(n, n_plus_1)
            self.assertEqual(stride, computed_stride["stride_effective"])
