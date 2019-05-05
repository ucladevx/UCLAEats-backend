import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room
from channels.auth import channel_session_user, channel_session_user_from_http
# from chat.push_notifications import PushClient


from .auth_token import rest_token_user

log = logging.getLogger(__name__)


# @channel_session_user_from_http
@channel_session_user
@rest_token_user
def ws_connect(message):
    """
    :param message:
    :return:
    """
    try:
        api, version, mess, prefix, label = message['path'].strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return

        # Find the chat room with that label and bail if it does not exist.
        try:
            room = Room.objects.get(label=label)
        except Room.DoesNotExist:
            return

        # While connecting to the socket, the client should send the chat room key.
        # Bail of it does not.
        # try:
        #     data = json.loads(message['text'])
        # except ValueError:
        #     log.debug("ws message isn't json text=%s", data)
        #     return

        # Bail if the provided key does not match the room key
        # if room.key != data['key']:
        #     return

    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return

    log.debug('chat connect room=%s client=%s:%s', room.label, message['client'][0], message['client'][1])
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    log.debug("{} room connected".format(room.label))

    message.channel_session['room'] = room.label
    message.reply_channel.send({'accept': True})


@channel_session_user
def ws_receive(message):
    """
    :param message:
    :return:
    """


    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)

    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('received message, but room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])

    except ValueError:
        log.debug("ws message isn't json text=%s", data)
        return

    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s',
                  room.label, data['handle'], data['message'])

        m = room.messages.create(**data)

        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

        log.debug("Chat received and added successfully.")

        # receiver_device_id = 0;
        # user_info = json.loads(room.users)
        # if int(data["handle"]) == user_info["user1_id"]:
        #     receiver_device_id = user_info["user2_device_id"]
        # else:
        #     receiver_device_id = user_info["user1_device_id"]
        # Push Notification to receiver
        # try:
        #     pc = PushClient()
        #     message = data["message"][:10]
        #     message_id = pc.send_apn(device_token=receiver_device_id, message=message)
        # except:
        #     pass


@channel_session_user
def ws_disconnect(message):
    """
    :param message:
    :return:
    """
    try:
        label = message.channel_session['room']
        _ = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
