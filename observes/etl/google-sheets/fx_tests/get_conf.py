from google_sheets_etl.bin_sdk.tap import (
    decode_conf,
    TapConfig,
)
from google_sheets_etl.utils.cache import (
    Cache,
)
from google_sheets_etl.utils.get_secret import (
    get_secret,
)
from pathlib import (
    Path,
)

_cache: Cache[TapConfig] = Cache(None)


def get_conf() -> TapConfig:
    return _cache.get_or_set(
        get_secret(Path("./secrets/conf.json")).map(
            lambda j: decode_conf(j).unwrap()
        )
    )
