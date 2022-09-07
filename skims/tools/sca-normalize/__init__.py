# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import copy
import glob
import json
import re


def main() -> None:
    for database_path in glob.glob("skims/static/sca/*.json"):
        with open(database_path, encoding="utf-8") as file:
            database = json.load(file)

        database_copy = copy.deepcopy(database)

        # Projects must be lowercase
        for project, vulnerabilities in database.items():
            if project != project.lower():
                database_copy[project.lower()] = database_copy.pop(project)

            # Versions must be lowercase
            for v_id, versions in vulnerabilities.items():
                database_copy[project.lower()][v_id] = " || ".join(
                    sorted(re.split(r"\s*\|\|\s*", versions.lower()))
                )

        with open(database_path, encoding="utf-8", mode="w") as file:
            file.write(json.dumps(database_copy, indent=2, sort_keys=True))
            file.write("\n")


if __name__ == "__main__":
    main()
