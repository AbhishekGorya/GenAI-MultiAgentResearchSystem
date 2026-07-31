# 🤖 AI Research Assistant using LangChain Multi-Agent Architecture

A production-oriented **Multi-Agent AI Research Assistant** built using **LangChain**, **Mistral AI**, **Tavily Search API**, and **BeautifulSoup**. Instead of relying on a single LLM prompt, this project divides the research task into multiple specialized agents and chains that work together to search the web, extract detailed information, generate a structured research report, and critique the final output.

---

# 📌 Project Overview

Large Language Models are powerful but have limitations:

- Knowledge cutoff
- Hallucinations
- Limited access to current information

This project addresses these limitations by giving the LLM access to external tools and dividing responsibilities among specialized AI components.

The workflow consists of:

1. Searching the web
2. Reading relevant webpages
3. Writing a professional report
4. Critiquing the generated report

This modular architecture closely resembles how modern AI agents are built for production applications.

---

# ✨ Features

- Autonomous Search Agent
- Autonomous Reader Agent
- Tavily-powered Web Search
- Web Scraping using BeautifulSoup
- Professional Research Report Generation
- AI-based Report Critique
- Modular LangChain Architecture
- Reusable Tools
- LCEL Chains
- Environment Variable Support
- Easy to Extend

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Framework | LangChain |
| LLM | Mistral Small 2506 |
| Search API | Tavily |
| Web Scraping | BeautifulSoup4 |
| HTTP Client | Requests |
| Environment Variables | python-dotenv |

---

# 📂 Project Structure

```text
AI_Research_Assistant/
│
├── agents.py              # Search Agent, Reader Agent, Writer Chain & Critic Chain
├── tools.py               # Custom LangChain Tools
├── main.py                # Complete Research Pipeline
├── .env                   # API Keys
├── requirements.txt
├── README.md
└── assets/
```

---

# 🧠 System Architecture

```text
                    User Topic
                         │
                         ▼
                Research Pipeline
                         │
                         ▼
                  Search Agent
                         │
                         ▼
                 Web Search Tool
                         │
                         ▼
                  Tavily Search API
                         │
                         ▼
                  Search Results
                         │
                         ▼
                  Reader Agent
                         │
                         ▼
                 Web Scraping Tool
                         │
                         ▼
                  BeautifulSoup
                         │
                         ▼
                Detailed Web Content
                         │
                         ▼
                  Writer Chain
                         │
                         ▼
              Structured Research Report
                         │
                         ▼
                  Critic Chain
                         │
                         ▼
                Report Evaluation
```

---

# ⚙️ Workflow

## Step 1 — Search Agent

The Search Agent receives the research topic and automatically decides to use the **Web Search Tool**.

Responsibilities:

- Search the internet
- Retrieve reliable sources
- Return titles, URLs, and snippets

---

## Step 2 — Reader Agent

The Reader Agent receives the search results.

Responsibilities:

- Select the most relevant webpage
- Scrape webpage content
- Clean HTML using BeautifulSoup
- Return readable text

---

## Step 3 — Writer Chain

The Writer Chain combines:

- Search Results
- Scraped Content

and generates a report containing:

- Introduction
- Key Findings
- Conclusion
- Sources

---

## Step 4 — Critic Chain

The Critic reviews the report and provides:

- Overall Score
- Strengths
- Areas to Improve
- Final Verdict

---

# 🔧 Project Components

## 1. Tools

### Web Search Tool

Uses Tavily Search API to retrieve current information.

Input

```text
Research Topic
```

Output

```text
Title
URL
Snippet
```

---

### Web Scraper Tool

Uses:

- Requests
- BeautifulSoup

to extract readable webpage content.

Workflow

```text
URL
 │
 ▼
requests.get()
 │
 ▼
BeautifulSoup
 │
 ▼
Remove:
• Script
• Style
• Footer
• Navigation
 │
 ▼
Clean Text
```

---

## 2. Agents

### Search Agent

Responsible for searching the web.

Available Tool:

- web_search()

---

### Reader Agent

Responsible for reading webpages.

Available Tool:

- scrape_url()

---

## 3. Chains

### Writer Chain

Transforms research into a structured report.

LCEL Pipeline

```text
Prompt
   │
   ▼
LLM
   │
   ▼
Output Parser
```

---

### Critic Chain

Evaluates the generated report.

Output Format

```text
Score

Strengths

Weaknesses

Verdict
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/AbhishekGorya/AI_Research_Assistant.git

cd AI_Research_Assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key

TAVILY_API_KEY=your_api_key
```

---

# ▶️ Running the Project

```bash
python main.py
```

Example

```text
Enter a research topic:

Artificial Intelligence in Healthcare
```

---

# 📋 Example Output

```text
===================================

Step 1
Searching the Web...

===================================

Step 2
Reading Webpages...

===================================

Step 3
Generating Report...

===================================

Step 4
Reviewing Report...
```

---

# 🏗 LangChain Concepts Used

## Agents

Autonomous AI components capable of deciding when to call tools.

Examples

- Search Agent
- Reader Agent

---

## Tools

Python functions exposed to agents.

Examples

```python
web_search()

scrape_url()
```

---

## Prompt Templates

Reusable prompts with placeholders.

```python
{topic}

{research}

{report}
```

---

## Chains

Fixed execution pipelines.

```text
Prompt

↓

LLM

↓

Output Parser
```

---

## LCEL

The project uses the LangChain Expression Language.

```python
prompt | llm | StrOutputParser()
```

---

# 📚 Learning Outcomes

By completing this project, you will understand:

- LangChain Agents
- Custom Tools
- Tool Calling
- Autonomous Agents
- Prompt Engineering
- LCEL
- BeautifulSoup
- Tavily Search API
- Multi-Agent Systems
- AI Workflow Orchestration

---

# 🔮 Future Improvements

- LangGraph Implementation
- Multi-Agent Collaboration
- Memory Support
- Parallel Tool Execution
- Async Processing
- PDF Report Generation
- Streamlit Interface
- Vector Database Integration
- Citation Generation
- Multi-Source Summarization
- RAG Integration
- Human-in-the-Loop Approval
- Agent Observability

---

# 🎯 Learning Flow

```text
User
 │
 ▼
Search Agent
 │
 ▼
Web Search
 │
 ▼
Search Results
 │
 ▼
Reader Agent
 │
 ▼
Scraper
 │
 ▼
Detailed Content
 │
 ▼
Writer Chain
 │
 ▼
Research Report
 │
 ▼
Critic Chain
 │
 ▼
Evaluation
```

---

# 💡 Why This Project?

This project demonstrates several important concepts used in modern AI applications:

- Tool Calling
- Multi-Agent Systems
- Workflow Orchestration
- Prompt Engineering
- Web Search Integration
- Web Scraping
- Structured Report Generation
- AI-based Self Evaluation

It serves as an excellent foundation for learning production-ready AI agent architectures and can be extended with LangGraph, RAG, vector databases, and deployment frameworks.

---

# 👨‍💻 Author

**Abhishek Gorya**

- GitHub: https://github.com/AbhishekGorya
- LinkedIn: https://www.linkedin.com/in/abhishekgorya

---

## ⭐ If you found this project helpful, consider giving it a star and following the repository for upcoming AI, GenAI, LangChain, and LangGraph projects.
