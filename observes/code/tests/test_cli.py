from code import cli


def test_cli_required_flags():
    cmds = [
        '--ammend-authors',
        '--compute-bills',
        '--upload'
    ]
    for cmd in cmds:
        parser = cli.main_parser()
        parser.parse_args(cmd.split())


def test_ammend_parser():
    cmd = '--mailmap-path test/path/to/mailmap'
    parser = cli.ammend_parser()
    parser.parse_args(cmd.split())


def test_bills_parser():
    cmd = '--folder test/path --year 2000 --month 1'
    parser = cli.bills_parser()
    parser.parse_args(cmd.split())


def test_upload_parser():
    cmd = '--namespace repositories'
    parser = cli.upload_parser()
    parser.parse_args(cmd.split())
