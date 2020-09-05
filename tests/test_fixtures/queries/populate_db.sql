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

-- :name populate_users
INSERT INTO users (username, password_hash) VALUES (
    'foobar',
    '$6$rounds=656000$DA2b7/HB7pXEwOUS$jW9EAxnXxG6Oj6prBoXh8p2dJNQYSKGgRu5xaYf6Z49bITqcF3/Yzf0YAjmpjTLPOErXyq7PZ6HLDprxhBO3s1'
),
(
    'xyzzy',
    '$6$rounds=656000$V4Rw6qjBE7BgJgJF$/xQMjQzFsl3l62PJj9ddsYDCJOwg7em8R5Q3eqgBC5J/x6ys66go4AkVSonKsvczjMpCJmLR7xoYOzDDq8jZu.'
)

-- :name populate_drawers
INSERT INTO drawers (name, userid) VALUES (
    'foo',
    1
),
(
    'bar',
    1
),
(
    'baz',
    2
)

-- :name populate_drawercontents
INSERT INTO drawercontents (drawerid, snackid) VALUES (
    1,
    1
),
(
    1,
    3
),
(
    3,
    2
)