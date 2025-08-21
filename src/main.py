import pandas as pd
import os, re
import numpy as np
from PIL import Image

def convert_tif_to_text(file, output_folder):
    """
    Converts a .tif image to a text file of RGB pixel values.
    
    Args:
        file (str): Path to input .tif file.
        output_folder (str): Directory where output .txt file will be saved.
    Returns:
        width, height: int, int: dimensions of the image.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    

    # Derive output filename
    base = os.path.splitext(os.path.basename(file))[0]
    output_path = os.path.join(output_folder, f"{base}_pixels.txt")
    
    with Image.open(file) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        width, height = img.size
        pixels = img.load()

        with open(output_path, 'w') as txtfile:
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    txtfile.write(f"{r},{g},{b}\n")
    
    print(f"Image data saved as RGB text to {output_path}")
    return width, height


def merge_channels(folder_path, channel_a, channel_b, output_folder):
    """
    For each set ID, merge the contents of channel_a and channel_b files
    by summing RGB tuples line by line.

    Args:
        folder_path (str): folder containing input files
        channel_a (str): first channel to merge (e.g. "CH2")
        channel_b (str): second channel to merge (e.g. "CH4")
        output_folder (str): where merged files will be written
    """
    # regex to extract the set ID and channel
    pattern = re.compile(r'(?:[^_]*_){6}(\d{5})_(CH\d)')

    # map: set_id -> {channel: filepath}
    files_by_set = {}

    for filename in os.listdir(folder_path):
        match = pattern.search(filename)
        if match:
            set_id, channel = match.groups()
            files_by_set.setdefault(set_id, {})[channel] = os.path.join(folder_path, filename)

    os.makedirs(output_folder, exist_ok=True)

    for set_id, channels in sorted(files_by_set.items()):
        if channel_a in channels and channel_b in channels:
            file_a = channels[channel_a]
            file_b = channels[channel_b]

            merged_lines = []
            with open(file_a, "r") as fa, open(file_b, "r") as fb:
                for line_a, line_b in zip(fa, fb):
                    # parse tuples, e.g. "(1,0,0)"
                    tup_a = tuple(map(int, line_a.strip("()\n ").split(",")))
                    tup_b = tuple(map(int, line_b.strip("()\n ").split(",")))

                    # sum elementwise
                    merged = tuple(a + b for a, b in zip(tup_a, tup_b))
                    merged_lines.append(f"{merged}\n")

            # write merged output
            out_file = os.path.join(output_folder, f"merged_{set_id}_{channel_a}_{channel_b}.txt")
            with open(out_file, "w") as fout:
                fout.writelines(merged_lines)

            print(f"Merged {set_id}: {channel_a} + {channel_b} -> {out_file}")
        else:
            print(f"Skipping {set_id}: missing {channel_a} or {channel_b}")


def convert_merged_txts_to_tifs(folder, output_folder, width, height):
    """
    Convert all 'Merged*.txt' files in a folder into TIFF images.
    
    Args:
        folder (str): Path to the folder containing txt files.
        output_folder (str): Directory where TIFF files will be saved.
        width (int): Width of the image.
        height (int): Height of the image.
    """

    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(folder):
        if filename.startswith("merged") and filename.endswith(".txt"):
            txt_path = os.path.join(folder, filename)
            print(f"Processing {txt_path}")
            # Read RGB tuples from txt
            rgb_list = []
            with open(txt_path, "r") as f:
                for line in f:
                    tup = tuple(map(int, line.strip("()\n ").split(",")))
                    rgb_list.append(tup)

            # Convert to NumPy array (H, W, 3)
            arr = np.array(rgb_list, dtype=np.uint8).reshape((height, width, 3))

            # Save as TIFF
            tif_name = os.path.splitext(filename)[0] + ".tif"
            tif_path = os.path.join(output_folder, tif_name)
            img = Image.fromarray(arr)
            img.save(tif_path)

            print(f"Converted {filename} -> {tif_name}")

def main():
    print("Biostats: Tiff RBG Tile Image Processor")
    
    # Convert tif files to readable text files (___)
    for file in os.listdir('data/raw_tif_files'):
        if file.endswith("Merge.tif"):
            output_folder = "data/test_output"
        else:
            output_folder = "data/test_input"
        # Uncomment this line below if we have new tif files to process
        w, h = convert_tif_to_text(os.path.join('data/raw_tif_files', file), output_folder)

    colour_mapping = {
        'R': 'CH1',
        'G': 'CH2',
        'B': 'CH4',
        'All': 'CH3'
    }
    # User specifies 2 colours to merge:
    merged_colours = ['R', 'G']
    print(f"Merging colours: {', '.join(merged_colours)}")
    merge_channels('data/test_input', colour_mapping[merged_colours[0]], colour_mapping[merged_colours[1]], 'data/test_output')
    convert_merged_txts_to_tifs('data/test_output', 'data/merged_tif_files', w, h)

if __name__ == "__main__":
    main()
