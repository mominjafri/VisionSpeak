# import easyocr
# from PIL import Image
# import io
# from pypdf import PdfReader

# # Initialize the easyocr reader for specific languages
# reader = easyocr.Reader(['en', 'ur'])

# def extract_text_from_image(image_path, language='eng'):
#     image = Image.open(image_path)
#     image_bytes = io.BytesIO()
#     image.save(image_bytes, format='PNG')
#     image_bytes = image_bytes.getvalue()

#     if language == 'urd':
#         # Extract text using easyocr with Urdu language
#         result = reader.readtext(image_bytes, detail=0, paragraph=True, decoder='wordbeamsearch')
#     else:
#         # Default to English language
#         result = reader.readtext(image_bytes, detail=0, paragraph=True, decoder='wordbeamsearch')
    
#     extracted_text = ' '.join(result)
#     return extracted_text

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n\n"
    return all_text

import boto3
from PIL import Image
import os
from pypdf import PdfReader

textract = boto3.client(
    'textract',
    aws_access_key_id=os.getenv('AKIATCKAQBAQEE2G42YO'),
    aws_secret_access_key=os.getenv('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'),
    region_name='us-east-2'
)



def extract_text_from_image(image_file, language='eng'):
    image_bytes = image_file.read()

    response = textract.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    extracted_text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + ' '

    return extracted_text.strip()

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n\n"
    return all_text
