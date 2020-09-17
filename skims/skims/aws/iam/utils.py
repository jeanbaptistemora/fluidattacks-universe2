# Standard library
import re


def match_pattern(pattern: str, target: str, flags: int = 0) -> bool:
    # Escape everything that is not `*` and replace `*` with regex `.*`
    pattern = r'.*'.join(map(re.escape, pattern.split('*')))

    return bool(re.match(f'^{pattern}$', target, flags=flags))
