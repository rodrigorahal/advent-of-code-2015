import fileinput


def parse():
    words = []
    for line in fileinput.input():
        word = line.strip()
        words.append(word)
    return words


def count(words):
    chars = in_mem_chars = encoded_chars = 0

    for word in words:
        escaped = word.encode("ascii").decode("unicode_escape")[1:-1]
        encoded = word.encode("unicode_escape").replace(b'"', b'\\"')
        chars += len(word)
        in_mem_chars += len(escaped)
        encoded_chars += len(encoded) + 2
    return chars, in_mem_chars, encoded_chars


def main():
    words = parse()
    chars, in_mem_chars, encoded_chars = count(words)
    print(f"Part 1: {chars - in_mem_chars}")
    print(f"Part 2: {encoded_chars - chars}")


if __name__ == "__main__":
    main()
