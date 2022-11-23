from singer_io.file import (
    DataFile,
)
import tempfile


def test_data_file_from_file() -> None:
    # Arrange
    raw_data = ["test data!", "test data 2!"]
    data_file: DataFile
    # Act
    with tempfile.NamedTemporaryFile("w+") as tmp:
        tmp.writelines(raw_data)
        data_file = DataFile.from_file(tmp)
    # Assert
    for index, line in enumerate(data_file.read()):
        assert line == raw_data[index]
