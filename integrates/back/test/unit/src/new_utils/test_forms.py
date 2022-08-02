from newutils.forms import (
    is_exploitable,
)
from numpy import (
    arange,
)


def test_is_exploitable() -> None:
    version = "3.1"
    for exploitability in arange(0.0, 0.96, 0.2):
        assert is_exploitable(exploitability, version) == "No"
    for exploitability in arange(0.97, 2, 0.3):
        assert is_exploitable(exploitability, version) == "Si"
    version = "2"
    exploitble_exploitabilities = [1.0, 0.95]
    for exploitability in exploitble_exploitabilities:
        assert is_exploitable(exploitability, version) == "Si"
    non_exploitable_exploitability = 0.5
    assert is_exploitable(non_exploitable_exploitability, version) == "No"
