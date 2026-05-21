import fitz
import os

def extract_images_from_pdf(pdf_path, output_folder="data/processed/images"):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    image_paths = []

    for page_index in range(len(doc)):

        page = doc[page_index]

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            image_path = f"{output_folder}/page_{page_index+1}_{img_index}.{image_ext}"

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

    return image_paths