# BioStats-Image-Processing-Colour-Merge
Input: set of "tile" output files (sets of 4 tiffs) that make up one big HiDef image. Each tile has an associated file for one of each the components Red, Green, Blue, and Overlay (R G B combined) 

Goal: Merge 2+ colours of tiles together. 

Method: For all "pixels" in an input tile of the form (r,g,b), add them up to the values of the pixel from the corresponding other selected colour.

Output: image with R pixels (end with ch2)  G pixels (end with ch1) merged for each tile

# To run, click on the TERMINAL tab below and type:
python src/main.py
