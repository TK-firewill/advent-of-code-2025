import re

class Node:
	def __init__(self, name: str):
		self.name = name
		self.outbound: set[Node] = set()
		self.parents: set[Node] = set()
		self.accessible: set[Node] = set()
	
	def add_outbound(self, node) -> None:
		self.outbound.add(node)
	
	def add_parent(self, node) -> None:
		self.parents.add(node)

	def add_accessible(self, node) -> None:
		self.accessible.add(node)
	
	def __repr__(self):
		return f'{self.name}: ' + ', '.join(map(lambda x: x.name, self.outbound))

with open('input') as input:
	node_schematics: list[str] = input.read().splitlines()
	node_schematics: list[list[str]] = [re.findall(r'(\w+)', schematic) for schematic in node_schematics]
	
	names: list[str] = [schema[0] for schema in node_schematics]
	directory: dict[str, Node] = {name: Node(name) for name in names} | {'out': Node('out')}

	for name, *outbound in node_schematics:
		for node in outbound:
			directory[name].add_outbound(directory[node])
			directory[node].add_parent(directory[name])

	you: Node = directory['you']
	out: Node = directory['out']

	dac: Node = directory['dac']
	fft: Node = directory['fft']
	svr: Node = directory['svr']

def build_map(interest: Node) -> None:
	seen: set[Node] = {interest}

	def expand_seen(seen: set[Node]) -> set[Node]:
		return {parent for node in seen for parent in node.parents}

	newly_seen = seen.copy()
	while newly_seen != (newly_seen := expand_seen(seen)):
		seen |= newly_seen

	for node in seen:
		node.add_accessible(interest)

def paths_from(start: Node, end: Node) -> int:
	M: dict[Node, int] = {end: 1}

	def recursion(start: Node, end: Node) -> int:
		if start not in M:
			M[start] = sum(paths_from(node, end) for node in start.outbound if end in node.accessible)
		return M[start]

	return recursion(start, end)

def accessible(start: Node, end: Node) -> int:
	state: set[Node] = set([start])
	while len(state) > 0 and end not in state:
		state = [outbound for node in state for outbound in node.outbound]
	return end in state

def solve_first(you: Node, out: Node) -> int:
	build_map(out)
	return paths_from(you, out)

def solve_second(svr: Node, dac: Node, fft: Node, out: Node) -> int:
	build_map(dac)
	build_map(fft)
	build_map(out)

	fst: Node = dac if fft in dac.accessible else fft
	snd: Node = fft if fft in dac.accessible else dac
	
	return paths_from(svr, fst) * paths_from(fst, snd) * paths_from(snd, out)

with open('output', 'w') as output:
    output.write( str( solve_first(you, out) ) + '\n')
    output.write( str( solve_second(svr, dac, fft, out) ) + '\n')