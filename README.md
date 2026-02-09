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

## Agent Modes

### 1️⃣ Single Agent

Direct question → LLM answer.

```bash
python run.py --mode single --query "What is OpenStack?"
```

Used only as a baseline.

---

### 2️⃣ ReAct Agent (Core of the Project)

A reasoning loop that:
- thinks
- retrieves evidence
- observes
- reasons again

```bash
python run.py --mode react --domain runtime \
  --query "Why is OpenStack unstable?"
```

This is where most of the interesting work happens.

---

### 3️⃣ RAG Agent

Classic retrieval-augmented generation over a document corpus (e.g. arXiv).

```bash
python run.py --mode rag --domain knowledge \
  --query "Why do distributed systems fail?"
```

Used to explain *why* a pattern is known — never to invent runtime facts.

---

### 4️⃣ Multi-Agent (Optional)

Combines runtime + knowledge agents.

Runtime answers *what is happening*.
Knowledge explains *why this pattern is known*.

---

## Runtime Diagnostic Mode (The Interesting Part)

### Baseline vs Abnormal Comparison

```bash
python run.py --mode react --domain runtime \
  --compare normal abnormal \
  --query "Why is OpenStack unstable?"
```

This forces the agent to:

- retrieve **normal** OpenStack behavior
- retrieve **abnormal** OpenStack behavior
- reason only over differences

Environmental facts shared by both baselines are **not allowed** as causes.

---

### Adding Live Incident Logs

```bash
python run.py --mode react --domain runtime \
  --compare normal abnormal \
  --current-logs data/incidents/current.log \
  --query "What is wrong with my cloud-init?"
```

Key design rule:

> Current logs are **ephemeral context**, not indexed knowledge.

They are injected once, reasoned over, and discarded.

---

## Evidence Hygiene (Why This Is Different)

This project enforces several non-negotiable rules:

### ✅ Evidence-Bounded Answers
If the logs don’t show it, the agent won’t invent it.

### ✅ Absence Is a Signal
If a subsystem *should* emit logs but doesn’t, the agent can conclude:

> “This likely never ran.”

### ✅ Causal Isolation
In comparison mode:

> Only differences between normal and abnormal baselines may be causal.

Old hardware, low RAM, or kernel quirks shared by both baselines are suppressed.

### ✅ Explicit Evidence Gaps
When evidence is missing, the agent says so and lists what would be needed next.

This is the opposite of hallucination.

---

## LLM Backends (User-Friendly by Design)

The CLI exposes **capability tiers**, not model internals:

```bash
python run.py --llm tiny     # very fast smoke tests
python run.py --llm mistral  # log summarisation
python run.py --llm llama3   # decent local reasoning
python run.py --llm phi3     # strong local diagnostics
python run.py --llm openai   # strongest reasoning
```

Under the hood (via Ollama):

| CLI flag | Actual model |
|--------|--------------|
| tiny | phi3:mini |
| mistral | mistral |
| llama3 | llama3:8b |
| phi3 | phi3:medium |

Missing local models are **downloaded automatically** by Ollama.

---

## Why Multiple Models Matter

Small local models are great for:
- speed
- summaries
- iteration

They are **not** good at:
- causal reasoning
- absence-of-evidence inference
- epistemic constraints

This project is designed to **expose those limits**, not hide them.

You can route serious diagnostic questions to stronger models without changing agent logic.

---

## Reproducibility & Determinism

- No hidden state
- No silent retries
- No background learning
- Every decision is inspectable

If the agent gives a bad answer, you can trace *why*.

---

## License

MIT