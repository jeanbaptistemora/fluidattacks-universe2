"""FLUIDIntegrates admin bot."""

import logging
import logging.config
import time
import re
import slackclient
from django.core.management.base import BaseCommand
from django.conf import settings
from app import util

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
        'invalidate_cache': do_invalidate_cache
    }

    COMMANDS_HELP = {
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
                ', '.join(list(self.COMMANDS_FUNCTIONS.keys())) +\
                '* commands, delimited by spaces: \n'
            response += '\n'.join('{} {}'.format(k, v)
                                  for k, v in list(self.COMMANDS_HELP.items()))
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
