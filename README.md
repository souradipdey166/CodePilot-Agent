# Autonomous Coding Agent

An agent that takes a bug description, explores a codebase, proposes a fix, 
runs tests to verify it, and retries with test-failure feedback if the fix is wrong.

## Status
Week 1 prototype — core agent loop working end-to-end, verified on a real GitHub repo.

**Example run:** given a bug where `dev(a, b)` used subtraction instead of integer 
division, the agent's first attempt failed a test, received the failure as feedback, 
and corrected itself on the second attempt. Full run log: `data/latest_run.json`.

## How it works
1. Reads the target file from the repo
2. LLM (Llama 3.3 70B via Groq) proposes a fix based on the issue description
3. Patch is applied and pytest is run to verify it
4. If tests fail, the failure output is fed back to the LLM for another attempt
5. Repeats up to 3 attempts

## Project structure
- `tools/` — agent capabilities: code search, repo cloning, patch application, test running
- `loop.py` — the core agent loop (explore → patch → test → retry)
- `patch_generator.py` — LLM interface for generating fixes
- `run_real_issue.py` — driver script to run the agent against a real repo/issue
- `scripts/` — early proof-of-concept scripts from initial setup (not part of the core system)

## Run it
python run_real_issue.py

## Next steps
- AST-aware code search (currently plain text search)
- Docker sandboxing for safer execution
- Run against real SWE-bench-lite issues for a benchmarked resolve rate
- Failure taxonomy and cost/latency tracking