# Autonomous Local Agent + Cloud LLMs: Project Bootstrap Plan

This document is the starting blueprint for building your local autonomous agent that can:
- run on this machine,
- use cloud LLMs for reasoning,
- create software/apps,
- self-improve within controlled boundaries,
- and execute a real-time trading workflow.

---

## 1) Product vision and constraints

### Vision
A local "operator" that can plan, code, test, run tools, and execute approved workflows end-to-end.

### Non-negotiable constraints
1. **Human-governed autonomy** for risky actions (fund movement, production deploys, shell access beyond allowlist).
2. **Deterministic audit log** of every observation, thought summary, tool call, and action result.
3. **Policy layer first** before any autonomous execution loop.
4. **Trading risk controls in hard code** (position sizing, max daily loss, market shutdown rules).

---

## 2) High-level architecture

Use a modular architecture so each capability is independently testable.

1. **Orchestrator (local)**
   - Manages goals, loops, memory, and tool routing.
   - Handles retries, timeouts, and budget limits.

2. **LLM Gateway (cloud)**
   - Provider adapters (OpenAI/Anthropic/etc.) behind one internal interface.
   - Model routing by task type (planner vs coder vs critic).

3. **Tool Runtime (local sandbox)**
   - File editor, terminal executor, browser automation, test runner.
   - Strict allow/deny policies.

4. **Memory System**
   - Short-term run memory.
   - Long-term vector + structured memory (projects, incidents, lessons).

5. **Policy & Safety Engine**
   - Action authorization checks.
   - Trading guardrails.
   - Kill switch and circuit breakers.

6. **Trading Execution Module**
   - Data ingestion, strategy evaluator, order manager, reconciliation.
   - Runs independently from coding agent but shares policy engine.

7. **Observability Layer**
   - Event log, run replay, metrics, alerting.

---

## 3) Recommended implementation stack

- **Language**: Python for fastest iteration.
- **API**: FastAPI for local service endpoints.
- **Task queue**: Celery/RQ (or lightweight async workers at first).
- **Storage**:
  - PostgreSQL for structured state.
  - Redis for queues/cache.
  - Optional vector DB (pgvector first to reduce complexity).
- **Execution isolation**: subprocess + jailed working dirs, then containerized tool workers.
- **UI** (optional early): lightweight React or terminal dashboard.

---

## 4) Build order (milestones)

### Milestone 0 — Foundation (Week 1)
- Repo structure, config system, secrets handling.
- Unified logger + run trace IDs.
- LLM gateway with one provider.
- Single-agent loop (Plan → Act → Observe → Reflect).

### Milestone 1 — Safe local coding agent (Week 2)
- Add tools: read/write files, run tests, execute commands.
- Add policy engine for command allowlist + path restrictions.
- Add regression harness for generated code.

### Milestone 2 — Autonomous app-builder mode (Week 3)
- Goal decomposition and subtask graph.
- PR-style checkpoints and auto-test gates.
- Add reviewer/critic agent to validate outputs before merge.

### Milestone 3 — Self-improvement mode (Week 4)
- Agent can propose changes to itself.
- Every self-edit requires:
  - benchmark run,
  - safety policy checks,
  - rollback snapshot,
  - explicit approval policy.

### Milestone 4 — Paper-trading agent (Week 5)
- Market data connector + strategy plugin system.
- Paper order simulator and PnL accounting.
- Hard risk rules and daily limits.

### Milestone 5 — Limited live trading (Week 6+)
- Small capital deployment.
- Exchange API key scoping.
- Real-time monitoring + automatic halt on anomalies.

---

## 5) Autonomy model (important)

You asked for full autonomy. The practical way is **graduated autonomy**:

1. **Level 1: Suggest** — agent proposes, human executes.
2. **Level 2: Execute low-risk** — agent executes local dev tasks autonomously.
3. **Level 3: Execute bounded high-risk** — agent can trade/code deploy within strict budgets and limits.
4. **Level 4: Continuous operation** — only after reliability and incident response maturity.

This path gives speed without catastrophic downside.

---

## 6) Core safety and governance controls

1. **Policy-as-code**
   - Every tool call evaluated against machine-readable rules.
2. **Risk budget manager**
   - Tokens, cost, runtime, file scope, network scope, and financial risk budgets.
3. **Mandatory simulation gates**
   - New trading strategies must pass backtest + forward paper-trade windows.
4. **Two-key actions**
   - Sensitive operations require either second model consensus or human confirmation.
5. **Continuous evaluation**
   - Track task success rate, regression rate, and incident count.

---

## 7) First coding sprint: exact deliverables

Start by asking me to implement these in order:

1. **Project skeleton**
   - `agent_core/`, `tooling/`, `policy/`, `memory/`, `trading/`, `api/`, `tests/`
2. **Config + secrets**
   - `.env` loader, typed settings, provider keys.
3. **LLM gateway**
   - `generate_plan()`, `generate_code()`, `critic_review()`.
4. **Local tool executor**
   - safe shell/file/browser tools with policy checks.
5. **Single run loop**
   - objective in, trace out, artifacts saved.
6. **Test harness**
   - unit + integration tests for policy and tool calls.

Once those are complete, we layer in autonomy and trading modules.

---

## 8) What I need from you to begin coding immediately

Provide these decisions in one message:

1. Preferred cloud LLM provider(s).
2. Target exchanges for trading (e.g., Binance, Coinbase Advanced).
3. Asset classes (spot only? futures?).
4. Maximum acceptable daily drawdown (% and absolute).
5. Language/runtime confirmation (Python default).
6. Whether you want a local web dashboard in v1.

After that, I can generate the full codebase scaffold and begin milestone 0 implementation.
