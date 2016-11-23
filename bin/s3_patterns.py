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
    "building organizations": [
        "align flow",
        "domain",
        "linking",
        "open systems",
    ],
    "people and roles": [
        "role",
        "role description",
        "role selection",
        "effectiveness review",
        "development plan",
        "support roles",
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
}


def all_patterns():
    """Return a sorted list of all patterns."""
    all_patterns = []
    for group in s3_patterns.keys():
        for pattern in s3_patterns[group]:
            all_patterns.append(pattern)
    return sorted(all_patterns)
