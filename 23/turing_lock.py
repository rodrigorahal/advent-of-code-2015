import fileinput


def parse():
    tape = []
    for line in fileinput.input():
        words = line.strip().split(" ")
        cmd = words[0]
        reg = words[1].strip(",")
        args = [reg]
        if len(words) > 2:
            args.append(int(words[2]))
        tape.append((cmd, args))
    return tape


def run(tape, regs):
    idx = 0
    while idx < len(tape):
        cmd, args = tape[idx]
        reg = args[0]

        if cmd == "hlf":
            regs[reg] //= 2

        elif cmd == "tpl":
            regs[reg] *= 3

        elif cmd == "inc":
            regs[reg] += 1

        elif cmd == "jmp":
            offset = int(reg)
            idx += offset
            continue

        elif cmd == "jie":
            offset = args[1]
            if regs[reg] % 2 == 0:
                idx += offset
                continue

        elif cmd == "jio":
            offset = args[1]
            if regs[reg] == 1:
                idx += offset
                continue

        idx += 1

    return regs


def main():
    tape = parse()
    regs = run(tape, {"a": 0, "b": 0})
    print(f"Part 1: {regs['b']}")
    regs = run(tape, {"a": 1, "b": 0})
    print(f"Part 2: {regs['b']}")


if __name__ == "__main__":
    main()
