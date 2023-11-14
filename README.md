# Prime Factor Codification

A converter and translator for the Prime Factor Writing System (or PFWS), a code I came up with for fun.

## How It Works

The essence of PFWS is that each alphanumerical character (digit or letter) is to be shown as its equivalent non-ambiguous representation based on its prime factors. As such, it operates under the following ruleset:

- **Codifying Numbers:**

    1. Decompose the number in prime factors;
    2. Count how many times every existing prime factor up until the highest appears in the decomposition;
    3. Sort the counts (highest factor -> lowest factor) and separate them with a single prime character `'`.
    4. For every group of *n* consecutive 0s, replace it with *n* in PFWS enclosed by brackets.

```
Turning 342 into PFWS:

1. 342 = 19 * 3 * 3 * 2
2. 19 appears one time. 17 appears zero times. 13 appears zero times. 11 appears zero times.
   7 appears zero times. 5 appears zero times. 3 appears two times. 2 appears one time.
3. 1 -> 0 -> 0 -> 0 -> 0 -> 0 -> 2 -> 1
4. 1'0'0'0'0'0'2'1 -> 1'(1'0'0)'2'1 -> 1'(1'(1))'2'1

342 in PFWS is 1'(1'(1))'2'1.
```
> **Note**: The single prime character separation is a way to avoid ambiguity. Without it, the number 10, coded in PFWS, could be interpreted as 3¹ * 2⁰ = 3 or 2¹⁰ = 1024!

> **Note 2**: 0 was a tricky number to represent! "()" was the representation I wound up going with, not only because it looks like a 0, but also because the parenthesis represent a sequence of 0s.

- **Codifying Letters:**

    1. Identify its PFWS number (letters a-z correspond to decimal numbers 1-26);
    2. If it has less than four digits, pad it with 0s until the slot for the fourth prime number (7) is filled.

```
Turning "g" into PFWS:

1. g is the seventh letter in the alphabet. 7 is the fourth prime number, and as such its PFWS number is 1'0'0'0 -> 1'(1'0).
2. 1'(1'0) has three digits, therefore it should be padded once: 0'1'(1'0).

"g" in PFWS is 0'1'(1'0).
```

  It would be unpractical to find a letter's code every time it is to be used. Luckily, `pfws.py` pre-stores every letter's code in a dictionary to   further optimize the code:

```python
letters : Dict[str, str] = {"a": "0'0'0'0", "b": "0'0'0'1", "c": "0'0'1'0", "d": "0'0'0'2", "e": "0'0'1'(1)", 
                            "f": "0'0'1'1", "g": "0'1'(1'0)", "h": "0'0'0'3", "i": "0'0'2'0", "j": "0'1'0'1", 
                            "k": "0'0'1'(2)", "l": "0'0'1'2", "m": "0'1'(1'(1))", "n": "0'1'(1)'1", "o": "0'1'1'0",
                            "p": "0'0'0'4", "q": "0'1'(1'1)", "r": "0'0'2'1", "s": "1'(1'(1'0))", "t": "0'1'0'2", 
                            "u": "1'0'1'0", "v": "1'(1'0)'1", "w": "0'0'1'(3)", "x": "0'0'1'3", "y": "0'2'0'0", 
                            "z": "0'1'(2)'1"}
```

  (To be continued)








