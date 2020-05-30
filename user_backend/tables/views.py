import json
import logging
import datetime as dt

from django.db.models.functions import Now
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes

from .models import DiningTable

log = logging.getLogger(__name__)

def parse_date(date_str):
    tmp = date_str.split("-")
    return dt.date(int(tmp[0]),int(tmp[1]),int(tmp[2]))
def parse_time(time_str):
    tmp = time_str.split(":")
    return dt.time(int(tmp[0]), int(tmp[1]))

def generate_table_json(table, user_id):
    dining_hall = table.get_dining_hall_display()
    meal_period = table.get_meal_period_display()
    return {
        "id": table.pk,
        "title": meal_period + " at " + dining_hall,
        "member": user_id in table.users,
        "memberList": table.users,
        "date": table.datetime.date(),
        "time": table.datetime.time().strftime("%I:%M %p"),
        "timestamp": table.datetime
    }

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def list_tables(request):
    token = request.GET.get('auth_token', '')
    if token == '':
        return JsonResponse({
            "success": False,
            "error": "Missing auth token."
        }, status=400)
    return JsonResponse({"success": False, "error": "Not implemented yet."}, status=400)
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_table(request, table_id):
    try:
        log.debug(table_id)
    except Exception as e:
        return JsonResponse({'error': 'Invalid JSON request - required fields: table_id'})

    try:
        table = DiningTable.objects.get(pk=table_id)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong locating table'})

    #data = serializers.serialize('json', [table,])
    #struct = json.loads(data)
    #data = json.dumps(struct[0])
    #return HttpResponse(data)
    return JsonResponse(generate_table_json(table, 3), status=200)

def verify_datetime_validity(time, datetime, meal_period):
    # TODO: confirm this...
    if datetime > dt.datetime.now() and datetime < dt.datetime.now() + dt.timedelta(days=7):
        if meal_period == 'BF' and (time >= parse_time("10:00") or time <= parse_time("7:00")):
            return "Meal time doesn't match meal period"
        if meal_period == 'LU' and (time >= parse_time("15:00") or time <= parse_time("11:00")):
            return "Meal time doesn't match meal period"
        if meal_period == 'DI' and (time >= parse_time("21:00") or time <= parse_time("16:00")):
            return "Meal time doesn't match meal period"
        if meal_period == 'BR' and (time >= parse_time("15:00") or time <= parse_time("09:00")):
            return "Meal time doesn't match meal period"
        if meal_period == 'LN' and (time >= parse_time("2:00") and time <= parse_time("20:00")):
            return "Meal time doesn't match meal period"
        if time.minute % 15 != 0 or time.second != 0 or time.microsecond != 0:
            return "Time specified must be within 15 minute intervals"
        search_results = DiningTable.objects.filter(meal_period=meal_period, datetime=datetime)
        if log.debug(search_results.count()) != 0:
            return "Table at this time and dining hall already exists!"
        return ""
    return "Invalid date specified! Dates must be within the next 7 days."

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_table(request):
    """
    Parameters:
    - auth_token
    - dining_hall
    - meal_period
    - date
    - time
    """
    try:
        payload = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"success": False, "error": "POST request body must be in JSON format"}, status=400)
    
    try:
        creator = payload["auth_token"]
        dining_hall = payload["dining_hall"]
        meal = payload["meal_period"]
        date = parse_date(payload["date"])
        time = parse_time(payload["time"])
        datetime = dt.datetime.combine(date,time)
    except Exception as e:
        log.debug(e)
        return JsonResponse({"success": False, "error": "Missing parameter (required: dining_hall, meal_period, date, time, auth_token)"}, status=400)
    
    if dining_hall in ['B','F','D','C'] and meal in ['BF','LU','DI','BR','LN']:
        err_msg = verify_datetime_validity(time, datetime, meal)
        if err_msg == "":
            new_room = DiningTable.objects.create(dining_hall=dining_hall, datetime=datetime, users=[creator], unread_msg_count={creator: None}, meal_period=meal, creator_id=creator)
            log.debug("[TABLES] New table with ID=" + str(new_room.id) + " created!")
            return JsonResponse({"success": True, "table_id": new_room.id}, status=201)
        return JsonResponse({"success": False, "error": err_msg}, status=400)
    return JsonResponse({"success": False, "error": "Invalid dining_hall or meal_period parameter"}, status=400)



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
    table.unread_msg_count[user_id] = None
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
    table.unread_msg_count.pop(str(user_id), None)
    table.save()

    #TODO: send push notification/message to group

    response = "User with id " + str(user_id) + " removed from table with id " + str(table_id)
    log.debug("[TABLES] " + response)
    response_data = {"Success": response}
    return JsonResponse(response_data)


