# Groups:
handbook_group_order = [
    "co-creation and evolution",
    "peer development",
    "enablers of co-creation",
    "agreements",
    "focussed interactions",
    "meeting practices",
    "organizing work",
    "building organizations",
    "connecting domains",
    "organizational structure",
]

s3_patterns = {
    "co-creation and evolution": [
        "driver",
        "objections",
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
        "governance facilitator",
        "be the change",
        "adopt the seven principles",
        "agree on values",
        "adapt patterns to context",
        "support roles",
        "bylaws",
        "transparent salary",
        "breaking agreements",
        "contracting and accountability",
        "pull-system for organizational change",
        "open S3 adoption",
    ],
    "agreements": [
        "strategy",
        "agreements",
        "logbook",
        "logbook keeper",
        "intended outcome",
        "deliverables",
        "evaluation criteria",
        "domain description",
        "evaluate agreements",
    ],
    "focussed interactions": [
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
    ],
    "connecting domains": [
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
