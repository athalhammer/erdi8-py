![example workflow](https://github.com/athalhammer/erdi8/actions/workflows/unit_tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/erdi8)](https://pypi.org/project/erdi8)
[![GitHub license](https://img.shields.io/github/license/athalhammer/erdi8.svg)](https://github.com/athalhammer/erdi8/blob/master/LICENSE)

# erdi8

erdi8 is a [unique identifier](https://www.wikidata.org/wiki/Q6545185) scheme and identifier generator and transformer that operates on the following alphabet:

```
['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

It is basically a base36 alphabet that intentionally avoids the ambiguous characters `[0, 1, and l]` and therefore shrinks to 33. In addition to that, it ensures that no identifier starts with a numeric value by using an offset of 8. The zero is represented by 'a', 25 is represented by 'a2', etc. With three characters or less one can create 28'075 (25 + 25 * 33 + 25 * 33 * 33) different identifiers. With 6 characters or less we have 1'008'959'350 options. In a traditional identifier world, one would use a prefix, e.g. M, and then an integer. This only gives you 100k identifiers (M0 to M99999) with up to 6 characters. The scheme enables consecutive counting and is therefore free of collisions. In particular, it is __not__ a method to create secret identifiers.

## Usage


### Basic (counting)
```
$ python3

>>> from erdi8 import Erdi8
>>> e8 = Erdi8()
>>> e8.increment("erdi8")
'erdi9'
>>> e8.decode_int("erdi8")
6545185
>>> e8.encode_int(6545185)
'erdi8'
```

### Advanced (still counting)
Fixed length "fancy" identifiers with `safe=True` 

```
$ python3

>>> from erdi8 import Erdi8
>>> safe = True
>>> start = 'b222222222'
>>> stride = 30321718760514
>>> e8 = Erdi8(safe)
>>> e8.increment_fancy(start, stride)
'fmzz7cwc43'
>>> current = e8.increment_fancy('fmzz7cwc43', stride)
>>> print(current)
k7zydqrp64

# reverse engineer stride from two consecutive identifiers
>>> e8.compute_stride('fmzz7cwc43', current)
{'stride_effective': 30321718760517, 'stride_other_candidates': [30321718760516, 30321718760515, 30321718760514]}
```

**NOTE**

0. These sequences may have a "fancy" appearance but __they are not random__. They are perfectly predictable and are designed to "fill up the whole mod space" before previously coined identifiers start re-appearing.
1. The `safe=True` option helps you to avoid unintended words (i.e. removes the characters `[aeiou]` from the alphabet)
2. The fancy increment works with fixed lengths. If you work with a length of 10 (like above) You will have `20 * 28^9 = 211'569'119'068'160` options with `safe=True`. If you think you have more things to identify at some point you have two options: a) start directly with more characters or b) check for the start value (in this case `b222222222`) to re-appear - this will be the identifier that will "show up twice" first.
3. Store the following four parts in a safe place: a) `safe` parameter b) the `start` value c) the `stride` value. On top, keep good track of the `current` value.


### Advanced (random)
Also see documentation of Python's integrated [`random`](https://docs.python.org/3/library/random.html) and [`secrets`](https://docs.python.org/3/library/secrets.html) modules, in particular for `random`: "The pseudo-random generators of this module should not be used for security purposes. For security or cryptographic uses, see the `secrets` module". In any case, you should know what you are doing.

`random` module:

```
$ python3

>>> import random
>>> from erdi8 import Erdi8
>>> e8 = Erdi8()

# get random erdi8 identifiers with length 10
>>> mini, maxi, _ = e8.mod_space(10)
>>> e8.encode_int(random.randint(mini, maxi))
'vvctyx7c6o'
```

`secrets` module:

```
$ python3

>>> import secrets
>>> from erdi8 import Erdi8
>>> e8 = Erdi8()

>>> e8.encode_int(int.from_bytes(secrets.token_bytes()))
'jtx3i83pii8wo98wzuucu7uag6khrfpabrdn3qrqrxdxauvcgjg'

>>> e8.encode_int(secrets.randbits(256))
'a53mpn3xntywcbdcvfa932ub34evne9oha8pzoy6ii3ur2e364z'
```

### Advanced (hash functions)
erdi8 is compatible to the most common hash functions that typically output the digest in hexadecimal format. Also refer to the integrated [`hashlib`](https://docs.python.org/3/library/hashlib.html) Python module. In addition, consider other [hash functions](https://softwareengineering.stackexchange.com/questions/49550/which-hashing-algorithm-is-best-for-uniqueness-and-speed).

```
$ python3

>>> from erdi8 import Erdi8
>>> import hashlib

# prepare the item to be hashed and display the digests for sha256 and md5
>>> s = "asdf".encode("ascii")
>>> hashlib.sha256(s).hexdigest()
'f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b'
>>> hashlib.md5(s).hexdigest()
'912ec803b2ce49e4a541068d495ab570'

# encode the respective digests with erdi8
>>> e8 = Erdi8()
>>> e8.encode_int(int.from_bytes(hashlib.sha256(s).digest()))
'n6vz5j427zw66qx9n4jk9sw7otrvu38gdteehsocbke3xocvqok'
>>> e8.encode_int(int.from_bytes(hashlib.md5(s).digest()))
'bcmhm477p7poz6sv8jpr4cqu4h'

# same as above but safe=True
>>> e9 = Erdi8(safe=True)
>>> e9.encode_int(int.from_bytes(hashlib.sha256(s).digest()))
'cg8644xv4txkj49sfzcwn49h3hvsqb8xm2pqxxfxxg7mpz3nwsmhnf'
>>> e9.encode_int(int.from_bytes(hashlib.md5(s).digest()))
'fv3y2y9mgbr4xs85z5qb6bp4dxm'

# re-establish the hexdigest
>>> hex(e8.decode_int('n6vz5j427zw66qx9n4jk9sw7otrvu38gdteehsocbke3xocvqok'))
'0xf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b'
>>> hex(e8.decode_int('bcmhm477p7poz6sv8jpr4cqu4h'))
'0x912ec803b2ce49e4a541068d495ab570

# re-establish the hexdigest with from safe=True
>>> hex(e9.decode_int('cg8644xv4txkj49sfzcwn49h3hvsqb8xm2pqxxfxxg7mpz3nwsmhnf'))
'0xf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b'
hex(e9.decode_int('fv3y2y9mgbr4xs85z5qb6bp4dxm'))
'0x912ec803b2ce49e4a541068d495ab570'

```

### Advanced (UUID)
Also see the documentation of the [`uuid`](https://docs.python.org/3/library/uuid.html) integrated Python module.

```
$ python3

>>> from erdi8 import Erdi8
>>> import uuid
>>> e8 = Erdi8()
>>> e9 = Erdi8(safe=True)

>>> a = uuid.uuid4()
>>> a
UUID('6e8f578c-577c-4f48-b6ac-bf135c310dc4')
>>> b = e8.encode_int(a.int)

# here we have the UUID encoded as erdi8 string - 10 char shorter than ordinary UUIDs
>>> b
'au3jqjghpb7dqfejdanskzoaik'

# same as above but with safe=True
>>> c = e9.encode_int(a.int)
>>> c
'drmhy438mjhqdsbxhzn6v27b8n6'

# reverse
>>> uuid.UUID(int=e8.decode_int(b))
UUID('6e8f578c-577c-4f48-b6ac-bf135c310dc4')

# reverse with safe=True
>>> uuid.UUID(int=e9.decode_int(c))
UUID('6e8f578c-577c-4f48-b6ac-bf135c310dc4')

```

**Note**: This will never start with a zero or will in any way generate "number only" strings.

### Advanced (xid)
See also [`xid`](https://github.com/rs/xid). With `erdi8` encoding you gain some properties i.e. omitting problematic `[0, 1, l]` or also `[a, e, i, o, u]` (with the `safe=True` option to avoid "bad" words, see below in the FAQ), reducing to 19 characters only (at least until 2065 where it will switch to 20) or maintaining 20 characters while omitting `[a, e, i, o, u]` with `safe=True` (until 2081 after which it will switch to 21), and always start with a char (in fact, current or future xids will also start with a char). The k-sortedness property of xids will be maintained with the respective length (e.g., you should not compare 19 and 20 char xid+erdi8 strings after 2065 without modifications. You could add a leading `0` which is not in the erdi8 alphabet and can serve as a padding after 2065). The properties of `xid`s are kept as there is a bijective transformation via the int value of the 12 bytes of any xid.
```
$ python3

>>> from erdi8 import Erdi8
>>> from xid import Xid

>>> x = Xid()

# or, if you want to reproduce the below:
>>> x = Xid([100, 144, 152, 133, 98, 39, 69, 106, 189, 98, 39, 93])

>>> x.string()
'ci89h1b24t2mlfb24teg'

>>> x.value
[100, 144, 152, 133, 98, 39, 69, 106, 189, 98, 39, 93]

>>> e8 = Erdi8()
>>> e = e8.encode_int(int.from_bytes(x.value))
>>> e
'op34e9rackpsch39few'

>>> y = Xid(e8.decode_int('op34e9rackpsch39few').to_bytes(12))
>>> y.string()
'ci89h1b24t2mlfb24teg'

>>> e9 = Erdi8(safe=True)
>>> f = e9.encode_int(int.from_bytes(x.value))
>>> f
'n7dsv982t6dxymy4z5t3'
>>> z = Xid(e9.decode_int('n7dsv982t6dxymy4z5t3').to_bytes(12))
>>> z.string()
'ci89h1b24t2mlfb24teg'

```

### Advanced (encode bytes)
`erdi8`, by default works with integer representations. In particular, it represents any larger sequence of bytes as an integer. There are two main assumptions: 1) The size of the integers is usually small as one of the goals is concise identifiers. 2) The data is static and we are *not* considering streams of data (at the time of encoding the beginning we don't know the end yet). However, these assumptions may be wrong or may not hold for your use case. Therefore, we offer a method that can encode four bytes as erdi8 at a time. It results in junks of `erdi8` identifiers of length seven that can be concatenated if needed. The respective function is called `encode_four_bytes`.

```
$ python3

>>> from erdi8 import Erdi8
>>> e8 = Erdi8()
>>> e8.encode_four_bytes(bytes("erdi", "ascii"))
'bci7jr2'

>>> e8.decode_four_bytes('bci7jr2')
b'erdi'

>>> e9 = Erdi8(True)
>>> e9.encode_four_bytes(bytes("erdi", "ascii"))
'fjx2mt3'
>>> e9.decode_four_bytes('fjx2mt3')
b'erdi'
```

**NOTE**: These two methods are not compatible to the other `erdi8` functions. The integers behind the four byte junks are altered so that we ensure it will always result in a `erdi8` identifier character length of 7.

### Even more advanced
Run a light-weight erdi8 identifier service via [fasterid](https://github.com/athalhammer/fasterid)


## Test cases

```
$ python3 -m unittest test/erdi8_test.py 
```

## FAQ

__Why should I use `erdi8` instead of [`shortuuid`](https://github.com/skorokithakis/shortuuid)?__

_There are multiple aspects to it: `shortuuid` with the normal alphabet contains upper and lowercase characters. In `erdi8` we avoid this (see below). There is the option to customize the alphabet of `shortuuid`: you could use the erdi8 alphabet for example. However, this leads to very long UUIDs. In this context, we find the following statement in the README particularly troublesome: "If 22 digits are too long for you, you can get shorter IDs by just truncating the string to the desired length.". This drops all beneficial stochastic properties of UUIDs and you need to run careful checks for potential identifier duplication. Here `erdi8` with its counting or "mod space counting" options has a significant advantage._

__Why no upper case characters?__

_Because we don't want to `erdi8` to be confused with `Erdi8`._

__Why no start with a number?__

_Because we want to avoid "number-only" identifiers. If we allowed to start with a number, we would have identifiers of the type `42` and `322` which could be mistaken for integers. We could achieve this with a more complex scheme avoiding any number-only combinations (would therefore still allow ids like `2z`, to be investigated). Further, certain technologies such as XML don't support element names that start with a number. In particular, QNAMES such as `asdf:123` are not allowed. Finally, it is important to note that programs like Excel are really creative when transforming input data, for example `08342 -> 8342`, `12e34 -> 12E+34`, `SEPT1 -> Sep-01` etc. erdi8 with the safe option on avoids 99% of these types of issues._

__How about combinations that form actual (bad) words?__

_This depends on the use case and the way erdi8 is used. Therefore, we can recommend to work with filter lists. In addition, an erdi8 object that avoids the `aeiou` characters can be created with `Erdi8(safe=True)`. This shrinks the available character space to 28 and the produced output is not compatible to `Erdi8(safe=False)` (default). The danger that unintended English words are created is lower with this setting.  It is recommended for erdi8 identifiers that are longer than three characters where filter lists start to become impractical._

__How does this relate to binary-to-text encodings such as base32 and base64?__

_erdi8 can be used for a binary-to-text encoding and the basic functions to implement this are provided with `encode_int` and `decode_int`. However, the primary purpose is to provide a short counting scheme for identifiers._

__What could be a drawback of using erdi8?__

_It depends how you use it. If you use it to re-encode integer representations of other byte-array-like objects (secret numbers, hash digests, UUIDs, xids) it is likely that the length of the strings produced by erdi8 will vary. This variance may be predictable (for example with `xid`s) but can also cover larger ranges (secrets, hash digests, etc). A minimum and maximum length can be calculated given the number of bytes and the chosen erdi8 options (`safe=True` vs `safe=False`). At the moment we don't support padding as a built-in function. It depends on the use case to determine if it is necessary or not._
