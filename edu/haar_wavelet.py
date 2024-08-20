import numpy as np
import pywt
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path


def map_range(x, x_min, x_max, y_min, y_max):
	return ((x - x_min) / (x_max - x_min)) * (y_max - y_min) + y_min

# Load an image
img = Image.open('lemon.jpg')
img_array = np.array(img)

wavelet_shape = (img_array.shape[0] // 2, img_array.shape[1] // 2, img_array.shape[2])
approximation_array = np.zeros(wavelet_shape)
horizontal_detail_array = np.zeros(wavelet_shape)
vertical_detail_array = np.zeros(wavelet_shape)
diagonal_detail_array = np.zeros(wavelet_shape)

for i in range(img_array.shape[2]):
	process = img_array[:, :, i]

	# Apply 2D Haar wavelet transform
	coefficients = pywt.dwt2(process, 'haar')
	approximation = coefficients[0]
	horizontal_detail, vertical_detail, diagonal_detail = coefficients[1]

	approximation_array[..., i] = map_range(approximation, np.min(approximation), np.max(approximation), 0.0, 255.0)
	horizontal_detail_array[..., i] = map_range(horizontal_detail, np.min(horizontal_detail), np.max(horizontal_detail), 0.0, 255.0)
	vertical_detail_array[..., i] = map_range(vertical_detail, np.min(vertical_detail), np.max(vertical_detail), 0.0, 255.0)
	diagonal_detail_array[..., i] = map_range(diagonal_detail, np.min(diagonal_detail), np.max(diagonal_detail), 0.0, 255.0)

Path("haar_coefficients").mkdir(parents=True, exist_ok=True)
approximation_img = Image.fromarray(approximation_array.astype(np.uint8))
approximation_img.save('haar_coefficients/approximation_img.png')
horizontal_detail_img = Image.fromarray(horizontal_detail_array.astype(np.uint8))
horizontal_detail_img.save('haar_coefficients/horizontal_detail_img.png')
vertical_detail_img = Image.fromarray(vertical_detail_array.astype(np.uint8))
vertical_detail_img.save('haar_coefficients/vertical_detail_img.png')
diagonal_detail_img = Image.fromarray(diagonal_detail_array.astype(np.uint8))
diagonal_detail_img.save('haar_coefficients/diagonal_detail_img.png')
