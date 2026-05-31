# Prime Factor Encoding

A converter and translator for the refactored Prime Factor Encoding (or PFE), an encoding method I came up with for fun.

## main.py

The Python file in which the program is coded. Upon running it, the user will be greeted with a console menu allowing the user to:
   1. Encode a message
   2. Decode a message
   3. See character–encoding correspondences
   4. End the program

It also supports `--file pfe` (encode `data/input.txt` → `data/output.txt`) and `--debug` (print per-character mappings).

## How It Works

The essence of PFE is that each Unicode character can be shown as its equivalent non-ambiguous representation based on its Unicode value's prime factors. As such, it operates under the following ruleset:

### Encoding Numbers

1. Decompose the number into prime factors;
2. Count how many times each prime factor appears (its exponent), sorted from highest prime to lowest;
3. Concatenate the exponents;
4. For every consecutive run of *n* zeros (*n* > 1), replace it with *n* in PFE enclosed by parentheses `(...)`.

```
Converting 342 into PFE:

1. 342 = 19¹ × 3² × 2¹
2. 19 appears once. 17 zero times. 13 zero times. 11 zero times.
   7 zero times. 5 zero times. 3 twice. 2 once.
3. 10000021
4. 10000021 → 1(1(1))21

342 in PFE is 1(1(1))21.
```

> **Note**: Exponents are concatenated without separators because, in the range 0–255, no prime factor can appear more than 7 times (2⁸ = 256 > 255), so every exponent is a single digit. Parenthesised groups are always unambiguous because they are explicitly bounded.

### Encoding Characters

Each Unicode character (values 0–255) is assigned a fixed PFE code:
1. Compute the PFE of its Unicode value.
2. If the resulting code could be mistaken for the prefix of another character's code, prepend a `0` to disambiguate.
3. Convert to *space form*: replace every `(` and `)` with a space. To allow unambiguous decoding, a digit equal to `(run_length − 1)` is inserted immediately after the earliest occurrence of the longest consecutive run of `)`.

```
Converting '@' into PFE:

1. '@' has Unicode value 64 = 2⁶, so its raw PFE is 6.
2. Appending any digit to "6" would decode to a number ≥ 3⁶ = 729 > 255,
   so no other valid code can start with "6" — no adjustment needed.
3. "6" contains no parentheses, so space form is unchanged.

'@' in PFE is 6.

Converting ' ' (space) into PFE:

1. Space has Unicode value 32 = 2⁵, so its raw PFE is 5.
2. "5" alone is too short to rule out a longer valid code starting with it,
   so a leading 0 is prepended: "05".
3. "05" contains no parentheses, so space form is unchanged.

' ' in PFE is 05.

Converting 'h' into PFE:

1. 'h' has Unicode value 104 = 2³ × 13, so its raw PFE is 1(2)3.
2. Appending "0" to "1(2)3" would decode to 459 > 255,
   so no other valid code can start with "1(2)3" — no adjustment needed.
3. Replace ( and ) with spaces. The single ) forms a run of length 1,
   so insert 1 − 1 = 0 right after it: 1(2)3 → 1 2 03.

'h' in PFE is 1 2 03.
```

> **Note**: Inputted numbers are interpreted as Unicode characters. The final codes use only digits and spaces.

### Encoding Expressions

Encoding a string applies a cipher-block-chaining (CBC) transform before substituting each character, so the same character encodes differently depending on its position:

1. For each character at index *n*, compute its shifted Unicode value: `val = (unicode + prev + prime(n)) mod 256`, where `prev` is the shifted value of the previous character (0 at the start) and `prime(n)` is the (*n*+1)-th prime;
2. Look up the shifted value's space-form code;
3. If that code is not self-delimiting, append a terminator — the smallest digit ≥ 1 that no other character's code starts with when appended;
4. Concatenate all codes with no separator.

```
Converting "hello" into PFE:

---CHARACTER CONVERSION (with CBC shift)---
'h'  → 1 1 1 01 11
'e'  → 1111
'l'  → 01 21 0
'l'  → 101 1 01        (same letter, different position → different code)
'o'  → 14

"hello" in PFE is 1 1 1 01 11111101 21 0101 1 0114
```

<!-- ### *N*-th order codifications

Since this codification method is non-ambiguous, you can run it on a given message and its successive code any given *n* times - creating an *n*-th order codification for the message - and then decodify it the same *n* times to obtain the original text. <br />
A given message's *n*-th order codification is said to be its pure codification if it is the first in which there are no digits.

```
Finding the pure codification for "PFE":

→ PFE
→ '[1'0]'4'[1]'1'1'[1]'1'(3)'1'(1'(1'0))
→ ''''['''()'''''''(')''']'''''''1'''''''['''()''']'''''''()'''''''()'''''''['''()''']'''''''()'''''''('''0'''()''')'''''''()'''''''('''()'''''''('''()'''''''(')''')''')
→ ''''''''['''''''(')'''''''''''''''(''')''''''']'''''''''''''''0'''''''''''''''['''''''(')''''''']'''''''''''''''(')'''''''''''''''(')'''''''''''''''['''''''(')''''''']'''''''''''''''(')'''''''''''''''('''''''()'''''''(')''''''')'''''''''''''''(')'''''''''''''''('''''''(')'''''''''''''''('''''''(')'''''''''''''''(''')''''''')''''''')
→ ''''''''''''''''['''''''''''''''(''')'''''''''''''''''''''''''''''''(''''''')''''''''''''''']'''''''''''''''''''''''''''''''()'''''''''''''''''''''''''''''''['''''''''''''''(''')''''''''''''''']'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''['''''''''''''''(''')''''''''''''''']'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''('''''''''''''''(')'''''''''''''''(''')''''''''''''''')'''''''''''''''''''''''''''''''(''')'''''''''''''''''''''''''''''''('''''''''''''''(''')'''''''''''''''''''''''''''''''('''''''''''''''(''')'''''''''''''''''''''''''''''''(''''''')''''''''''''''')''''''''''''''')

The pure codification for "PFE" is its 4th order codification.
``` -->

## License

This project is licensed under the [MIT License](LICENSE).
