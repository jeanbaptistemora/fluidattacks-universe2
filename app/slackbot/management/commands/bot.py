"""FLUIDIntegrates admin bot."""

import logging
import logging.config
import time
import slackclient
from django.core.management.base import BaseCommand
from django.conf import settings

from __init__ import FI_SLACK_BOT_ID

# Constants
AT_BOT = '<@{}>'.format(FI_SLACK_BOT_ID)
BOT_NAME = 'integrates'
CMD_SEP = ' '
CHANNEL = 'fluidintegrates'

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Class Command."""

    COMMANDS_FUNCTIONS = {
    }

    COMMANDS_HELP = {
    }

    help = 'Starts the admin bot'

    def __init__(self, *args, **kwargs):
        """Init Fluid Integrates Bot."""
        super(Command, self).__init__(*args, **kwargs)
        self.slack_client = None

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
