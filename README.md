# AI Agents Playground — Runtime & Infrastructure Reasoning

A **minimal, end‑to‑end demonstration of modern agent architectures** for **runtime and infrastructure diagnostics**, built around **real system logs**, **OpenStack control‑plane events**, and **swappable LLM backends**.

This repository is a **reference implementation** showing how agents can reason over operational evidence.

---

## Why

Most “AI troubleshooting” tools hallucinate answers when evidence is missing.

This project does the opposite:

- Enforces **evidence scope**
- Detects **evidence gaps**
- Separates **baseline vs incident behavior**
- Guides the **next diagnostic step**
- Refuses to guess

The result is an agent that behaves like a **senior infrastructure engineer**, not a chatbot.

---

## What this repo demonstrates

### Agent architectures
- **Single Agent** – plain LLM reasoning (no tools)
- **ReAct Agent** – reasoning + tool use
- **RAG Agent** – retrieval‑augmented reasoning
- **Multi‑Agent** – orchestration patterns

### Runtime reasoning (core focus)
- Linux boot and system logs
- OpenStack control‑plane and service logs
- Baseline vs abnormal comparison
- Subsystem‑aware diagnostics (API, compute, MQ, DB)
- Cross‑layer reasoning (host ↔ control plane)

### Knowledge reasoning (secondary)
- arXiv research corpus
- Isolated from runtime evidence
- Explicit domain selection

---

## Key design principles

### 1. Evidence‑first reasoning
Agents reason **only** from retrieved runtime evidence.
If data is missing, the agent says so.

### 2. Explicit scope & gaps
Every answer declares:
- what evidence was used
- what evidence is missing
- what would be needed next

### 3. No hallucination paths
If logs do not support a conclusion, no conclusion is drawn.

### 4. Runtime ≠ Knowledge
Operational logs and research papers are treated as **separate epistemic domains**.

---

## Repository structure

```
Agents/
├── core/                # Agent kernel, ReAct logic, tool routing
├── rag/                 # Retrieval layers (Linux, OpenStack, arXiv, comparison)
├── sources/             # Ingestion & normalization code (Linux / OpenStack)
│   ├── linux/
│   └── openstack/
├── data/                # Runtime artifacts & evidence (gitignored)
│   ├── arxiv_index/     # FAISS index for research knowledge
│   ├── linux_index/     # FAISS index for Linux runtime logs
│   └── sources/
│       ├── linux/       # Raw Linux logs
│       └── openstack/   # Raw OpenStack logs (normal / abnormal)
├── execution/           # LLM runtimes (local / OpenAI)
├── examples/            # Runnable agent demos (single / ReAct / RAG / multi)
├── orchestration/       # Multi-agent / graph experiments
├── tests/               # Kernel and routing tests
├── run.py               # Unified CLI entrypoint
└── README.md
```

---

## Running the system

### Runtime diagnostics (Linux / OpenStack)

```bash
python run.py   --mode react   --llm local   --domain runtime   --query "Why is the OpenStack service unstable?"
```

### Knowledge search (arXiv)

```bash
python run.py   --mode react   --llm local   --domain knowledge   --query "Research on dialogue system safety"
```

### Single agent (no tools)

```bash
python run.py   --mode single   --llm local   --query "Explain OpenStack at a high level"
```

---


## License

MIT