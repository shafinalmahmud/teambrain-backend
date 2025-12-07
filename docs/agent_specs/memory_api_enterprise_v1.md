🚀 THE MEMORY API (Enterprise, Multi-Agent, Hybrid Memory Architecture)

This is the API your agents will use to read, write, query, update, and delete memory across the three layers:

Identity Memory (shared, stable)

Project Memory (shared, evolving)

Workspace Memory (private, dynamic)

This API is stateless, simple, fast, and fully vector-DB backed.

🧠 1. Memory API — High-Level Overview

Your Memory API has 5 main functionalities:

1. WRITE

Store a new memory record (identity, project, or workspace).

2. READ

Fetch relevant memories using semantic search or IDs.

3. UPDATE

Modify an existing memory.

4. DELETE

Remove stale or invalid memories.

5. QUERY-MODE SWITCH

Chooses retrieval mode based on layer:

Identity → semantic + keyword

Project → semantic + rules

Workspace → ID-specific + strict

This keeps your system fast and clean.

🧠 2. Memory Object Structure (Universal Format)

Every memory item across all layers follows the same object schema, so agents never get confused.

MemoryObject {
    id: string; 
    layer: "identity" | "project" | "workspace";
    title: string;
    content: string;
    embeddings: float[];
    metadata: {
        agent?: string;
        task_id?: string;
        user_visible?: boolean;   
        timestamp: string;
        expiry?: string;
        tags?: string[];
    };
}

Notes:

user_visible = false by default for workspace items.

Timestamps are stored in UTC.

Expiry is optional — identity memories usually have none.

🧠 3. Memory API Endpoints (Enterprise Detail)

You will implement these endpoints in your orchestrator/backend.

I’m giving you exact request/response structures.

✅ Endpoint 1 — memory.write()
Purpose

Store a new memory in the proper namespace.

Input
{
  layer: "identity" | "project" | "workspace",
  title: string,
  content: string,
  metadata: {
      agent?: string,
      task_id?: string,
      user_visible?: boolean,
      expiry?: string,
      tags?: string[]
  }
}

Output
{
  success: true,
  id: "mem_xxxxx"
}

Rules

Identity & Project writes must come from Manager Agent or explicit user instruction.

Workspace writes can come from Planner/Analyst/Executor/Guardian/Manager.

auto-embed content before storing.

✅ Endpoint 2 — memory.read()
Purpose

Retrieve memory.

Modes

Depending on layer:

Identity Layer:
mode: "semantic" | "keyword"

Project Layer:
mode: "semantic"

Workspace Layer:
mode: "id" | "task"

Input
{
  layer: "identity" | "project" | "workspace",
  query?: string,  
  id?: string,
  task_id?: string,
  limit?: number
}

Output
{
  success: true,
  results: MemoryObject[]
}

✅ Endpoint 3 — memory.update()
Input
{
  id: string,
  new_title?: string,
  new_content?: string,
  new_metadata?: object
}

Output
{
  success: true
}

Rules

Identity memory updates require user confirmation (unless it's a system refinement).

Workspace updates are free-flow (agents can update as tasks evolve).

✅ Endpoint 4 — memory.delete()
Input
{
  id: string
}

Output
{
  success: true
}

Rules

Identity memories should almost never be deleted unless the user explicitly requests it.

Workspace memories auto-expire after task completion.

✅ Endpoint 5 — memory.search()
Purpose

Run advanced semantic search across layers.

Input
{
  layer: "identity" | "project" | "workspace",
  query: string,
  top_k: number
}

Output
{
  results: MemoryObject[]
}

Rules

Workspace search only allowed by system agents.

User agent cannot search workspace or access workspace items.

🧠 4. Memory Routing Logic (Critical Layer)

This is where most developers screw up.
Here’s the correct routing:

When a memory is added → which layer?
Identity Memory

If memory answers:
“Who is the user? What do they want long-term?”
→ goes to identity_memory.

Project Memory

If memory answers:
“How does the system work? What is the architecture? What are the rules?”
→ goes to project_memory.

Workspace Memory

If memory answers:
“What task is currently being executed?”
→ goes to workspace_memory.

When an agent fetches memory → how?
User Chat Agent

identity: semantic

project: semantic

workspace: ❌ never allowed

Planner / Analyst / Executor / Guardian / Manager

Have full access.

🧠 5. Memory Retrieval Priority (Enterprise)

This prevents contradictions and hallucinations.

Identity Layer Priority

Exact match on user identity tags

Keyword match

Semantic match

Recentness

Project Layer Priority

Architecture-critical

Role-critical

Safety-critical

Semantic relevance

Workspace Layer Priority

task_id

agent metadata

recency

semantic match

🧠 6. Memory Expiration Rules
Identity Memory

Permanent, unless user corrects something.

Project Memory

Persistent across product versions.

Updated by Manager Agent when architecture changes.

Workspace Memory

Auto-deleted when task completes.

Auto-deleted after X hours of inactivity.

Manually deleted when switching projects.

🧠 7. Error Handling (Enterprise-Level)
Types of errors:

Missing memory

Invalid layer

Attempted workspace leakage

Unauthorized write

Embedding failure

Response example:
{
  success: false,
  error_type: "workspace_restricted",
  message: "User-facing agent is not allowed to access workspace memory."
}

🧠 8. Final API Summary (Production-Ready)

Your Memory API will expose:

memory.write()
memory.read()
memory.update()
memory.delete()
memory.search()


Built on top of:

Vector DB

Metadata filters

Embeddings

Layer-based retrieval logic

This memory API is clean, modular, scalable, and engineered for multi-agent systems.