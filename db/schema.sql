-- install enable pgvector extension for postgres
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE customers (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    price_cents INTEGER NOT NULL CHECK(price_cents >= 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE orders (
    id              SERIAL PRIMARY KEY,
    customer_id     INTEGER not null references customers(id),
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (STATUS IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    ordered_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    shipped_at      TIMESTAMPTZ
);


CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);

CREATE TABLE order_items (
    id                SERIAL PRIMARY KEY,
    order_id          INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id        INTEGER NOT NULL REFERENCES products(id),
    quantity          INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents  INTEGER NOT NULL CHECK (unit_price_cents >= 0)
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);


create table document_chunks (
    id              SERIAL PRIMARY KEY,
    source_id       TEXT NOT NULL,
    source_url      TEXT,
    content         TEXT NOT NULL,
    content_hash    TEXT NOT NULL,
    embedding       vector(1536),
    search_vec      tsvector generated always as (to_tsvector('english', content)) STORED,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_chunks_source_id ON document_chunks(source_id);
CREATE UNIQUE INDEX idx_chunks_source_hash ON document_chunks(source_id, content_hash);
CREATE INDEX idx_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_chunks_search_vec ON document_chunks USING gin (search_vec);

-- create readonly role for llm to connect to db

CREATE ROLE langchain_mcp_llm_reader WITH LOGIN PASSWORD 'llm_read';
GRANT CONNECT ON DATABASE langchain_mcp_llm TO langchain_mcp_llm_reader;
GRANT USAGE ON SCHEMA public TO langchain_mcp_llm_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO langchain_mcp_llm_reader;

-- ensures any table created later is also read-only for this role automatically
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO langchain_mcp_llm_reader;