import re

with open('input') as input:
    product_ids: list[str] = input.read().split(',')
    product_ids: list[tuple[str, str]] = [re.match(r'(\d+)\-(\d+)', instruction).groups() for instruction in product_ids]
    product_ids: list[tuple[int, int]] = [(int(a), int(b)) for a, b in product_ids]

def get_2_irregulars_between(a: int, b: int) -> int:
	return sum(i for i in range(a, b+1) if re.match(r'^(\d+)\1$', str(i)))

def get_n_irregulars_between(a: int, b: int) -> int:
	return sum(i for i in range(a, b+1) if re.match(r'^(\d+)\1+$', str(i)))

with open('output', 'w') as output:
    output.write( str(sum(get_2_irregulars_between(a, b) for a, b in product_ids)) + '\n')
    output.write( str(sum(get_n_irregulars_between(a, b) for a, b in product_ids)) + '\n')