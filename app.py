import os
from flask import Flask, render_template, request, session, jsonify, send_file, make_response
from image_processing import extract_text_from_image, extract_text_from_pdf
from language_codes import language_codes
from speak import speak_txt
from io import BytesIO
import deepl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document

app = Flask(__name__)
app.secret_key = 'your_secret_key'

voice_names = ["Momin", "Danny", "Laurie", "Hassan"]

@app.route('/')
def load():
    return render_template('load.html', language_codes=language_codes)


@app.route('/select_language', methods=['POST'])
def select_language():
    selected_language = request.form.get('language')
    session['selected_language'] = selected_language
    return jsonify(success=True), 200


@app.route('/index')
def index():
    selected_language = session.get('selected_language', 'en')
    return render_template('index.html', language=selected_language, language_codes=language_codes, voice_names=voice_names)


@app.route('/change_language', methods=['POST'])
def change_language():
    selected_language = request.form.get('language')
    session['selected_language'] = selected_language
    return 'Language selected successfully', 200


@app.route('/extract_text', methods=['POST'])
def extract_text():
    image_file = request.files['image']
    if image_file:
        if image_file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(image_file)
        else:
            extracted_text = extract_text_from_image(image_file)
        return jsonify({'text': extracted_text})
    return jsonify({'error': 'No image file received'})


@app.route('/translate_text', methods=['POST'])
def translate_text_endpoint():
    text = request.form['text'].strip()
    selected_language_code = session.get('selected_language', 'EN').upper()
    print(selected_language_code)

    auth_key = "911156d2-68da-46ea-9c10-c1dec5127149:fx"  # Replace with your key
    translator = deepl.Translator(auth_key)

    if selected_language_code:
        result = translator.translate_text(text, target_lang=selected_language_code)
        translated_text = result.text
        print(translated_text)
        return jsonify({'translated_text': translated_text})
    else:
        return jsonify({'error': 'No language selected'})


@app.route('/speak_text', methods=['POST'])
def speak_text():
    text = request.form['text'].strip()
    voice_name = request.form.get('voice', 'Kelvin')  # Default to 'Kelvin' if no voice is selected
    if text:
        audio = speak_txt(text, voice_name)
        response = make_response(audio)
        response.headers.set('Content-Type', 'audio/mpeg')
        response.headers.set('Content-Disposition', 'attachment', filename='speech.mp3')
        return response
    return jsonify({'error': 'No text to speak'})


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    text = request.form['text']
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.drawString(100, height - 100, text)
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')


@app.route('/generate_docx', methods=['POST'])
def generate_docx():
    text = request.form['text']
    buffer = BytesIO()
    document = Document()
    document.add_paragraph(text)
    document.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='output.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

#import sys
#path = '/home//yourproject'
#if path not in sys.path:
#    sys.path.append(path)
#from yourapp import app as application



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
