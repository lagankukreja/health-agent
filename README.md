# 🏥 AI Health Agent

An intelligent health assistant powered by OpenAI's GPT-4 that can answer health questions, track symptoms, and provide wellness recommendations.

## ✨ Features

- 💬 Natural language health Q&A
- 📊 BMI calculation
- 💧 Water intake recommendations
- 💊 Medication reminders
- 🔍 Symptom analysis
- 🌐 Web interface with real-time chat
- 📚 RAG (Retrieval Augmented Generation) support

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lagankukreja/health-agent.git
cd health-agent
```

2. Install dependencies:
```bash
pip install openai python-dotenv flask scikit-learn numpy
```

3. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

### Running the Agent

#### Command Line Version
```bash
python health_agent.py
```

#### Advanced Version (with function calling)
```bash
python advanced_health_agent.py
```

#### Web Interface
```bash
python health_webapp_connected.py
```
Then open your browser to: http://localhost:8081

#### RAG Version (with knowledge base)
```bash
python rag_health_agent.py
```

## 📁 Project Structure

```
health-agent/
├── health_agent.py              # Basic command-line agent
├── advanced_health_agent.py     # Agent with function calling

├── health_webapp.py   # Flask web interface

├── templates/
│   ├── index.html              # Web UI
│   
├── .env                         # Environment variables (not in Git)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🎯 Usage Examples

### Basic Health Questions
```
You: What are some tips for better sleep?
Agent: For better sleep, maintain a consistent schedule...
```

### Function Calling (Advanced Version)
```
You: Calculate my BMI. I'm 70kg and 175cm tall.
Agent: Your BMI is 22.86 (Normal weight)...
```

### Symptom Tracking
```
You: log symptom: Headache and mild fever
Agent: ✓ Logged symptom: Headache and mild fever

You: show symptoms
Agent: [Shows all logged symptoms with timestamps]
```

## 🛠️ Technologies Used

- **OpenAI GPT-4**: AI model for natural language understanding
- **Flask**: Web framework for the interface
- **Python**: Backend programming language
- **scikit-learn**: For RAG embeddings and similarity search

## ⚠️ Important Notes

- This agent is NOT a replacement for professional medical advice
- Always consult healthcare providers for serious health concerns
- API usage will incur costs based on OpenAI pricing

## 🔐 Security

- Never commit your `.env` file or API keys
- The `.gitignore` file is configured to prevent this
- Store sensitive data securely

## 📝 License

MIT License - feel free to use and modify

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 👨‍💻 Author

Lagan Kukreja

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Flask framework
- The open-source community