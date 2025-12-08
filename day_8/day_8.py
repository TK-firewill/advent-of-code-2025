import re
from math import prod
from itertools import product
type vector3 = tuple[int, int, int]

with open('input') as input:
	junction_boxes: list[str] = input.read().splitlines()
	junction_boxes: list[vector3] = [tuple(map(int, re.findall(r'\d+', junction_box))) for junction_box in junction_boxes]

def distance(v: vector3, w: vector3) -> float:
	return (v[0] - w[0])**2 + (v[1] - w[1])**2 + (v[2] - w[2])**2

def solve_N_closest_junction_boxes(junction_boxes: list[vector3], n: int) -> int:

	box2connections: dict[vector3, frozenset[vector3]] = {junction_box: frozenset() for junction_box in junction_boxes}
	box2circuit: dict[vector3, frozenset[vector3]] = {junction_box: frozenset({junction_box}) for junction_box in junction_boxes}

	pairs = iter(sorted([(v, w) for v, w in product(junction_boxes, repeat=2) if v != w], key=lambda vw: distance(*vw)))

	while sum(map(len, box2connections.values())) // 2 < n:
		v, w = next(pairs)
		
		if w not in box2connections[v]:
			vw_circuit: frozenset[vector3] = box2circuit[v].union(box2circuit[w])
			for u in vw_circuit:
				box2circuit[u] = vw_circuit
			box2connections[v] = box2connections[v].union([w])
			box2connections[w] = box2connections[w].union([v])
	
	circuits: set[frozenset[vector3]] = set(s for s in box2circuit.values())
	circuit_sizes: list[int] = [len(circuit) for circuit in circuits]
	circuit_sizes.sort(reverse=True)
	
	return prod(circuit_sizes[:3])

def solve_all_closest_junction_boxes(junction_boxes: list[vector3]) -> int:

	box2connections: dict[vector3, frozenset[vector3]] = {junction_box: frozenset() for junction_box in junction_boxes}
	box2circuit: dict[vector3, frozenset[vector3]] = {junction_box: frozenset({junction_box}) for junction_box in junction_boxes}

	pairs = iter(sorted([(v, w) for v, w in product(junction_boxes, repeat=2) if v != w], key=lambda vw: distance(*vw)))

	while len(set(box2circuit.values())) > 1:
		v, w = next(pairs)
		
		if w not in box2connections[v]:
			vw_circuit: frozenset[vector3] = box2circuit[v].union(box2circuit[w])
			for u in vw_circuit:
				box2circuit[u] = vw_circuit
			box2connections[v] = box2connections[v].union([w])
			box2connections[w] = box2connections[w].union([v])
	
	return v[0] * w[0]

with open('output', 'w') as output:
    output.write( str( solve_N_closest_junction_boxes(junction_boxes, 1000) ) + '\n')
    output.write( str( solve_all_closest_junction_boxes(junction_boxes) ) + '\n')