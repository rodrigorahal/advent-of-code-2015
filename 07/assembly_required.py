import fileinput
import operator


def parse():
    def parse_wire(wire):
        try:
            return int(wire)
        except Exception:
            return wire

    instructions = []
    for line in fileinput.input():
        ins, out = line.strip().split(" -> ")
        operands = ins.split(" ")
        if len(operands) == 1:  # asignment
            instructions.append([parse_wire(operands[0]), out])
        elif len(operands) == 2:  # single-input operation
            instructions.append([operands[0], parse_wire(operands[1]), out])
        elif len(operands) == 3:  # double-input operation
            instructions.append(
                [parse_wire(operands[0]), operands[1], parse_wire(operands[2]), out]
            )
    return instructions


def assemble(instructions):
    wires = {}
    remaining_instructions = instructions[:]
    while remaining_instructions:
        remaining_instructions = step(remaining_instructions, wires)
    return wires


def step(instructions, wires):
    remaining_instructions = []

    for i, instruction in enumerate(instructions):
        operands, out = instruction[:-1], instruction[-1]

        if len(operands) == 1:  # asignment
            wire_in = operands[0]
            if wire_value(wire_in, wires) is not None:
                wires[out] = wire_value(wire_in, wires)
                break

        elif len(operands) == 2:  # single-input operation
            operation, wire_in = operands
            if wire_value(wire_in, wires) is not None:
                wires[out] = apply(operation, wire_value(wire_in, wires))
                break

        elif len(operands) == 3:  # double-input operation
            wire_in_1, operation, wire_in_2 = operands

            if (
                wire_value(wire_in_1, wires) is not None
                and wire_value(wire_in_2, wires) is not None
            ):
                wires[out] = apply(
                    operation,
                    wire_value(wire_in_1, wires),
                    wire_value(wire_in_2, wires),
                )
                break

        remaining_instructions.append(instruction)

    if i < len(instructions) - 1:
        remaining_instructions.extend(instructions[i + 1 :])

    return remaining_instructions


def wire_value(wire, wires):
    if isinstance(wire, int):
        return wire
    if wire in wires:
        return wires[wire]
    return None


def apply(op, *args):
    if op == "AND":
        return operator.and_(*args)
    if op == "OR":
        return operator.or_(*args)
    elif op == "LSHIFT":
        return operator.lshift(*args)
    elif op == "RSHIFT":
        return operator.rshift(*args)
    elif op == "NOT":
        return operator.and_(operator.inv(*args), 65535)
    else:
        raise ValueError(f"unsupported op {op}")


def main():
    instructions = parse()
    wires = assemble(instructions)
    print(f"Part 1: {wires['a']}")

    # -> b assignment instruction
    instructions[-5] = [wires["a"], "b"]
    wires = assemble(instructions)
    print(f"Part 2: {wires['a']}")


if __name__ == "__main__":
    main()
