from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.http import Http404
from django.conf import settings
from django.db.models import Q

from matching.models import WaitingUser, MatchedUsers
from matching.serializers import WaitingUserSerializer, MatchedUsersSerializer
from .match import *

class MatchingService(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        user_id = request.GET.get('id')
        matched_users = MatchedUsers.objects.filter(user1=user_id)
        serializer = MatchedUsersSerializer(matched_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = WaitingUserSerializer(data=request.data)
        if serializer.is_valid():
            waiting_user = serializer.save()
            attempt_match(waiting_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



