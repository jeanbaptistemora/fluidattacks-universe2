from fa_purity import (
    FrozenList,
)
import os
import pytest
from target_s3.in_buffer import (
    process_buffer,
)
from tempfile import (
    NamedTemporaryFile,
)


def test_process_buffer() -> None:
    test_data = ("This", "is", "a", "test")
    with NamedTemporaryFile(
        "w+", encoding="utf-8", delete=False, buffering=1
    ) as input_file:
        for data in test_data:
            input_file.write(data)
            input_file.write("\n")
        input_file_name = input_file.name
    output_file_name = NamedTemporaryFile(
        "r", encoding="utf-8", delete=False
    ).name

    def _test(data: FrozenList[str]) -> None:
        assert data == test_data

    with pytest.raises(SystemExit):
        try:
            with open(
                input_file_name, "r", encoding="utf-8", buffering=1
            ) as input_buffer:
                with open(
                    output_file_name, "w", encoding="utf-8", buffering=1
                ) as output_buffer:
                    process_buffer(input_buffer, output_buffer, True).map(
                        lambda x: x.strip()
                    ).to_list().map(_test).compute()

        finally:
            os.remove(input_file_name)
            os.remove(output_file_name)
