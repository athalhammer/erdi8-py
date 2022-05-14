#    erdi8
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
        self.alph_BAK = self.alph
        self.alph_len = len(self.alph)

    def check(self, string):
        if string == "":
            return True
        flag = True
        flag = string[0] not in self.alph[: self.OFFSET]
        if not flag:
            print(
                "Error: Not a valid erdi8 string, starts with " + string[0],
                file=sys.stderr,
            )
        for i in string:
            if self.alph_map.get(i) is None:
                print(
                    "Error: Dectected unknown character: "
                    + i
                    + "; allowed are the following: "
                    + self.alph,
                    file=sys.stderr,
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

    def increment_fancy(self, current, seed):
        if not self.check(current):
            return None
        length = len(current)
        mini = self.decode_int('z' * (length - 1)) + 1
        maxi = self.decode_int('z' * length)
        space = maxi - mini + 1
        while math.gcd(mini + seed, space) != 1:
            seed = seed + 1
        return self.encode_int(mini + ((self.decode_int(current) + seed) % space))

    def encode_int(self, div):
        result = ""
        mod = div % self.alph_len
        div = div // self.alph_len
        if mod + self.OFFSET > self.alph_len - 1:
            div = div + 1
        mod = mod + self.OFFSET
        while(div >= 1):
            div = div - 1
            result = self.alph[mod % self.alph_len] + result
            mod = div % self.alph_len
            div = div // self.alph_len
            if mod + self.OFFSET > self.alph_len - 1:
                div = div + 1
            mod = mod + self.OFFSET
        return(self.alph[mod % self.alph_len] + result)

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
                + (self.alph_map[tail] + 1) * (self.alph_len ** counter)
                - self.OFFSET * self.alph_len ** counter
            )
            counter = counter + 1
        return result - 1
