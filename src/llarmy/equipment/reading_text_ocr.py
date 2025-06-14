"""
Equipment for LLagents: OCR utilities for extracting text.

Extract text from images using tesseract (printed material) and EasyOCR (general purpose).
"""

from pathlib import Path
from typing import Union
import easyocr
import easyocr.utils
from PIL import Image
import pytesseract


# OCR with tesseract for printed material
def printed_material_extract_text(
    image_input: Union[str, Image.Image],
    lang: str = "eng",
) -> str:
    """
    Extract text from an image using tesseract OCR.

    Args:
        image_input: Path to the image file or a PIL Image object.
        lang: Language of the text in the image.

    Returns:
        Extracted text from the image.
    """
    try:
        print("🔍 Extracting text using tesseract")
        # Handle either image path or PIL Image
        image: Image.Image
        if isinstance(image_input, str):
            img_path = Path(image_input).resolve()
            image = Image.open(img_path)
        elif isinstance(image_input, Image.Image):
            image = image_input

        # Process with tesseract
        extracted_text = pytesseract.image_to_string(image, lang=lang)
        extracted_text = extracted_text.strip()

        if extracted_text:
            return f"Extracted text: {extracted_text}\n"
        return "No text found in the image"

    except pytesseract.TesseractError as e:
        return f"Reading Printed Material Text Error (tesseract): {e!s}"


# Enhanced OCR with multiple backends
def general_purpose_extract_text(
    image_path: str,
    lang_list: list[str],
) -> str:
    """
    Extract text from an image using EasyOCR.

    Args:
        image_path: Path to the image file.
        lang_list: Language codes (ISO 639) for languages to be recognized during analysis.

    Returns:
        Extracted text from the image or an error message.
    """
    try:
        img_path = Path(image_path).resolve()
        if len(lang_list) == 0:
            lang_list = ["en"]
        reader = easyocr.Reader(lang_list)
        results = reader.readtext(str(img_path))
        extracted_text = " ".join([result[1] for result in results])

        extracted_text = extracted_text.strip()

        if extracted_text:
            return f"Extracted text: {extracted_text}\n"
        return "No text found in the image"

    except easyocr.utils.Image.UnidentifiedImageError as e:
        return f"General Purpose Reading Text Module Error (EasyOCR): {e!s}"
