from tap_announcekit.api.gql_schema import (
    PostContent as RawPostContent,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.post_contents import (
    _encode,
    _factory,
)
from tests.stream import (
    mock_data,
)


def test_queries() -> None:
    mock_post = PostId(ProjectId("1234"), "4321")
    _factory.PostContentQuery(mock_post).query().operation()


def test_schema() -> None:
    encoder = _encode.PostContentEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_post_content_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())


def test_from_raw() -> None:
    mock_raw = {
        "post_id": "",
        "locale_id": "",
        "title": "",
        "body": "",
        "slug": "",
        "url": "",
    }
    _factory.from_raw(ProjectId("1234"), RawPostContent(mock_raw))
