# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name

"""
Removes input vulnerabilities reported by Machine
with the specific splitted into two

Execution Time:    TBD
Finalization Time: TBD
"""
from aioextensions import (
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from organizations import (
    domain as orgs_domain,
)
import re
import time
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
)

INPUT_FINDINGS_DESCRIPTIONS: Dict[str, List[str]] = {
    "F024": [
        "Security groups contain RFC-1918 CIDRs open\n",
        "Los grupos de seguridad contienen RFC-1918 CIDRs abiertas\n",
        (
            "Missing egress rules allows all egress traffic, "
            "explicitly define egress rules"
        ),
        (
            "La falta de reglas de salida permite todo el tráfico de salida, "
            "defina explícitamente las reglas de salida\n"
        ),
    ],
    "F031": [
        (
            "Al usuario de IAM se le otorgan privilegios, "
            "pero no a través de un rol"
        ),
        (
            "El grupo de IAM se le otorgan privilegios, "
            "pero no a través de un rol"
        ),
        "Excessive privileges, complete access over all resources",
        "Privilegios excesivos, acceso completo sobre todos los recursos",
        "Excessive privileges, avoid the use of negative statements",
        "Privilegios excesivos, evitar el uso de políticas negativas",
    ],
    "F043": [
        "Missing frame-ancestors",
        "frame-ancestors ausente",
        "Missing object-src",
        "object-src ausente",
        "Missing script-src",
        "script-src ausente",
        "Missing Content-Security-Policy",
        "Content-Security-Policy ausente",
        "block-all-mixed-content is deprecated",
        "block-all-mixed-content esta deprecada",
        "script-src has unsafe-inline",
        "script-src contiene unsafe-inline",
        "Could not found upgrade-insecure-requests header or CSP directive",
        (
            "No se encontró la cabecera upgrade-insecure-requests "
            "ni la directiva CSP"
        ),
    ],
    "F052": [
        (
            "server accepts connections "
            "with weak cipher method {insecure_cipher}, "
            "included in: {v_name}\n"
        ),
        (
            "el servidor acepta conexiones "
            "con el siguiente método de cifrado débil: {insecure_cipher}, "
            "included in: {v_name}\n"
        ),
    ],
    "F071": [
        "Missing Referrer-Policy",
        "Referrer-Policy ausente",
        "The Referrer-Policy header is set to a weak value",
        "La cabecera Referrer-Policy posee un valor debil",
        "Weak Referrer-Policy",
        "Referrer-Policy debil",
    ],
    "F086": [
        (
            "The application does not properly check "
            "the integrity of resources loaded from third-party servers.\n"
        )
    ],
    "F094": [
        (
            "server accepts connections "
            "with weak cipher method: {insecure_cipher}, "
            "that supports CBC in {v_name}\n"
        ),
        (
            "el servidor acepta conexiones "
            "con el método de encripción insegura: {insecure_cipher}, "
            "que soporta CBC en {v_name}\n"
        ),
    ],
    "F131": [
        "Missing Strict-Transport-Security",
        "Strict-Transport-Security ausente",
        "max-age less than 31536000",
        "max-age menor que 31536000",
    ],
    "F132": [
        "Missing X-Content-Type-Options",
        "X-Content-Type-Options ausente",
    ],
}


def get_tls_information(
    description: str,
) -> Tuple[Optional[str], Optional[str]]:
    cipher_regexes = [
        r"cipher method:? ([A-Z0-9_]*)",
        r"cifrado débil: ([A-Z0-9_]*)",
        r"encripción insegura: ([A-Z0-9_]*)",
    ]
    protocol_regexes = [
        r"included in: ([A-Z0-9v\.]*)",
        r"supports CBC in ([A-Z0-9v\.]*)",
        r"soporta CBC en ([A-Z0-9v\.]*)",
    ]

    cipher: Optional[str] = None
    protocol: Optional[str] = None
    for regex in cipher_regexes:
        if match := re.search(regex, description):
            cipher = match.group(1)
            break
    for regex in protocol_regexes:
        if match := re.search(regex, description):
            protocol = match.group(1)
            break
    return cipher, protocol


def get_vulns_with_description_issues(
    f_id: str, vulns: Iterable[Vulnerability]
) -> List[Vulnerability]:
    vulns_with_issues: List[Vulnerability] = []
    finding_key: str = f"F{f_id}"
    descriptions: List[str] = INPUT_FINDINGS_DESCRIPTIONS[finding_key]
    descriptions_splits: List[List[str]] = [
        description.split(",")
        if "," in description
        else description.split("-")
        for description in descriptions
    ]

    for vuln in vulns:
        aux_descriptions: List[str] = descriptions
        aux_descriptions_splits: List[List[str]] = descriptions_splits
        vuln_description = vuln.specific

        if f_id in ["F052", "F094"]:
            cipher, protocol = get_tls_information(vuln_description)
            if cipher is None and protocol is None:
                print(
                    "\t\t" + f"Could not determine SSL information for {vuln}"
                )
                continue
            aux_descriptions = [
                description.replace(
                    "{insecure_cipher}", cipher if cipher is not None else ""
                ).replace("{v_name}", protocol if protocol is not None else "")
                for description in descriptions
            ]
            aux_descriptions_splits = [
                description.split(",")
                if "," in description
                else description.split("-")
                for description in aux_descriptions
            ]

        for idx, description in enumerate(aux_descriptions):
            if vuln_description != description and any(
                vuln_description == split
                for split in aux_descriptions_splits[idx]
            ):
                vulns_with_issues.append(vuln)
                break

    return vulns_with_issues


async def main() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_group_names(loaders)
    groups_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups)
    total_groups: int = len(groups)
    machine_input_findings: List[str] = [
        key[1:] for key in INPUT_FINDINGS_DESCRIPTIONS
    ]

    for idx, (group, findings) in enumerate(zip(groups, groups_findings)):
        print(f"Processing group {group} ({idx+1}/{total_groups})...")
        input_findings: List[Finding] = [
            finding
            for finding in findings
            if any(
                finding.title.startswith(_id) for _id in machine_input_findings
            )
        ]
        if input_findings:
            vulns_to_delete: List[Vulnerability] = []
            input_findings_vulns: Tuple[
                Tuple[Vulnerability, ...], ...
            ] = await loaders.finding_vulnerabilities.load_many(
                [finding.id for finding in input_findings]
            )
            for finding, vulns in zip(input_findings, input_findings_vulns):
                machine_vulns: List[Vulnerability] = [
                    vuln
                    for vuln in vulns
                    if (
                        vuln.state.source == Source.MACHINE
                        and vuln.type == VulnerabilityType.INPUTS
                    )
                ]
                if machine_vulns:
                    vulns_to_delete += get_vulns_with_description_issues(
                        finding.title[:2], machine_vulns
                    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
