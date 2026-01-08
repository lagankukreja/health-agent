
"""
AI Health Agent - A beginner-friendly health assistant
This agent helps with health questions, symptom tracking, and health tips
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import json

# Loading environment variables from .env file
load_dotenv()

# API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class HealthAgent:
    """Main Health Agent Class - This is the brain of our agent"""
    
    def __init__(self):
        """Initialize the agent with empty memory"""
        # This stores all our conversation history
        self.conversation_history = []
        
        # This stores symptoms the user reports
        self.symptoms_log = []
        
        # System prompt - This tells the AI how to behave
        self.system_prompt = """You are a helpful AI health assistant. 

Your role:
- Answer health-related questions with accurate, helpful information
- Provide general health tips and wellness advice
- Help users track their symptoms
- Be empathetic and supportive

Important rules:
- Always remind users you're not a replacement for professional medical advice
- For serious symptoms, advise users to consult a healthcare provider
- Be clear, concise, and caring in your responses
- If you're unsure, say so and recommend seeing a doctor

Keep responses conversational and easy to understand."""

        # Add system prompt to conversation history
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def log_symptom(self, symptom):
        """Save a symptom with timestamp"""
        symptom_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symptom": symptom
        }
        self.symptoms_log.append(symptom_entry)
        return f"✓ Logged symptom: {symptom}"
    
    def get_symptoms_summary(self):
        """Get a summary of all logged symptoms"""
        if not self.symptoms_log:
            return "No symptoms logged yet."
        
        summary = "📋 Your Symptom Log:\n" + "-" * 40 + "\n"
        for entry in self.symptoms_log:
            summary += f"{entry['timestamp']}: {entry['symptom']}\n"
        return summary
    
    def chat(self, user_message):
        """Main chat function - sends message to AI and gets response"""
        
        # Check if user wants to log a symptom
        if user_message.lower().startswith("log symptom:"):
            symptom = user_message[12:].strip()
            return self.log_symptom(symptom)
        
        # Check if user wants to see symptoms
        if user_message.lower() in ["show symptoms", "my symptoms", "symptom log"]:
            return self.get_symptoms_summary()
        
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call OpenAI API
            # This sends our conversation to ChatGPT and gets a response
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4 mini - fast and cost-effective
                messages=self.conversation_history,
                temperature=0.7,  # Controls randomness (0=focused, 1=creative)
                max_tokens=500  # Maximum length of response
            )
            
            # Extract the AI's response
            assistant_message = response.choices[0].message.content
            
            # Add AI response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"❌ Error: {str(e)}\nPlease check your API key and internet connection."
    
    def save_session(self, filename="health_session.json"):
        """Save the current session to a file"""
        session_data = {
            "conversation": self.conversation_history,
            "symptoms": self.symptoms_log,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return f"✓ Session saved to {filename}"


def print_welcome():
    """Print a nice welcome message"""
    print("\n" + "=" * 60)
    print("🏥 AI HEALTH AGENT - Your Personal Health Assistant")
    print("=" * 60)
    print("\n📌 What I can do:")
    print("  • Answer health questions")
    print("  • Track your symptoms")
    print("  • Provide health tips")
    print("  • Remember our conversation")
    print("\n💡 Special Commands:")
    print("  • 'log symptom: [description]' - Log a symptom")
    print("  • 'show symptoms' - View your symptom log")
    print("  • 'save' - Save this session")
    print("  • 'quit' or 'exit' - End the conversation")
    print("\n⚠️  Remember: I'm not a doctor. For serious concerns, consult a healthcare professional.")
    print("=" * 60 + "\n")


def main():
    """Main function - runs the agent"""
    
    # Print welcome message
    print_welcome()
    
    # Create our health agent
    agent = HealthAgent()
    
    print("Agent: Hello! I'm your AI Health Assistant. How can I help you today?\n")
    
    # Main conversation loop
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nAgent: Take care! Stay healthy! 👋")
            # Ask if they want to save
            save = input("\nSave this session? (yes/no): ").lower()
            if save == 'yes':
                print(agent.save_session())
            break
        
        # Check if user wants to save
        if user_input.lower() == 'save':
            print("\n" + agent.save_session())
            continue
        
        # Skip empty input
        if not user_input:
            continue
        
        # Get response from agent
        response = agent.chat(user_input)
        
        # Print response
        print(f"\nAgent: {response}\n")


# This runs when you execute the script
if __name__ == "__main__":
    main()