from singer_io.singer2.json_schema import (
    JsonSchemaFactory,
)
from tap_announcekit.jschema import (
    ObjEncoder,
)
from tap_announcekit.streams.id_objs import (
    ImageId,
    PostId,
    ProjectId,
    UserId,
)

_str_type = JsonSchemaFactory.from_prim_type(str).to_json()
_obj_encoder = ObjEncoder(
    {
        ImageId: _str_type,
        ProjectId: _str_type,
        PostId: _str_type,
        UserId: _str_type,
    }
)


class StreamsObjsEncoder:
    # pylint: disable=too-few-public-methods
    @staticmethod
    def encoder() -> ObjEncoder:
        return _obj_encoder
