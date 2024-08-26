# https://en.wikipedia.org/wiki/Fast_Walsh%E2%80%93Hadamard_transform#Python_example_code
def fwht(arr):
	current_size = 1
	while current_size < len(arr):
		for start_i in range(0, len(arr), current_size * 2):
			for element_i in range(start_i, start_i + current_size):
				x = arr[element_i]
				y = arr[element_i + current_size]
				arr[element_i] = x + y
				arr[element_i + current_size] = x - y
		current_size *= 2
	return arr

def rfwht(arr):
	return [x // len(arr) for x in fwht(arr)]

if __name__ == '__main__':
	x = [255] * 16**2
	# x = [1, 0, 1, 0, 0, 1, 1, 0]
	print(x)
	x = fwht(x)
	print(x)
	x = rfwht(x)
	print(x)
