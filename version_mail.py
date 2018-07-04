""" Software version email for FLUIDIntegrates """

from  app import mailer
from git import Repo
import time
import os


def get_integrates_version():
    cur_time = time.localtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime('%y.%m.{}').format(min_month)

def get_commit_message():
    repo = Repo(os.getcwd())
    changelog = repo.git.log('-1', '--pretty=<b>%s</b>\n%b')
    return changelog.replace("\n", "<br />\n")

def send_mail():
    to = ['engineering@fluidattacks.com']
    context = {
        'version': get_integrates_version(),
        'message': get_commit_message(),
        }
    mailer.send_mail_integrates_new_version(to, context)

send_mail()
