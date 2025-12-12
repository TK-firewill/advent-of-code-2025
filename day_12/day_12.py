import re

with open('input') as input:
	input_bundle: list[str] = input.read().split('\n\n')
	present_sizes: list[int] = [package.count('#') for package in input_bundle[:-1]]

	input_trees = input_bundle[-1].split('\n')
	trees = [map(int, re.findall(r'(\d+)', tree)) for tree in input_trees]

solvable = 0

def can_fit_presents(present_sizes: list[int], tree: list[int]) -> bool:
	n, m, *presents = tree
	required_size = sum([c * s for c, s in zip(presents, present_sizes)])
	return n * m - required_size > 0

with open('output', 'w') as output:
    output.write( str( sum(1 for tree in trees if can_fit_presents(present_sizes, tree)) ) + '\n')