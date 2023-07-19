# This script was written by Hannah R Bridges with help from ChatGPT for Python3 17.07.2023

# It finds the best box sizes and particle downsampling to use when you want to merge two single particle cryo-EM datasets of differing pixel sizes. This is useful if your software can only combine data with exactly the same pixel and box size, or one or both datasets were not processed at the calibrated pixel size.

# Notes and hints on script usage:

# Before running the script, ensure that you have properly calibrated the pixel sizes of your data collections to one another, for example in ChimeraX by adjusting one dataset voxel size until the fit-in-map returns the highest correlation
# Only use the nominal pixel sizes provided by your facility if you have ensured that the 2 maps match perfectly without any rescaling in ChimeraX
# If the calibrated pixel size is different from the nominal magnification used at the start of processing, motioncorr and CTF estimation need to be re-run at the calibrated pixel size, and extraction performed from there.
# If you are extracting from motion corrected micrographs, the calibrated pixel size here refers to the binned pixel size (if binning was used)
# If you are polishing in RELION, the calibrated pixel size refers to the raw images, which may be in super-resolution pixels
# If particles will be extracted in CryoSPARC, the calibrated pixel size refers to that of the motion correction job (whether binning was used or not) and rescaled pixel sizes need to be identical or thr same to 4 decimal places beteeen pix1 and pix2 as it does not tolerate larger differences in merged dataset pixel sizes.

# For the preferred box size, this is usually 1.5 - 2 times the longest diameter of your protein in Angstroms, then converted to pixels using the Apix 
# If a narrow range of box tolerance is given, the accuracy of the pixels size matching may be poorer
# If a wide range of tolerance is given, the box sizes with the most accurate pixel size matching may be too small (cut off high resolution information) or too large (include too much noise)

# Once the results have been returned, you may need to use the RELION additional argument --force_header in relion extract or polish to specify the pixel size in one dataset to exactly match the other. 
# This should avoid issues where software cannot tolerate even small discrepancies.
# Minor alterations in pixel size can also be acheived by modifying the STAR file in a text editor
# If the calibrated pixel size is different to the nominal pixel size used for initial processing, be aware that further CTF and defocus refinement is likely necessary to achieve the highest resolution.

# The script will prompt you to enter the necessary values in the command line - enjoy!!


# Function to validate and get user input
def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid floating-point number.")

# User input to define the ideal box size and range, as well as the calibrated pixel size of the raw micrographs
# or binned micrographs at MotionCorr, whichever will be extracted from.
pix1 = get_float_input("Enter the first calibrated pixel size: ")
pix2 = get_float_input("Enter the second calibrated pixel size: ")
target_pixel_size = get_float_input("Enter the target pixel size after rescaling: ")
box_aim = get_float_input("Enter your preferred extraction box size in pixels for the smallest pixel size: ")
tolerance = get_float_input("Enter the box size tolerance in pixels: ")

# Values are ordered so that pix1 is the largest pixel size
if pix1 < pix2:
    pix1, pix2 = pix2, pix1

print(" ")
print("The largest pixel size (pix1) is:", pix1)
print("The smallest pixel size (pix2) is:", pix2)
print(" ")

# Check if the target pixel size is smaller than pix1
if target_pixel_size < pix1:
    print("The target pixel size must be equal to or larger than pix1.")
    target_pixel_size = get_float_input("Enter a new target pixel size: ")

# Create a list of possible even integer box sizes within the input parameters
def generate_even_integers(box_aim, tolerance):
    result = []
    lower_limit = box_aim - tolerance
    upper_limit = box_aim + tolerance

    for num in range(int(lower_limit), int(upper_limit) + 1):
        if num % 2 == 0:
            result.append(num)
    return result

# User input to define how many box size options they want
num_results = int(input("Enter the number of results to select: "))

all_pix2_boxes = generate_even_integers(box_aim, tolerance)

# Check if tolerance is less than 2
if tolerance < 2:
    print("Please provide a wider tolerance:")
    tolerance = get_float_input("Enter the tolerance: ")
    all_pix2_boxes = generate_even_integers(box_aim, tolerance)

# Check if the number of results can be satisfied
while len(all_pix2_boxes) < num_results:
    print("Please provide a smaller number of results or adjust the tolerance:")
    num_results = int(input("Enter the number of results to select: "))
    tolerance = get_float_input("Enter the box size tolerance in pixels: ")
    all_pix2_boxes = generate_even_integers(box_aim, tolerance)

# Define the list of efficient box sizes for FFT
available_box_sizes = [
    24, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 84, 96, 100, 104, 112, 120, 128, 132, 140, 168, 180, 192, 196, 208,
    216, 220, 224, 240, 256, 260, 288, 300, 320, 352, 360, 384, 416, 440, 448, 480, 512, 540, 560, 576, 588, 600,
    630, 640, 648, 672, 686, 700, 720, 750, 756, 768, 784, 800, 810, 840, 864, 882, 896, 900, 960, 972, 980, 1000,
    1008, 1024, 1050, 1080, 1120, 1134, 1152, 1176, 1200, 1250, 1260, 1280, 1296, 1344, 1350, 1372, 1400, 1440, 1458,
    1470, 1500, 1512, 1536, 1568, 1600, 1620, 1680, 1728, 1750, 1764, 1792, 1800, 1890, 1920, 1944, 1960, 2000, 2016,
    2048, 2058, 2100, 2160, 2240, 2250, 2268, 2304, 2352, 2400, 2430, 2450, 2500, 2520, 2560, 2592, 2646, 2688, 2700,
    2744, 2800, 2880, 2916, 2940, 3000, 3024, 3072, 3136, 3150, 3200, 3240, 3360, 3402, 3430, 3456, 3500, 3528, 3584,
    3600, 3750, 3780, 3840, 3888, 3920, 4000, 4032, 4050, 4096
]

answer = input("Is FFT efficiency more important than the exact target pixel size? Enter 'yes' or 'no': ")

while answer.lower() not in ['yes', 'no', 'y', 'n']:
    print("Invalid input. Please enter 'yes' or 'no'.")
    answer = input("Is FFT efficiency more important than the exact target pixel size? Enter 'yes' or 'no': ")

if answer.lower() in ['yes', 'y']:
    # Script 1: FFT Efficiency
    def script1():
        # Calculate the unrounded corresponding box sizes for pix2 that will yield a box with the same dimensions
        # as pix1 in Angstrom
        all_pix1_boxes_unrounded = [(num / pix1) * pix2 for num in all_pix2_boxes]
        # Round these values to the nearest even integer
        all_pix1_boxes_rounded = [int(value) if int(value) % 2 == 0 else int(value) + 1 for value in all_pix1_boxes_unrounded]

        # Calculate the closest box sizes
        closest_values = sorted(
            all_pix1_boxes_rounded,
            key=lambda x: abs(x - all_pix1_boxes_unrounded[all_pix1_boxes_rounded.index(x)])
        )[:num_results]

        # Display the results of the best compatible extraction box sizes that have the closest pixel sizes between datasets after rescaling, and the best rescaling for FFT efficiency
        print(" ")
        print("The best compatible box sizes and their details are:")
        results = set()  # Use a set to store unique results

        while len(results) < num_results:
            for i, value in enumerate(closest_values):
                index = all_pix1_boxes_rounded.index(value)
                deviation = round(value - all_pix1_boxes_unrounded[index], 4)
                pix1_box_size = value
                pix2_box_size = all_pix2_boxes[index]

                # Calculate pix1_box_size_rescaled
                pix1_box_size_rescaled = round(pix1_box_size * pix1 / target_pixel_size)

                # Find the closest available box size in the efficient box sizes list
                closest_available_box_size = min(
                    available_box_sizes,
                    key=lambda x: abs(x - pix1_box_size_rescaled)
                )

                rescaled_pixel_size = pix2_box_size / closest_available_box_size * pix2

                result = (pix1_box_size, closest_available_box_size, target_pixel_size, rescaled_pixel_size)

                # Check if the result is unique
                if result not in results:
                    results.add(result)
                    print(f"Result {len(results)}:")
                    print("Extract pix1 with a box size of:", pix1_box_size, "which should be rescaled to a box size of ",
                          closest_available_box_size, "giving a pixel size of",
                          round(pix1 * pix1_box_size / closest_available_box_size, 5))
                    print("Extract pix2 with a box size of:", pix2_box_size, "which should be rescaled to a box size of ",
                          closest_available_box_size, "giving a pixel size of", round(pix2 * pix2_box_size / closest_available_box_size, 5))
                    print("")
                if len(results) == num_results:
                    break

        # Add an input prompt to hold the console window open
        input("Press Enter to exit...")

    # Call the script1 function
    script1()

else:
    # Script 2: Exact Target Pixel Size
    def script2():
        # Calculate the unrounded corresponding box sizes for pix2 that will yield a box with the same dimensions
        # as pix1 in Angstrom
        all_pix1_boxes_unrounded = [(num / pix1) * pix2 for num in all_pix2_boxes]
        # Round these values to the nearest even integer
        all_pix1_boxes_rounded = [round(value) if round(value) % 2 == 0 else round(value) + 1 for value in
                                  all_pix1_boxes_unrounded]

        closest_values = sorted(
            all_pix1_boxes_rounded,
            key=lambda x: abs(x - all_pix1_boxes_unrounded[all_pix1_boxes_rounded.index(x)])
        )[:num_results]
        # Display the results of the best compatible box sizes that have the closest pixel sizes between datasets after rescaling
        print(" ")
        print("The best compatible box sizes and their details are:")
        for i, value in enumerate(closest_values):
            index = all_pix1_boxes_rounded.index(value)
            deviation = round(value - all_pix1_boxes_unrounded[index], 4)
            pix1_box_size = value
            pix2_box_size = all_pix2_boxes[index]
            # Take into account the target pixel size if this differs from pix1
            if target_pixel_size > pix1:
                pix1_box_size_rescaled = round(pix1_box_size * pix1 / target_pixel_size)

                # Find the closest available box size in the efficient box sizes list
                closest_available_box_size = min(
                    available_box_sizes,
                    key=lambda x: abs(x - pix1_box_size_rescaled)
                )

                rescaled_pixel_size = pix2_box_size / closest_available_box_size * pix2

                print("Extract pix1 with a box size of:", pix1_box_size, "which should be rescaled to a box size of ",
                      closest_available_box_size, "giving a pixel size of", round(pix1 * pix1_box_size / closest_available_box_size, 5))
                print("Extract pix2 with a box size of:", pix2_box_size, "which should be rescaled to a box size of ",
                      closest_available_box_size, "giving a pixel size of", round(rescaled_pixel_size, 5))
            # Ignore target pixel size if this is equal to pix1
            else:
                rescaled_pixel_size = pix2_box_size / pix1_box_size * pix2
                print("Extract pix1 with a box size of:", pix1_box_size, "with a pixel size of", pix1)
                print("Extract pix2 with a box size of:", pix2_box_size, "which should be rescaled to a box size of", pix1_box_size,
                      "giving a pixel size of", round(rescaled_pixel_size, 5))
            print("")

        # Add an input prompt to hold the console window open
        input("Press Enter to exit...")

    # Call the script2 function
    script2()
