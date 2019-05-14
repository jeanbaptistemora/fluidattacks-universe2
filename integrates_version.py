# -*- coding:utf-8 -*-
""" Software version email and env variable for FLUIDIntegrates """

from git import Repo
from app import mailer
import os, git
import fileinput
from __init__ import FI_MAIL_ENGINEERING

def send_mail_version(commit_sha, commit_before_sha, project):
    version = open('version.txt', 'r').read()
    repo = Repo(os.getcwd())
    message = repo.git.log(commit_before_sha + '...' + commit_sha,
        '--pretty=format:<b>%s</b>%n%bCommitted by: %aN%n')
    to = [FI_MAIL_ENGINEERING]
    context = {
        'project': project,
        'version': version,
        'message': message.replace('\n', '<br/>\n')
    }
    mailer.send_mail_new_version(to, context)

if __name__ == '__main__':
    commit_sha = os.environ['CI_COMMIT_SHA']
    commit_before_sha = os.environ['CI_COMMIT_BEFORE_SHA']
    project = 'integrates'
    send_mail_version(commit_sha, commit_before_sha, project)
