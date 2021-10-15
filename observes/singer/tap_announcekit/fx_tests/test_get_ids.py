from tap_announcekit.api.auth import (
    get_creds,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.streams.posts._factory import (
    PostIdFactory,
)


def test_get_ids() -> None:
    client = ApiClient(get_creds())
    getter = PostIdFactory(client, ProjectId("11264"))
    getter.get_ids()
