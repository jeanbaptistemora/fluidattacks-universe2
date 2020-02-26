import os


def set_xlsx_password(filepath: str, password: str):
    cmd = 'cat {filepath} | secure-spreadsheet '
    cmd += '--password {password} '
    cmd += '--input-format xlsx '
    cmd += '> {filepath}-pwd'
    cmd = cmd.format(filepath=filepath, password=password)

    os.system(cmd)
    os.unlink(filepath)
    os.rename('{filepath}-pwd'.format(filepath=filepath), filepath)
