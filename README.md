# erdi8

erdi8 is a [unique identifier](https://www.wikidata.org/wiki/Q6545185) generator that operates on the following alphabet:

```
['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

It is basically a base36 alphabet that intentionally avoids the ambigous characters `[0, 1, and l]` and therefore shrinks to 33. In addition to that, it ensures that no identifier starts with a numeric value by using an offset of 8. The zero is represented by 'a', 25 is represented by 'a2', etc. With three characters or less one can create 28'075 (25 + 25 * 33 + 25 * 33 * 33) different identifiers. With 6 characters or less we have 1'008'959'350 options. In a traditional identifier world one would use a prefix, e.g. M, and then an integer. This only gives you 100k identifiers (M0 to M99999) with up to 6 characters. The scheme enables consecutive counting and is therefore free of collissions. In particular, it is __not__ a method to create secret identifiers.

## FAQ

__Why no upper case characters?__

Because we don't want to `erdi8` to be confused with `Erdi8`.

__Why no start with a number?__

Because we want to avoid "number-only" identifiers. If we allowed to start with a number we would have identifiers of the type `42` and `322` which could be mistaken for integers. We could achieve this with a more complex scheme avoiding any number-only combinations (would therefore still allow ids like `2z`, to be investigated).
