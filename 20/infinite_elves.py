import math


def divisors(n):
    i = 1
    while i <= math.sqrt(n):
        if n % i == 0:
            if n // i == i:
                yield i
            else:
                yield i
                yield n // i
        i += 1


def presents(n, capped=False):
    count = 0
    for div in divisors(n):
        if not capped:
            count += div * 10
        elif capped and div * 50 >= n:
            count += div * 11
    return count


def search(target, capped=False):
    n = 1
    while True:
        if presents(n, capped) >= target:
            return n
        n += 1


def main():
    INPUT = 33100000
    print(f"Part 1: {search(INPUT)}")
    print(f"Part 2: {search(INPUT, capped=True)}")


if __name__ == "__main__":
    main()
