"""
Equipment for LLagents: OCR utilities for extracting text.

Extract text from images using tesseract (printed material) and EasyOCR (general purpose).
Includes multi language support.
"""

import base64
from io import BytesIO
from pathlib import Path
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import easyocr
import easyocr.utils
from PIL import Image
import pytesseract


def load_image_from_input(image_input: str) -> Image.Image:
    """
    Load image from file path or base64 string.

    Args:
        image_input: File path or base64 encoded image string.

    Returns:
        PIL Image object.
    """
    # Check if input is base64 (common base64 image prefixes)
    if any(
        image_input.startswith(prefix)
        for prefix in ["data:image/", "/9j/", "iVBOR", "R0lGOD", "UklGR"]
    ):
        # Handle base64
        if image_input.startswith("data:image/"):
            # Remove data:image/[type];base64, prefix
            image_input = image_input.split(",")[1]

        # Decode base64 and create PIL Image
        image_data = base64.b64decode(image_input)
        return Image.open(BytesIO(image_data))

    # Handle file path
    img_path = Path(image_input).resolve()
    return Image.open(img_path)


class ReadingTextOCRToolSpec(BaseToolSpec):
    """Reading Text OCR tool spec."""

    def __init__(self) -> None:
        """Initialize the Reading Text OCR tool spec."""

    spec_functions = [
        "printed_material_extract_text",
        "general_purpose_extract_text",
    ]

    def general_purpose_extract_text(
        self,
        image_path_or_base64: str,
        lang_list: list[str],
    ) -> str:
        """
        Extract text from an image using EasyOCR.

        This tool is designed to extract text from general purpose images.
        If the image is a printed material, use the printed_material_extract_text tool.

        Args:
            image_path: Path to the image file.
            lang_list: Language codes (ISO 639) for languages to be recognized during analysis.

        Returns:
            Extracted text from the image or an error message.
        """
        try:
            if len(lang_list) == 0:
                lang_list = ["en"]
            reader = easyocr.Reader(lang_list)
            image = load_image_from_input(image_path_or_base64)
            results = reader.readtext(image)
            extracted_text = " ".join([result[1] for result in results])

            extracted_text = extracted_text.strip()

            if extracted_text:
                return f"Extracted text: {extracted_text}\n"
            return "No text found in the image"

        except easyocr.utils.Image.UnidentifiedImageError as e:
            return f"General Purpose Reading Text Module Error (EasyOCR): {e!s}"

    def printed_material_extract_text(
        self,
        image_path_or_base64: str,
        lang: str = "eng",
    ) -> str:
        """
        Extract text from an image using tesseract OCR.

        This tool is designed to extract text from printed material.
        If the image is not a printed material, use the general_purpose_extract_text tool.

        Args:
            image_input: Path to the image file or string representation of the image.
            lang: Language of the text in the image.

        Returns:
            Extracted text from the image.
        """
        try:
            print("🔍 Extracting text using tesseract")
            image = load_image_from_input(image_path_or_base64)

            # Process with tesseract
            extracted_text = pytesseract.image_to_string(image, lang=lang)
            extracted_text = extracted_text.strip()

            if extracted_text:
                return f"Extracted text: {extracted_text}\n"
            return "No text found in the image"

        except pytesseract.TesseractError as e:
            return f"Reading Printed Material Text Error (tesseract): {e!s}"
