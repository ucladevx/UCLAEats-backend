import random
import string
import json
import sys
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import haikunator
from .models import Room
from chat.push_notifications import PushClient

def about(request):
    return render(request, "chat/about.html")

def new_random_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)


#@csrf_protect
"""
def new_room(request):

    #Create a new room based on the user ids.
    #The request json should contain user1 and user2 fields (with User ids)
    print("NEW ROOM CALLED!\n\n\n\n\n\n")

    # Read user1, user2 info from GET headers
    user1, user2 = request.GET['user1_id'], request.GET['user2_id']
    #device1, device2 = request.GET['user1_device_id'], \
            #request.GET['user2_device_id']
    #user1, user2 = request.POST['user1'], request.POST['user2']
    user1, user2 = min(user1, user2), max(user1, user2)
    label = user1 + '_' + user2
    print("{} label is created.".format(label))
    # TODO: Encrypt the label
    if not Room.objects.filter(label=label).exists():
        new_room = None
        while not new_room:
            # Creates chat rooms with that list of users
            with transaction.atomic():
                users = {"user1" : user1, "user2": user2}
                new_room = Room.objects.create(label=label, users=json.dumps(users))
                print("{} label is created2222.".format(label))

    # Need to Encrypt the label
    responseData = {
        "label": label
    }

    print("New Label Sent")

    return JsonResponse(responseData)
"""
#@csrf_protect
def new_room(request):

    if request.method != 'POST':
        return


    print(request.body, file=sys.stderr)
    payload = json.loads(request.body)
    user1_id, user2_id = payload["user1_id"], payload["user2_id"]
    user1_id, user2_id = min(user1_id, user2_id), max(user1_id, user2_id)

    user1_device_id, user2_device_id = payload["user1_device_id"], \
                payload["user2_device_id"]

    label = str(user1_id) + '_' + str(user2_id)

    print("{} label is created.".format(label))
    # TODO: Encrypt the label
    if not Room.objects.filter(label=label).exists():
        new_room = None
        while not new_room:
            # Creates chat rooms with that list of users
            with transaction.atomic():
                users = {"user1_id" : user1_id, "user2_id": user2_id, "user1_device_id": user1_device_id, "user2_device_id": user2_device_id}
                new_room = Room.objects.create(label=label,  users=json.dumps(users))
                print("{} label is created2222.".format(label))

    responseData = {
        "label" : label
    }

    try:
        message = "Matched! Head to the chat!"
        #   Push Notification to both parties
        pc = PushClient()
        message_id_1 = pc.send_apn(device_token=user1_device_id, message=message)
        message_id_2 = pc.send_apn(device_token=user2_device_id, message=message)
    except:
        pass

    return JsonResponse(responseData)


def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """

    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    print("THE NEW VIEW IS CALLED!!!!\n\n\n\n\n")
    room, created = Room.objects.get_or_create(label=label)

    #  Sanity check to check as to who sent the message
    #  The frontend will need to send a user_id with their GET request
    """
    room_user_info = json.loads(room.users)
    sender_id = request.GET["user_id"]


    if sender_id != room_user_info["user1_id"] and sender_id != room_user_info["user2_id"]:
        error_message = {
            "error": "You are not authorized to download these messages."
        }
        return JsonResponse(error_message)
    """

    # We want to show the last 50 messages, ordered most-recent-last
    messages = room.messages.order_by('-timestamp')[:50]
    extractedMessages = []
    for message in messages:
        messageDict = {
            "timestamp": message.timestamp,
            "handle": message.handle,
            "message": message.message
        }
        extractedMessages.append(messageDict)

    responseData = {
        'tester': "BRUIN BITE",
        'messages': extractedMessages
    }

    return JsonResponse(responseData)


    #return render(request, "chat/room.html", {
    #    'room': label,
    #   'messages': messages,
    #})

def push_notification(request):
    pc = PushClient()
    device_token = request.GET['device_token']
    # message = request.GET['message']
    apns_dict = {
        "aps": {
            "mutable-content": 1,
            "alert": request.GET['message'],
        }
    }
    message = {
        "default": "default",
        "APNS_SANDBOX": json.dumps(apns_dict),
    }
    message_id = pc.send_apn(device_token=device_token, MessageStructure="json",
            message=message)
    return JsonResponse({"message_id": message_id})
