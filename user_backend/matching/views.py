from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.http import Http404
from django.conf import settings

from matching.models import WaitingUser
from matching.serializers import WaitingUserSerializer



class MatchingService(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        serializer = WaitingUserSerializer(data=request.data)
        if serializer.is_valid():
            waiting_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
