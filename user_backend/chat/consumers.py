import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room
# from chat.push_notifications import PushClient

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        api, version, mess, prefix, label = message['path'].strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return

        room,_ = Room.objects.get_or_create(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s', room.label, message['client'][0], message['client'][1])

    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label
    print(room.label)
    print("!!!!!______successful connection")
    message.reply_channel.send({'accept': True})

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    print("!!!!!MESSAGE RECIEVED!!!!!")
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)

    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, but room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        print(message['text'])
        data = json.loads(message['text'])

    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s',
            room.label, data['handle'], data['message'])
        m = room.messages.create(**data)

        # See above for the note about Group
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})


        receiver_device_id = 0;
        user_info = json.loads(room.users)

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


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
