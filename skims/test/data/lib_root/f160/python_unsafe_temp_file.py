# pylint: skip-file
import tempfile


def unsafe_tempfile() -> None:
    filename = tempfile.mktemp()  # Noncompliant
    open(filename, "w+")


def safe_tempfile() -> None:
    # Compliant; Easy replacement to tempfile.mktemp()
    tmp_file1 = tempfile.NamedTemporaryFile(delete=False)
    tmp_file2 = tempfile.NamedTemporaryFile()
    open(tmp_file1, "w+")
    open(tmp_file2, "w+")
