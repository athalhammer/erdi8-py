#    erdi8 -  a unique identifier scheme and identifier generator and transformer
#    that operates on the base-36 alphabet without [0, 1, and l]
#
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

"""
erdi8 is a unique identifier scheme and identifier generator and transformer
that operates on the following alphabet:

"23456789abcdefghijkmnopqrstuvwxyz"

It is basically a base36 alphabet that intentionally avoids the ambiguous 
characters [0, 1, and l] and therefore shrinks to 33. In addition to that, it
ensures that no identifier starts with a numeric value by using an offset of 8.
The zero is represented by 'a', 25 is represented by 'a2', etc. With three
characters or less one can create 28'075 (25 + 25 * 33 + 25 * 33 * 33) different
identifiers. With 6 characters or less we have 1'008'959'350 options. In a traditional
identifier world, one would use a prefix, e.g. M, and then an integer. This only
gives you 100k identifiers (M0 to M99999) with up to 6 characters. The scheme enables
consecutive counting and is therefore free of collisions. In particular, it is not a
method to create secret identifiers.
"""

import math
from typing import TypedDict, List, Optional, Tuple


class ComputedStride(TypedDict):
    """
    Custom type for computed stride. It resturns the effective stride as well as
    a list of candidates that were not suitable due to not having a greatest
    common denominator of 1 with the actual size of the space.
    """

    stride_effective: int
    stride_other_candidates: List[int]


class Erdi8:
    """
    The Erdi8 class.
    """

    # A value of 8 avoids that the first character of the identifier is a number
    OFFSET = 8
    UNSAFE = "aeiou"

    alph = "23456789abcdefghijkmnopqrstuvwxyz"

    def __init__(self, safe: bool = False):
        """
        Erdi8 Constructor.

        :param safe: A boolean to indicate whether [a,e,i,o,u] should be excluded
        as a profanity filter.

        """
        if safe:
            self.alph = "".join([a for a in self.alph if a not in self.UNSAFE])
        self.alph_map = {a: self.alph.find(a) for a in self.alph}
        self.alph_len = len(self.alph)

    def check(self, string: str) -> bool:
        """
        Method that supports checking or valid erdi8 strings.

        :param string: returns True if it's a valid erd8 string, otherwise False.
        """
        if string == "":
            return True
        flag = True
        flag = string[0] not in self.alph[: self.OFFSET]
        if not flag:
            raise ValueError(
                "Error: Not a valid erdi8 string, starts with " + string[0]
            )
        for i in string:
            if self.alph_map.get(i) is None:
                raise ValueError(
                    "Error: Dectected unknown character: "
                    + i
                    + "; allowed are the following: "
                    + self.alph
                )
        return flag

    def increment(self, current: Optional[str] = None) -> Optional[str]:
        """
        Simple increment for erdi8

        :param current: current erdi8 value
        :returns: next erdi8 value
        """
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

    def mod_space(self, length: int) -> Tuple[int, int, int]:
        """
        This function uses the decode_int function that has a loop in it. To get to the
        exact size of the mod space (min max space) some type of recursion/loop is required.

        :param length: the modspace length in which we are operating
        :returns: a tuple of three values: min, max, and space size of the mod space.
        """
        mini = self.decode_int(self.alph[-1] * (length - 1)) + 1
        maxi = self.decode_int(self.alph[-1] * length)
        space = maxi - mini + 1
        return (mini, maxi, space)

    def increment_fancy(self, current: str, stride: int) -> Optional[str]:
        """
        This method increments to the next value but uses a stride. It operates in a mod space

        :param current: current erdi8 value
        :param stride: stride parameter - a int denoting the stride
        :returns: next erdi8 value
        """
        if not self.check(current):
            return None
        mini, _, space = self.mod_space(len(current))
        while math.gcd(mini + stride, space) != 1:
            stride = stride + 1
        return self.encode_int(mini + ((self.decode_int(current) + stride) % space))

    def encode_int(self, div: int) -> str:
        """
        This method encodes a integer to an erdi8 string.

        :param div: integer to be encoded.
        :returns: encoded integer as erdi8 value.
        """
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

    def decode_int(self, erdi8: str) -> Optional[int]:
        """
        This method retuns a integer given a erdi8 string.

        :param erdi8: erdi8 string to be decoded.
        :returns: decoded integer value.
        """
        if not self.check(erdi8):
            return None
        result = 0
        counter = 0
        while erdi8:
            tail = erdi8[-1]
            erdi8 = erdi8[:-1]
            result = (
                result
                + (self.alph_map[tail] + 1) * (self.alph_len**counter)
                - self.OFFSET * self.alph_len**counter
            )
            counter = counter + 1
        return int(result - 1)

    def encode_four_bytes(self, bts: List[int]) -> str:
        """
        This method encodes a bytes object of size 4 to an erdi8 string. This will return a string with a
        fixed length of 7. Using this method will result in a compaction of 4 bytes to 7 characters.
        Note that this is significantly worse than the base64 encoding which encodes 3 bytes to 4 characters and
        also base32 which encodes 5 bytes to 8 characters. The advantage of this method is that it can be used
        with the option safe=True to avoid profanity. It also ensures that the first character is not a number
        therefore also avoids number-only identifiers.

        :param bytes: bytes object of length 4 to be encoded.
        :returns: bytes object as erdi8 value of length 7.
        """
        if not (isinstance(bts, list) or isinstance(bts, bytes)):
            raise ValueError(
                f"Error: We only encode lists of bytes. You provided {type(bts)}."
            )
        if len(bts) == 4:
            # type check
            for b in bts:
                if not isinstance(b, int):
                    raise ValueError(
                        f"Error: We only encode bytes. You provided {type(b)}."
                    )
                else:
                    if b < 0 or b > 255:
                        raise ValueError(
                            f"Error: A byte has a value between 0 and 255. You provided {b}."
                        )

            return self.encode_int(
                int.from_bytes(bts, "big") + self.decode_int("zzzzzz") + 1
            )
        else:
            raise ValueError(
                f"Error: We only encode 4 bytes at at time. You provided {len(bts)} bytes."
            )

    def decode_four_bytes(self, erdi8: str) -> Optional[List[int]]:
        """
        This method decodes an erdi8 string of length 7 to a bytes object of size 4. This will return a bytes object

        :param erdi8: erdi8 string of length 7 to be decoded.
        :returns: decoded bytes object of length 4.
        """
        if not self.check(erdi8):
            return None
        if len(erdi8) == 7:
            return (self.decode_int(erdi8) - self.decode_int("zzzzzz") - 1).to_bytes(
                4, "big"
            )
        else:
            raise ValueError(
                f"Error: We only decode 7 characters at at time. You provided {len(erdi8)} characters."
            )

    def compute_stride(self, erdi8: str, next_erdi8: str) -> ComputedStride:
        """
        This method computes possible stride values as well as the finally effective
        stride. It needs two successing erdi8 values from a mod-space setting. It reverse
        engineers the stride for the increment_fancy method.

        :param erdi8: n erdi8 value.
        :param next_erdi8: n+1 erdi8 value.
        :returns: effective stride and possible alternatives.
        """
        if not len(erdi8) == len(next_erdi8):
            raise ValueError(
                f"Error: '{erdi8}' and '{next_erdi8}' are of different length."
            )
        if not self.check(erdi8) or not self.check(next_erdi8):
            pass
        if erdi8 == next_erdi8:
            raise ValueError(f"Error: '{erdi8}' and '{next_erdi8}' are the same")
        mini, _, space = self.mod_space(len(erdi8))
        next_erdi8_int = self.decode_int(next_erdi8)
        erdi8_int = self.decode_int(erdi8)
        result = next_erdi8_int - erdi8_int - mini
        while result < 0:
            result = result + space
        if math.gcd(mini + result, space) != 1:
            raise ValueError(
                f"Error: '{result}' was detected as a stride but it is not suitable for an "
                f"erdi8 mod space with length '{len(erdi8)}'. "
                f"Are you sure the two numbers '{erdi8}' and '{next_erdi8}' are consecutive?"
            )
        candidates = []
        stride = result - 1
        while math.gcd(mini + stride, space) != 1:
            candidates.append(stride)
            stride = stride - 1
        return {"stride_effective": result, "stride_other_candidates": candidates}
