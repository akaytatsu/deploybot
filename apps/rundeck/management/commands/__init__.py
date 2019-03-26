from slackclient import SlackClient
from django.core.management.base import BaseCommand
import time
from django.conf import settings

class Command(BaseCommand):
    help = 'Start bot for listen'
def start_listening(self):
    client = SlackClient(settings.sla)
    if client.rtm_connect():
        while True:
            events = client.rtm_read()
            for event in events:
                if event['type']=='message' and event['text']=='hi':
                    client.rtm_send_message(
                        event['channel'],
                        "Hello World!"
                    )
            time.sleep(1)
