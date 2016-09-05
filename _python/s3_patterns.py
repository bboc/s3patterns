#!/usr/bin/env python

# Groups:
handbook_group_order = [
    "making and evolving agreements",
    "governance",
    "effective meetings",
    "coordinating work",
    "building organizations",
    "people and roles",
    "organizational structure",
    "alignment",
    "bringing in S3 patterns",
]

s3_patterns = {
    "alignment": [
        "adopt the seven principles",
        "agree on values",
        "transparent salary",
        "contracting and accountability",
        "bylaws",
    ],
    "bringing in S3 patterns": [
        "pull-system for organizational change",
        "adapt patterns to context",
        "driver mapping",
        "continuous improvement of work process",
        "open S3 adoption",
        "be the change",
    ],
    "building organizations": [
        "align flow",
        "organize in nested domains",
        "linking",
        "open systems",
    ],
    "coordinating work": [
        "prioritized backlog",
        "visualize work",
        "pull-system for work",
        "daily standup",
        "retrospective",
        "planning and review meetings",
        "coordination meeting",
        "coordinator role",
    ],
    "effective meetings": [
        "rounds",
        "artful participation",
        "meeting facilitation",
        "meeting evaluation",
        "S3 facilitator",
        "logbook",
        "logbook keeper",
        "meeting host",
    ],
    "making and evolving agreements": [
        "agreements",
        "those affected decide",
        "driver",
        "circle",
        "objections",
        "consent decision making",
        "resolve objections",
        "proposal forming",
        "strategy",
        "evaluate agreements",
        "intended outcome",
        "deliverables",
        "evaluation criteria",
        "qualifying drivers",
    ],
    "governance": [
        "governance backlog",
        "governance meeting",
        "navigating via tension",
    ],
    "organizational structure": [
        "representative",
        "double linking",
        "delegate circle",
        "coordination circle",
        "service circle",
        "nested circle",
        "helping circle",
        "double-linked hierarchy",
        "peach organization",
        "backbone organization",
        "fractal organization",
    ],
    "people and roles": [
        "role",
        "role description",
        "role selection",
        "effectiveness review",
        "development plan",
        "support roles",
    ],
}


# TODO: add the seven principles to the handbook

# Renaming process:
# 1. upate new names in both structures above
# 2. add renames to both structures below
# 3. run the rename tool


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
    ('organizing in circles', 'organize in nested domains'),
    ('role descriptions', 'role description'),
    ('secretary', 'meeting host'),
]


def all_patterns():
    """Return a sorted list of all patterns."""
    all_patterns = []
    for group in s3_patterns.keys():
        for pattern in s3_patterns[group]:
            all_patterns.append(pattern)
    return sorted(all_patterns)
