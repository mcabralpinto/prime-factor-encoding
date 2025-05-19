from math import sqrt
from typing import List, Dict
from primePy import primes
from dataclasses import dataclass
import os


@dataclass
class PFE_Translator:
    char_num = 256
    max_digits = 7
    chars: Dict[str, str] = None
    inv_chars: Dict[str, str] = None

    def __post_init__(self):
        self.chars = {chr(i): self.pfn(i, True) for i in range(self.char_num)}
        self.inv_chars = {v: k for k, v in self.chars.items()}

    def pfn(self, num: int, char: bool = False) -> str:
        if num == 1:
            return "0" if not char else "0'0'0'0'0'0"
        if num == 0:
            return "()" if not char else "0'0'0'0'0'()"

        prime_list: List[int] = primes.upto(num)
        prime_list.reverse()
        factors: List[int] = primes.factors(num)
        final: str = ""

        for p in prime_list:
            count = 0
            while p in factors:
                count += 1
                factors.remove(p)
            final += f"{count}'"
        final = final[:-1]
        curr: str = final[0]

        while curr == "0" or curr == "'":
            final = final[1:]
            curr = final[0]

        simplified = self.simplify_pfn(final)

        if char:
            count = sum(1 for c in simplified if c in "0123456789")
            if count < self.max_digits:
                simplified = "0'" * (self.max_digits - count) + simplified
        return simplified

    def simplify_pfn(self, unsimplified: str) -> str:
        temp: str = ""
        final: str = ""

        for curr in unsimplified:
            if curr == "'" or curr == "0":
                temp += curr
            else:
                amount = len(temp) // 2
                if amount > 1:
                    new = self.simplify_pfn(self.pfn(amount))
                    final += f"'({new})'"
                else:
                    final += temp
                temp = ""
                # if (not curr.isalpha() and not curr.isnumeric()) and final[-1] == "'": final = final[:-1]
                final += curr

        if len(temp) > 0:
            amount = (len(temp)) // 2
            if amount > 1:
                new = self.simplify_pfn(self.pfn(amount))
                final += f"'({new})"
            else:
                final += temp

        return final

    def unsimplify_pfn(self, simplified: str) -> int:
        final: str = ""
        layer: int = 0
        i: int = 0
        while i != len(simplified):
            if simplified[i] == "(":
                layer += 1
                start: int = i
                while layer != 0:
                    i += 1
                    if simplified[i] == "(":
                        layer += 1
                    elif simplified[i] == ")":
                        layer -= 1
                count: int = self.unsimplify_pfn(simplified[start + 1 : i])
                final += "0"
                for _ in range(count - 1):
                    final += "'0"
            else:
                final += simplified[i]
            i += 1
        return self.normal_num(final)

    def normal_num(self, pfn: str) -> int:
        prime_list: List[int] = primes.first((len(pfn) // 2) + 1)
        prime_list.reverse()
        num: int = 1
        for i in range(len(prime_list)):
            num *= pow(prime_list[i], int(pfn[i * 2]))
        return num

    def pfe(self, text: str) -> str:
        return "'".join([self.chars[char] for char in text])

    def simplify_pfe(self, unsimplified: str) -> str:
        temp: str = ""
        final: str = ""
        prev: str = " "
        for curr in unsimplified:
            if (curr == "'" and prev == "0") or curr == "0":
                temp += curr
            else:
                amount = len(temp) // 2
                if amount > 1:
                    new = self.pfn(amount)
                    final += f"[{new}]'"
                else:
                    final += temp
                temp = ""
                final += curr
            prev = curr

        if len(temp) > 0:
            amount = (len(temp) + 1) // 2
            if amount > 1:
                new = self.pfn(amount)
                final += f"[{new}]"
            else:
                final += temp

        return final

    def unsimplify_pfe(self, simplified: str) -> str:
        final: str = ""
        strlen: int = len(simplified) + 1
        simplified = f" {simplified} "
        layer: int = 0
        i: int = 1
        while i != strlen:
            if simplified[i] == "[" and simplified[i + 1].isnumeric():
                layer += 1
                start: int = i
                while layer != 0:
                    i += 1
                    if simplified[i] == "[":
                        layer += 1
                    elif simplified[i] == "]":
                        layer -= 1
                count: int = self.unsimplify_pfn(simplified[start + 1 : i])
                final += "0"
                for _ in range(count - 1):
                    final += "'0"
            else:
                final += simplified[i]
            i += 1

        return final

    def normal_text(self, pfe: str) -> str:
        num_count: int = 0
        idx: int = 0
        final: str = ""

        for i in range(len(pfe)):
            curr = pfe[i]
            if num_count < self.max_digits:
                num_count += 1 if curr in "0123456789" else 0
            else:
                if curr == "'":
                    final += self.inv_chars[pfe[idx:i]]
                    # print(f"{pfe[idx:i]} -> {self.inv_chars[pfe[idx:i]]}")
                    idx = i + 1
                    num_count = 0
            if i == len(pfe) - 1:
                print(f"{pfe[idx:]} -> {self.inv_chars[pfe[idx:]]}")
                final += self.inv_chars[pfe[idx:]]

        return final

    def convert(self) -> None:
        os.system("cls")
        prompt: str = input("(unicode -> pfe)\n\nprompt: ").lower()

        pfe: str = self.pfe(prompt)
        print(f"\nraw pfe:        {pfe}")
        simplified = self.simplify_pfe(pfe)
        print(f"\nsimplified pfe: {simplified}")

        input("\n\npress enter...")

    def translate(self) -> None:
        os.system("cls")
        prompt: str = input("(pfe -> unicode)\n\nprompt: ").lower()

        pfe: str = self.unsimplify_pfe(prompt)
        print(f"\nraw pfe: {pfe}")
        text: str = self.normal_text(pfe)
        print(f"\nunicode: {text}")

        input("\n\npress enter...")

    # def convert_pure(self) -> None:
    #     os.system("cls")
    #     prompt: str = input("(unicode -> pure pfe)\n\nprompt: ").lower()

    #     count: int = 1
    #     simplified = self.simplify_pfe(self.pfe(prompt))
    #     while any(c in "1234567890" for c in simplified):
    #         simplified = self.simplify_pfe(self.pfe(simplified))
    #         count += 1
    #         print(f"iteration {count}: {simplified[0:10]} ... {simplified[-10:]}")

    #     with open("output.txt", "w") as f:
    #         f.write(simplified)
    #     input(
    #         f"successfully encoded the prompt {count} times and stored it in output.txt"
    #         "\n\npress enter..."
    #     )

    def show_dict(self) -> None:
        os.system("cls")
        print("dictionary:\n")
        for k, v in self.chars.items():
            print(f"{k}: {v}")
        input("\n\npress enter...")

    def run(self) -> None:
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
    translator = PFE_Translator()
    translator.run()


if __name__ == "__main__":
    main()

# There is some useless code left from the previous version, I'll clean it up later