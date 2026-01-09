import time
import threading
from src.transcription.deepgram_stt import RealTimeTranscriber
from src.brain.llm_agent import InterviewBrain
from src.audio.tts_engine import TextToSpeech

class InterviewAgent(RealTimeTranscriber):
    def __init__(self):
        # Initialize the ears (Parent class)
        super().__init__()
        
        # Initialize the Brain and Mouth
        print("Initializing Brain (Groq)...")
        self.brain = InterviewBrain(provider="groq")
        
        print("Initializing Mouth (Deepgram)...")
        self.mouth = TextToSpeech()
        
        # State to prevent overlap
        self.is_processing = False

    def on_message(self, sender, result, **kwargs):
        # 1. If we are already talking/thinking, ignore new audio
        if self.is_processing:
            return

        # 2. Get the transcript
        sentence = result.channel.alternatives[0].transcript
        
        # 3. If the sentence is empty, ignore it
        if len(sentence.strip()) == 0:
            return

        # 4. Process the input
        self.process_conversation(sentence)

    def process_conversation(self, user_text):
        try:
            self.is_processing = True
            print(f"\nCandidate: {user_text}")

            # We pause the microphone stream so the AI doesn't hear itself
            if self.stream.is_active():
                self.stream.stop_stream()

            ai_response = self.brain.get_response(user_text)
            print(f"Interviewer: {ai_response}")
            
            self.mouth.speak(ai_response)

        except Exception as e:
            print(f"Error in conversation loop: {e}")
            
        finally:
            # Turn the mic back on for the user's turn
            print("\nListening...")
            if self.stream.is_stopped():
                self.stream.start_stream()
            
            self.is_processing = False

if __name__ == "__main__":
    print("-------------------------------------------------")
    print("   V2V INTERVIEW AGENT (Deepgram + Groq + Aura)  ")
    print("-------------------------------------------------")
    
    # Initialize the integrated agent
    agent = InterviewAgent()

    agent.start_transcription()
