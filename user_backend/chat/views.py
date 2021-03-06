import json
import logging
import secrets
import sys

from chat.push_notifications import PushClient
from django.db import transaction
from django.http import Http404, JsonResponse
from rest_framework.decorators import (action, api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.views import APIView
from users.models import User

from .models import Room

log = logging.getLogger(__name__)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def new_chat_room(request):
    """
    :param request:
    :return:
    """

    payload = json.loads(request.body)
    user1_id, user2_id = payload["user1_id"], payload["user2_id"]
    user1_device_id, user2_device_id = payload["user1_device_id"], payload["user2_device_id"]
    
    user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)
    
    # user1_device_id, user2_device_id = payload["user1_device_id"], payload["user2_device_id"]
    
    label = str(user1_id) + '_' + str(user2_id)
    
    log.debug('The label for the new room created is: ' + label)
    
    if not Room.objects.filter(label=label).exists():
        new_room = None
        while not new_room:
            # Creates chat rooms with that list of users
            with transaction.atomic():
                users = {
                    "user1_id": user1_id,
                    "user2_id": user2_id
                }
                room_key = secrets.token_urlsafe(16)
    
                # No try-catch since assuming the matcher always sends correct ids
    
                user1 = User.objects.get(id=user1_id)
                user2 = User.objects.get(id=user2_id)
                new_room = Room.objects.create(label=label, users=json.dumps(users), key=room_key, user1=user1, user2=user2)
    
    try:
        title = "Matched!"
        message_body = "View your matches to see who you're eating with!"
        message = {'APNS':json.dumps({'aps':{'alert': {'body': message_body, 'title': title} }})}
        message_structure = 'json'
        
        # pc = PushClient()
        # if not len(str(user1_device_id)) == 0:
        #     message_id_1 = pc.send_apn(device_token=user1_device_id, MessageStructure=message_structure, message=message)
        # if not len(str(user2_device_id)) == 0:
        #     message_id_2 = pc.send_apn(device_token=user2_device_id, MessageStructure=message_structure, message=message)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong', 'label': label})
    response_data = {"label": label}
    return JsonResponse(response_data)


# The following two end points use default authentication and permission classes.

@api_view(['GET'])
def messages(request, label):
    """
    :param request:
    :param label:
    :return:
    """

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


@api_view(['GET'])
def key(request, label):

    """
    :param request: HTTP GET request
    :param label: The unique label of the chat room
    :return: The unique key associated with the chat room
    """

    try:
        room = Room.objects.get(label=label)
    except Room.DoesNotExist:
        raise Http404

    room_key = room.key

    response_dict = {
        "key": room_key
    }

    return JsonResponse(response_dict)


# TODO: Put this in push_notif_utils.py file
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
