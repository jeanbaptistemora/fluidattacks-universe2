import copy
import glob
import json


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
                database_copy[project.lower()][v_id] = [
                    version.lower() for version in versions
                ]

        with open(database_path, encoding="utf-8", mode="w") as file:
            file.write(json.dumps(database_copy, indent=2, sort_keys=True))
            file.write("\n")


if __name__ == "__main__":
    main()
