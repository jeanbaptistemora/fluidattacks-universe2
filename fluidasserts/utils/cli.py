#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""Asserts CLI."""

# standard imports
import os
import sys
import textwrap
import argparse
import contextlib
from io import StringIO
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
        except KeyError:
            style = SUMMARY_COLORS

        message = yaml.safe_dump(node,
                                 default_flow_style=False,
                                 explicit_start=True,
                                 allow_unicode=True)
        highlight(message, PropertiesLexer(),
                  TerminalFormatter(colorscheme=style),
                  OUTFILE)


def return_strict(condition):
    """Return according to FA_STRICT value."""
    if 'FA_STRICT' in os.environ:
        if os.environ['FA_STRICT'] == 'true':
            if condition:
                return 1
    return 0


def get_parsed_output(content):
    """Get parsed YAML output."""
    try:
        ret = [x for x in yaml.safe_load_all(content) if x]
    except yaml.scanner.ScannerError:  # pragma: no cover
        print(content, flush=True)
        sys.exit(return_strict(True))
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


def filter_content(parsed: list, args) -> list:
    """Show filtered content according to args."""
    result: list = [
        node
        for node in parsed
        if 'status' not in node
        or (args.show_open and node.get('status') == 'OPEN')
        or (args.show_closed and node.get('status') == 'CLOSED')
        or (args.show_unknown and node.get('status') == 'UNKNOWN')]
    return result


def get_risk_levels(parsed_content):
    """Get risk levels of opened checks."""
    try:
        filtered = [
            x for x in parsed_content
            if 'status' in x and 'risk-level' in x and x['status'] == 'OPEN']

        high_risk = sum(1 for x in filtered if x['risk-level'] == 'high')
        medium_risk = sum(1 for x in filtered if x['risk-level'] == 'medium')
        low_risk = sum(1 for x in filtered if x['risk-level'] == 'low')

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
    yield stdout
    sys.stdout = old


@contextlib.contextmanager
def stderr_redir():
    """Redirect stderr."""
    old = sys.stderr
    stderr = StringIO()
    sys.stderr = stderr
    yield stderr
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
                [r'print[\s]*\(']
        },
        '004': {
            'description':
            'Avoid using exit().',
            'regexes':
                [r'exit[\s]*\(']
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


def exec_wrapper(exploit):
    """Execute exploit wrapper."""
    lint_exploit(exploit)
    with stdout_redir() as stdout_result, stderr_redir() as stderr_result:
        code = compile(exploit, 'exploit', 'exec', optimize=0)
        exec(code)
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
            http.is_header_cache_control_missing('__url__')
            http.is_header_content_security_policy_missing('__url__')
            http.is_header_content_type_missing('__url__')
            http.is_header_expires_missing('__url__')
            http.is_header_pragma_missing('__url__')
            http.is_header_server_present('__url__')
            http.is_header_x_content_type_options_missing('__url__')
            http.is_header_x_frame_options_missing('__url__')
            http.is_header_perm_cross_dom_pol_missing('__url__')
            http.is_header_x_xxs_protection_missing('__url__')
            http.is_header_hsts_missing('__url__')
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
            """).replace('__url__', url)
    return exec_wrapper(template)


def exec_ssl_package(ip_addresses):
    """Execute generic checks of SSL package."""
    template = textwrap.dedent("""\
        from fluidasserts.proto import ssl
        from fluidasserts.format import x509
        """)
    for ip_addr in ip_addresses:
        template += textwrap.dedent("""
            ssl.is_pfs_disabled('__ip__')
            ssl.is_sslv3_enabled('__ip__')
            ssl.is_tlsv1_enabled('__ip__')
            ssl.is_tlsv11_enabled('__ip__')
            ssl.not_tls13_enabled('__ip__')
            ssl.has_poodle_tls('__ip__')
            ssl.has_poodle_sslv3('__ip__')
            ssl.has_breach('__ip__')
            ssl.allows_anon_ciphers('__ip__')
            ssl.allows_weak_ciphers('__ip__')
            ssl.has_beast('__ip__')
            ssl.has_heartbleed('__ip__')
            ssl.has_sweet32('__ip__')
            ssl.allows_modified_mac('__ip__')
            ssl.allows_insecure_downgrade('__ip__')
            ssl.tls_uses_cbc('__ip__')
            ssl.has_tls13_downgrade_vuln('__ip__')
            x509.is_cert_cn_not_equal_to_site('__ip__')
            x509.is_cert_inactive('__ip__')
            x509.is_cert_validity_lifespan_unsafe('__ip__')
            x509.is_sha1_used('__ip__')
            x509.is_md5_used('__ip__')
            x509.is_cert_untrusted('__ip__')
            """).replace('__ip__', ip_addr)
    return exec_wrapper(template)


def exec_dns_package(nameservers):
    """Execute generic checks of DNS package."""
    template = textwrap.dedent("""\
        from fluidasserts.proto import dns
        """)
    for nameserver in nameservers:
        template += textwrap.dedent("""
            dns.has_cache_snooping('__ip__')
            dns.has_recursion('__ip__')
            dns.can_amplify('__ip__')
            """).replace('__ip__', nameserver)
    return exec_wrapper(template)


def exec_lang_package(codes):
    """Execute generic checks of LANG package."""
    template = textwrap.dedent("""\
        from fluidasserts.lang import csharp
        from fluidasserts.lang import dotnetconfig
        from fluidasserts.lang import html
        from fluidasserts.lang import java
        from fluidasserts.lang import javascript
        from fluidasserts.lang import python
        from fluidasserts.lang import rpgle
        from fluidasserts.lang import php
        from fluidasserts.proto import git
        from fluidasserts.sca import maven
        from fluidasserts.sca import nuget
        from fluidasserts.sca import pypi
        from fluidasserts.sca import npm
        """)
    for code in codes:
        template += textwrap.dedent("""
            csharp.has_generic_exceptions('__code__')
            csharp.swallows_exceptions('__code__')
            csharp.has_switch_without_default('__code__')
            csharp.has_insecure_randoms('__code__')
            csharp.has_if_without_else('__code__')
            csharp.uses_md5_hash('__code__')
            csharp.uses_sha1_hash('__code__')
            csharp.uses_ecb_encryption_mode('__code__')
            csharp.uses_debug_writeline('__code__')
            csharp.uses_console_writeline('__code__')
            dotnetconfig.is_header_x_powered_by_present('__code__')
            dotnetconfig.has_ssl_disabled('__code__')
            dotnetconfig.has_debug_enabled('__code__')
            dotnetconfig.not_custom_errors('__code__')
            java.has_generic_exceptions('__code__')
            java.uses_catch_for_null_pointer_exception('__code__')
            java.uses_print_stack_trace('__code__')
            java.swallows_exceptions('__code__')
            java.has_switch_without_default('__code__')
            java.has_insecure_randoms('__code__')
            java.has_if_without_else('__code__')
            java.uses_md5_hash('__code__')
            java.uses_sha1_hash('__code__')
            java.uses_des_algorithm('__code__')
            java.has_log_injection('__code__')
            java.uses_system_exit('__code__')
            javascript.uses_console_log('__code__')
            javascript.uses_eval('__code__')
            javascript.uses_localstorage('__code__')
            javascript.has_insecure_randoms('__code__')
            javascript.swallows_exceptions('__code__')
            javascript.has_switch_without_default('__code__')
            javascript.has_if_without_else('__code__')
            python.has_generic_exceptions('__code__')
            python.swallows_exceptions('__code__')
            python.uses_insecure_functions('__code__')
            rpgle.has_dos_dow_sqlcod('__code__')
            rpgle.has_unitialized_vars('__code__')
            rpgle.has_generic_exceptions('__code__')
            rpgle.swallows_exceptions('__code__')
            php.has_preg_ce('__code__')
            git.has_insecure_gitignore('__code__')
            maven.project_has_vulnerabilities('__code__')
            nuget.project_has_vulnerabilities('__code__')
            pypi.project_has_vulnerabilities('__code__')
            npm.project_has_vulnerabilities('__code__')
            """).replace('__code__', code)
    return exec_wrapper(template)


def get_exploit_content(exploit_path: str) -> str:
    """Read the exploit as a string."""
    with open(exploit_path) as exploit:
        return exploit.read()


def exec_exploits(exploit_paths: list, enable_multiprocessing: bool) -> str:
    """Execute the exploits list."""
    try:
        exploit_contents = map(get_exploit_content, exploit_paths)
        if enable_multiprocessing:
            with Pool(processes=cpu_count()) as agents:
                results = agents.map(exec_wrapper, exploit_contents, 1)
        else:
            results = map(exec_wrapper, exploit_contents)
        return "".join(results)
    except FileNotFoundError:
        print('Exploit not found')
        sys.exit(return_strict(False))


def get_content(args):
    """Get raw content according to args parameter."""
    content = ''
    if args.http:
        content += exec_http_package(args.http)
    if args.ssl:
        content += exec_ssl_package(args.ssl)
    if args.dns:
        content += exec_dns_package(args.dns)
    if args.lang:
        content += exec_lang_package(args.lang)
    elif args.exploits:
        content += exec_exploits(args.exploits, args.multiprocessing)
    return get_parsed_output(content)


def check_boolean_env_var(var_name):
    """Check value of boolean environment variable."""
    if var_name in os.environ:
        accepted_values = ['true', 'false']
        if os.environ[var_name] not in accepted_values:
            print((f'{var_name} env variable is set but with an '
                   f'unknown value. It must be "true" or "false".'))
            sys.exit(-1)


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
    argparser.add_argument('-S', '--ssl', nargs='+', metavar='IP',
                           help='perform generic SSL checks over given IP')
    argparser.add_argument('-D', '--dns', nargs='+', metavar='NS',
                           help=('perform generic DNS checks '
                                 'over given nameserver'))
    argparser.add_argument('-L', '--lang', nargs='+', metavar='FILE/DIR',
                           help=('perform static security checks '
                                 'over given files or directories'))
    argparser.add_argument('exploits', nargs='*', help='exploits to execute')

    args = argparser.parse_args()
    show_banner(args)

    if not args.exploits and not args.http \
       and not args.ssl and not args.dns and not args.lang:
        argparser.print_help()
        sys.exit(-1)

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
    div_checks = total_checks if total_checks else 1

    final_message = {
        'summary': {
            'test time': '%.4f seconds' % elapsed_time,
            'checks': {
                'total': '{} ({}%)'.format(total_checks, '100'),
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

    sys.exit(return_strict(open_checks))
