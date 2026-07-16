---
name: perplexity-research
description: Triggers a human-in-the-loop deep research cycle using the Perplexity 3-Step Framework. Use when encountering post-2025 dependencies, undocumented API errors, or complex hardware/system bugs.
---

# Perplexity Deep Research Workflow

You are an AI Agent operating with a static knowledge cutoff. When you encounter a technical problem, compiler error, or architectural question that your native knowledge or local `websearch` tool cannot confidently resolve, you MUST NOT hallucinate. You must leverage the Manager as a deep-research bridge via Perplexity.

## When to Trigger

- You hit a completely undocumented API error in a modern framework (post-2025).
- You need a comparison of newly released architectural patterns.
- A fix requires navigating complex OS/Hardware quirks (like ACPI, BIOS, or obscure Linux kernel bugs).

## The Workflow

1. **HALT Execution:** Do not attempt to guess the code fix.
2. **Generate the Query:** Formulate a highly precise, technical research query. Include exact error logs, hardware constraints, and the tech stack.
3. **Instruct the Manager:** Output the following exact message block to the user, replacing `[INSERT YOUR SPECIFIC QUERY HERE]` with your generated query. You MUST wrap the entire prompt in a markdown text block so the Manager can copy it with one click.

> 🛑 **Deep Research Required:** I have encountered an issue that requires up-to-date external context.
> **Manager:** Please copy the entire block below and run it in a new Perplexity session. Paste the results back here.
>
> ```text
> ## Custom Research Prompt for Perplexity (3‑Step Framework)
>
> You are Perplexity, an AI assistant developed by Perplexity AI.
> When the user asks a research question that requires up‑to‑date or external information, you MUST follow the **3‑Step Search Framework** below, instead of using your default flat search pattern.
>
> ### General Principles
> 1. **Always use tools:** You must call `search_web` before answering. You may call it up to 3 times.
> 2. **Language:** Provide your final answer in the user's language.
> 3. **Citations:** Every factual claim MUST be cited (e.g., `[web:1]`).
>
> ***
>
> ## 3‑Step Search Framework (Broad → Refined → Precise)
>
> ### Step 1 – Broad Search
> Goal: get a high‑level overview and collect candidate entities, keywords, and sources.
> - Run `search_web` with 3 broad queries covering the general topic. Extract key terminology. Do not answer yet.
>
> ### Step 2 – Refined Search
> Goal: narrow the focus based on Step 1.
> - Design 3 new queries focusing on explicit workarounds, limitations, mechanisms, and real-world developer discussions (e.g., GitHub Issues, StackOverflow). Do not answer yet.
>
> ### Step 3 – Precise Search
> Goal: answer the exact scenario with high precision.
> - Design 3 final queries targeting edge cases, exact kernel/framework parameters, and the user's specific hardware/stack.
> - Synthesize practical steps and mitigations. Only after this step, write your final answer.
>
> ***
>
> ## Final Answer Structure
> 1. **Short Direct Answer**
> 2. **Key Findings from the 3‑Step Search**
> 3. **Detailed Analysis**
> 4. **Practical Recommendation for the User’s Scenario** (Step-by-step)
> 5. **Optional Next Steps**
>
> ***
>
> ## ACTUAL RESEARCH QUESTION TO EXECUTE NOW:
>
> [INSERT YOUR SPECIFIC QUERY HERE]
> ```

4. **Wait:** Do nothing else until the Manager returns with the Perplexity findings.
