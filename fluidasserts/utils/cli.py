#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""Asserts CLI."""

# standard imports
import os
import sys
import textwrap
import argparse
import itertools
import contextlib
from io import StringIO
from typing import Dict, Tuple, List
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count

# pylint: disable=no-name-in-module
# pylint: disable=global-statement
# pylint: disable=exec-used

# 3rd party imports
import yaml
from colorama import init
from pygments import highlight
from pygments.lexers import PropertiesLexer
from pygments.formatters import TerminalFormatter
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Whitespace
from pygments.util import UnclosingTextIOWrapper

# local imports
import fluidasserts


OUTFILE = sys.stdout

DEF_EXIT_CODES: Dict[str, int] = {
    'closed': 0,
    'open': 1,
    'unknown': 0,

    'config-error': 78,

    'exploit-error': 1,
    'exploit-not-found': 0,
}

RICH_EXIT_CODES: Dict[str, int] = {
    'closed': 0,
    'open': 101,
    'unknown': 102,

    'config-error': 78,

    'exploit-error': 103,
    'exploit-not-found': 104,
}

EXIT_CODES: Dict[str, int] = DEF_EXIT_CODES

OPEN_COLORS = {
    Token: ('', ''),
    Whitespace: ('gray', 'gray'),
    Comment: ('red', 'red'),
    Comment.Preproc: ('red', 'red'),
    Keyword: ('blue', 'blue'),
    Keyword.Type: ('cyan', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('cyan', 'turquoise'),
    Name.Function: ('green', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_green_', '_green_'),
    Name.Exception: ('cyan', 'turquoise'),
    Name.Decorator: ('gray', 'gray'),
    Name.Variable: ('red', 'red'),
    Name.Constant: ('red', 'red'),
    Name.Attribute: ('gray', 'gray'),
    Name.Tag: ('blue', 'blue'),
    String: ('red', 'red'),
    Number: ('red', 'red'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('green', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('red', 'red'),
}

CLOSE_COLORS = {
    Token: ('', ''),
    Whitespace: ('gray', 'gray'),
    Comment: ('gray', 'gray'),
    Comment.Preproc: ('cyan', 'turquoise'),
    Keyword: ('blue', 'blue'),
    Keyword.Type: ('cyan', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('cyan', 'turquoise'),
    Name.Function: ('green', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_green_', '_green_'),
    Name.Exception: ('cyan', 'turquoise'),
    Name.Decorator: ('gray', 'gray'),
    Name.Variable: ('red', 'red'),
    Name.Constant: ('red', 'red'),
    Name.Attribute: ('gray', 'gray'),
    Name.Tag: ('blue', 'blue'),
    String: ('*green*', '*green*'),
    Number: ('*green*', '*green*'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('green', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('*green*', '*green*'),
}

UNKNOWN_COLORS = {
    Token: ('', ''),
    Whitespace: ('gray', 'gray'),
    Comment: ('gray', 'gray'),
    Comment.Preproc: ('cyan', 'turquoise'),
    Keyword: ('blue', 'blue'),
    Keyword.Type: ('cyan', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('cyan', 'turquoise'),
    Name.Function: ('green', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_green_', '_green_'),
    Name.Exception: ('cyan', 'turquoise'),
    Name.Decorator: ('gray', 'gray'),
    Name.Variable: ('red', 'red'),
    Name.Constant: ('red', 'red'),
    Name.Attribute: ('gray', 'gray'),
    Name.Tag: ('blue', 'blue'),
    String: ('*cyan*', '*cyan*'),
    Number: ('*cyan*', '*cyan*'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('green', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('*cyan*', '*cyan*'),
}

SUMMARY_COLORS = {
    Token: ('', ''),
    Whitespace: ('gray', 'gray'),
    Comment: ('gray', 'gray'),
    Comment.Preproc: ('cyan', 'turquoise'),
    Keyword: ('blue', 'blue'),
    Keyword.Type: ('cyan', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('cyan', 'turquoise'),
    Name.Function: ('green', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_green_', '_green_'),
    Name.Exception: ('cyan', 'turquoise'),
    Name.Decorator: ('white', 'gray'),
    Name.Variable: ('red', 'red'),
    Name.Constant: ('red', 'red'),
    Name.Attribute: ('gray', 'white'),
    Name.Tag: ('blue', 'blue'),
    String: ('white', 'white'),
    Number: ('white', 'white'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('green', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('white', 'white'),
}


def enable_win_colors():
    """Enable windows colors."""
    global OUTFILE
    if sys.platform in ('win32', 'cygwin'):  # pragma: no cover
        try:
            OUTFILE = UnclosingTextIOWrapper(sys.stdout.buffer)
        except AttributeError:
            pass
        try:
            import colorama.initialise
        except ImportError:
            pass
        else:
            OUTFILE = colorama.initialise.wrap_stream(OUTFILE, convert=None,
                                                      strip=None,
                                                      autoreset=False,
                                                      wrap=True)


def colorize_text(message, without_color=False):
    """Print colorized text content."""
    if without_color:
        print(message, end='')
    else:
        enable_win_colors()
        formatter = TerminalFormatter(colorscheme=SUMMARY_COLORS)
        highlight(message, PropertiesLexer(), formatter, OUTFILE)


def colorize(parsed_content):
    """Colorize content."""
    enable_win_colors()
    for node in parsed_content:
        try:
            if node['status'] == 'OPEN':
                style = OPEN_COLORS
            elif node['status'] == 'CLOSED':
                style = CLOSE_COLORS
            elif node['status'] == 'UNKNOWN':
                style = UNKNOWN_COLORS
            elif node['status'] == 'ERROR':
                style = OPEN_COLORS
        except KeyError:
            style = SUMMARY_COLORS

        message = yaml.safe_dump(node,
                                 default_flow_style=False,
                                 explicit_start=True,
                                 allow_unicode=True)
        highlight(message, PropertiesLexer(),
                  TerminalFormatter(colorscheme=style),
                  OUTFILE)


def exit_asserts(reason: str) -> None:
    """Return according to FA_STRICT value."""
    if os.environ.get('FA_STRICT') == 'true':
        sys.exit(EXIT_CODES[reason])
    sys.exit(0)


def get_parsed_output(content):
    """Get parsed YAML output."""
    try:
        ret = [x for x in yaml.safe_load_all(content) if x]
    except yaml.scanner.ScannerError:  # pragma: no cover
        print(content, flush=True)
        exit_asserts('exploit-error')
    else:
        return ret


def get_total_checks(output_list):
    """Get total checks."""
    return sum(1 for output in output_list if 'status' in output)


def get_total_open_checks(output_list):
    """Get total open checks."""
    return sum(1 for output in output_list
               if 'status' in output and output['status'] == 'OPEN')


def get_total_closed_checks(output_list):
    """Get total closed checks."""
    return sum(1 for output in output_list
               if 'status' in output and output['status'] == 'CLOSED')


def get_total_unknown_checks(output_list):
    """Get total unknown checks."""
    return sum(1 for output in output_list
               if 'status' in output and output['status'] == 'UNKNOWN')


def get_total_error_checks(output_list):
    """Get total error checks."""
    return sum(1 for output in output_list
               if 'status' in output and output['status'] == 'ERROR')


def filter_content(parsed: list, args) -> list:
    """Show filtered content according to args."""
    result: list = [
        node
        for node in parsed
        if 'status' not in node
        or (node.get('status') == 'ERROR')
        or (args.show_open and node.get('status') == 'OPEN')
        or (args.show_closed and node.get('status') == 'CLOSED')
        or (args.show_unknown and node.get('status') == 'UNKNOWN')]
    return result


def get_risk_levels(parsed_content):
    """Get risk levels of opened checks."""
    try:
        filtered = [
            x for x in parsed_content
            if 'status' in x and 'risk' in x and x['status'] == 'OPEN']

        high_risk = sum(1 for x in filtered if x['risk'] == 'high')
        medium_risk = sum(1 for x in filtered if x['risk'] == 'medium')
        low_risk = sum(1 for x in filtered if x['risk'] == 'low')

        opened = get_total_open_checks(parsed_content)

        if opened > 0:
            risk_level = {
                'high': '{} ({:.2f}%)'.format(high_risk,
                                              high_risk / opened * 100),
                'medium': '{} ({:.2f}%)'.format(medium_risk,
                                                medium_risk / opened * 100),
                'low': '{} ({:.2f}%)'.format(low_risk,
                                             low_risk / opened * 100),
            }
        else:
            risk_level = {
                'high': '0 (0%)',
                'medium': '0 (0%)',
                'low': '0 (0%)',
            }
    except KeyError:
        risk_level = 'undefined'
    return risk_level


def print_message(message, args):
    """Print message according to args."""
    if args.no_color:
        for node in message:
            print(yaml.safe_dump(node,
                                 default_flow_style=False,
                                 explicit_start=True,
                                 allow_unicode=True),
                  flush=True,
                  end='')
    else:
        colorize(message)


def show_banner(args):
    """Show Asserts banner."""
    enable_win_colors()
    header = textwrap.dedent(f"""\
        # Fluid Asserts (v. {fluidasserts.__version__})
        #  ___
        # | >>|> fluid
        # |___|  attacks, we hack your software
        #
        # Loading attack modules ...
        #
        """)

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
    import re
    rules = {
        '001': {
            'description':
            'Avoid importing requests. Use fluidasserts.helper.http instead.',
            'regexes':
                ['import requests', 'from requests import']
        },
        '002': {
            'description':
            'Avoid hardcoding session cookies.',
            'regexes':
                ['[cC]ookie: ']
        },
        '003': {
            'description':
            'Avoid printing aditional info in Asserts using print().',
            'regexes':
                [r'(?<![^ ])print[\s]*\(']
        },
        '004': {
            'description':
            'Avoid using exit().',
            'regexes':
                [r'(?<![^ ])exit[\s]*\(']
        },
        '005': {
            'description':
            'Exploit does not use fluidasserts.util.generic.add_finding()',
            'regexes':
                [r'^((?!generic\.add_finding\().)*$']
        }
    }
    warnings = []
    warnings += ('{}: {}'.format(rule, rules[rule]['description'])
                 for rule in rules
                 for x in rules[rule]['regexes'] if re.search(x, exploit))

    if warnings:
        enable_win_colors()
        message = textwrap.dedent("""
            ---
            linting: warnings
            {}

            """).format("\n  ".join(warnings))
        highlight(message, PropertiesLexer(),
                  TerminalFormatter(colorscheme=UNKNOWN_COLORS),
                  sys.stderr)


def exec_wrapper(exploit_name: str, exploit_content: str) -> str:  # noqa
    """Execute an exploit and handle its errors, propagate it's stdout."""
    lint_exploit(exploit_content)
    try:
        with stdout_redir() as stdout_result, stderr_redir() as stderr_result:
            code = compile(exploit_content, exploit_name, 'exec', optimize=0)
            exec(code, dict(), dict())
    except BaseException as exc:  # lgtm [py/catch-base-exception]
        print(stderr_result.getvalue(), end='', file=sys.stderr)
        print(stdout_result.getvalue(), end='', file=sys.stdout)
        return yaml.safe_dump(dict(status='ERROR',
                                   exploit=exploit_name,
                                   exception=str(type(exc)),
                                   message=str(exc)),
                              default_flow_style=False,
                              explicit_start=True,
                              allow_unicode=True)
    print(stderr_result.getvalue(), end='', file=sys.stderr)
    return stdout_result.getvalue()


def exec_http_package(urls):
    """Execute generic checks of HTTP package."""
    template = textwrap.dedent("""\
        from fluidasserts.proto import http
        """)
    for url in urls:
        template += textwrap.dedent("""
            http.is_header_x_asp_net_version_present('__url__')
            http.is_header_x_powered_by_present('__url__')
            http.is_header_access_control_allow_origin_missing('__url__')
            http.is_header_content_security_policy_missing('__url__')
            http.is_header_content_type_missing('__url__')
            http.is_header_expires_missing('__url__')
            http.is_header_server_present('__url__')
            http.is_header_x_content_type_options_missing('__url__')
            http.is_header_x_frame_options_missing('__url__')
            http.is_header_x_xxs_protection_missing('__url__')
            http.is_header_hsts_missing('__url__')
            http.is_basic_auth_enabled('__url__')
            http.has_trace_method('__url__')
            http.has_delete_method('__url__')
            http.has_put_method('__url__')
            http.is_sessionid_exposed('__url__')
            http.is_version_visible('__url__')
            http.has_dirlisting('__url__')
            http.has_clear_viewstate('__url__')
            http.is_response_delayed('__url__')
            http.has_clear_viewstate('__url__')
            http.is_date_unsyncd('__url__')
            http.has_host_header_injection('__url__')
            http.has_mixed_content('__url__')
            http.has_reverse_tabnabbing('__url__')
            """).replace('__url__', url)
    return exec_wrapper('built-in HTTP package', template)


def exec_ssl_package(addresses: List[str], enable_multiprocessing: bool):
    """Execute generic checks from the SSL package."""
    template = textwrap.dedent("""
        from fluidasserts.proto import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Protocols - {title} Module')

        {methods}
        """)

    source: Dict[str, str] = {
        ('ssl', 'SSL.allows'): """
            ssl.allows_anon_ciphers('{ip_address}', {port})
            ssl.allows_insecure_downgrade('{ip_address}', {port})
            ssl.allows_modified_mac('{ip_address}', {port})
            ssl.allows_weak_ciphers('{ip_address}', {port})
            """,
        ('ssl', 'SSL.has'): """
            ssl.has_beast('{ip_address}', {port})
            ssl.has_breach('{ip_address}', {port})
            ssl.has_heartbleed('{ip_address}', {port})
            ssl.has_poodle_sslv3('{ip_address}', {port})
            ssl.has_poodle_tls('{ip_address}', {port})
            ssl.has_sweet32('{ip_address}', {port})
            ssl.has_tls13_downgrade_vuln('{ip_address}', {port})
            """,
        ('ssl', 'SSL.is'): """
            ssl.is_pfs_disabled('{ip_address}', {port})
            ssl.is_sslv3_enabled('{ip_address}', {port})
            ssl.is_tlsv11_enabled('{ip_address}', {port})
            ssl.is_tlsv1_enabled('{ip_address}', {port})
            ssl.not_tls13_enabled('{ip_address}', {port})
            """,
        ('ssl', 'SSL.uses'): """
            ssl.tls_uses_cbc('{ip_address}', {port})
            """,
    }

    exploits = [
        (module[1], template.format(
            title=module[1],
            module=module[0],
            methods=textwrap.dedent(methods.format(
                ip_address=address.split(':')[0],
                port=address.split(':')[1] if ':' in address else 443))))
        for address in addresses
        for module, methods in source.items()]

    return exec_exploits(exploit_contents=exploits,
                         enable_multiprocessing=enable_multiprocessing)


def exec_aws_package(credentials: List[str], enable_multiprocessing: bool):
    """Execute generic methods from the AWS package."""
    template = textwrap.dedent("""
        from fluidasserts.cloud.aws import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Amazon Web Services - {title} Module')

        {methods}
        """)

    source: Dict[str, str] = {
        ('cloudfront', 'CloudFront'): """
            cloudfront.has_logging_disabled('{key}', '{secret}')
            cloudfront.has_not_geo_restrictions('{key}', '{secret}')
            """,
        ('cloudtrail', 'CloudTrail'): """
            cloudtrail.files_not_validated('{key}', '{secret}')
            cloudtrail.has_unencrypted_logs('{key}', '{secret}')
            cloudtrail.is_trail_bucket_logging_disabled('{key}', '{secret}')
            cloudtrail.is_trail_bucket_public('{key}', '{secret}')
            cloudtrail.trails_not_multiregion('{key}', '{secret}')
            """,
        ('ec2', 'EC2'): """
            ec2.default_seggroup_allows_all_traffic('{key}', '{secret}')
            ec2.has_unencrypted_snapshots('{key}', '{secret}')
            ec2.has_unencrypted_volumes('{key}', '{secret}')
            ec2.has_unused_seggroups('{key}', '{secret}')
            ec2.seggroup_allows_anyone_to_admin_ports('{key}', '{secret}')
            ec2.vpcs_without_flowlog('{key}', '{secret}')
            """,
        ('generic', 'Generic'): """
            generic.are_valid_credentials('{key}', '{secret}')
            """,
        ('iam', 'IAM'): """
            iam.has_mfa_disabled('{key}', '{secret}')
            iam.has_not_support_role('{key}', '{secret}')
            iam.have_full_access_policies('{key}', '{secret}')
            iam.have_old_access_keys('{key}', '{secret}')
            iam.have_old_creds_enabled('{key}', '{secret}')
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
            """,
        ('rds', 'RDS'): """
            rds.has_public_instances('{key}', '{secret}')
            """,
        ('redshift', 'RedShift'): """
            redshift.has_public_clusters('{key}', '{secret}')
            """,
        ('s3', 'S3'): """
            s3.has_public_buckets('{key}', '{secret}')
            s3.has_server_access_logging_disabled('{key}', '{secret}')
            """,
    }

    exploits = [
        (module[1], template.format(
            title=module[1],
            module=module[0],
            methods=textwrap.dedent(methods.format(
                key=credential.split(':')[0],
                secret=credential.split(':')[1]))))
        for credential in credentials
        for module, methods in source.items()]

    return exec_exploits(exploit_contents=exploits,
                         enable_multiprocessing=enable_multiprocessing)


def exec_dns_package(nameservers):
    """Execute generic checks of DNS package."""
    template = textwrap.dedent("""\
        from fluidasserts.proto import dns
        """)
    for nameserver in nameservers:
        template += textwrap.dedent("""
            dns.has_cache_snooping('{ip_address}')
            dns.has_recursion('{ip_address}')
            dns.can_amplify('{ip_address}')
            """).replace('{ip_address}', nameserver)
    return exec_wrapper('built-in DNS package', template)


def exec_lang_package(paths: List[str], enable_multiprocessing: bool):
    """Execute generic methods from the lang package."""
    template = textwrap.dedent("""
        from fluidasserts.lang import {module}
        from fluidasserts.utils.generic import add_finding

        add_finding('Fluid Asserts - Lang - {title} Module')

        {methods}
        """)

    source: Dict[str, str] = {
        ('core', 'Core'): """
            # core.file_does_not_exist
            # core.file_exists
            # core.has_all_text
            # core.has_any_secret
            # core.has_any_text
            # core.has_not_any_text
            # core.has_not_text
            # core.has_secret
            # core.has_text
            # core.has_weak_cipher
            # core.is_file_hash_in_list
            core.uses_unencrypted_sockets('__path__')
            """,
        ('csharp', 'C#'): """
            csharp.has_generic_exceptions('__path__')
            csharp.has_if_without_else('__path__')
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
        ('docker', 'Docker'): """
            docker.not_pinned('__path__')
            """,
        ('dotnetconfig', '.NET Config'): """
            dotnetconfig.has_debug_enabled('__path__')
            dotnetconfig.has_ssl_disabled('__path__')
            dotnetconfig.is_header_x_powered_by_present('__path__')
            dotnetconfig.not_custom_errors('__path__')
            """,
        ('html', 'HTML'): """
            # html.has_not_autocomplete('__path__')
            html.has_reverse_tabnabbing('__path__')
            # html.is_cacheable('__path__')
            # html.is_header_content_type_missing('__path__')
            """,
        ('java', 'Java'): """
            # java.does_not_handle_exceptions
            java.has_generic_exceptions('__path__')
            java.has_if_without_else('__path__')
            java.has_insecure_randoms('__path__')
            java.has_log_injection('__path__')
            java.has_switch_without_default('__path__')
            java.swallows_exceptions('__path__')
            java.uses_catch_for_null_pointer_exception('__path__')
            java.uses_catch_for_runtime_exception('__path__')
            java.uses_des_algorithm('__path__')
            # java.uses_insecure_cipher
            # java.uses_insecure_hash
            java.uses_md5_hash('__path__')
            java.uses_print_stack_trace('__path__')
            java.uses_sha1_hash('__path__')
            java.uses_system_exit('__path__')
            """,
        ('javascript', 'Javascript'): """
            javascript.has_if_without_else('__path__')
            javascript.has_insecure_randoms('__path__')
            javascript.has_switch_without_default('__path__')
            javascript.swallows_exceptions('__path__')
            javascript.uses_console_log('__path__')
            javascript.uses_eval('__path__')
            javascript.uses_localstorage('__path__')
            """,
        ('php', 'PHP'): """
            php.has_preg_ce('__path__')
            """,
        ('python', 'Python'): """
            python.has_generic_exceptions('__path__')
            python.uses_catch_for_memory_error('__path__')
            python.uses_catch_for_syntax_errors('__path__')
            python.swallows_exceptions('__path__')
            python.uses_insecure_functions('__path__')
            """,
        ('rpgle', 'RPG'): """
            rpgle.has_dos_dow_sqlcod('__path__')
            rpgle.has_generic_exceptions('__path__')
            rpgle.has_unitialized_vars('__path__')
            rpgle.swallows_exceptions('__path__')
            """,
    }

    exploits = [
        (module[1], template.format(
            title=module[1],
            module=module[0],
            methods=textwrap.dedent(methods.replace('__path__', path))))
        for path in paths
        for module, methods in source.items()]

    return exec_exploits(exploit_contents=exploits,
                         enable_multiprocessing=enable_multiprocessing)


def get_exploit_content(exploit_path: str) -> Tuple[str, str]:
    """Read the exploit as a string."""
    with open(exploit_path) as exploit:
        return exploit_path, exploit.read()


def exec_exploits(
        exploit_paths: List[str] = None,
        exploit_contents: List[str] = None,
        enable_multiprocessing: bool = False) -> str:
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
        print('Exploit not found')
        exit_asserts('exploit-not-found')


def get_content(args):
    """Get raw content according to args parameter."""
    content = ''
    if args.http:
        content += exec_http_package(args.http)
    if args.ssl:
        content += exec_ssl_package(args.ssl, args.multiprocessing)
    if args.dns:
        content += exec_dns_package(args.dns)
    if args.lang:
        content += exec_lang_package(args.lang, args.multiprocessing)
    if args.aws:
        content += exec_aws_package(args.aws, args.multiprocessing)
    if args.exploits:
        content += exec_exploits(exploit_paths=args.exploits,
                                 enable_multiprocessing=args.multiprocessing)
    return get_parsed_output(content)


def check_boolean_env_var(var_name):
    """Check value of boolean environment variable."""
    if var_name in os.environ:
        accepted_values = ['true', 'false']
        if os.environ[var_name] not in accepted_values:
            print((f'{var_name} env variable is set but with an '
                   f'unknown value. It must be "true" or "false".'))
            exit_asserts('config-error')


def main():
    """Run CLI."""
    init()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-q', '--quiet', help='decrease output verbosity',
                           action='store_true')
    argparser.add_argument('-n', '--no-color', help='remove colors',
                           action='store_true')
    argparser.add_argument('-o', '--show-open', help='show only opened checks',
                           action='store_true')
    argparser.add_argument('-c', '--show-closed',
                           help='show only closed checks',
                           action='store_true')
    argparser.add_argument('-u', '--show-unknown',
                           help='show only unknown (error) checks',
                           action='store_true')
    argparser.add_argument('-ms', '--show-method-stats',
                           help='show method-level stats at the end',
                           action='store_true')
    argparser.add_argument('-eec', '--enrich-exit-codes',
                           help='make the exit codes more expressive',
                           action='store_true')
    argparser.add_argument('-mp', '--multiprocessing',
                           help=('enable multiprocessing over '
                                 'the provided list of exploits.'
                                 'The number of used cpu cores defaults to '
                                 'the local cpu count provided by the OS.'),
                           action='store_true')
    argparser.add_argument('-O', '--output', nargs=1, metavar='FILE',
                           help='save output in FILE')
    argparser.add_argument('-H', '--http', nargs='+', metavar='URL',
                           help='perform generic HTTP checks over given URL')
    argparser.add_argument('-S', '--ssl', nargs='+',
                           metavar='IP_ADDRESS:PORT',
                           help=('perform generic SSL checks over given IP '
                                 'address and port, if port is not specified '
                                 'it defaults to 443'))
    argparser.add_argument('-D', '--dns', nargs='+', metavar='NS',
                           help=('perform generic DNS checks '
                                 'over given nameserver'))
    argparser.add_argument('-L', '--lang', nargs='+', metavar='FILE/DIR',
                           help=('perform static security checks '
                                 'over given files or directories'))
    argparser.add_argument('-A', '--aws', nargs='+',
                           metavar='AWS_ACCESS_KEY_ID:AWS_SECRET_ACCESS_KEY',
                           help=('perform AWS checks using the given '
                                 'credentials'))
    argparser.add_argument('exploits', nargs='*', help='exploits to execute')

    args = argparser.parse_args()
    show_banner(args)

    if not args.exploits and not args.http \
       and not args.ssl and not args.dns \
       and not args.lang and not args.aws:
        argparser.print_help()
        exit_asserts('config-error')

    global EXIT_CODES
    EXIT_CODES = RICH_EXIT_CODES if args.enrich_exit_codes else DEF_EXIT_CODES

    check_boolean_env_var('FA_STRICT')
    check_boolean_env_var('FA_NOTRACK')

    start_time = timer()
    parsed = get_content(args)
    end_time = timer()
    elapsed_time = end_time - start_time

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

    final_message = {
        'summary': {
            'test time': '%.4f seconds' % elapsed_time,
            'checks': {
                'total': '{} ({}%)'.format(total_checks, '100'),
                'errors':
                    '{} ({:.2f}%)'.format(error_checks,
                                          error_checks / div_checks * 100.0),
                'unknown':
                    '{} ({:.2f}%)'.format(unknown_checks,
                                          unknown_checks / div_checks * 100.0),
                'closed':
                    '{} ({:.2f}%)'.format(closed_checks,
                                          closed_checks / div_checks * 100.0),
                'opened':
                    '{} ({:.2f}%)'.format(open_checks,
                                          open_checks / div_checks * 100.0),
            },
            'risk': get_risk_levels(parsed),
        }
    }

    message = yaml.safe_dump(final_message,
                             default_flow_style=False,
                             explicit_start=True,
                             allow_unicode=True)

    if args.show_method_stats:
        show_method_stats = {
            'method level stats': fluidasserts.method_stats_parse_stats()
        }
        show_method_stats_yaml = yaml.safe_dump(show_method_stats,
                                                default_flow_style=False,
                                                explicit_start=True,
                                                allow_unicode=True)
        colorize_text(show_method_stats_yaml, args.no_color)

    colorize_text(message, args.no_color)

    if args.output:
        with open(args.output[0], 'a+') as fd_out:
            result = yaml.safe_dump(parsed,
                                    default_flow_style=False,
                                    explicit_start=True,
                                    allow_unicode=True)
            fd_out.write(result)
            fd_out.write(message)

    if error_checks:
        exit_asserts('exploit-error')
    if args.enrich_exit_codes and unknown_checks:
        exit_asserts('unknown')
    if open_checks:
        exit_asserts('open')
    exit_asserts('closed')
