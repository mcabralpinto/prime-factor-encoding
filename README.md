# Prime Factor Encoding

A converter and translator for the Prime Factor Codification / Writing System (or PFWS), a code I came up with for fun.

## pfws.py

The Python file in which the program is coded. Upon running it, the user will be greeted with a console menu allowing the user to:
   1. Encode a message;
   2. Decode a message;
   3. End the program.

## How It Works

The essence of PFWS is that each alphanumerical character (digit or letter) is to be shown as its equivalent non-ambiguous representation based on its prime factors. As such, it operates under the following ruleset:

### Encoding Numbers

1. Decompose the number in prime factors;
2. Count how many times every existing prime factor up until the highest appears in the decomposition;
3. Sort the counts (highest factor -> lowest factor) and separate them with a single quote character `'`;
4. For every group of *n* consecutive 0s, replace it with *n* in PFWS enclosed by parenthesis `( ... )`.

```
Converting 342 into PFWS:

1. 342 = 19 * 3 * 3 * 2
2. 19 appears one time. 17 appears zero times. 13 appears zero times. 11 appears zero times.
   7 appears zero times. 5 appears zero times. 3 appears two times. 2 appears one time.
3. 1 -> 0 -> 0 -> 0 -> 0 -> 0 -> 2 -> 1
4. 1'0'0'0'0'0'2'1 -> 1'(1'0'0)'2'1 -> 1'(1'(1))'2'1

342 in PFWS is 1'(1'(1))'2'1.
```
> **Note**: The single quote character separation is a way to avoid ambiguity. Without it, the number 10, encoded in PFWS, could be interpreted as 3¹ * 2⁰ = 3 or 2¹⁰ = 1024!

> **Note 2**: 0 was a tricky number to represent! `()` was the representation I wound up going with, not only because it looks like a 0, but also because the parenthesis represent a sequence of 0s.

### Encoding Letters

1. Identify its PFWS number (letters a - z correspond to decimal numbers 1 - 26);
2. If it has less than four digits, pad it with 0s until the slot for the fourth prime number (7) is filled.

```
Converting "g" into PFWS:

1. g is the seventh letter in the alphabet. 7 is the fourth prime number, and as such its PFWS number is 1'0'0'0 -> 1'(1'0).
2. 1'(1'0) has three digits, therefore it should be padded once: 0'1'(1'0).

"g" in PFWS is 0'1'(1'0).
```

It would be unpractical to find a letter's code every time it is to be used. Luckily, `pfws.py` pre-stores every letter's specific code in a dictionary to further optimize the program:

```python
letters : Dict[str, str] = {"a": "0'0'0'0", "b": "0'0'0'1", "c": "0'0'1'0", "d": "0'0'0'2", "e": "0'0'1'(1)", 
                            "f": "0'0'1'1", "g": "0'1'(1'0)", "h": "0'0'0'3", "i": "0'0'2'0", "j": "0'1'0'1", 
                            "k": "0'0'1'(2)", "l": "0'0'1'2", "m": "0'1'(1'(1))", "n": "0'1'(1)'1", "o": "0'1'1'0",
                            "p": "0'0'0'4", "q": "0'1'(1'1)", "r": "0'0'2'1", "s": "1'(1'(1'0))", "t": "0'1'0'2", 
                            "u": "1'0'1'0", "v": "1'(1'0)'1", "w": "0'0'1'(3)", "x": "0'0'1'3", "y": "0'2'0'0", 
                            "z": "0'1'(2)'1"}
```

### Encoding Expressions

1. PFWS letters, numbers and symbols are connected by single quote characters. If a letter is following a non-letter character or if a number is following a letter, it should include an extra single quote to avoid ambiguity between letters and numbers.
2. In the same way numbers can be simplified, groups of *n* consecutive 0s formed by letters should be replaced with *n* in PFWS enclosed by square brackets `[ ... ]`.
3. Whitespace is awarded a special character `[]` in the PFWS system, as a symbolic representation of an empty character.
4. Every other character has the same representation as they would in the regular writing system.

```
Converting "pf20 ws23" into PFWS:

---SYMBOL CONVERSION---
"p" -> 0'0'0'4
"f" -> 0'0'1'1
"20" -> 1'0'2
" " -> [] (rule 3)
"w" -> 0'0'1'(3)
"s" -> 1'(1'(1'0))
"23" -> 1'(3)

"pf20 ws23" in PFWS is '0'0'0'4'0'0'1'1''1'0'2'[]''0'0'1'(3)'1'(1'(1'0))''1'(3)   (rule 1)
                    -> '[1'0]'4'[1]'1'1''1'0'2'[]''[1]'1'(3)'1'(1'(1'0))''1'(3)   (rule 2)
```

```
Converting "2 + 2 = 4" into PFWS:

---SYMBOL CONVERSION---
"2" -> 1
" " -> [] (rule 3)
"+" -> + (rule 4)
"=" -> = (rule 4)
"4" -> 2

"2 + 2 = 4" in PFWS is 1'[]'+'[]'1'[]'='[]'2   (rule 1)
```

### *N*-th order codifications

Since this codification method is non-ambiguous, you can run it on a given message and its successive code any given *n* times - creating an *n*-th order codification for the message - and then decodify it the same *n* times to obtain the original text. <br />
A given message's *n*-th order codification is said to be its pure codification if it is the first in which there are no digits.

```
Finding the pure codification for "pfws":

-> pfws
-> '[1'0]'4'[1]'1'1'[1]'1'(3)'1'(1'(1'0))
-> ''''['''()'''''''(')''']'''''''1'''''''['''()''']'''''''()'''''''()'''''''['''()''']'''''''()'''''''('''0'''()''')'''''''()'''''''('''()'''''''('''()'''''''(')''')''')
-> ''''''''['''''''(')'''''''''''''''(''')''''''']'''''''''''''''0'''''''''''''''['''''''(')''''''']'''''''''''''''(')'''''''''''''''(')'''''''''''''''['''''''(')''''''']'''''''''''''''(')'''''''''''''''('''''''()'''''''(')''''''')'''''''''''''''(')'''''''''''''''('''''''(')'''''''''''''''('''''''(')'''''''''''''''(''')''''''')''''''')
-> ''''''''''''''''['''''''''''''''(''')'''''''''''''''''''''''''''''''(''''''')''''''''''''''']'''''''''''''''''''''''''''''''()'''''''''''''''''''''''''''''''['''''''''''''''(''')''''''''''''''']'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''['''''''''''''''(''')''''''''''''''']'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''('''''''''''''''(')'''''''''''''''(''')''''''''''''''')'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''('''''''''''''''(''')'''''''''''''''''''''''''''''''('''''''''''''''(''')'''''''''''''''''''''''''''''''(''''''')''''''''''''''')''''''''''''''')

The pure codification for "pfws" is its 4th order codification.
```

## License

This project is licensed under the [MIT License](LICENSE).
