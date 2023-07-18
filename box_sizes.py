# This script was written by Hannah R Bridges with help from ChatGPT for Python3 on 17.07.2023

#This script estimates an appropriate box size for extraction based on the image pixel size and particle diameter, and suggests FFT efficient boxes within this range.

import math

# user enters values for pixel size and particle diameter
pixel_size = float(input("Enter pixel size: "))
lomgest particle_diameter = int(input("Enter longest particle diameter in Angstrom: "))

#calculate the required box sizes with 1.5 or 2x particle diameter
good_box_size_low = int(round((particle_diameter * 1.5) / pixel_size))
good_box_size_high = int(round((particle_diameter * 2) / pixel_size))

# Round the box sizes to the nearest even integer
if good_box_size_low % 2 != 0:
    good_box_size_low += 1

if good_box_size_high % 2 != 0:
    good_box_size_high -= 1

#print the range if box sizes
print("Your particles need a box size between", good_box_size_low, "and", good_box_size_high)

#look for box sizes between these two values that are FFT efficient#
fft_box_sizes = [
    size for size in [24, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 84, 96, 100, 104, 112, 120, 128, 132, 140, 168, 180, 192, 196, 208,
                      216, 220, 224, 240, 256, 260, 288, 300, 320, 352, 360, 384, 416, 440, 448, 480, 512, 540, 560, 576, 588, 600,
                      630, 640, 648, 672, 686, 700, 720, 750, 756, 768, 784, 800, 810, 840, 864, 882, 896, 900, 960, 972, 980, 1000,
                      1008, 1024, 1050, 1080, 1120, 1134, 1152, 1176, 1200, 1250, 1260, 1280, 1296, 1344, 1350, 1372, 1400, 1440, 1458,
                      1470, 1500, 1512, 1536, 1568, 1600, 1620, 1680, 1728, 1750, 1764, 1792, 1800, 1890, 1920, 1944, 1960, 2000, 2016,
                      2048, 2058, 2100, 2160, 2240, 2250, 2268, 2304, 2352, 2400, 2430, 2450, 2500, 2520, 2560, 2592, 2646, 2688, 2700,
                      2744, 2800, 2880, 2916, 2940, 3000, 3024, 3072, 3136, 3150, 3200, 3240, 3360, 3402, 3430, 3456, 3500, 3528, 3584,
                      3600, 3750, 3780, 3840, 3888, 3920, 4000, 4032, 4050, 4096]
    if good_box_size_low <= size <= good_box_size_high and size % 2 == 0
]
#print the best box sizes for these particles
print("Suggested FFT efficient box sizes:", fft_box_sizes)
