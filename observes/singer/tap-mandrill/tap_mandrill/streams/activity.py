from fa_purity import (
    Cmd,
    PureIter,
)
from fa_purity.utils import (
    raise_exception,
)
from tap_mandrill._files import (
    CsvFile,
    StrFile,
)
from tap_mandrill.api.export import (
    ExportApi,
)
from tap_mandrill.api.objs.activity import (
    Activity,
)


def all_activity(client: ExportApi) -> Cmd[PureIter[Activity]]:
    data: Cmd[StrFile] = (
        client.export_activity.bind(
            lambda j: client.until_finish(j, 60 * 1, 30)
        )
        .bind(lambda r: r.map(client.download).alt(raise_exception).unwrap())
        .map(lambda r: r.alt(raise_exception).unwrap())
    )
    return data.map(CsvFile.read_dicts).map(
        lambda p: p.map(
            lambda r: r.bind(Activity.decode).alt(raise_exception).unwrap()
        )
    )
