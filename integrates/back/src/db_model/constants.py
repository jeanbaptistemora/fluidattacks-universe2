from decimal import (
    Decimal,
)

DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")
DEFAULT_VULNERABILITY_GRACE_PERIOD = int(0)
DEFAULT_INACTIVITY_PERIOD = int(90)
POLICIES_FORMATTED = {
    "inactivity_period": (
        "Number of days to remove a stakeholder from the organization "
        "due to inactivity"
    ),
    "max_acceptance_days": (
        "Maximum number of calendar days a finding "
        "can be temporarily accepted"
    ),
    "max_acceptance_severity": (
        "Maximum temporary CVSS 3.1 score for the range "
        "within which a finding can be accepted"
    ),
    "min_breaking_severity": (
        "Minimum CVSS 3.1 score of an open "
        "vulnerability for the DevSecOps agent "
        "to break the build in strict mode"
    ),
    "min_acceptance_severity": (
        "Minimum temporary CVSS 3.1 score for the range "
        "within which a finding can be accepted"
    ),
    "vulnerability_grace_period": (
        "Grace period in days where newly "
        "reported vulnerabilities won't break the build (DevSecOps only)"
    ),
    "max_number_acceptances": (
        "Maximum number of times a finding can be temporarily accepted"
    ),
}
