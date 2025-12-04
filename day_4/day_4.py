from itertools import product

with open('input') as input:
    warehouse: list[str] = input.read().splitlines()
    warehouse: list[list[str]] = [[tile for tile in row] for row in warehouse]


def all_indices(warehouse: list[str]) -> list[tuple[int, int]]:
	return list(product(range(len(warehouse)), range(len(warehouse[0]))))

def all_roll_indices(warehouse: list[str]) -> list[tuple[int, int]]:
	return set(filter(lambda t: warehouse[t[0]][t[1]] == '@', all_indices(warehouse)))


def in_range(warehouse: list[str], row: int, col: int) -> bool:
    return 0 <= row < len(warehouse) and 0 <= col < len(warehouse[0])

def index_neighbours(warehouse: list[str], row: int, col: int) -> list[tuple[int, int]]:
	return [(row+y, col+x) for y, x in product([-1, 0, 1], [-1, 0, 1]) if (x != 0 or y != 0) and in_range(warehouse, row+y, col+x)]

def neighbours(warehouse: list[str], row: int, col: int) -> list[str]:
	return [warehouse[y][x] for y, x in index_neighbours(warehouse, row, col)]

def accessible(warehouse: list[str], row: int, col: int) -> bool:
	return neighbours(warehouse, row, col).count('@') < 4

def accessible_rolls(warehouse: list[str], candidates: set[tuple[int, int]]) -> set[tuple[int, int]]:
	return {(row, col) for row, col in candidates if accessible(warehouse, row, col)}

def all_accessible_rolls(warehouse: list[str]) -> set[tuple[int, int]]:
	warehouse = [[tile for tile in row] for row in warehouse]
	result: set[tuple[int, int]] = set()
	candidates: set[tuple[int, int]] = all_roll_indices(warehouse)

	while len(currently_accessible_rolls := accessible_rolls(warehouse, candidates)) != 0:
		for row, col in currently_accessible_rolls:
			warehouse[row][col] = '.'
		result = result.union(currently_accessible_rolls)
		candidates = [(y, x) for candidate in currently_accessible_rolls for y, x in index_neighbours(warehouse, *candidate) if warehouse[y][x] == '@']

	return result

with open('output', 'w') as output:
    output.write( str( len(accessible_rolls(warehouse, all_roll_indices(warehouse)))) + '\n')
    output.write( str( len(all_accessible_rolls(warehouse))) + '\n')
    pass