import numpy as np
from PIL import Image

# https://stackoverflow.com/questions/50445847/how-to-zigzag-order-and-concatenate-the-value-every-line-using-python
def zigzag_rearrange(arr):
	result = []
	for i in range(1 - arr.shape[0], arr.shape[0]):
		diagonal = np.diagonal(arr[::-1, ...], offset=i)

		step = 2 * (i % 2) - 1
		result.append(diagonal[::step])

	return np.concatenate(result)

def rotate90_clockwise(arr):
	return np.rot90(arr)

def filter_up_sub(arr):
	row, col = arr.shape

	for y in range(0, col):
		last_value = arr[y, 0]
		for x in range(1, row):
			arr[y, x], last_value = arr[y, x] - last_value, arr[y, x]

	last_value = arr[0, 0]
	for y in range(1, col):
		arr[y, 0], last_value = arr[y, 0] - last_value, arr[y, 0]

	return arr

def unfilter_up_sub(arr):
	row, col = arr.shape

	last_value = arr[0, 0]
	for y in range(1, col):
		arr[y, 0] += last_value
		last_value = arr[y, 0]

	for y in range(0, col):
		last_value = arr[y, 0]
		for x in range(1, row):
			arr[y, x] += last_value
			last_value = arr[y, 0]

	return arr

img = np.array(Image.open("../edu/model_012_intimate.png").convert('L'))

original_px1 = np.array(img[0:8, 0:8], dtype=np.int64)
px1 = np.copy(original_px1)

# print(zigzag_rearrange(indices_zig).reshape(indices_zig.shape))
# print(px1)
# print(zigzag_rearrange(px1).reshape(px1.shape))
# print(rotate90_clockwise(zigzag_rearrange(px1).reshape(px1.shape)))

sub = filter_up_sub(px1)
print(sub)
print(unfilter_up_sub(sub))
