import re

with open('input') as input:
    fresh_ids, available_ids = input.read().split('\n\n')
    fresh_ids, available_ids = fresh_ids.splitlines(), available_ids.splitlines()
    fresh_ids: set[tuple[int, int]] = {tuple(map(int, re.match(r'(\d+)-(\d+)', id_range).groups())) for id_range in fresh_ids}
    available_ids: set[int] = set(map(int, available_ids))

def merge_segments(fresh_ids: set[tuple[int, int]]) -> set[tuple[int, int]]:
	fresh_ids = set(fresh_ids.copy())
	new_fresh_ids = set()
	for s in fresh_ids:
		mins, maxs = tuple(zip(*filter(lambda t: t[0] <= s[0] <= t[1] or s[0] <= t[0] <= s[1], fresh_ids)))
		new_fresh_ids.add((min(mins), max(maxs)))
	return new_fresh_ids
    
while fresh_ids != (fresh_ids := merge_segments(fresh_ids)):
	pass

with open('output', 'w') as output:
    output.write( str( len([id for id in available_ids if any(start <= id <= end for start, end in fresh_ids)]) ) + '\n')
    output.write( str( sum(end - start + 1 for start, end in fresh_ids) ) + '\n')