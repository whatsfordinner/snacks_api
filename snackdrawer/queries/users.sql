-- :name get_user :one
SELECT * FROM users WHERE id = :user_id

-- :name get_user_no_hash :one
SELECT id,username FROM users WHERE id = :user_id

-- :name get_user_by_username :one
SELECT * FROM users WHERE username = :username

-- :name get_user_by_username_no_hash :one
SELECT id,username FROM users WHERE username = :username

-- :name insert_user :insert
INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)

-- :name update_password
UPDATE users SET password_hash = :password_hash WHERE id = :user_id