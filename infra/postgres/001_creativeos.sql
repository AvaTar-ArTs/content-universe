create schema if not exists creativeos;

create table if not exists creativeos.workflow_nodes (
  id text primary key,
  workflow_id text not null,
  kind text not null,
  label text not null,
  status text not null check (status in ('observed','modeled','available','executed','verified','blocked')),
  metadata jsonb not null default '{}'
);

create table if not exists creativeos.workflow_edges (
  id bigserial primary key,
  workflow_id text not null,
  source_id text not null references creativeos.workflow_nodes(id),
  verb text not null,
  target_id text not null references creativeos.workflow_nodes(id),
  metadata jsonb not null default '{}',
  unique(workflow_id, source_id, verb, target_id)
);

create table if not exists creativeos.prompt_manifests (
  id text primary key,
  version text not null,
  original_intent text not null,
  operation text not null,
  manifest jsonb not null,
  created_at timestamptz not null default now()
);

create index if not exists prompt_manifests_manifest_gin on creativeos.prompt_manifests using gin (manifest);
