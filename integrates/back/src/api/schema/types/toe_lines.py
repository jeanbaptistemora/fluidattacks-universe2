from api.resolvers.toe_lines import (
    attacked_at,
    attacked_by,
    attacked_lines,
    be_present,
    be_present_until,
    comments,
    first_attack_at,
    has_vulnerabilities,
    last_author,
    last_commit,
    loc,
    modified_date,
    root,
    seen_at,
    sorts_risk_level,
    sorts_suggestions,
)
from ariadne import (
    ObjectType,
)

TOELINES = ObjectType("ToeLines")
TOELINES.set_field("attackedAt", attacked_at.resolve)
TOELINES.set_field("attackedBy", attacked_by.resolve)
TOELINES.set_field("attackedLines", attacked_lines.resolve)
TOELINES.set_field("bePresent", be_present.resolve)
TOELINES.set_field("bePresentUntil", be_present_until.resolve)
TOELINES.set_field("comments", comments.resolve)
TOELINES.set_field("firstAttackAt", first_attack_at.resolve)
TOELINES.set_field("hasVulnerabilities", has_vulnerabilities.resolve)
TOELINES.set_field("lastAuthor", last_author.resolve)
TOELINES.set_field("lastCommit", last_commit.resolve)
TOELINES.set_field("loc", loc.resolve)
TOELINES.set_field("modifiedDate", modified_date.resolve)
TOELINES.set_field("root", root.resolve)
TOELINES.set_field("seenAt", seen_at.resolve)
TOELINES.set_field("sortsSuggestions", sorts_suggestions.resolve)
TOELINES.set_field("sortsRiskLevel", sorts_risk_level.resolve)
