from slackclient import SlackClient
from django.core.management.base import BaseCommand
import time
from django.conf import settings
from apps.slackbot.api import request_process

class Command(BaseCommand):
    help = 'Start bot for listen'

    def handle(self, *args, **kwargs):
        print("Started listener event")
        client = SlackClient(settings.SLACK_BOT_TOKEN)
        if client.rtm_connect():
            while True:
                events = client.rtm_read()
                for event in events:
                    request_process(event, client)
                time.sleep(1)
