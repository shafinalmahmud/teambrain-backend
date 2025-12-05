-- docs/schema.sql
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text UNIQUE,
    plan text DEFAULT 'free',
    created_at timestamp DEFAULT now()
);

CREATE TABLE projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES users(id),
    name text,
    settings jsonb,
    created_at timestamp DEFAULT now()
);

CREATE TABLE teams (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid REFERENCES projects(id),
    type text,
    config jsonb,
    created_at timestamp DEFAULT now()
);

CREATE TABLE tasks (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id uuid REFERENCES teams(id),
    user_id uuid REFERENCES users(id),
    input text,
    status text DEFAULT 'queued',
    result jsonb,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now()
);

CREATE TABLE memories (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES users(id),
    team_id uuid,
    task_id uuid,
    content text,
    embedding vector(1536),
    tags jsonb,
    importance float,
    last_used_at timestamp
);

CREATE TABLE agent_logs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id uuid REFERENCES tasks(id),
    agent_name text,
    raw_output text,
    trace jsonb,
    tokens_used integer,
    score float,
    created_at timestamp DEFAULT now()
);