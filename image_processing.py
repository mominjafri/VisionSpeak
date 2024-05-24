# from PIL import Image
# import pytesseract
# from pypdf import PdfReader

# def extract_text_from_image(image_path, language='eng'):
#     image = Image.open(image_path)
#     if language == 'urd':
#         # Set Tesseract to use Urdu language
#         # WINDOWS pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\\tesseract.exe'
#         pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
#         custom_config = r'--oem 3 --psm 6'
#         extracted_text = pytesseract.image_to_string(image, lang='urd', config=custom_config)
#     else:
#         # Default to English language
#         # WINDOWS pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\\tesseract.exe'
#         pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
#         extracted_text = pytesseract.image_to_string(image)
#     return extracted_text

# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     all_text = ""
#     for page in reader.pages:
#         text = page.extract_text()
#         if text:
#             all_text += text + "\n\n"
#     return all_text

import easyocr
from PIL import Image
import io
from pypdf import PdfReader

# Initialize the easyocr reader for specific languages
reader = easyocr.Reader(['en', 'ur'])

def extract_text_from_image(image_path, language='eng'):
    image = Image.open(image_path)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()

    if language == 'urd':
        # Extract text using easyocr with Urdu language
        result = reader.readtext(image_bytes, detail=0, paragraph=True, decoder='wordbeamsearch')
    else:
        # Default to English language
        result = reader.readtext(image_bytes, detail=0, paragraph=True, decoder='wordbeamsearch')
    
    extracted_text = ' '.join(result)
    return extracted_text

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n\n"
    return all_text

