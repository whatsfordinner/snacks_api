-- :name get_drawers_by_userid :many
SELECT * FROM drawers WHERE userid = :user_id

-- :name get_drawers_by_name :many
SELECT * FROM drawers WHERE name = :drawer_name

-- :name get_drawer_by_id_and_userid :one
SELECT id, name FROM drawers WHERE userid = :user_id AND id = :drawer_id

-- :name get_drawer_by_name_and_userid :one
SELECT id, name FROM drawers WHERE userid = :user_id AND name = :drawer_name

-- :name create_new_drawer :insert
INSERT INTO drawers (userid, name) VALUES (:user_id, :drawer_name)

-- :name get_snacks_in_drawer :many
SELECT * FROM snacks WHERE id IN (
    SELECT snackid FROM drawercontents WHERE drawerid = :drawer_id
)

-- :name add_snack_to_drawer :insert
INSERT INTO drawercontents (drawerid, snackid) VALUES (:drawer_id, :snack_id)