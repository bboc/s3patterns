# TODO: add the seven principles to the handbook

# Renaming process:
# 1. upate new names in both structures above
# 2. add renames to both structures below
# 3. run the rename tool
# 4. regenerate TOCs: python bin/build_patterns.py build --toc


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


additional_texts_for_handbook = [

 	('introduction.md', 1),
    ('seven-principles.md', 2),
 	('s3-in-a-nutshell.md', 1),
    ('changelog.md', 2),
]

additional_content_to_export = ['introduction', 'changelog']

artefacts_to_export = [
    '_DROPBOX_WORKFLOW.md',
    '_TODO.md',
    'README.md',
    'S3-patterns-handbook.epub',
    'S3-patterns-handbook.pdf',
]

MD_FILE_TEMPLATE = "%s.md"
