🚨 STEP: Build the Memory Manager Agent (Enterprise-Grade)
🎯 Core Purpose

The Memory Manager Agent is responsible for three critical missions:

1. Protect memory integrity

Nothing gets added, updated, or deleted without passing its rules.

2. Maintain memory structure and hygiene

It performs auto-cleaning, expiration, conflict resolution, duplication removal, and consistency checks.

3. Enforce layer boundaries

Identity, project, and workspace memories cannot leak into each other.

If the Memory Manager fails at ANY of these, the whole product collapses.

🧠 1. Memory Manager Agent — Capabilities

This agent has exclusive control over the memory layer.
Every other agent must go through it.

Here’s the exact capability list:

(A) memory.validate_request()

Checks if the request is allowed:

Validates agent permissions

Ensures correct memory layer

Confirms format correctness

Prevents workspace access by user-facing agents

If invalid → returns REJECT.

(B) memory.normalize()

Before any write, update, or search:

Removes filler words

Converts bullets to full sentences

Standardizes timestamp format

Fixes inconsistent punctuation or casing

This keeps memory clean.

(C) memory.classify_layer()

The Manager classifies which layer a memory belongs to:

Layer	Criteria
Identity	"Who is the user?" / "What is the user's long-term preferences/goals/traits?"
Project	"How does the system work?" / "Architecture, rules, roles, dependencies."
Workspace	"Temporary task info, transcripts, partial calculations, drafts."

If ambiguous → assign to workspace until clarified.

(D) memory.route()

Decides EXACTLY where each memory goes.

Identity → KV store + vector DB
Project → vector DB + rule index
Workspace → isolated vector DB

(E) memory.write()

Only the Memory Manager can execute writes.

Other agents must send:

{
  action: "write",
  content: "...",
  origin: "Strategist/Analyst/Executor/etc",
  metadata: { task_id, tags }
}


Memory Manager checks:

Scope

Valid content

Expiration rules

Whether this memory already exists

Whether it needs merging

(F) memory.update()

For modifications:

Updates identity only when the user clarifies or corrects

Updates project when architecture changes

Updates workspace freely

(G) memory.delete()

Rules:

Workspace memories deleted after task completion

Project memories deleted only on version migration

Identity never deleted unless user explicitly commands

(H) memory.dedupe()

Every memory object is checked against:

Vector similarity

Keyword overlap

Metadata overlap

If >85% match → merge into one.

(I) memory.expire()

The Manager applies expiration rules:

Workspace auto-expires

Project only expires when replaced

Identity rarely expires

(J) memory.audit()

A daily or per-task audit does:

Remove corrupt items

Repair broken embeddings

Check for missing metadata

Reembed outdated content

🛡️ 2. Memory Manager — Permission Model
Allowed to read:

All layers

Allowed to write:

All layers

Allowed to update:

All layers (identity with caution)

Allowed to delete:

Workspace freely

Project with rules

Identity only on user command

Forbidden actions:

Act as a planning agent

Modify content on its own

Generate user-facing messages

It is a backend guardian, not a conversational agent.

🧠 3. Memory Manager Agent — Internal Architecture

This is EXACTLY how you structure it:

MemoryManagerAgent {
    classify_layer();
    validate_request();
    normalize();
    check_duplicates();
    decide_route();
    write();
    update();
    delete();
    expire();
    audit();
    monitor_leaks();
}

🧩 4. Memory Manager Agent — Example Flow
Example Scenario

The Analyst agent sends:

{
  action: "write",
  content: "The project uses three agents. Executor runs tasks. Analyst plans tasks. Manager synchronizes everything.",
  origin: "Analyst Agent",
  metadata: { tags: ["architecture"], task_id:"task_92" }
}

Memory Manager Steps:

1. Validate

Analyst is allowed to propose project memory → OK

2. Normalize

Clean ambiguous grammar → OK

3. Classify

This is about system architecture → Project memory

4. Route

Goes to project_memory namespace

5. Dedupe

Checks for similar architecture memory → none → OK

6. Write

Creates memory object proj_11124

7. Audit

Adds index to architecture-rule table

📦 5. Memory Manager — Required Components

To build it fully, you need:

A. Permissions Table

Which agent can write/update which layer.

B. Dictionary of rules

identity_rules.json

project_rules.json

workspace_rules.json

C. Embedding handler

Automatic embedding after normalization.

D. Expiry Cron

For clearing workspace.

E. Memory router

Implements the hybrid routing logic.

F. Dedupe engine

Uses vector similarity threshold (0.85).

🧠 6. Pseudo-Code (Production-Level)

Here is production-style pseudocode you will use when implementing:

function handleMemoryRequest(request) {
    validate_request(request);

    cleaned = normalize(request.content);

    layer = request.layer ?? classify_layer(cleaned);

    route = decide_route(layer);

    if (request.action === "write") {
        if (exists(cleaned)) {
            merged = merge(cleaned, existing);
            return update(merged);
        }
        return write(cleaned, route);
    }

    if (request.action === "update") {
        return update(request.id, cleaned);
    }

    if (request.action === "delete") {
        return delete(request.id);
    }

    throw Error("Invalid memory action");
}

🧠 7. Memory Manager Agent — Description Block (For Your System)

Use this when defining the agent in your architecture file:

The Memory Manager Agent is responsible for validating, structuring, routing, storing, updating, auditing, and protecting all memory entities across identity, project, and workspace layers. I