import os
import time  # Changed from asyncio to time
from dotenv import load_dotenv
import pyaudio 

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()

# --- CONFIGURATION ---
INPUT_DEVICE_INDEX = 45

class RealTimeTranscriber:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        self.config = DeepgramClientOptions(options={"keepalive": "true"})
        self.deepgram = DeepgramClient(self.api_key, self.config)
        self.connection = None
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def on_message(self, sender, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) > 0:
            print(f"\nUser: {sentence}")
        else:
            print(".", end="", flush=True)

    def on_error(self, sender, error, **kwargs):
        print(f"\nDeepgram Error: {error}")

    def start_transcription(self):
        try:
            self.connection = self.deepgram.listen.websocket.v("1")
            self.connection.on(LiveTranscriptionEvents.Transcript, self.on_message)
            self.connection.on(LiveTranscriptionEvents.Error, self.on_error)

            options = LiveOptions(
                model="nova-2", 
                language="en-US", 
                smart_format=True,
                encoding="linear16",
                channels=1,
                sample_rate=16000,
            )

            if self.connection.start(options) is False:
                print("Failed to connect to Deepgram")
                return

            def callback(in_data, frame_count, time_info, status):
                try:
                    # Only send data if the connection is open
                    if self.connection: 
                        self.connection.send(in_data)
                except Exception:
                    pass
                return (None, pyaudio.paContinue)

            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                stream_callback=callback,
                frames_per_buffer=1024
            )

            print(f"Listening on Device Index {INPUT_DEVICE_INDEX}...")
            self.stream.start_stream()

            # --- KEY FIX IS HERE ---
            # We use 'while True' so the program stays alive even if we 
            # temporarily pause the stream in main.py
            while True:
                time.sleep(0.5) 

        except KeyboardInterrupt:
            print("\nStopping...")
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            if self.connection:
                self.connection.finish()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            self.audio.terminate()

if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.start_transcription()