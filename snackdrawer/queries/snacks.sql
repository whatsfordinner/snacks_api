-- :name get_snacks :many
SELECT * FROM snacks

-- :name get_snack :one
SELECT * FROM snacks WHERE id = :snack_id

-- :name get_snack_by_name :one
SELECT * FROM snacks WHERE name = :snack_name

-- :name insert_snack :insert
INSERT INTO snacks (name) VALUES (:snack_name)
