![example workflow](https://github.com/athalhammer/erdi8/actions/workflows/unit_tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/erdi8)](https://pypi.org/project/erdi8)
[![GitHub license](https://img.shields.io/github/license/athalhammer/erdi8.svg)](https://github.com/athalhammer/erdi8/blob/master/LICENSE)

# erdi8

erdi8 is a [unique identifier](https://www.wikidata.org/wiki/Q6545185) scheme and counter that operates on the following alphabet:

```
['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

It is basically a base36 alphabet that intentionally avoids the ambiguous characters `[0, 1, and l]` and therefore shrinks to 33. In addition to that, it ensures that no identifier starts with a numeric value by using an offset of 8. The zero is represented by 'a', 25 is represented by 'a2', etc. With three characters or less one can create 28'075 (25 + 25 * 33 + 25 * 33 * 33) different identifiers. With 6 characters or less we have 1'008'959'350 options. In a traditional identifier world, one would use a prefix, e.g. M, and then an integer. This only gives you 100k identifiers (M0 to M99999) with up to 6 characters. The scheme enables consecutive counting and is therefore free of collisions. In particular, it is __not__ a method to create secret identifiers.

## Usage


### Basic
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

### Advanced
Fixed length "fancy" identifiers with `safe=True` 

```
$ python3

>>> from erdi8 import Erdi8
>>> safe = True
>>> start = 'b222222222'
>>> seed = 453459956896834
>>> e8 = Erdi8(safe)
>>> e8.increment_fancy(start, seed)
'fmzz7cwc43'
>>> current = e8.increment_fancy('fmzz7cwc43', seed)
>>> print(current)
k7zydqrp64
```

**NOTE**

0. These sequences may have a fancy appearance but __they are not random__. They are perfectly predictable and are designed to "fill up the whole mod space" before previously coined identifiers start re-appearing.
1. The `safe=True` option helps you to avoid unintended words (i.e. removes the characters `[aeiou]` from the alphabet)
2. The fancy increment works with fixed lengths. If you work with a length of 10 (like above) You will have `20 * 28^9 = 211'569'119'068'160` options with `safe=True`. If you think you have more things to identify at some point you have two options: a) start directly with more characters or b) check for the start value (in this case `b222222222`) to re-appear - this will be the identifier that will "show up twice" first.
3. Store the following four parts in a safe place: a) `safe` parameter b) the `start` value c) the `seed` value. On top, keep good track of the `current` value.

## Test cases

```
$ python3 -m unittest test/erdi8_test.py 
```

## Intended use

When you run an identifier redirect service of the type `https://purl.example.org/` your users can reserve "their space" for their current business application and or domain. We encourage the administrator of such a service to offer opaque folder names for long-term identifier stability. These folder names can be chosen to follow the erdi8 scheme and offer 825 (25 * 33) potential two-character folder names. In addition, also subfolder names and local accession identifiers can be generated with this scheme such that FAIR data objects can be identified with URIs of the type `https://purl.example.org/b7/a/erdi8`.

## FAQ

__Why no upper case characters?__

_Because we don't want to `erdi8` to be confused with `Erdi8`._

__Why no start with a number?__

_Because we want to avoid "number-only" identifiers. If we allowed to start with a number, we would have identifiers of the type `42` and `322` which could be mistaken for integers. We could achieve this with a more complex scheme avoiding any number-only combinations (would therefore still allow ids like `2z`, to be investigated)._

__How about combinations that form actual (bad) words?__

_This depends on the use case and the way erdi8 is used. Therefore, we can recommend to work with filter lists. In addition, an erdi8 object that avoids the `aeiou` characters can be created with `Erdi8(safe=True)`. This shrinks the available character space to 28 and the produced output is not compatible to `Erdi8(safe=False)` (default). The danger that unintended English words are created is lower with this setting.  It is recommended for erdi8 identifiers that are longer than three characters where filter lists start to become impractical._

__How does this relate to binary-to-text encodings such as base32 and base64?__

_erdi8 can be used for a binary-to-text encoding and the basic functions to implement this are provided with `encode_int` and `decode_int`. However, the primary purpose is to provide a short counting scheme for identifiers._
