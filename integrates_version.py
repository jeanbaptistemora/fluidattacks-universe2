# -*- coding:utf-8 -*-
""" Software version email and env variable for FLUIDIntegrates """

from git import Repo
from app import mailer
import os
import fileinput
from __init__ import FI_MAIL_ENGINEERING

def send_mail_version(commit_sha, commit_before_sha):
    version = open('version.txt', 'r').read()
    repo = Repo(os.getcwd())
    message = repo.git.log(commit_before_sha + '...' + commit_sha,
        '--pretty=format:<b>%s</b>%n%bCommitted by: %aN%n')
    to = [FI_MAIL_ENGINEERING]
    context = {
        'version': version,
        'message': message.replace('\n', '<br/>\n')
    }
    mailer.send_mail_new_version(to, context)

if __name__ == '__main__':
    commit_sha = os.environ['CI_COMMIT_SHA']
    commit_before_sha = os.environ['CI_COMMIT_BEFORE_SHA']
    send_mail_version(commit_sha, commit_before_sha)
