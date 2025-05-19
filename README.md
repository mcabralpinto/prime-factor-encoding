# Prime Factor Encoding

A converter and translator for the refactored Prime Factor Encoding (or PFE), an encoding method I came up with for fun.

## main.py

The Python file in which the program is coded. Upon running it, the user will be greeted with a console menu allowing the user to:
   1. Encode a message
   2. Decode a message
   3. See character - encoding correspondences
   3. End the program

## How It Works

The essence of PFE is that each Unicode character can be shown as its equivalent non-ambiguous representation based on its Unicode value's prime factors. As such, it operates under the following ruleset:

### Encoding Numbers

1. Decompose the number in prime factors;
2. Count how many times each existing prime factor appears in the decomposition;
3. Sort the counts (highest factor → lowest factor) and separate them with a single quote character `'`;
4. For every group of *n* consecutive 0s, replace it with *n* in PFE enclosed by parenthesis `( ... )`.

```
Converting 342 into PFE:

1. 342 = 19 * 3 * 3 * 2
2. 19 appears one time. 17 appears zero times. 13 appears zero times. 11 appears zero times.
   7 appears zero times. 5 appears zero times. 3 appears two times. 2 appears one time.
3. 1 → 0 → 0 → 0 → 0 → 0 → 2 → 1
4. 1'0'0'0'0'0'2'1 → 1'(1'0'0)'2'1 → 1'(1'(1))'2'1

342 in PFE is 1'(1'(1))'2'1.
```
> **Note**: The single quote character separation is a way to avoid ambiguity. Without it, the number 10, encoded in PFE, could be interpreted as 3¹ * 2⁰ = 3 or 2¹⁰ = 1024!

<!-- > **Note 2**: 0 was a tricky number to represent! `()` was the representation I wound up going with, not only because it looks like a 0, but also because the parenthesis represent a sequence of 0s. -->

### Encoding Characters

The program initially populates a dictionary with the code for every Unicode character by:
1. Converting its unicode value into PFE.
2. If the resulting string has less than seven digits, pad it with preceding 0s until it reaches that amount (this is done because the max number of digits an encoded PFE number in the range of 0 to 255 can have is seven, so by padding every character becomes seven digits long, making it uniquely identifiable).

```
Converting "a" into PFE:

1. "a" has a Unicode value of 97, which is the twenty fifth prime number, and as such its PFE number is 1'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0'0 → 1'(1'3).
2. 1'(1'3) has three digits, therefore it should be padded four times: 0'0'0'0'1'(1'3).

"a" in PFE is 0'0'0'0'1'(1'3).
```

> **Note**: Inputted numbers are treated as characters. 

### Encoding Expressions

1. Every Unicode character is replaced with its corresponding PFE encoding and separated from their neighbors with a single quote character `'`.
2. In the same way numbers can be simplified, groups of *n* consecutive 0s formed by letters should be replaced with *n* in PFE enclosed by square brackets `[ ... ]`.

```
Converting "yolo 2025" into PFE:

---SYMBOL CONVERSION---
y → 0'0'0'0'0'2'(2)
o → 0'0'1'(2'0)'1'0
l → 0'0'0'0'0'3'2
o → 0'0'1'(2'0)'1'0
  → 0'0'0'0'0'0'5
2 → 0'0'0'0'2'0'1
0 → 0'0'0'0'0'1'4
2 → 0'0'0'0'2'0'1
5 → 0'0'0'1'(1'1'0)

"pf20 ws23" in PFE is 0'0'0'0'0'2'(2)'0'0'1'(2'0)'1'0'0'0'0'0'0'3'2'0'0'1'(2'0)'1'0'0'0'0'0'0'0'5'0'0'0'0'2'0'1'0'0'0'0'0'1'4'0'0'0'0'2'0'1'0'0'0'1'(1'1'0)   (rule 1)
                    → [1'(1)]'2'(2)'[1]'1'(2'0)'1'[1'1]'3'2'[1]'1'(2'0)'1'[1'(1'0)]'5'[2]'2'0'1'[1'(1)]'1'4'[2]'2'0'1'[1'0]'1'(1'1'0)   (rule 2)
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
