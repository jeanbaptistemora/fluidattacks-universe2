from functools import (
    partial,
)
import glob
import json
import os
from utils.encodings import (
    yaml_dumps_blocking,
)


def main() -> None:
    folder: str = "../androguard"

    suite = dict(
        apk=dict(
            include=sorted(
                map(
                    partial(os.path.relpath, start=folder),
                    glob.iglob(f"{folder}/**/*.apk", recursive=True),
                )
            ),
        ),
        namespace="APK",
        output="skims/test/outputs/lib_apk.csv",
        working_dir=folder,
    )

    with open(
        "skims/test/data/config/lib_apk.yaml", "w", encoding="utf-8"
    ) as file:
        file.write(yaml_dumps_blocking(suite))
        file.write("\n")

    print(json.dumps(suite, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
