-- :name drop_snacks
DROP TABLE snacks

-- :name create_snacks
CREATE TABLE IF NOT EXISTS snacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL
)