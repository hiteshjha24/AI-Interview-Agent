import os
import wave
import pyaudio
from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakOptions

load_dotenv()

class TextToSpeech:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("Deepgram API Key missing from .env")
            
        self.client = DeepgramClient(self.api_key)
        self.p = pyaudio.PyAudio()

    def speak(self, text):
        if not text:
            return
            
        try:
            # 1. Use a standard sample rate (16000 Hz) that is safer for all hardware
            RATE = 16000
            
            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",      
                container="none",         
                sample_rate=RATE,        
            )
            
            # 2. Fetch the audio stream
            response = self.client.speak.rest.v("1").stream(
                {"text": text}, 
                options
            )

            # 3. BUFFERING: Collect all audio bytes first to avoid "network stutter" noise
            audio_data = bytearray()
            for chunk in response.stream:
                if chunk:
                    audio_data.extend(chunk)

            # 4. DEBUG: Save to a file to verify quality
            with wave.open("debug_output.wav", "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2) # 2 bytes for 16-bit audio
                wf.setframerate(RATE)
                wf.writeframes(audio_data)

            # 5. Playback
            stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                output=True
            )
            
            stream.write(bytes(audio_data))
            
            stream.stop_stream()
            stream.close()

        except Exception as e:
            print(f"TTS Error: {e}")

    def cleanup(self):
        self.p.terminate()

    # --- FIX: THIS METHOD IS NOW INSIDE THE CLASS ---
    def generate_audio_stream(self, text):
        """
        Generates audio but does NOT play it. 
        Yields chunks of bytes for the API to send to the client.
        """
        if not text:
            return

        try:
            # Same options as before, but we will yield the result
            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",      
                container="none",         
                sample_rate=16000,        
            )
            
            response = self.client.speak.rest.v("1").stream(
                {"text": text}, 
                options
            )

            for chunk in response.stream:
                if chunk:
                    yield chunk
                    
        except Exception as e:
            print(f"TTS Generation Error: {e}")

if __name__ == "__main__":
    tts = TextToSpeech()
    print("Generating audio... (Wait a moment)")
    tts.speak("Hello Hitesh. This is a test using sixteen kilohertz audio. It should sound much clearer now.")
    print("Done. Check 'debug_output.wav' in your folder if it still sounds bad.")
    tts.cleanup()