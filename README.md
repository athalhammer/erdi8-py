![example workflow](https://github.com/athalhammer/erdi8/actions/workflows/unit_tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/erdi8)](https://pypi.org/project/erdi8)
[![GitHub license](https://img.shields.io/github/license/athalhammer/erdi8.svg)](https://github.com/athalhammer/erdi8/blob/master/LICENSE)

# erdi8

erdi8 is a [unique identifier](https://www.wikidata.org/wiki/Q6545185) scheme and identifier generator that counts with the following alphabet:

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
>>> mini, maxi, space = e8.mod_space(10)
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

### Advanced (UUID)
Also see the documentation of the [`uuid`](https://docs.python.org/3/library/uuid.html) integrated Python module.

```
$ python3

>>> from erdi8 import Erdi8
>>> import uuid
>>> e8 = Erdi8()

>>> a = uuid.uuid4()
>>> a
UUID('6e8f578c-577c-4f48-b6ac-bf135c310dc4')
>>> b = e8.encode_int(a.int)

# here we have the UUID encoded as erdi8 string - 10 char shorter than ordinary UUIDs
>>> b
'au3jqjghpb7dqfejdanskzoaik'

>>> uuid.UUID(int=e8.decode_int(b))
UUID('6e8f578c-577c-4f48-b6ac-bf135c310dc4')

```

**Note**: This will never start with a zero or will in any way generate "number only" strings.

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

_Because we want to avoid "number-only" identifiers. If we allowed to start with a number, we would have identifiers of the type `42` and `322` which could be mistaken for integers. We could achieve this with a more complex scheme avoiding any number-only combinations (would therefore still allow ids like `2z`, to be investigated). In essence it is important to note that programs like Excel are really creative when transforming input data, for example `08342 -> 8342`, `12e34 -> 12E+34`, `SEPT1 -> Sep-01` etc. erdi8 with the safe option on avoids 99% of these types of issues._

__How about combinations that form actual (bad) words?__

_This depends on the use case and the way erdi8 is used. Therefore, we can recommend to work with filter lists. In addition, an erdi8 object that avoids the `aeiou` characters can be created with `Erdi8(safe=True)`. This shrinks the available character space to 28 and the produced output is not compatible to `Erdi8(safe=False)` (default). The danger that unintended English words are created is lower with this setting.  It is recommended for erdi8 identifiers that are longer than three characters where filter lists start to become impractical._

__How does this relate to binary-to-text encodings such as base32 and base64?__

_erdi8 can be used for a binary-to-text encoding and the basic functions to implement this are provided with `encode_int` and `decode_int`. However, the primary purpose is to provide a short counting scheme for identifiers._
