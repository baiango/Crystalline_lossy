from PIL import Image
import numpy as np
from scipy.signal import convolve2d

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
	contrast_ratio_diff_val = np.sum(np.abs(cd1 - cd2))
	contrast_ratio_diff_db = 10.0 * np.log10(contrast_ratio_diff_val + 1.0)

	return contrast_ratio_diff_db

def calculate_brightness_difference(original, transformed):
	brightness_diff = np.abs(np.mean(original) - np.mean(transformed))
	return brightness_diff

def calculate_saturation_difference(original, transformed):
	original = np.array(original.convert('HSV'))
	transformed = np.array(transformed.convert('HSV'))

	# Calculate the mean value of the S channel (saturation)
	saturation_diff = np.abs(np.mean(original[:, :, 1]) - np.mean(transformed[:, :, 1]))
	return saturation_diff

def calculate_laplacian(image):
	laplacian = np.array([[0, 1, 0],
						  [1, -4, 1],
						  [0, 1, 0]])
	laplacian_image = np.zeros_like(image)
	laplacian_image = convolve2d(image, laplacian, mode='same', boundary='symm')
	return laplacian_image

def calculate_sharpness_change(img1, img2, threshold=8):
	img1 = np.array(img1.convert('L'))
	img2 = np.array(img2.convert('L'))

	laplacian1 = calculate_laplacian(img1)
	laplacian2 = calculate_laplacian(img2)

	sharpness_diff = np.abs(laplacian1 - laplacian2)
	sharpness_change_detected = sharpness_diff >= threshold
	sharpness_diff_db = 10.0 * np.log10(np.sum(sharpness_diff)) if sharpness_diff.any() else 0.0
	sharpness_threshold_db = 10.0 * np.log10(np.sum(sharpness_change_detected)) if sharpness_change_detected.any() else 0.0

	return sharpness_diff_db, sharpness_threshold_db

def compare_metrics(image1_path, image2_path):
	img1 = Image.open(image1_path)
	img2 = Image.open(image2_path)

	psnr = calculate_psnr(np.array(img1), np.array(img2))
	contrast_ratio = calculate_contrast_ratio(img1, img2)
	brightness_diff = calculate_brightness_difference(np.array(img1), np.array(img2))
	saturation_diff = calculate_saturation_difference(img1, img2)
	sharpness_diff_db, sharpness_threshold_db = calculate_sharpness_change(img1, img2)

	return psnr, contrast_ratio, brightness_diff, saturation_diff, sharpness_threshold_db


if __name__ == '__main__':
	# Usage
	image1_path = 'eye.png'
	image2_path = 'eye_100.jpg'
	image3_path = 'eye_99.jpg'
	image4_path = 'eye_95.jpg'
	image5_path = 'eye_5.jpg'
	image6_path = 'eye_noise.png'

	print("Image Pair | PSNR (dB) | Contrast Ratio Difference (dB) | Brightness Difference | Saturation Difference | Sharpness Threshold (dB)")
	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image4_path, image4_path)
	print(f'{image4_path} vs {image4_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')

	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image1_path, image6_path)
	print(f'{image1_path} vs {image6_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')

	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image1_path, image2_path)
	print(f'{image1_path} vs {image2_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')

	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image1_path, image3_path)
	print(f'{image1_path} vs {image3_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')

	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image1_path, image4_path)
	print(f'{image1_path} vs {image4_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')

	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image3_path, image4_path)
	print(f'{image3_path} vs {image4_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')

	psnr, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db = compare_metrics(image1_path, image5_path)
	print(f'{image1_path} vs {image5_path} | {psnr:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f}')
