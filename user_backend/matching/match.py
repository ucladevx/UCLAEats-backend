from matching.models import WaitingUser
from matching.serializers import WaitingUserSerializer, MatchedUsersSerializer
from users.models import User
import sys
import requests
import json
from .model_constants import *

def attempt_match(waiting_user):
    if waiting_user.status != PENDING:
        print("Attempted match on nonpending request")
        return

    users = WaitingUser.objects.filter(status=PENDING) \
        .filter(meal_day=waiting_user.meal_day) \
        .filter(meal_period=waiting_user.meal_period)

    for user in users:
        if user.user_id != waiting_user.user_id:
            common_dining_halls = list(set(user.dining_halls)
                .intersection(set(waiting_user.dining_halls)))
            if len(common_dining_halls) == 0:
                continue
            common_times = list(set(user.meal_times)
                    .intersection(set(waiting_user.meal_times)))
            if len(common_times) == 0:
                continue

            chat_url = create_chat_room(waiting_user.user_id, user.user_id)
            # Terribly choose the first time and dining hall
            user1 = User.objects.get(pk=waiting_user.user_id)
            user2 = User.objects.get(pk=user.user_id)
            matched_users_data = {
                "user1" : user1.id,
                "user1_first_name": user1.first_name,
                "user1_last_name": user1.last_name,
                "user2" : user2.id,
                "user2_first_name": user2.first_name,
                "user2_last_name": user2.last_name,
                "meal_datetime" : common_times[0],
                "meal_period" : waiting_user.meal_period,
                "dining_hall" : common_dining_halls[0],
                "chat_url": chat_url,
            }

            serializer1 = MatchedUsersSerializer(data=matched_users_data)
            if serializer1.is_valid():
                serializer1.save()
                # pass this point, they have a match
                user.status = SUCCESS
                waiting_user.status = SUCCESS
                user.save()
                waiting_user.save()
                # Send request to match making through messenger

                # swap the users, and resave
                matched_users_data["user1"], matched_users_data["user2"] = \
                        matched_users_data["user2"], matched_users_data["user1"]
                matched_users_data["user1_first_name"], matched_users_data["user2_first_name"] = \
                        matched_users_data["user2_first_name"], matched_users_data["user1_first_name"]
                matched_users_data["user1_last_name"], matched_users_data["user2_last_name"] = \
                        matched_users_data["user2_last_name"], matched_users_data["user1_last_name"]
                serializer2 = MatchedUsersSerializer(data=matched_users_data)
                if serializer2.is_valid():
                    serializer2.save()
            else:
                print("Serializer Not Valid", serializer.errors)
            return 

def create_chat_room(user1_id, user2_id):
    payload = {
        'user1_id' : user1_id,
        'user1_device_id' : User.objects.get(pk=user1_id).device_id,
        'user2_id' : user2_id,
        'user2_device_id' : User.objects.get(pk=user2_id).device_id,
    }
    response = requests.post(
            'http://daphne:8888/api/v1/messaging/messages/new/dedicated/', 
	    data=json.dumps(payload))
    return response.json()['label']

