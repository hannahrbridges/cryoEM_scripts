# cryoEM_scripts
python scripts for single particle cryoEM

Scripts was written by Hannah R Bridges with help from ChatGPT for Python3

# compatible_box.py

This script finds the best box sizes and particle downsampling to use when you want to merge two single particle cryo-EM datasets of differing pixel sizes. This is useful if your software can only combine data with exactly the same pixel and box size.

# Notes on preparing your data for compatible_box.py:

Before running the compatible_box.py script, ensure that you have properly calibrated the pixel sizes of your data collections to one another, for example in ChimeraX by adjusting one dataset voxel size until the fit-in-map returns the highest correlation.

Only use the nominal pixel sizes provided by your facility if you have ensured that the 2 maps match perfectly without any rescaling in ChimeraX.

If the calibrated pixel size is different from the nominal magnification used at the start of processing, motioncorr and CTF estimation need to be re-run at the calibrated pixel size, and extraction performed from there.

If you are extracting from motion corrected micrographs, the calibrated pixel size here refers to the binned pixel size (if binning was used).

If you are polishing in RELION, the calibrated pixel size refers to the raw images, which may be in super-resolution pixels

If particles will be extracted in CryoSPARC, the calibrated pixel size refers to that of the motion correction job (whether binning was used or not) and rescaled pixel sizes need to be identical beteeen pix1 and pix2 as it does not tolerate even small differences in merged dataset pixel sizes. This has not been extensively tested as I usually extract from RELION.

# Usage hints for compatibly_box.py:

For the preferred box size, this is usually 1.5 - 2 times the longest diameter of your protein in Angstroms, then converted to pixels using the Apix 
If a narrow range of box tolerance is given, the accuracy of the pixels size matching may be poorer.

If a wide range of tolerance is given, the box sizes with the most accurate pixel size matching may be too small (cut off high resolution information) or too large (include too much noise)

Once the results have been returned, you may need to use the RELION additional argument --force_header in relion extract or polish to specify the pixel size in one dataset to exactly match the other. This should avoid issues where software cannot tolerate even small discrepancies.

Very minor rounding of pixel size can alternatively be acheived by modifying the STAR file in a text editor.

If the calibrated pixel size is different to the nominal pixel size used for initial processing, be aware that further CTF and defocus refinement is likely necessary to achieve the highest resolution.

The script will prompt you to enter the necessary values in the command line, and let you choose between either an FFT-efficient box size, or a box that is closest to your target pixel size - enjoy!!
-
