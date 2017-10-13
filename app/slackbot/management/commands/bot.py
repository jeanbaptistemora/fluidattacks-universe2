#
# FLUIDIntegrates admin bot
#

import time
import slackclient
from django.core.management.base import BaseCommand
from django.conf import settings
# pylint: disable=F0401
from app.dao import integrates_dao

# constants
BOT_ID = 'U7H8PVATA'
AT_BOT = "<@" + BOT_ID + ">"
VALID_COMMANDS = ['add_access',
                  'remove_access',
                  'unregister_user',
                  'list_projects',
                  'list_users']
BOT_NAME = 'integrates'
CMD_SEP = ' '
CHANNEL = 'fluidintegrates'

class Command(BaseCommand):
    help = 'Starts the admin bot'

    def handle_command(self, command, channel):
        command_parsed = command.split(' ')
        if command_parsed[0] in VALID_COMMANDS:
            response = "Running " + " ".join(command_parsed)
            if command_parsed[0] == 'add_access':
                response = self.do_add_access(command)
            elif command_parsed[0] == 'remove_access':
                response = self.do_remove_access(command)
            elif command_parsed[0] == 'list_projects':
                response = self.do_list_projects(command)
            elif command_parsed[0] == 'list_users':
                response = self.do_list_users(command)
        else:
            response = "Not sure what you mean. Use the *" + ", ".join(VALID_COMMANDS) + \
               "* commands, delimited by spaces."
        self.slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)

    def has_access_to_bot(self, user):
        pass

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list:
            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']
        return None, None

    def do_unregister_user(self, data):
        try:
            user = data.split(CMD_SEP)[1:]
            user = user[user.index('|'):user.index('>')][1:]
            if user.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                output = 'Unregistering user *%s*...' % (user)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output


    def do_add_access(self, data):
        try:
            user, project, company = data.split(CMD_SEP)[1:]
            user = user[user.index('|'):user.index('>')][1:]
            if user.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                output = 'Adding access to *%s* to project *%s*...' % (user, project)
                if integrates_dao.is_registered_dao(user) == '0':
                    integrates_dao.register(user)
                    integrates_dao.assign_role(user, 'customer')
                    integrates_dao.assign_company(user, company)
                integrates_dao.add_access_to_project_dao(user, project)
                output = 'Adding access to *%s* to project *%s*...' % (user, project)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    def do_remove_access(self, data):
        try:
            user, project = data.split(CMD_SEP)[1:]
            user = user[user.index('|'):user.index('>')][1:]
            if user.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                output = '[UNDER CONSTRUCTION] Removing access to *%s* to project *%s*...' % (user, project)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    def do_list_projects(self, data):
        try:
            user = data.split(CMD_SEP)[1:][0]
            user = user[user.index('|'):user.index('>')][1:]
            output = 'None'
            if user.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                output = integrates_dao.get_projects_by_user(user)
                output = "\n".join([x[0] + ": " + x[1] for x in output])
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    def do_list_users(self, data):
        try:
            project = data.split(CMD_SEP)[1:][0]
            output = 'None'
            if project.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                output = integrates_dao.get_project_users(project)
                output = "\n".join([x[0] for x in output])
        except ValueError:
            output = "That's not something I can do yet, human."
        return output
# pylint: disable=W0613
    def handle(self, *args, **kwargs):
        READ_WEBSOCKET_DELAY = 1
        self.slack_client = slackclient.SlackClient(settings.SLACK_BOT_TOKEN)
        if self.slack_client.rtm_connect():
            try:
                print("FLUIDIntegrates connected and running!")
                start_msg = "FLUIDIntegrates admin bot now available."
                self.slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                      text=start_msg, as_user=True)
                while True:
                    command, channel = self.parse_slack_output(self.slack_client.rtm_read())
                    if command and channel:
                        self.handle_command(command, channel)
                    time.sleep(READ_WEBSOCKET_DELAY)
            except KeyboardInterrupt:
                bye_msg = "FLUIDIntegrates admin bot has disconnected."
                self.slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                      text=bye_msg, as_user=True)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
