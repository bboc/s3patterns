# Groups:
handbook_group_order = [
    "co-creation and evolution",
    "peer development",
    "enablers of co-creation",
    "defining agreements",
    "focused interactions",
    "meeting practices",
    "organizing work",
    "building organizations",
    "organizational structure",
]

s3_patterns = {
    "co-creation and evolution": [
        "driver",
        "objection",
        "navigating via tension",
        "qualifying organizational drivers",
        "proposal forming",
        "consent decision making",
        "resolve objections",
        "those affected decide",
        "role selection",
        "driver mapping",
    ],
    "peer development": [
        "ask for help",
        "peer feedback",
        "effectiveness review",
        "development plan",
    ],
    "enablers of co-creation": [
        "artful participation",
        "be the change",
        "adopt the seven principles",
        "evaluate agreements",
        "pull in S3",
        "pull-system for organizational change",
        "adapt patterns to context",
        "agree on values",
        "governance facilitator",
        "bylaws",
        "contracting and accountability",
        "transparent salary",
        "breaking agreements",
        "support roles",
        "open S3 adoption",
    ],
    "defining agreements": [
        "strategy",
        "agreements",
        "logbook",
        "logbook keeper",
        "intended outcome",
        "describing deliverables",
        "evaluation criteria",
        "domain description",
    ],
    "focused interactions": [
        "governance meeting",
        "retrospective",
        "daily standup",
        "planning and review meetings",
        "coordination meeting",
    ],
    "meeting practices": [
        "rounds",
        "meeting facilitation",
        "meeting evaluation",
        "meeting host",
        "governance backlog",
    ],
    "organizing work": [
        "visualize work",
        "operations backlog",
        "prioritized backlog",
        "pull-system for work",
        "limit work in progress",
        "continuous improvement of work process",
        "align flow",
        "coordinator role",
    ],
    "building organizations": [
        "domain",
        "circle",
        "role",
        "nested domains",
        "linking",
        "double linking",
        "representative",
    ],
    "organizational structure": [
        "delegate circle",
        "service circle",
        "helping team",
        "coordination circle",
        "peach organization",
        "double-linked hierarchy",
        "backbone organization",
        "fractal organization",
        "open systems",
    ],
}


def all_patterns():
    """Return a sorted list of all patterns."""
    all_patterns = []
    for group in s3_patterns.keys():
        for pattern in s3_patterns[group]:
            all_patterns.append(pattern)
    return sorted(all_patterns)
