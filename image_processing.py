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
    aws_access_key_id=os.getenv("AWS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS"),
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
