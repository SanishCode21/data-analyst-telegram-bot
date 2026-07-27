# Data Analyst Telegram Bot

An AI-powered Telegram bot that answers **data-analysis questions** using an LLM and returns **exactly one JSON object** as required by the TDS Project 1 specification.

The bot supports:

- Natural language data-analysis questions
- CSV dataset analysis
- Public dataset URLs
- Multi-turn conversations
- JSONL execution logging
- Cloud deployment for 24×7 availability

---

## Live Demo

### Telegram Bot

https://t.me/tds_sanish_p1_bot

### Live Deployment

https://data-analyst-telegram-bot-4vgo.onrender.com

Health endpoint:

https://data-analyst-telegram-bot-4vgo.onrender.com/health

---

## Project Objective

Build a Telegram bot that:

- receives a plain text data-analysis question
- understands the required JSON output format
- performs the required computation
- returns **only one JSON object**
- provides a public JSONL execution log URL

Example reply:

```json
{
  "answer": {
    "state": "Assam"
  },
  "log_url": "https://your-domain.com/run.jsonl"
}
```

---

# Features

- AI-powered Data Analyst
- Exact JSON output
- Multi-turn conversation support
- Public dataset support
- CSV analysis using Pandas
- Automatic JSON validation
- JSONL logging
- Environment-variable based configuration
- Deployable on Render

---

# Project Structure

```
.
├── bot.py
├── telegram_handler.py
├── llm.py
├── config.py
├── logger.py
├── json_utils.py
├── memory.py
├── web_server.py
├── run.jsonl
├── requirements.txt
├── .env.example
│
├── tools
│   ├── csv_tool.py
│   ├── dataset_tool.py
│   ├── data_analyser.py
│   └── url_detector.py
│
└── README.md
```

---

# Architecture

```
Telegram User
        │
        ▼
 Telegram Bot
        │
        ▼
 telegram_handler.py
        │
        ├───────────────┐
        ▼               ▼
 Dataset Tools      Conversation Memory
        │               │
        └──────┬────────┘
               ▼
           GPT-5 Mini
               │
               ▼
      JSON Validation
               │
               ▼
      Telegram JSON Reply
```

---

# Technologies Used

- Python 3.12+
- python-telegram-bot
- OpenAI SDK
- GPT-5 Mini (AI Pipe)
- Pandas
- Requests
- Flask
- python-dotenv

---

# Environment Variables

Create a `.env` file.

```
BOT_TOKEN=xxxxxxxxxxxxxxxx

AI_TOKEN=xxxxxxxxxxxxxxxx

BASE_URL=https://aipipe.org/openai/v1

MODEL_NAME=gpt-5-mini

LOG_URL=https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/run.jsonl
```

---

# Installation

Clone repository

```bash
git clone https://github.com/SanishCode21/data-analyst-telegram-bot.git

cd YOUR_REPO
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run locally

```bash
python bot.py
```

---

# Testing

The project was tested using the official grading pipeline.

Generate test cases

```bash
python generate.py --students students.csv
```

Collect bot responses

```bash
python collect.py --students students.csv
```

Grade responses

```bash
python grade.py --students students.csv
```

Example successful result

```
1/1 correct
```

---

# Supported Question Types

## Arithmetic

```
What is 25% of 400?

Reply ONLY with

{"answer":0,"log_url":"..."}
```

---

## CSV Dataset

```
Use this dataset:

https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv

How many rows?

Reply ONLY with

{"rows":0,"log_url":"..."}
```

---

## Public Dataset URLs

The bot can download and inspect public CSV datasets before answering.

---

## Multi-turn Conversations

The bot stores recent conversation history so it can answer the **last user message** while using earlier messages as context.

---

# Logging

Every interaction is recorded as JSONL.

Example

```json
{"type":"incoming","text":"What is 25% of 400?"}
{"type":"outgoing","text":"{\"answer\":100}"}
```

Public log URL

```
https://raw.githubusercontent.com/SanishCode21/data-analyst-telegram-bot/main/run.jsonl
```

---

# Deployment

The bot is deployed on Render.

Since free Background Workers are unavailable, a lightweight Flask health server is included to keep the Web Service active.

Health endpoint

```
/health
```

---

# JSON Response Rules

The bot always returns

- exactly one JSON object
- no markdown
- no explanations
- no code fences
- valid JSON only

---

# Repository

- GitHub: https://github.com/SanishCode21/data-analyst-telegram-bot

---

# Future Improvements

- Support Excel files
- Support SQL datasets
- Visualization generation
- Automatic statistical summaries
- Improved tool routing
- Support additional public datasets

---

# Author

**Sanish Kumar Singh**

BS in Data Science  
Indian Institute of Technology Madras

- GitHub: https://github.com/SanishCode21

- LinkedIn: https://www.linkedin.com/in/sanish-kumar-singh-163679289

---

# Acknowledgements

- IIT Madras TDS Course
- OpenAI
- Python Telegram Bot
- Pandas
- Numpy
- Render
