import unittest
import random
import math
from erdi8 import Erdi8


class E8Test(unittest.TestCase):
    KNOWN_VALUES = "test/test.csv"
    KNOWN_VALUES_SAFE = "test/test_safe.csv"

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

    def test_known_values_safe(self):
        e8 = Erdi8(safe=True)
        k = []
        with open(self.KNOWN_VALUES_SAFE, "r") as f:
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
        for _ in range(target_len):
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
        for _ in range(target_len):
            col_set.add(current)
            current = e8.increment_fancy(current, stride)
        self.assertEqual(len(col_set), target_len)
        self.assertEqual(current, "erd")

    def test_split_fancy(self):
        for flag in (False, True):
            e8 = Erdi8(flag)
            lsts = []
            num_splits = random.randint(2, 10)
            stride = random.randint(0, 100000000000000000000000)
            length = random.randint(2, 4)
            splits = e8.split_fancy_space(length, stride, num_splits)
            _, _, space_size = e8.mod_space(length)
            for i in range(num_splits):
                lst = []
                min = splits[i]
                max = splits[i + 1] if i + 1 < num_splits else splits[0]
                current = min
                while current != max:
                    lst.append(current)
                    current = e8.increment_fancy(current, stride)
                lsts.append(lst)
            lengths = [len(lst) for lst in lsts]
            total = sum(lengths)

            # make sure there are no duplicates
            st = set()
            for lst in lsts:
                for item in lst:
                    st.add(item)
            self.assertEqual(len(st), total)

            # make sure we covered the whole space
            self.assertEqual(total, space_size)

    def test_string_check(self):
        e8 = Erdi8()
        self.assertRaises(ValueError, e8.check, "23")
        self.assertRaises(ValueError, e8.check, "2ab")
        self.assertRaises(ValueError, e8.check, "a23l")
        self.assertRaises(ValueError, e8.check, "ab1")

    def test_safe(self):
        e8 = Erdi8(safe=True)
        self.assertRaises(ValueError, e8.check, "b23a")
        self.assertRaises(ValueError, e8.check, "b2e3")
        self.assertRaises(ValueError, e8.check, "bi23")
        self.assertRaises(ValueError, e8.check, "b23o")
        self.assertRaises(ValueError, e8.check, "b2u3")

    def safe_stride(self, erdi8, current, stride):
        mini, _, space = erdi8.mod_space(len(current))
        stride = stride % space
        while math.gcd(mini + stride, space) != 1:
            stride = stride + 1
        return stride

    def test_stride_compute(self):
        for _ in range(10000):
            e8 = Erdi8(safe=True)
            n = e8.encode_int(random.randint(0, 100000000000000000000000))
            stride = self.safe_stride(
                e8, n, random.randint(0, 100000000000000000000000)
            )
            n_plus_1 = e8.increment_fancy(n, stride)
            computed_stride = e8.compute_stride(n, n_plus_1)
            print(n, n_plus_1, stride)
            self.assertEqual(stride, computed_stride["stride_effective"])

    def test_stride_compute_safe_false(self):
        for _ in range(10000):
            e8 = Erdi8(safe=False)
            n = e8.encode_int(random.randint(0, 100000000000000000000000))
            stride = self.safe_stride(
                e8, n, random.randint(0, 100000000000000000000000)
            )
            n_plus_1 = e8.increment_fancy(n, stride)
            print(n, n_plus_1, stride)
            computed_stride = e8.compute_stride(n, n_plus_1)
            self.assertEqual(stride, computed_stride["stride_effective"])

    def test_stride_edge_cases_safe_false(self):
        e8 = Erdi8()
        self.assertRaises(ValueError, e8.compute_stride, "a", "f")
        self.assertRaises(ValueError, e8.compute_stride, "abc", "def")
        self.assertRaises(ValueError, e8.compute_stride, "abc", "defg")
        self.assertRaises(ValueError, e8.compute_stride, "b", "b")

    def test_stride_edge_cases(self):
        e8 = Erdi8(safe=True)
        self.assertRaises(ValueError, e8.compute_stride, "b", "j")
        self.assertRaises(ValueError, e8.compute_stride, "bcd", "fgj")
        self.assertRaises(ValueError, e8.compute_stride, "bcd", "fgjh")
        self.assertRaises(ValueError, e8.compute_stride, "b", "b")

    def test_encode_four_bytes(self):
        e8 = Erdi8()
        self.assertRaises(ValueError, e8.encode_four_bytes, [12, 12, 12])
        self.assertRaises(ValueError, e8.encode_four_bytes, "asdf")
        self.assertRaises(ValueError, e8.encode_four_bytes, [12.0, 12, 12, 12])
        self.assertRaises(ValueError, e8.encode_four_bytes, 12)
        self.assertRaises(ValueError, e8.encode_four_bytes, [12, 12, 12, 12, 12])
        self.assertRaises(ValueError, e8.encode_four_bytes, (12, 12, 12, 12))

    def test_encode_four_bytes(self):
        e8 = Erdi8()
        e8.encode_four_bytes([12, 12, 12, 12])
        e8.encode_four_bytes(bytes("asdf", "utf-8"))
        e8.encode_four_bytes(b"\xaa\xee\x00\xff")
