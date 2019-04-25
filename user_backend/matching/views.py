from rest_framework import status as s
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.http import Http404
from django.conf import settings
from django.db.models import Q

from matching.models import WaitingUser, MatchedUsers
from matching.serializers import WaitingUserSerializer, MatchedUsersSerializer
from .match import *
from .model_constants import *
import requests
from datetime import datetime
import dateutil.parser

def convert_time(t):
    return dateutil.parser.parse(t).strftime('%Y-%m-%d %H:%M:%S')

def format_matcheduser(data):
    data['meal_datetime'] = convert_time(data['meal_datetime'])
    return data

def format_waitinguser(data):
    data['meal_times'] = list(map(convert_time, data['meal_times']))
    data['date_updated'] = convert_time(data['date_updated'])
    return data

class WaitingService(APIView):
    #authentication_classes = ()
    permission_classes = ()

    #get all requests of status
    def get(self, request, format=None):
        statuses = request.GET.getlist('status')

        query = Q(user=request.GET.get('user_id'))
        query.add(Q(status__in=statuses), Q.AND)
        
        matched = WaitingUser.objects.filter(query)
        serializer = WaitingUserSerializer(matched, many=True)
        data = list(map(format_waitinguser, serializer.data))
        return Response(data, status=s.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = WaitingUserSerializer(data=request.data)

        if serializer.is_valid():
            #check for unique (user,meal_day,meal_period)
            duplicate_requests = WaitingUser.objects.filter(
                Q(user=request.data['user']),
                Q(meal_period=request.data['meal_period']),
                Q(meal_day=request.data['meal_day']),
                Q(status=PENDING)|Q(status=SUCCESS)
            )

            if duplicate_requests:
                return Response({"error": "duplicate request"}, 
                    status=s.HTTP_400_BAD_REQUEST)

            waiting_user = serializer.save()
            attempt_match(waiting_user)
            data = format_waitinguser(serializer.data)
            return Response(data, status=s.HTTP_201_CREATED)
        return Response(serializer.errors, status=s.HTTP_400_BAD_REQUEST)


class MatchingService(APIView):
    #authentication_classes = ()
    permission_classes = ()

    #get all matches
    def get(self, request, format=None):
        user_id = request.GET.get('id')
        matched_users = MatchedUsers.objects.filter(user1=user_id)
        serializer = MatchedUsersSerializer(matched_users, many=True)
        data = list(map(format_matcheduser, serializer.data))
        return Response(data, status=s.HTTP_200_OK)

    #TODO: get match on chat_url
    #examine postgres

    #delete MatchedUsers record, update status of both WaitingUser records to CANCELLED
    def delete(self, request, format=None):
        to_delete = MatchedUsers.objects.filter(chat_url=request.GET.get('chat_url'))
        if not to_delete:
            return Response({"error": "match with chat_url not found"}, status=s.HTTP_400_BAD_REQUEST)

        #update status to 'cancelled' on original request records
        for t_d in to_delete:
            WaitingUser.objects.filter(user=t_d.user1,meal_day=t_d.meal_datetime,meal_period=t_d.meal_period).update(status=CANCELLED)

        to_delete.delete()

        response = requests.delete(
            'http://daphne:8888/api/v1/messaging/messages/' + request.GET.get('chat_url'))

        if response.status_code == 200:
            return Response({"status":"success"},status=s.HTTP_200_OK)
        else:
            return Response({
                "error":"status code " + response.status_code + " from deleting chat room"},
                status=s.HTTP_400_BAD_REQUEST)

class MatchByURLService(APIView):
    #authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        chat_url = request.GET.get('chat_url')
        user = request.GET.get('user')
        matched_users = MatchedUsers.objects.filter(chat_url=chat_url, user1=user)
        serializer = MatchedUsersSerializer(matched_users, many=True)
        data = list(map(format_matcheduser, serializer.data))
        return Response(data, status=s.HTTP_200_OK)

class StatusService(APIView):
    #authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        wait_id = int(request.GET.get('id'))
        waiting_user = WaitingUser.objects.get(id=wait_id)
        return Response({"status": waiting_user.status},
            status=s.HTTP_200_OK)





