from itertools import accumulate
import re

with open('input') as input:
    instructions: list[str] = input.read().splitlines()
    instructions: list[tuple[str, str]] = [re.match(r'(R|L)(\d+)', instruction).groups() for instruction in instructions]
    instructions: list[int] = [(1 if direction == 'R' else -1) * int(amount) for direction, amount in instructions]

def zero_end(start: int, instructions: list[int]) -> list[int]:
    points = accumulate(instructions, lambda x, y: (x + y) % 100, initial=start)
    return sum(map(lambda x: x == 0, points))

def zero_pass(start: int, instructions: list[int]) -> list[int]:
    points = accumulate(instructions, lambda x, y: divmod(x[1] + y, 100), initial=(0, start))
    return sum(map(lambda x: abs(x[0]), points))
    
with open('output', 'w') as output:
    output.write( str(zero_end(50, instructions)) + '\n')
    output.write( str(zero_pass(50, instructions)) + '\n')