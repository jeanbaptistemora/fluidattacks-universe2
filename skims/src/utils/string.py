# Standard library
from difflib import SequenceMatcher


def are_similar(string_a: str, string_b: str, threshold: float = 0.85) -> bool:
    return SequenceMatcher(None, string_a, string_b).ratio() >= threshold
