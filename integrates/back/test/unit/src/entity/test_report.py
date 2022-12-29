from context import (
    STARTDIR,
)
import os
import pytest

pytestmark = pytest.mark.asyncio


def test_pdf_paths() -> None:
    # secure_pdf.py paths
    base = f"{STARTDIR}/integrates/back/src/reports"
    secure_pdf_paths = [
        base,
        f"{base}/results/results_pdf/",
        f"{base}/resources/themes/watermark_integrates_en.pdf",
        f"{base}/resources/themes/overlay_footer.pdf",
    ]

    for path in secure_pdf_paths:
        assert os.path.exists(path), f"path: {path} is not valid"

    # pdf.py paths
    path = f"{STARTDIR}/integrates/back/src/reports"
    pdf_paths = [
        path,
        f"{path}/resources/fonts",
        f"{path}/resources/themes",
        f"{path}/results/results_pdf/",
        f"{path}/templates/pdf/executive.adoc",
        f"{path}/templates/pdf/tech.adoc",
        f"{path}/tpls/",
    ]

    for path in pdf_paths:
        assert os.path.exists(path), f"path: {path} is not valid"
