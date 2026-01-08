"""
Advanced Health Agent with Function Calling
This agent can intelligently decide when to use tools!
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============= TOOLS/FUNCTIONS THE AGENT CAN USE =============

def calculate_bmi(weight_kg, height_cm):
    """Calculate Body Mass Index"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return {
        "bmi": round(bmi, 2),
        "category": category,
        "message": f"Your BMI is {round(bmi, 2)} ({category})"
    }


def calculate_daily_water(weight_kg, activity_level="moderate"):
    """Calculate recommended daily water intake"""
    # Base: 30-35ml per kg of body weight
    base_ml = weight_kg * 33
    
    multipliers = {
        "sedentary": 1.0,
        "moderate": 1.2,
        "active": 1.5
    }
    
    total_ml = base_ml * multipliers.get(activity_level, 1.0)
    liters = total_ml / 1000
    cups = total_ml / 240  # 240ml per cup
    
    return {
        "liters": round(liters, 2),
        "cups": round(cups, 1),
        "message": f"You should drink approximately {round(liters, 1)}L ({round(cups)} cups) of water daily"
    }


def set_medication_reminder(medication_name, times_per_day, start_time="09:00"):
    """Create medication reminder schedule"""
    reminders = []
    hour, minute = map(int, start_time.split(':'))
    
    interval_hours = 24 / times_per_day
    
    for i in range(times_per_day):
        time_offset = timedelta(hours=interval_hours * i)
        reminder_time = (datetime.now().replace(hour=hour, minute=minute) + time_offset).strftime("%H:%M")
        reminders.append(reminder_time)
    
    return {
        "medication": medication_name,
        "times": reminders,
        "message": f"Reminders set for {medication_name} at: {', '.join(reminders)}"
    }


def search_symptoms(symptoms_list):
    """Search for possible conditions based on symptoms"""
    # This is a simple mock - in production, you'd use a medical API
    symptom_db = {
        "fever,headache,fatigue": ["Common Cold", "Flu", "COVID-19"],
        "cough,fever": ["Respiratory Infection", "Bronchitis"],
        "headache,nausea": ["Migraine", "Tension Headache"],
        "fever,body ache": ["Flu", "Viral Infection"],
    }
    
    symptoms_key = ",".join(sorted([s.lower().strip() for s in symptoms_list]))
    
    # Find closest match
    possible_conditions = []
    for key, conditions in symptom_db.items():
        if any(s in key for s in symptoms_key.split(',')):
            possible_conditions.extend(conditions)
    
    if not possible_conditions:
        possible_conditions = ["Unable to determine - Please consult a doctor"]
    
    return {
        "symptoms": symptoms_list,
        "possible_conditions": list(set(possible_conditions)),
        "message": "⚠️ These are possible conditions. Please consult a healthcare provider for proper diagnosis."
    }


# ============= FUNCTION DEFINITIONS FOR OPENAI =============

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "Calculate Body Mass Index given weight and height",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {
                        "type": "number",
                        "description": "Weight in kilograms"
                    },
                    "height_cm": {
                        "type": "number",
                        "description": "Height in centimeters"
                    }
                },
                "required": ["weight_kg", "height_cm"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_daily_water",
            "description": "Calculate recommended daily water intake based on weight and activity level",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {
                        "type": "number",
                        "description": "Weight in kilograms"
                    },
                    "activity_level": {
                        "type": "string",
                        "enum": ["sedentary", "moderate", "active"],
                        "description": "Activity level"
                    }
                },
                "required": ["weight_kg"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_medication_reminder",
            "description": "Set up medication reminder schedule",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication_name": {
                        "type": "string",
                        "description": "Name of the medication"
                    },
                    "times_per_day": {
                        "type": "integer",
                        "description": "How many times per day to take medication"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "First dose time in HH:MM format"
                    }
                },
                "required": ["medication_name", "times_per_day"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_symptoms",
            "description": "Search for possible medical conditions based on symptoms",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptoms_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of symptoms"
                    }
                },
                "required": ["symptoms_list"]
            }
        }
    }
]


# ============= ADVANCED HEALTH AGENT CLASS =============

class AdvancedHealthAgent:
    """Health Agent with Function Calling capabilities"""
    
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = """You are an advanced AI health assistant with access to specialized tools.

Your capabilities:
- Calculate BMI and health metrics
- Recommend water intake based on weight and activity
- Set up medication reminders
- Search for possible conditions based on symptoms
- Provide general health advice

When a user asks about BMI, water intake, medication reminders, or symptoms, 
USE YOUR TOOLS to provide accurate calculations and recommendations.

Always be empathetic and remind users you're not a replacement for professional medical care.
For serious symptoms or concerns, always advise consulting a healthcare provider."""

        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def execute_function(self, function_name, arguments):
        """Execute the called function"""
        functions_map = {
            "calculate_bmi": calculate_bmi,
            "calculate_daily_water": calculate_daily_water,
            "set_medication_reminder": set_medication_reminder,
            "search_symptoms": search_symptoms
        }
        
        if function_name in functions_map:
            return functions_map[function_name](**arguments)
        else:
            return {"error": f"Function {function_name} not found"}
    
    def chat(self, user_message):
        """Main chat with function calling support"""
        
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # First API call - agent decides if it needs tools
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history,
                tools=tools,
                tool_choice="auto"  # Let the model decide when to use tools
            )
            
            response_message = response.choices[0].message
            
            # Check if the agent wants to use a tool
            if response_message.tool_calls:
                # Add assistant's message with tool calls
                self.conversation_history.append(response_message)
                
                # Execute each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 Using tool: {function_name}")
                    print(f"   Arguments: {function_args}")
                    
                    # Execute the function
                    function_result = self.execute_function(function_name, function_args)
                    
                    # Add function result to conversation
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(function_result)
                    })
                
                # Second API call - get final response with function results
                second_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=self.conversation_history
                )
                
                final_message = second_response.choices[0].message.content
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })
                
                return final_message
            
            else:
                # No tool calls needed, just return the response
                assistant_message = response_message.content
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                return assistant_message
        
        except Exception as e:
            return f"❌ Error: {str(e)}"


# ============= MAIN PROGRAM =============

def print_welcome():
    print("\n" + "=" * 70)
    print("🏥 ADVANCED HEALTH AGENT - With AI Function Calling")
    print("=" * 70)
    print("\n✨ I can now:")
    print("  • Calculate your BMI")
    print("  • Recommend daily water intake")
    print("  • Set medication reminders")
    print("  • Search symptoms for possible conditions")
    print("  • Answer any health questions")
    print("\n💡 Try asking:")
    print("  'Calculate my BMI - I'm 70kg and 175cm'")
    print("  'How much water should I drink? I weigh 65kg and I'm moderately active'")
    print("  'Set a reminder for aspirin 3 times a day'")
    print("  'I have fever and headache, what could it be?'")
    print("\n⚠️  Remember: I'm not a doctor. Always consult healthcare professionals.")
    print("=" * 70 + "\n")


def main():
    print_welcome()
    
    agent = AdvancedHealthAgent()
    
    print("Agent: Hello! I'm your advanced AI health assistant with specialized tools.")
    print("       Ask me anything, and I'll use my tools when needed!\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nAgent: Take care and stay healthy! 👋\n")
            break
        
        if not user_input:
            continue
        
        print()  # Blank line before response
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()