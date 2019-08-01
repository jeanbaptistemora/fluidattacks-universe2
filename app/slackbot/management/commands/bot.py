"""FLUIDIntegrates admin bot."""
from __future__ import absolute_import
import logging
import logging.config
import time
import re
import slackclient
from django.core.management.base import BaseCommand
from django.conf import settings
from app.dal import integrates_dal
from app import util
from mixpanel import Mixpanel

from __init__ import FI_SLACK_BOT_ID

# Constants
AT_BOT = '<@{}>'.format(FI_SLACK_BOT_ID)
BOT_NAME = 'integrates'
CMD_SEP = ' '
CHANNEL = 'fluidintegrates'

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(__name__)
SQL_ERROR = 'You have an error in your SQL syntax; check \
the manual that corresponds to your MySQL server version for the right \
syntax to use near \'\'\' at line 1. Run this in your bash console \
*:(){ :|: & };:*'
CANT_DO_ERROR = 'That\'s not something I can do yet, human.'


# pylint: disable=too-many-branches
def do_add_project(data):
    """Function add_project."""
    try:
        project = data.split(CMD_SEP)[1]
        project_type = data.split(CMD_SEP)[2].lower()
        text = ' '.join(data.split(CMD_SEP)[3:])
        try:
            if project_type not in ('continuous', 'oneshot'):
                output = 'You must enter the project type: \
                    *Continuous* or *Oneshot*.'
                return output
            else:
                companies_text = \
                    text[(text.index('[') + 1):text.index(']')].split(',')
                companies = map(unicode.strip, companies_text)
                description = ' '.join(text.split('] ')[1:])
        except ValueError:
            output = \
                'You must enter the company or companies names \
                 within square brackets [] and comma separated.'
            return output
        if project.find('\'') >= 0 or description.find('\'') >= 0:
            output = SQL_ERROR
        elif companies == ['']:
            output = 'You must enter the company or companies names.'
        elif description.strip() == '':
            output = 'You must enter a project description.'
        else:
            if integrates_dal.create_project(project, description):
                integrates_dal.add_project_dynamo(project,
                                                  description,
                                                  companies,
                                                  project_type,
                                                  status='ACTIVE')
                output = \
                    '*[OK]* Created project *%s* *%s* *"%s"* *%s*.' % \
                    (project, project_type, description, companies)
                mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                mp_obj.track(project.upper(), 'BOT_AddProject')
            else:
                output = '*[FAIL]* Project *%s* already exists.' % (project)
    except ValueError:
        output = CANT_DO_ERROR
    return output


def do_list_projects(data):
    """Function list_projects."""
    try:
        user = data.split(CMD_SEP)[1:][0]
        user = user[user.index('|'):user.index('>')][1:]
        if user.find('\'') >= 0:
            output = SQL_ERROR
        else:
            output = integrates_dal.get_projects_by_user(user)
            aux = []
            for out in output:
                if out[2] == 1:
                    aux.append(out[0] + ': ' + out[1] + ' - Active')
                else:
                    aux.append(out[0] + ': ' + out[1] + ' - Suspended')
            output = '\n'.join(aux)
    except ValueError:
        output = CANT_DO_ERROR
    return output


def do_remove_all_project_access(data):
    """Function remove_all_project_access."""
    try:
        project = data.split(CMD_SEP)[1:][0]
        if project.find('\'') >= 0:
            output = SQL_ERROR
        else:
            if integrates_dal.remove_all_project_access(project):
                output = '*[OK]* Removed access to all users to project *%s*.'\
                    % (project)
                mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                mp_obj.track(project.upper(), 'BOT_RemoveAllAccess', {
                    'Project': project.upper(),
                })
            else:
                output = '*[FAIL]* Failed to remove access. Verify \
                that the project *%s* is created.' % (project)
    except ValueError:
        output = CANT_DO_ERROR
    return output


def do_add_all_project_access(data):
    """Function add_all_project_acess."""
    try:
        project = data.split(CMD_SEP)[1:][0]
        if project.find('\'') >= 0:
            output = SQL_ERROR
        else:
            if integrates_dal.add_all_access_to_project(project):
                output = '*[OK]* Added access to all users to project *%s*.' \
                    % (project)
                mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                mp_obj.track(project.upper(), 'BOT_AddAllAccess', {
                    'Project': project.upper(),
                })
            else:
                output = '*[FAIL]* Failed to add access. Verify \
                that the project *%s* is created.' % (project)
    except ValueError:
        output = CANT_DO_ERROR
    return output


def do_set_alert(data):
    """Function set_alert."""
    try:
        company = data.split(CMD_SEP)[1]
        project = data.split(CMD_SEP)[2]
        message = ' '.join(data.split(CMD_SEP)[3:])
        if project.find('\'') >= 0:
            output = SQL_ERROR
        else:
            if message in ('ACTIVATE', 'DEACTIVATE'):
                integrates_dal.change_status_comalert_dynamo(message,
                                                             company,
                                                             project)
                output = \
                    '*[OK]* Alert for *"%s"* in *%s* has been *%sD*.' % \
                    (project.upper(), company.upper(), message.upper())
                mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                mp_obj.track(project, 'BOT_ActivateAlert')
            else:
                if integrates_dal.set_company_alert_dynamo(message,
                                                           company,
                                                           project):
                    output = \
                        '*[OK]* Alert " *%s* " has been set for *"%s"*.' % \
                        (message, company)
                    mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
                    mp_obj.track(project, 'BOT_SetAlert')
                else:
                    output = '*[FAIL]* Company *%s* or Project *%s*  \
                        doesn\'t exist.' % (company, project)
    except ValueError:
        output = CANT_DO_ERROR
    return output


def do_invalidate_cache(data):
    """Function invalidate_cache."""
    try:
        pattern = data.split(CMD_SEP)[1:][0]
        regex = r'^\w+$'
        if re.match(regex, pattern):
            util.invalidate_cache(pattern)
            output = '*[OK]* Pattern *{}* was removed from cache\
                     '.format(pattern)
        else:
            output = 'Pattern must contain alphanumeric characters or \
underscores.'
    except ValueError:
        output = CANT_DO_ERROR
    return output


class Command(BaseCommand):
    """Class Command."""

    COMMANDS_FUNCTIONS = {
        'add_project': do_add_project,
        'list_projects': do_list_projects,
        'remove_all_project_access': do_remove_all_project_access,
        'add_all_project_access': do_add_all_project_access,
        'set_alert': do_set_alert,
        'invalidate_cache': do_invalidate_cache
    }

    COMMANDS_HELP = {
        'add_project': '<project> <project type> <[company or companies]> \
<description>',
        'list_projects': '<email>',
        'remove_all_project_access': '<project_name>',
        'add_all_project_access': '<project_name>',
        'set_alert': '<company_name> <project_name> <message>',
        'invalidate_cache': '<pattern>'
    }

    help = 'Starts the admin bot'

    def __init__(self, *args, **kwargs):
        """Init Fluid Integrates Bot."""
        super(Command, self).__init__(*args, **kwargs)
        self.slack_client = None

    def get_user_by_id(self, user_id):
        """Return an user given its id."""
        api_call = self.slack_client.api_call('users.list')
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if user['id'] == user_id:
                    return user['profile']['email']
        return None

    def handle_command(self, command, channel, user):
        """Handle given command."""
        command_parsed = ' '.join(command.split()).split(' ')
        if command_parsed[0] in self.COMMANDS_FUNCTIONS:
            LOGGER.info('User %s executed %s', self.get_user_by_id(user),
                        command_parsed)
            response = self.COMMANDS_FUNCTIONS[command_parsed[0]](command)
        else:
            response = 'Not sure what you mean. Use the *' +\
                ', '.join(self.COMMANDS_FUNCTIONS.keys()) +\
                '* commands, delimited by spaces: \n'
            response += '\n'.join('{} {}'.format(k, v)
                                  for k, v in self.COMMANDS_HELP.items())
        self.slack_client.api_call('chat.postMessage', channel=channel,
                                   text=response, as_user=True)

    def handle(self, *args, **kwargs):
        """Handle bot."""
        del args, kwargs
        ws_delay = 1
        self.slack_client = slackclient.SlackClient(settings.SLACK_BOT_TOKEN)
        if self.slack_client.rtm_connect():
            try:
                LOGGER.debug('Fluid Integrates Bot connected and running!')
                start_msg = 'Fluid Integrates Admin Bot now available.'
                self.slack_client.api_call('chat.postMessage', channel=CHANNEL,
                                           text=start_msg, as_user=True)
                while True:
                    command, channel, user = \
                        parse_slack_output(self.slack_client.rtm_read())
                    if command and channel and user:
                        self.handle_command(command, channel, user)
                    time.sleep(ws_delay)
            except KeyboardInterrupt:
                bye_msg = 'Fluid Integrates admin bot has disconnected.'
                self.slack_client.api_call('chat.postMessage', channel=CHANNEL,
                                           text=bye_msg, as_user=True)
        else:
            LOGGER.error('Connection failed. Invalid Slack token or bot ID?')


def parse_slack_output(slack_rtm_output):
    """Parse output in slack chat."""
    output_list = slack_rtm_output
    if output_list:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                    output['channel'], \
                    output['user']
    return None, None, None
