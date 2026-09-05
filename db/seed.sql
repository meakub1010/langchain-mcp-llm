-- db/seed.sql
-- Run against an already-migrated schema (db/schema.sql).

-- ── customers ──────────────────────────────────────────────
INSERT INTO customers (name, email, created_at) VALUES
    ('Alice Chen',       'alice.chen@example.com',    CURRENT_DATE - INTERVAL '90 days'),
    ('Brian Osei',       'brian.osei@example.com',    CURRENT_DATE - INTERVAL '85 days'),
    ('Carla Mendes',     'carla.mendes@example.com',  CURRENT_DATE - INTERVAL '80 days'),
    ('David Kim',        'david.kim@example.com',     CURRENT_DATE - INTERVAL '70 days'),
    ('Elena Petrova',    'elena.petrova@example.com', CURRENT_DATE - INTERVAL '60 days'),
    ('Farrukh Aziz',     'farrukh.aziz@example.com',  CURRENT_DATE - INTERVAL '45 days'),
    ('Grace Lin',        'grace.lin@example.com',     CURRENT_DATE - INTERVAL '30 days'),
    ('Hassan Malik',     'hassan.malik@example.com',  CURRENT_DATE - INTERVAL '15 days');

-- ── products ───────────────────────────────────────────────
INSERT INTO products (name, category, price_cents) VALUES
    ('Wireless Mouse',        'Electronics', 2499),
    ('Mechanical Keyboard',   'Electronics', 8999),
    ('USB-C Hub',             'Electronics', 3499),
    ('27" Monitor',           'Electronics', 24999),
    ('Desk Lamp',             'Home',        1999),
    ('Ceramic Mug Set',       'Home',        1599),
    ('Standing Desk',         'Home',        34999),
    ('Ergonomic Chair Cushion','Home',       2899),
    ('The Pragmatic Programmer', 'Books',    3299),
    ('Designing Data-Intensive Applications', 'Books', 4499),
    ('Cotton T-Shirt',        'Apparel',     1499),
    ('Wool Beanie',           'Apparel',     1899);

-- ── orders ─────────────────────────────────────────────────
-- statuses span the full lifecycle; dates spread from ~60 days ago to ~2 days ago
INSERT INTO orders (customer_id, status, ordered_at, shipped_at) VALUES
    (1, 'delivered', CURRENT_DATE - INTERVAL '58 days', CURRENT_DATE - INTERVAL '55 days'),
    (2, 'delivered', CURRENT_DATE - INTERVAL '50 days', CURRENT_DATE - INTERVAL '47 days'),
    (3, 'delivered', CURRENT_DATE - INTERVAL '45 days', CURRENT_DATE - INTERVAL '42 days'),
    (1, 'cancelled', CURRENT_DATE - INTERVAL '40 days', NULL),
    (4, 'delivered', CURRENT_DATE - INTERVAL '38 days', CURRENT_DATE - INTERVAL '35 days'),
    (5, 'delivered', CURRENT_DATE - INTERVAL '33 days', CURRENT_DATE - INTERVAL '30 days'),
    (2, 'shipped',   CURRENT_DATE - INTERVAL '25 days', CURRENT_DATE - INTERVAL '23 days'),
    (6, 'delivered', CURRENT_DATE - INTERVAL '22 days', CURRENT_DATE - INTERVAL '19 days'),
    (3, 'delivered', CURRENT_DATE - INTERVAL '20 days', CURRENT_DATE - INTERVAL '17 days'),
    (7, 'shipped',   CURRENT_DATE - INTERVAL '14 days', CURRENT_DATE - INTERVAL '12 days'),
    (1, 'paid',      CURRENT_DATE - INTERVAL '12 days', NULL),
    (8, 'delivered', CURRENT_DATE - INTERVAL '11 days', CURRENT_DATE - INTERVAL '9 days'),
    (4, 'shipped',   CURRENT_DATE - INTERVAL '9 days',  CURRENT_DATE - INTERVAL '7 days'),
    (5, 'shipped',   CURRENT_DATE - INTERVAL '8 days',  CURRENT_DATE - INTERVAL '6 days'),
    (2, 'paid',      CURRENT_DATE - INTERVAL '6 days',  NULL),
    (6, 'shipped',   CURRENT_DATE - INTERVAL '6 days',  CURRENT_DATE - INTERVAL '4 days'),
    (7, 'pending',   CURRENT_DATE - INTERVAL '4 days',  NULL),
    (3, 'shipped',   CURRENT_DATE - INTERVAL '3 days',  CURRENT_DATE - INTERVAL '1 day'),
    (8, 'pending',   CURRENT_DATE - INTERVAL '2 days',  NULL),
    (1, 'pending',   CURRENT_DATE - INTERVAL '1 day',   NULL);

-- ── order_items ────────────────────────────────────────────
-- unit_price_cents intentionally copies the product's price at seed time
-- (mirrors "price at time of purchase" — real app code would do the same on insert)
INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents) VALUES
    (1, 1, 1, 2499), (1, 3, 1, 3499),
    (2, 4, 1, 24999),
    (3, 9, 2, 3299),
    (4, 2, 1, 8999),
    (5, 5, 2, 1999), (5, 6, 1, 1599),
    (6, 7, 1, 34999),
    (7, 11, 3, 1499),
    (8, 10, 1, 4499), (8, 9, 1, 3299),
    (9, 1, 2, 2499),
    (10, 12, 2, 1899),
    (11, 2, 1, 8999), (11, 3, 1, 3499),
    (12, 8, 1, 2899),
    (13, 4, 1, 24999),
    (14, 6, 4, 1599),
    (15, 1, 1, 2499),
    (16, 11, 2, 1499),
    (17, 5, 1, 1999),
    (18, 9, 1, 3299), (18, 10, 1, 4499),
    (19, 7, 1, 34999),
    (20, 3, 2, 3499);