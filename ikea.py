from random import randint
from data import Data
import os


def write_n_words(filename: str, num: int) -> None:
    """ Generates and writes <num> amount of words
    into given file."""
    path = f"{os.getcwd()}/{filename}"
    with open(path, "w", encoding="utf-8") as x:
        for _ in range(num):
            word = ""
            data = Data()
            length = randint(3, 9)
            for __ in range(length):
                letter = data.get_letter(length, word)
                word += letter
            x.write(word + "\n")


def generate(length=randint(3, 9)) -> str:
    """Returns one generated ikea word."""
    word = ''
    data = Data()
    for _ in range(length):
        letter = data.get_letter(length, word)
        word += letter
    return word


if __name__ == "__main__":
    write_n_words("result.txt", 10000)
