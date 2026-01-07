import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class InterviewBrain:
    def __init__(self, provider="groq"): 
        # Options for provider: 'openai' or 'groq'
        self.provider = provider
        self.history = [
            {"role": "system", "content": "You are a strict but fair Technical Interviewer. You ask one question at a time. Keep your responses short (under 2 sentences) to keep the conversation flowing naturally. Do not say 'Great' or 'Okay' too often. Dive straight into the next question."}
        ]

        if provider == "groq":
            # Groq is recommended for speed (Llama 3 model)
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=os.getenv("GROQ_API_KEY")
            )
            self.model = "llama-3.1-8b-instant" 
        else:
            # Fallback to OpenAI if you prefer
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4o-mini" 

    def get_response(self, user_input):
        # 1. Add user's input to history so the bot remembers context
        self.history.append({"role": "user", "content": user_input})

        try:
            # 2. Call the LLM
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=0.7,
                max_tokens=150, # Keep it short for speed
                stream=False    
            )

            ai_response = completion.choices[0].message.content
            
            # 3. Add AI's response to history
            self.history.append({"role": "assistant", "content": ai_response})
            
            return ai_response

        except Exception as e:
            print(f"LLM Error: {e}")
            return "I'm sorry, I encountered an error processing that."

# --- TEST BLOCK (Run this file directly to chat via text) ---
if __name__ == "__main__":
    # Ensure you have GROQ_API_KEY in your .env file
    # If using OpenAI, change provider to "openai"
    bot = InterviewBrain(provider="groq") 
    
    print("Bot: Hello! I am your interviewer today. (Type 'quit' to exit)")
    while True:
        u_input = input("You: ")
        if u_input.lower() in ["quit", "exit"]:
            break
        
        response = bot.get_response(u_input)
        print(f"Bot: {response}")