# GEMINI.md

This file provides guidance to GEMINI when working with code in this repository.

## Project Overview

This is an educational repository for "Ingeniería de Soluciones con Inteligencia Artificial" (AI Solutions Engineering) course. The project follows a comprehensive three-phase learning structure covering generative AI fundamentals, intelligent agents development, and production deployment considerations.

## Architecture & Structure

### Learning Experiences (RA)
- **RA1 - Fundamentals of Generative AI and Prompt Engineering**
  - IL1.1: Introduction to LLMs and API connections
  - IL1.2: Prompt engineering techniques (zero-shot, few-shot, chain-of-thought)
  - IL1.3: RAG (Retrieval-Augmented Generation) infrastructure design
  - IL1.4: Evaluation and optimization of LLMs
  
- **RA2 - Development of Intelligent Agents with LLM**
  - IL2.1: Agent architecture and frameworks (LangChain, CrewAI)
  - IL2.2: Memory systems and external tool integration (Model Context Protocol)
  - IL2.3: Planning and orchestration strategies
  - IL2.4: Technical documentation and architecture design
  
- **RA3 - Observability, Security and Ethics in AI Agents**
  - IL3.1: Observability tools and performance metrics
  - IL3.2: Traceability analysis and log processing
  - IL3.3: Security protocols and ethical considerations
  - IL3.4: Scalability and sustainability strategies

### Assessment Structure
- **Formative Evaluations**: Quizzes (8 questions each) on theoretical concepts
- **Partial Evaluations**: Practical projects with presentations/deliverables
- **Final Transversal Evaluation**: Comprehensive project (40% weighting) covering all learning outcomes

### Code Organization
- Each RA contains introductory materials and specific learning modules (IL)
- Jupyter notebooks (.ipynb) contain practical implementations
- Markdown files (.md) provide conceptual guidance and requirements
- Projects are developed in pairs with individual presentations

## Development Environment

### LLM Provider: Groq
The course uses **Groq** (https://console.groq.com/) as its only LLM provider. GitHub Models
was dropped when its free tier ended — there must be **no** references to `GITHUB_TOKEN`,
`GITHUB_BASE_URL`, `OPENAI_BASE_URL`, `models.inference.ai.azure.com` or `gpt-4o` anywhere in the repo.

### Required Environment Variables
- `GROQ_API_KEY`: Groq API key (starts with `gsk_`), from console.groq.com > API Keys
- `GROQ_MODEL`: default chat model — `llama-3.3-70b-versatile`
- `GROQ_MODEL_FAST`: cheap/fast model for high-volume loops — `llama-3.1-8b-instant`
- `EMBEDDING_MODEL`: local embeddings — `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `LANGSMITH_TRACING` / `LANGSMITH_API_KEY` / `LANGSMITH_PROJECT`: observability (RA3)

### Key Dependencies
Based on notebook imports and course materials:
- `langchain-groq` (`ChatGroq`): the default way to call an LLM in this repo
- `groq`: official SDK, used only where a notebook teaches the raw API
- `langchain-huggingface` + `sentence-transformers`: local embeddings for RAG
- Agent frameworks: LangChain, CrewAI (LiteLLM — model ids need the `groq/` prefix)
- Observability tools: LangSmith, Langfuse, Arize for monitoring
- Standard Python libraries: `os`, `pandas`, `requests`

### Canonical Code Patterns
```python
# LangChain chat (default)
from langchain_groq import ChatGroq
llm = ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), temperature=0.2)

# Raw SDK (only where the notebook teaches the bare API)
from groq import Groq
cliente = Groq()  # reads GROQ_API_KEY from the environment

# Embeddings — Groq has NO embeddings endpoint, so these run locally
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"),
    encode_kwargs={"normalize_embeddings": True},
)

# CrewAI (LiteLLM needs the groq/ prefix)
from crewai import LLM
llm = LLM(model=f"groq/{os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}", temperature=0.2)
```

Notebooks load credentials in a way that works both in Google Colab (Secrets) and locally (`.env`);
keep that dual pattern when editing them. Free-tier limits (Aug 2026): both models 30 req/min;
`llama-3.3-70b-versatile` 12K tokens/min and **100K tokens/day**; `llama-3.1-8b-instant`
6K tokens/min and **500K tokens/day**. The daily token cap is what actually runs out — a few
hours of running agent notebooks exhausts the 70B. Avoid tight LLM call loops in notebooks,
and prefer `GROQ_MODEL_FAST` for anything high-volume.

### Tool calling on Groq is model-dependent — and the winner flips by code path
Both Llama models sometimes emit a malformed function call, which Groq rejects with HTTP 400
`tool_use_failed`. Measured on this repo's own tools:

| Code path | `llama-3.3-70b-versatile` | `llama-3.1-8b-instant` |
|---|---|---|
| Raw `groq` SDK, hand-written JSON schema, Spanish prompt | 7/10 | **10/10** |
| LangChain `create_openai_tools_agent` + `hwchase17/openai-tools-agent` (English prompt) | **6/6** | 4/6 |

So there is no single "best tool-calling model" here — it depends on the prompt and the path:
- **Raw SDK tool calling** → `GROQ_MODEL_FAST` (`llama-3.1-8b-instant`).
  Used by `RA2/IL2.1/2-agent-function-calling.ipynb`, `RA2/IL2.2/3-herramientas-externas.ipynb`.
- **LangChain tools agents** → `GROQ_MODEL` (`llama-3.3-70b-versatile`).
  Used by `RA2/IL2.1/3-langchain-agent.ipynb`, `RA2/IL2.2/1-memory-agent.ipynb`,
  `RA2/IL2.2/2-memory-agent-advanced.ipynb`.
- **Prompt-based ReAct** (`create_react_agent`) is unaffected; keeps `GROQ_MODEL`.

Don't "unify" these onto one model without re-measuring — each notebook's comment records why.
Streaming was ruled out as a factor (identical pass rates with `disable_streaming` on and off).

### Development Workflow
- Environment setup with Python and Jupyter Notebook
- API configuration with authentication keys
- Progressive implementation from basic API calls to complex agent systems
- Documentation requirements include README.md files for agent implementations

## Common Patterns

### API Integration
- All LLM calls go to Groq, configured through environment variables
- Supports both the direct `groq` SDK and LangChain's `ChatGroq` abstraction
- Temperature and token limits are commonly configured for different use cases

### Agent Development
- Function calling integration with external tools
- Memory systems implementation (short-term and long-term)
- Planning algorithms for multi-stage task execution
- Error handling and recovery mechanisms

### Educational Progression
- Conceptual introduction (markdown) → practical implementation (notebook)
- Individual skill building → collaborative project development
- Progressive complexity from basic prompts to production-ready agents
- Strong emphasis on organizational/business context applications

### Project Deliverables
- Technical documentation with architecture diagrams
- Performance metrics and observability dashboards
- Security and ethical considerations documentation
- Scalability and deployment strategies