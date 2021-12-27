from hashlib import md5


def search(key, zeroes=5):
    for n in range(1, int(10e6)):
        if md5(f"{key}{n}".encode("ascii")).hexdigest().startswith("0" * zeroes):
            return n


def main():
    n = search("ckczppom", zeroes=5)
    print(f"Part 1: {n}")

    n = search("ckczppom", zeroes=6)
    print(f"Part 2: {n}")


if __name__ == "__main__":
    main()
