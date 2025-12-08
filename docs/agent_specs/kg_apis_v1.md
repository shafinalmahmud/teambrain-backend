STEP H — KNOWLEDGE GRAPH APIs (The Real Interface)

Everything here becomes actual Python functions later.

We define 7 API categories, each with required methods.

H1 — Core Entity API

Handles CRUD (Create, Read, Update, Delete) for graph nodes.

1. create_entity()
create_entity(
    entity_type: str,
    label: str,
    properties: dict,
    embedding: vector = None
) -> entity_id


Agents use this when:

new tasks appear

new goals emerge

new user preferences are detected

new documents appear

new concepts are referenced

2. get_entity()
get_entity(entity_id: str) -> dict

3. update_entity()
update_entity(entity_id: str, properties: dict)

4. delete_entity()
delete_entity(entity_id: str)


Rarely used except by Guardian.

H2 — Relationship API

Adding and removing edges between nodes.

1. link()
link(source_id, relation_name, target_id, weight=1.0)

2. unlink()
unlink(source_id, relation_name, target_id)

3. get_relations()
get_relations(entity_id) -> dict

H3 — Graph Query API

Everything needed for reasoning, analysis, planning.

1. neighbors()
neighbors(entity_id, relation=None) -> list

2. walk()
walk(start_id, max_hops=3) -> dict

3. pattern_match()
pattern_match(pattern_dict) -> list


Used for:

“all tasks blocked by tasks with status=stalled”

“all projects requiring research”

“relationships involving deadline risk”

H4 — Embedding / Semantic API
1. embed_text()

Call your embedding model.

embed_text(text) -> vector

2. search_embeddings()
search_embeddings(query_vector, top_k=10) -> list

3. update_embedding()
update_embedding(entity_id, vector)

4. semantic_link()

Automatically create symbolic + semantic edges.

H5 — Reasoning API (Inference Layer)

This is the part that makes your system smart, not just stored data.

1. infer_related()
infer_related(entity_id) -> list


Finds nodes logically connected.

2. infer_missing_links()
infer_missing_links(entity_id) -> list[(source, relation, target)]

3. predict_next_steps()
predict_next_steps(entity_id) -> list


Used by Strategist Agent.

H6 — Validation & Integrity API

Guardian uses this.

1. validate_entity()
validate_entity(entity_id) -> list[errors]

2. detect_conflicts()
detect_conflicts(entity_id) -> list[conflict_nodes]

3. resolve_conflict()
resolve_conflict(entity_id, policy="latest_wins")

H7 — Persistence API (Disk Sync)
1. save_snapshot()
save_snapshot(path="kg/") -> bool

2. load_snapshot()
load_snapshot(path="kg/")

3. backup_to_remote()

Optional but good for enterprise.

H8 — Metadata & Graph Enhancements API
1. tag_entity()
tag_entity(entity_id, tags: list)

2. set_context_vector()

Stores the “session + identity + project” hybrid context vector.

3. cluster_graph()

Graph clustering.

4. rank_entities()

Prioritization.

5. temporal_decay()

Decay scoring integration.

H9 — API Surfaces by Agent
Strategist uses:

walk

pattern_match

infer_related

predict_next_steps

cluster_graph

Analyst uses:

embed_text

search_embeddings

rank_entities

infer_missing_links

Executor uses:

neighbors

get_relations

update_entity

link

Guardian uses:

validate_entity

detect_conflicts

resolve_conflict

unlink

Manager uses:

save_snapshot

load_snapshot

backup

cluster_graph

H10 — Final Output: Full Knowledge Graph API Specification

You now have a complete API surface that will later translate to:

kg.py

agent_orchestrator.py

controllers/memory_manager.py

controllers/knowledge_graph.py

models/entity.py

models/relation.py

This is literally the design stage Meta, Anthropic, and Adept use:
Define all APIs first → write implementation later.