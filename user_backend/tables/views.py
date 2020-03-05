import json
import logging

from django.db.models.functions import Now
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes

from .models import DiningTable

log = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_table(request):
    """
    Example JSON Request:
    { "dining_hall": "F",
      "meal_period": "BR",
      "creator_id": 3
    }
    """
    try:
        payload = json.loads(request.body)
        dining_hall = payload["dining_hall"]
        datetime = Now() #change later
        meal = payload["meal_period"]
        creator = payload["creator_id"]
    except Exception as e:
        return JsonResponse({'error': 'Invalid JSON request - required fields: dining_hall, datetime, meal, creator'})

    new_room = DiningTable.objects.create(dining_hall=dining_hall, datetime=datetime, users=[creator], meal_period=meal, creator_id=creator)

    response = "Created new table at " + new_room.get_dining_hall_display() + " with ID " + str(new_room.id)
    log.debug("[TABLES] " + response)
    response_data = {"Success": response}
    return JsonResponse(response_data)



@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def join_table(request):
    try:
        payload = json.loads(request.body)
        table_id = payload["table_id"]
        user_id = payload["user_id"]
    except Exception as e:
        return JsonResponse({'error': 'Invalid JSON request - required fields: table_id, user_id'})

    try:
        table = DiningTable.objects.get(pk=table_id)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong locating table'})

    if user_id in table.users:
        return JsonResponse({'error': "User is already part of table"})

    table.users.append(user_id)
    table.save()

    #TODO: send push notification/message to group

    response = "User with id " + str(user_id) + " added to table with id " + str(table_id)
    log.debug("[TABLES] " + response)
    response_data = {"Success": response}
    return JsonResponse(response_data)


@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def leave_table(request):
    try:
        payload = json.loads(request.body)
        table_id = payload["table_id"]
        user_id = payload["user_id"]
    except Exception as e:
        return JsonResponse({'error': 'Invalid JSON request - required fields: table_id, user_id'})

    try:
        table = DiningTable.objects.get(pk=table_id)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong locating table'})

    if user_id not in table.users:
        return JsonResponse({'error': "User not part of table"})

    table.users.remove(user_id)
    table.save()

    #TODO: send push notification/message to group

    response = "User with id " + str(user_id) + " removed from table with id " + str(table_id)
    log.debug("[TABLES] " + response)
    response_data = {"Success": response}
    return JsonResponse(response_data)


