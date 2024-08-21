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

**Archiver**
-	BZip3
