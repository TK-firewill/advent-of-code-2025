from typing import Callable
from operator import add, mul
from itertools import groupby
from functools import reduce
import re

with open('input') as input:
	lines: list[str] = input.read().splitlines()
	numbers: list[str] = lines[:-1]
	operations: list[str] = lines[-1]

def parse_naive_cephalopod(numbers: list[str], operations: list[str]) -> list[tuple[list[int], Callable]]:
	numbers: list[list[int]] = [[int(number) for number in re.findall(r'\d+', line)] for line in numbers]
	numbers: list[tuple[int, ...]] = zip(*(numbers))
	operations: list[Callable] = [add if op == '+' else mul for op in re.findall(r'(\+|\*)', operations)]
	return list(zip(numbers, operations))

def parse_columns_cephalopod(numbers: list[str], operations: list[str]) -> list[tuple[list[int], Callable]]:
	numbers: list[tuple[str, ...]] = zip(*numbers)
	numbers: list[str] = map(''.join, numbers)
	numbers: list[tuple[re.Match, str]] = groupby(numbers, lambda x: re.match(r'^ +$', x))
	numbers: list[list[str]] = [list(group) for empty, group in numbers if not empty]
	numbers: list[list[int]] = [[int(n.strip(' ')) for n in problem] for problem in numbers]
	operations: list[Callable] = [add if op == '+' else mul for op in re.findall(r'(\+|\*)', operations)]
	return list(zip(numbers, operations))

def solve_problems(problems: list[tuple[list[int], Callable]]) -> int:
	return sum(reduce(lambda x, r: op(r, x), numbers[1:], numbers[0]) for numbers, op in problems)

with open('output', 'w') as output:
    output.write( str( solve_problems(parse_naive_cephalopod(numbers, operations)) ) + '\n')
    output.write( str( solve_problems(parse_columns_cephalopod(numbers, operations)) ) + '\n')