# AI Agents Playground

A minimal, end-to-end demonstration of modern **agent architectures**, progressing from simple LLM calls to multi-agent orchestration:

**Single → ReAct → RAG → Multi-Agent**

This repository is intentionally **not a framework**.  
It is a **clear, inspectable reference implementation** designed for learning, demos, and architectural discussion.

---

## What This Repo Demonstrates

This project shows how agent systems *evolve in capability* as you add structure:

| Mode   | Adds What? | Why It Exists |
|------|------------|---------------|
| Single | LLM call | Baseline behaviour |
| ReAct | Reasoning + tools | Controlled thinking & actions |
| RAG | External knowledge | Grounded answers |
| Multi | Coordination | Separation of concerns |

Each mode builds directly on the previous one.

---

## Agent Modes Explained

### 1. Single Agent – *Baseline LLM*

**What it is:**  
A direct prompt → response interaction with an LLM.

**What it demonstrates:**
- Pure model capability
- Prompt sensitivity
- No memory, no tools, no grounding

**Why it matters:**  
This is the control group. Every more complex agent should be compared against this.

```bash
python run.py --mode single --query "What is diphoton production at the LHC?"
```

### 2. ReAct Agent – Reasoning + Acting

**What it is:**
An agent that follows a Reason → Act → Observe loop:
- Uses an explicit **reasoning loop** instead of a single LLM call
- Alternates between **thinking**, **acting (tool use / retrieval)**, and **observing results**
- Makes intermediate decisions **visible and inspectable**
- Reduces hallucinations by grounding actions in observations
- Well-suited for **multi-step questions**, analysis, and controlled tool usage
- Serves as the **foundation for the multi-agent orchestration** mode


**Demo shows:**

- Explicit intermediate reasoning
- Tool selection based on thoughts
- Iterative problem solving

**Why it matters:**
ReAct shows how structure improves reliability without adding external data.

```bash
python run.py --mode react --llm local --query "Show research on dialogue safety"
```

### 3. RAG Agent – Grounded Knowledge

** What RAG:**
A Retrieval-Augmented Generation (RAG) pipeline over a real dataset.

** Demo shows:**

- Embedding-based semantic search
- Separation of retrieval and generation
- Answers grounded in source documents

** Why it matters:**
This is where agents stop hallucinating and start behaving like systems.

```bash
python run.py --mode rag --query "Diphoton production at the LHC"
```

On first run, the arXiv index is built and cached locally.
Subsequent runs reuse the FAISS index for speed.

### 4. Multi-Agent – Orchestration

** What it is:**
A composed agent that coordinates:
- retrieval
- reasoning
- synthesis

** Demo shows:**
- Clear separation of responsibilities
- Reuse of existing agents
- More robust, explainable outputs


** Why it matters:**
This mirrors how production agent systems are actually built.

```bash
python run.py --mode multi --query "Summarise recent diphoton research"
```

** Example Data: arXiv Corpus**
The RAG and Multi-Agent modes use the public arXiv metadata snapshot (~5M papers):
- Titles
- Authors
- Categories
- Abstracts

### Indexing Stack

Embeddings: sentence-transformers/all-MiniLM-L6-v2

Vector Store: FAISS (local, persisted)

Index Lifecycle: build once → reuse across runs

### LLM Backends

All agent modes use a shared LLM abstraction.

Select at runtime:

```bash
--llm openai
--llm local
```

This allows direct comparison between:

hosted vs local models

reasoning quality vs grounding

latency vs cost

```bash
Installation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

All demos share a single entrypoint:

```bash
python run.py --mode <single|react|rag|multi> [--llm local|openai] --query "<your question>"
```