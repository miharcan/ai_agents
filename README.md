# AI Agents Playground

A minimal, end-to-end demonstration of **agent architectures for real system reasoning**, progressing from:

**Single → ReAct → RAG → Multi-Agent**

with **explicit epistemic control** and **real infrastructure data**.

This repository is designed as a **clear learning and experimentation reference**, not a framework.

---

## Core Focus: Runtime & Infrastructure Debugging

The primary focus of this project is **infrastructure-grade reasoning over runtime evidence**, such as:

- Linux system logs
- OpenStack service logs
- (extensible to metrics, traces, and events)

The goal is to explore how modern agent architectures can:

- reason over **what actually happened**, not assumptions
- remain grounded in **observed system behavior**
- avoid hallucination by **controlling evidence domains explicitly**
- scale from simple summarisation to multi-step diagnostic reasoning

This makes the repository especially relevant for:
- infrastructure debugging
- SRE / platform engineering workflows
- operational AI agents
- incident analysis and post-mortems

---

## Epistemic Domains (Key Design Idea)

A central design principle in this repo is **explicit epistemic separation**.

Agents do not implicitly decide *what kind of truth* they are allowed to use — this is controlled at runtime.

### Runtime Domain (Primary)

The **runtime** domain is the default and primary focus.

It represents **ground-truth operational evidence**, such as:

- Linux boot logs
- OpenStack control-plane logs
- service startup sequences
- error, retry, and timeout behavior

When operating in this domain, agents are expected to:
- reason strictly from retrieved evidence
- summarise, correlate, and interpret observed signals
- avoid theoretical explanations unless explicitly enabled

### Knowledge Domain (Secondary, Optional)

The **knowledge** domain (e.g. arXiv) is intentionally isolated.

It represents **theoretical and contextual knowledge**, such as:
- academic research
- known design patterns
- prior studies and explanations

This domain is useful for:
- understanding *why* a class of problems exists
- contextualising observed failures
- research and learning use-cases

It is **not** used by default for infrastructure debugging.

---

## Agent Modes

All agent modes share:
- a unified CLI
- a common agent kernel
- swappable LLM backends (local or OpenAI)
- deterministic, inspectable execution paths

### Single Agent
Direct LLM question answering with no tools.
Useful as a baseline.

### ReAct Agent
Reasoning-and-acting loop with explicit tool usage.
This is the **core mode for infrastructure debugging**.

### RAG Agent
Retrieval-augmented reasoning over domain-specific corpora:
- runtime logs (Linux / OpenStack)
- knowledge corpora (arXiv)

### Multi-Agent
Orchestration of multiple reasoning components.
Designed for future expansion into coordinated diagnostic agents.

---

## Runtime Evidence Pipeline

For infrastructure domains, data flows through a clear pipeline:

```
Raw logs
 → light normalization
 → coarse segmentation
 → structured narration (signal extraction)
 → retrieval
 → agent reasoning
```

Narration **highlights signals** (e.g. legacy behavior, retries, disabled features)
without hard-coding diagnoses or rules.

Agents remain responsible for interpretation.

---

## Example Usage

### Infrastructure / Runtime Debugging

```bash
python run.py \
  --mode react \
  --llm local \
  --domain runtime \
  --query "Are there any issues or anomalies in this Linux boot?"
```

### Research / Knowledge Exploration

```bash
python run.py \
  --mode react \
  --llm local \
  --domain knowledge \
  --query "Show research on dialogue system safety"
```

---

## Why arXiv Is Included

arXiv is included **deliberately but safely**.

It serves as:
- a contrasting domain to runtime evidence
- a demonstration that the same agent architecture can reason over
  very different kinds of truth
- a foundation for future “runtime + theory” explanations (opt-in only)

arXiv is **never mixed implicitly** with infrastructure logs.

---

## What This Repository Is (and Isn’t)

**This repo is:**
- a learning and experimentation playground
- a reference for clean agent architecture
- focused on reasoning quality, not benchmarks
- intentionally minimal and readable

**This repo is not:**
- a production framework
- an automated remediation system
- a rules-based expert system

---

## Status & Direction

Current strengths:
- clean agent abstractions
- explicit domain control
- grounded runtime reasoning
- extensible evidence pipelines

Planned / natural extensions:
- OpenStack + Linux cross-layer diagnostics
- baseline vs incident comparison
- severity-aware narration
- metrics and trace integration