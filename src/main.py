import pandas as pd
import os
from PIL import Image

def convert_tif_to_text(file, output_folder):
    """
    Converts a .tif image to a text file of RGB pixel values.
    
    Args:
        file (str): Path to input .tif file.
        output_folder (str): Directory where output .txt file will be saved.
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

# Example usage:
# convert_tif_to_text("input_image.tif", "./output")



def main():
    print("Biostats: Tiff RBG Tile Image Processor")
    
    # Convert tif files to readable text files (___)
    for file in os.listdir('data/raw_tif_files'):
        if file.endswith("Merge.tif"):
            output_folder = "test_output"
        else:
            output_folder = "test_input"
        convert_tif_to_text(os.path.join('data/raw_tif_files', file), output_folder)

    # df = pd.read_csv("../data/sample.csv")
    # print(df.head())

if __name__ == "__main__":
    main()
