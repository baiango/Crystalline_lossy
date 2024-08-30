# CLY - Crystalline lossy
An Unlicense custom image format. You can check [license information in edu/README.md](edu/README.md). Please don't affiliate your project with me. You can claim that you made it or found it in a buried hard drive instead.

Other assets, such as image, are under CC0.

There will be some educational Python scripts in the `edu` folder used during creation of CLY. I took time to name them descriptively.

Blueprint v1 is inherently complex, so I started from scratch to lower the scope, and make it easier for me to complete. They are named `blueprint_v*.md` in the root folder.

I developed more effective methods and lessen compute cost for every time I started from the beginning.

- [blueprint_v1.md](blueprint_v1.md)

## Blueprint v2
This blueprint attempts to improve lossless compression ratio with rearrangement, lossy mode is deferred.

Color Space: RGB888
Macroblock size: 256x256
Rearrangement: Zig-Zag | Clockwise 90 degrees rotation
Filters: Sub
Machine Learning Prediction: 3-channels Bitwise Trigram
Entropy coding: Elias gamma coding + Bzip3
