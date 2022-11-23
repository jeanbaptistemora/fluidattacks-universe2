from fa_purity.frozen import (
    freeze,
)
from fa_singer_io.json_schema import (
    JSchemaFactory,
)
from fa_singer_io.singer.encoder import (
    EncodeItem,
    SingerEncoder,
)
from fa_singer_io.singer.schema.core import (
    Property,
)
from tap_checkly.objs import (
    CheckId,
    CheckResultId,
    IndexedObj,
)
from tap_checkly.objs.result import (
    ApiCheckResult,
)
from tap_checkly.singer._core import (
    SingerStreams,
)
from typing import (
    Dict,
    Tuple,
)

_str_type = JSchemaFactory.from_prim_type(str)
_opt_str_type = JSchemaFactory.opt_prim_type(str)
_opt_int_type = JSchemaFactory.opt_prim_type(str)
_opt_float_type = JSchemaFactory.opt_prim_type(float)
ApiCheckResultObj = IndexedObj[Tuple[CheckId, CheckResultId], ApiCheckResult]


def _encoder() -> SingerEncoder[ApiCheckResultObj]:
    _mapper: Dict[str, EncodeItem[ApiCheckResultObj]] = {
        "check_id": EncodeItem.new(
            lambda x: x.id_obj[0].id_str,
            Property(_str_type, True, False),
            ApiCheckResultObj,
        ),
        "result_id": EncodeItem.new(
            lambda x: x.id_obj[1].id_str,
            Property(_str_type, True, False),
            ApiCheckResultObj,
        ),
        "request_error": EncodeItem.new(
            lambda x: x.obj.request_error.value_or(None),
            Property(_opt_str_type, False, False),
            ApiCheckResultObj,
        ),
        "status": EncodeItem.new(
            lambda x: x.obj.response.map(lambda r: r.status).value_or(None),
            Property(_opt_int_type, False, False),
            ApiCheckResultObj,
        ),
        "status_text": EncodeItem.new(
            lambda x: x.obj.response.map(lambda r: r.status).value_or(None),
            Property(_opt_str_type, False, False),
            ApiCheckResultObj,
        ),
        "timings_socket": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timings.map(lambda t: t.socket)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timings_lookup": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timings.map(lambda t: t.lookup)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timings_connect": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timings.map(lambda t: t.connect)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timings_response": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timings.map(lambda t: t.response)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timings_end": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timings.map(lambda t: t.end)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timing_phases_wait": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timing_phases.map(lambda t: t.wait)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timing_phases_dns": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timing_phases.map(lambda t: t.dns)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timing_phases_tcp": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timing_phases.map(lambda t: t.tcp)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timing_phases_first_byte": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timing_phases.map(lambda t: t.first_byte)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timing_phases_download": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timing_phases.map(lambda t: t.download)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
        "timing_phases_total": EncodeItem.new(
            lambda x: x.obj.response.bind(
                lambda r: r.timing_phases.map(lambda t: t.total)
            ).value_or(None),
            Property(_opt_float_type, False, False),
            ApiCheckResultObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_results_api.value, freeze(_mapper)
    )


encoder = _encoder()
