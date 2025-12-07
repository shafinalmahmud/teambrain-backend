🔥 1. CORE INPUT CLASSIFICATION ENGINE

Every incoming message (user → system) passes through a classifier:

CLASSIFIER OUTPUTS
message_type:
  - Task_Command
  - Personal_Info
  - Preference
  - Project_Specific_Info
  - Long-Term_Knowledge
  - Temporary_Context
  - File/Document
  - Emotional_State
  - Safety_Risk


Each type triggers different routing rules.

If you skip this layer, you’re building trash. This is mandatory.

🔥 2. ROUTING DECISION TREE (TOP LEVEL)
IF message_type == Personal_Info:
    route → Identity Namespace
ELSE IF message_type == Preference:
    route → Personal Pref Namespace
ELSE IF message_type == Project_Specific_Info:
    route → Project Namespace
ELSE IF message_type == Long-Term_Knowledge:
    route → Global Knowledge Namespace
ELSE IF message_type == Temporary_Context:
    route → Session Memory (auto-expire)
ELSE IF message_type == File/Document:
    route → Document Store + Vector Index
ELSE IF message_type == Safety_Risk:
    route → Guardian Agent → Controlled Memory Rules
ELSE:
    route → Default Session + Executor Agent


This is the top-level router.
Now let’s drill deeper.

🔥 3. ENTERPRISE MEMORY RULESET (Hybrid Model)

Since you selected Option C (Hybrid + Enterprise):

Shared Memory (team-wide):

User identity

Preferences

High-level goals

Approved long-term project data

Public knowledge & documents

Isolated (per-agent workspace memory):

Intermediate reasoning

Drafts

Temporary task deconstruction

Agent-specific subgoals

Protected memory (Guardian-controlled):

Sensitive personal data

Safety-critical instructions

Access-controlled organization data

Each requires separate routing rules.

🔥 4. ROUTING LOGIC PER AGENT
Strategist Agent Routing Rules

Stores:

High-level user goals

Strategic plans

Long-term roadmaps

Multi-week/month workflows

Reads:

Identity namespace

Preference namespace

Global knowledge

Approved project memories

Blocks:

Temporary task states

Raw personal data

Analyst Agent Routing Rules

Stores:

Structured insights

Analysis summaries

Extracted entities

Data patterns

Reads:

Documents

Project namespace

Session memory

Global knowledge

Blocks:

Personal identity memory

Preference memory

Executor Agent Routing Rules

Stores:

Action results

Task statuses

Execution logs

Reads:

Analyst insights

Strategist plans

Task details

Blocks:

Identity namespace

Anything irrelevant to execution

Guardian Agent Routing Rules

Stores:

Safety incidents

Sensitive data fingerprints

Restricted resource access keys

Reads:

EVERYTHING
(only at request or risk trigger)

Blocks:

Nothing
(but can deny writes globally)

Manager Agent Routing Rules

Stores:

Agent coordination logs

Pipeline optimization data

Performance reports

Workflow metadata

Reads:

All non-sensitive namespaces

Blocks:

Protected memory unless allowed by Guardian

🔥 5. MEMORY WRITE DECISIONS
Write Allowed?
IF data is sensitive:
    Guardian approval required
ELSE IF data impacts personalization:
    Store in Identity/Preferences
ELSE IF data impacts project:
    Store in Project namespace
ELSE IF temporary:
    Store in Session
ELSE:
    Store in Global Knowledge

Write Format Rules

Convert to structured JSON

Chunk large texts

Generate embeddings

Attach metadata

Store in appropriate index

If not structured → reject and trigger reformatting.

🔥 6. MEMORY READ DECISIONS
Who can read what?
Strategist:
    read → identity, prefs, global, project
    block → raw sensitive

Analyst:
    read → docs, project, global
    block → identity/prefs

Executor:
    read → task, analyst_output

Guardian:
    read → ALL (restricted usage)

Manager:
    read → all non-sensitive


If a forbidden read is attempted → throw a “Memory Access Violation”.

🔥 7. ADVANCED LOGIC — MEMORY EXPIRY & RETENTION
Session Memory

expires in 1–24 hours

used for chat context

never stored permanently

Project Memory

expires only when project closes

enterprise can override

Identity/Preferences

permanent until user edits

Sensitive Data

never expires unless forced delete

Guardian encrypted

🔥 8. FULL ROUTER FLOW (FINAL)
INPUT → classifier

classifier → message_type

message_type → memory_ruleset

memory_ruleset → target_namespace

target_namespace → embedding + metadata pipeline

pipeline → vector db write OR denial

denial → guardian handler

guardian handler → escalate / block / sanitize

successful write → update Manager Agent logs