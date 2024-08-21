from PIL import Image
import numpy as np
from scipy.signal import convolve2d
from skimage.metrics import structural_similarity

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

def calculate_sharpness_change(original, transformed, threshold=8):
	original_array = np.array(original.convert('L'))
	transformed_array = np.array(transformed.convert('L'))

	laplacian1 = calculate_laplacian(original_array)
	laplacian2 = calculate_laplacian(transformed_array)

	sharpness_diff = np.abs(laplacian1 - laplacian2)
	sharpness_change_detected = sharpness_diff >= threshold
	sharpness_diff_pct = np.sum(sharpness_diff) / np.prod(sharpness_diff.shape) * 100.0
	sharpness_threshold_pct = np.sum(sharpness_change_detected) / np.prod(sharpness_diff.shape) * 100.0

	return sharpness_diff_pct, sharpness_threshold_pct

def calculate_ssim(original, transformed):
	return structural_similarity(original, transformed, multichannel=True, channel_axis=2)

def calculate_pixel_difference(original, transformed):
	return np.sum(np.abs(original - transformed)) / np.prod(original.shape)

def compare_metrics(image1_path, image2_path):
	img1 = Image.open(image1_path)
	img2 = Image.open(image2_path)

	psnr = calculate_psnr(np.array(img1), np.array(img2))
	ssim = calculate_ssim(np.array(img1), np.array(img2))
	contrast_ratio_db = calculate_contrast_ratio(img1, img2)
	brightness_diff = calculate_brightness_difference(np.array(img1), np.array(img2))
	saturation_diff = calculate_saturation_difference(img1, img2)
	sharpness_diff_db, sharpness_threshold_db = calculate_sharpness_change(img1, img2)
	pixel_diff = calculate_pixel_difference(np.array(img1), np.array(img2))

	return psnr, ssim, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db, pixel_diff

def print_metrics(image1_path, image2_path):
	psnr, ssim, contrast_ratio_db, brightness_diff, saturation_diff, sharpness_threshold_db, pixel_diff = compare_metrics(image1_path, image2_path)
	print(f'{image1_path} & {image2_path} | {psnr:.2f} | {ssim:.2f} | {contrast_ratio_db:.2f} | {brightness_diff:.2f} | {saturation_diff:.2f} | {sharpness_threshold_db:.2f} | {pixel_diff:.2f}')

if __name__ == '__main__':
	# Usage
	original_image = 'eye.png'
	jpg_100_image = 'eye_100.jpg'
	jpg_99_image = 'eye_99.jpg'
	jpg_95_image = 'eye_95.jpg'
	jpg_5_image = 'eye_5.jpg'
	noisy_image = 'eye_noise.png'
	color_noisy_image = 'eye_color_noise.png'

	print("Image Pair | PSNR (dB) | SSIM (f) | Contrast Ratio Difference (dB) | Brightness Difference (n) | Saturation Difference (n) | Sharpness Threshold Measure (%) | Pixel Difference (n)")
	print_metrics(jpg_95_image, jpg_95_image)
	print_metrics(original_image, noisy_image)
	print_metrics(original_image, color_noisy_image)
	print_metrics(original_image, jpg_100_image)
	print_metrics(original_image, jpg_99_image)
	print_metrics(original_image, jpg_95_image)
	print_metrics(jpg_99_image, jpg_100_image)
	print_metrics(jpg_99_image, jpg_95_image)
	print_metrics(original_image, jpg_5_image)
	print_metrics(jpg_100_image, jpg_5_image)
