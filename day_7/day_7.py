type vector2 = tuple[int, int]

with open('input') as input:
	board: list[str] = input.read().splitlines()
	board: list[list[str]] = [[c for c in row] for row in board]
	start: vector2 = next((0, col) for col in range(len(board[0])) if board[0][col] == 'S')

def solve_tachyon_deterministic(board: list[list[str]], start: vector2) -> int:

	result: int = 0
	beams: set[vector2] = {start}

	for _ in range(start[0], len(board)):
		next_beams: set[vector2] = set()
		for row, col in beams:
			match board[row][col]:
				case 'S' | '.':
					next_beams.add((row + 1, col))
				case '^':
					next_beams.add((row + 1, col - 1))
					next_beams.add((row + 1, col + 1))
					result += 1
				case _:
					pass
		beams = next_beams

	return result

def solve_tachyon_quantic(board: list[list[str]], start: vector2) -> int:

	def below(position: vector2) -> vector2 | None:
		return next(((i, position[1]) for i in range(position[0], len(board)) if board[i][position[1]] == '^'), None)

	timelines_by_splitter: dict[vector2, int] = {None: 1}
	for row, col in [(row, col) for row in reversed(range(len(board))) for col in range(len(board[row])) if board[row][col] in {'^', 'S'}]:
		left : vector2 = timelines_by_splitter[below((row, col-1))]
		right: vector2 = timelines_by_splitter[below((row, col+1))]
		timelines_by_splitter[(row, col)] = left + right
	
	return max(timelines_by_splitter.values())


with open('output', 'w') as output:
    output.write( str( solve_tachyon_deterministic(board, start) ) + '\n')
    output.write( str( solve_tachyon_quantic(board, start) ) + '\n')