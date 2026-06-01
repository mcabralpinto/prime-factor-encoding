import argparse
from dataclasses import dataclass
import os
from typing import Dict, List

from primePy import primes


@dataclass
class PFE_Translator:
    """maps unicode chars to prime-factor encoding and back."""

    char_num = 256
    chars: Dict[str, str] = None
    inv_chars: Dict[str, str] = None
    debug: bool = False

    def __post_init__(self):
        # prime cache must come first: pfn/unsimplify_pfn/normal_num all use it
        self._prime_cache: List[int] = list(primes.first(256))

        raw = {chr(i): self.pfn(i) for i in range(self.char_num)}

        # self-delimiting check on raw pfns before any adjustment.
        # encodings that start with '(' (only "()" currently) are treated as
        # self-delimiting because no other valid pfn shares that prefix.
        initial_no_term = frozenset(
            enc for enc in raw.values()
            if enc.startswith("(") or self.unsimplify_pfn(enc + "0") > 255
        )

        # non-self-delimiting chars get a preceding zero when either:
        #   rule 1 — pfn has 1-3 digits (can be extended to another valid char)
        #   rule 2 — terminator digit > '3' (only checked when rule 1 doesn't apply,
        #             so each char gets at most one preceding zero)
        # both rules are evaluated on the raw pfn form before space conversion.
        pfn_adjusted: Dict[str, str] = {}
        for i in range(self.char_num):
            enc = raw[chr(i)]
            if enc not in initial_no_term:
                digit_count = sum(1 for c in enc if c.isdigit())
                rule1 = 1 <= digit_count <= 3
                rule2 = not rule1 and int(self._terminator(enc)) > 3
                if rule1 or rule2:
                    enc = "0" + enc
            pfn_adjusted[chr(i)] = enc

        # convert every pfn encoding to its parenthesis-free space form.
        # closing-paren runs are disambiguated by inserting (streak_len - 1)
        # immediately after the earliest longest run (see _pfn_to_space).
        self.chars = {ch: self._pfn_to_space(enc) for ch, enc in pfn_adjusted.items()}

        self.inv_chars = {v: k for k, v in self.chars.items()}
        all_encs = set(self.chars.values())
        self.no_term = frozenset(
            enc for enc in all_encs
            if not any(other != enc and other.startswith(enc) for other in all_encs)
        )

        # terminator for space-form encodings: smallest digit d >= 1 such that
        # no space encoding starts with enc + d (prefix-free termination).
        self._term_map: Dict[str, str] = {
            enc: self._terminator_space(enc, all_encs)
            for enc in all_encs
            if enc not in self.no_term
        }
        self._terminated_encs: frozenset = frozenset(
            enc + t for enc, t in self._term_map.items()
        )

    @staticmethod
    def _closing_streaks(enc: str) -> List[tuple]:
        # return (start_pos, length) for every run of consecutive closing parens
        streaks, i = [], 0
        while i < len(enc):
            if enc[i] == ")":
                start = i
                while i < len(enc) and enc[i] == ")":
                    i += 1
                streaks.append((start, i - start))
            else:
                i += 1
        return streaks

    @staticmethod
    def _pfn_to_space(enc: str) -> str:
        # replace ( and ) with spaces; disambiguate by inserting (streak_len - 1)
        # right after the earliest occurrence of the longest closing-paren run.
        streaks = PFE_Translator._closing_streaks(enc)
        if not streaks:
            return enc  # no parens at all — string is already space-form

        max_len  = max(s[1] for s in streaks)
        earliest = min((s for s in streaks if s[1] == max_len), key=lambda s: s[0])
        pos, streak_len = earliest

        before = enc[:pos + streak_len].replace("(", " ").replace(")", " ")
        after  = enc[pos + streak_len:].replace("(", " ").replace(")", " ")

        # collapse consecutive spaces (may arise when parens are adjacent)
        def collapse(s: str) -> str:
            out, prev_sp = [], False
            for c in s:
                if c == " ":
                    if not prev_sp:
                        out.append(" ")
                    prev_sp = True
                else:
                    out.append(c)
                    prev_sp = False
            return "".join(out)

        return collapse(before + str(streak_len - 1) + after)

    @staticmethod
    def _strip_leading_zeros(encoded: str) -> str:
        # drop unused leading 0 tokens from the factor-count stream
        return encoded.lstrip("0") or "0"

    @staticmethod
    def _factor_counts_desc(num: int) -> str:
        # compute prime exponents in descending-prime order as single chars
        prime_list: List[int] = primes.upto(num)
        prime_list.reverse()
        factors: List[int] = primes.factors(num)
        result: List[str] = []

        for p in prime_list:
            count = 0
            while p in factors:
                count += 1
                factors.remove(p)
            result.append(str(count))

        return "".join(result)

    def pfn(self, num: int) -> str:
        if num == 1:
            return "0"
        if num == 0:
            return "()"

        final = self._strip_leading_zeros(self._factor_counts_desc(num))
        return self.simplify_pfn(final)

    def _flush_pfn_temp(self, temp: str) -> str:
        # collapse long zero-runs into recursive parenthesized chunks
        amount = len(temp)
        if amount > 1:
            new = self.simplify_pfn(self.pfn(amount))
            return f"({new})"
        return temp

    def simplify_pfn(self, unsimplified: str) -> str:
        # compress repeated zero patterns while keeping structure intact
        temp: str = ""
        final: str = ""

        for curr in unsimplified:
            if curr == "0":
                temp += curr
            else:
                final += self._flush_pfn_temp(temp)
                temp = ""
                final += curr

        if temp:
            final += self._flush_pfn_temp(temp)

        return final

    def unsimplify_pfn(self, simplified: str) -> int:
        # expand paren groups and compute the integer value of a PFE string
        final: str = ""
        i: int = 0
        while i < len(simplified):
            if simplified[i] == "(":
                layer = 1
                start = i
                while layer != 0:
                    i += 1
                    if simplified[i] == "(":
                        layer += 1
                    elif simplified[i] == ")":
                        layer -= 1
                count = self.unsimplify_pfn(simplified[start + 1:i])
                final += "0" * count
            else:
                final += simplified[i]
            i += 1
        return self.normal_num(final)

    def normal_num(self, pfn: str) -> int:
        # rebuild numeric value from exponent stream and prime bases
        if not pfn:
            return 1
        length = len(pfn)
        # extend prime cache if the exponent stream is longer than expected
        while len(self._prime_cache) < length:
            self._prime_cache = list(primes.first(len(self._prime_cache) * 2))
        num: int = 1
        for i in range(length):
            exp = int(pfn[i])
            if exp:
                num *= pow(self._prime_cache[length - 1 - i], exp)
        return num

    def _nth_prime(self, n: int) -> int:
        # return the (n+1)-th prime (0-indexed); extend the cache if needed
        while len(self._prime_cache) <= n:
            self._prime_cache = list(primes.first(len(self._prime_cache) * 2))
        return self._prime_cache[n]

    def _terminator(self, encoded: str) -> str:
        # first digit d >= 1 such that appending it pushes the decoded value above 255
        # used only on raw pfn encodings during __post_init__ (rule 2 check).
        for d in range(1, 10):
            if self.unsimplify_pfn(encoded + str(d)) > 255:
                return str(d)
        raise ValueError(f"no terminator found for {encoded!r}")

    def _terminator_space(self, space_enc: str, all_encs: set) -> str:
        # first digit d >= 1 such that no space encoding starts with space_enc + d.
        # this guarantees the terminated token is unambiguous in the output stream.
        for d in range(1, 10):
            candidate = space_enc + str(d)
            if not any(enc.startswith(candidate) for enc in all_encs):
                return str(d)
        raise ValueError(f"no space-form terminator found for {space_enc!r}")

    def pfe(self, text: str) -> str:
        # CBC transform then encode each char; terminator omitted if already self-delimiting.
        # trailing space is stripped from the final token: it is unambiguous within a
        # sequence (the next token always begins with a digit) but redundant at the end.
        result = []
        prev = 0
        for n, char in enumerate(text):
            val = (ord(char) + prev + self._nth_prime(n)) % 256
            prev = val
            encoded = self.chars[chr(val)]
            if encoded not in self.no_term:
                encoded += self._term_map[encoded]
            if self.debug:
                print(f"  {char!r:4s} -> {encoded}")
            result.append(encoded)
        if result and result[-1].endswith(" "):
            result[-1] = result[-1][:-1]
        return "".join(result)

    def normal_text(self, pfe: str) -> str:
        # encodings are now parenthesis-free (digits and spaces only), so token
        # boundaries are found purely by prefix-matching against no_term /
        # _terminated_encs — no depth tracking needed.
        final: str = ""
        i: int = 0
        prev, n = 0, 0
        while i < len(pfe):
            start = i
            terminated = False
            while i < len(pfe):
                i += 1
                accum = pfe[start:i]
                if accum in self._terminated_encs:
                    terminated = True
                    break
                if accum in self.no_term:
                    break
            natural_pfe = pfe[start:i - 1] if terminated else pfe[start:i]
            # if end of input was reached and the token is not found, try
            # appending a space — handles trailing-space encodings whose final
            # space was stripped by pfe() or omitted by the user.
            if natural_pfe not in self.inv_chars and natural_pfe + " " in self.inv_chars:
                natural_pfe += " "
            val = ord(self.inv_chars[natural_pfe])
            decoded = chr((val - prev - self._nth_prime(n)) % 256)
            if self.debug:
                print(f"  {natural_pfe:20s} -> {decoded!r}")
            final += decoded
            prev, n = val, n + 1
        return final

    def convert(self) -> None:
        # interactive unicode -> pfe flow
        os.system("cls")
        prompt: str = input("(unicode -> pfe)\n\nprompt: ")

        pfe: str = self.pfe(prompt)
        print(f"\npfe: {pfe}")

        input("\n\npress enter...")

    def translate(self) -> None:
        # interactive pfe -> unicode flow
        os.system("cls")
        prompt: str = input("(pfe -> unicode)\n\nprompt: ")

        text: str = self.normal_text(prompt)
        print(f"\nunicode: {text}")

        input("\n\npress enter...")

    def show_dict(self) -> None:
        # print full char <-> code dictionary
        os.system("cls")
        print("dictionary:\n")
        for k, v in self.chars.items():
            print(f"{k}: {v}")
        input("\n\npress enter...")

    def run(self) -> None:
        # simple cli menu loop
        while True:
            os.system("cls")
            print(
                "1. unicode -> pfe\n2. pfe -> unicode\n"
                "3. see dictionary\n4. leave\n"
            )
            opt: str = input("> choose (1 - 4): ")
            match opt:
                case "1":
                    self.convert()
                case "2":
                    self.translate()
                case "3":
                    self.show_dict()
                case "4":
                    break
                case _:
                    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", choices=["pfe", "uni"])
    parser.add_argument("--debug", action="store_true",
                        help="print per-character mappings after each encode/decode")
    args = parser.parse_args()

    translator = PFE_Translator(debug=args.debug)

    if args.file:
        os.makedirs("data", exist_ok=True)
        with open(os.path.join("data", "input.txt"), "r", encoding="utf-8") as f:
            content = f.read()

        if args.file == "pfe":
            result = translator.pfe(content)
        else:
            result = translator.normal_text(content)

        with open(os.path.join("data", "output.txt"), "w", encoding="utf-8") as f:
            f.write(result)

        print("written to data/output.txt")
    else:
        translator.run()


if __name__ == "__main__":
    main()
