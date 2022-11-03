# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    BrowserCheckResult,
)
from tap_checkly.singer._core import (
    SingerStreams,
)
from typing import (
    Dict,
    Tuple,
)

_str_type = JSchemaFactory.from_prim_type(str)
_int_type = JSchemaFactory.from_prim_type(int)
BrowserCheckResultObj = IndexedObj[
    Tuple[CheckId, CheckResultId], BrowserCheckResult
]


def encoder() -> SingerEncoder[BrowserCheckResultObj]:
    _mapper: Dict[str, EncodeItem[BrowserCheckResultObj]] = {
        "check_id": EncodeItem.new(
            lambda x: x.id_obj[0].id_str,
            Property(_str_type, True, False),
            BrowserCheckResultObj,
        ),
        "result_id": EncodeItem.new(
            lambda x: x.id_obj[1].id_str,
            Property(_str_type, True, False),
            BrowserCheckResultObj,
        ),
        "framework": EncodeItem.new(
            lambda x: x.obj.framework,
            Property(_str_type, False, False),
            BrowserCheckResultObj,
        ),
        "runtime_ver": EncodeItem.new(
            lambda x: x.obj.runtime_ver,
            Property(_str_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_console_errors": EncodeItem.new(
            lambda x: x.obj.summary.console_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_network_errors": EncodeItem.new(
            lambda x: x.obj.summary.network_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_document_errors": EncodeItem.new(
            lambda x: x.obj.summary.document_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_user_script_errors": EncodeItem.new(
            lambda x: x.obj.summary.user_script_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_results_browser.value, freeze(_mapper)
    )
