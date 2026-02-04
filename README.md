# AI Agents Playground

A minimal, end-to-end demonstration of modern agent architectures:
**Single → ReAct → RAG → Multi-Agent**, using real data and swappable LLM backends.

This repository is designed as a **clear learning and demo reference**, not a framework.

---

## Demo:

- **Single Agent** – direct LLM question answering
- **ReAct Agent** – reasoning + tool usage loop
- **RAG Agent** – retrieval-augmented generation over a real corpus
- **Multi-Agent** – orchestration of reasoning + retrieval

All modes share:
- a common CLI
- a unified LLM backend abstraction
- deterministic, inspectable execution paths

---

## Example Data Repository: arXiv

The RAG pipeline indexes the public **arXiv metadata snapshot** (~5M papers):

- Titles
- Authors
- Categories
- Abstracts

Embeddings:
- `sentence-transformers/all-MiniLM-L6-v2`

Vector store:
- **FAISS** (locally persisted)

The index is built **once** and reused across runs.

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Usage

All demos are run via a single entrypoint:

```bash
python run.py --mode <single|react|rag|multi> --query "<your question>"
```

## Examples

Single agent (OpenAI):

```bash 
python run.py --mode single --query "What is diphoton production at the LHC?"
```


## ReAct agent (local LLM via Ollama):

```bash
python run.py --mode react --llm local --query "Show research on dialogue safety"
```

## RAG over arXiv (first run builds index):

```bash
python run.py --mode rag --query "Diphoton production at the LHC"
```

## Multi-agent orchestration:

```bash
python run.py --mode multi --query "Summarise recent diphoton research"
```

## LLM Backends

The system supports pluggable LLM backends:

- openai (default)
0 local (via Ollama)

Select at runtime:

```bash
--llm openai
--llm local
```