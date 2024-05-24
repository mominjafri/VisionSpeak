from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="d0337cbd4f944ab2d58b04ac4ccde385"
)

def speak_txt(text):
    audio = client.generate(
            text=text,
            voice="Kelvin",
            model="eleven_multilingual_v2"
        )
        
        
    return play(audio)
