from pathlib import (
    Path,
)
import re
import tap_mandrill


def test_forbidden_built_ins() -> None:
    all_modules = Path(tap_mandrill.__file__).parent.rglob("*.py")
    allowed = (Path(tap_mandrill.__file__).parent / "_files",)
    for m in all_modules:
        with open(m, "r", encoding="UTF-8") as module:
            match = re.search("[\n ]open\(", module.read())
            if match and not any(a in m.parents for a in allowed):
                raise Exception(
                    f"Illegal possible call to builtin `open()` at {m}"
                )
