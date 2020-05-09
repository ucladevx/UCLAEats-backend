import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room
from .push_notifications import PushClient

log = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        # Retrieve from URL
        self.room_label = self.scope["url_route"]["kwargs"]["room_label"]
        self.room_group_name = f'chat-{self.room_label}'

        log.debug('websocket connecting')

        try:
            room = Room.objects.get(label=self.room_label)
        except Room.DoesNotExist:
            log.debug('room not found=%s', self.room_label)
            return

        log.debug('chat connect room=%s client=%s:%s', room.label, event['client'][0], event['client'][1])

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        log.debug('%s room connected', room.label)

    async def websocket_receive(self, event):
        # Look up the room from the channel session, bailing if it doesn't exist
        try:
            room = Room.objects.get(label=self.room_label)
        except Room.DoesNotExist:
            log.debug('received message, but room does not exist label=%s', self.room_label)
            return

        # Parse out a chat message from the content text, bailing if it doesn't
        # conform to the expected message format.
        try:
            data = json.loads(event['text'])
        except ValueError:
            log.debug("ws message isn't json text=%s", data)
            return

        if set(data.keys()) != set(('handle', 'message')):
            log.debug("ws message unexpected format data=%s", data)
            return

        if data:
            log.debug('chat message room=%s handle=%s message=%s', room.label, data['handle'], data['message'])

            m = room.messages.create(**data)

            await self.channel_layer.group_send(self.room_group_name, {'text': json.dumps(m.as_dict())})

            log.debug("Chat received and added successfully.")
            user_device_id = room.user1.device_id if not str(room.user1.id) == str(data['handle']) else room.user2.device_id
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" + str(user_device_id) + "Len = " + str(len(str(user_device_id))))

            # Push notification to receiver
            try:
                pc = PushClient()
                message_body = data["message"]
                sender = room.user1.first_name if str(room.user1.id) == str(data['handle']) else room.user2.first_name
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" + sender)
                message = {'APNS':json.dumps({'aps':{'alert': {'body': message_body, 'title': sender} }})}
                #message =message_body
                message_structure = 'json'
                log.debug("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" + str(json.dumps(message)))     
                message_id = pc.send_apn(device_token=user_device_id, MessageStructure=message_structure, message=message)
            except:
                pass

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
