STEP N — TOOL INVOCATION PROTOCOL (LLM → RUNTIME → TOOL CALL FORMAT)

This is the exact protocol your LLM must follow when:

deciding a tool is needed,

producing a tool call,

returning the arguments,

receiving the tool’s result,

continuing the reasoning.

This is EXTREMELY sensitive — if you screw up the format by even one comma, the entire tool system collapses.

N.1 — TOOL CALL FORMAT (Strict OpenAI-Style Tool Schema)

Your LLM must ALWAYS return tool calls in this exact JSON shape:

{
  "tool": {
    "name": "tool_name",
    "arguments": {
        ... validated payload ...
    }
  }
}


NOTHING extra.
NO natural language.
NO explanation.
NO reasoning before or after.
Just this clean JSON block.

This prevents hallucinations and parsing failures.

N.2 — FULL RULESET (MANDATORY)
Rule 1 — The LLM must NEVER mix natural language and tool JSON.

Wrong:

Sure, let me use the search tool
{
 "tool": ...
}


Correct:

{
 "tool": ...
}

Rule 2 — The tool name MUST match EXACTLY the registry.

If the registered name is web.search, the LLM must return:

"name": "web.search"


Not:

"search"

"web_Search"

"WebSearch"

"search_google"

Rule 3 — Arguments must NEVER include extra fields.

If the schema is:

{ "query": string, "num_results": integer }


Then even this will break your system:

{ "query": "hello", "num_results": 5, "extra": 1 }

Rule 4 — Every required field MUST be present.

If a required field is missing → reject.

Rule 5 — Types MUST match (string where string, number where number).

Otherwise → automatic tool error.

Rule 6 — The runtime ALWAYS returns:
{
  "tool_result": {
    "tool": "tool_name",
    "output": { ... }
  }
}


The LLM must accept this and continue reasoning WITHOUT hallucinating new structure.

N.3 — FULL TOOL CALL LIFECYCLE (LLM → Engine → Tool → LLM)
1. LLM decides tool is needed

It produces:

{
  "tool": {
    "name": "web.search",
    "arguments": {
        "query": "AI agent memory issues",
        "num_results": 5
    }
  }
}

2. Execution engine receives JSON

validates schema

runs the tool

captures output

3. Engine returns the result to the LLM

The runtime MUST wrap tool output like this:

{
  "tool_result": {
    "tool": "web.search",
    "output": {
       "results": [...]
    }
  }
}

4. LLM continues thinking

Now the LLM can “see” the tool result and produce either:

normal text

OR another tool call

OR chain actions

This forms your agentic loop.

N.4 — PROTOCOL FOR MULTI-STEP REASONING

When your Orchestrator calls a tool, the LLM MUST NOT:

summarize tool calls

alter arguments

generate commentary

output invalid JSON

Instead:

Correct loop example:

LLM: (decides to search)

{
  "tool": {
    "name": "web.search",
    "arguments": {
      "query": "best GPT-4o memory frameworks",
      "num_results": 5
    }
  }
}


Runtime → returns result:

{
  "tool_result": {
    "tool": "web.search",
    "output": {
      "results": [ ... ]
    }
  }
}


LLM (continues):

Based on the results, I recommend...

N.5 — PROTOCOL FOR MULTI-AGENT TOOL CALLS

Each agent uses the SAME protocol, but with role metadata:

{
  "agent": "Analyst",
  "tool": {
    "name": "data.vector_search",
    "arguments": {
        "embedding": [...],
        "top_k": 5
    }
  }
}


Runtime MUST validate:

whether this agent has permission

whether rate limits allow it

whether project context matches

This is how you prevent a rogue agent from spamming tools.

N.6 — INLINE COT (Chain-of-Thought) IS DISALLOWED IN TOOL CALL MODE

Inside tool decisions, the LLM cannot “think” normally.

Instead you enforce:

STRICT MODE:

No Chain-of-Thought

No reasoning

No verbose text

Only JSON tool calls

This keeps the system deterministic.

N.7 — FALLBACK / NO TOOL NEEDED MODE

If the LLM decides a tool is unnecessary, output normal text:

Here’s the result without using any tool...


No JSON in that case.

N.8 — ORCHESTRATOR ENFORCEMENT RULES

Before executing any tool call:

Validate JSON

Validate schema

Validate agent permissions

Validate rate limits

Validate workspace context

Validate project boundaries

Log event

Execute tool

Wrap result

Return to LLM

This prevents errors and misuse.

✔️ Step N is COMPLETE.

Your tool system now follows a professional, enterprise-grade protocol.