from singer_io.singer2.json_schema import (
    JsonSchemaFactory,
)
from tap_announcekit.jschema import (
    ObjEncoder,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    PostId,
    ProjectId,
    UserId,
)

_str_type = JsonSchemaFactory.from_prim_type(str).to_json()
encoder_1 = ObjEncoder(
    {
        ImageId: _str_type,
        ProjectId: _str_type,
        PostId: _str_type,
        UserId: _str_type,
    }
)
