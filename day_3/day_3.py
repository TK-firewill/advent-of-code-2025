with open('input') as input:
    banks: list[str] = input.read().splitlines()
    banks: list[list[int]] = [list(map(int, bank)) for bank in banks]

def solve_bank(bank: list[int], trailing: int) -> int:
	if len(bank) < trailing + 1:
		raise ValueError
	elif trailing <= 0:
		return max(bank)
	else:
		left_bank: list[int] = bank[:-trailing]
		index: int = left_bank.index(max(left_bank))
		return max(left_bank) * (10**trailing) + solve_bank(bank[index+1:], trailing-1)

with open('output', 'w') as output:
    output.write( str(sum(solve_bank(bank,  1) for bank in banks)) + '\n')
    output.write( str(sum(solve_bank(bank, 11) for bank in banks)) + '\n')