# CLY - Crystalline lossy
An Unlicense custom image crate. Please don't affiliate your project with me. You can claim that you made it or found it in a buried hard drive instead.

Other assets, such as image, are under CC0.

There will be some educational Python scripts in the `/edu` folder used during creation of CLY. I took time to name them descriptively.

## Blueprint
**Quadtree split macroblocks:**
-	**Lossless**
	-	RGB565 -> Self-similarity transform -> Sparse (XOR/Delta encoding & swap) bitplane encoding -> RLE -> Elias gamma coding
	-	RGB565 -> Self-similarity transform -> FWHT -> RLE -> Elias gamma coding
	-	RGB565 -> Self-similarity transform -> Haar wavelet -> RLE -> Elias gamma coding
-	**Lossy**
	-	YCoCg655 -> 4:2:0 -> DCT-II -> Attention map quantization -> Self-similarity transform -> Zig-Zag -> block-to-block delta coding -> Elias gamma coding
	-	YCoCg655 -> 4:2:0 -> DST-II -> Attention map quantization -> Self-similarity transform -> Zig-Zag -> block-to-block delta coding -> Elias gamma coding
	-	YCoCg655 -> 4:2:0 -> FWHT -> Attention map quantization -> Self-similarity transform -> Zig-Zag -> block-to-block delta coding -> Elias gamma coding
	-	YCoCg655 -> 4:2:0 -> Haar wavelet -> Attention map quantization -> Self-similarity transform -> Zig-Zag -> block-to-block delta coding -> Elias gamma coding
	-	RGB565 -> Self-similarity search -> Macroblock copy

**Notes**
-	Self-similarity transform will use rotations and flips to match the previous block.
-	The strength of quantization will be based on Sharpness Threshold Measure (%)
-	Sharpness Threshold Measure (%) is an in-house grayscale image metric that ignores subtle noise, like film grains. While checking for distracting noise like denoiser removed-noise. It returns in percentage scale.

**Archiver**
-	BZip3

**Sharpness Threshold Measure (%) implementation**

The Laplacian function is defined as below, where `$I(x, y)` is the index of the image:
```math
\nabla^2 I(x, y) =
\begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
I
```
The Sharpness Threshold Measure function is defined as below, where `Img` is two grayscale images to compare and `T` is the threshold:  
It's recommended to set the threshold to 8 to ignore film grains.
```math
\left( \frac{\sum \mathbb{I}_{\left| \nabla^2 Img_1 - \nabla^2 Img_2 \right| \geq T}}{\text{total\_pixels}} \right) \times 100\%
```
