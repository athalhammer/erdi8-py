#    erdi8 - a unique identifier scheme and counter that operates on the
#    base-36 alphabet without [0, 1, and l]
#    Copyright (C) 2021  Andreas Thalhammer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import math
import sys


class Erdi8:
    # A value of 8 avoids that the first character of the identifier is a number
    OFFSET = 8
    UNSAFE = "aeiou"

    alph = "23456789abcdefghijkmnopqrstuvwxyz"
    safe = False

    def __init__(self, safe=False):
        if safe:
            self.alph = "".join([a for a in self.alph if a not in self.UNSAFE])
            self.safe = True
        self.alph_map = {a: self.alph.find(a) for a in self.alph}
        self.alph_len = len(self.alph)

    def check(self, string):
        if string == "":
            return True
        flag = True
        flag = string[0] not in self.alph[: self.OFFSET]
        if not flag:
            raise Exception("Error: Not a valid erdi8 string, starts with " + string[0])
        for i in string:
            if self.alph_map.get(i) is None:
                raise Exception(
                    "Error: Dectected unknown character: "
                    + i
                    + "; allowed are the following: "
                    + self.alph
                )
                flag = False
        return flag

    def increment(self, current=None):
        if not current:
            return self.alph[self.OFFSET]
        if not self.check(current):
            return None
        current = list(current)
        carry = True
        count = 1
        while carry:
            char = current[len(current) - count]
            pos = self.alph_map[char] + 1
            current[len(current) - count] = self.alph[pos % self.alph_len]
            if pos >= self.alph_len:
                count = count + 1
            else:
                carry = False
            if count > len(current):
                current.insert(0, self.alph[self.OFFSET - 1])
        return "".join(current)

    def mod_space(self, length):
        """
        This function uses the decode_int function that has a loop in it. To get to the
        exact size of the mod space (min max space) some type of recursion/loop is required.
        """
        mini = self.decode_int(self.alph[-1] * (length - 1)) + 1
        maxi = self.decode_int(self.alph[-1] * length)
        space = maxi - mini + 1
        return (mini, maxi, space)

    def increment_fancy(self, current, stride):
        if not self.check(current):
            return None
        mini, maxi, space = self.mod_space(len(current))
        while math.gcd(mini + stride, space) != 1:
            stride = stride + 1
        return self.encode_int(mini + ((self.decode_int(current) + stride) % space))

    def encode_int(self, div):
        result = ""
        mod = div % self.alph_len
        div = div // self.alph_len
        if mod + self.OFFSET > self.alph_len - 1:
            div = div + 1
        mod = mod + self.OFFSET
        while div >= 1:
            div = div - 1
            result = self.alph[mod % self.alph_len] + result
            mod = div % self.alph_len
            div = div // self.alph_len
            if mod + self.OFFSET > self.alph_len - 1:
                div = div + 1
            mod = mod + self.OFFSET
        return self.alph[mod % self.alph_len] + result

    def decode_int(self, e8):
        if not self.check(e8):
            return None
        result = 0
        counter = 0
        while e8:
            tail = e8[-1]
            e8 = e8[:-1]
            result = (
                result
                + (self.alph_map[tail] + 1) * (self.alph_len**counter)
                - self.OFFSET * self.alph_len**counter
            )
            counter = counter + 1
        return result - 1

    def compute_stride(self, n, n_plus_1):
        if not len(n) == len(n_plus_1):
            raise Exception(f"Error: '{n}' and '{n_plus_1}' are of different length.")
        if not self.check(n) or not self.check(n_plus_1):
            pass
        if n == n_plus_1:
            raise Exception(f"Error: '{n}' and '{n_plus_1}' are the same")
        mini, maxi, space = self.mod_space(len(n))
        a = self.decode_int(n_plus_1)
        b = self.decode_int(n)
        result = a - b - mini
        while result < 0:
            result = result + space
        if math.gcd(mini + result, space) != 1:
            raise Exception(
                f"Error: '{result}' was detected as a stride but it is not suitable for an erdi8 mod space with length '{len(n)}'. Are you sure the two numbers '{n}' and '{n_plus_1}' are consecutive?"
            )
        candidates = []
        stride = result - 1
        while math.gcd(mini + stride, space) != 1:
            candidates.append(stride)
            stride = stride - 1
        return {"stride_effective": result, "stride_other_candidates": candidates}
