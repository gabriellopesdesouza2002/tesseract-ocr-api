import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from tqdm import tqdm
import uuid


def pdf_to_images(pdf_path: str, dpi: int = 300, limit_pages: int | None = None) -> list[str]:
    """Converts PDF pages to images with given DPI."""
    images = []
    with fitz.open(pdf_path) as pdf:
        total_pages = len(pdf) if limit_pages is None else min(limit_pages, len(pdf))
        for i in tqdm(range(total_pages), desc='PDF→IMG'):
            page = pdf.load_page(i)
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            img_path = f'/tmp/page_{i}.png'
            pix.save(img_path)
            images.append(img_path)
    return images


def ocr_pdf(pdf_path: str, dpi: int = 300, lang: str = 'por', limit_pages: int | None = None) -> str:
    """Performs OCR on a PDF using Tesseract with a configurable language."""
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    temp_txt = f'/tmp/{uuid.uuid4()}.txt'
    images = pdf_to_images(pdf_path, dpi=dpi, limit_pages=limit_pages)

    with open(temp_txt, 'w', encoding='utf-8') as f_out:
        for img_path in tqdm(images, desc=f'OCR ({lang})'):
            try:
                text = pytesseract.image_to_string(Image.open(img_path), lang=lang, timeout=120)
                f_out.write(text + '\n')
            except Exception as e:
                print(f'Error processing {img_path}: {e}')

    with open(temp_txt, 'r', encoding='utf-8') as f:
        text_final = f.read()

    os.remove(temp_txt)
    for img in images:
        os.remove(img)
    return text_final.strip()
