# CLY - Crystalline lossy
An Unlicense custom image crate. Please don't affiliate your project with me. You can claim that you made it or found it in a buried hard drive instead.

Other assets, such as image, are under CC0.

There will be some educational Python scripts in the `/edu` folder used during creation of CLY. I took time to name them descriptively.

## Blueprint
**Quadtree split macroblocks:**
-	**Lossless**
	-	RGB565 -> Similarity transform -> Sparse (XOR/Delta encoding & flip) bitplane encoding -> RLE -> Elias gamma coding
	-	RGB565 -> Similarity transform -> FWHT -> RLE -> Elias gamma coding
	-	RGB565 -> Similarity transform -> Haar wavelet -> RLE -> Elias gamma coding
-	**Lossy**
	-	YCoCg655 -> 4:2:0 -> DCT-II -> Attention map quantization -> Similarity transform -> Zigzag -> block-to-block delta coding -> Elias gamma coding
	-	YCoCg655 -> 4:2:0 -> DST-II -> Attention map quantization -> Similarity transform -> Zig-Zag -> delta coding -> Elias gamma coding
	-	YCoCg655 -> 4:2:0 -> FWHT -> Attention map quantization -> Similarity transform -> Zig-Zag -> delta coding -> Elias gamma coding
	-	YCoCg655 -> 4:2:0 -> Haar wavelet -> Attention map quantization -> Similarity transform -> Zigzag -> delta coding -> Elias gamma coding

**Archiver**
-	BZip3
