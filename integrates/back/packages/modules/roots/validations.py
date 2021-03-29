# Standard
import os
import re
from ipaddress import ip_address
from typing import List
from urllib.parse import ParseResult, unquote_plus, urlparse

# Third party
from git import Git, GitCommandError


def is_exclude_valid(exclude_patterns: List[str], url: str) -> bool:
    is_valid: bool = True

    # Get repository name
    url_obj = urlparse(url)
    url_path = unquote_plus(url_obj.path)
    repo_name = os.path.basename(url_path)
    if repo_name.endswith('.git'):
        repo_name = repo_name[0:-4]

    for pattern in exclude_patterns:
        pattern_as_list: List[str] = pattern.lower().split('/')
        if (
            repo_name in pattern_as_list
            and pattern_as_list.index(repo_name) == 0
        ):
            is_valid = False
    return is_valid


def is_valid_url(url: str) -> bool:
    url_attributes: ParseResult = urlparse(url)

    return bool(url_attributes.netloc and url_attributes.scheme)


def is_valid_git_branch(branch_name: str) -> bool:
    try:
        Git().check_ref_format('--branch', branch_name)
        return True
    except GitCommandError:
        return False


def is_valid_ip(address: str) -> bool:
    try:
        ip_address(address)
        return True
    except ValueError:
        return False


def validate_nickname(nickname: str) -> bool:
    if re.search('/', nickname):
        return False
    return True
