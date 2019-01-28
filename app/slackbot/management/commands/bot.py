#
# FLUIDIntegrates admin bot
#

import logging
import logging.config
import time
import slackclient
from django.core.management.base import BaseCommand
from django.conf import settings
# pylint: disable=F0401
from app.dao import integrates_dao
from mixpanel import Mixpanel

# Constants
BOT_ID = 'U7H8PVATA'
AT_BOT = "<@" + BOT_ID + ">"
VALID_COMMANDS = ['add_project',
                  'unregister_user',
                  'list_projects',
                  'remove_all_project_access',
                  'add_all_project_access',
                  'set_alert']
BOT_NAME = 'integrates'
CMD_SEP = ' '
CHANNEL = 'fluidintegrates'

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Starts the admin bot'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.slack_client = None

    def get_user_by_id(self, user_id):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if user['id'] == user_id:
                    return user['profile']['email']

    def handle_command(self, command, channel, user):
        command_parsed = ' '.join(command.split()).split(' ')
        if command_parsed[0] in VALID_COMMANDS:
            response = "Running " + " ".join(command_parsed)
            # pylint: disable=W1201
            LOGGER.info('User %s executed %s' % (self.get_user_by_id(user),
                        " ".join(command_parsed),))
            if command_parsed[0] == 'add_project':
                response = do_add_project(command)
            elif command_parsed[0] == 'list_projects':
                response = self.do_list_projects(command)
            elif command_parsed[0] == 'remove_all_project_access':
                response = self.do_remove_all_project_access(command)
            elif command_parsed[0] == 'add_all_project_access':
                response = self.do_add_all_project_access(command)
            elif command_parsed[0] == 'set_alert':
                response = self.do_set_alert(command)

        else:
            response = "Not sure what you mean. Use the *" +\
                ", ".join(VALID_COMMANDS) + "* commands, delimited by spaces:"
            response += """
            add_project <project> <project type> <[company or companies]> <description>
            list_projects <email>
            remove_all_project_access <project_name>
            add_all_project_access <project_name>
            set_alert <company_name> <project_name> <message>
            """
        self.slack_client.api_call("chat.postMessage", channel=channel,
                                   text=response, as_user=True)

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
                aux = []
                for out in output:
                    if out[2] == 1:
                        aux.append(out[0] + ": " + out[1] + " - Active")
                    else:
                        aux.append(out[0] + ": " + out[1] + " - Suspended")
                output = "\n".join(aux)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    def do_remove_all_project_access(self, data):
        try:
            project = data.split(CMD_SEP)[1:][0]
            output = 'None'
            if project.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                if integrates_dao.remove_all_project_access_dao(project):
                    output = '*[OK]* Removed access to all users to project *%s*.' % (project)
                    mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                    mp_obj.track(project.upper(), 'BOT_RemoveAllAccess', {
                        'Project': project.upper(),
                    })
                else:
                    output = '*[FAIL]* Failed to remove access. Verify \
                    that the project *%s* is created.' % (project)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    def do_add_all_project_access(self, data):
        try:
            project = data.split(CMD_SEP)[1:][0]
            output = 'None'
            if project.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                if integrates_dao.add_all_access_to_project_dao(project):
                    output = '*[OK]* Added access to all users to project *%s*.' % (project)
                    mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                    mp_obj.track(project.upper(), 'BOT_AddAllAccess', {
                        'Project': project.upper(),
                    })
                else:
                    output = '*[FAIL]* Failed to add access. Verify \
                    that the project *%s* is created.' % (project)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    def do_set_alert(self, data):
        try:
            company = data.split(CMD_SEP)[1]
            project = data.split(CMD_SEP)[2]
            message = ' '.join(data.split(CMD_SEP)[3:])
            if project.find("'") >= 0:
                output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
            else:
                if message == 'ACTIVATE' or message == 'DEACTIVATE':
                    integrates_dao.change_status_comalert_dynamo(message, company, project)
                    output = \
                        '*[OK]* Alert for *"%s"* in *%s* has been *%sD*.' % \
                        (project.upper(), company.upper(), message.upper())
                    mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                    mp_obj.track(project, 'BOT_ActivateAlert')
                else:
                    if integrates_dao.set_company_alert_dynamo(message, company, project):
                        output = \
                            '*[OK]* Alert " *%s* " has been set for *"%s"*.' % \
                            (message, company)
                        mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                        mp_obj.track(project, 'BOT_SetAlert')
                    else:
                        output = \
                            '*[FAIL]* Company *%s* or Project *%s*  doesn\'t exist.' % \
                            (company, project)
        except ValueError:
            output = "That's not something I can do yet, human."
        return output

    # pylint: disable=W0613
    def handle(self, *args, **kwargs):
        ws_delay = 1
        self.slack_client = slackclient.SlackClient(settings.SLACK_BOT_TOKEN)
        if self.slack_client.rtm_connect():
            try:
                LOGGER.debug("FLUIDIntegrates connected and running!")
                start_msg = "FLUIDIntegrates admin bot now available."
                self.slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                           text=start_msg, as_user=True)
                while True:
                    command, channel, user = parse_slack_output(self.slack_client.rtm_read())
                    if command and channel and user:
                        self.handle_command(command, channel, user)
                    time.sleep(ws_delay)
            except KeyboardInterrupt:
                bye_msg = "FLUIDIntegrates admin bot has disconnected."
                self.slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                           text=bye_msg, as_user=True)
        else:
            LOGGER.error("Connection failed. Invalid Slack token or bot ID?")


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                    output['channel'], \
                    output['user']
    return None, None, None


# pylint: disable=too-many-branches
def do_add_project(data):
    try:
        project = data.split(CMD_SEP)[1]
        project_type = data.split(CMD_SEP)[2].lower()
        text = ' '.join(data.split(CMD_SEP)[3:])
        try:
            if project_type != "continuous" and project_type != "oneshot":
                output = 'You must enter the project type: *Continuous* or *Oneshot*.'
                return output
            else:
                companies_text = \
                    text[(text.index("[") + 1):text.index("]")].split(',')
                companies = map(unicode.strip, companies_text)
                description = ' '.join(text.split("] ")[1:])
        except ValueError:
            output = \
                "You must enter the company or \
companies names within square brackets [] and comma separated."
            return output
        if project.find("'") >= 0 or description.find("'") >= 0:
            output = """You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near ''' at line 1. Run this in your bash console \
*:(){ :|: & };:*"""
        elif companies == [""]:
            output = """You must enter the company or companies names."""
        elif description.strip() == "":
            output = """You must enter a project description."""
        else:
            if integrates_dao.create_project_dao(project, description):
                integrates_dao.add_project_dynamo(project, description, companies, project_type)
                output = \
                    '*[OK]* Created project *%s* *%s* *"%s"* *%s*.' % \
                    (project, project_type, description, companies)
                mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                mp_obj.track(project.upper(), 'BOT_AddProject')
            else:
                output = '*[FAIL]* Project *%s* already exists.' % (project)
    except ValueError:
        output = "That's not something I can do yet, human."
    return output
