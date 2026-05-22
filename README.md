# GPT-Answer-Evaluation-Module
<div align="center">

# 🧠 GPT Answer Evaluation API

**An AI-powered answer evaluation engine built with FastAPI and OpenAI GPT.**  
Submit a question and a candidate's answer — get back structured scores and feedback instantly.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?style=for-the-badge&logo=openai&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-60%20Passed-2ecc71?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

## 📌 What is this?

This project is a **REST API** that acts as an intelligent evaluator — like an AI interviewer or teacher. You send it a question and a candidate's answer, and it uses GPT to analyze the response across three dimensions and return structured feedback.

**Example:**

```json
// Request
{
  "question": "Explain FastAPI",
  "answer": "FastAPI is a Python framework used for APIs."
}

// Response
{
  "correctness": 8,
  "depth": 6,
  "clarity": 7,
  "feedback": "Good basic explanation, but missing async support and automatic API documentation."
}
```

---

## ✨ Features

- 🤖 **GPT-powered evaluation** — uses OpenAI to analyze answers intelligently
- 📊 **3 scoring dimensions** — correctness, depth, clarity (each scored 0–10)
- 🛡️ **Robust input validation** — catches empty, null, and too-short inputs via Pydantic v2
- 🔁 **3-layer response parser** — handles clean JSON, markdown-wrapped JSON, and malformed GPT output with graceful fallback
- ⚡ **Production-ready error handling** — rate limits, auth failures, API errors all handled cleanly
- 🧪 **60 passing tests** — full unit + integration test suite with mocked OpenAI
- 📄 **Auto-generated API docs** — Swagger UI available at `/docs`

---

## 🗂️ Project Structure

```
gpt_answer_evaluator/
│
├── app/
│   ├── api/
│   │   └── routes.py              # POST /evaluate, GET /health endpoints
│   │
│   ├── services/
│   │   ├── evaluator.py           # Main pipeline: prompt → GPT → parse → return
│   │   ├── prompt_builder.py      # Builds deterministic GPT prompt messages
│   │   └── response_parser.py     # 3-layer JSON parser with fallback
│   │
│   ├── models/
│   │   ├── request_models.py      # Pydantic schemas for input/output
│   │   └── response_models.py     # Re-exports for clean imports
│   │
│   ├── core/
│   │   ├── config.py              # Settings loaded from .env
│   │   └── constants.py           # System prompt, user template, fallback dict
│   │
│   ├── utils/
│   │   ├── validators.py          # Length/content helpers
│   │   └── helpers.py             # Logging setup, text utilities
│   │
│   └── main.py                    # FastAPI app factory + exception handlers
│
├── tests/
│   ├── test_api.py                # Integration tests (mocked OpenAI)
│   ├── test_evaluator.py          # Unit tests: prompt builder, parser, validators
│   └── test_parser.py             # Deep unit tests for response parser
│
├── .env.example                   # Environment variable template
├── requirements.txt
├── pytest.ini
├── run.py                         # Uvicorn server entrypoint
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

### ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/gpt-answer-evaluator.git
cd gpt-answer-evaluator
```

**2. Create and activate a virtual environment**

```bash
# Mac / Linux
python -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

```bash
cp .env.example .env
```

Open `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-proj-your-key-here
GPT_MODEL=gpt-3.5-turbo
```

**5. Run the server**

```bash
python run.py
```

The API is now live at:

```
http://localhost:8000
```

Swagger docs (interactive UI):

```
http://localhost:8000/docs
```

---

## 🔌 API Reference

### `POST /api/v1/evaluate`

Evaluate a candidate's answer to a question.

**Request Body**

| Field      | Type   | Required | Description                        |
|------------|--------|----------|------------------------------------|
| `question` | string | ✅        | The question being answered        |
| `answer`   | string | ✅        | The candidate's answer to evaluate |

**Example Request**

```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is a REST API?",
    "answer": "REST is an architectural style for building web services using HTTP."
  }'
```

**Example Response**

```json
{
  "correctness": 8,
  "depth": 5,
  "clarity": 9,
  "feedback": "Accurate and clear answer. Consider mentioning statelessness, resource-based URLs, and standard HTTP methods to improve depth."
}
```

**Scoring Guide**

| Field         | Range | Meaning                                          |
|---------------|-------|--------------------------------------------------|
| `correctness` | 0–10  | How factually accurate and relevant the answer is |
| `depth`       | 0–10  | How thoroughly the topic is covered              |
| `clarity`     | 0–10  | How well-structured and readable the answer is   |

**Error Responses**

| Status | When it happens                         |
|--------|-----------------------------------------|
| `422`  | Empty, null, or too-short input fields  |
| `502`  | GPT API returned an unexpected error    |
| `503`  | OpenAI rate limit exceeded              |
| `500`  | Unexpected internal server error        |

---

### `GET /api/v1/health`

Check if the API is running.

```bash
curl http://localhost:8000/api/v1/health
```

```json
{ "status": "ok", "service": "GPT Answer Evaluator" }
```

---

## 🧪 Running Tests

Tests use mocked OpenAI responses — **no API key or internet required**.

```bash
pytest tests/ -v
```

Expected output:

```
60 passed in 0.78s
```

**What's tested:**

| Test File           | Coverage                                              |
|---------------------|-------------------------------------------------------|
| `test_api.py`       | Valid requests, validation errors, edge cases, health |
| `test_evaluator.py` | Prompt builder, response parser, input validators     |
| `test_parser.py`    | JSON clamping, codeblock extraction, regex fallback   |

---

## ⚙️ Configuration

All configuration is via the `.env` file:

| Variable            | Default         | Description                                      |
|---------------------|-----------------|--------------------------------------------------|
| `OPENAI_API_KEY`    | *(required)*    | Your OpenAI secret key                           |
| `GPT_MODEL`         | `gpt-3.5-turbo` | OpenAI model to use (`gpt-4` also works)         |
| `MAX_TOKENS`        | `500`           | Max tokens allowed in GPT's response             |
| `MAX_ANSWER_LENGTH` | `5000`          | Characters before answer is truncated            |
| `MIN_ANSWER_LENGTH` | `3`             | Minimum characters for a valid answer            |

---

## 🛠️ Edge Cases Handled

| Scenario                  | Behavior                                       |
|---------------------------|------------------------------------------------|
| Empty question or answer  | `422` validation error before hitting GPT      |
| Whitespace-only input     | Stripped and rejected with `422`               |
| Answer too long (>5000ch) | Truncated with `[truncated]` marker            |
| GPT returns plain text    | 3-layer parser extracts JSON or returns fallback |
| GPT wraps JSON in markdown | Codeblock extractor handles it                |
| Missing keys in GPT output | Fallback response returned, no crash          |
| Rate limit hit            | `503` with clear error message                 |
| Wrong API key             | `502` with "Invalid API key" message           |

---

## 🧠 Design Decisions

**`temperature = 0`**
Deterministic outputs — identical inputs produce identical scores every time. Essential for fair, consistent evaluation.

**3-layer response parser**
GPT doesn't always return clean JSON. The parser tries: direct parse → extract from ` ```json ``` ` block → regex scan for `{...}` → graceful fallback dict. The API never returns a 500 due to a bad GPT response.

**Pydantic v2 validators**
Input is stripped and validated before any GPT call is made — saves tokens, prevents wasted API calls, and returns clear error messages.

**Lazy OpenAI client**
The client is created once on first use via `_get_client()`, making it easy to mock in tests without needing real credentials.

---

## 📦 Tech Stack

| Technology     | Purpose                          |
|----------------|----------------------------------|
| FastAPI        | REST API framework               |
| Pydantic v2    | Request/response validation      |
| OpenAI Python  | GPT API integration              |
| Uvicorn        | ASGI server                      |
| python-dotenv  | Environment variable management  |
| Pytest         | Testing framework                |
| HTTPX          | Async HTTP client for tests      |

---

## 🪟 Windows Users

If you're on Windows and running into issues, here's the only extra step you may need.

If activating the virtual environment gives a permissions error, run this once in PowerShell as Administrator:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate normally:

```cmd
venv\Scripts\activate
```

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it.

---

## 🙋 Author

Built as part of an internship assignment demonstrating production-grade API development with FastAPI and OpenAI integration.

---

<div align="center">
  <sub>If this helped you, consider giving it a ⭐ on GitHub</sub>
</div>
