#! /usr/bin/env python3

import json
import os
import re
from typing import (
    List,
)
import yaml  # type: ignore

# constants
BASE = "/data/gitlab/gitlab-org/advisories-community"


def maven_parse_ranges(text: str) -> List[str]:
    ranges: List[str] = []
    text = text.replace(" ", "")
    text = text.lower()

    match = re.findall(r"[\(\[].*?[\]\)]", text)

    if not match:
        raise NotImplementedError()

    for range_ in match:
        ranges.append(maven_parse_range(range_))

    return ranges


def maven_parse_range(text: str) -> str:
    match = re.match(
        r"""
            (?P<boundary_left>[\[\(])
            (
                (?P<version_left>.*?)
                (?P<comma>,)
            )?
            (?P<version_right>.*?)
            (?P<boundary_right>[\)|\]])
        """,
        text,
        flags=re.VERBOSE,
    )

    if not match:
        raise NotImplementedError()

    boundary_left = match.group("boundary_left")
    version_left = match.group("version_left")
    comma = match.group("comma")
    version_right = match.group("version_right")
    boundary_right = match.group("boundary_right")

    constraint_left = {"[": ">=", "(": ">"}[boundary_left]
    constraint_right = {"]": "<=", ")": "<"}[boundary_right]

    if (
        boundary_left == "["
        and not version_left
        and not comma
        and version_right
        and boundary_right == "]"
    ):
        return version_right

    if not version_left:
        constraint_left = ">="
        version_left = "0"

    if not version_right:
        constraint_right = ""
        version_right = ""

    text = f"{constraint_left}{version_left} {constraint_right}{version_right}"
    return text.strip()


def maven_yield():
    root = os.path.join(BASE, "maven")
    for group in os.listdir(root):
        group_path = os.path.join(root, group)

        for artifact in os.listdir(group_path):
            artifact_path = os.path.join(group_path, artifact)
            if not os.path.isdir(artifact_path):
                continue

            for vuln in os.listdir(artifact_path):
                vuln_path = os.path.join(artifact_path, vuln)
                with open(vuln_path, encoding="utf-8") as file:
                    vuln_data = yaml.safe_load(file)

                yield f"{group}:{artifact}", vuln_data


def maven(data) -> None:
    for project, vuln_data in maven_yield():
        project = project.lower()

        affected_versions = vuln_data["affected_versions"]
        vuln_ids = vuln_data["identifiers"]
        ranges_raw = vuln_data["affected_range"]

        print("---")
        print(f"project: {project}")
        print(f"affected: {affected_versions}")
        print(f"ranges_raw: {ranges_raw}")
        ranges_parsed = maven_parse_ranges(ranges_raw)
        print(f"ranges_parsed: {ranges_parsed}")
        print(f"vuln_ids: {vuln_ids}")
        for vuln_id in vuln_ids:
            data.setdefault(project, {})
            data[project][vuln_id] = " || ".join(ranges_parsed)

    return data


def npm_yield():
    root = os.path.join(BASE, "npm")
    for namespace in os.listdir(root):
        namespace_path = os.path.join(root, namespace)

        for artifact in os.listdir(namespace_path):
            artifact_path = os.path.join(namespace_path, artifact)

            if os.path.isdir(artifact_path):
                for vuln in os.listdir(artifact_path):
                    vuln_path = os.path.join(artifact_path, vuln)
                    with open(vuln_path, encoding="utf-8") as file:
                        vuln_data = yaml.safe_load(file)

                    yield f"{namespace}/{artifact}", vuln_data
            else:
                with open(artifact_path, encoding="utf-8") as file:
                    vuln_data = yaml.safe_load(file)

                yield namespace, vuln_data


def npm(data):
    for project, vuln_data in npm_yield():
        project = project.lower()

        affected_versions = vuln_data["affected_versions"]
        vuln_ids = vuln_data["identifiers"]
        ranges_raw = vuln_data["affected_range"]
        ranges_raw = re.sub(r"\s+", r" ", ranges_raw)
        ranges_raw = re.sub(r"(>=?)\s+", r"\1", ranges_raw)
        ranges_raw = re.sub(r"(<=?)\s+", r"\1", ranges_raw)
        ranges_raw = re.sub(r"\s*(\|\|)\s*", r" || ", ranges_raw)

        print("---")
        print(f"project: {project}")
        print(f"affected: {affected_versions}")
        print(f"ranges_raw: {ranges_raw}")
        print(f"vuln_ids: {vuln_ids}")
        for vuln_id in vuln_ids:
            data.setdefault(project, {})
            data[project][vuln_id] = " || ".join(
                range if range else ">=0" for range in ranges_raw.split(" || ")
            )

    return data


def nuget_yield():
    root = os.path.join(BASE, "nuget")

    for artifact in os.listdir(root):
        artifact_path = os.path.join(root, artifact)

        for vuln in os.listdir(artifact_path):
            vuln_path = os.path.join(artifact_path, vuln)
            with open(vuln_path, encoding="utf-8") as file:
                vuln_data = yaml.safe_load(file)

            yield artifact, vuln_data


def nuget(data):
    for project, vuln_data in nuget_yield():
        project = project.lower()

        affected_versions = vuln_data["affected_versions"]
        vuln_ids = vuln_data["identifiers"]
        ranges_raw = vuln_data["affected_range"]

        print("---")
        print(f"project: {project}")
        print(f"affected: {affected_versions}")
        print(f"ranges_raw: {ranges_raw}")
        ranges_parsed = maven_parse_ranges(ranges_raw)
        print(f"ranges_parsed: {ranges_parsed}")
        print(f"vuln_ids: {vuln_ids}")
        for vuln_id in vuln_ids:
            data.setdefault(project, {})
            data[project][vuln_id] = " || ".join(ranges_parsed)

    return data


def main() -> None:
    for generator, path in [
        (maven, "skims/static/sca/maven.json"),
        (npm, "skims/static/sca/npm.json"),
        (nuget, "skims/static/sca/nuget.json"),
    ]:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        data = generator(data)

        with open(path, encoding="utf-8", mode="w") as file:
            file.write(json.dumps(data, indent=2, sort_keys=True))
            file.write("\n")


if __name__ == "__main__":
    main()
