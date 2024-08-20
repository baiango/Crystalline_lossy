from PIL import Image
import numpy as np

def calculate_mse(original, transformed):
	return np.mean((original - transformed) ** 2)

def calculate_psnr(original, transformed):
	mse_val = calculate_mse(original, transformed)
	if mse_val == 0.0:
		return float('inf')
	signal_power = np.mean(original ** 2)
	return 10.0 * np.log10(signal_power / mse_val)

def calculate_contrast_ratio(original, transformed):
	# Calculate cumulative distributions
	cd1 = np.cumsum(original) / np.sum(original)
	cd2 = np.cumsum(transformed) / np.sum(transformed)

	# Calculate contrast ratio using the area between the cumulative distributions
	contrast_ratio_diff_val = np.abs(np.sum(np.abs(cd1 - cd2)))
	contrast_ratio_diff_db = 10.0 * np.log10(contrast_ratio_diff_val + 1.0)

	return contrast_ratio_diff_db

def compare_psnr(image1_path, image2_path):
	# Open images using Pillow
	img1 = Image.open(image1_path)
	img2 = Image.open(image2_path)

	# Calculate PSNR
	return calculate_psnr(np.array(img1), np.array(img2))

def compare_contrast_ratio(image1_path, image2_path):
	# Open images using Pillow
	img1 = Image.open(image1_path).convert('L')
	img2 = Image.open(image2_path).convert('L')

	# Calculate contrast ratio using the area between the cumulative distributions
	return calculate_contrast_ratio(img1, img2)

if __name__ == '__main__':
	# Usage
	image1_path = 'eye.png'
	image2_path = 'eye_100.jpg'
	image3_path = 'eye_99.jpg'
	image4_path = 'eye_95.jpg'
	image5_path = 'eye_5.jpg'

	print("Image Pair | PSNR (dB) | Contrast Ratio Difference (dB)")
	psnr_val = compare_psnr(image4_path, image4_path)
	contrast_ratio_diff_val = compare_contrast_ratio(image4_path, image4_path)
	print(f'{image4_path} vs {image4_path} | {psnr_val:.2f} | {contrast_ratio_diff_val:.2f}')

	psnr_val = compare_psnr(image1_path, image2_path)
	contrast_ratio_diff_val = compare_contrast_ratio(image1_path, image2_path)
	print(f'{image1_path} vs {image2_path} | {psnr_val:.2f} | {contrast_ratio_diff_val:.2f}')

	psnr_val = compare_psnr(image1_path, image3_path)
	contrast_ratio_diff_val = compare_contrast_ratio(image1_path, image3_path)
	print(f'{image1_path} vs {image3_path} | {psnr_val:.2f} | {contrast_ratio_diff_val:.2f}')

	psnr_val = compare_psnr(image1_path, image4_path)
	contrast_ratio_diff_val = compare_contrast_ratio(image1_path, image4_path)
	print(f'{image1_path} vs {image4_path} | {psnr_val:.2f} | {contrast_ratio_diff_val:.2f}')

	psnr_val = compare_psnr(image3_path, image4_path)
	contrast_ratio_diff_val = compare_contrast_ratio(image3_path, image4_path)
	print(f'{image3_path} vs {image4_path} | {psnr_val:.2f} | {contrast_ratio_diff_val:.2f}')

	psnr_val = compare_psnr(image1_path, image5_path)
	contrast_ratio_diff_val = compare_contrast_ratio(image1_path, image5_path)
	print(f'{image1_path} vs {image5_path} | {psnr_val:.2f} | {contrast_ratio_diff_val:.2f}')
