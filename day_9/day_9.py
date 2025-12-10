import re
from itertools import product
type Vector2 = tuple[int, int]
type Line    = tuple[Vector2, Vector2]

with open('input') as input:
	red_tiles: list[str] = input.read().splitlines()
	red_tiles: list[Vector2] = [tuple(map(int, re.findall(r'\d+', tile))) for tile in red_tiles]

def inside(v: Vector2, lines: set[Line]) -> bool:
	x, y = v
	above: bool = any([(b == d) and y >= b and min(a, c) <= x <= max(a, c) for (a, b), (c, d) in lines])
	right: bool = any([(a == c) and x <= a and min(b, d) <= y <= max(b, d) for (a, b), (c, d) in lines])
	below: bool = any([(b == d) and y <= b and min(a, c) <= x <= max(a, c) for (a, b), (c, d) in lines])
	left : bool = any([(a == c) and x >= a and min(b, d) <= y <= max(b, d) for (a, b), (c, d) in lines])
	return above and right and below and left

def intersects_hv(s: Line, t: Line) -> Vector2 | None:
	a, b = s
	p, q = t
	if min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(p[1], q[1]) <= a[1] <= max(p[1], q[1]):
		return (p[0], a[1])
	else:
		return None

def area(v: Vector2, w: Vector2) -> int:
	return (abs(v[0] - w[0]) + 1) * (abs(v[1] - w[1]) + 1)

areas = [area(v, w) for v, w in product(red_tiles, red_tiles)]

lines: list[Line] = list(zip(red_tiles, red_tiles[1:] + red_tiles[:1]))

horizontal_lines: list[Line] = [line for line in lines if line[0][1] == line[1][1]]
vertical_lines: list[Line] = [line for line in lines if line[0][0] == line[1][0]]

best = 0
for v, w in product(red_tiles, red_tiles):
	if area(v, w) > best:
		a, b, c, d = min(v[0], w[0]), max(v[0], w[0]), min(v[1], w[1]), max(v[1], w[1])
		p, q, r, s = ((a + 1, d), (b - 1, d)), ((b, d - 1), (b, c + 1)), ((b - 1, c), (a + 1, c)), ((a, c + 1), (a, d - 1))

		intersects_p = [intersects_hv(p, line) for line in vertical_lines if intersects_hv(p, line) != None]
		intersects_r = [intersects_hv(r, line) for line in vertical_lines if intersects_hv(r, line) != None]

		intersects_p = [(col + 1, row) for col, row in intersects_p if col + 1 < b] + [(col - 1, row) for col, row in intersects_p if col - 1 > a]
		intersects_r = [(col + 1, row) for col, row in intersects_r if col + 1 < b] + [(col - 1, row) for col, row in intersects_r if col - 1 > a]

		intersects_q = [intersects_hv(line, q) for line in horizontal_lines if intersects_hv(line, q) != None]
		intersects_s = [intersects_hv(line, s) for line in horizontal_lines if intersects_hv(line, s) != None]

		intersects_q = [(col, row + 1) for col, row in intersects_q if row + 1 < d] + [(col, row - 1) for col, row in intersects_q if row - 1 > c]
		intersects_s = [(col, row + 1) for col, row in intersects_s if row + 1 < d] + [(col, row - 1) for col, row in intersects_s if row - 1 > c]

		critical_points = [p[0], p[1], q[0], q[1], r[0], r[1], s[0], s[1]] + intersects_p + intersects_q + intersects_r + intersects_s
			
		any_outside = any(not inside(p, lines) for p in critical_points)
		if not any_outside:
			best = area(v, w)		

with open('output', 'w') as output:
    output.write( str( max(areas) ) + '\n')
    output.write( str( best ) + '\n')