import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
from pathlib import Path
from img_metrics import calculate_mse, calculate_psnr, calculate_contrast_ratio


def rgb_to_ycocg(r, g, b):
	y = r // 4 + g // 2 + b // 4
	co = r // 2 + -b // 2
	cg = -r // 4 + g // 2 + -b // 4
	return (y, co, cg)

def ycocg_to_rgb(y, co, cg):
	r = y + co + -cg
	g = y + cg
	b = y - co - cg
	return (r, g, b)

def example_rgb_to_ycocg_to_rgb():
	print('----- example_rgb_to_ycocg_to_rgb() -----')
	# Generate random RGB colors
	np.random.seed(13) # For reproducibility
	rgb_colors = np.random.randint(0, 255, size=(1000, 3))  # 1000 random colors

	# Convert RGB to YCoCg and back to RGB
	ycocg_colors = np.array([rgb_to_ycocg(*color) for color in rgb_colors])
	restored_colors = np.array([ycocg_to_rgb(*color) for color in ycocg_colors])

	# Calculate MSE and SNR
	mse_val = calculate_mse(rgb_colors, restored_colors)
	snr_val = calculate_psnr(rgb_colors, restored_colors)
	print(f"YCoCg restored MSE: {mse_val:.4f}")
	print(f"YCoCg restored PSNR: {snr_val:.2f} dB")

	print(f'YCoCg difference R: {(np.sum(rgb_colors[:, 0] - restored_colors[:, 0])) / np.sum(rgb_colors[:, 0]) * 100.0:.2f}%')
	print(f'YCoCg difference G: {(np.sum(rgb_colors[:, 1] - restored_colors[:, 1])) / np.sum(rgb_colors[:, 1]) * 100.0:.2f}%')
	print(f'YCoCg difference B: {(np.sum(rgb_colors[:, 2] - restored_colors[:, 2])) / np.sum(rgb_colors[:, 2]) * 100.0:.2f}%')

def example_ycocg_and_rgb_bitplane(image_path='lemon.jpg'):
	print('----- example_ycocg_and_rgb_bitplane() -----')
	# Open the image file
	img = Image.open(image_path)
	img_array = np.array(img)
	y_array = np.zeros(img_array.shape)
	co_array = np.zeros(img_array.shape)
	cg_array = np.zeros(img_array.shape)
	co_re_array = np.zeros(img_array.shape)
	cg_re_array = np.zeros(img_array.shape)

	# Iterate through the rows and columns of the image
	for i in range(img_array.shape[0]):
		for j in range(img_array.shape[1]):
			pixel = img_array[i, j]
			y, co, cg = rgb_to_ycocg(pixel[0], pixel[1], pixel[2])
			y_array[i, j] = y
			co_array[i, j] = co
			cg_array[i, j] = cg

			co_re_array[i, j] = ycocg_to_rgb(0, co, 0)
			cg_re_array[i, j] = ycocg_to_rgb(0, 0, cg)

			linear_index = j * img_array.shape[0] + i
			if linear_index % 100_000 == 0:
				print(f"Pixel ({i + 1}, {j + 1}): {pixel}")

	Path("ycocg_converted").mkdir(parents=True, exist_ok=True)
	img_edit = Image.fromarray(img_array & 0b1111_1000)
	img_edit.save(f'ycocg_converted/img_edit.png')
	y_img = Image.fromarray(y_array.astype(np.uint8))
	y_img.save('ycocg_converted/y_img.png')
	co_img = Image.fromarray(co_array.astype(np.uint8))
	co_img.save('ycocg_converted/co_img.png')
	cg_img = Image.fromarray(cg_array.astype(np.uint8))
	cg_img.save('ycocg_converted/cg_img.png')
	co_re_img = Image.fromarray(co_re_array.astype(np.uint8))
	co_re_img.save('ycocg_converted/co_re_img.png')
	cg_re_img = Image.fromarray(cg_re_array.astype(np.uint8))
	cg_re_img.save('ycocg_converted/cg_re_img.png')

	Path("rgb_bitplanes").mkdir(parents=True, exist_ok=True)
	for i in range(8):
		img_bitplane_array = (img_array & (1 << i) != 0).astype(np.uint8) * 255
		img_bitplane = Image.fromarray(img_bitplane_array)
		img_bitplane.save(f'rgb_bitplanes/img_rgb_bitplane_{i}.png')

def example_pca_components(image_path='lemon.jpg'):
	print('----- example_pca_components() -----')
	# Open the image file
	img = Image.open(image_path)
	img_array = np.array(img)
	x, y, ch = img_array.shape
	img_array_r = img_array[..., 0]
	img_array_g = img_array[..., 1]
	img_array_b = img_array[..., 2]

	pca_component_test = x // 64
	pca = PCA(n_components=pca_component_test)
	img_array_r_pc = pca.fit_transform(img_array_r)
	img_array_r_re = pca.inverse_transform(img_array_r_pc)
	img_array_g_pc = pca.fit_transform(img_array_g)
	img_array_g_re = pca.inverse_transform(img_array_g_pc)
	img_array_b_pc = pca.fit_transform(img_array_b)
	img_array_b_re = pca.inverse_transform(img_array_b_pc)

	Path("pca_component_test").mkdir(parents=True, exist_ok=True)
	img_r_edit_pca = Image.fromarray(img_array_r_re.astype(np.uint8), 'L')
	img_r_edit_pca.save(f'pca_component_test/img_r_edit_pca_{pca_component_test}.png')
	img_g_edit_pca = Image.fromarray(img_array_g_re.astype(np.uint8), 'L')
	img_g_edit_pca.save(f'pca_component_test/img_g_edit_pca_{pca_component_test}.png')
	img_b_edit_pca = Image.fromarray(img_array_b_re.astype(np.uint8), 'L')
	img_b_edit_pca.save(f'pca_component_test/img_b_edit_pca_{pca_component_test}.png')

	Path("pca_component_iter").mkdir(parents=True, exist_ok=True)
	print(f"PCA (n_components) | PSNR | Contrast Ratio Difference")
	for i in range(0, x + 1, 10):
		pca = PCA(n_components=i)
		img_array_b_pc = pca.fit_transform(img_array_r)
		img_array_b_re = pca.inverse_transform(img_array_b_pc)
		img_b_edit = Image.fromarray(img_array_b_re.astype(np.uint8), 'L')
		img_b_edit.save(f'pca_component_iter/img_b_{i}.png')

		psnr_val = calculate_psnr(img_array_r, img_array_b_re)
		contrast_ratio_diff_val = calculate_contrast_ratio(img_array_r, img_array_b_re)
		print(f"{i} | {psnr_val:.2f} dB | {contrast_ratio_diff_val:.2f} dB")

if __name__ == '__main__':
	example_rgb_to_ycocg_to_rgb()
	example_ycocg_and_rgb_bitplane()
	example_pca_components()
