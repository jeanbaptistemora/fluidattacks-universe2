import operator
import re
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.function import (
    RetryAndFinallyReturn,
    shield,
)
from typing import (
    Match,
    Optional,
    Tuple,
)

VALID__SCOPES_DESC: Tuple[Tuple[str, str], ...] = (
    ("enum", "Enumeration of ToE without testing"),
    ("conf", "Configuration files change"),
    ("cross", "Comprehensive (lines and inputs) testing"),
    ("lines", "Source code testing"),
    ("inputs", "Environment/App/Machine testing"),
)
VALID__TYPES_DESC: Tuple[Tuple[str, str], ...] = (
    ("drills", "Drills service related commit"),
)

VALID_SCOPES: Tuple[str, ...] = tuple(
    map(operator.itemgetter(0), VALID__SCOPES_DESC)
)
VALID_TYPES: Tuple[str, ...] = tuple(
    map(operator.itemgetter(0), VALID__TYPES_DESC)
)
VALID_REASONS: Tuple[str, ...] = tuple(
    map(
        lambda r: f"not-drills(cross)-because: {r}",
        (
            "i-already-tested-all-lines",
            "i-already-tested-all-inputs",
            "i-was-increasing-lines-coverage",
            "i-was-increasing-inputs-coverage",
            "toe-has-lines-only",
            "there-is-a-lines-eventuality",
            "there-is-an-inputs-eventuality",
            "inputs-have-no-corresponding-lines",
            "i-think-lines-have-more-vulns-than-inputs",
            "i-think-inputs-have-more-vulns-than-lines",
            "other: ",
        ),
    )
)


def _match_is_valid_summary(body: str, scope: str) -> bool:
    if scope == "cross" or any(reason in body for reason in VALID_REASONS):
        LOGGER.info("Drills daily commit: OK")
        return True
    LOGGER.error("Provide a valid reason for non-cross hack")
    LOGGER.info("Valid reasons are:")
    for reason in VALID_REASONS:
        LOGGER.info("  - %s", reason)
    return False


def _enum_match_is_valid_summary(
    match: Optional[Match[str]], enum_pattern: str
) -> bool:
    if match:
        LOGGER.info("Drills enumeration commit: OK")
        is_valid = True
    else:
        LOGGER.error("Enumeration commit must match: %s", enum_pattern)
        is_valid = False

    return is_valid


def _config_match_is_valid_summary(
    match: Optional[Match[str]], config_pattern: str
) -> bool:
    if match:
        LOGGER.info("Drills config commit: OK")
        return True
    LOGGER.error("Config commit must match: %s", config_pattern)
    return False


@shield(on_error_return=False)
def is_valid_summary(  # noqa: MC0001
    summary: str,
    body: str = str(),
) -> bool:
    """Plugable validator for drills commits."""
    is_valid: bool = True

    # xxx(yyy)
    base_pattern: str = r"^(?P<type>[a-z]+)\((?P<scope>[a-z]+)\)"
    # drills(lines/inputs/cross): continuoustest - 72.75%, 0 el, 6 ei
    daily_pattern: str = base_pattern + (
        r": "
        r"(?P<group>[a-z0-9]+)"
        r" - "
        r"(?P<coverage>\d+\.\d{2}%)"
        r", "
        r"(?P<evaluated_lines>\d+) el"
        r", "
        r"(?P<evaluated_inputs>\d+) ei"
        r"$"
    )
    # drills(enum): continuoustest - 0 nl, 3ni
    enum_pattern: str = base_pattern + (
        r": "
        r"(?P<group>[a-z0-9]+)"
        r" - "
        r"(?P<new_lines>\d+) nl"
        r", "
        r"(?P<new_inputs>\d+) ni"
        r"$"
    )
    # drills(conf): continuoustest - comment, continued
    config_pattern = base_pattern + (
        ": " r"(?P<group>[a-z0-9]+) - (?P<comment>[a-z, _-]+)$"
    )

    match: Optional[Match] = re.match(base_pattern, summary)
    match_groups = match.groupdict() if match else {}
    type_: str = match_groups.get("type", "")
    scope: str = match_groups.get("scope", "")
    if match and type_ in VALID_TYPES and scope in VALID_SCOPES:
        if type_ == "drills" and scope in ("lines", "inputs", "cross"):
            match = re.match(daily_pattern, summary)
            if match:
                is_valid = _match_is_valid_summary(body, scope)
            else:
                LOGGER.error("Daily commit must match: %s", daily_pattern)
                is_valid = False
        elif type_ == "drills" and scope == "enum":
            match = re.match(enum_pattern, summary)
            is_valid = _enum_match_is_valid_summary(match, enum_pattern)
        elif type_ == "drills" and scope == "conf":
            match = re.match(config_pattern, summary)
            is_valid = _config_match_is_valid_summary(match, config_pattern)
        else:
            LOGGER.error("Unrecognized scope: %s(%s)", type_, scope)
            is_valid = False
    else:
        LOGGER.error("Provide a valid commit type(scope)")
        LOGGER.info("Yours is: %s(%s)", type_, scope)
        LOGGER.info("Valid types are:")
        for type_, desc in VALID__TYPES_DESC:
            LOGGER.info("  - %s: %s", type_, desc)
        LOGGER.info("Valid scopes are:")
        for scope, desc in VALID__SCOPES_DESC:
            LOGGER.info("  - %s: %s", scope, desc)
        is_valid = False

    if not is_valid:
        raise RetryAndFinallyReturn(is_valid)

    return is_valid


def is_drills_commit(summary: str) -> bool:
    return "drills(" in summary
