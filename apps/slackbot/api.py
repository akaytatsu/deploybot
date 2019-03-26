from django.conf import settings
from apps.core.api import get_type_conversation, get_answer_for_type

def request_process(event, client):
    type_conversation = None

    if not event.get("type") == "message":
        return

    if not event.get("channel") == settings.SLACK_CHANNEL_ID:
        client.rtm_send_message(
            event['channel'],
            "Olha, não quero ser mal educado, mas só posso atender pelo canal <#{}>".format(settings.SLACK_CHANNEL_ID)
        )

        return

    if event.get("text", None):
        type_conversation = get_type_conversation(event['text'])

    if type_conversation is None:
        pass
    else:
        answer_user, answer_log = get_answer_for_type(type_conversation, term=event['text'], message_user_id=event['user'])

        client.rtm_send_message(
            event['channel'],
            answer_user
        )

        if answer_user and settings.SLACK_DEPLOY_CHANNEL_ID != "":
            client.rtm_send_message(
                settings.SLACK_DEPLOY_CHANNEL_ID,
                answer_log
            )