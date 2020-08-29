-- :name create_snacks
CREATE TABLE IF NOT EXISTS snacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL
)

-- :name populate_snacks
INSERT INTO snacks (name) VALUES (
    'chips'
),
(
    'chocolate'
),
(
    'cookies'
)