# A value of 8 avoids that the first character of the identifier is a number
OFFSET = 8

ALPH = "23456789abcdefghijkmnopqrstuvwxyz"
ALPH_MAP = {a: ALPH.find(a) for a in ALPH}
LEN = len(ALPH)


def increment(current):
    if not current:
        return ALPH[OFFSET]
    tail = current[-1]
    current = current[:-1]
    pos = ALPH_MAP[tail] + 1
    if pos > len(ALPH) - 1:
        return increment(current) + ALPH[pos % LEN]
    else:
        return current + ALPH[pos]


def encode_int(dec):
    div = dec // LEN
    mod = dec % LEN
    if mod + OFFSET > LEN - 1:
        div = div + 1
    if div >= 1:
        return encode_int(div - 1) + ALPH[(mod + OFFSET) % LEN]
    else:
        return ALPH[(mod + OFFSET) % LEN]


def decode_int(e8):
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
