"""Main module to build and check Assert Exploits."""

# Standard library
import datetime
import re
import textwrap
from typing import (
    Any,
    Tuple,
)

# Third parties libraries

# Local libraries

# Compiled regular expresions
RE_SPACE_CHARS = re.compile(r'\s', flags=re.M)
RE_NOT_ALLOWED_CHARS = re.compile(r'[^a-zá-úñÁ-ÚÑA-Z0-9\s,._]', flags=re.M)


def sanitize_string(string: Any) -> str:
    """Sanitize the string to allow only certain values."""
    string = RE_NOT_ALLOWED_CHARS.sub('', str(string)[0:512])
    string = RE_SPACE_CHARS.sub(' ', string)
    string = string.strip()
    return string


def append_finding_title_to_exploit(
    exploit_path: str,
    finding_title: str,
):
    """Append the finding title to an exploit at the beginning."""
    with open(exploit_path) as exploit:
        exploit_content = exploit.read()

    with open(exploit_path, 'w') as exploit:
        exploit.write(textwrap.dedent(
            f"""
            # {datetime.datetime.utcnow()}
            from fluidasserts.utils import generic

            generic.add_finding('{finding_title}')
            del generic

            """)[1:])
        exploit.write(exploit_content)


def _normalize(who: str, where: str) -> Tuple[str, str]:
    """Some checks like has_not_text don't have line number."""
    try:
        int(where)
    except ValueError:
        who = f'{who} [{where}]'
        where = '0'
    return who, where
