import sys

# A value of 8 avoids that the first character of the identifier is a number
OFFSET = 8

# Defines the alphabet
ALPH = "23456789abcdefghijkmnopqrstuvwxyz"


def init():
    global ALPH_MAP, LEN
    ALPH_MAP = {a: ALPH.find(a) for a in ALPH}
    LEN = len(ALPH)


init()


def safe():
    global ALPH, ALPH_BAK, ALPH_MAP, LEN
    ALPH_BAK = ALPH
    ALPH = "".join([a for a in ALPH if a not in "aeiuo"])
    init()


def un_safe():
    global ALPH, ALPH_BAK, ALPH_MAP, LEN
    ALPH = ALPH_BAK
    init()


def check(string):
    if string == "":
        return True
    flag = True
    flag = string[0] not in ALPH[:OFFSET]
    if not flag:
        print(
            "Error: Not a valid erdi8 string, starts with " + string[0], file=sys.stderr
        )
    for i in string:
        if ALPH_MAP.get(i) is None:
            print(
                "Error: Dectected unknown character: "
                + i
                + "; allowed are the following: "
                + ALPH,
                file=sys.stderr,
            )
            flag = False
    return flag


def increment(current, alph=ALPH):
    if not check(current):
        return None
    if not current:
        return ALPH[OFFSET]
    tail = current[-1]
    current = current[:-1]
    pos = ALPH_MAP[tail] + 1
    if pos > len(ALPH) - 1:
        return increment(current) + ALPH[pos % LEN]
    else:
        return current + ALPH[pos]


def encode_int(dec, alph=ALPH):
    div = dec // LEN
    mod = dec % LEN
    if mod + OFFSET > LEN - 1:
        div = div + 1
    if div >= 1:
        return encode_int(div - 1) + ALPH[(mod + OFFSET) % LEN]
    else:
        return ALPH[(mod + OFFSET) % LEN]


def decode_int(e8, alph=ALPH):
    if not check(e8):
        return None
    result = 0
    counter = 0
    while e8:
        tail = e8[-1]
        e8 = e8[:-1]
        result = (
            result + (ALPH_MAP[tail] + 1) * (LEN ** counter) - OFFSET * LEN ** counter
        )
        counter = counter + 1
    return result - 1
