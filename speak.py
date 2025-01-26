from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="d0337cbd4f944ab2d58b04ac4ccde385"
)

def speak_txt(text, voice_name):
    audio = client.generate(
        text=text,
        voice=voice_name,
        model="eleven_multilingual_v2"
    )
    return audio


