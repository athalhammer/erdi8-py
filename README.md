# erdi8

erdi8 is a [unique identifier](https://www.wikidata.org/wiki/Q6545185) scheme and generator that operates on the following alphabet:

```
['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

It is basically a base36 alphabet that intentionally avoids the ambigous characters `[0, 1, and l]` and therefore shrinks to 33. In addition to that, it ensures that no identifier starts with a numeric value by using an offset of 8. The zero is represented by 'a', 25 is represented by 'a2', etc. With three characters or less one can create 28'075 (25 + 25 * 33 + 25 * 33 * 33) different identifiers. With 6 characters or less we have 1'008'959'350 options. In a traditional identifier world one would use a prefix, e.g. M, and then an integer. This only gives you 100k identifiers (M0 to M99999) with up to 6 characters. The scheme enables consecutive counting and is therefore free of collissions. In particular, it is __not__ a method to create secret identifiers.

## Usage

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

## Test cases

```
$ python3 -m unittest test/erdi8_test.py 
```

## Intended use

When you run an identifier redirect service of the type `https://id.example.org/` your users can reserve "their space" for their current business application and or domain. We encourage the administrator of such a service to offer opaque folder names for long-term identifier stability. These folder names can be chosen to follow the erdi8 scheme and offer 825 (25 * 33) potential two-character folder names. In addition, also subfolder names and local accession identifiers can be generated with this scheme such that FAIR data objects can be identified with URIs of the type `https://id.example.org/b7/a/erdi8`.

## FAQ

__Why no upper case characters?__

_Because we don't want to `erdi8` to be confused with `Erdi8`._

__Why no start with a number?__

_Because we want to avoid "number-only" identifiers. If we allowed to start with a number we would have identifiers of the type `42` and `322` which could be mistaken for integers. We could achieve this with a more complex scheme avoiding any number-only combinations (would therefore still allow ids like `2z`, to be investigated)._

__How about combinations that form actual (bad) words?__

_This depends on the use case and the way erdi8 is used. Therefore, we can recommend to work with filter lists. In addition an erdi8 object that avoids the `aeiou` characters can be created with `Erdi8(safe=True)`. This shrinks the available character space to 28 and the produced output is not compatible to `Erdi8(safe=False)` (default). However, the danger that unintended English words are created is lower._

__How does this relate to binary-to-text encodings such as base32 and base64?__

_erdi8 can be used for a binary-to-text encoding and the basic functions to implement this are provided with `encode_int` and `decode_int`. However, the primary purpose is to provide a short counting scheme for identifiers._
