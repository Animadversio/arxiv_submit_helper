import os
from PIL import Image


text_file_path = "refered_figs.tex"
search_directory = 'NeurIPS 2023 Geometry of Diffusion_Best_Arxiv'

# TODO: obtain the listed file from tex file. 
# read the list of file paths from the text file
with open(text_file_path, 'r') as file:
    listed_files = set(file.read().splitlines())

# Function to traverse the directory and its subdirectories
def traverse_dir_prune_files(directory, rm=False, excluded=[".tex",".sty",".bib"]):
    """Traverse a directory and find files not mentioned in the text file. """
    for root, _, files in os.walk(directory):
        for file in files:
            # Construct the relative path of the current file
            relative_path = os.path.relpath(os.path.join(root, file), start=directory)
            file_extension = os.path.splitext(relative_path)[1]
            # Check if this relative path is not in the list of known files and not in the excluded extensions
            if relative_path not in listed_files and file_extension not in excluded:
                print(relative_path)
                if rm:
                    os.remove(os.path.join(directory, relative_path))
                    print(os.path.join(directory, relative_path), "removed")
# Start the traversal
traverse_dir_prune_files(search_directory)


def compress_images_in_directory(input_directory, output_directory=None, size_limit=0*1024*1024, 
                                quality=75, suffix="_compressed"):
    """
    Compresses image files in the specified directory that are larger than the given size limit
    and saves them into another directory.
    
    :param input_directory: Path to the directory to search for image files.
    :param output_directory: Path to the directory where compressed images will be saved.
            Recommended to be different from the input directory to avoid overwriting original images and easier cleanup.
    :param size_limit: File size limit in bytes. Files larger than this will be compressed. Default is 0MB.
    :param quality: The image quality to use for the output JPEG files, where 1 is worst and 95 is best.
                    Lower quality numbers will result in smaller file sizes.
    """
    if output_directory is None:
        output_directory = input_directory
    # Create the output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for root, _, files in os.walk(input_directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is an image, its size exceeds the specified limit, and it is not already compressed
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) and \
               (os.path.getsize(file_path) > size_limit):
                # and not file_path.lower().endswith("_compressed.jpg"):
                original_size = os.path.getsize(file_path)
                try:
                    # Open the image
                    with Image.open(file_path) as img:
                        # Convert the image to RGB if it's not already, as JPEG doesn't support alpha channel
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")

                        # Construct the new filename within the output directory
                        relative_path = os.path.relpath(file_path, start=input_directory)
                        new_file_path = os.path.join(output_directory, relative_path)
                        new_file_directory = os.path.dirname(new_file_path)
                        
                        # Ensure the directory structure in the output directory mirrors that of the input
                        if not os.path.exists(new_file_directory):
                            os.makedirs(new_file_directory)
                        
                        new_filename = os.path.splitext(new_file_path)[0] + f"{suffix}.jpg"
                        # Save the image with the specified quality
                        img.save(new_filename, "JPEG", quality=quality) 
                        compressed_size = os.path.getsize(new_filename)
                        print(f"Compressed and saved: {new_filename}")
                        print(f"Original size: {original_size / 1024:.2f} KB, Compressed size: {compressed_size / 1024:.2f} KB")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Example usage
# input_directory = '/path/to/your/input/images'
# output_directory = '/path/to/your/output/images'
# compress_images_in_directory(input_directory, output_directory)


directory = '/Users/binxuwang/Library/CloudStorage/OneDrive-HarvardUniversity/NeurIPS2023_Diffusion/NeurIPS 2023 Geometry of Diffusion_Best_Arxiv/figs'
outdir = "figs"
compress_images_in_directory(directory, outdir, quality=75, suffix="")

