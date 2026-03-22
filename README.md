# BER Mecha Agent v1 — Multi-channel AI Automation System

## 🚀 Overview
This is my first multi-channel AI automation agent.

The project was not only built as a portfolio for job applications, but also as a personal tool to improve my own workflow — managing information, processing emails, and supporting daily decisions.

During the process, I gradually integrated multiple tools such as Gmail, Notion, and WhatsApp, turning it into a working system rather than a single script.

This is not a one-time project, but an evolving system that I will continue to iterate and improve over time.


## 🧠 What it does

- Fetch unread emails from Gmail
- Filter out already processed emails using labels
- Structure email data for further AI processing
- Apply automated labeling logic
- Store results into Notion for tracking and logging
- Enable interaction and control via WhatsApp
- Connect multiple tools into a unified automation workflow


## ⚙️ System Architecture

ChatGPT (decision-making / brain)  
→ Python (logic layer)  
→ OpenClaw / workflow system (execution layer)

Connected channels:

- Gmail (data input)
- Notion (data storage & logging)
- WhatsApp (interaction & control)

This forms a basic AI agent loop:

Input → Process → Decide → Execute → Store


## 📂 Key Components

- `gmail_assistant.py`  
  Handles Gmail authentication, email fetching, filtering, and labeling logic

- OpenClaw workflow  
  Manages multi-step automation and tool orchestration

- Notion integration  
  Used for logging and structured data storage


## 💡 Why I built this

I am transitioning from a business / e-commerce background into AI and automation.

Instead of only learning theory, I chose to build real systems to:

- Understand how AI connects with real-world tools
- Improve execution and system-building ability
- Create practical, demonstrable experience


## 🛠 Tech Stack

- Python
- Gmail API
- Notion API
- LLM (ChatGPT)
- JSON / API integration
- Automation workflow design


## ⚠️ Notes

Sensitive files such as credentials and tokens are excluded for security reasons.


## 📈 Next Steps

- Move to cloud deployment for better stability
- Replace local logic with API-based architecture
- Improve LLM-based classification
- Expand to more channels (e.g., Slack, Webhooks)
- Build a more robust agent system


## 👤 Author

Jiayue Li （Seline） 
