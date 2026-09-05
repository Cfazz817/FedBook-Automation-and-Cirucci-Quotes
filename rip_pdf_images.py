import sys
import fitz  # PyMuPDF
from pathlib import Path
from dataclasses import dataclass, asdict
import base64
import json


@dataclass
class ImageData:
    filename: str
    filepath: str  # Changed to str to ensure JSON serializability
    bytes: bytes
    source_pdf: str


def extract_images_from_pdf(pdf_path: Path | str):
    # 1. Initialize our Path objects
    pdf_file = Path(pdf_path).resolve()

    # The IF statement: routes the output safely without making duplicates
    if pdf_file.parent.name == pdf_file.stem:
        out_dir = pdf_file.parent
    else:
        out_dir = pdf_file.parent / pdf_file.stem

    # 2. Validate input using pathlib
    if not pdf_file.exists() or not pdf_file.is_file():
        print(
            f"Error: The file '{pdf_file}' does not exist or is not a file.", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    # 3. Open the PDF
    try:
        doc = fitz.open(pdf_file)
    except Exception as e:
        print(f"Fatal error opening PDF: {e}", file=sys.stderr)
        sys.exit(1)

    image_count = 0
    all_image_metadata = []  # List to hold all metadata payload dicts

    # 4. Iterate through pages and extract
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]

            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                ext = base_image["ext"]

                image_filename = f"{pdf_file.stem}_page{page_index + 1}_img{img_index}.{ext}"

                # out_dir / image_filename inherently creates a new Path object
                image_filepath = out_dir / image_filename

                # Write the binary data to disk
                with open(image_filepath, "wb") as f:
                    f.write(image_bytes)

                # Instantiate dataclass, casting Path objects to strings for JSON
                image_data = ImageData(
                    filename=image_filename,
                    filepath=str(image_filepath),
                    bytes=image_bytes,
                    source_pdf=str(pdf_file)
                )

                output_dict = asdict(image_data)
                output_dict['bytes'] = base64.b64encode(
                    output_dict['bytes']).decode('utf-8')

                # Append the dictionary to our tracking list
                all_image_metadata.append(output_dict)
                image_count += 1
                print(
                    f"Success: Extracted image {img_index} from page {page_index + 1} to '{image_filepath.resolve()}'")

            except Exception as e:
                print(
                    f"Warning: Failed to extract image on page {page_index + 1}: {e}", file=sys.stderr)
                continue

    # 5. Write the final JSON file once, outside the loop
    if all_image_metadata:
        # Saving the JSON directly into the generated output directory
        output_file = out_dir / "image_metadata.json"
        output_file.write_text(json.dumps(
            all_image_metadata, indent=4), encoding='utf-8')

    # Clean up and close the document
    doc.close()
    print(f"Success: Extracted {image_count} images to '{out_dir.resolve()}'")
