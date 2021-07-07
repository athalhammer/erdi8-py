from collections import OrderedDict

# A value of 8 avoids that the first character of the identifier is a number
OFFSET = 8

# Definition of B33
B33 = OrderedDict(
    {
        "2": 0,
        "3": 1,
        "4": 2,
        "5": 3,
        "6": 4,
        "7": 5,
        "8": 6,
        "9": 7,
        "a": 8,
        "b": 9,
        "c": 10,
        "d": 11,
        "e": 12,
        "f": 13,
        "g": 14,
        "h": 15,
        "i": 16,
        "j": 17,
        "k": 18,
        "m": 19,
        "n": 20,
        "o": 21,
        "p": 22,
        "q": 23,
        "r": 24,
        "s": 25,
        "t": 26,
        "u": 27,
        "v": 28,
        "w": 29,
        "x": 30,
        "y": 31,
        "z": 32,
    }
)
B33_KEYS = list(B33.keys())

def increment(current):
    if not current:
        return B33_KEYS[OFFSET]
    tail = current[-1]
    current = current[:-1]
    pos = B33[tail] + 1
    if pos > len(B33) - 1:
        return increment(current) + B33_KEYS[pos % len(B33)]
    else:
        return current + B33_KEYS[pos]

def encode_int(dec):
    div = dec // len(B33)
    mod = dec % len(B33)
    if mod + OFFSET > len(B33) - 1:
        div = div + 1
    if div >= 1:
        return encode_int(div - 1) + B33_KEYS[(mod + OFFSET) % len(B33)]
    else:
        return B33_KEYS[(mod + OFFSET) % len(B33)]

def decode_int(e8):
    result = 0
    counter = 0
    while e8:
        tail = e8[-1]
        e8 = e8[:-1]
        result = result + (B33[tail] + 1) * (len(B33) ** counter) - OFFSET * len(B33) ** counter
        counter = counter + 1
    return result - 1
 
