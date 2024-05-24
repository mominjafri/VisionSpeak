from googletrans import Translator

def translate_text(text, dest_language):
    print(text)
    translator = Translator()
    translated = translator.translate(text, dest=dest_language).text
    print (translated)
    return translated