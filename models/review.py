from dataclasses import dataclass
import json
from colorama import Fore, Style


@dataclass
class Review:
    file_name: str
    text: str
    subjectivity: float
    polarity: float

    def print(self):
        print()
        print(f"File Name: {self.file_name}")
        self.print_subjectivity()
        self.print_polarity()
        print()
        print(f"{self.text}")

    def print_subjectivity(self):
        if self.subjectivity >=0.5:
            print(Style.BRIGHT + Fore.YELLOW + f"Subjectivity: {self.subjectivity}")
        else:
            print(Style.DIM + Fore.WHITE + f"Subjectivity: {self.subjectivity}")
        print(Style.RESET_ALL, end='')

    def print_polarity(self):
        if self.polarity > 0:
            print(Style.BRIGHT + Fore.GREEN + f"Polarity: {self.polarity}")
        elif self.polarity == 0:
            print(Style.DIM + Fore.WHITE + f"Polarity: {self.polarity}")
        else:
            print(Style.BRIGHT + Fore.RED + f"Polarity: {self.polarity}")
        print(Style.RESET_ALL, end='')