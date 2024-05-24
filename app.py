from flask import Flask, render_template, request, session, jsonify, redirect, url_for
# from text_processing import translate_text
from image_processing import extract_text_from_image, extract_text_from_pdf
from gtts import gTTS
from language_codes import language_codes
import io
from speak import speak_txt
import pygame
import deepl

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Global variable to store the selected language code
selected_language_code = ''

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
    return render_template('index.html', language=selected_language, language_codes=language_codes)


# Route for processing the language selection and redirecting to index
@app.route('/change_language', methods=['POST'])
def change_language():
    # global selected_language_code
    # language = request.form['language']
    # # Set the selected language code
    # selected_language_code = language_codes.get(language)
    # # Redirect to index
    # return redirect(url_for('index'))

    selected_language = request.form.get('language')
    session['selected_language'] = selected_language
    return 'Language selected successfully', 200


# Route for extracting text from image or PDF
@app.route('/extract_text', methods=['POST'])
def extract_text():
    global text_area
    image_file = request.files['image']
    if image_file:
        if image_file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(image_file)
        else:
            extracted_text = extract_text_from_image(image_file)
        text_area = extracted_text
        return jsonify({'text': extracted_text})
    return jsonify({'error': 'No image file received'})


@app.route('/translate_text', methods=['POST'])
def translate_text_endpoint():
    global text_area, selected_language_code
    text = text_area.strip()

    selected_language_code = session.get('selected_language')
    selected_language_code = selected_language_code.upper()
    print(selected_language_code)

    auth_key = "911156d2-68da-46ea-9c10-c1dec5127149:fx"  # Replace with your key
    translator = deepl.Translator(auth_key)

    if selected_language_code:
        result = translator.translate_text(text, target_lang = selected_language_code)
        text_area = result.text
        print(result.text)  
        return jsonify({'translated_text': result.text})
    else:
        return jsonify({'error': 'No language selected'})

# Route for speaking text
@app.route('/speak_text', methods=['POST'])
def speak_text():
    global text_area
    text = text_area.strip()
    if text:  # Ensure there's non-empty text to speak
        speak_txt(text)
    return jsonify({'error': 'No text to speak'})

if __name__ == "__main__":
    app.run(debug=True)




