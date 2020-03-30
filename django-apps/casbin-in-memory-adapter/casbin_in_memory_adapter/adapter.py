"""In-memory Casbin Adapter."""

# Standard library
from typing import (
    Tuple,
)

# Third parties libraries
import casbin.model
import casbin.persist

# Types
Attribute = str
PolicyType = str
Rule = Tuple[Attribute, ...]
Policy = Tuple[PolicyType, Rule]
Policies = Tuple[Policy, ...]


class Adapter(casbin.persist.Adapter):
    """Casbin adapter interface."""

    def __init__(self, policies: Policies):
        """Init constructor method."""
        self.policies: Policies = policies

    def load_policy(self, model: casbin.model.Model):
        """Load all policy rules from the storage."""
        policy_type: PolicyType
        rule: Rule
        for policy_type, rule in self.policies:
            csv = policy_type + ', '.join(rule)
            casbin.persist.load_policy_line(csv, model)
