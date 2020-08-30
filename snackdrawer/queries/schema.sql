-- :name drop_snacks
DROP TABLE snacks

-- :name delete_all_snacks
DELETE FROM snacks

-- :name create_snacks
CREATE TABLE IF NOT EXISTS snacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL
)

-- :name drop_users
DROP TABLE users

-- :name delete_all_users
DROP TABLE users

-- :name create_users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL,
    password_hash VARCHAR(256) NOT NULL
)

-- :name drop_drawers
DROP TABLE drawers

-- :name delete_all_drawers
DELETE FROM drawers

-- :name create_drawers
CREATE TABLE IF NOT EXISTS drawers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    name VARCHAR(64) NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
)

-- :name drop_drawercontents
DROP TABLE drawercontents

-- :name delete_all_drawercontents
DELETE FROM drawercontents

-- :name create_drawercontents
CREATE TABLE IF NOT EXISTS drawercontents (
    drawerid INTEGER NOT NULL,
    snackid INTEGER NOT NULL,
    CONSTRAINT con_primary_contents PRIMARY KEY (drawerid, snackid),
    FOREIGN KEY (drawerid) REFERENCES drawers(id) ON DELETE CASCADE,
    FOREIGN KEY (snackid) REFERENCES snacks(id) ON DELETE CASCADE
)