from code_etl.mailmap import (
    MailmapFactory,
    MailmapItem,
)
from code_etl.objs import (
    User,
)

original = User("Super User", "root@foo.com")
alias = User("Super Alias", "root-alias3@foo3.com")
alias2 = User("Termi Nator", "termi@matrix.skynet")
items = (
    MailmapItem(original, alias),
    MailmapItem(original, alias2),
)


def test_from_lines() -> None:
    mailmap = MailmapFactory.from_lines(tuple(i.encode() for i in items))
    print(mailmap.alias_map)
    assert mailmap.alias_map[alias] == original
    assert mailmap.alias_map[alias2] == original
