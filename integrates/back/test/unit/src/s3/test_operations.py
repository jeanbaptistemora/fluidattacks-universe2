import os
from s3.operations import (
    upload_memory_file,
)
from starlette.datastructures import (
    UploadFile,
)

BUCKET_NAME = "test_bucket"


async def test_upload_memory_file() -> None:
    file_name = "test-file-records.csv"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data.name, data, "text/csv")
        await upload_memory_file(test_file, file_name, BUCKET_NAME)
