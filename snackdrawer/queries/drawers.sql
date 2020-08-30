-- :name get_drawers_by_userid :many
SELECT * FROM drawers WHERE userid = :user_id

-- :name create_new_drawer :insert
INSERT INTO drawers (userid, name) VALUES (:user_id, :drawer_name)

-- :name get_snacks_in_drawer :many
SELECT * FROM snacks WHERE snackid IN (
    SELECT snackid FROM drawercontents WHERE drawerid = :drawer_id
)

-- :name add_snack_to_drawer :insert
INSERT INTO drawercontents (drawerid, snackid) VALUES (:drawer_id, :snack_id)