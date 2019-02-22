import json
import sys

from django.db import transaction
from django.http import Http404
from django.http import JsonResponse

from rest_framework.views import APIView

from .models import Room
# from chat.push_notifications import PushClient




class UserChatView(APIView):

    # authentication_classes = ()
    # permission_classes = ()

    #@staticmethod
    def post(self, request):

        print(request)

        # if request.method != 'POST':
        #     return

        print(request.body, file=sys.stderr)
        payload = json.loads(request.body)
        user1_id, user2_id = payload["user1_id"], payload["user2_id"]
        user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)

        # user1_device_id, user2_device_id = payload["user1_device_id"], payload["user2_device_id"]

        label = str(user1_id) + '_' + str(user2_id)

        # TODO: Encrypt the label
        if not Room.objects.filter(label=label).exists():
            new_room = None
            while not new_room:
                # Creates chat rooms with that list of users
                with transaction.atomic():
                    users = {"user1_id" : user1_id, "user2_id": user2_id}  #"user1_device_id": user1_device_id, "user2_device_id": user2_device_id}
                    new_room = Room.objects.create(label=label,  users=json.dumps(users))
                    print("{} label is created2222.".format(label))

        response_data = {
            "label": label
        }

        # try:
        #     message = "Matched! Head to the chat!"
        #     #   Push Notification to both parties
        #     pc = PushClient()
        #     message_id_1 = pc.send_apn(device_token=user1_device_id, message=message)
        #     message_id_2 = pc.send_apn(device_token=user2_device_id, message=message)
        # except:
        #     pass

        return JsonResponse(response_data)

    # @staticmethod
    def get(self, request, label):
        """
        Room view - show the room, with latest messages.
        """
        # If the room with the given label doesn't exist, automatically create it
        # upon first visit (a la etherpad).

        try:
            room = Room.objects.get(label=label)
        except Room.DoesNotExist:
            raise Http404

        # We want to show the last 50 messages, ordered most-recent-last
        messages = room.messages.order_by('-timestamp')[:50]
        extracted_messages = []
        for message in messages:
            message_dict = {
                "timestamp": message.timestamp,
                "handle": message.handle,
                "message": message.message
            }
            extracted_messages.append(message_dict)

        response_data = {
            'tester': "BRUIN BITE",
            'messages': extracted_messages
        }

        return JsonResponse(response_data)

    # def push_notification(request):
    #     pc = PushClient()
    #     device_token = request.GET['device_token']
    #     # message = request.GET['message']
    #     apns_dict = {
    #         "aps": {
    #             "mutable-content": 1,
    #             "alert": request.GET['message'],
    #         }
    #     }
    #     message = {
    #         "default": "default",
    #         "APNS_SANDBOX": json.dumps(apns_dict),
    #     }
    #     message_id = pc.send_apn(device_token=device_token, MessageStructure="json",
    #             message=message)
    #     return JsonResponse({"message_id": message_id})
