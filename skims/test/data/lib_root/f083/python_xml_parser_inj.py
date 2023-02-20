# pylint: skip-file
from lxml import (
    etree,
)

CONFIG_VAL = True


def main_unsafe() -> None:
    # Noncompliant: by default resolve_entities is set to true
    etree.XMLParser()
    etree.XMLParser(resolve_entities=CONFIG_VAL)


def main_safe() -> None:
    config_val = False
    etree.XMLParser(resolve_entities=config_val)  # Compliant
