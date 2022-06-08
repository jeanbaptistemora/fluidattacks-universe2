from git import (
    Repo,
)
import glob
import json
import tempfile
import yaml


def get_remote_advisories(language: str):
    with tempfile.TemporaryDirectory() as tmp_dirname:
        Repo.clone_from(
            "https://gitlab.com/gitlab-org/advisories-community.git",
            tmp_dirname,
        )
        print(tmp_dirname)
        filenames = sorted(
            glob.glob(f"{tmp_dirname}/{language}/**/*yml", recursive=True)
        )
        advisories: dict = {}
        for filename in filenames:
            with open(filename, "r") as stream:
                try:
                    parsed_yaml = yaml.safe_load(stream)
                    key = filename.replace(
                        f"{tmp_dirname}/{language}/", ""
                    ).replace("/", ":")
                    package_key, cve_key = key.rsplit(":", 1)
                    if package_key not in advisories:
                        advisories.update({package_key: {}})
                    if cve_key not in advisories[package_key]:
                        advisories[package_key].update(
                            {cve_key: parsed_yaml["affected_range"]}
                        )
                except yaml.YAMLError as exc:
                    print(exc)
        with open(f"{language}.json", "w") as outfile:
            json.dump(advisories, outfile, indent=2, sort_keys=True)
