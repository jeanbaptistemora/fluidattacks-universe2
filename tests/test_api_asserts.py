# Local libraries
from toolbox import utils
from toolbox.api.asserts import (
    iterate_vulnerabilities_from_content,
    Vulnerability,
)


def test_iterate_vulnerabilities_from_content(relocate):
    status, stdout, _ = utils.generic.run_command(
        cmd=[
            'asserts',
            '--no-color',
            '--lang',
            'subscriptions/continuoustest/forces/static/resources/poc.py',
            'this-one-does-not-exists-and-therefore-is-unknown',
        ],
        cwd='.',
        env={})

    assert not status

    vulnerabilities = \
        tuple(iterate_vulnerabilities_from_content(stdout, 'continuous'))

    vulnerabilities_open = \
        tuple(vul for vul in vulnerabilities if vul.status == 'OPEN')
    vulnerabilities_closed = \
        sum(vul.status == 'CLOSED' for vul in vulnerabilities)
    vulnerabilities_unknown = \
        sum(vul.status == 'UNKNOWN' for vul in vulnerabilities)

    assert len(vulnerabilities_open) == 1, stdout
    assert vulnerabilities_closed == 53, stdout
    assert vulnerabilities_unknown == 54, stdout

    assert sorted(vulnerabilities_open) == [
        Vulnerability(
            finding_title='Fluid Asserts - Lang - Python Module',
            finding_id='',
            status='OPEN',
            kind='SAST',
            what=(
                'continuous/subscriptions/continuoustest/'
                'forces/static/resources/poc.py'
            ),
            where='5',
        ),
    ], stdout
