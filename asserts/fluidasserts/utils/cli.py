#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""Asserts CLI."""


import argparse
from colorama import (
    init,
)
import contextlib
import fluidasserts
from fluidasserts import (
    CLOSED,
    ERROR,
    OPEN,
    UNKNOWN,
)
from fluidasserts.utils import (
    constants,
)
import importlib
from io import (
    StringIO,
)
import itertools
from multiprocessing import (
    cpu_count,
    Pool,
)
import os
from pygments import (
    highlight,
)
from pygments.formatters import (
    TerminalFormatter,
)
from pygments.lexers import (
    PropertiesLexer,
)
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    String,
    Token,
    Whitespace,
)
from pygments.util import (
    UnclosingTextIOWrapper,
)
import re
import sys
import textwrap
from timeit import (
    default_timer as timer,
)
from typing import (
    Dict,
    List,
    Tuple,
)
import yaml

# pylint: disable=no-name-in-module
# pylint: disable=global-statement
# pylint: disable=exec-used
# pylint: disable=too-many-lines


OUTFILE = sys.stdout

DEF_EXIT_CODES: Dict[str, int] = {
    "closed": 0,
    "open": 1,
    "unknown": 0,
    "config-error": 78,
    "exploit-error": 0,
    "exploit-not-found": 0,
}

RICH_EXIT_CODES: Dict[str, int] = {
    "closed": 0,
    "open": 101,
    "unknown": 102,
    "config-error": 78,
    "exploit-error": 103,
    "exploit-not-found": 104,
}

EXIT_CODES: Dict[str, int] = DEF_EXIT_CODES

OPEN_COLORS = {
    Token: ("", ""),
    Whitespace: ("gray", "gray"),
    Comment: ("red", "red"),
    Comment.Preproc: ("red", "red"),
    Keyword: ("blue", "blue"),
    Keyword.Type: ("cyan", "turquoise"),
    Operator.Word: ("purple", "fuchsia"),
    Name.Builtin: ("cyan", "turquoise"),
    Name.Function: ("green", "green"),
    Name.Namespace: ("_teal_", "_turquoise_"),
    Name.Class: ("_green_", "_green_"),
    Name.Exception: ("cyan", "turquoise"),
    Name.Decorator: ("gray", "gray"),
    Name.Variable: ("red", "red"),
    Name.Constant: ("red", "red"),
    Name.Attribute: ("gray", "gray"),
    Name.Tag: ("blue", "blue"),
    String: ("red", "red"),
    Number: ("red", "red"),
    Generic.Deleted: ("red", "red"),
    Generic.Inserted: ("green", "green"),
    Generic.Heading: ("**", "**"),
    Generic.Subheading: ("*purple*", "*fuchsia*"),
    Generic.Prompt: ("**", "**"),
    Generic.Error: ("red", "red"),
    Error: ("red", "red"),
}

CLOSE_COLORS = {
    Token: ("", ""),
    Whitespace: ("gray", "gray"),
    Comment: ("gray", "gray"),
    Comment.Preproc: ("cyan", "turquoise"),
    Keyword: ("blue", "blue"),
    Keyword.Type: ("cyan", "turquoise"),
    Operator.Word: ("purple", "fuchsia"),
    Name.Builtin: ("cyan", "turquoise"),
    Name.Function: ("green", "green"),
    Name.Namespace: ("_teal_", "_turquoise_"),
    Name.Class: ("_green_", "_green_"),
    Name.Exception: ("cyan", "turquoise"),
    Name.Decorator: ("gray", "gray"),
    Name.Variable: ("red", "red"),
    Name.Constant: ("red", "red"),
    Name.Attribute: ("gray", "gray"),
    Name.Tag: ("blue", "blue"),
    String: ("*green*", "*green*"),
    Number: ("*green*", "*green*"),
    Generic.Deleted: ("red", "red"),
    Generic.Inserted: ("green", "green"),
    Generic.Heading: ("**", "**"),
    Generic.Subheading: ("*purple*", "*fuchsia*"),
    Generic.Prompt: ("**", "**"),
    Generic.Error: ("red", "red"),
    Error: ("*green*", "*green*"),
}

UNKNOWN_COLORS = {
    Token: ("", ""),
    Whitespace: ("gray", "gray"),
    Comment: ("gray", "gray"),
    Comment.Preproc: ("cyan", "turquoise"),
    Keyword: ("blue", "blue"),
    Keyword.Type: ("cyan", "turquoise"),
    Operator.Word: ("purple", "fuchsia"),
    Name.Builtin: ("cyan", "turquoise"),
    Name.Function: ("green", "green"),
    Name.Namespace: ("_teal_", "_turquoise_"),
    Name.Class: ("_green_", "_green_"),
    Name.Exception: ("cyan", "turquoise"),
    Name.Decorator: ("gray", "gray"),
    Name.Variable: ("red", "red"),
    Name.Constant: ("red", "red"),
    Name.Attribute: ("gray", "gray"),
    Name.Tag: ("blue", "blue"),
    String: ("*cyan*", "*cyan*"),
    Number: ("*cyan*", "*cyan*"),
    Generic.Deleted: ("red", "red"),
    Generic.Inserted: ("green", "green"),
    Generic.Heading: ("**", "**"),
    Generic.Subheading: ("*purple*", "*fuchsia*"),
    Generic.Prompt: ("**", "**"),
    Generic.Error: ("red", "red"),
    Error: ("*cyan*", "*cyan*"),
}

SUMMARY_COLORS = {
    Token: ("", ""),
    Whitespace: ("gray", "gray"),
    Comment: ("gray", "gray"),
    Comment.Preproc: ("cyan", "turquoise"),
    Keyword: ("blue", "blue"),
    Keyword.Type: ("cyan", "turquoise"),
    Operator.Word: ("purple", "fuchsia"),
    Name.Builtin: ("cyan", "turquoise"),
    Name.Function: ("green", "green"),
    Name.Namespace: ("_teal_", "_turquoise_"),
    Name.Class: ("_green_", "_green_"),
    Name.Exception: ("cyan", "turquoise"),
    Name.Decorator: ("white", "gray"),
    Name.Variable: ("red", "red"),
    Name.Constant: ("red", "red"),
    Name.Attribute: ("gray", "white"),
    Name.Tag: ("blue", "blue"),
    String: ("white", "white"),
    Number: ("white", "white"),
    Generic.Deleted: ("red", "red"),
    Generic.Inserted: ("green", "green"),
    Generic.Heading: ("**", "**"),
    Generic.Subheading: ("*purple*", "*fuchsia*"),
    Generic.Prompt: ("**", "**"),
    Generic.Error: ("red", "red"),
    Error: ("white", "white"),
}


# pylint: disable=import-outside-toplevel
def enable_win_colors():
    """Enable windows colors."""
    global OUTFILE
    if sys.platform in ("win32", "cygwin"):
        with contextlib.suppress(AttributeError):
            OUTFILE = UnclosingTextIOWrapper(sys.stdout.buffer)
        try:
            import colorama.initialise
        except ImportError:
            pass
        else:
            OUTFILE = colorama.initialise.wrap_stream(
                OUTFILE, convert=None, strip=None, autoreset=False, wrap=True
            )


def warn_python_version():
    """Check the interpreter version and emit a warning in case of mismatch."""
    suggested_versions: List[Tuple[int, int]] = [
        (3, 7),
        (3, 8),
    ]

    version_info = sys.version_info
    v_minor: int = version_info.minor
    v_major: int = version_info.major

    if (v_major, v_minor) not in suggested_versions:
        print(
            textwrap.dedent(
                f"""
        # Warning!! You are running Asserts in python{v_major}.{v_minor}
        #   some functionality may not work!!
        #
        #   suggested versions are:"""[
                    1:
                ]
            )
        )
        for major, minor in suggested_versions:
            print(f"#     - python{major}.{minor}")


def colorize_text(message, without_color=False):
    """Print colorized text content."""
    if without_color:
        print(message, end="")
    else:
        enable_win_colors()
        formatter = TerminalFormatter(colorscheme=SUMMARY_COLORS)
        highlight(message, PropertiesLexer(), formatter, OUTFILE)


def colorize(parsed_content):
    """Colorize content."""
    enable_win_colors()
    for node in parsed_content:
        try:
            if node["status"] == OPEN:
                style = OPEN_COLORS
            elif node["status"] == CLOSED:
                style = CLOSE_COLORS
            elif node["status"] == UNKNOWN:
                style = UNKNOWN_COLORS
            elif node["status"].startswith(ERROR):
                style = OPEN_COLORS
        except KeyError:
            style = SUMMARY_COLORS

        message = yaml.safe_dump(
            node,
            default_flow_style=False,
            explicit_start=True,
            allow_unicode=True,
        )
        highlight(
            message,
            PropertiesLexer(),
            TerminalFormatter(colorscheme=style),
            OUTFILE,
        )


def exit_asserts(reason: str) -> None:
    """Return according to FA_STRICT value."""
    if os.environ.get("FA_STRICT") == "true":
        sys.exit(EXIT_CODES[reason])
    sys.exit(0)


def get_parsed_output(content):
    """Get parsed YAML output."""
    try:
        ret = [x for x in yaml.safe_load_all(content) if x]
    except yaml.scanner.ScannerError:
        print(content, flush=True)
        exit_asserts("exploit-error")
    else:
        return ret


def get_total_checks(output_list):
    """Get total checks."""
    return sum(1 for output in output_list if "status" in output)


def get_total_open_checks(output_list):
    """Get total open checks."""
    return sum(
        1
        for output in output_list
        if "status" in output and output["status"] == OPEN
    )


def get_total_closed_checks(output_list):
    """Get total closed checks."""
    return sum(
        1
        for output in output_list
        if "status" in output and output["status"] == CLOSED
    )


def get_total_unknown_checks(output_list):
    """Get total unknown checks."""
    return sum(
        1
        for output in output_list
        if "status" in output and output["status"] == UNKNOWN
    )


def get_total_error_checks(output_list):
    """Get total error checks."""
    return sum(
        1
        for output in output_list
        if "status" in output and output["status"].startswith(ERROR)
    )


def get_total_vulnerabilities(output_list):
    """Get total vulnerabilities on all checks."""
    return sum(
        1
        for output in output_list
        for vuln in output.get("vulnerabilities", [])
    )


def filter_content(parsed: list, args) -> list:
    """Show filtered content according to args."""
    result: list = [
        node
        for node in parsed
        if "status" not in node
        or (node.get("status", "").startswith(ERROR))
        or (args.show_open and node.get("status") == OPEN)
        or (args.show_closed and node.get("status") == CLOSED)
        or (args.show_unknown and node.get("status") == UNKNOWN)
    ]
    return result


def get_risk_levels(parsed_content):
    """Get risk levels of opened checks."""
    try:
        filtered = [
            x
            for x in parsed_content
            if "status" in x and "risk" in x and x["status"] == OPEN
        ]

        high_risk = sum(1 for x in filtered if x["risk"] == "high")
        medium_risk = sum(1 for x in filtered if x["risk"] == "medium")
        low_risk = sum(1 for x in filtered if x["risk"] == "low")

        opened = get_total_open_checks(parsed_content)

        if opened > 0:
            risk_level = {
                "high": "{} ({:.2f}%)".format(
                    high_risk, high_risk / opened * 100
                ),
                "medium": "{} ({:.2f}%)".format(
                    medium_risk, medium_risk / opened * 100
                ),
                "low": "{} ({:.2f}%)".format(
                    low_risk, low_risk / opened * 100
                ),
            }
        else:
            risk_level = {
                "high": "0 (0%)",
                "medium": "0 (0%)",
                "low": "0 (0%)",
            }
    except KeyError:
        risk_level = "undefined"
    return risk_level


def print_message(message, args):
    """Print message according to args."""
    if args.no_color:
        for node in message:
            print(
                yaml.safe_dump(
                    node,
                    default_flow_style=False,
                    explicit_start=True,
                    allow_unicode=True,
                ),
                flush=True,
                end="",
            )
    else:
        colorize(message)


def show_banner(args):
    """Show Asserts banner."""
    enable_win_colors()
    header = textwrap.dedent(
        rf"""
        #     ________      _     __   ___                        __
        #    / ____/ /_  __(_)___/ /  /   |  _____________  _____/ /______
        #   / /_  / / / / / / __  /  / /| | / ___/ ___/ _ \/ ___/ __/ ___/
        #  / __/ / / /_/ / / /_/ /  / ___ |(__  |__  )  __/ /  / /_(__  )
        # /_/   /_/\__,_/_/\__,_/  /_/  |_/____/____/\___/_/   \__/____/
        #
        # v. {fluidasserts.__version__}
        #  ___
        # | >>|> fluid
        # |___|  attacks, we hack your software
        #
        """
    )

    colorize_text(header, args.no_color)


@contextlib.contextmanager
def stdout_redir():
    """Redirect stdout."""
    old = sys.stdout
    stdout = StringIO()
    sys.stdout = stdout
    try:
        yield stdout
    finally:
        sys.stdout = old


@contextlib.contextmanager
def stderr_redir():
    """Redirect stderr."""
    old = sys.stderr
    stderr = StringIO()
    sys.stderr = stderr
    try:
        yield stderr
    finally:
        sys.stderr = old


def lint_exploit(exploit):
    """Verify Asserts exploit guidelines against given exploit code."""
    rules = {
        "001": {
            "description": "Avoid importing requests. Use fluidasserts.helper.http instead.",
            "regexes": ["import requests", "from requests import"],
        },
        "002": {
            "description": "Avoid hardcoding session cookies.",
            "regexes": ["[cC]ookie: "],
        },
        "003": {
            "description": "Avoid printing aditional info in Asserts using print().",
            "regexes": [r"(?<![^ ])print[\s]*\("],
        },
        "004": {
            "description": "Avoid using exit().",
            "regexes": [r"(?<![^ ])exit[\s]*\("],
        },
        "005": {
            "description": "Exploit does not use fluidasserts.util.generic.add_finding()",
            "regexes": [r"^((?!generic\.add_finding\().)*$"],
        },
    }
    warnings = []
    warnings += (
        "{}: {}".format(rule, rules[rule]["description"])
        for rule in rules
        for x in rules[rule]["regexes"]
        if re.search(x, exploit)
    )

    if warnings:
        enable_win_colors()
        message = textwrap.dedent(
            """
            ---
            linting: warnings
            {}

            """
        ).format("\n  ".join(warnings))
        highlight(
            message,
            PropertiesLexer(),
            TerminalFormatter(colorscheme=UNKNOWN_COLORS),
            sys.stderr,
        )


def exec_wrapper(exploit_name: str, exploit_content: str) -> str:  # noqa
    """Execute an exploit and handle its errors, propagate it's stdout."""
    lint_exploit(exploit_content)
    try:
        with stdout_redir() as stdout_result, stderr_redir() as stderr_result:
            code = compile(exploit_content, exploit_name, "exec", optimize=0)
            exec(code, {"print": lambda *x, **y: (x, y)}, dict())
    except BaseException as exc:  # lgtm [py/catch-base-exception]
        print(stderr_result.getvalue(), end="", file=sys.stderr)
        print(stdout_result.getvalue(), end="", file=sys.stdout)
        exc_type = type(exc)
        exc_name: str = getattr(exc_type, "__name__", str(exc_type))
        return yaml.safe_dump(
            dict(
                status=f"{ERROR}/{exc_name}, {exc}", source_file=exploit_name
            ),
            default_flow_style=False,
            explicit_start=True,
            allow_unicode=True,
        )
    print(stderr_result.getvalue(), end="", file=sys.stderr)
    return stdout_result.getvalue()


def exec_ssl_package(addresses: List[str], enable_multiprocessing: bool):
    """Execute generic checks from the SSL package."""
    template = textwrap.dedent(
        """
        from fluidasserts.proto import ssl
        from fluidasserts.format import x509
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Protocols - {title} Module')

        {methods}
        """
    )

    source: Dict[str, str] = {
        (
            "ssl",
            "SSL part 1",
        ): """
            ssl.allows_modified_mac('{ip_address}', {port})
            """,
        (
            "ssl",
            "SSL part 2",
        ): """
            ssl.has_poodle_sslv3('{ip_address}', {port})
            ssl.has_poodle_tls('{ip_address}', {port})
            """,
        (
            "x509",
            "X509 verifications",
        ): """
            x509.is_cert_cn_not_equal_to_site('{ip_address}', {port})
            x509.is_cert_cn_using_wildcard('{ip_address}', {port})
            x509.is_cert_inactive('{ip_address}', {port})
            x509.is_cert_untrusted('{ip_address}', {port})
            x509.is_cert_validity_lifespan_unsafe('{ip_address}', {port})
            x509.is_sha1_used('{ip_address}', {port})
            x509.is_md5_used('{ip_address}', {port})
            """,
    }

    exploits = [
        (
            module[1],
            template.format(
                title=module[1],
                methods=textwrap.dedent(
                    methods.format(
                        ip_address=address.split(":")[0],
                        port=address.split(":")[1] if ":" in address else 443,
                    )
                ),
            ),
        )
        for address in addresses
        for module, methods in source.items()
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_aws_package(credentials: List[str], enable_multiprocessing: bool):
    """Execute generic methods from the AWS package."""
    template = textwrap.dedent(
        """
        from fluidasserts.cloud.aws import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Amazon Web Services - {title} Module')

        {methods}
        """
    )

    source: Dict[str, str] = {
        (
            "cloudtrail",
            "CloudTrail",
        ): """
            cloudtrail.files_not_validated('{key}', '{secret}')
            cloudtrail.has_unencrypted_logs('{key}', '{secret}')
            cloudtrail.is_trail_bucket_logging_disabled('{key}', '{secret}')
            cloudtrail.is_trail_bucket_public('{key}', '{secret}')
            cloudtrail.trails_not_multiregion('{key}', '{secret}')
            """,
        (
            "cognito",
            "Cognito",
        ): """
                cognito.mfa_disabled('{key}', '{secret}')
                """,
        (
            "dynamodb",
            "DynamoDB",
        ): """
            dynamodb.encrypted_with_aws_master_keys('{key}', '{secret}')
            dynamodb.has_disabled_continuous_backups('{key}', '{secret}')
            """,
        (
            "ec2",
            "EC2",
        ): """
            ec2.default_seggroup_allows_all_traffic('{key}', '{secret}')
            ec2.has_associate_public_ip_address('{key}', '{secret}')
            ec2.has_default_security_groups_in_use('{key}', '{secret}')
            ec2.has_insecure_port_range_in_security_group('{key}', '{secret}')
            ec2.has_instances_using_iam_roles('{key}', '{secret}')
            ec2.has_instances_using_unapproved_amis('{key}', '{secret}')
            ec2.has_not_deletion_protection('{key}', '{secret}')
            ec2.has_security_groups_ip_ranges_in_rfc1918('{key}', '{secret}')
            ec2.has_terminate_shutdown_behavior('{key}', '{secret}')
            ec2.has_unencrypted_amis('{key}', '{secret}')
            ec2.has_publicly_shared_amis('{key}', '{secret}')
            ec2.has_unencrypted_snapshots('{key}', '{secret}')
            ec2.has_unencrypted_volumes('{key}', '{secret}')
            ec2.has_unrestricted_dns_access('{key}', '{secret}')
            ec2.has_unrestricted_ftp_access('{key}', '{secret}')
            ec2.has_unused_ec2_key_pairs('{key}', '{secret}')
            ec2.has_unused_seggroups('{key}', '{secret}')
            ec2.seggroup_allows_anyone_to_admin_ports('{key}', '{secret}')
            ec2.vpcs_without_flowlog('{key}', '{secret}')
            ec2.has_defined_user_data('{key}', '{secret}')
            """,
        (
            "ecs",
            "Elastic Container Service",
        ): """
            ecs.has_not_resources_usage_limits('{key}', '{secret}')
            ecs.no_iam_role_for_tasks('{key}', '{secret}')
            ecs.run_containers_as_root_user('{key}', '{secret}')
            ecs.write_root_file_system('{key}', '{secret}')
            ecs.write_volumes('{key}', '{secret}')
            """,
        (
            "eks",
            "Elastic Kubernetes Service",
        ): """
            eks.allows_insecure_inbound_traffic('{key}', '{secret}')
            eks.has_disable_cluster_logging('{key}', '{secret}')
            eks.has_endpoints_publicly_accessible('{key}', '{secret}')
            """,
        (
            "elb2",
            "Elastic Load Balancer version 2",
        ): """
            elb2.has_access_logging_disabled('{key}', '{secret}')
            elb2.has_not_deletion_protection('{key}', '{secret}')
            """,
        (
            "generic",
            "Generic",
        ): """
            generic.are_valid_credentials('{key}', '{secret}')
            """,
        (
            "iam",
            "IAM",
        ): """
            iam.group_with_inline_policies('{key}', '{secret}')
            iam.has_mfa_disabled('{key}', '{secret}')
            iam.has_not_support_role('{key}', '{secret}')
            iam.has_old_ssh_public_keys('{key}', '{secret}')
            iam.has_permissive_role_policies('{key}', '{secret}')
            iam.has_privileges_over_iam('{key}', '{secret}')
            iam.has_root_active_signing_certificates('{key}', '{secret}')
            iam.has_wildcard_resource_on_write_action('{key}', '{secret}')
            iam.have_full_access_policies('{key}', '{secret}')
            iam.have_old_access_keys('{key}', '{secret}')
            iam.have_old_creds_enabled('{key}', '{secret}')
            iam.mfa_disabled_for_users_with_console_password('{key}',
                                                             '{secret}')
            iam.min_password_len_unsafe('{key}', '{secret}')
            iam.not_requires_lowercase('{key}', '{secret}')
            iam.not_requires_numbers('{key}', '{secret}')
            iam.not_requires_symbols('{key}', '{secret}')
            iam.not_requires_uppercase('{key}', '{secret}')
            iam.password_expiration_unsafe('{key}', '{secret}')
            iam.password_reuse_unsafe('{key}', '{secret}')
            iam.policies_attached_to_users('{key}', '{secret}')
            iam.root_has_access_keys('{key}', '{secret}')
            iam.root_without_mfa('{key}', '{secret}')
            iam.users_with_password_and_access_keys('{key}', '{secret}')
            iam.has_full_access_to_ssm('{key}', '{secret}')
            iam.users_with_multiple_access_keys('{key}', '{secret}')
            iam.allows_priv_escalation_by_policies_versions('{key}','{secret}')
            iam.allows_priv_escalation_by_attach_policy('{key}', '{secret}')
            """,
        (
            "kms",
            "Key Management Service",
        ): """
            kms.has_key_rotation_disabled('{key}', '{secret}')
            kms.has_master_keys_exposed_to_everyone('{key}', '{secret}')
            """,
        (
            "rds",
            "RDS",
        ): """
            rds.has_not_deletion_protection('{key}', '{secret}')
            rds.has_public_instances('{key}', '{secret}')
            rds.is_cluster_not_inside_a_db_subnet_group('{key}', '{secret}')
            rds.is_instance_not_inside_a_db_subnet_group('{key}', '{secret}')
            rds.has_encryption_disabled('{key}', '{secret}')
            rds.has_public_snapshots('{key}', '{secret}')
            rds.not_uses_iam_authentication('{key}', '{secret}')
            rds.unrestricted_db_security_groups('{key}', '{secret}')
            """,
        (
            "redshift",
            "RedShift",
        ): """
            redshift.has_public_clusters('{key}', '{secret}')
            """,
        (
            "s3",
            "S3",
        ): """
            s3.buckets_allow_unauthorized_public_access('{key}', '{secret}')
            s3.has_buckets_without_default_encryption('{key}', '{secret}')
            s3.has_disabled_server_side_encryption('{key}', '{secret}')
            s3.has_insecure_transport('{key}', '{secret}')
            s3.has_public_buckets('{key}', '{secret}')
            s3.has_server_access_logging_disabled('{key}', '{secret}')
            """,
        (
            "secretsmanager",
            "Secrets Manager",
        ): """
            secretsmanager.has_automatic_rotation_disabled('{key}', '{secret}')
            secretsmanager.secrets_encrypted_with_default_keys('{key}',
                                                               '{secret}')
            """,
    }

    exploits = [
        (
            module[1],
            template.format(
                title=module[1],
                module=module[0],
                methods=textwrap.dedent(
                    methods.format(
                        key=credential.split(":")[0],
                        secret=credential.split(":")[1],
                    )
                ),
            ),
        )
        for credential in credentials
        for module, methods in source.items()
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_azure_package(credentials, enable_multiprocessing: bool):
    """Execute generic methods from the Azure package."""
    template = textwrap.dedent(
        """
        from fluidasserts.cloud.azure import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Azure - {title} Module')

        {methods}
        """
    )

    source: Dict[str, str] = {
        ("app_services", "App Services"): [
            "has_authentication_disabled",
            "has_client_certificates_disabled",
            "has_https_only_disabled",
            "has_identity_disabled",
            "use_insecure_tls_version",
        ],
        ("key_vaults", "Key vaults"): [
            "entities_have_all_access",
            "has_key_expiration_disabled",
            "has_secret_expiration_disabled",
        ],
        ("network_security_groups", "Network security groups"): [
            "allow_all_ingress_traffic",
            "has_admin_ports_open_to_the_public",
            "has_flow_logs_disabled",
            "has_insecure_port_ranges",
            "has_open_all_ports_to_the_public",
        ],
        ("storage_accounts", "Storage accounts"): [
            "allow_access_from_all_networks",
            "blob_containers_are_public",
            "file_shares_acl_permissions_do_not_expire",
            "file_shares_has_global_acl_permissions",
            "has_insecure_transport",
            "use_microsoft_managed_keys",
        ],
        ("security_center", "Security Center"): [
            "has_admin_security_alerts_disabled",
            "has_api_endpoint_monitor_disabled",
            "has_auto_provisioning_disabled",
            "has_blob_encryption_monitor_disabled",
            "has_disk_encryption_monitor_disabled",
            "has_high_security_alerts_disabled",
            "has_security_configuration_monitor_disabled",
            "has_security_contacts_disabled",
            "has_system_updates_monitor_disabled",
            "has_vm_vulnerabilities_monitor_disabled",
        ],
        ("sqlserver", "SQLServer"): [
            "allow_public_access",
            "has_ad_administration_disabled",
            "has_advanced_data_security_disabled",
            "has_server_auditing_disabled",
            "has_transparent_encryption_disabled",
            "use_microsoft_managed_keys",
        ],
        ("storage_accounts", "Storage Accounts"): [
            "allow_access_from_all_networks",
            "blob_containers_are_public",
            "file_shares_acl_permissions_do_not_expire",
            "file_shares_has_global_acl_permissions",
            "has_blob_container_mutability",
            "has_insecure_transport",
            "use_microsoft_managed_keys",
        ],
        ("virtual_machines", "Virtual machines"): [
            "has_associate_public_ip_address",
            "has_data_disk_encryption_disabled",
            "has_identity_disabled",
            "has_os_disk_encryption_disabled",
            "have_automatic_updates_disabled",
        ],
    }
    exploits = [
        (
            mod[1],
            template.format(
                title=mod[1],
                module=mod[0],
                methods="\n".join(
                    [
                        (
                            f"{mod[0]}.{x}('{cred.split(':')[1]}',"  # noqa
                            f"'{cred.split(':')[2]}','{cred.split(':')[3]}',"
                            f"'{cred.split(':')[0]}')"
                        )
                        for x in methods
                    ]
                ),
                # module.method(client_id,secret,tenant,subscription_id)
            ),
        )
        for cred in credentials
        for mod, methods in source.items()
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_mssql_package(credentials, enable_multiprocessing: bool):
    """Execute generic methods from the mssql package."""
    template = textwrap.dedent(
        """
        from fluidasserts.db import mssql
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - DB - MSSQL Module')

        {methods}
        """
    )

    source = [
        "can_alter_any_credential",
        "can_alter_any_database",
        "can_alter_any_login",
        "can_control_server",
        "can_execute_commands",
        "can_shutdown_server",
        "has_asymmetric_keys_with_unencrypted_private_keys",
        "has_clr_option_enabled",
        "has_contained_dbs_with_auto_close_enabled",
        "has_enabled_ad_hoc_queries",
        "has_login_password_expiration_disabled",
        "has_password_policy_check_disabled",
        "has_remote_access_option_enabled",
        "has_sa_account_login_enabled",
        "has_smo_and_dmo_xps_option_enabled",
        "has_trustworthy_status_on",
        "has_unencrypted_storage_procedures",
        "has_xps_option_enabled",
        "have_access",
        "sa_account_has_not_been_renamed",
    ]
    exploits = [
        (
            "MSSQL",
            template.format(
                methods="\n".join(
                    [
                        (
                            f"mssql.{method}('{cred.split(' ')[2]}',"  # noqa
                            f"'{' '.join(cred.split(' ')[3:])}',"
                            f"'{cred.split(' ')[0]}',"
                            f"'{cred.split(' ')[1]}')"
                        )
                        for method in source
                    ]
                ),
                # module.method(user,password,host,port)
            ),
        )
        for cred in credentials
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_cloudformation_package(
    paths: List[str], enable_multiprocessing: bool
):
    """Execute generic methods from the CloudFormation package."""
    template = textwrap.dedent(
        """
        from fluidasserts.cloud.aws.cloudformation import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - CloudFormation - {title} Module')

        {method}{method_args}
        """
    )

    source: Dict[str, str] = {
        ("ec2", "EC2 (Elastic Cloud Compute)"): [
            "ec2.has_not_an_iam_instance_profile",
            "ec2.has_not_termination_protection",
            "ec2.has_terminate_shutdown_behavior",
            "ec2.has_unencrypted_volumes",
            "ec2.has_unrestricted_cidrs",
            "ec2.has_unrestricted_ip_protocols",
            "ec2.has_unrestricted_ports",
            "ec2.is_associate_public_ip_address_enabled",
            "ec2.uses_default_security_group",
        ],
        ("elb2", "ELBv2 (Elastic Load Balancing v2)"): [
            "elb2.has_access_logging_disabled",
            "elb2.has_not_deletion_protection",
        ],
        ("iam", "IAM (Identity and Access Management)"): [
            "iam.has_privileges_over_iam",
            "iam.has_wildcard_resource_on_write_action",
            "iam.is_managed_policy_miss_configured",
            "iam.is_policy_miss_configured",
            "iam.is_role_over_privileged",
            "iam.missing_role_based_security",
        ],
        ("rds", "RDS (Relational Database Service)"): [
            "rds.has_not_automated_backups",
            "rds.has_not_termination_protection",
            "rds.has_unencrypted_storage",
            "rds.is_not_inside_a_db_subnet_group",
            "rds.is_publicly_accessible",
        ],
        ("secretsmanager", "Secrets Manager"): [
            "secretsmanager.insecure_generate_secret_string",
        ],
    }

    exploits = [
        (
            module[1],
            template.format(
                title=module[1],
                module=module[0],
                method=method,
                method_args=f'("{path}")',
            ),
        )
        for path in paths
        for module, methods in source.items()
        for method in methods
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_terraform_package(paths: List[str], enable_multiprocessing: bool):
    """Execute generic methods from the Terraform package."""
    template = textwrap.dedent(
        """
        from fluidasserts.cloud.aws.terraform import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Terraform - {title} Module')

        {method}{method_args}
        """
    )

    source: Dict[str, str] = {
        ("ebs", "EBS (Elastic Block Storage)"): [
            "ebs.default_encryption_disabled",
        ],
        ("ec2", "EC2 (Elastic Cloud Compute)"): [
            "ec2.allows_all_outbound_traffic",
            "ec2.has_unencrypted_volumes",
            "ec2.has_unrestricted_ip_protocols",
            "ec2.has_unrestricted_ports",
            "ec2.has_unrestricted_cidrs",
            "ec2.has_not_an_iam_instance_profile",
            "ec2.has_not_termination_protection",
            "ec2.has_terminate_shutdown_behavior",
            "ec2.is_associate_public_ip_address_enabled",
            "ec2.uses_default_security_group",
        ],
        ("elb", "ELB (Elastic Load Balancer)"): [
            "elb.has_access_logging_disabled",
        ],
        ("fsx", "FSx (Amazon FSx file systems)"): [
            "fsx.has_unencrypted_volumes",
        ],
        ("iam", "IAM (Identity and Access Management)"): [
            "iam.is_policy_miss_configured",
            "iam.has_wildcard_resource_on_write_action",
        ],
        ("kms", "KMS (Key Management Service)"): [
            "kms.is_key_rotation_absent_or_disabled",
        ],
        ("rds", "RDS (Relational Database Service)"): [
            "rds.has_not_termination_protection",
            "rds.has_unencrypted_storage",
            "rds.has_not_automated_backups",
            "rds.is_publicly_accessible",
            "rds.is_not_inside_a_db_subnet_group",
        ],
        ("s3", "S3 (Simple Storage Service)"): [
            "s3.has_not_private_access_control",
        ],
    }

    exploits = [
        (
            module[1],
            template.format(
                title=module[1],
                module=module[0],
                method=method,
                method_args=f'("{path}")',
            ),
        )
        for path in paths
        for module, methods in source.items()
        for method in methods
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_apk_package(apks):
    """Execute generic checks of APK module."""
    template = textwrap.dedent(
        """\
        from fluidasserts.format import apk
        """
    )
    for apk in apks:
        template += textwrap.dedent(
            """
            apk.uses_dangerous_perms('{apk}')
            apk.has_fragment_injection('{apk}')
            apk.webview_caches_javascript('{apk}')
            apk.webview_allows_resource_access('{apk}')
            apk.not_forces_updates('{apk}')
            apk.not_verifies_ssl_hostname('{apk}')
            apk.allows_user_ca('{apk}')
            apk.uses_insecure_delete('{apk}')
            apk.uses_http_resources('{apk}')
            apk.socket_uses_getinsecure('{apk}')
            apk.has_frida('{apk}')
            """
        ).replace("{apk}", apk)
    return exec_wrapper("built-in APK package", template)


def exec_dns_package(nameservers):
    """Execute generic checks of DNS package."""
    template = textwrap.dedent(
        """\
        from fluidasserts.proto import dns
        """
    )
    for nameserver in nameservers:
        template += textwrap.dedent(
            """
            dns.has_cache_snooping('{ip_address}')
            dns.has_recursion('{ip_address}')
            dns.can_amplify('{ip_address}')
            """
        ).replace("{ip_address}", nameserver)
    return exec_wrapper("built-in DNS package", template)


def exec_lang_package(paths: List[str], enable_multiprocessing: bool):
    """Execute generic methods from the lang package."""
    template = textwrap.dedent(
        """
        from fluidasserts.lang import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Lang - {title} Module')

        {methods}
        """
    )

    source: Dict[str, str] = {
        (
            "core",
            "Core",
        ): """
            core.uses_unencrypted_sockets('__path__')
            """,
        (
            "csharp",
            "C#",
        ): """
            csharp.has_generic_exceptions('__path__')
            csharp.has_insecure_randoms('__path__')
            csharp.has_switch_without_default('__path__')
            csharp.swallows_exceptions('__path__')
            csharp.uses_catch_for_null_reference_exception('__path__')
            csharp.uses_console_writeline('__path__')
            csharp.uses_debug_writeline('__path__')
            csharp.uses_ecb_encryption_mode('__path__')
            csharp.uses_md5_hash('__path__')
            csharp.uses_sha1_hash('__path__')
            """,
        (
            "docker",
            "Docker",
        ): """
            docker.not_pinned('__path__')
            """,
        (
            "dotnetconfig",
            ".NET Config",
        ): """
            dotnetconfig.has_debug_enabled('__path__')
            dotnetconfig.has_ssl_disabled('__path__')
            dotnetconfig.is_header_x_powered_by_present('__path__')
            dotnetconfig.not_custom_errors('__path__')
            """,
        (
            "html",
            "HTML",
        ): """
            html.has_reverse_tabnabbing('__path__')
            html.has_not_subresource_integrity('__path__')
            """,
        (
            "java",
            "Java",
        ): """
            java.has_generic_exceptions('__path__')
            java.has_insecure_randoms('__path__')
            java.has_log_injection('__path__')
            java.has_switch_without_default('__path__')
            java.swallows_exceptions('__path__')
            java.uses_catch_for_null_pointer_exception('__path__')
            java.uses_catch_for_runtime_exception('__path__')
            java.uses_des_algorithm('__path__')
            java.uses_md5_hash('__path__')
            java.uses_print_stack_trace('__path__')
            java.uses_sha1_hash('__path__')
            java.uses_system_exit('__path__')
            java.uses_broken_password_encryption('__path__')
            java.uses_cipher_in_ecb_mode('__path__')
            java.uses_insecure_aes('__path__')
            java.uses_insecure_key_pair_length('__path__')
            java.uses_insecure_rsa('__path__')
            java.uses_insecure_ssl_context('__path__')
            java.uses_various_verbs_in_request_mapping('__path__')
            java.throws_generic_exceptions('__path__')
            """,
        (
            "javascript",
            "Javascript",
        ): """
            javascript.has_insecure_randoms('__path__')
            javascript.has_switch_without_default('__path__')
            javascript.swallows_exceptions('__path__')
            javascript.uses_console_log('__path__')
            javascript.uses_eval('__path__')
            javascript.uses_localstorage('__path__')
            """,
        (
            "php",
            "PHP",
        ): """
            php.has_preg_ce('__path__')
            """,
        (
            "python",
            "Python",
        ): """
            python.has_generic_exceptions('__path__')
            python.uses_catch_for_memory_error('__path__')
            python.uses_catch_for_syntax_errors('__path__')
            python.swallows_exceptions('__path__')
            python.uses_insecure_functions('__path__')
            """,
        (
            "rpgle",
            "RPG",
        ): """
            rpgle.has_dos_dow_sqlcod('__path__')
            rpgle.has_generic_exceptions('__path__')
            rpgle.swallows_exceptions('__path__')
            rpgle.uses_debugging('__path__')
            """,
    }

    exploits = [
        (
            module[1],
            template.format(
                title=module[1],
                module=module[0],
                methods=textwrap.dedent(methods.replace("__path__", path)),
            ),
        )
        for path in paths
        for module, methods in source.items()
    ]

    return exec_exploits(
        exploit_contents=exploits,
        enable_multiprocessing=enable_multiprocessing,
    )


def exec_module(module: List[str], args: List[str]):
    """Execute specific module."""
    module = module[0]
    args = args[0]
    try:
        package, check = module.rsplit(".", maxsplit=1)
    except ValueError:
        print("Module must in the form package.check. Ejm: ssl.has_poodle_tls")
        exit_asserts("config-error")
    try:
        package = "fluidasserts." + package
        asserts_module = importlib.import_module(package)
    except ModuleNotFoundError:
        print(f"Module {package} not found")
        exit_asserts("config-error")
    try:
        getattr(asserts_module, check)
    except AttributeError:
        print(f"Function {check} not found on {package}")
        exit_asserts("config-error")
    args_list = args.replace("#", "', '")
    template = textwrap.dedent(
        f"""\
        from {package} import {check}

        {check}('__args__')
        """
    ).replace("__args__", args_list)
    return exec_wrapper(f"execution of {package}.{check}", template)


def get_exploit_content(exploit_path: str) -> Tuple[str, str]:
    """Read the exploit as a string."""
    with open(exploit_path) as exploit:
        return exploit_path, exploit.read()


def exec_exploits(
    exploit_paths: List[str] = None,
    exploit_contents: List[str] = None,
    enable_multiprocessing: bool = False,
) -> str:
    """Execute the exploits list."""
    try:
        if not exploit_contents:
            exploit_contents = map(get_exploit_content, exploit_paths)
        if enable_multiprocessing:
            with Pool(processes=cpu_count()) as agents:
                results = agents.starmap(exec_wrapper, exploit_contents, 1)
        else:
            results = itertools.starmap(exec_wrapper, exploit_contents)
        return "".join(results)
    except FileNotFoundError:
        print("No exploits found")
        exit_asserts("exploit-not-found")


def get_content(args):  # noqa: MC0001
    """Get raw content according to args parameter."""
    content = ""
    if args.ssl:
        content += exec_ssl_package(args.ssl, args.multiprocessing)
    if args.dns:
        content += exec_dns_package(args.dns)
    if args.apk:
        content += exec_apk_package(args.apk)
    if args.lang:
        content += exec_lang_package(args.lang, args.multiprocessing)
    if args.aws:
        content += exec_aws_package(args.aws, args.multiprocessing)
    if args.cloudformation:
        content += exec_cloudformation_package(
            args.cloudformation, args.multiprocessing
        )
    if args.terraform:
        content += exec_terraform_package(args.terraform, args.multiprocessing)
    if args.azure:
        content += exec_azure_package(args.azure, args.multiprocessing)
    if args.mssql:
        content += exec_mssql_package(args.mssql, args.multiprocessing)
    if args.module:
        content += exec_module(args.module, args.args)
    if args.exploits:
        content += exec_exploits(
            exploit_paths=args.exploits,
            enable_multiprocessing=args.multiprocessing,
        )
    return get_parsed_output(content)


def check_boolean_env_var(var_name):
    """Check value of boolean environment variable."""
    if var_name in os.environ:
        accepted_values = ["true", "false"]
        if os.environ[var_name] not in accepted_values:
            print(
                (
                    f"{var_name} env variable is set but with an "
                    f'unknown value. It must be "true" or "false".'
                )
            )
            exit_asserts("config-error")


def get_argparser():
    """Return an argparser with the CLI arguments."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-q", "--quiet", help="do not show checks output", action="store_true"
    )
    argparser.add_argument(
        "-mod",
        "--module",
        nargs=1,
        metavar="package.check",
        help=("module to execute. " "Ex: proto.ssl.has_poodle_tls"),
    )
    argparser.add_argument(
        "--args",
        nargs=1,
        metavar="arg1#arg2#argN",
        help=(
            "args for the check. "
            "Separate args with #. "
            "Ex: example.com#443"
        ),
    )
    argparser.add_argument(
        "-k",
        "--kiss",
        help=(
            "keep it simple, shows only who and where "
            "has been found to be vulnerable"
        ),
        action="store_true",
    )
    argparser.add_argument(
        "-n", "--no-color", help="remove colors", action="store_true"
    )
    argparser.add_argument(
        "-o",
        "--show-open",
        help="show only opened checks",
        action="store_true",
    )
    argparser.add_argument(
        "-c",
        "--show-closed",
        help="show only closed checks",
        action="store_true",
    )
    argparser.add_argument(
        "-u",
        "--show-unknown",
        help="show only unknown (error) checks",
        action="store_true",
    )
    argparser.add_argument(
        "-ms",
        "--show-method-stats",
        help="show method-level stats at the end",
        action="store_true",
    )
    argparser.add_argument(
        "-eec",
        "--enrich-exit-codes",
        help="make the exit codes more expressive",
        action="store_true",
    )
    argparser.add_argument(
        "-mp",
        "--multiprocessing",
        help=(
            "enable multiprocessing over "
            "the provided list of exploits. "
            "The number of used cpu cores defaults to "
            "the local cpu count provided by the OS."
        ),
        action="store_true",
    )
    argparser.add_argument(
        "-O", "--output", nargs=1, metavar="FILE", help="save output in FILE"
    )
    argparser.add_argument(
        "--ssl",
        nargs="+",
        metavar="IP_ADDRESS:PORT",
        help=(
            "perform generic SSL checks over given IP "
            "address and port, if port is not specified "
            "it defaults to 443"
        ),
    )
    argparser.add_argument(
        "--dns",
        nargs="+",
        metavar="NS",
        help=("perform generic DNS checks " "over given nameserver"),
    )
    argparser.add_argument(
        "--apk",
        nargs="+",
        metavar="APK",
        help=("perform generic APK checks " "over given APK file(s)"),
    )
    argparser.add_argument(
        "--lang",
        nargs="+",
        metavar="FILE/DIR",
        help=(
            "perform static security checks " "over given files or directories"
        ),
    )
    argparser.add_argument(
        "--aws",
        nargs="+",
        metavar="AWS_ACCESS_KEY_ID:AWS_SECRET_ACCESS_KEY",
        help=("perform AWS checks using the given " "credentials"),
    )
    argparser.add_argument(
        "--azure",
        nargs="+",
        metavar=(
            "AZURE_SUBSCRIPTION_ID:AZURE_CLIENT_ID:"
            "AZURE_CLIENT_SECRET:AZURE_TENANT_ID"
        ),
        help=("perform Azure checks using the given " "credentials"),
    )
    argparser.add_argument(
        "--cloudformation",
        nargs="+",
        metavar="FILE/DIR",
        help=(
            "perform AWS checks over CloudFormation "
            "templates starting recursively from "
            "FILE/DIR"
        ),
    )
    argparser.add_argument(
        "--terraform",
        nargs="+",
        metavar="FILE/DIR",
        help=(
            "perform AWS checks over Terraform "
            "templates starting recursively from "
            "FILE/DIR"
        ),
    )
    argparser.add_argument(
        "--mssql",
        nargs="+",
        metavar="host port user password",
        help=("perform MSSQL checks using the given " "credentials."),
    )

    argparser.add_argument("exploits", nargs="*", help="exploits to execute")

    args = argparser.parse_args()

    if not any(
        (
            args.module,
            args.apk,
            args.aws,
            args.cloudformation,
            args.terraform,
            args.dns,
            args.exploits,
            args.http,
            args.lang,
            args.ssl,
            args.azure,
            args.mssql,
        )
    ):
        argparser.print_help()
        exit_asserts("config-error")

    if args.module and not args.args:
        print("`args` parameter is required.")
        exit_asserts("config-error")

    return args


def main():  # noqa: MC0001
    """Run CLI."""
    # On Windows this will filter ANSI escape sequences out of any text sent
    #   to stdout or stderr, and replace them with equivalent Win32 calls.
    init()

    args = get_argparser()

    # Print the Fluid Asserts banner
    show_banner(args)
    warn_python_version()

    # Set the exit codes
    global EXIT_CODES
    EXIT_CODES = RICH_EXIT_CODES if args.enrich_exit_codes else DEF_EXIT_CODES

    # Set the checks verbosity level
    constants.VERBOSE_CHECKS = bool(not args.kiss)

    check_boolean_env_var("FA_STRICT")
    check_boolean_env_var("FA_NOTRACK")

    start_time = timer()
    parsed = get_content(args)
    elapsed_time = timer() - start_time

    if not args.quiet:
        if args.show_open or args.show_closed or args.show_unknown:
            print_message(filter_content(parsed, args), args)
        else:
            print_message(parsed, args)

    total_checks = get_total_checks(parsed)
    open_checks = get_total_open_checks(parsed)
    closed_checks = get_total_closed_checks(parsed)
    unknown_checks = get_total_unknown_checks(parsed)
    error_checks = get_total_error_checks(parsed)
    div_checks = total_checks if total_checks else 1
    total_vulnerabilities = get_total_vulnerabilities(parsed)

    final_message = {
        "summary": {
            "test time": "%.4f seconds" % elapsed_time,
            "checks": {
                "total": "{} ({}%)".format(total_checks, "100"),
                "errors": "{} ({:.2f}%)".format(
                    error_checks, error_checks / div_checks * 100.0
                ),
                "unknown": "{} ({:.2f}%)".format(
                    unknown_checks, unknown_checks / div_checks * 100.0
                ),
                "closed": "{} ({:.2f}%)".format(
                    closed_checks, closed_checks / div_checks * 100.0
                ),
                "opened": "{} ({:.2f}%)".format(
                    open_checks, open_checks / div_checks * 100.0
                ),
            },
            "vulnerabilities": total_vulnerabilities,
            "risk": get_risk_levels(parsed),
        }
    }

    if args.exploits:
        final_message["summary"]["exploits"] = {
            "total": len(args.exploits),
        }

    message = yaml.safe_dump(
        final_message,
        default_flow_style=False,
        explicit_start=True,
        allow_unicode=True,
    )

    if args.show_method_stats:
        show_method_stats = {
            "method level stats": fluidasserts.method_stats_parse_stats()
        }
        show_method_stats_yaml = yaml.safe_dump(
            show_method_stats,
            default_flow_style=False,
            explicit_start=True,
            allow_unicode=True,
        )
        colorize_text(show_method_stats_yaml, args.no_color)

    colorize_text(message, args.no_color)

    if args.output:
        with open(args.output[0], "a+") as fd_out:
            result = yaml.safe_dump(
                parsed,
                default_flow_style=False,
                explicit_start=True,
                allow_unicode=True,
            )
            fd_out.write(result)
            fd_out.write(message)

    if args.enrich_exit_codes:
        if error_checks:
            exit_asserts("exploit-error")
        if unknown_checks:
            exit_asserts("unknown")
    if open_checks:
        exit_asserts("open")
    exit_asserts("closed")
