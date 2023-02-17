import json


def unsafe_print(some_input: str) -> None:
    message = "Variable"
    print(json.dumps(some_input))
    print(f"Have {message} concatenation")


def safe_print() -> None:
    print("Regular info that should not be marked as vuln")
