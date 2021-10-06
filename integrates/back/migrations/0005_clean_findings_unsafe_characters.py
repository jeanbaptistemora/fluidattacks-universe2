#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration browses through the findings and removes the unsafe characters
introduced by the Google spreadsheet that autocompletes the finding information

Execution Time: 2020-05-29 22:03 UTC-5
Finalization Time: 2020-05-29 22:24 UTC-5
"""

import argparse
import bugsnag
from collections import (
    OrderedDict,
)
from findings.dal import (
    TABLE_NAME as FINDINGS_TABLE,
)
import hashlib
import re
from typing import (
    Dict,
    List,
    Optional,
)

STRINGS_TO_REPLACE: Dict[str, Dict[str, str]] = {
    "vulnerability": OrderedDict(
        {
            "**Especificar": "__Especificar",
            "IP's": "direcciones IP",
            "'catch'": "_catch_",
            "'Exception'": "_Exception_",
            "'ValueError'": "_ValueError_",
            "'ConnectionError'": "_ConnectionError_",
            "'NullPointerException'": "_NullPointerException_",
            "'catch Exception'": "_catch Exception_",
            '"+"': "(signo más)",
            '"usuario@ejemplo.com"': "usuario@ejemplo.com",
            '"usuario+1@ejemplo.com"': "usuario(signo más)1@ejemplo.com",
            '"usuario+2000@ejemplo.com"': "usuario(signo más)2000@ejemplo.com",
            '"."': "(punto)",
            "'catch statement'": "_catch statement_",
        }
    ),
    "effect_solution": OrderedDict(
        {
            "Usar autocomplete=off": "Deshabilitar el campo _autocomplete_",
            "JavaScript's LocalStorage": "LocalStorage en JavaScript",
            "rel=noopener": "el atributo _rel_ con el valor _noopener_",
            "HTTPS + TLS": "HTTPS utilizando TLS",
            "SRTP + TLS": "SRTP y TLS",
        }
    ),
}
STRING_REGEX: str = (
    r"^[\^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ \\t\\n\\r\\x0b\\x0c(),./:;@_\$#-]*$"
)


def clean_unsafe_characters(finding: Dict[str, str], dry_run: bool) -> None:
    finding_id = finding["finding_id"]
    original_description = finding.get("vulnerability", "")
    original_recommendation = finding.get("effect_solution", "")

    new_description = replace_unsafe_strings(
        original_description, "vulnerability"
    )
    new_recommendation = replace_unsafe_strings(
        original_recommendation, "effect_solution"
    )

    info_to_update: Dict[str, Optional[str]] = {}
    for field, values in {
        "vulnerability": [original_description, new_description],
        "effect_solution": [original_recommendation, new_recommendation],
    }.items():
        if values[0] != values[1]:
            info_to_update.update(
                {
                    field + "_new": values[1],
                    field
                    + "_hash": hashlib.sha512(values[0].encode()).hexdigest(),
                }
            )

    if info_to_update:
        if dry_run:
            print(f"Changes in finding {finding_id}\n\t{info_to_update}")
        else:
            update_finding(finding_id, info_to_update)
            log(
                f"Migration 0005: fields "
                f'{", ".join(list(info_to_update.keys()))} '
                f"were updated in finding {finding_id}",
                dry_run,
            )


def get_all_findings() -> List[Dict[str, str]]:
    response = FINDINGS_TABLE.scan(
        ProjectionExpression=(
            "finding_id,effect_solution,effect_solution_new,"
            "effect_solution_hash,vulnerability,vulnerability_new,"
            "vulnerability_hash"
        )
    )
    items: List[Dict[str, str]] = response["Items"]
    while response.get("LastEvaluatedKey"):
        response = FINDINGS_TABLE.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            ProjectionExpression=(
                "finding_id,effect_solution,effect_solution_new,"
                "effect_solution_hash,vulnerability,vulnerability_new,"
                "vulnerability_hash"
            ),
        )
        items += response["Items"]
    return items


def persist_changes(finding: Dict[str, str], dry_run: bool) -> None:
    info_to_update: Dict[str, Optional[str]] = {
        "effect_solution_hash": None,
        "effect_solution_new": None,
        "vulnerability_hash": None,
        "vulnerability_new": None,
    }
    finding_id = finding["finding_id"]
    current_description_hash = hashlib.sha512(
        finding.get("vulnerability", "").encode()
    ).hexdigest()
    current_recommendation_hash = hashlib.sha512(
        finding.get("effect_solution", "").encode()
    ).hexdigest()
    old_description_hash = finding.get("vulnerability_hash", "")
    old_recommendation_hash = finding.get("effect_solution_hash", "")

    for field, hashes in {
        "vulnerability": [old_description_hash, current_description_hash],
        "effect_solution": [
            old_recommendation_hash,
            current_recommendation_hash,
        ],
    }.items():
        if hashes[0]:
            if hashes[0] != hashes[1]:
                field_value = replace_unsafe_strings(finding[field], field)
            else:
                field_value = finding[field + "_new"]
            info_to_update.update({field: field_value})

    if dry_run:
        print(f"Changes in finding {finding_id}\n\t{info_to_update}")
    else:
        update_finding(finding_id, info_to_update)
        log(
            f"Migration 0005: changes were applied to finding {finding_id}",
            dry_run,
        )


def replace_unsafe_strings(original_string: str, field: str) -> str:
    safe_string = original_string
    for tainted_string, clean_string in STRINGS_TO_REPLACE[field].items():
        if tainted_string in safe_string:
            safe_string = safe_string.replace(tainted_string, clean_string)
    if safe_string != original_string and not re.match(
        STRING_REGEX, safe_string
    ):
        print(f"Missing unsafe characters in {safe_string}")
    return safe_string


def log(message: str, dry_run: bool) -> None:
    if not dry_run:
        bugsnag.notify(Exception(message), severity="info")


def update_finding(finding_id: str, data: Dict[str, Optional[str]]) -> bool:
    success = False
    primary_keys = {"finding_id": finding_id}
    attrs_to_remove = [attr for attr in data if data[attr] is None]
    for attr in attrs_to_remove:
        response = FINDINGS_TABLE.update_item(
            Key=primary_keys,
            UpdateExpression="REMOVE #attr",
            ExpressionAttributeNames={"#attr": attr},
        )
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
        del data[attr]

    if data:
        attributes = [f"{attr} = :{attr}" for attr in data]
        values = {f":{attr}": data[attr] for attr in data}

        response = FINDINGS_TABLE.update_item(
            Key=primary_keys,
            UpdateExpression=f'SET {",".join(attributes)}',
            ExpressionAttributeValues=values,
        )
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", required=False, action="store_true")
    ap.add_argument("--execute", required=False, action="store_true")

    args: Dict[str, bool] = vars(ap.parse_args())
    dry_run_flag: bool = args["dry_run"]
    execute_flag: bool = args["execute"]

    log(
        "Starting migration 0005 to clean unsafe characters from "
        "autocompleted fields.",
        dry_run_flag,
    )

    for finding_to_process in get_all_findings():
        if execute_flag:
            if finding_to_process.get(
                "vulnerability_new", ""
            ) or finding_to_process.get("effect_solution_new", ""):
                persist_changes(finding_to_process, dry_run_flag)
        else:
            clean_unsafe_characters(finding_to_process, dry_run_flag)
