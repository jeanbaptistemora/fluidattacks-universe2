from dynamo_etl_conf.core import (
    SEGMENTATION,
    TargetTables,
)


def test_completeness() -> None:
    for t in TargetTables:
        assert SEGMENTATION[t]
