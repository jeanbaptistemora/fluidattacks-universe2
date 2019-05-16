#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""Asserts CLI."""

# standard imports
from io import StringIO
from timeit import default_timer as timer
import contextlib
import argparse
import os
import sys

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
    Whitespace: ('lightgray', 'darkgray'),
    Comment: ('darkred', 'red'),
    Comment.Preproc: ('darkred', 'red'),
    Keyword: ('darkblue', 'blue'),
    Keyword.Type: ('teal', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('teal', 'turquoise'),
    Name.Function: ('darkgreen', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_darkgreen_', '_green_'),
    Name.Exception: ('teal', 'turquoise'),
    Name.Decorator: ('darkgray', 'lightgray'),
    Name.Variable: ('darkred', 'red'),
    Name.Constant: ('darkred', 'red'),
    Name.Attribute: ('lightgray', 'darkgray'),
    Name.Tag: ('blue', 'blue'),
    String: ('red', 'red'),
    Number: ('red', 'red'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('darkgreen', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('red', 'red'),
}

CLOSE_COLORS = {
    Token: ('', ''),
    Whitespace: ('lightgray', 'darkgray'),
    Comment: ('lightgray', 'darkgray'),
    Comment.Preproc: ('teal', 'turquoise'),
    Keyword: ('darkblue', 'blue'),
    Keyword.Type: ('teal', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('teal', 'turquoise'),
    Name.Function: ('darkgreen', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_darkgreen_', '_green_'),
    Name.Exception: ('teal', 'turquoise'),
    Name.Decorator: ('darkgray', 'lightgray'),
    Name.Variable: ('darkred', 'red'),
    Name.Constant: ('darkred', 'red'),
    Name.Attribute: ('lightgray', 'darkgray'),
    Name.Tag: ('blue', 'blue'),
    String: ('*darkgreen*', '*green*'),
    Number: ('*darkgreen*', '*green*'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('darkgreen', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('*darkgreen*', '*green*'),
}

UNKNOWN_COLORS = {
    Token: ('', ''),
    Whitespace: ('lightgray', 'darkgray'),
    Comment: ('lightgray', 'darkgray'),
    Comment.Preproc: ('teal', 'turquoise'),
    Keyword: ('darkblue', 'blue'),
    Keyword.Type: ('teal', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('teal', 'turquoise'),
    Name.Function: ('darkgreen', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_darkgreen_', '_green_'),
    Name.Exception: ('teal', 'turquoise'),
    Name.Decorator: ('darkgray', 'lightgray'),
    Name.Variable: ('darkred', 'red'),
    Name.Constant: ('darkred', 'red'),
    Name.Attribute: ('lightgray', 'darkgray'),
    Name.Tag: ('blue', 'blue'),
    String: ('*teal*', '*teal*'),
    Number: ('*teal*', '*teal*'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('darkgreen', 'green'),
    Generic.Heading: ('**', '**'),
    Generic.Subheading: ('*purple*', '*fuchsia*'),
    Generic.Prompt: ('**', '**'),
    Generic.Error: ('red', 'red'),
    Error: ('*teal*', '*teal*'),
}

SUMMARY_COLORS = {
    Token: ('', ''),
    Whitespace: ('lightgray', 'darkgray'),
    Comment: ('lightgray', 'darkgray'),
    Comment.Preproc: ('teal', 'turquoise'),
    Keyword: ('darkblue', 'blue'),
    Keyword.Type: ('teal', 'turquoise'),
    Operator.Word: ('purple', 'fuchsia'),
    Name.Builtin: ('teal', 'turquoise'),
    Name.Function: ('darkgreen', 'green'),
    Name.Namespace: ('_teal_', '_turquoise_'),
    Name.Class: ('_darkgreen_', '_green_'),
    Name.Exception: ('teal', 'turquoise'),
    Name.Decorator: ('white', 'lightgray'),
    Name.Variable: ('darkred', 'red'),
    Name.Constant: ('darkred', 'red'),
    Name.Attribute: ('lightgray', 'white'),
    Name.Tag: ('blue', 'blue'),
    String: ('white', 'white'),
    Number: ('white', 'white'),
    Generic.Deleted: ('red', 'red'),
    Generic.Inserted: ('darkgreen', 'green'),
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
        OUTFILE = UnclosingTextIOWrapper(sys.stdout.buffer)
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
    """Colorize text content."""
    if without_color:
        print(message, end='')
    else:
        enable_win_colors()
        highlight(message, PropertiesLexer(),
                  TerminalFormatter(colorscheme=SUMMARY_COLORS),
                  OUTFILE)


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

        message = yaml.safe_dump(node, default_flow_style=False,
                                 explicit_start=True)
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
        ret = [x for x in yaml.safe_load_all(content) if len(x) > 0]
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
    return sum(output['status'] == 'OPEN' for output in output_list
               if 'status' in output)


def get_total_closed_checks(output_list):
    """Get total closed checks."""
    return sum(output['status'] == 'CLOSED' for output in output_list
               if 'status' in output)


def get_total_unknown_checks(output_list):
    """Get total unknown checks."""
    return sum(output['status'] == 'UNKNOWN' for output in output_list
               if 'status' in output)


def filter_content(parsed_content, args):
    """Show filtered content according to args."""
    opened_nodes = filter(lambda x: x['status'] == 'OPEN' and args.show_open,
                          parsed_content)
    closed_nodes = filter(lambda x: x['status'] == 'CLOSED' and
                          args.show_closed,
                          parsed_content)
    unknown_nodes = filter(lambda x: x['status'] == 'UNKNOWN' and
                           args.show_unknown,
                           parsed_content)

    return list(opened_nodes) + list(closed_nodes) + list(unknown_nodes)


def get_risk_levels(parsed_content):
    """Get risk levels of opened checks."""
    try:
        high_risk = sum(x['status'] == 'OPEN' and
                        x['risk-level'] == 'high' for x in parsed_content
                        if 'status' and 'risk-level' in x)
        medium_risk = sum(x['status'] == 'OPEN' and
                          x['risk-level'] == 'medium' for x in parsed_content
                          if 'status' and 'risk-level' in x)
        low_risk = sum(x['status'] == 'OPEN' and
                       x['risk-level'] == 'low' for x in parsed_content
                       if 'status' and 'risk-level' in x)

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
            print(yaml.safe_dump(node, default_flow_style=False,
                                 explicit_start=True), flush=True, end='')
    else:
        colorize(message)


def show_banner(args):
    """Show Asserts banner."""
    enable_win_colors()
    header = """# Fluid Asserts (v. {})
#  ___
# | >>|> fluid
# |___|  attacks, we hack your software
#
# Loading attack modules ...
""".format(fluidasserts.__version__)

    colorize_text(header, args.no_color)


@contextlib.contextmanager
def std_redir(stdout=None):
    """Redirect stdout."""
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


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
        }
    }
    warnings = []
    for rule in rules:
        for regex in rules[rule]['regexes']:
            match = re.search(regex, exploit)
            if match:
                warnings.append('{}: {}'.format(rule,
                                                rules[rule]['description']))

    if warnings:
        enable_win_colors()
        message = """
---
linting: warnings
  {}

""".format("\n  ".join(warnings))
        highlight(message, PropertiesLexer(),
                  TerminalFormatter(colorscheme=UNKNOWN_COLORS),
                  sys.stderr)


def exec_wrapper(exploit):
    """Execute exploit wrapper."""
    lint_exploit(exploit)
    with std_redir() as exploit_result:
        code = compile(exploit, 'exploit', 'exec', optimize=0)
        exec(code)
    return exploit_result.getvalue()


def exec_http_package(urls):
    """Execute generic checks of HTTP package."""
    template = """
from fluidasserts.proto import http
"""
    for url in urls:
        template += """
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
""".replace('__url__', url)
    return exec_wrapper(template)


def exec_ssl_package(ip_addresses):
    """Execute generic checks of SSL package."""
    template = """
from fluidasserts.proto import ssl
from fluidasserts.format import x509
"""
    for ip_addr in ip_addresses:
        template += """
ssl.is_pfs_disabled('__ip__')
ssl.is_sslv3_enabled('__ip__')
ssl.is_tlsv1_enabled('__ip__')
ssl.is_tlsv11_enabled('__ip__')
ssl.has_poodle_tls('__ip__')
ssl.has_poodle_sslv3('__ip__')
ssl.has_breach('__ip__')
ssl.allows_anon_ciphers('__ip__')
ssl.allows_weak_ciphers('__ip__')
ssl.has_beast('__ip__')
ssl.has_heartbleed('__ip__')
ssl.allows_modified_mac('__ip__')
x509.is_cert_cn_not_equal_to_site('__ip__')
x509.is_cert_inactive('__ip__')
x509.is_cert_validity_lifespan_unsafe('__ip__')
x509.is_sha1_used('__ip__')
x509.is_md5_used('__ip__')
x509.is_cert_untrusted('__ip__')
""".replace('__ip__', ip_addr)
    return exec_wrapper(template)


def exec_dns_package(nameservers):
    """Execute generic checks of DNS package."""
    template = """
from fluidasserts.proto import dns
"""
    for nameserver in nameservers:
        template += """
dns.has_cache_snooping('__ip__')
dns.has_recursion('__ip__')
dns.can_amplify('__ip__')
""".replace('__ip__', nameserver)
    return exec_wrapper(template)


def exec_lang_package(codes):
    """Execute generic checks of LANG package."""
    template = """
from fluidasserts.lang import csharp
from fluidasserts.lang import dotnetconfig
from fluidasserts.lang import html
from fluidasserts.lang import java
from fluidasserts.lang import javascript
from fluidasserts.lang import python
from fluidasserts.lang import rpgle
from fluidasserts.lang import php
from fluidasserts.sca import maven
from fluidasserts.sca import nuget
from fluidasserts.sca import pypi
from fluidasserts.sca import npm
"""
    for code in codes:
        template += """
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
java.uses_print_stack_trace('__code__')
java.swallows_exceptions('__code__')
java.has_switch_without_default('__code__')
java.has_insecure_randoms('__code__')
java.has_if_without_else('__code__')
java.uses_md5_hash('__code__')
java.uses_sha1_hash('__code__')
java.uses_des_algorithm('__code__')
java.has_log_injection('__code__')
javascript.uses_console_log('__code__')
javascript.uses_eval('__code__')
javascript.uses_localstorage('__code__')
javascript.has_insecure_randoms('__code__')
javascript.swallows_exceptions('__code__')
javascript.has_switch_without_default('__code__')
javascript.has_if_without_else('__code__')
python.has_generic_exceptions('__code__')
python.swallows_exceptions('__code__')
rpgle.has_dos_dow_sqlcod('__code__')
rpgle.has_unitialized_vars('__code__')
rpgle.has_generic_exceptions('__code__')
rpgle.swallows_exceptions('__code__')
php.has_preg_ce('__code__')
maven.project_has_vulnerabilities('__code__')
nuget.project_has_vulnerabilities('__code__')
pypi.project_has_vulnerabilities('__code__')
npm.project_has_vulnerabilities('__code__')
""".replace('__code__', code)
    return exec_wrapper(template)


def exec_exploit(exploit):
    """Execute exploit file."""
    try:
        return exec_wrapper(open(exploit).read())
    except FileNotFoundError:
        print('Exploit not found')
        sys.exit(return_strict(True))


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
    elif args.exploit:
        content += exec_exploit(args.exploit)
    return get_parsed_output(content)


def check_boolean_env_var(var_name):
    """Check value of boolean environment variable."""
    if var_name in os.environ:
        accepted_values = ['true', 'false']
        if os.environ[var_name] not in accepted_values:
            print(var_name + ' env variable is \
set but with an unknown value. It must be "true" or "false".')
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
    argparser.add_argument('-H', '--http', nargs='+', metavar='URL',
                           help='perform generic HTTP checks over given URL')
    argparser.add_argument('-S', '--ssl', nargs='+', metavar='IP',
                           help='perform generic SSL checks over given IP')
    argparser.add_argument('-D', '--dns', nargs='+', metavar='NS',
                           help='perform generic DNS checks \
over given nameserver')
    argparser.add_argument('-L', '--lang', nargs='+', metavar='FILE/DIR',
                           help='perform static security checks over \
given files or directories')
    argparser.add_argument('exploit', nargs='?', help='exploit to execute')

    args = argparser.parse_args()
    show_banner(args)

    if not args.exploit and not args.http \
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

    final_message = {
        'summary': {
            'test time': '%.4f seconds' % elapsed_time,
            'checks': {
                'total': '{} ({}%)'.format(total_checks, '100'),
                'unknown':
                    '{} ({:.2f}%)'.format(unknown_checks,
                                          unknown_checks / total_checks * 100),
                'closed':
                    '{} ({:.2f}%)'.format(closed_checks,
                                          closed_checks / total_checks * 100),
                'opened':
                    '{} ({:.2f}%)'.format(open_checks,
                                          open_checks / total_checks * 100),
            },
            'risk': get_risk_levels(parsed),
        }
    }

    message = yaml.safe_dump(final_message, default_flow_style=False,
                             explicit_start=True)

    colorize_text(message, args.no_color)

    sys.exit(return_strict(open_checks))
