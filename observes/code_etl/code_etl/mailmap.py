from code_etl.objs import (
    User,
)
from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenDict,
    FrozenList,
)
import re
from returns.maybe import (
    Maybe,
)
from typing import (
    Pattern,
)

Alias = User


@dataclass(frozen=True)
class MailmapItem:
    canon: User
    alias: User

    def encode(self) -> str:
        return (
            f"{self.canon.name} <{self.canon.email}>"
            f" {self.alias.name} <{self.alias.email}>"
        )


@dataclass(frozen=True)
class Mailmap:
    alias_map: FrozenDict[Alias, User]


class MailmapFactory:
    @staticmethod
    def from_line(line: str) -> Maybe[MailmapItem]:
        mailmap_line: Pattern = re.compile(
            r"^(?P<canon_name>[A-Z][a-z]+ [A-Z][a-z]+) "
            r"<(?P<canon_email>.*)> "
            r"(?P<alias_name>.*?) "
            r"<(?P<alias_email>.*?)>$",
        )
        match = Maybe.from_optional(mailmap_line.match(line))
        return match.map(lambda m: m.groupdict()).map(
            lambda i: MailmapItem(
                User(i["canon_name"], i["canon_email"]),
                User(i["alias_name"], i["alias_email"]),
            )
        )

    @classmethod
    def from_lines(cls, lines: FrozenList[str]) -> Mailmap:
        mailmap_dict = {}
        for line in lines:
            item = cls.from_line(line).value_or(None)
            if item:
                if item.canon != item.alias:
                    mailmap_dict[item.alias] = item.canon
        return Mailmap(FrozenDict(mailmap_dict))

    @classmethod
    def from_file_path(cls, mailmap_path: str) -> Mailmap:
        with open(mailmap_path, encoding="UTF-8") as file:
            return cls.from_lines(tuple(file.read().splitlines()))
