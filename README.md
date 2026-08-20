# Autonomous Coding Agent

An agent that takes a bug description, explores a codebase, proposes a fix, 
runs tests to verify it, and retries with test-failure feedback if the fix is wrong.

## Status
Week 2 in progress — core agent loop, AST-aware search, and persistent memory 
implemented and verified on a real GitHub repo.

**Example run:** given a bug where `dev(a, b)` used subtraction instead of integer 
division, the agent's first attempt failed a test, received the failure as feedback, 
and corrected itself on the second attempt. Full run log: `data/latest_run.json`.

## How it works
1. Reads the target file from the repo
2. LLM (gpt-oss-120b via Groq) proposes a fix based on the issue description
3. Patch is applied and pytest is run to verify it
4. If tests fail, the failure output is fed back to the LLM for another attempt
5. Repeats up to 3 attempts
6. Past failed attempts on the same file are recorded to persistent memory and 
   surfaced in future prompts (see known limitation below)

## Project structure
- `tools/` — agent capabilities: code search (plain + AST-based), repo cloning, 
  patch application, test running, persistent memory
- `loop.py` — the core agent loop (explore → patch → test → retry)
- `patch_generator.py` — LLM interface for generating fixes
- `run_real_issue.py` — driver script to run the agent against a real repo/issue
- `scripts/` — early proof-of-concept scripts from initial setup (not part of the core system)

## Run it
python run_real_issue.py

## Next steps
- Planner step (separate "understand the bug" from "write the fix")
- Docker sandboxing for safer execution
- Run against real SWE-bench-lite issues for a benchmarked resolve rate
- Failure taxonomy and cost/latency tracking

## Known limitation: prompt-based memory
Implemented persistent cross-session memory that records failed attempts and 
injects them into future prompts as "avoid this" context. Verified the memory 
system correctly loads and injects past failures — however, testing showed 
the LLM (gpt-oss-120b via Groq) sometimes repeats the exact same mistake 
even when explicitly warned against it in the prompt. This suggests naive 
prompt-based memory has real limits; a more robust approach might involve 
structured output validation or explicit constraint-checking rather than 
relying on the model to honor a warning embedded in context.

## Known limitation: plan-following consistency
Added a planning step where the LLM reasons about root cause and approach 
before writing code. Testing revealed the generated plan and the actual code 
written aren't always consistent — in one verified run, the plan's stated 
conclusion favored regular division (`a / b`), but the code-generation step 
produced integer division (`a // b`), which was actually correct. The final 
code was right, but by chance alignment with the original issue text rather 
than because it faithfully followed its own plan. This reinforces the memory 
finding above: LLM-generated intermediate artifacts (plans, memory warnings) 
influence but don't reliably constrain subsequent generations in this setup.


## Known limitation: plan-following consistency
Added a planning step where the LLM reasons about root cause and approach 
before writing code. Across multiple runs, the generated plan consistently 
favored true division (`a / b`) in its stated reasoning, while the actual 
code-generation step produced integer division (`a // b`) — the correct fix. 
This divergence was observed reproducibly across 3+ separate runs, suggesting 
the plan reliably influences but does not strictly constrain the final code 
generation step. Combined with the memory-injection finding above, this points 
to a broader pattern: prompt-embedded reasoning artifacts in this pipeline 
provide guidance rather than hard constraints on model behavior.

## Next steps
- Run against real SWE-bench-lite issues for a benchmarked resolve rate
- Formal failure taxonomy across many runs
- Cost/latency tracking and one real ablation experiment