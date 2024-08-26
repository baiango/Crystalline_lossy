import numpy as np
import hashlib
from PIL import Image

def rand_sha_256(number):
	return int.from_bytes(hashlib.sha256(str(number).encode()).digest())

width, height = 1024, 1024
image_array = np.zeros((width, height, 3), dtype=np.uint8)

for x in range(width):
	for y in range(height):
		linear_index = y * width + x

		pixel_rgb = (
			rand_sha_256(linear_index) & 0xff,
			rand_sha_256(linear_index * 2.213) & 0xff,
			rand_sha_256(linear_index * 3.541) & 0xff,
		)
		image_array[x, y] = pixel_rgb

		if linear_index % 100_000 == 0:
			print(f"Pixel ({x + 1}, {y + 1}): {image_array[x, y]}")

image = Image.fromarray(image_array)
image.save("sha_256_color_noise.bmp")
