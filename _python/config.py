# TODO: add the seven principles to the handbook

# Renaming process:
# 1. upate new names in both structures above
# 2. add renames to both structures below
# 3. run the rename tool
# 4. regenerate TOCs: python _python/build_patterns.py build --toc


groups_to_rename = [

    ('navigation', 'governance'),
    ('roles', 'people and roles'),
]

patterns_to_rename = [

    ("navigation backlog", "governance meeting"),
    ("navigation meeting", "governance backlog"),
    ('adopt S3 principles', 'adopt the seven principles'),
    ('evaluating decisions', 'evaluate agreements'),
    ('navigation via tensions', 'navigating via tension'),
    ('organizing in circles', 'domain'),
    ('organize in nested domains', 'domain'),
    ('role descriptions', 'role description'),
    ('secretary', 'meeting host'),
]

