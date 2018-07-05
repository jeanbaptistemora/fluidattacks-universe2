# -*- coding:utf-8 -*-
""" Software version email and env variable for FLUIDIntegrates """

from git import Repo
from app import mailer
import time
import os
import sys
import fileinput

def set_integrates_version():
    cur_time = time.localtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    version = time.strftime('%y.%m.{}').format(min_month)
    file = fileinput.FileInput('/usr/src/app/app/templates/dashboard.html', inplace=True)
    for line in file:
        sys.stdout.write (line.replace(">v.<", ">v. " + version + "<"))
    file.close()

def send_mail_version():
    version = get_integrates_version()
    repo = Repo(os.getcwd())
    changelog = repo.git.log('-1', '--pretty=<b>%s</b>\n%b')
    commit_message = changelog.replace("\n", "<br />\n")
    to = ['engineering@fluidattacks.com']
    context = {
        'version': version,
        'message': commit_message,
        }
    mailer.send_mail_integrates_new_version(to, context)

def get_integrates_version():
    file = fileinput.FileInput('/usr/src/app/app/templates/dashboard.html')
    version = ""
    for line in file:
        if ">v." in line:
            version = line.split(">v. ")[1].split("<")[0]
            return version
    file.close()
    return version
