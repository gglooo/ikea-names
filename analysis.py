import os

def analyze(source_name: str) -> None:

    alphabet, duplets, triples = {}, {}, {}
    alph_total, dup_total, trip_total = 0, 0, 0
    
    path = os.getcwd()
    with open(f"{path}/{source_name}", 'r', encoding="utf-8") as f:
        words = f.readlines()

    for word in words:
        for i, letter in enumerate(word.rstrip()):
            alphabet[letter] = alphabet.get(letter, 0) + 1
            alph_total += 1
            if i >= 1:
                duplets[word[i - 1:i + 1]] = duplets.get(word[i-1:i+1], 0) + 1
                dup_total += 1
            if i >= 2:
                triples[word[i - 2:i + 1]] = triples.get(word[i - 2:i + 1], 0) + 1
                trip_total += 1

    with open(f"{path}/analysis.txt", 'w', encoding="utf-8") as f:
        f.write("SINGLE LETTER FREQUENCY\n")
        for letter, count in sorted(alphabet.items()):
           f.write(f"{letter} : {100 * count / alph_total}\n")
        
        f.write("\nBIGRAM LETTER FREQUENCY\n")
        for letter, count in sorted(duplets.items()):
             if 100 * count / dup_total > 0.6:
                f.write(f"{letter} : {100 * count / dup_total}\n")
        
        f.write("\nTRIGRAM LETTER FREQUENCY\n")
        for letter, count in sorted(triples.items()):
            if 100 * count / trip_total > 0.3:
                f.write(f"{letter} : {100 * count / trip_total}\n")


if __name__ == "__main__":
    analyze("result.txt")