from filetime import get_alpha_dirlist
from rip_pdf_images import extract_images_from_pdf
from pathlib import Path
import sys


def main(directory: str):
    pdfs = get_alpha_dirlist(directory)
    for pdf in pdfs:
        if pdf.suffix.lower() == '.pdf':
            print(f"Extracting images from: {pdf}")
            extract_images_from_pdf(pdf)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must provide a directory of pdfs: 'python extract_images_dir.py ~/path/to/dir'")
        sys.exit(1)
    input_dir = sys.argv[1]
    try:
        main(input_dir)
    except TypeError as e:
        print(f"Error: {e}. Ensure you provide a valid directory path.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
